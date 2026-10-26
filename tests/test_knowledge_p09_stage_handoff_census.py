import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "knowledge/palaces/P09_career/gaps/P09_STAGE_HANDOFF_CENSUS_v0.1.json"
STATE = ROOT / "knowledge/states/P09_CAREER_STATE.yaml"
SOURCE_AUDIT = ROOT / "knowledge/wp07a/CAREER_888_CLOSURE_AUDIT_v0.1.json"
FINAL36 = ROOT / "knowledge/wp07a/CAREER_FINAL36_CLOSURE_v0.1.json"
CLOSURE = ROOT / "knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251_v0.16.json"
CENSUS = ROOT / "knowledge/wp08/CAREER_COMPILER_READINESS_CENSUS_26_v0.1.json"
GRAPH = ROOT / "knowledge/wp08/CAREER_ANTECEDENT_DEPENDENCY_GRAPH_65_v0.1.json"
RELATION = ROOT / "knowledge/palaces/P09_career/gaps/P09_RELATION_SCOPE_GAP_DISPOSITION_3_v0.1.json"
INHERITED = ROOT / "knowledge/palaces/P09_career/gaps/P09_INHERITED_DEPENDENCY_SOURCE_AUDIT_11_v0.1.json"

EXPECTED_INHERITED = {
    "CA01-058", "CA01-060", "CA02-108", "CA02-134", "CA02-157",
    "CA02-167", "CA02-168", "CA02-170", "CA02-171", "CA02-199", "CA03-235",
}
EXPECTED_RELATION = {"CA05-484", "CA06-582", "CA07-699"}
EXPECTED_DISPOSITIONS = {
    "STRUCTURE_PRESERVED_NO_PRODUCT_EXECUTION_CLAIM": 48,
    "SOURCE_REFINED_FAIL_CLOSED_NO_PRODUCT_EXECUTION_CLAIM": 44,
    "OPEN_CATEGORY_GENERIC_REFINED_FAIL_CLOSED_NO_PRODUCT_EXECUTION_CLAIM": 53,
    "THIRD_LAYER_CLASSIFIED_FAIL_CLOSED_NO_PRODUCT_EXECUTION_CLAIM": 92,
    "SOURCE_LOCAL_RESOLVED_NO_PRODUCT_EXECUTION_CLAIM": 2,
    "SOURCE_REPAIRED_FAIL_CLOSED_NO_PRODUCT_EXECUTION_CLAIM": 4,
    "KEEP_UNKNOWN_UNTIL_SOURCE_EXPLICIT": 1,
    "KEEP_UNKNOWN_OR_NO_UNIVERSAL_RULE_UNTIL_SOURCE_EXPLICIT": 2,
    "SOURCE_LOCAL_SEMANTICS_RESOLVED_NO_PRODUCT_EXECUTION_CLAIM": 3,
    "SOURCE_RECHECK_RESOLVED_NO_PRODUCT_EXECUTION_CLAIM": 1,
    "CONTEXTUAL_GROUP_ACTIVATION_PRESERVED_NO_DEFAULT": 1,
}


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_p09_handoff_census_reconciles_888_251_65_and_26_partitions():
    handoff = load(HANDOFF)
    audit = load(SOURCE_AUDIT)
    tail = load(FINAL36)
    closure = load(CLOSURE)
    census = load(CENSUS)
    graph = load(GRAPH)

    assert handoff["artifact_id"] == "KB-P09-STAGE-HANDOFF-CENSUS-EXPLICIT-RESIDUALS-v0.1"
    assert handoff["status"] == "SOURCE_AUDIT_COMPLETE_WITH_EXPLICIT_RESIDUALS"
    assert handoff["issue"] == 789
    assert handoff["decision"]["source_audit_stage"] == "COMPLETE_WITH_EXPLICIT_RESIDUALS"
    assert handoff["decision"]["next_palace"] == "P07"
    assert handoff["decision"]["next_issue"] == 669

    assert audit["canonical_source_rules"] == 888
    assert audit["structured_unique_ids_expected"] == 888
    assert audit["strict_review_disposition_rows"] + audit["pre_hundred_batch_specialized_structured_ids"] == 888
    assert audit["closure_claims"]["all_canonical_ids_have_structured_disposition"] is True
    assert audit["closure_claims"]["all_rules_executable"] is False
    assert tail["progress_counts"]["source_rules_rechecked"] == 36
    assert tail["progress_counts"]["canonical_source_reviewed_after"] == 888
    assert tail["progress_counts"]["new_production_executable_rules"] == 0

    assert closure["coverage"] == {"total": 251, "unique_source_rule_ids": 251, "complete": True}
    assert len(closure["records"]) == 251
    ids = [row["source_rule_id"] for row in closure["records"]]
    assert len(set(ids)) == 251
    assert all(row.get("canonical_source_disposition") for row in closure["records"])
    assert Counter(row["canonical_source_disposition"] for row in closure["records"]) == Counter(EXPECTED_DISPOSITIONS)

    readiness = closure["summary"]["readiness_class_counts"]
    assert readiness == {
        "MULTI_CLASS_BLOCKED": 44,
        "LOCAL_STRUCTURE_READY": 26,
        "SOURCE_UNDERDETERMINED": 157,
        "DEPENDENCY_COMPILER_GATED": 24,
    }
    assert sum(readiness.values()) == 251
    assert closure["summary"]["rows_with_source_underdetermination"] == 201
    assert closure["summary"]["blocked_rows_without_deep_source_review"] == 0
    assert closure["summary"]["deep_source_review_partition"] == {
        "issue_489": 100, "issue_498": 100, "issue_501": 28,
        "total_blocked_rows_reviewed": 228, "overlap": 0,
    }

    assert census["summary"]["audited_local_structure_ready_rows"] == 26
    assert census["summary"]["total_knowledge_condition_ir_ready"] == 12
    assert census["summary"]["not_condition_ir_ready_despite_local_structure_ready"] == 14
    assert sum(census["summary"]["band_counts"].values()) == 26

    assert graph["summary"]["explicit_reference_nodes"] == 65
    assert graph["summary"]["explicit_edges"] == 66
    assert graph["summary"]["cycles"] == 0
    assert graph["summary"]["unresolved_parent_ids"] == 0
    assert graph["summary"]["dependency_only_parent_underdetermined"] == 24
    assert graph["summary"]["rows_with_transitive_inherited_blockers"] == 38


def test_p09_handoff_census_accounts_for_all_14_non_ir_ready_local_structure_rows():
    handoff = load(HANDOFF)
    census = load(CENSUS)
    relation = load(RELATION)
    inherited = load(INHERITED)

    not_ready = {
        row["source_rule_id"] for row in census["records"]
        if row["compiler_readiness_band"] in {
            "DEPENDENCY_EFFECTIVE_UNDERDETERMINED",
            "DIRECT_RELATION_OR_COMPOSITION_DEFERRED",
        }
    }
    assert not_ready == EXPECTED_INHERITED | EXPECTED_RELATION
    assert len(not_ready) == 14

    assert {row["source_rule_id"] for row in relation["records"]} == EXPECTED_RELATION
    assert relation["summary"]["rows_rechecked"] == 3
    assert relation["summary"]["rows_retained_unresolved"] == 3
    assert relation["summary"]["rows_with_source_supported_new_geometry"] == 0
    assert all(row["disposition"] == "RETAINED_UNRESOLVED" for row in relation["records"])

    assert {row["source_rule_id"] for row in inherited["records"]} == EXPECTED_INHERITED
    assert inherited["summary"]["rows_rechecked"] == 11
    assert inherited["summary"]["rows_retained_fail_closed"] == 11
    assert inherited["summary"]["antecedent_edges_changed"] == 0
    assert inherited["summary"]["canonical_source_rows_changed"] == 0
    assert all(row["disposition"] == "RETAINED_UNRESOLVED" for row in inherited["records"])

    local = handoff["local_structure_ready_reconciliation"]
    assert local["total_rows"] == 26
    assert local["knowledge_condition_ir_ready"] == 12
    assert local["not_condition_ir_ready"] == 14
    assert local["not_ready_partition"]["inherited_dependency_rows"] == 11
    assert local["not_ready_partition"]["relation_or_composition_rows"] == 3
    assert local["all_14_have_direct_source_disposition"] is True
    assert local["all_14_remain_fail_closed"] is True


def test_p09_stage_handoff_state_keeps_residuals_explicit_and_execution_locked():
    handoff = load(HANDOFF)
    state = STATE.read_text(encoding="utf-8")

    assert handoff["execution_boundary"]["conditions_compiled"] == 0
    assert handoff["execution_boundary"]["execution_unlocked"] == 0
    assert handoff["execution_boundary"]["product_runtime_authorized"] is False
    assert handoff["execution_boundary"]["shared_core_semantics_changed"] is False
    assert handoff["guardrails"]["no_universal_all_any_n_of_default"] is True
    assert handoff["guardrails"]["no_closed_world_absence_default"] is True
    assert handoff["guardrails"]["next_palace_not_activated_by_this_artifact_alone"] is True

    assert 'status: "ACTIVE_NO_ACTIVE_WORK"' in state
    assert "active_issue: null" in state
    assert "active_branch: null" in state
    assert "active_pr: null" in state
    assert 'source_audit_status: "COMPLETE_WITH_EXPLICIT_RESIDUALS"' in state
    assert "P07 #669" in state
    assert "Future P09 ontology mapping remains a separate Core/Human-Gate-gated work unit" in state
    assert "conditions_compiled: 0" in state
    assert "execution_unlocked: 0" in state

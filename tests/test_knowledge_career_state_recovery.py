import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "knowledge/states/P09_CAREER_STATE.yaml"
SOURCE_AUDIT = ROOT / "knowledge/wp07a/CAREER_888_CLOSURE_AUDIT_v0.1.json"
SOURCE_TAIL = ROOT / "knowledge/wp07a/CAREER_FINAL36_CLOSURE_v0.1.json"
CLOSURE = ROOT / "knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251_v0.15.json"
GRAPH = ROOT / "knowledge/wp08/CAREER_ANTECEDENT_DEPENDENCY_GRAPH_65_v0.1.json"
IR = ROOT / "knowledge/wp08/CAREER_DEPENDENCY_IR_3_v0.1.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_p09_state_cache_matches_accepted_recovery_checkpoint():
    state = STATE.read_text(encoding="utf-8")
    assert 'status: "ACTIVE_NO_ACTIVE_WORK"' in state
    assert "active_issue: null" in state
    assert "active_branch: null" in state
    assert "active_pr: null" in state
    assert (
        'canonical_checkpoint: "CAREER_CANONICAL_888_OF_888_SOURCE_REVIEWED; '
        'CLOSURE_251_V0_15; DEPENDENCY_IR_3_OF_3; '
        '12_CONDITION_IR_READY_14_LOCAL_FAIL_CLOSED"'
    ) in state
    assert "Issue #508 / PR #509" in state
    assert "conditions_compiled=0" in state
    assert "execution_unlocked=0" in state
    assert "Future work is gap-driven" in state


def test_career_source_id_coverage_remains_888_of_888():
    audit = load(SOURCE_AUDIT)
    tail = load(SOURCE_TAIL)

    assert audit["canonical_source_rules"] == 888
    assert audit["structured_unique_ids_expected"] == 888
    assert (
        audit["strict_review_disposition_rows"]
        + audit["pre_hundred_batch_specialized_structured_ids"]
        == 888
    )
    assert sum(audit["disposition_totals"].values()) == 836
    assert audit["closure_claims"]["all_canonical_ids_have_structured_disposition"] is True
    assert audit["closure_claims"]["all_rules_executable"] is False
    assert tail["scope"]["closure_target_unique_ids"] == 888
    assert tail["progress_counts"]["unique_structured_rule_records_after"] == 888
    assert len(tail["mappings"]) == 36


def test_v015_activation_closure_counts_and_execution_boundary_reconcile():
    closure = load(CLOSURE)
    assert closure["coverage"] == {
        "total": 251,
        "unique_source_rule_ids": 251,
        "complete": True,
    }
    summary = closure["summary"]
    assert summary["blocker_counts"]["ANTECEDENT_DEPENDENCY"] == 47
    assert summary["readiness_class_counts"]["LOCAL_STRUCTURE_READY"] == 26
    assert summary["readiness_class_counts"]["DEPENDENCY_COMPILER_GATED"] == 24
    assert summary["rows_with_no_current_activation_blocker"] == 26
    assert summary["rows_with_source_underdetermination"] == 201
    assert summary["source_resolution_changes"] == 45
    assert summary["source_condition_repairs"] == 13
    assert summary["conditions_compiled"] == 0
    assert summary["execution_unlocked"] == 0


def test_dependency_graph_and_ir_have_exact_accepted_scope():
    graph = load(GRAPH)
    ir = load(IR)
    graph_summary = graph["summary"]

    assert len(graph["records"]) == 65
    assert graph_summary["explicit_reference_nodes"] == 65
    assert graph_summary["explicit_edges"] == 66
    assert graph_summary["cycles"] == 0
    assert graph_summary["max_explicit_reference_depth"] == 2
    assert graph_summary["unresolved_parent_ids"] == 0
    assert graph["scope"]["source_rule_registry_size"] == 888

    pairs = [(row["child_rule_id"], row["parent_rule_id"]) for row in ir["records"]]
    assert pairs == [
        ("CA05-420", "CA05-419"),
        ("CA07-639", "CA07-638"),
        ("CA07-682", "CA07-681"),
    ]
    assert ir["summary"]["ir_records"] == 3
    assert ir["summary"]["conditions_compiled"] == 0
    assert ir["summary"]["execution_unlocked"] == 0
    assert {
        row["source_rule_id"] for row in ir["negative_controls"]
    } == {"CA02-171", "CA03-236", "CA04-323"}
    assert all(row["must_not_promote"] for row in ir["negative_controls"])

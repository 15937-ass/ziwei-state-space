import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "knowledge/wp08/CAREER_SOURCE_DEEPEN_100B_v0.1.json"
C11 = ROOT / "knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251_v0.11.json"
C12 = ROOT / "knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251_v0.12.json"

def load(p):
    return json.loads(p.read_text(encoding="utf-8"))

def test_target_count_and_exact_selection():
    r=load(REVIEW)
    assert r["summary"]["reviewed"] == 100
    assert len(r["selection"]["target_ids"]) == 100
    assert len(set(r["selection"]["target_ids"])) == 100
    assert r["summary"]["antecedent_dependency_rows"] == 50
    assert r["summary"]["antecedent_only_compiler_gated_rows"] == 27
    assert r["summary"]["pair_or_closed_group_rows"] == 29
    assert r["summary"]["closed_category_rows"] == 22

def test_all_rows_directly_rechecked_and_fail_closed():
    r=load(REVIEW)
    assert len(r["records"]) == 100
    assert all(x["direct_source_recheck"] is True for x in r["records"])
    assert all(x["condition_compiled"] is False for x in r["records"])
    assert all(x["execution_unlocked"] is False for x in r["records"])

def test_ca08704_scope_repaired_only():
    r=load(REVIEW); x={z["source_rule_id"]:z for z in r["records"]}["CA08-704"]
    assert x["review_disposition"] == "SOURCE_SCOPE_METADATA_REPAIRED_DEPENDENCY_RETAINED"
    assert "巨门" in x["source_scope_override"]
    assert x["blockers_after"] == ["ANTECEDENT_DEPENDENCY"]

def test_ca08800_relation_scope_repaired_without_group_default():
    r=load(REVIEW); x={z["source_rule_id"]:z for z in r["records"]}["CA08-800"]
    assert x["review_disposition"] == "SOURCE_CLAUSE_STRUCTURE_REPAIRED_FAIL_CLOSED"
    assert "SAME_PALACE" in x["normalized_expression"]
    assert "MEET" in x["normalized_expression"]
    assert "更不宜" in x["normalized_expression"]
    assert x["blockers_after"] == x["blockers_before"]

def test_ca09805_duplicate_alias():
    r=load(REVIEW); x={z["source_rule_id"]:z for z in r["records"]}["CA09-805"]
    assert x["duplicate_source_rule_of"] == "CA08-800"
    assert x["review_disposition"] == "DUPLICATE_ALIAS_CONFIRMED_FAIL_CLOSED"

def test_ca09847_clears_only_antecedent_condition_recheck():
    r=load(REVIEW); x={z["source_rule_id"]:z for z in r["records"]}["CA09-847"]
    assert "ANTECEDENT_SOURCE_CONDITION_RECHECK_REQUIRED" in x["blockers_before"]
    assert "ANTECEDENT_SOURCE_CONDITION_RECHECK_REQUIRED" not in x["blockers_after"]
    assert "ANTECEDENT_DEPENDENCY" in x["blockers_after"]
    assert "AUXILIARY_SUPPORT_ACTIVATION_CONTEXTUAL_UNRESOLVED" in x["blockers_after"]
    assert x["antecedent_source_condition_override"]["optional_strengtheners"] == ["破军化禄","破军化权"]

def test_closure_v012_census():
    c11,c12=load(C11),load(C12)
    assert len(c11["records"]) == 251 == len(c12["records"])
    assert c12["summary"]["rows_with_no_current_activation_blocker"] == 23
    assert c12["summary"]["rows_with_source_underdetermination"] == 201
    assert c12["summary"]["source_resolution_changes"] == 43
    assert c12["summary"]["source_condition_repairs"] == 11
    assert c12["summary"]["blocker_counts"]["ANTECEDENT_SOURCE_CONDITION_RECHECK_REQUIRED"] == 0
    assert c12["summary"]["conditions_compiled"] == 0
    assert c12["summary"]["execution_unlocked"] == 0
    assert c12["summary"]["fifth_layer_newly_no_blocker_rows"] == 0

def test_guardrails():
    g=load(REVIEW)["guardrails"]
    assert all(v is False for v in g.values())

import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
R=ROOT/"knowledge/wp08/CAREER_RESIDUAL_28_FINAL_SOURCE_PASS_v0.1.json"
C12=ROOT/"knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251_v0.12.json"
C13=ROOT/"knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251_v0.13.json"
def load(p): return json.loads(p.read_text(encoding="utf-8"))
def test_exact_28_final_partition():
    r=load(R)
    assert r["summary"]["reviewed"]==28
    assert len(r["selection"]["target_ids"])==28
    assert len(set(r["selection"]["target_ids"]))==28
    assert (r["summary"]["issue489_partition"],r["summary"]["issue498_partition"],r["summary"]["issue501_partition"])==(100,100,28)
    assert r["summary"]["all_blocked_career_rows_deep_source_reviewed_after_this_pass"]==228
def test_direct_source_review_and_fail_closed():
    r=load(R)
    assert len(r["records"])==28
    assert all(x["direct_source_recheck"] for x in r["records"])
    assert all(not x["condition_compiled"] and not x["execution_unlocked"] for x in r["records"])
def test_ca04337_local_transformation_alternatives_only():
    x={z["source_rule_id"]:z for z in load(R)["records"]}["CA04-337"]
    assert "SOURCE_LIST_QUANTIFIER_UNSPECIFIED" in x["blockers_before"]
    assert "SOURCE_LIST_QUANTIFIER_UNSPECIFIED" not in x["blockers_after"]
    assert x["blockers_after"]==["AUXILIARY_SUPPORT_ACTIVATION_CONTEXTUAL_UNRESOLVED"]
    assert "LOCAL_ANY_OF" in x["normalized_expression"]
def test_ca05471_baiguan_is_example_not_mandatory_threshold():
    x={z["source_rule_id"]:z for z in load(R)["records"]}["CA05-471"]
    assert "BAIGUAN_ACTIVATION_NO_UNIVERSAL_THRESHOLD" in x["blockers_before"]
    assert "BAIGUAN_ACTIVATION_NO_UNIVERSAL_THRESHOLD" not in x["blockers_after"]
    assert x["blockers_after"]==["OPEN_VALENCE_CATEGORY_ACTIVATION_CONTEXTUAL_UNRESOLVED"]
    assert "百官朝拱_as_example" in x["normalized_expression"]
def test_v013_census_and_full_deep_review():
    c=load(C13)
    assert len(c["records"])==251
    assert c["summary"]["rows_with_no_current_activation_blocker"]==23
    assert c["summary"]["rows_with_source_underdetermination"]==201
    assert c["summary"]["source_resolution_changes"]==44
    assert c["summary"]["source_condition_repairs"]==13
    assert c["summary"]["blocked_rows_without_deep_source_review"]==0
    assert c["summary"]["deep_source_review_partition"]=={"issue_489":100,"issue_498":100,"issue_501":28,"total_blocked_rows_reviewed":228,"overlap":0}
    assert c["summary"]["conditions_compiled"]==0 and c["summary"]["execution_unlocked"]==0
def test_blocker_count_deltas_exact():
    a,b=load(C12),load(C13)
    assert b["summary"]["blocker_counts"]["SOURCE_LIST_QUANTIFIER_UNSPECIFIED"]==a["summary"]["blocker_counts"]["SOURCE_LIST_QUANTIFIER_UNSPECIFIED"]-1
    assert b["summary"]["blocker_counts"]["BAIGUAN_ACTIVATION_NO_UNIVERSAL_THRESHOLD"]==a["summary"]["blocker_counts"]["BAIGUAN_ACTIVATION_NO_UNIVERSAL_THRESHOLD"]-1
def test_guardrails():
    assert all(v is False for v in load(R)["guardrails"].values())

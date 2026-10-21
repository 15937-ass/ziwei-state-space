import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RECHECK=ROOT/"knowledge/wp08/CAREER_SOURCE_LEXICAL_RECHECK_10_v0.2.json"
BASELINE=ROOT/"knowledge/wp08/CAREER_SOURCE_LEXICON_QUANTIFIER_10_v0.1.json"
C10=ROOT/"knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251_v0.10.json"
C11=ROOT/"knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251_v0.11.json"

def load(p): return json.loads(p.read_text(encoding="utf-8"))

def test_exact_overlap_is_disclosed_and_all_ten_rechecked():
    r,b=load(RECHECK),load(BASELINE)
    assert r["summary"]["reviewed"]==10
    assert r["scope"]["exact_overlap_with_issue_469"]==10
    assert {x["source_rule_id"] for x in r["records"]}=={x["source_rule_id"] for x in b["records"]}

def test_ca01059_restores_inner_list_quantifier_blocker():
    r=load(RECHECK); x={z["source_rule_id"]:z for z in r["records"]}["CA01-059"]
    assert "SOURCE_LIST_QUANTIFIER_UNSPECIFIED" in x["blockers_after"]
    assert "CLOSED_WORLD_ABSENCE_EVIDENCE" in x["blockers_after"]
    assert "AUXILIARY_SUPPORT_ACTIVATION_CONTEXTUAL_UNRESOLVED" in x["blockers_after"]

def test_ca03289_pair_internal_only_outer_quantifier_stays_blocked():
    r=load(RECHECK); x={z["source_rule_id"]:z for z in r["records"]}["CA03-289"]
    assert "SOURCE_LIST_QUANTIFIER_UNSPECIFIED" in x["blockers_after"]
    assert "SOURCE_OPEN_TAIL_MEMBERSHIP_UNSPECIFIED" in x["blockers_after"]
    assert "ANY_OF" not in x["normalized_expression"]
    assert "PAIR_CO_PRESENT(三台,八座)" in x["normalized_expression"]
    assert "PAIR_CO_PRESENT(恩光,天贵)" in x["normalized_expression"]

def test_ca06502_uses_existing_contextual_lu_blocker():
    r=load(RECHECK); x={z["source_rule_id"]:z for z in r["records"]}["CA06-502"]
    assert x["blockers_before"]==["SOURCE_SHORTHAND_MEMBERSHIP_UNSPECIFIED"]
    assert x["blockers_after"]==["LU_SHORTHAND_CONTEXTUAL_UNRESOLVED"]
    assert x["source_resolution_changed_after"] is True

def test_all_recheck_rows_remain_fail_closed_or_already_ready():
    r=load(RECHECK)
    assert all(x["condition_compiled"] is False and x["execution_unlocked"] is False for x in r["records"])
    assert r["summary"]["newly_blocker_free_rows"]==0
    assert r["summary"]["conditions_compiled"]==0
    assert r["summary"]["execution_unlocked"]==0

def test_closure_v011_census_and_deltas():
    r,c10,c11=load(RECHECK),load(C10),load(C11)
    assert len(c10["records"])==251==len(c11["records"])
    assert c11["summary"]["rows_with_no_current_activation_blocker"]==22
    assert c11["summary"]["rows_with_source_underdetermination"]==202
    assert c11["summary"]["source_resolution_changes"]==41
    assert c11["summary"]["source_condition_repairs"]==9
    assert c11["summary"]["blocker_counts"]["SOURCE_LIST_QUANTIFIER_UNSPECIFIED"]==8
    assert c11["summary"]["blocker_counts"]["SOURCE_SHORTHAND_MEMBERSHIP_UNSPECIFIED"]==0
    assert c11["summary"]["blocker_counts"]["LU_SHORTHAND_CONTEXTUAL_UNRESOLVED"]==5
    assert c11["summary"]["conditions_compiled"]==0 and c11["summary"]["execution_unlocked"]==0
    assert c11["summary"]["lexical_recheck_target_overlap_with_issue_469"]==10

def test_guardrails():
    g=load(RECHECK)["guardrails"]
    assert all(v is False for v in g.values())


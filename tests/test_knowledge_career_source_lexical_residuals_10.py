import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RES=ROOT/"knowledge/wp08/CAREER_SOURCE_LEXICAL_RESIDUALS_10_v0.1.json"
CLOSURE=ROOT/"knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251_v0.5.json"

def load(p):
    return json.loads(p.read_text(encoding="utf-8"))

def test_ten_of_ten_dispositioned():
    d=load(RES)
    assert d["summary"]["reviewed"]==10
    assert len(d["records"])==10
    assert {r["source_rule_id"] for r in d["records"]}=={
        "CA01-059","CA02-107","CA03-289","CA04-345","CA04-391",
        "CA05-433","CA05-484","CA06-502","CA08-723","CA09-864"
    }
    assert d["guardrails"]["global_any_default"] is False
    assert d["guardrails"]["global_all_default"] is False
    assert d["guardrails"]["numeric_threshold_inferred"] is False
    assert d["guardrails"]["execution_unlocked"] is False

def test_source_repairs_are_not_silent_semantic_inflation():
    d=load(RES)
    by={r["source_rule_id"]:r for r in d["records"]}
    assert "廉贞化禄、贪狼化禄、武曲化禄" in by["CA01-059"]["repaired_source_surface"]
    assert "SOURCE_LIST_QUANTIFIER_UNSPECIFIED" in by["CA01-059"]["remaining_blockers"]
    assert "属火的星曜" in by["CA04-345"]["normalized_expression"]
    assert "CARDINALITY_THRESHOLD_UNSPECIFIED" in by["CA04-345"]["remaining_blockers"]
    assert "+" not in by["CA05-484"]["normalized_expression"]
    assert by["CA05-484"]["remaining_blockers"]==[]

def test_pair_resolution_is_source_local():
    d=load(RES)
    by={r["source_rule_id"]:r for r in d["records"]}
    x=by["CA03-289"]
    assert x["disposition"]=="SOURCE_LOCAL_ANY_OF_PAIRED_PATTERNS_RESOLVED"
    assert "PAIR_CO_PRESENT(三台,八座)" in x["normalized_expression"]
    assert "PAIR_CO_PRESENT(恩光,天贵)" in x["normalized_expression"]
    assert x["remaining_blockers"]==[]

def test_legitimate_unknowns_stay_unknown():
    d=load(RES)
    by={r["source_rule_id"]:r for r in d["records"]}
    assert by["CA04-391"]["disposition"].startswith("NO_UNIVERSAL_RULE")
    assert by["CA05-433"]["disposition"].startswith("INSUFFICIENT_SOURCE")
    assert by["CA06-502"]["remaining_blockers"]==["OPEN_CATEGORY_MEMBER_OR_QUANTIFIER_UNSPECIFIED"]
    assert "SOURCE_PATTERN_BINDING_UNSPECIFIED" in by["CA08-723"]["remaining_blockers"]
    assert "SOURCE_SHORTHAND_MEMBERSHIP_UNSPECIFIED" not in by["CA09-864"]["remaining_blockers"]

def test_closure_v05_counts_and_no_execution_unlock():
    c=load(CLOSURE)
    assert c["coverage"]["total"]==251
    assert c["summary"]["source_lexical_residuals_reviewed"]==10
    assert c["summary"]["source_shorthand_membership_unspecified_before"]==6
    assert c["summary"]["source_shorthand_membership_unspecified_after"]==0
    assert c["summary"]["source_list_quantifier_unspecified_before"]==4
    assert c["summary"]["source_list_quantifier_unspecified_after"]==3
    assert c["summary"]["blocker_counts"].get("SOURCE_SHORTHAND_MEMBERSHIP_UNSPECIFIED",0)==0
    assert c["summary"]["blocker_counts"]["SOURCE_LIST_QUANTIFIER_UNSPECIFIED"]==3
    assert c["summary"]["blocker_counts"]["OPEN_CATEGORY_MEMBER_OR_QUANTIFIER_UNSPECIFIED"]==132
    assert c["summary"]["blocker_counts"]["SOURCE_PATTERN_BINDING_UNSPECIFIED"]==1
    assert c["summary"]["rows_with_no_current_activation_blocker"]==19
    assert c["summary"]["rows_with_source_underdetermination"]==205
    assert c["summary"]["source_resolution_changes"]==26
    assert c["summary"]["source_condition_repairs"]==4
    assert c["summary"]["execution_unlocked"]==0

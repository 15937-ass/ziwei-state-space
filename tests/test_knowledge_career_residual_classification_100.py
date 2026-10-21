import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/"knowledge/wp08/CAREER_RESIDUAL_CLASSIFICATION_100_v0.1.json"
C5=ROOT/"knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251_v0.5.json"

def load(p):
    return json.loads(p.read_text(encoding="utf-8"))

def test_exact_100_selected_with_93_plus_7_strategy():
    a=load(ART)
    assert a["selection"]["member_quantifier_rows_selected"]==93
    assert a["selection"]["open_category_supplement_rows_selected"]==7
    assert a["selection"]["total"]==100
    assert a["summary"]["reviewed"]==100
    assert len(a["records"])==100
    assert len({r["source_rule_id"] for r in a["records"]})==100

def test_disposition_counts_are_frozen():
    a=load(ART)
    assert a["summary"]["disposition_counts"]=={
        "CLOSED_WORLD_NEGATION_GATED":11,
        "SOURCE_LOCAL_QUANTIFIER_CANDIDATE":14,
        "NAMED_GROUP_RELATION_REVIEW":60,
        "COMPOUND_OR_DEPENDENCY_GATED":7,
        "OPEN_CATEGORY_NO_UNIVERSAL_RULE_CANDIDATE":4,
        "SOURCE_RECHECK_REQUIRED":4,
    }
    assert a["summary"]["source_researchable_rows"]==78
    assert a["summary"]["structural_gate_rows"]==18
    assert a["summary"]["open_no_universal_rule_candidate_rows"]==4

def test_selected_rows_match_canonical_v05_strategy():
    a,c=load(ART),load(C5)
    member=[r["source_rule_id"] for r in c["records"] if "MEMBER_QUANTIFIER_UNSPECIFIED" in r["blockers"]]
    open_only=[r["source_rule_id"] for r in c["records"] if "MEMBER_QUANTIFIER_UNSPECIFIED" not in r["blockers"] and "OPEN_CATEGORY_MEMBER_OR_QUANTIFIER_UNSPECIFIED" in r["blockers"]]
    expected=member+open_only[:7]
    assert [r["source_rule_id"] for r in a["records"]]==expected

def test_no_blocker_or_execution_change():
    a=load(ART)
    assert a["summary"]["blockers_cleared"]==0
    assert a["summary"]["source_resolution_changes"]==0
    assert a["summary"]["conditions_compiled"]==0
    assert a["summary"]["execution_unlocked"]==0
    assert all(r["blockers_cleared"]==[] for r in a["records"])
    assert all(r["source_resolution_changed"] is False for r in a["records"])
    assert all(r["condition_compiled"] is False and r["execution_unlocked"] is False for r in a["records"])

def test_high_frequency_surfaces_are_preserved():
    a=load(ART)
    freq={x["surface"]:x["count"] for x in a["top_source_group_surfaces"]}
    assert freq["空劫"]==29
    assert freq["昌曲"]==21
    assert freq["火铃"]==18
    assert freq["辅弼"]==11
    assert freq["魁钺"]==9

def test_pair_context_reconnaissance_blocks_global_default():
    a=load(ART)
    evidence={x["evidence_id"]:x for x in a["source_reconnaissance"]}
    assert "见齐对星始吉" in evidence["RC100-E01"]["source_excerpt"]
    assert "见单星者" in evidence["RC100-E01"]["source_excerpt"]
    assert "必须见辅佐对星" in evidence["RC100-E02"]["source_excerpt"]
    assert "见昌曲对星" in evidence["RC100-E03"]["source_excerpt"]
    g=a["guardrails"]
    assert g["global_any_default"] is False
    assert g["global_all_default"] is False
    assert g["global_n_of_default"] is False

def test_guardrails_keep_product_and_actions_out():
    g=load(ART)["guardrails"]
    assert g["product_runtime_modified"] is False
    assert g["github_actions_used"] is False
    assert g["numeric_weights_added"] is False
    assert g["probabilities_added"] is False

def test_canonical_category_lexicon_prevents_false_open_classification():
    a=load(ART)
    rows={r["source_rule_id"]:r for r in a["records"]}
    assert rows["CA01-085"]["primary_disposition"]=="NAMED_GROUP_RELATION_REVIEW"  # 煞曜 closed membership
    assert rows["CA02-133"]["primary_disposition"]=="NAMED_GROUP_RELATION_REVIEW"  # 吉化 closed membership
    assert rows["CA02-147"]["primary_disposition"]=="NAMED_GROUP_RELATION_REVIEW"  # 见煞 scoped alias
    assert rows["CA01-098"]["primary_disposition"]=="OPEN_CATEGORY_NO_UNIVERSAL_RULE_CANDIDATE"
    assert rows["CA02-107"]["primary_disposition"]=="OPEN_CATEGORY_NO_UNIVERSAL_RULE_CANDIDATE"

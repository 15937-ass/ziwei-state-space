import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REVIEW=ROOT/"knowledge/wp08/CAREER_SOURCE_LEXICON_QUANTIFIER_10_v0.1.json"
N1=ROOT/"knowledge/wp08/CAREER_SEMANTIC_NORMALIZATION_36_v0.1.json"
N2=ROOT/"knowledge/wp08/CAREER_SEMANTIC_NORMALIZATION_36_v0.2.json"
C4=ROOT/"knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251_v0.4.json"
C5=ROOT/"knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251_v0.5.json"

def load(p):
    return json.loads(p.read_text(encoding="utf-8"))

def test_exact_ten_residuals_reviewed():
    r=load(REVIEW)
    assert r["summary"]["target_rows"]==10
    assert r["summary"]["reviewed"]==10
    assert len(r["records"])==10
    assert {x["source_rule_id"] for x in r["records"]}=={"CA01-059","CA02-107","CA03-289","CA04-345","CA04-391","CA05-433","CA05-484","CA06-502","CA08-723","CA09-864"}

def test_disposition_counts_are_frozen():
    r=load(REVIEW)
    counts={}
    for x in r["records"]:
        counts[x["disposition"]]=counts.get(x["disposition"],0)+1
    assert counts=={"SOURCE_RESOLVED":2,"NO_UNIVERSAL_RULE":5,"STILL_UNDERDETERMINED":3}

def test_ca01059_repairs_projection_compression():
    r={x["source_rule_id"]:x for x in load(REVIEW)["records"]}["CA01-059"]
    assert "财星化禄" in r["source_repair"]
    for token in ["廉贞","贪狼","武曲"]:
        assert f"TRANSFORM({token},化禄)" in r["normalized_expression"]
    assert "SOURCE_SHORTHAND_MEMBERSHIP_UNSPECIFIED" not in r["blockers_after"]
    assert "MEMBER_QUANTIFIER_UNSPECIFIED" in r["blockers_after"]

def test_ca05484_restores_source_local_or_not_false_and():
    r={x["source_rule_id"]:x for x in load(REVIEW)["records"]}["CA05-484"]
    assert "TRANSFORM(武曲,化禄) OR ATOM(禄存)" in r["normalized_expression"]
    assert "OR TRANSFORM(天府,化科)" in r["normalized_expression"]
    assert r["ordinal_preference"]==["TRANSFORM(武曲,化禄)","ATOM(禄存)"]
    assert r["blockers_after"]==[]

def test_open_or_compound_source_semantics_are_not_forced_closed():
    r={x["source_rule_id"]:x for x in load(REVIEW)["records"]}
    assert r["CA02-107"]["disposition"]=="NO_UNIVERSAL_RULE"
    assert "OPEN_FUNCTIONAL_CATEGORY(刑曜)"==r["CA02-107"]["normalized_expression"]
    assert "OPEN_TAIL(等杂曜)" in r["CA03-289"]["normalized_expression"]
    assert "多见属火的星曜" in r["CA04-345"]["normalized_expression"]
    assert "CARDINALITY_THRESHOLD_UNSPECIFIED" in r["CA04-345"]["blockers_after"]
    assert "SOURCE_COMPOUND(刑忌)" in r["CA08-723"]["normalized_expression"]
    assert "OPEN_QUALIFIED_SUPPORT_CATEGORY(吉辅)" in r["CA09-864"]["normalized_expression"]

def test_true_list_ambiguity_remains_fail_closed():
    r={x["source_rule_id"]:x for x in load(REVIEW)["records"]}
    for rid in ["CA04-391","CA05-433"]:
        assert r[rid]["disposition"]=="STILL_UNDERDETERMINED"
        assert "SOURCE_LIST_QUANTIFIER_UNSPECIFIED" in r[rid]["blockers_after"]
    assert r["CA06-502"]["disposition"]=="STILL_UNDERDETERMINED"
    assert "SOURCE_SHORTHAND_MEMBERSHIP_UNSPECIFIED" in r["CA06-502"]["blockers_after"]

def test_normalization_v02_keeps_all_36_and_applies_recheck():
    n1,n2=load(N1),load(N2)
    assert len(n1["records"])==36 and len(n2["records"])==36
    assert {x["source_rule_id"] for x in n1["records"]}=={x["source_rule_id"] for x in n2["records"]}
    rows={x["source_rule_id"]:x for x in n2["records"]}
    assert rows["CA05-484"]["blockers_after"]==[]
    assert "SOURCE_SHORTHAND_MEMBERSHIP_UNSPECIFIED" not in rows["CA01-059"]["blockers_after"]
    assert all(x["execution_unlocked"] is False for x in n2["records"])

def test_closure_v05_preserves_251_and_only_advances_local_readiness():
    c4,c5=load(C4),load(C5)
    assert len(c4["records"])==251 and len(c5["records"])==251
    assert {x["source_rule_id"] for x in c4["records"]}=={x["source_rule_id"] for x in c5["records"]}
    assert c4["summary"]["rows_with_no_current_activation_blocker"]==17
    assert c5["summary"]["rows_with_no_current_activation_blocker"]==18
    assert c5["summary"]["source_shorthand_membership_unspecified_after"]==1
    assert c5["summary"]["source_list_quantifier_unspecified_after"]==2
    assert c5["summary"]["execution_unlocked"]==0
    row={x["source_rule_id"]:x for x in c5["records"]}["CA05-484"]
    assert row["readiness_class"]=="LOCAL_STRUCTURE_READY"
    assert row["blockers"]==[]

def test_no_any_all_nof_or_product_unlock():
    r=load(REVIEW)
    g=r["guardrails"]
    assert g["global_any_default"] is False
    assert g["global_all_default"] is False
    assert g["global_n_of_default"] is False
    assert g["product_runtime_modified"] is False
    assert r["summary"]["conditions_compiled"]==0
    assert r["summary"]["execution_unlocked"]==0

def test_source_resolution_change_bookkeeping_is_pass_local():
    n={x["source_rule_id"]:x for x in load(N2)["records"]}
    changed={"CA01-059","CA02-107","CA03-289","CA04-345","CA05-484","CA08-723","CA09-864"}
    unchanged={"CA04-391","CA05-433","CA06-502"}
    assert all(n[rid]["source_resolution_changed"] is True for rid in changed)
    assert all(n[rid]["source_resolution_changed"] is False for rid in unchanged)
    assert load(REVIEW)["summary"]["source_repairs"]==4
    assert load(REVIEW)["summary"]["source_resolution_changes"]==7
    assert load(C5)["summary"]["source_lexicon_quantifier_source_repairs"]==4
    assert load(C5)["summary"]["source_lexicon_quantifier_source_resolution_changes"]==7

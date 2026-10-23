import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SEM=ROOT/"knowledge/wp08/CAREER_PAIR_CLOSED_GROUP_CONTEXTUAL_63_v0.1.json"
C5=ROOT/"knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251_v0.5.json"
C6=ROOT/"knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251_v0.6.json"

def load(p): return json.loads(p.read_text(encoding='utf-8'))

def test_63_exact_targets_and_refinements():
    s=load(SEM)
    assert s["summary"]["target_rules"]==63
    assert s["summary"]["reviewed"]==63
    assert len(s["records"])==63
    assert len({r["source_rule_id"] for r in s["records"]})==63
    assert s["summary"]["generic_member_quantifier_refined"]==60
    assert s["summary"]["false_open_category_refined"]==3

def test_family_counts_and_membership_contracts():
    s=load(SEM)
    fam={x["family_id"]:x for x in s["family_contracts"]}
    assert fam["PAIR_KONG_JIE"]["target_count"]==21
    assert fam["PAIR_CHANG_QU"]["target_count"]==18
    assert fam["PAIR_HUO_LING"]["target_count"]==17
    assert fam["PAIR_KUI_YUE"]["target_count"]==9
    assert fam["PAIR_FU_BI"]["target_count"]==7
    assert fam["PAIR_KONG_JIE"]["members"]==["地空","地劫"]
    assert fam["PAIR_CHANG_QU"]["members"]==["文昌","文曲"]
    assert fam["PAIR_HUO_LING"]["members"]==["火星","铃星"]
    assert fam["CAT_FOUR_MALEFICS"]["members"]==["擎羊","陀罗","火星","铃星"]

def test_no_global_quantifier_default():
    s=load(SEM)
    assert s["summary"]["universal_any_defaults_added"]==0
    assert s["summary"]["universal_all_defaults_added"]==0
    assert s["summary"]["universal_n_of_defaults_added"]==0
    assert all(f["universal_any_supported"] is False for f in s["family_contracts"])
    assert all(f["universal_all_supported"] is False for f in s["family_contracts"])

def test_closure_blocker_census():
    c5,c6=load(C5),load(C6)
    assert len(c5["records"])==251==len(c6["records"])
    assert c6["summary"]["member_quantifier_unspecified_before"]==93
    assert c6["summary"]["member_quantifier_unspecified_after"]==33
    assert c6["summary"]["open_category_member_or_quantifier_unspecified_before"]==132
    assert c6["summary"]["open_category_member_or_quantifier_unspecified_after"]==129
    assert c6["summary"]["pair_or_closed_group_activation_contextual_unresolved"]==60
    assert c6["summary"]["closed_category_activation_contextual_unresolved"]==3
    assert c6["summary"]["contextual_group_blockers_cleared"]==0

def test_specific_false_open_rows_are_reclassified():
    c6=load(C6); rows={r['source_rule_id']:r for r in c6['records']}
    for rid in ['CA01-085','CA02-133','CA02-147']:
        assert 'OPEN_CATEGORY_MEMBER_OR_QUANTIFIER_UNSPECIFIED' not in rows[rid]['blockers']
        assert 'CLOSED_CATEGORY_ACTIVATION_CONTEXTUAL_UNRESOLVED' in rows[rid]['blockers']

def test_unrelated_blockers_preserved():
    s=load(SEM)
    rows={r['source_rule_id']:r for r in s['records']}
    assert 'OPEN_CATEGORY_MEMBER_OR_QUANTIFIER_UNSPECIFIED' in rows['CA02-166']['blockers_after']
    assert 'CARDINALITY_THRESHOLD_UNSPECIFIED' in rows['CA04-345']['blockers_after']

def test_no_execution_unlock_or_product_change():
    s,c6=load(SEM),load(C6)
    assert s["summary"]["blockers_cleared"]==0
    assert s["summary"]["conditions_compiled"]==0
    assert s["summary"]["execution_unlocked"]==0
    assert s["guardrails"]["product_runtime_modified"] is False
    assert all(r["execution_unlocked"] is False for r in s["records"])
    assert c6["summary"]["execution_unlocked"]==0

import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
R37=ROOT/"knowledge/wp08/CAREER_RESIDUAL_CLOSURE_37_v0.1.json"
R100=ROOT/"knowledge/wp08/CAREER_RESIDUAL_SECOND_LAYER_100_v0.1.json"
C6=ROOT/"knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251_v0.6.json"
C7=ROOT/"knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251_v0.7.json"

def load(p): return json.loads(p.read_text(encoding='utf-8'))

def test_exact_37_and_cluster_partition():
    r=load(R37)
    assert r["summary"]["target_rules"]==37
    assert r["summary"]["reviewed"]==37
    assert len(r["records"])==37
    assert len({x["source_rule_id"] for x in r["records"]})==37
    assert r["summary"]["cluster_counts"]=={"NEGATION_CLOSED_WORLD":11,"LU_SHORTHAND_CONTEXT":8,"ANTECEDENT_COMPOSITION":7,"OPEN_CATEGORY_CONTEXT":5,"AUXILIARY_SUPPORT_CONTEXT":4,"SOURCE_LITERAL_RECHECK":2}

def test_four_source_local_resolutions():
    r=load(R37); rows={x['source_rule_id']:x for x in r['records']}
    solved={rid for rid,x in rows.items() if x['disposition']=='SOURCE_LOCAL_RESOLVED'}
    assert solved=={'CA05-411','CA07-681','CA09-820'}
    assert all(rows[rid]['blockers_after']==[] for rid in solved)
    assert rows['CA04-382']['disposition']=='SOURCE_LOCAL_PARTIAL_RESOLUTION'
    assert rows['CA04-382']['blockers_after']==['TRANSFORMATION_CARRIER_UNSPECIFIED']
    assert 'SOURCE_CONTEXT_UNSPECIFIED' in rows['CA04-382']['normalized_expression']
    assert 'TRANSFORM(巨门,化禄)' in rows['CA07-681']['normalized_expression']
    assert 'TRANSFORM(破军,化禄)' in rows['CA09-820']['normalized_expression']
    assert 'LOCAL_ANY_OF' in rows['CA05-411']['normalized_expression']

def test_source_repair_preserves_uncertainty():
    r=load(R37); rows={x['source_rule_id']:x for x in r['records']}
    x=rows['CA04-337']
    assert x['source_repair']
    assert 'SOURCE_LIST_QUANTIFIER_UNSPECIFIED' in x['blockers_after']
    assert 'AUXILIARY_SUPPORT_ACTIVATION_CONTEXTUAL_UNRESOLVED' in x['blockers_after']

def test_kewen_membership_refined_not_overclosed():
    r=load(R37); rows={x['source_rule_id']:x for x in r['records']}
    for rid in ['CA02-141','CA06-583','CA06-584','CA06-594']:
        assert 'CAREER_KEWEN_ACTIVATION_CONTEXTUAL_UNRESOLVED' in rows[rid]['blockers_after']
    assert 'OPEN_FUNCTIONAL_CATEGORY_MEMBERSHIP_OR_ACTIVATION_UNRESOLVED' in rows['CA06-584']['blockers_after']

def test_negation_and_antecedent_stay_fail_closed():
    r=load(R37); rows={x['source_rule_id']:x for x in r['records']}
    for rid in ['CA01-059','CA01-080','CA01-082','CA01-097','CA06-574','CA06-594','CA07-629','CA08-726','CA09-871','CA09-879','CA01-100']:
        assert 'CLOSED_WORLD_ABSENCE_EVIDENCE' in rows[rid]['blockers_after']
    for rid in ['CA04-323','CA04-357','CA04-359','CA04-363','CA05-429','CA06-573']:
        assert 'ANTECEDENT_DEPENDENCY' in rows[rid]['blockers_after']
    assert 'ANTECEDENT_DEPENDENCY' not in rows['CA02-117']['blockers_after']

def test_closure_v07_census_and_no_unlock():
    c6,c7=load(C6),load(C7)
    assert len(c6['records'])==251==len(c7['records'])
    assert c6['summary']['rows_with_no_current_activation_blocker']==18
    assert c7['summary']['rows_with_no_current_activation_blocker']==21
    assert c6['summary']['blocker_counts']['MEMBER_QUANTIFIER_UNSPECIFIED']==33
    assert c7['summary']['blocker_counts'].get('MEMBER_QUANTIFIER_UNSPECIFIED',0)==0
    assert c6['summary']['blocker_counts']['OPEN_CATEGORY_MEMBER_OR_QUANTIFIER_UNSPECIFIED']==129
    assert c7['summary']['blocker_counts'].get('OPEN_CATEGORY_MEMBER_OR_QUANTIFIER_UNSPECIFIED',0)==110
    assert c7['summary']['source_resolution_changes']==28
    assert c7['summary']['conditions_compiled']==0
    assert c7['summary']['execution_unlocked']==0

def test_combined_hundred_complete():
    r=load(R100)
    assert r['summary']['reviewed']==100
    assert r['scope']['pair_closed_group_second_layer']==63
    assert r['scope']['remaining_second_layer']==37
    assert len(r['records'])==100
    assert len({x['source_rule_id'] for x in r['records']})==100
    assert all(x['execution_unlocked'] is False for x in r['records'])

def test_guardrails():
    r=load(R37); g=r['guardrails']
    assert g['global_any_default'] is False
    assert g['global_all_default'] is False
    assert g['global_n_of_default'] is False
    assert g['global_lu_carrier_registry_added'] is False
    assert g['closed_world_default_added'] is False
    assert g['product_runtime_modified'] is False
    assert g['github_actions_used'] is False

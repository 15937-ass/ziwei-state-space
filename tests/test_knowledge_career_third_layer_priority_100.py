import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
R=ROOT/"knowledge/wp08/CAREER_THIRD_LAYER_PRIORITY_100_v0.1.json"
C8=ROOT/"knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251_v0.8.json"
C9=ROOT/"knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251_v0.9.json"

def load(p): return json.loads(p.read_text(encoding='utf-8'))

def test_exact_priority_selection_100():
    r,c8=load(R),load(C8)
    generic=[x for x in c8['records'] if 'OPEN_CATEGORY_MEMBER_OR_QUANTIFIER_UNSPECIFIED' in x['blockers']]
    pair=[x for x in c8['records'] if x['blockers']==['PAIR_OR_CLOSED_GROUP_ACTIVATION_CONTEXTUAL_UNRESOLVED']]
    closed=[x for x in c8['records'] if x['blockers']==['CLOSED_CATEGORY_ACTIVATION_CONTEXTUAL_UNRESOLVED']]
    comp=[x for x in c8['records'] if x['blockers']==['SOURCE_COMPOUND_COMPOSITION_UNSPECIFIED']]
    val=[x for x in c8['records'] if x['blockers']==['VALENCE_STATE_CRITERION_UNSPECIFIED']][:3]
    expected=generic+pair+closed+comp+val
    assert (len(generic),len(pair),len(closed),len(comp),len(val))==(10,49,26,12,3)
    assert len(expected)==100
    assert [x['source_rule_id'] for x in r['records']]==[x['source_rule_id'] for x in expected]

def test_generic_open_fully_retired():
    r,c9=load(R),load(C9)
    assert r['summary']['generic_open_before']==10
    assert r['summary']['generic_open_after']==0
    assert c9['summary']['blocker_counts'].get('OPEN_CATEGORY_MEMBER_OR_QUANTIFIER_UNSPECIFIED',0)==0
    assert all('OPEN_CATEGORY_MEMBER_OR_QUANTIFIER_UNSPECIFIED' not in x['blockers_after'] for x in r['records'])

def test_ca03228_source_local_fire_bell_resolution():
    r,c9=load(R),load(C9); rows={x['source_rule_id']:x for x in r['records']}; c={x['source_rule_id']:x for x in c9['records']}
    x=rows['CA03-228']
    assert x['disposition']=='SOURCE_LOCAL_RESOLVED'
    assert x['blockers_after']==[]
    assert 'LOCAL_ANY_OF[火星,铃星]' in x['normalized_expression']
    assert c['CA03-228']['readiness_class']=='LOCAL_STRUCTURE_READY'

def test_source_branch_repairs_fail_closed():
    r=load(R); rows={x['source_rule_id']:x for x in r['records']}
    for rid in ['CA03-277','CA04-397','CA09-859']:
        assert rows[rid]['source_resolution_changed'] is True
        assert 'SOURCE_BRANCH_DECOMPOSITION_REQUIRED' in rows[rid]['blockers_after']
        assert rows[rid]['execution_unlocked'] is False
    assert 'SOURCE_BRANCH_SET' in rows['CA04-397']['normalized_expression']
    assert 'SOURCE_BRANCH_SET' in rows['CA09-859']['normalized_expression']

def test_ca09847_dependency_repaired():
    r,c9=load(R),load(C9); rows={x['source_rule_id']:x for x in r['records']}; c={x['source_rule_id']:x for x in c9['records']}
    assert rows['CA09-847']['antecedent_rule_ids_after']==['CA09-846']
    assert 'ANTECEDENT_DEPENDENCY' in rows['CA09-847']['blockers_after']
    assert 'ANTECEDENT_SOURCE_CONDITION_RECHECK_REQUIRED' in rows['CA09-847']['blockers_after']
    assert c['CA09-847']['antecedent_mode']=='EXPLICIT_RULE_REFERENCE'
    assert c['CA09-847']['antecedent_rule_ids']==['CA09-846']

def test_duplicate_alias_recorded_without_deletion():
    r=load(R); rows={x['source_rule_id']:x for x in r['records']}
    assert rows['CA09-804']['duplicate_source_rule_of']=='CA08-799'
    assert rows['CA09-804']['blockers_after']==['PAIR_OR_CLOSED_GROUP_ACTIVATION_CONTEXTUAL_UNRESOLVED']
    assert r['guardrails']['duplicate_rule_deleted'] is False

def test_final_generic_row_semantics():
    r=load(R); rows={x['source_rule_id']:x for x in r['records']}
    assert rows['CA09-833']['blockers_after']==['CLOSED_CATEGORY_ACTIVATION_CONTEXTUAL_UNRESOLVED']
    assert 'AUXILIARY_SUPPORT_ACTIVATION_CONTEXTUAL_UNRESOLVED' in rows['CA09-840']['blockers_after']
    assert rows['CA09-849']['blockers_after']==['MIXED_VALENCE_COMPOSITION_UNSPECIFIED']
    assert rows['CA09-861']['blockers_after']==['OPEN_FUNCTIONAL_CATEGORY_MEMBERSHIP_OR_ACTIVATION_UNRESOLVED']
    assert rows['CA09-865']['blockers_after']==['OPEN_VALENCE_CATEGORY_ACTIVATION_CONTEXTUAL_UNRESOLVED']
    assert 'MIXED_VALENCE_COMPOSITION_UNSPECIFIED' in rows['CA09-885']['blockers_after']
    assert 'SOURCE_COMPOUND_COMPOSITION_UNSPECIFIED' in rows['CA09-886']['blockers_after']

def test_closure_v09_census_and_no_runtime_unlock():
    c8,c9=load(C8),load(C9)
    assert len(c8['records'])==251==len(c9['records'])
    assert c8['summary']['rows_with_no_current_activation_blocker']==21
    assert c9['summary']['rows_with_no_current_activation_blocker']==22
    assert c9['summary']['source_resolution_changes']==37
    assert c9['summary']['source_condition_repairs']==8
    assert c9['summary']['dependency_scope_corrections']==2
    assert c9['summary']['third_layer_source_local_resolved']==1
    assert c9['summary']['third_layer_source_branch_repairs']==3
    assert c9['summary']['third_layer_dependency_repairs']==1
    assert c9['summary']['conditions_compiled']==0
    assert c9['summary']['execution_unlocked']==0

def test_guardrails():
    g=load(R)['guardrails']
    for k in ['universal_any_default_added','universal_all_default_added','universal_n_of_default_added','global_pair_default_changed','global_closed_category_default_changed','source_compound_boolean_inserted','duplicate_rule_deleted','product_runtime_modified','github_actions_used']:
        assert g[k] is False

import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
R=ROOT/"knowledge/wp08/CAREER_SOURCE_DEEPEN_100_v0.1.json"
C9=ROOT/"knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251_v0.9.json"
C10=ROOT/"knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251_v0.10.json"

def load(p): return json.loads(p.read_text(encoding='utf-8'))

def test_exact_source_deepen_selection_100():
    r,c9=load(R),load(C9)
    expected=[]
    spec=[
      ('PAIR_OR_CLOSED_GROUP_ACTIVATION_CONTEXTUAL_UNRESOLVED',45),
      ('CLOSED_CATEGORY_ACTIVATION_CONTEXTUAL_UNRESOLVED',28),
      ('SOURCE_COMPOUND_COMPOSITION_UNSPECIFIED',12),
      ('VALENCE_STATE_CRITERION_UNSPECIFIED',8),
      ('OPEN_FUNCTIONAL_CATEGORY_MEMBERSHIP_OR_ACTIVATION_UNRESOLVED',5),
    ]
    for b,n in spec:
        rows=[x for x in c9['records'] if x['blockers']==[b]]
        assert len(rows)==n
        expected.extend(rows)
    expected.extend([x for x in c9['records'] if x['blockers']==['OPEN_VALENCE_CATEGORY_ACTIVATION_CONTEXTUAL_UNRESOLVED']][:2])
    assert len(expected)==100
    assert [x['source_rule_id'] for x in r['records']]==[x['source_rule_id'] for x in expected]

def test_ca06593_missing_kewen_blocker_restored():
    r=load(R); rows={x['source_rule_id']:x for x in r['records']}; x=rows['CA06-593']
    assert x['source_resolution_changed'] is True
    assert 'PAIR_OR_CLOSED_GROUP_ACTIVATION_CONTEXTUAL_UNRESOLVED' in x['blockers_after']
    assert 'CAREER_KEWEN_ACTIVATION_CONTEXTUAL_UNRESOLVED' in x['blockers_after']

def test_ca07700_carrier_ambiguity_is_explicit():
    r=load(R); x={z['source_rule_id']:z for z in r['records']}['CA07-700']
    assert x['source_resolution_changed'] is True
    assert 'TRANSFORMATION_CARRIER_UNSPECIFIED' in x['blockers_after']
    assert '文昌' in x['normalized_expression'] and '文曲' in x['normalized_expression']

def test_ca08702_same_star_transform_list_is_or_not_and():
    r=load(R); x={z['source_rule_id']:z for z in r['records']}['CA08-702']
    assert x['source_resolution_changed'] is True
    assert x['disposition']=='SOURCE_CONDITION_REPAIRED_STILL_BLOCKED'
    assert 'LOCAL_OR[TRANSFORM(巨门,化禄),TRANSFORM(巨门,化权)]' in x['normalized_expression']
    assert x['blockers_after']==['PAIR_OR_CLOSED_GROUP_ACTIVATION_CONTEXTUAL_UNRESOLVED']

def test_negative_evidence_is_preserved_fail_closed():
    r=load(R)
    changed={'CA06-593','CA07-700','CA08-702'}
    for x in r['records']:
        assert x['condition_compiled'] is False
        assert x['execution_unlocked'] is False
        if x['source_rule_id'] not in changed:
            assert x['blockers_after']==x['blockers_before']
    assert r['summary']['source_local_resolved']==0
    assert r['summary']['newly_no_blocker_rows']==0

def test_family_negative_findings():
    r=load(R)
    statuses={x['source_evidence_status'] for x in r['records']}
    assert 'NO_SOURCE_LOCAL_MEMBER_REALIZATION_EVIDENCE' in statuses
    assert 'CLOSED_MALEFIC_MEMBERSHIP_ACTIVATION_STILL_CONTEXTUAL' in statuses
    assert 'NO_SOURCE_BOOLEAN_COMPOSITION_EVIDENCE' in statuses
    assert 'NO_OPERATIONAL_VALENCE_CRITERION_IN_SOURCE' in statuses
    assert 'OPEN_FUNCTIONAL_MEMBERSHIP_REMAINS_OPEN' in statuses
    assert 'OPEN_VALENCE_MEMBERSHIP_REMAINS_OPEN' in statuses

def test_closure_v010_census():
    c9,c10=load(C9),load(C10)
    assert len(c9['records'])==251==len(c10['records'])
    assert c10['summary']['rows_with_no_current_activation_blocker']==22
    assert c10['summary']['rows_with_source_underdetermination']==202
    assert c10['summary']['source_resolution_changes']==40
    assert c10['summary']['source_condition_repairs']==9
    assert c10['summary']['dependency_scope_corrections']==2
    assert c10['summary']['fourth_layer_source_semantic_changes']==3
    assert c10['summary']['fourth_layer_source_local_resolved']==0
    assert c10['summary']['conditions_compiled']==0
    assert c10['summary']['execution_unlocked']==0
    assert c10['summary']['blocker_counts']['CAREER_KEWEN_ACTIVATION_CONTEXTUAL_UNRESOLVED']==5
    assert c10['summary']['blocker_counts']['TRANSFORMATION_CARRIER_UNSPECIFIED']==4

def test_guardrails():
    g=load(R)['guardrails']
    for k,v in g.items():
        assert v is False, k

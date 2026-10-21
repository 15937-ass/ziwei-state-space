import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
R=ROOT/"knowledge/wp08/CAREER_OPEN_CATEGORY_REFINEMENT_100_v0.1.json"
C7=ROOT/"knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251_v0.7.json"
C8=ROOT/"knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251_v0.8.json"

def load(p): return json.loads(p.read_text(encoding='utf-8'))

def test_exact_first_hundred_selection():
    r,c7=load(R),load(C7)
    all_open=[x for x in c7['records'] if 'OPEN_CATEGORY_MEMBER_OR_QUANTIFIER_UNSPECIFIED' in x['blockers']]
    assert len(all_open)==110
    assert len(r['records'])==100
    assert [x['source_rule_id'] for x in r['records']]==[x['source_rule_id'] for x in all_open[:100]]
    assert r['selection']['remaining_unselected_rule_ids']==[x['source_rule_id'] for x in all_open[100:]]

def test_generic_open_removed_but_no_false_ready():
    r=load(R)
    for x in r['records']:
        assert 'OPEN_CATEGORY_MEMBER_OR_QUANTIFIER_UNSPECIFIED' not in x['blockers_after']
        assert x['blockers_after']
        assert x['execution_unlocked'] is False
    assert r['summary']['generic_open_removed']==100
    assert r['summary']['blockers_cleared_to_zero']==0

def test_closed_vs_open_category_distinctions():
    r=load(R); rows={x['source_rule_id']:x for x in r['records']}
    assert 'CLOSED_CATEGORY_ACTIVATION_CONTEXTUAL_UNRESOLVED' in rows['CA03-238']['blockers_after']
    assert 'OPEN_VALENCE_CATEGORY_ACTIVATION_CONTEXTUAL_UNRESOLVED' in rows['CA03-231']['blockers_after']
    assert 'OPEN_FUNCTIONAL_CATEGORY_MEMBERSHIP_OR_ACTIVATION_UNRESOLVED' in rows['CA05-413']['blockers_after']
    assert 'AUXILIARY_SUPPORT_ACTIVATION_CONTEXTUAL_UNRESOLVED' in rows['CA08-784']['blockers_after']
    assert 'CLOSED_CATEGORY_ACTIVATION_CONTEXTUAL_UNRESOLVED' in rows['CA09-819']['blockers_after']

def test_compound_and_valence_semantics_preserved():
    r=load(R); rows={x['source_rule_id']:x for x in r['records']}
    for rid in ['CA02-184','CA03-225','CA04-316','CA05-442','CA07-691','CA08-723']:
        assert 'SOURCE_COMPOUND_COMPOSITION_UNSPECIFIED' in rows[rid]['blockers_after']
    for rid in ['CA03-256','CA03-257','CA03-258','CA04-304','CA04-305','CA06-508','CA08-771','CA08-772']:
        assert 'VALENCE_STATE_CRITERION_UNSPECIFIED' in rows[rid]['blockers_after']
    assert 'MIXED_VALENCE_COMPOSITION_UNSPECIFIED' in rows['CA03-246']['blockers_after']

def test_open_tail_elemental_and_thresholds():
    r=load(R); rows={x['source_rule_id']:x for x in r['records']}
    for rid in ['CA03-289','CA03-298']:
        assert 'SOURCE_OPEN_TAIL_MEMBERSHIP_UNSPECIFIED' in rows[rid]['blockers_after']
        assert 'SOURCE_LIST_QUANTIFIER_UNSPECIFIED' in rows[rid]['blockers_after']
    assert 'ELEMENTAL_CATEGORY_MEMBERSHIP_UNSPECIFIED' in rows['CA04-345']['blockers_after']
    assert 'CARDINALITY_THRESHOLD_UNSPECIFIED' in rows['CA04-345']['blockers_after']
    assert 'SEVERITY_THRESHOLD_UNSPECIFIED' in rows['CA04-366']['blockers_after']
    assert 'CARDINALITY_THRESHOLD_UNSPECIFIED' in rows['CA07-632']['blockers_after']

def test_closure_v08_census():
    c7,c8=load(C7),load(C8)
    assert len(c7['records'])==251==len(c8['records'])
    assert c7['summary']['blocker_counts']['OPEN_CATEGORY_MEMBER_OR_QUANTIFIER_UNSPECIFIED']==110
    assert c8['summary']['blocker_counts']['OPEN_CATEGORY_MEMBER_OR_QUANTIFIER_UNSPECIFIED']==10
    assert c8['summary']['rows_with_no_current_activation_blocker']==21
    assert c8['summary']['open_category_refinement_target_rows']==100
    assert c8['summary']['open_category_refinement_blockers_cleared_to_zero']==0
    assert c8['summary']['conditions_compiled']==0
    assert c8['summary']['execution_unlocked']==0

def test_guardrails():
    g=load(R)['guardrails']
    assert g['universal_any_default_added'] is False
    assert g['universal_all_default_added'] is False
    assert g['universal_n_of_default_added'] is False
    assert g['open_valence_membership_closed'] is False
    assert g['open_functional_membership_closed'] is False
    assert g['source_compound_boolean_inserted'] is False
    assert g['numeric_threshold_invented'] is False
    assert g['product_runtime_modified'] is False
    assert g['github_actions_used'] is False

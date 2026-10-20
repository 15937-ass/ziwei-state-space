import csv
import json
from pathlib import Path

import pytest

from src.product.condition_atoms import ALLOWED_ATOM_TYPES, compile_condition_spec
from src.product.palace_structure import load_palace_ontology, resolve_palace_structure

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'knowledge/wp07a/CAREER_ZIWEI_ZIPO_STATIC_8_MAP_v0.1.json'
BRANCHES = '子丑寅卯辰巳午未申酉戌亥'
PALACES = ['命宫','兄弟宫','夫妻宫','子女宫','财帛宫','疾厄宫','迁移宫','交友宫','事业宫','田宅宫','福德宫','父母宫']
IDS = ['CA01-047','CA01-050','CA01-083','CA01-087','CA01-088','CA01-089','CA01-093','CA01-095']
MUTAGENS = {'CA01-087':'禄','CA01-088':'禄','CA01-089':'权'}
TARGETS = ['independent_responsibility','independent_work_or_department_responsibility',
           'career_favors_creation_over_preservation','career_changes_frequent',
           'extra_work_or_multiple_responsibilities_common','career_setbacks_or_turbulence',
           'broad_spending_or_scale_can_exceed_actual_return','career_creation_receives_more_assistance']


def document():
    return json.loads(PATH.read_text())


def mapping(rid):
    return next(x for x in document()['mappings'] if x['source_rule_id']==rid)


def required(rid):
    stars = ['紫微'] if rid in IDS[:2] else ['紫微','破军']
    if rid=='CA01-095': stars += ['左辅','右弼']
    return [{'name':s, **({'mutagen':MUTAGENS[rid]} if s=='破军' and rid in MUTAGENS else {})} for s in stars]


def snapshot(branch, placements):
    offset = (BRANCHES.index(branch)-8)%12
    return {'schema_version':'0.2','engine':{'name':'ziwei-static-test','version':'1','adapter_version':'0.2'},'input':{},'natal':{'palaces':{
        BRANCHES[(i+offset)%12]: {'name':name,'stem':'甲','branch':BRANCHES[(i+offset)%12],
            'is_body_palace':False,'major_stars':placements.get(f'P{i+1:02}',[]),'minor_stars':[],'adjective_stars':[]}
        for i,name in enumerate(PALACES)}}}


def matches(rid, branch='丑', placements=None):
    facts = resolve_palace_structure(snapshot(branch, placements if placements is not None else {'P09':required(rid)}),
        load_palace_ontology(ROOT/'knowledge/wp05/palace_ontology_v0.1.csv')).runtime_facts()
    return compile_condition_spec(mapping(rid)['condition']).matches(facts)


def test_exact_scope_source_and_progress_counts():
    doc=document()
    with (ROOT/'validation/wp05/CA01_career_projection_review_001_100.csv').open(encoding='utf-8-sig',newline='') as h:
        rows={r['projection_rule_id']:r for r in csv.DictReader(h)}
    assert [m['source_rule_id'] for m in doc['mappings']] == doc['scope']['nominated_source_rule_ids'] == IDS
    for rid,target in zip(IDS,TARGETS):
        m=mapping(rid);r=rows[rid];p=m['source_provenance']
        for key in ('source_id','source_location','review_status','time_layer','history_feedback'): assert p[key]==r[key]
        assert p['source_span_verified'] is True and r['source_span_verified']=='true'
        assert p['case_support_only'] is False and r['case_support_only']=='false'
        assert p['time_layer']=='NATAL' and p['source_id']=='SRC-ZZ-003'
        assert m['source_condition_text']==r['condition']
        assert m['expected_projection']=={k:r[k] for k in ('projection_domain','projection_target','projection_mode')}
        assert m['expected_projection']['projection_target']==target
        assert m['source_anchor_printed_page']==(133 if rid in IDS[:2] else 134)
        assert m['source_anchor_pdf_page']==67
        assert m['executable_registry_entry'] is False
    before=set()
    # This is the historical predecessor snapshot, not a live count of future units.
    for name in ['CAREER_CONTEXT_MAP_CA01_020_v0.1.json', 'CAREER_CONTEXT_MAP_CA01_035_043_045_v0.1.json', 'CAREER_CROSS_PALACE_MAP_CA01_066_CA02_188_CA03_255_v0.1.json', 'CAREER_DIRECT_TRANSFORM_MAP_CA04_CA09_v0.1.json', 'CAREER_NATAL_ATOMIZATION_MAP_v0.1.json', 'CAREER_NATAL_TRANSFORMATION_MAP_CA01_CA03_v0.1.json', 'CAREER_SPOUSE_KONGJIE_CA01_023_v0.1.json', 'CAREER_STAR_PRESENCE_MAP_CA01_026_044_v0.1.json']:
        f = ROOT/'knowledge/wp07a'/name
        if f==PATH: continue
        before.update(x['source_rule_id'] for x in json.loads(f.read_text()).get('mappings',[]))
    assert not before.intersection(IDS)
    counts=doc['progress_counts']
    assert counts['structured_rule_records_before']==len(before)==44
    assert counts['structured_rule_records_after']==len(before|set(IDS))==52
    assert counts['source_rules_rechecked_this_unit']==counts['new_unique_condition_mappings']==8
    assert counts['career_source_reviewed_before']==counts['career_source_reviewed_after']==888
    assert counts['blocked_rows_this_unit']==counts['new_production_executable_rules']==0


@pytest.mark.parametrize('rid',IDS)
def test_all_twelve_branch_positions_and_complete_alternatives(rid):
    for b in BRANCHES:
        assert matches(rid,b)==(rid in IDS[:2] or b in '丑未')
    condition=mapping(rid)['condition']
    specs=[condition['all_of']] if rid in IDS[:2] else condition['alternatives']
    assert len(specs)==(1 if rid in IDS[:2] else 2)
    for atoms in specs:
        assert all(a['atom_type'] in ALLOWED_ATOM_TYPES and a['args']['palace']=='P09' for a in atoms)
        assert {a['args']['star'] for a in atoms if a['atom_type']=='PALACE_HAS_STAR'}=={s['name'] for s in required(rid)}
    if rid not in IDS[:2]:
        assert {next(a['args']['branch'] for a in atoms if a['atom_type']=='BRANCH_PRESENT') for atoms in specs}=={'丑','未'}


@pytest.mark.parametrize('rid',IDS)
def test_each_required_star_missing_or_in_another_palace_fails(rid):
    for missing in required(rid):
        remaining=[s for s in required(rid) if s['name']!=missing['name']]
        assert not matches(rid,placements={'P09':remaining})
        for i in range(1,13):
            if i!=9: assert not matches(rid,placements={'P09':remaining,f'P{i:02}':[missing]})
    assert not matches(rid,placements={'P09':[{'name':'天府'}]})


@pytest.mark.parametrize('rid',sorted(MUTAGENS))
def test_named_transformation_cannot_be_missing_wrong_or_rebound(rid):
    for mutagen in (None,'禄','权','科','忌'):
        if mutagen==MUTAGENS[rid]: continue
        stars=[{'name':'紫微'},{'name':'破军',**({'mutagen':mutagen} if mutagen else {})}]
        assert not matches(rid,placements={'P09':stars})
    assert not matches(rid,placements={'P09':[{'name':'紫微','mutagen':MUTAGENS[rid]},{'name':'破军'}]})
    assert not matches(rid,placements={'P09':[{'name':'紫微'},{'name':'破军'}], 'P05':[{'name':'破军','mutagen':MUTAGENS[rid]}]})


def test_inherited_and_unconditional_within_paragraph_scopes_are_distinct():
    assert mapping('CA01-088')['source_context']['inherited_source_rule_ids']==['CA01-083','CA01-087']
    assert mapping('CA01-088')['condition']==mapping('CA01-087')['condition']
    # 无论如何 broadens the preceding sub-branch, while retaining 丑未 and the named star system.
    assert mapping('CA01-093')['source_context']['inherited_source_rule_ids']==['CA01-083']
    for mutagen in (None,'禄','权','忌'):
        assert matches('CA01-093',placements={'P09':[{'name':'紫微'},{'name':'破军',**({'mutagen':mutagen} if mutagen else {})}]})
    assert not matches('CA01-093','申')
    for rid in IDS[:2]:
        assert '不' in mapping(rid)['source_span_summary']
    registry=json.loads((ROOT/'product/PL3N_CAREER_DOMAIN_PROVIDER_v0.1.json').read_text())
    assert not set(IDS).intersection(registry['rules'])
    assert all(m['execution_readiness']=='STATIC_PROJECTION_CANDIDATE_NOT_EXECUTABLE' for m in document()['mappings'])

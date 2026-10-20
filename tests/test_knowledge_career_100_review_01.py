"""One hundred source reviews; incomplete context can never become an outcome condition."""
import copy
import csv
import json
from collections import Counter
from pathlib import Path

import pytest

from src.product.condition_atoms import ALLOWED_ATOM_TYPES, compile_condition_spec, fact_from_atom
from src.product.palace_structure import load_palace_ontology, resolve_palace_structure

ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'knowledge/wp07a/CAREER_100_REVIEW_01_v0.1.json'
DOC=json.loads(PATH.read_text())
RECORDS={m['source_rule_id']:m for m in DOC['mappings']}
BRANCHES='子丑寅卯辰巳午未申酉戌亥'
PALACES=['命宫','兄弟宫','夫妻宫','子女宫','财帛宫','疾厄宫','迁移宫','交友宫','事业宫','田宅宫','福德宫','父母宫']
FULL={67:'子午',68:'子午',72:'子午',76:'子午',77:'子午',84:'丑未',102:'寅申',103:'寅申',104:'寅申',105:'寅申',109:'寅申',110:'寅申',111:'寅申',112:'卯酉',114:'卯酉',119:'卯酉',120:'卯酉',122:'卯酉',124:'卯酉',128:'辰戌'}
def rule_id(n):return ('CA01-' if n<=100 else 'CA02-')+f'{n:03}'


def source_rows():
    result=[]
    for path in sorted((ROOT/'validation/wp05').glob('CA*_career_projection_review_*.csv')):
        with path.open(encoding='utf-8-sig',newline='') as h:result.extend(csv.DictReader(h))
    return result


def alternatives(condition):
    common=condition.get('all_of',[])
    return [common+branch for branch in condition['alternatives']] if condition.get('alternatives') else [common]


def snapshot_for(atoms,forced_branch=None):
    branch=forced_branch or next((a['args']['branch'] for a in atoms if a['atom_type']=='BRANCH_PRESENT' and a['args']['palace']=='P09'),'申')
    stars={}
    for a in atoms:
        if a['atom_type'] in ('PALACE_HAS_STAR','TRANSFORMATION_PRESENT'):
            args=a['args'];stars.setdefault(args['palace'],{}).setdefault(args['star'],{'name':args['star']})
            if a['atom_type']=='TRANSFORMATION_PRESENT':stars[args['palace']][args['star']]['mutagen']=args['mutagen']
    offset=(BRANCHES.index(branch)-8)%12
    return {'schema_version':'0.2','engine':{'name':'batch-review-test','version':'1','adapter_version':'0.2'},'input':{},'natal':{'palaces':{
        BRANCHES[(i+offset)%12]:{'name':name,'stem':'甲','branch':BRANCHES[(i+offset)%12],'is_body_palace':False,'major_stars':list(stars.get(f'P{i+1:02}',{}).values()),'minor_stars':[],'adjective_stars':[]}
        for i,name in enumerate(PALACES)}}}


def runtime_facts(snapshot):
    return resolve_palace_structure(snapshot,load_palace_ontology(ROOT/'knowledge/wp05/palace_ontology_v0.1.csv')).runtime_facts()


def test_exact_hundred_selection_and_nonoverlapping_historical_counts():
    before=set()
    for path in DOC['baseline_mapping_paths']:
        before.update(m['source_rule_id'] for m in json.loads((ROOT/path).read_text())['mappings'])
    expected=[r['projection_rule_id'] for r in source_rows() if r['projection_rule_id'] not in before][:100]
    assert len(before)==52
    assert len(RECORDS)==len(DOC['mappings'])==100
    assert list(RECORDS)==DOC['scope']['nominated_source_rule_ids']==expected
    assert not before.intersection(RECORDS)
    assert len(before|set(RECORDS))==152
    assert DOC['scope']['reasoning_sub_batches']==[50,50]
    assert Counter(m['review_sub_batch'] for m in RECORDS.values())=={1:50,2:50}
    counts=DOC['progress_counts']
    assert counts['source_rules_rechecked']==100
    assert counts['first_time_complete_condition_mappings']==20
    assert counts['methodology_or_context_only']==30
    assert counts['blocked_outcome_mappings']==50
    assert counts['new_production_executable_rules']==0
    assert counts['canonical_source_reviewed_before']==counts['canonical_source_reviewed_after']==888
    assert counts['unique_structured_rule_records_before']==52
    assert counts['unique_structured_rule_records_after']==152


@pytest.mark.parametrize('rid',list(RECORDS))
def test_each_review_preserves_exact_canonical_record_and_individual_reason(rid):
    r=next(x for x in source_rows() if x['projection_rule_id']==rid);m=RECORDS[rid]
    assert m['source_record']==r
    assert m['source_condition_text']==r['condition']
    p=m['source_provenance']
    for k in ('source_id','source_location','review_status','time_layer','history_feedback'):assert p[k]==r[k]
    assert p['source_span_verified']==(r['source_span_verified']=='true')
    assert p['case_support_only']==(r['case_support_only']=='true')
    assert m['expected_projection']=={k:r[k] for k in ('projection_domain','projection_target','projection_mode')}
    spans={s['span_id']:s for s in DOC['source_spans']}
    assert m['source_span_ids'] and set(m['source_span_ids'])<=set(spans)
    assert all(spans[s]['visual_reviewed'] and spans[s]['extracted_text_not_silently_corrected'] for s in m['source_span_ids'])
    assert len(m['review_reason_zh'])>18
    assert m['executable_registry_entry'] is False
    if m['condition'] is None:
        assert m['blocker_code'] and m['execution_readiness'].startswith('BLOCKED_')
        assert m['source_context']['context_is_complete_antecedent'] is False
    else:assert m['review_disposition']=='COMPLETE_CONDITION_MAPPING'


@pytest.mark.parametrize('number',list(FULL))
def test_each_complete_rule_actual_runtime_alternatives_and_required_facts(number):
    m=RECORDS[rule_id(number)];c=m['condition'];compiled=compile_condition_spec(c)
    for atoms in alternatives(c):
        assert atoms
        assert all(a['atom_type'] in ALLOWED_ATOM_TYPES for a in atoms)
        snap=snapshot_for(atoms);facts=runtime_facts(snap)
        assert compiled.matches(facts)
        for atom in atoms:
            assert not compiled.matches(frozenset(facts-{fact_from_atom(atom["atom_type"], **atom["args"])}))
        for b in BRANCHES:
            assert compiled.matches(runtime_facts(snapshot_for(atoms,b)))==(b in FULL[number])
        # Named stars and transformations must remain bound to their palaces/carriers.
        for branch,palace in snap['natal']['palaces'].items():
            for star in palace['major_stars']:
                changed=copy.deepcopy(snap)
                changed['natal']['palaces'][branch]['major_stars'].remove(star)
                assert not compiled.matches(runtime_facts(changed))
                if star.get('mutagen'):
                    for wrong in ('禄','权','科','忌'):
                        if wrong==star['mutagen']:continue
                        mutated=copy.deepcopy(snap)
                        next(x for x in mutated['natal']['palaces'][branch]['major_stars'] if x['name']==star['name'])['mutagen']=wrong
                        assert not compiled.matches(runtime_facts(mutated))


def test_opposite_allocations_and_conditional_inheritance_are_exact():
    assert len(alternatives(RECORDS['CA01-068']['condition']))==8
    assert len(alternatives(RECORDS['CA02-124']['condition']))==4
    for rid in ('CA01-068','CA02-124'):
        for atoms in alternatives(RECORDS[rid]['condition']):
            rel=[a for a in atoms if a['atom_type']=='PALACE_RELATION']
            assert rel==[{'atom_type':'PALACE_RELATION','args':{'source':'P09','target':'P03','relation':'OPPOSITE'}}]
    prior=json.loads((ROOT/'knowledge/wp07a/CAREER_CROSS_PALACE_MAP_CA01_066_CA02_188_CA03_255_v0.1.json').read_text())['mappings'][0]
    assert RECORDS['CA01-067']['condition']==prior['condition']
    assert RECORDS['CA01-077']['condition']==RECORDS['CA01-076']['condition']
    assert RECORDS['CA02-105']['condition']==RECORDS['CA02-104']['condition']
    assert RECORDS['CA02-120']['condition']==RECORDS['CA02-119']['condition']
    assert {k for k,v in RECORDS.items() if v['condition'] is not None}=={rule_id(n) for n in FULL}


def test_unrepresented_behaviors_groups_timing_and_methods_cannot_become_empty_conditions():
    examples={'CA01-011':'VALENCE','CA01-018':'EXAMPLE','CA01-024':'ACTION','CA01-028':'ACTION',
              'CA01-037':'RELATION','CA01-040':'COMPOSITE','CA01-046':'TEMPORAL','CA01-061':'RELATION',
              'CA01-075':'ACTION','CA01-096':'RELATION','CA02-101':'COMPOSITE','CA02-115':'TEMPORAL',
              'CA02-116':'GROUP','CA02-121':'TEMPORAL','CA02-126':'RELATION'}
    for rid,code in examples.items():
        assert RECORDS[rid]['condition'] is None and RECORDS[rid]['blocker_code']==code
        assert RECORDS[rid]['review_disposition']=='BLOCKED_OUTCOME_MAPPING'
    for rid in ('CA01-048','CA01-049','CA01-069','CA01-090','CA02-129'):
        assert RECORDS[rid]['condition'] is None
        assert RECORDS[rid]['review_disposition']=='METHODOLOGY_OR_CONTEXT_ONLY'
    assert DOC['status']=='HUNDRED_RULE_REVIEW_COMPLETE_NOT_PRODUCTION'
    assert DOC['progress_counts']['new_production_executable_rules']==0
    assert DOC['guardrails']['production_registry_modified'] is False
    assert all(m['executable_registry_entry'] is False for m in RECORDS.values())
    assert DOC['guardrails']['null_condition_must_not_be_coerced_to_empty'] is True

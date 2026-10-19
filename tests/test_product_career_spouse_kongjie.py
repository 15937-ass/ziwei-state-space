"""寅申+opposition+split 空劫: actual Product execution and source context."""
import copy
from dataclasses import replace
import json
from pathlib import Path

import pytest

from src.product.career_inference_report import build_career_inference_report
from src.product.career_inference_service import run_career_inference
from src.product.career_natal_domain_provider import load_default_career_natal_provider, load_career_source_mappings
from tests.test_product_career_cross_palace import snapshot

ROOT=Path(__file__).resolve().parents[1]
MP='knowledge/wp07a/CAREER_SPOUSE_KONGJIE_CA01_023_v0.1.json'
MAPPING=json.loads((ROOT/MP).read_text())['mappings'][0]
REGISTRY=json.loads((ROOT/'product/PL3N_CAREER_DOMAIN_PROVIDER_v0.1.json').read_text())


@pytest.mark.parametrize('career_star,spouse_star',[('地空','地劫'),('地劫','地空')])
def test_both_allocations_across_all_branches_and_exact_report_context(career_star,spouse_star):
    for branch in '子丑寅卯辰巳午未申酉戌亥':
        value=snapshot(branch,{'P09':[(career_star,None)],'P03':[(spouse_star,None)]})
        before=copy.deepcopy(value)
        run=run_career_inference(ROOT,value,target_id='T-DEMO',question='事业夫妻空劫条件与来源范围')
        report=build_career_inference_report(ROOT,run)
        active={r['rule_id']:r for r in report['natal']['active_rules']}
        assert ('CA01-023' in active)==(branch in {'寅','申'})
        if branch in {'寅','申'}:
            item=active['CA01-023']
            assert item['source_context']==MAPPING['source_context']
            assert item['source_summary']==MAPPING['source_context']['normalized_reading']
            assert 'OCR 噪声' in item['source_context']['source_scope_note']
            assert item['source_context']['branch_gate_reading']=='此唯寅申两宫有之'
            assert item['source']['source_location']==MAPPING['source_provenance']['source_location']
            assert item['projection']=={k:MAPPING['expected_projection']['projection_'+k] for k in ('domain','target','mode')}
        assert report['real_world_event_prediction_supported'] is False
        assert report['temporal']['matched_reaction_rule_ids']==[]
        assert run.status=='PARTIAL_TEMPORAL_REGISTRY_EMPTY'
        assert value==before


@pytest.mark.parametrize('branch',['寅','申'])
@pytest.mark.parametrize('career_star,spouse_star',[('地空','地劫'),('地劫','地空')])
def test_missing_or_misplaced_stars_and_wrong_spouse_branch_do_not_match(branch,career_star,spouse_star):
    provider=load_default_career_natal_provider(ROOT)
    stars={'P09':[(career_star,None)],'P03':[(spouse_star,None)]}
    def matches(value):return 'CA01-023' in {r.rule_id for r in provider.build_domain_evidence(value,question='跨宫负例').active_rules}
    assert matches(snapshot(branch,stars))
    for palace in ('P09','P03'):
        missing=copy.deepcopy(stars);star=missing.pop(palace)[0]
        assert not matches(snapshot(branch,missing))
        for other in (f'P{i:02d}' for i in range(1,13) if f'P{i:02d}'!=palace):
            misplaced=copy.deepcopy(missing);misplaced.setdefault(other,[]).append(star)
            assert not matches(snapshot(branch,misplaced))
    value=snapshot(branch,stars)
    palaces=value['natal']['palaces'];spouse=next(p for p in palaces.values() if p['name']=='夫妻')
    other=next(p for p in palaces.values() if p['name']=='兄弟')
    spouse['name'],other['name']=other['name'],spouse['name']
    # Move star with the spouse label: only its branch prerequisite is now wrong.
    spouse['major_stars'],other['major_stars']=other['major_stars'],spouse['major_stars']
    assert not matches(value)


def test_relation_is_an_independent_required_runtime_fact():
    provider=load_default_career_natal_provider(ROOT)
    value=snapshot('寅',{'P09':[('地空',None)],'P03':[('地劫',None)]})
    assert 'CA01-023' in {r.rule_id for r in provider.build_domain_evidence(value,question='关系正例').active_rules}
    entries=dict(provider.palace_ontology.entries)
    entries['P09']=replace(entries['P09'],opposite_palace_id='P02')
    # In-memory negative fixture only; no ontology file or production semantics edit.
    missing_relation=replace(provider,palace_ontology=replace(provider.palace_ontology,entries=entries))
    assert 'CA01-023' not in {r.rule_id for r in missing_relation.build_domain_evidence(value,question='缺对宫关系').active_rules}


@pytest.mark.parametrize('mutation,error',[
    ('missing_context','complete source context'),('empty_context','complete source context'),
    ('context_drift','drift in source context'),('unpinned_context','drift in source context'),
    ('relation_drop','condition atoms'),('branch_drop','condition atoms'),
])
def test_context_and_structural_gates_cannot_drift(tmp_path,mutation,error):
    registry=copy.deepcopy(REGISTRY)
    for meta in [registry['source_mapping'],*registry['additional_source_mappings']]:
        p=tmp_path/meta['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((ROOT/meta['path']).read_bytes())
    p=tmp_path/MP;doc=json.loads(p.read_text());mapping=doc['mappings'][0];rule=registry['rules']['CA01-023']
    if mutation=='missing_context':del mapping['source_context']
    if mutation=='empty_context':mapping['source_context']['normalized_reading']=' '
    if mutation=='context_drift':mapping['source_context']['branch_gate_reading']='任意宫支'
    if mutation=='unpinned_context':del rule['expected_source_context']
    if mutation=='relation_drop':rule['condition']['all_of']=[]
    if mutation=='branch_drop':rule['condition']['alternatives'][0].pop(1)
    p.write_text(json.dumps(doc,ensure_ascii=False))
    with pytest.raises(ValueError,match=error):load_career_source_mappings(tmp_path,registry)

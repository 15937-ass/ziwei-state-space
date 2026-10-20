"""All eight Ziwei/Zipo candidates through the actual Product API/report."""
import copy
import json
from pathlib import Path

import pytest

from src.product.career_inference_report import build_career_inference_report
from src.product.career_inference_service import run_career_inference
from src.product.career_natal_domain_provider import load_career_source_mappings, load_default_career_natal_provider
from tests.test_product_career_cross_palace import snapshot

ROOT=Path(__file__).resolve().parents[1]
MP='knowledge/wp07a/CAREER_ZIWEI_ZIPO_STATIC_8_MAP_v0.1.json'
MAPPING=json.loads((ROOT/MP).read_text())
REGISTRY=json.loads((ROOT/'product/PL3N_CAREER_DOMAIN_PROVIDER_v0.1.json').read_text())


def requirements(mapping):
    c=mapping['condition'];groups=c.get('alternatives',[c.get('all_of',[])])
    atoms=groups[0]
    stars={a['args']['star']:None for a in atoms if a['atom_type']=='PALACE_HAS_STAR'}
    for a in atoms:
        if a['atom_type']=='TRANSFORMATION_PRESENT':stars[a['args']['star']]=a['args']['mutagen']
    return stars


@pytest.mark.parametrize('mapping',MAPPING['mappings'],ids=lambda m:m['source_rule_id'])
def test_all_branches_and_source_context_through_api_and_report(mapping):
    stars=requirements(mapping)
    allowed=set(mapping['source_context']['required_branch_gate']) or set('子丑寅卯辰巳午未申酉戌亥')
    for branch in '子丑寅卯辰巳午未申酉戌亥':
        value=snapshot(branch,{'P09':list(stars.items())});before=copy.deepcopy(value)
        run=run_career_inference(ROOT,value,target_id='T-DEMO',question='紫微紫破原局性质与来源范围')
        report=build_career_inference_report(ROOT,run)
        active={r['rule_id']:r for r in report['natal']['active_rules']}
        rid=mapping['source_rule_id'];assert (rid in active)==(branch in allowed)
        if rid in active:
            item=active[rid]
            assert item['source_context']==mapping['source_context']
            assert item['source_summary']==mapping['source_span_summary']
            assert item['condition']==mapping['source_condition_text']
            assert item['source']['source_location']==mapping['source_provenance']['source_location']
            assert item['projection']=={k:mapping['expected_projection']['projection_'+k] for k in ('domain','target','mode')}
        assert value==before
        assert run.status=='PARTIAL_TEMPORAL_REGISTRY_EMPTY'
        assert report['real_world_event_prediction_supported'] is False
        assert report['temporal']['matched_reaction_rule_ids']==[]


@pytest.mark.parametrize('mapping',MAPPING['mappings'],ids=lambda m:m['source_rule_id'])
def test_each_required_star_palace_mutagen_and_named_carrier(mapping):
    provider=load_default_career_natal_provider(ROOT);stars=requirements(mapping);rid=mapping['source_rule_id']
    branch=(mapping['source_context']['required_branch_gate'] or ['子'])[0]
    def matches(st):return rid in {r.rule_id for r in provider.build_domain_evidence(snapshot(branch,st),question='完整前提验收').active_rules}
    assert matches({'P09':list(stars.items())})
    for star,mutagen in stars.items():
        remaining=[(s,m) for s,m in stars.items() if s!=star]
        assert not matches({'P09':remaining})
        for i in range(1,13):
            if i!=9:assert not matches({'P09':remaining,f'P{i:02d}':[(star,mutagen)]})
        if mutagen:
            for replacement in [None,*[m for m in '禄权科忌' if m!=mutagen]]:
                assert not matches({'P09':[(s,replacement if s==star else m) for s,m in stars.items()]})
            # An unrelated carrier cannot supply the required 破军 transformation.
            wrong=[(s,None if s==star else mutagen if s=='紫微' else m) for s,m in stars.items()]
            assert not matches({'P09':wrong})


def test_scope_and_explanation_boundaries_are_visible_in_report():
    run=run_career_inference(ROOT,snapshot('丑',{'P09':[('紫微',None),('破军','禄'),('左辅',None),('右弼',None)]}),target_id='T-DEMO',question='完整分支')
    active={r['rule_id']:r for r in build_career_inference_report(ROOT,run)['natal']['active_rules']}
    assert {'CA01-047','CA01-050','CA01-083','CA01-087','CA01-088','CA01-093','CA01-095'}<=set(active)
    assert 'CA01-089' not in active
    assert '不等于可以自行经营' in active['CA01-047']['source_summary']
    assert '或关系' in active['CA01-050']['source_summary']
    assert active['CA01-088']['source_context']['inherited_source_rule_ids']==['CA01-083','CA01-087']
    assert '不额外继承前句化禄' in active['CA01-093']['source_summary']
    # 093 remains in the general paragraph branch even without any transformation.
    neutral=run_career_inference(ROOT,snapshot('丑',{'P09':[('紫微',None),('破军',None)]}),target_id='T-DEMO',question='段落总范围')
    assert 'CA01-093' in {r.rule_id for r in neutral.natal_profile.domains[0].active_rules}


@pytest.mark.parametrize('mutation,error',[
    ('missing_modality','complete source context'),('scope_drift','drift in source context'),
    ('inheritance_drift','drift in source context'),('unknown_schema','unsupported source context schema'),
    ('invalid_branch','invalid paragraph context scope'),('condition_drop','condition atoms'),
])
def test_paragraph_context_and_conditions_fail_closed(tmp_path,mutation,error):
    registry=copy.deepcopy(REGISTRY)
    for meta in [registry['source_mapping'],*registry['additional_source_mappings']]:
        p=tmp_path/meta['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((ROOT/meta['path']).read_bytes())
    p=tmp_path/MP;doc=json.loads(p.read_text());ctx=doc['mappings'][0]['source_context']
    if mutation=='missing_modality':del ctx['modality_note']
    if mutation=='scope_drift':ctx['source_scope_note']='必然担任领袖'
    if mutation=='inheritance_drift':doc['mappings'][4]['source_context']['inherited_source_rule_ids']=[]
    if mutation=='unknown_schema':registry['additional_source_mappings'][-1]['source_context_schema']='UNKNOWN'
    if mutation=='invalid_branch':ctx['required_branch_gate']=['无']
    if mutation=='condition_drop':registry['rules']['CA01-088']['condition']['alternatives'][0].pop(2)
    p.write_text(json.dumps(doc,ensure_ascii=False))
    with pytest.raises(ValueError,match=error):load_career_source_mappings(tmp_path,registry)

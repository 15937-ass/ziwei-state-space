"""Cross-palace compound conditions through source-pinned provider and API."""
import copy
import json
from pathlib import Path

import pytest

from src.product.career_inference_report import build_career_inference_report
from src.product.career_inference_service import run_career_inference
from src.product.career_natal_domain_provider import load_default_career_natal_provider, load_career_source_mappings
from tests.test_product_career_natal_domain_provider import _full_snapshot, _star

ROOT = Path(__file__).resolve().parents[1]
MP = 'knowledge/wp07a/CAREER_CROSS_PALACE_MAP_CA01_066_CA02_188_CA03_255_v0.1.json'
MAPPING = json.loads((ROOT / MP).read_text())
REGISTRY = json.loads((ROOT / 'product/PL3N_CAREER_DOMAIN_PROVIDER_v0.1.json').read_text())
CASES = [
    ('CA01-066', {'P09':[('紫微',None)],'P05':[('廉贞','禄')]}, {'子','午'}),
    ('CA02-188', {'P09':[('天机','禄')],'P05':[('太阴','忌')]}, {'午'}),
    ('CA03-255', {'P09':[('天机','科')],'P01':[('天同',None),('巨门','忌')]}, set('子丑寅卯辰巳午未申酉戌亥')),
]
NAMES = ['命','兄弟','夫妻','子女','财帛','疾厄','迁移','交友','事业','田宅','福德','父母']


def snapshot(branch, stars):
    value = _full_snapshot()
    palaces = value['natal']['palaces']
    branches = list('子丑寅卯辰巳午未申酉戌亥')
    offset = (branches.index(branch)-8)%12
    for index, name in enumerate(NAMES):
        p = palaces[branches[(index+offset)%12]]
        p['name'] = name
        p['major_stars'] = [_star(s,m) for s,m in stars.get(f'P{index+1:02d}',[])]
    return value


@pytest.mark.parametrize('rule_id,stars,allowed',CASES,ids=[c[0] for c in CASES])
def test_complete_cross_palace_condition_and_branch_gates_in_api_report(rule_id,stars,allowed):
    mapping = next(m for m in MAPPING['mappings'] if m['source_rule_id']==rule_id)
    for branch in '子丑寅卯辰巳午未申酉戌亥':
        value = snapshot(branch,stars);before = copy.deepcopy(value)
        run = run_career_inference(ROOT,value,target_id='T-DEMO',question='跨宫复合条件验收')
        report = build_career_inference_report(ROOT,run)
        active = {r['rule_id']:r for r in report['natal']['active_rules']}
        assert (rule_id in active) == (branch in allowed)
        if rule_id in active:
            item = active[rule_id]
            assert item['source_summary']==mapping['source_span_summary']
            assert item['condition']==mapping['source_condition_text']
            assert item['source']['source_id']==mapping['source_provenance']['source_id']
            assert item['source']['source_location']==mapping['source_provenance']['source_location']
            assert item['projection']=={k:mapping['expected_projection']['projection_'+k] for k in ('domain','target','mode')}
            assert item['projection']['mode']=='CROSS_PALACE_CONSTRAINT'
        assert run.status=='PARTIAL_TEMPORAL_REGISTRY_EMPTY'
        assert report['real_world_event_prediction_supported'] is False
        assert report['temporal']['matched_reaction_rule_ids']==[]
        assert value==before


@pytest.mark.parametrize('rule_id,stars,allowed',CASES,ids=[c[0] for c in CASES])
def test_every_star_and_mutagen_is_required_in_its_own_palace(rule_id,stars,allowed):
    provider=load_default_career_natal_provider(ROOT)
    branch=sorted(allowed)[0]
    def matches(st):
        return rule_id in {r.rule_id for r in provider.build_domain_evidence(snapshot(branch,st),question='跨宫负例').active_rules}
    assert matches(stars)
    for palace,group in stars.items():
        for index,(star,mutagen) in enumerate(group):
            missing=copy.deepcopy(stars);del missing[palace][index]
            assert not matches(missing)
            for other in (f'P{i:02d}' for i in range(1,13) if f'P{i:02d}'!=palace):
                misplaced=copy.deepcopy(missing);misplaced.setdefault(other,[]).append((star,mutagen))
                assert not matches(misplaced)
            if mutagen:
                for replacement in [None,*[x for x in '禄权科忌' if x!=mutagen]]:
                    wrong=copy.deepcopy(stars);wrong[palace][index]=(star,replacement)
                    assert not matches(wrong)


def test_exact_three_selected_and_unreviewed_extensions_absent():
    meta=next(m for m in REGISTRY['additional_source_mappings'] if m['path']==MP)
    assert set(meta['selected_rule_ids'])=={c[0] for c in CASES}
    assert len(load_career_source_mappings(ROOT,REGISTRY))==35
    assert not {'CA01-020','CA01-064','CA01-065'} & set(REGISTRY['rules'])


@pytest.mark.parametrize('mutation,error',[
    ('entry_status','provenance'),('source_status','reviewed non-executable'),
    ('branch_drop','condition atoms'),('palace_drift','condition atoms'),
    ('projection','projection_target'),('blocked','readiness'),
])
def test_cross_handoff_rejects_entry_status_and_compound_condition_drift(tmp_path,mutation,error):
    registry=copy.deepcopy(REGISTRY)
    for meta in [registry['source_mapping'],*registry['additional_source_mappings']]:
        p=tmp_path/meta['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((ROOT/meta['path']).read_bytes())
    path=tmp_path/MP;mapping=json.loads(path.read_text());rule=registry['rules']['CA01-066']
    if mutation=='entry_status':mapping['mappings'][0]['mapping_status']='MAPPED_EXISTING_ATOM'
    if mutation=='source_status':mapping['status']='SOURCE_GROUNDED_MAPPING_COMPLETE_NOT_EXECUTABLE'
    if mutation=='branch_drop':rule['condition']['alternatives'][0].pop(1)
    if mutation=='palace_drift':rule['condition']['alternatives'][0][-1]['args']['palace']='P09'
    if mutation=='projection':rule['expected_projection_target']='venture_will_succeed'
    if mutation=='blocked':mapping['mappings'][0]['execution_readiness']='BLOCKED_UNKNOWN'
    path.write_text(json.dumps(mapping,ensure_ascii=False))
    with pytest.raises(ValueError,match=error):load_career_source_mappings(tmp_path,registry)

"""Source modality and same-palace conjunctions through actual Career execution."""
import copy
import json
from pathlib import Path

import pytest

from src.product.career_inference_service import run_career_inference
from src.product.career_inference_report import build_career_inference_report
from src.product.career_natal_domain_provider import load_career_source_mappings, load_default_career_natal_provider
from tests.test_product_career_natal_domain_provider import _full_snapshot, _star

ROOT = Path(__file__).resolve().parents[1]
MP = 'knowledge/wp07a/CAREER_STAR_PRESENCE_MAP_CA01_026_044_v0.1.json'
MAPPING = json.loads((ROOT / MP).read_text())
REGISTRY = json.loads((ROOT / 'product/PL3N_CAREER_DOMAIN_PROVIDER_v0.1.json').read_text())
IDS = {'CA01-026', 'CA01-027', 'CA01-031', 'CA01-032', 'CA01-033', 'CA01-034', 'CA01-042', 'CA01-044'}


def snapshot(stars_by_palace, branch='子'):
    value = _full_snapshot()
    palaces = value['natal']['palaces']
    career = next(p for p in palaces.values() if p['name'] == '事业')
    career['name'], palaces[branch]['name'] = palaces[branch]['name'], career['name']
    for p in palaces.values():
        # Presence facts must cover non-major stars without inventing mutagens.
        p['adjective_stars'] = [_star(s) for s in sorted(stars_by_palace.get(p['name'], set()))]
    return value


@pytest.mark.parametrize('mapping', MAPPING['mappings'], ids=lambda m:m['source_rule_id'])
def test_each_presence_rule_matches_and_report_retains_exact_modality(mapping):
    required = {a['args']['star'] for a in mapping['condition']['all_of']}
    for branch in '子丑寅卯辰巳午未申酉戌亥':
        value = snapshot({'事业': required}, branch)
        before = copy.deepcopy(value)
        run = run_career_inference(ROOT, value, target_id='T-DEMO', question='事业星曜条件与来源限定')
        report = build_career_inference_report(ROOT, run)
        item = next(x for x in report['natal']['active_rules'] if x['rule_id'] == mapping['source_rule_id'])
        assert item['source_modality_note'] == mapping['source_modality_note']
        assert item['source_summary'] == mapping['source_span_summary']
        assert item['source']['source_location'] == mapping['source_provenance']['source_location']
        assert item['projection'] == {k:mapping['expected_projection']['projection_'+k] for k in ('domain','target','mode')}
        assert report['status'] == 'PARTIAL_TEMPORAL_REGISTRY_EMPTY'
        assert report['temporal']['matched_reaction_rule_ids'] == []
        assert report['real_world_event_prediction_supported'] is False
        assert value == before


@pytest.mark.parametrize('mapping', MAPPING['mappings'], ids=lambda m:m['source_rule_id'])
def test_every_required_star_missing_or_in_any_other_palace_fails(mapping):
    provider = load_default_career_natal_provider(ROOT)
    required = {a['args']['star'] for a in mapping['condition']['all_of']}
    names = [p['name'] for p in snapshot({})['natal']['palaces'].values() if p['name'] != '事业']
    for missing in required:
        for other in [None, *names]:
            stars = {'事业':required - {missing}}
            if other: stars[other] = {missing}
            evidence = provider.build_domain_evidence(snapshot(stars), question='同宫条件负例')
            assert mapping['source_rule_id'] not in {r.rule_id for r in evidence.active_rules}


def test_shared_conditions_preserve_distinct_targets_and_three_star_refinement():
    def active(stars):
        run = run_career_inference(ROOT,snapshot({'事业':set(stars)}),target_id='T-DEMO',question='复合条件验收')
        return {r['rule_id']:r for r in build_career_inference_report(ROOT,run)['natal']['active_rules']}
    kongjie = active(['地空','地劫'])
    assert set(kongjie) == {'CA01-026','CA01-027'}
    assert len({r['projection']['target'] for r in kongjie.values()}) == 2
    assert set(active(['陀罗'])) == {'CA01-031','CA01-032','CA01-033'}
    assert set(active(['禄存'])) == {'CA01-042'}
    assert set(active(['禄存','地空','地劫'])) == {'CA01-026','CA01-027','CA01-042','CA01-044'}
    assert active([]) == {}
    assert not {'CA01-035','CA01-043','CA01-045'} & set(REGISTRY['rules'])
    assert {m['source_rule_id'] for m in MAPPING['mappings']} == IDS


@pytest.mark.parametrize('mutation,error', [
    ('unknown_status','approved reviewed'), ('source_status','reviewed non-executable'),
    ('missing_modality','modality note is required'), ('empty_modality','modality note is required'),
    ('modality_drift','drift in source modality'), ('condition_drift','condition atoms'),
    ('readiness','readiness'),
])
def test_star_handoff_rejects_status_modality_and_condition_drift(tmp_path,mutation,error):
    registry = copy.deepcopy(REGISTRY)
    for meta in [registry['source_mapping'], *registry['additional_source_mappings']]:
        path = tmp_path / meta['path'];path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes((ROOT / meta['path']).read_bytes())
    mapping_path = tmp_path / MP
    mapping = json.loads(mapping_path.read_text())
    meta = next(m for m in registry['additional_source_mappings'] if m['path'] == MP)
    if mutation == 'unknown_status': meta['mapping_status'] = 'UNREVIEWED'
    if mutation == 'source_status': mapping['status'] = 'UNREVIEWED'
    if mutation == 'missing_modality': del mapping['mappings'][0]['source_modality_note']
    if mutation == 'empty_modality': mapping['mappings'][0]['source_modality_note'] = ' '
    if mutation == 'modality_drift': mapping['mappings'][0]['source_modality_note'] = '必然如此'
    if mutation == 'condition_drift': registry['rules']['CA01-026']['condition'] = {'all_of': []}
    if mutation == 'readiness': mapping['mappings'][0]['execution_readiness'] = 'BLOCKED_UNKNOWN'
    mapping_path.write_text(json.dumps(mapping,ensure_ascii=False))
    with pytest.raises(ValueError,match=error): load_career_source_mappings(tmp_path,registry)

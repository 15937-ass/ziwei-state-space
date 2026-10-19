"""Six source-pinned CA04–CA09 rules through the real API and report."""
import copy
import json
from pathlib import Path

import pytest

from src.product.career_inference_report import build_career_inference_report
from src.product.career_inference_service import run_career_inference
from src.product.career_natal_domain_provider import load_career_source_mappings, load_default_career_natal_provider
from tests.test_product_career_static_expansion import snapshot

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = json.loads((ROOT / 'product/PL3N_CAREER_DOMAIN_PROVIDER_v0.1.json').read_text())
PATH = 'knowledge/wp07a/CAREER_DIRECT_TRANSFORM_MAP_CA04_CA09_v0.1.json'
MAPPING = json.loads((ROOT / PATH).read_text())
SELECTED_IDS = {'CA04-327', 'CA05-469', 'CA07-671', 'CA07-672', 'CA07-673', 'CA08-765'}
SELECTED = [m for m in MAPPING['mappings'] if m['source_rule_id'] in SELECTED_IDS]


def test_handoff_activates_exact_six_static_candidates_and_keeps_prior_seventeen():
    meta = next(m for m in REGISTRY['additional_source_mappings'] if m['path'] == PATH)
    assert set(meta['selected_rule_ids']) == SELECTED_IDS
    assert set(REGISTRY['rules']) - SELECTED_IDS == {
        'CA04-347', 'CA04-349', 'CA09-852', 'CA01-052', 'CA01-053',
        'CA01-054', 'CA01-055', 'CA01-070', 'CA01-071', 'CA01-078',
        'CA02-155', 'CA02-160', 'CA03-252', 'CA03-254', 'CA03-279', 'CA03-283', 'CA03-285',
    }
    assert all(m['execution_readiness'] == 'STATIC_PROJECTION_CANDIDATE_NOT_EXECUTABLE' for m in SELECTED)
    assert len(load_career_source_mappings(ROOT, REGISTRY)) == 23


@pytest.mark.parametrize('mapping', SELECTED, ids=lambda m: m['source_rule_id'])
def test_each_rule_through_api_report_and_all_branch_positions(mapping):
    transform = mapping['condition']['all_of'][0]['args']
    for branch in '子丑寅卯辰巳午未申酉戌亥':
        value = snapshot(transform['star'], transform['mutagen'], branch)
        before = copy.deepcopy(value)
        run = run_career_inference(ROOT, value, target_id='T-DEMO', question='事业性质与来源限定')
        report = build_career_inference_report(ROOT, run)
        active = {r['rule_id']: r for r in report['natal']['active_rules']}
        item = active[mapping['source_rule_id']]
        assert item['source_summary'] == mapping['source_span_summary']
        assert item['condition'] == mapping['source_condition_text']
        assert item['source']['source_id'] == mapping['source_provenance']['source_id']
        assert item['source']['source_location'] == mapping['source_provenance']['source_location']
        assert item['projection'] == {k: mapping['expected_projection']['projection_'+k] for k in ('domain', 'target', 'mode')}
        assert run.status == 'PARTIAL_TEMPORAL_REGISTRY_EMPTY'
        assert run.blockers == ('PRODUCTION_TEMPORAL_REACTION_REGISTRY_EMPTY',)
        assert report['temporal']['matched_reaction_rule_ids'] == []
        assert report['real_world_event_prediction_supported'] is False
        assert value == before


@pytest.mark.parametrize('mapping', SELECTED, ids=lambda m: m['source_rule_id'])
def test_each_rule_requires_correct_star_mutagen_and_palace(mapping):
    transform = mapping['condition']['all_of'][0]['args']
    provider = load_default_career_natal_provider(ROOT)
    for star, mutagen, palace in [
        (transform['star'], None, '事业'),
        (transform['star'], next(x for x in '禄权科忌' if x != transform['mutagen']), '事业'),
        ('文昌', transform['mutagen'], '事业'),
        (transform['star'], transform['mutagen'], '命'),
    ]:
        evidence = provider.build_domain_evidence(snapshot(star, mutagen, '子', palace), question='负例')
        assert mapping['source_rule_id'] not in {r.rule_id for r in evidence.active_rules}


@pytest.mark.parametrize('blocked', ['CA05-403', 'CA08-766'])
def test_timing_and_path_targets_are_rejected_even_if_manually_selected(blocked):
    registry = copy.deepcopy(REGISTRY)
    meta = next(m for m in registry['additional_source_mappings'] if m['path'] == PATH)
    meta['selected_rule_ids'].append(blocked)
    registry['rules'][blocked] = copy.deepcopy(registry['rules']['CA08-765'])
    with pytest.raises(ValueError, match='execution readiness'):
        load_career_source_mappings(ROOT, registry)


def test_scene_and_success_limitations_are_present_in_actual_report_summaries():
    cases = [('廉贞', '忌', 'CA05-469', '不是疾病或伤害事件预测'),
             ('巨门', '忌', 'CA07-673', '不应直接推为官非诉讼'),
             ('巨门', '权', 'CA07-672', '不把表达优势升级为必然职业成功')]
    for star, mutagen, rule_id, limitation in cases:
        run = run_career_inference(ROOT, snapshot(star, mutagen, '子'), target_id='T-DEMO', question='来源限制验收')
        report = build_career_inference_report(ROOT, run)
        item = next(r for r in report['natal']['active_rules'] if r['rule_id'] == rule_id)
        assert limitation in item['source_summary']
        assert report['real_world_event_prediction_supported'] is False

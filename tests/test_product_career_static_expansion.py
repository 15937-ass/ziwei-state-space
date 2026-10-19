"""Real provider/API gates for the explicit CA01–CA03 static handoff."""
import copy
import json
from pathlib import Path

import pytest

from src.product.career_natal_domain_provider import load_default_career_natal_provider, load_career_source_mappings
from src.product.career_inference_service import run_career_inference
from src.product.career_inference_report import build_career_inference_report
from tests.test_product_career_natal_domain_provider import _full_snapshot, _star

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = json.loads((ROOT / 'product/PL3N_CAREER_DOMAIN_PROVIDER_v0.1.json').read_text())
MAPPING_PATH = 'knowledge/wp07a/CAREER_NATAL_TRANSFORMATION_MAP_CA01_CA03_v0.1.json'
MAPPING = json.loads((ROOT / MAPPING_PATH).read_text())
SELECTED = [m for m in MAPPING['mappings'] if m['execution_readiness'] == 'STATIC_PROJECTION_CANDIDATE_NOT_EXECUTABLE']


def snapshot(star, mutagen, branch, palace='事业'):
    value = _full_snapshot()
    palaces = value['natal']['palaces']
    current = next(p for p in palaces.values() if p['name'] == palace)
    other = palaces[branch]
    current['name'], other['name'] = other['name'], current['name']
    other['major_stars'] = [_star(star, mutagen)]
    return value


@pytest.mark.parametrize('mapping', SELECTED, ids=lambda m: m['source_rule_id'])
def test_each_new_rule_exact_condition_across_all_branches_and_negative_bindings(mapping):
    provider = load_default_career_natal_provider(ROOT)
    condition = mapping['condition']
    alternatives = condition.get('alternatives', [condition.get('all_of', [])])
    transform = next(a['args'] for a in alternatives[0] if a['atom_type'] == 'TRANSFORMATION_PRESENT')
    branches = {a['args']['branch'] for alt in alternatives for a in alt if a['atom_type'] == 'BRANCH_PRESENT'}
    for branch in '子丑寅卯辰巳午未申酉戌亥':
        value = snapshot(transform['star'], transform['mutagen'], branch)
        before = copy.deepcopy(value)
        run = run_career_inference(ROOT, value, target_id='T-DEMO', question='事业本命映射验收')
        report = build_career_inference_report(ROOT, run)
        active = {r['rule_id']: r for r in report['natal']['active_rules']}
        expected = not branches or branch in branches
        assert (mapping['source_rule_id'] in active) == expected
        if expected:
            item = active[mapping['source_rule_id']]
            assert item['source_summary'] == mapping['source_span_summary']
            assert item['condition'] == mapping['source_condition_text']
            assert item['source']['source_location'] == mapping['source_provenance']['source_location']
            assert item['projection'] == {k: mapping['expected_projection']['projection_'+k] for k in ('domain','target','mode')}
        assert value == before
        assert run.status == 'PARTIAL_TEMPORAL_REGISTRY_EMPTY'
        assert report['real_world_event_prediction_supported'] is False
        assert report['temporal']['matched_reaction_rule_ids'] == []
    branch = next(iter(branches), '子')
    for value in [snapshot(transform['star'], None, branch), snapshot('文昌', transform['mutagen'], branch), snapshot(transform['star'], transform['mutagen'], branch, palace='命')]:
        evidence = provider.build_domain_evidence(value, question='负例')
        assert mapping['source_rule_id'] not in {r.rule_id for r in evidence.active_rules}


def test_path_and_event_dependent_rules_cannot_be_selected():
    for blocked in ('CA02-158', 'CA02-164', 'CA02-194'):
        registry = copy.deepcopy(REGISTRY)
        meta = registry['additional_source_mappings'][0]
        meta['selected_rule_ids'].append(blocked)
        registry['rules'][blocked] = copy.deepcopy(registry['rules']['CA02-160'])
        with pytest.raises(ValueError, match='execution readiness'):
            load_career_source_mappings(ROOT, registry)


@pytest.mark.parametrize('mutation,error', [
    ('condition', 'condition atoms'), ('projection', 'projection_target'),
    ('source', 'source_location'), ('duplicate', 'disjoint'),
    ('uncovered', 'cover every'), ('escape', 'inside repository'),
])
def test_expanded_handoff_fails_closed_on_drift(mutation, error):
    registry = copy.deepcopy(REGISTRY)
    rule = registry['rules']['CA01-070']
    if mutation == 'condition': rule['condition'] = {'all_of': []}
    if mutation == 'projection': rule['expected_projection_target'] = 'unsupported'
    if mutation == 'source': rule['expected_source_location'] = 'unsupported'
    if mutation == 'duplicate': registry['additional_source_mappings'].append(registry['source_mapping'])
    if mutation == 'uncovered': registry['rules']['UNMAPPED'] = rule
    if mutation == 'escape': registry['additional_source_mappings'][0]['path'] = '../outside.json'
    with pytest.raises(ValueError, match=error):
        load_career_source_mappings(ROOT, registry)

"""Source-context fidelity; chart context must not become a complete outcome rule."""
import csv
import json
from pathlib import Path

import pytest

from src.product.condition_atoms import ALLOWED_ATOM_TYPES, compile_condition_spec
from src.product.palace_structure import load_palace_ontology, resolve_palace_structure
from src.product.career_natal_domain_provider import load_default_career_natal_provider

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'knowledge/wp07a/CAREER_CONTEXT_MAP_CA01_035_043_045_v0.1.json'
SOURCE = ROOT / 'validation/wp05/CA01_career_projection_review_001_100.csv'
ONTOLOGY = ROOT / 'knowledge/wp05/palace_ontology_v0.1.csv'
PALACES = ['命宫', '兄弟宫', '夫妻宫', '子女宫', '财帛宫', '疾厄宫',
           '迁移宫', '交友宫', '事业宫', '田宅宫', '福德宫', '父母宫']
IDS = {'CA01-035', 'CA01-043', 'CA01-045'}
EXPECTED_CONTEXT = {'CA01-043': {'禄存'}, 'CA01-045': {'禄存', '地空', '地劫'}}


def document():
    return json.loads(PATH.read_text())


def mapping(rule_id):
    return next(x for x in document()['mappings'] if x['source_rule_id'] == rule_id)


def snapshot(stars_by_palace):
    branches = '子丑寅卯辰巳午未申酉戌亥'
    return {'schema_version': '0.2',
            'engine': {'name': 'context-audit', 'version': '1', 'adapter_version': '0.2'},
            'input': {}, 'natal': {'palaces': {
                branch: {'name': name, 'stem': '甲', 'branch': branch, 'is_body_palace': False,
                         'major_stars': [], 'minor_stars': [],
                         'adjective_stars': [{'name': s} for s in stars_by_palace.get(f'P{i:02}', [])]}
                for i, (branch, name) in enumerate(zip(branches, PALACES), 1)}}}


def matches_context(rule_id, placements):
    spec = mapping(rule_id)['source_context']['chart_context_spec']
    facts = resolve_palace_structure(snapshot(placements), load_palace_ontology(ONTOLOGY)).runtime_facts()
    return compile_condition_spec(spec).matches(facts)


def test_exact_source_fields_and_projection_preserved():
    with SOURCE.open(encoding='utf-8-sig', newline='') as h:
        rows = {x['projection_rule_id']: x for x in csv.DictReader(h)}
    doc = document()
    assert len(doc['mappings']) == len(IDS)
    assert {x['source_rule_id'] for x in doc['mappings']} == IDS
    assert set(doc['scope']['nominated_source_rule_ids']) == IDS
    for m in doc['mappings']:
        row = rows[m['source_rule_id']]
        p = m['source_provenance']
        for k in ('source_id', 'source_location', 'review_status', 'time_layer', 'history_feedback'):
            assert p[k] == row[k]
        assert p['source_id'] == 'SRC-ZZ-003'
        assert p['review_status'] == 'SOURCE_SPAN_VERIFIED'
        assert p['time_layer'] == 'NATAL'
        assert p['source_span_verified'] is True and row['source_span_verified'] == 'true'
        assert p['case_support_only'] is False and row['case_support_only'] == 'false'
        assert m['source_condition_text'] == row['condition']
        assert m['expected_projection'] == {k: row[k] for k in (
            'projection_domain', 'projection_target', 'projection_mode')}
        assert m['source_anchor_printed_page'] == 133
        assert m['source_anchor_pdf_page'] == 67


@pytest.mark.parametrize('rule_id', sorted(EXPECTED_CONTEXT))
def test_context_requires_all_stars_bound_to_career(rule_id):
    required = EXPECTED_CONTEXT[rule_id]
    spec = mapping(rule_id)['source_context']['chart_context_spec']
    assert set(spec) == {'all_of'}
    assert {a['args']['star'] for a in spec['all_of']} == required
    assert all(a['atom_type'] == 'PALACE_HAS_STAR' and a['atom_type'] in ALLOWED_ATOM_TYPES
               and a['args']['palace'] == 'P09' for a in spec['all_of'])
    assert matches_context(rule_id, {'P09': sorted(required)})
    assert not matches_context(rule_id, {})
    for star in required:
        remaining = sorted(required - {star})
        assert not matches_context(rule_id, {'P09': remaining})
        for i in range(1, 13):
            pid = f'P{i:02}'
            if pid != 'P09':
                assert not matches_context(rule_id, {'P09': remaining, pid: [star]})


def test_methodological_warning_is_not_wealth_negation():
    m = mapping('CA01-043')
    ctx = m['source_context']
    assert ctx['inherited_source_rule_ids'] == ['CA01-042']
    assert ctx['methodological_force'] == 'INSUFFICIENT_BASIS_FOR_WEALTH_INFERENCE'
    assert ctx['wealth_outcome_assertion'] is None
    assert m['expected_projection']['projection_mode'] == 'STRUCTURAL_CONSTRAINT'
    assert m['expected_projection']['projection_target'] == 'lucun_in_career_does_not_itself_imply_wealth'
    assert {'WEALTH_ABSENT', 'WEALTH_NEGATIVE', 'POOR', 'LUCUN_ALONE_SUFFICIENT_FOR_WEALTH'} == set(ctx['forbidden_reinterpretations'])
    assert matches_context('CA01-043', {'P09': ['禄存']})
    assert matches_context('CA01-043', {'P09': ['禄存', '地空', '地劫']})
    assert ctx['required_non_chart_prerequisites'] == []
    assert m['condition'] is None


def test_action_cannot_be_deduced_from_complete_chart_context():
    m = mapping('CA01-045')
    ctx = m['source_context']
    assert ctx['inherited_source_rule_ids'] == ['CA01-042', 'CA01-044']
    assert matches_context('CA01-045', {'P09': ['禄存', '地空', '地劫']})
    assert ctx['action_prerequisite_required'] is True
    assert ctx['context_completeness'] == 'CHART_CONTEXT_COMPLETE_FULL_ANTECEDENT_INCOMPLETE'
    assert ctx['required_non_chart_prerequisites'] == [{
        'text': '勉强求变', 'kind': 'ACTION_PREREQUISITE',
        'source_status': 'EXPLICIT_IN_SOURCE_SENTENCE',
        'representation_status': 'UNREPRESENTED_BY_APPROVED_CHART_FACTS',
        'satisfied_by_chart_context_alone': False,
    }]
    assert m['condition'] is None
    assert m['outcome_condition_compilation_supported'] is False
    assert m['execution_readiness'] == 'BLOCKED_NON_CHART_ACTION_PREREQUISITE'


def test_fire_bell_interpretations_remain_unselected():
    m = mapping('CA01-035')
    ctx = m['source_context']
    assert m['condition'] is None and ctx['chart_context_spec'] is None
    assert ctx['resolution_status'] == 'INSUFFICIENT_SOURCE_IN_REVIEWED_PASSAGE'
    assert {x['interpretation_id'] for x in ctx['unresolved_interpretations']} == {'BOTH_STARS', 'EITHER_STAR'}
    assert all(x['selected'] is False for x in ctx['unresolved_interpretations'])
    assert m['execution_readiness'] == 'BLOCKED_FIRE_BELL_AND_OR_UNRESOLVED'


def test_no_audit_record_can_be_selected_as_a_production_outcome_rule():
    doc = document()
    assert doc['validation']['executable_outcome_conditions'] == 0
    assert doc['validation']['executable_registry_entries'] == 0
    assert doc['validation']['reviewed_rows'] == 3
    assert doc['validation']['context_recovered_rows'] == 2
    assert doc['validation']['shorthand_unresolved_rows'] == 1
    assert doc['consumer_boundary']['production_selection_allowed'] is False
    assert doc['consumer_boundary']['null_condition_must_not_be_coerced_to_empty_condition'] is True
    assert doc['consumer_boundary']['chart_context_spec_is_complete_outcome_condition'] is False
    for m in doc['mappings']:
        assert m['condition'] is None
        assert m['executable_registry_entry'] is False
        assert m['outcome_condition_compilation_supported'] is False
        assert m['execution_readiness'].startswith('BLOCKED_')
    registry = json.loads((ROOT / 'product/PL3N_CAREER_DOMAIN_PROVIDER_v0.1.json').read_text())
    assert not IDS.intersection(registry['rules'])
    evidence = load_default_career_natal_provider(ROOT).build_domain_evidence(
        snapshot({'P09': ['禄存', '地空', '地劫', '火星', '铃星']}), question='来源语境边界验收')
    assert not IDS.intersection(x.rule_id for x in evidence.active_rules)

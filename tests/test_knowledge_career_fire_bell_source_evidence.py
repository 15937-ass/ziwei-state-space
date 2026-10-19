"""Quantifier evidence remains passage-specific; no implicit Career promotion."""
import csv
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'knowledge/wp07a/CAREER_FIRE_BELL_SOURCE_EVIDENCE_v0.1.json'
EXPECTED = {
    'FB01': ('SRC-ZZ-001', 21, 41, 'NOT_EXPRESSED'),
    'FB02': ('SRC-ZZ-002', 87, 173, 'NOT_EXPRESSED'),
    'FB03': ('SRC-ZZ-002', 87, 173, 'EXPLICIT_OR'),
    'FB04': ('SRC-ZZ-002', 88, 174, 'BOTH_FOR_THIS_FLANKING_STRUCTURE'),
    'FB05': ('SRC-ZZ-002', 72, 142, 'LOCAL_SEPARATE_DISCUSSION_NO_UNIVERSAL_QUANTIFIER'),
    'FB06': ('SRC-ZZ-001', 65, 129, 'EXPLICIT_OR'),
    'FB07': ('SRC-ZZ-001', 65, 129, 'EXPLICIT_BOTH'),
    'FB08': ('SRC-ZZ-003', 67, 133, 'NOT_EXPRESSED'),
}


def document():
    return json.loads(PATH.read_text())


def evidence():
    return {x['evidence_id']: x for x in document()['evidence']}


def test_bounded_scope_and_unique_evidence_ids():
    d = document()
    assert len(d['evidence']) == len(evidence()) == d['scope']['reviewed_spans'] == 8
    assert set(evidence()) == set(EXPECTED)
    assert d['scope']['reviewed_spans'] <= d['scope']['max_review_spans'] == 10
    assert d['scope']['target_source_rule_ids'] == ['CA01-035']
    assert d['scope']['not_exhaustive_search'] is True
    assert set(d['scope']['approved_source_ids']) == {'SRC-ZZ-001', 'SRC-ZZ-002', 'SRC-ZZ-003'}


@pytest.mark.parametrize('evidence_id', sorted(EXPECTED))
def test_each_visual_span_has_approved_source_and_exact_page_anchor(evidence_id):
    with (ROOT / 'sources/source_index.csv').open(encoding='utf-8-sig', newline='') as h:
        sources = {x['source_id']: x for x in csv.DictReader(h)}
    e = evidence()[evidence_id]
    sid, physical, printed, quantifier = EXPECTED[evidence_id]
    src = sources[sid]
    assert src['school'] == '中州派' and src['role_in_paper1'] == 'core'
    assert e['source_id'] == sid
    assert e['source_title'] == src['title']
    assert e['source_attachment_sha256'] == src['file_sha256']
    assert e['pdf_page'] == physical <= int(src['pdf_pages'])
    assert e['printed_page'] == printed
    assert e['local_quantifier_finding'] == quantifier
    assert e['source_span_verified'] is True
    assert e['review_method'] == 'DIRECT_PDF_VISUAL_REVIEW'
    assert e['source_epistemic'] == 'EXPLICIT'
    assert e['source_excerpt'] and e['page_region'] and e['source_local_scope'] and e['transfer_limit']
    assert e['target_applicable_quantifier_evidence'] is False


def test_explicit_or_and_both_are_kept_in_their_different_local_scopes():
    es = evidence()
    assert '火星或铃星' in es['FB03']['source_excerpt']
    assert '火星或铃星' in es['FB06']['source_excerpt']
    assert '同时见火星铃星' in es['FB07']['source_excerpt']
    assert es['FB06']['source_local_scope'] != es['FB07']['source_local_scope']
    # The same page has different qualified clauses, so page identity cannot license transfer.
    assert es['FB06']['source_id'] == es['FB07']['source_id']
    assert es['FB06']['printed_page'] == es['FB07']['printed_page'] == 129
    assert document()['findings']['explicit_or_examples'] == ['FB03', 'FB06']
    assert document()['findings']['explicit_both_example'] == ['FB07']


def test_flanking_relation_is_not_replaced_with_same_palace_conjunction():
    e = evidence()['FB04']
    assert e['source_excerpt'] == '火铃分居命宫两邻宫'
    assert e['evidence_category'] == 'EXPLICIT_TWO_STAR_SPATIAL_STRUCTURE'
    assert e['condition'] is None
    assert '两邻宫' in e['transfer_limit']
    assert document()['findings']['two_star_flanking_example'] == ['FB04']


def test_local_separate_star_reading_is_transparent_inference():
    e = evidence()['FB05']
    assert '铃星同度最坏，火星同度次之' in e['source_excerpt']
    assert e['normalization_epistemic'] == 'INFERRED_FROM_LOCAL_EXPOSITION'
    assert e['normalization_note']
    assert document()['findings']['universal_and_supported'] is False
    assert document()['findings']['universal_or_supported'] is False


def test_target_source_unchanged_and_insufficient_evidence_does_not_compile():
    d = document()
    with (ROOT / 'validation/wp05/CA01_career_projection_review_001_100.csv').open(
            encoding='utf-8-sig', newline='') as h:
        source = next(x for x in csv.DictReader(h) if x['projection_rule_id'] == 'CA01-035')
    assert d['target_source'] == source
    assert source['condition'] == '事业宫见火铃'
    assert source['projection_target'] == 'career_setbacks_before_stabilization'
    assert d['findings']['target_passage'] == 'FB08'
    assert d['findings']['identified_stars'] == ['火星', '铃星']
    assert d['findings']['star_identity_supported'] is True
    assert d['findings']['target_quantifier'] == 'UNRESOLVED'
    assert d['findings']['target_condition'] is None
    assert d['findings']['target_evidence_sufficiency'] == 'INSUFFICIENT_FOR_TARGET_SPECIFIC_QUANTIFIER'
    assert d['findings']['target_execution_readiness'] == 'BLOCKED_FIRE_BELL_AND_OR_UNRESOLVED'
    prior = json.loads((ROOT / 'knowledge/wp07a/CAREER_CONTEXT_MAP_CA01_035_043_045_v0.1.json').read_text())
    target = next(x for x in prior['mappings'] if x['source_rule_id'] == 'CA01-035')
    assert target['condition'] is None
    assert target['execution_readiness'] == d['findings']['target_execution_readiness']
    assert target['executable_registry_entry'] is False


def test_dossier_is_not_production_rules_or_new_default_semantics():
    d = document()
    assert d['guardrails']['role'] == 'AUDIT_ONLY_SOURCE_EVIDENCE'
    assert d['guardrails']['conditions_compiled'] == 0
    assert d['guardrails']['production_selection_allowed'] is False
    assert d['guardrails']['new_semantic_default_frozen'] is False
    assert d['findings']['executable_registry_entry'] is False
    assert all(e['condition'] is None and e['executable_registry_entry'] is False for e in d['evidence'])
    registry = json.loads((ROOT / 'product/PL3N_CAREER_DOMAIN_PROVIDER_v0.1.json').read_text())
    assert 'CA01-035' not in registry['rules']

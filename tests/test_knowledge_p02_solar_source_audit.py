import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'knowledge/palaces/P02_siblings/wp05/SIBLINGS_SB03_SOLAR_SOURCE_AUDIT_v0.1.json'


def load():
    return json.loads(PATH.read_text())


def test_prior_source_and_gap_ledgers_are_byte_preserved_with_disjoint_new_ids():
    d = load()
    previous = []
    for pin in d['accepted_input_pins']:
        raw = (ROOT / pin['path']).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == pin['sha256'] and pin['read_only']
        previous += json.loads(raw)['records']
    assert len(previous) == 83
    assert [r['projection_rule_id'] for r in d['records']] == [f'P02S-{i:03d}' for i in range(84, 135)]
    assert not ({r['projection_rule_id'] for r in previous} & {r['projection_rule_id'] for r in d['records']})


def test_source_counts_and_gap_coverage_include_all_unresolved_atoms_once():
    d = load()
    rs = {r['projection_rule_id']: r for r in d['records']}
    assert {r['source_anchor'] for r in rs.values()} == {f'S{i:02d}' for i in range(1, 22)}
    held = {rid for rid, r in rs.items() if not r['canonical_promotion']}
    covered = []
    for g in d['source_coverage_gaps']:
        assert g['normalized_term'] is None and g['local_work_can_continue'] and g['reason']
        for rid in g['affected_record_ids']:
            assert rs[rid]['gap_id'] == g['gap_id'] and not rs[rid]['normalization_verified']
            assert rs[rid]['normalization_epistemic'] == 'UNRESOLVED'
        covered += g['affected_record_ids']
    assert len(covered) == len(set(covered)) == len(held) == 17
    assert set(covered) == held
    assert sum(r['canonical_promotion'] for r in rs.values()) == 34
    assert sum(r['canonical_promotion'] and r['case_support_only'] for r in rs.values()) == 7
    assert sum(r['canonical_promotion'] and not r['case_support_only'] for r in rs.values()) == 27
    assert d['summary']['durable_review_object_count'] == len(rs) + 4 <= 100
    assert all(b['count'] <= 50 for b in d['summary']['reasoning_sub_batches'])


def test_cross_page_quote_and_different_transformation_subjects_are_preserved():
    rs = {r['projection_rule_id']: r for r in load()['records']}
    cross = rs['P02S-105']
    assert cross['printed_page'] == 26 and cross['printed_page_end'] == 27
    assert cross['pdf_physical_page'] == 13 and cross['pdf_physical_page_end'] == 14
    assert cross['source_literal_claim'] == '有极大纠纷'
    assert '丑宫' in rs['P02S-099']['condition'] and '太阳化忌' in rs['P02S-099']['condition']
    assert '未宫' in rs['P02S-100']['condition'] and '太阴化忌' in rs['P02S-100']['condition']
    for rid in ('P02S-103', 'P02S-104', 'P02S-105'):
        assert rs[rid]['gap_id'].endswith('C02')
    assert rs['P02S-108']['condition'] == '申宫苦' and rs['P02S-108']['gap_id'].endswith('L01')
    assert rs['P02S-119']['source_literal_claim'] == '且主助力'


def test_year_dual_and_unspecified_periods_cannot_collapse_or_release_conditions():
    rs = {r['projection_rule_id']: r for r in load()['records']}
    for rid in ('P02S-097', 'P02S-098'):
        assert rs[rid]['time_layer'] is None
        assert rs[rid]['source_time_layers'] == ['DECADE', 'YEAR']
        assert rs[rid]['gap_id'].endswith('T02')
    assert rs['P02S-092']['time_layer'] is None and rs['P02S-092']['source_time_layers'] == []
    for rid in ('P02S-106', 'P02S-115', 'P02S-125', 'P02S-134'):
        assert rs[rid]['time_layer'] == 'YEAR' and rs[rid]['source_time_layers'] == ['YEAR']
    for rid in ('P02S-106', 'P02S-125'):
        assert not rs[rid]['canonical_promotion'] and rs[rid]['gap_id'].endswith('C01')
    assert '本宫及对宫' in rs['P02S-115']['condition']
    assert '太阳、巨门、天梁、天同' in rs['P02S-134']['condition']


def test_counterexamples_case_and_runtime_boundaries_remain_explicit():
    rs = {r['projection_rule_id']: r for r in load()['records']}
    assert '离散后仍主助力' in rs['P02S-091']['literal_claim']
    assert '见吉曜' in rs['P02S-124']['condition'] and rs['P02S-124']['literal_claim'] == '不耐久'
    for rid in ('P02S-088', 'P02S-093', 'P02S-095', 'P02S-099', 'P02S-100', 'P02S-103', 'P02S-105', 'P02S-111', 'P02S-118', 'P02S-120', 'P02S-121', 'P02S-129'):
        assert rs[rid]['case_support_only'] and rs[rid]['case_support_reason']
    for r in rs.values():
        assert not r['canonical_mapping_approved'] and not r['executable'] and r['history_feedback'] == 0
        assert r['condition_encoding'] == 'SOURCE_NATIVE_TEXT_NOT_BOOLEAN_IR'
        assert r['source_epistemic'] == 'EXPLICIT' and r['source_span_verified']
    assert not load()['whole_chapter_complete'] and '4 武曲' in load()['next_source_anchor']

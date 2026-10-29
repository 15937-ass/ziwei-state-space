"""Source-boundary regressions, not empirical validation of source claims."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WP = ROOT / 'knowledge/palaces/P11_fortune/wp05'


def data():
    return json.loads((WP / 'FORTUNE_FD07_SOURCE_AUDIT_v0.1.json').read_text())


def test_prior_six_ledgers_and_thirty_gaps_remain_byte_identical():
    d = data()
    assert len(d['accepted_prior']) == 6
    gaps = []
    for p in d['accepted_prior']:
        b = (ROOT / p['path']).read_bytes()
        assert hashlib.sha256(b).hexdigest() == p['sha256']
        assert p['gap_ids'] == [g['gap_id'] for g in json.loads(b)['source_coverage_gaps']]
        gaps += p['gap_ids']
    assert len(gaps) == len(set(gaps)) == 30
    old = json.loads((WP / 'FORTUNE_FD06_SOURCE_AUDIT_v0.1.json').read_text())
    for k, v in old['cumulative'].items():
        assert d['cumulative'][k] == v + d['summary'][k]


def test_final_source_range_and_no_unreviewed_parent_chapter():
    d = data()
    assert [r['projection_rule_id'] for r in d['records']] == [f'P11S-{i:03}' for i in range(411, 475)]
    assert {r['printed_page'] for r in d['records']} == {175, 176}
    assert {r['pdf_physical_page'] for r in d['records']} == {88}
    assert {r['source_anchor'] for r in d['records']} == {f'Q{i:02}' for i in range(1, 10)} | {f'P{i:02}' for i in range(1, 11)}
    assert d['records'][-1]['source_span'] == '时生突破现状之心而不能实行。'
    assert 'coverage census' in d['next_source_anchor']


def test_every_held_atom_is_accounted_for_once_and_not_promoted():
    d = data()
    rows = {r['projection_rule_id']: r for r in d['records']}
    ids = [i for g in d['source_coverage_gaps'] for i in g['affected_record_ids']]
    assert len(ids) == len(set(ids)) == 21
    assert set(ids) == {i for i, r in rows.items() if not r['canonical_promotion']}
    assert all(rows[i]['normalization_epistemic'] == 'UNRESOLVED' and not rows[i]['normalization_verified'] for i in ids)
    assert all(not r['canonical_promotion'] for r in rows.values() if '病善' in r['source_span'] or '在刑' in r['source_span'])
    assert all(not r['canonical_promotion'] for r in rows.values() if r['source_anchor'] == 'Q09')
    acc = [r for r in rows.values() if r['canonical_promotion']]
    assert len(acc) == 43
    assert sum(r['case_support_only'] for r in acc) == 19
    assert sum(not r['case_support_only'] for r in acc) == 24


def test_relational_and_transformation_subjects_do_not_leak_across_paragraphs():
    rows = data()['records']
    q6 = [r for r in rows if r['source_anchor'] == 'Q06' and '与武曲' in r['source_span']]
    assert q6 and all('化忌' not in r['condition'] for r in q6)
    assert any('紫微化权' in r['condition'] and '对宫紫微天府' in r['condition'] for r in rows)
    assert any(r['source_anchor'] == 'P05' and '廉贞化忌' in r['condition'] for r in rows)
    assert any(r['source_anchor'] == 'P06' and '武曲化忌' in r['condition'] for r in rows)
    assert any(r['source_anchor'] == 'P07' and '紫微化科' in r['condition'] for r in rows)
    assert any(r['source_anchor'] == 'P07' and '紫微化权' in r['condition'] for r in rows)
    assert all(not r['canonical_promotion'] for r in rows if r['source_anchor'] in {'P04', 'P09'})


def test_event_value_and_temporal_boundaries_fail_closed():
    d = data()
    for r in d['records']:
        assert r['source_span_verified'] and r['reviewer_id'] and r['reviewed_at']
        assert r['time_layer'] == r['primary_time_layer'] == 'NATAL'
        assert r['source_time_expression'] is None
        assert not r['canonical_mapping_approved'] and not r['executable']
        if any(x in r['source_span'] for x in ['婚姻', '迟婚', '偏房', '继室', '刑克', '配偶', '疾病', '虚伪', '偏激', '自我陶醉', '好高骛远']):
            assert r['case_support_only']
    assert all(d['execution_boundary'][k] == 0 for k in ['history_feedback', 'conditions_compiled', 'execution_unlocked', 'new_independent_time_scale', 'probability', 'numeric_weight', 'decay'])
    assert d['summary']['durable_review_object_count'] == len(d['records']) + len(d['source_coverage_gaps']) + len(d['source_section_inventory']) <= 100

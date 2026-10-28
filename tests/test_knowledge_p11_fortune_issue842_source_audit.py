import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WP = ROOT / 'knowledge/palaces/P11_fortune/wp05'


def data():
    return json.loads((WP / 'FORTUNE_FD05_SOURCE_AUDIT_v0.1.json').read_text())


def test_fd05_ids_counts_and_four_prior_ledgers_are_preserved():
    d = data()
    assert [r['projection_rule_id'] for r in d['records']] == [f'P11S-{i:03}' for i in range(287, 355)]
    acc = [r for r in d['records'] if r['canonical_promotion']]
    assert len(acc) == d['summary']['source_records_added'] == 47
    assert sum(r['case_support_only'] for r in acc) == 9
    assert sum(not r['case_support_only'] for r in acc) == 38
    gaps = []
    for p in d['accepted_prior']:
        b = (ROOT / p['path']).read_bytes()
        assert hashlib.sha256(b).hexdigest() == p['sha256']
        assert p['gap_ids'] == [g['gap_id'] for g in json.loads(b)['source_coverage_gaps']]
        gaps += p['gap_ids']
    assert len(gaps) == len(set(gaps)) == 23
    old = json.loads((WP / 'FORTUNE_FD04_SOURCE_AUDIT_v0.1.json').read_text())
    for k in d['cumulative']:
        assert d['cumulative'][k] == old['cumulative'][k] + d['summary'][k]
    assert d['cumulative']['source_atoms_reviewed'] == 354
    assert d['cumulative']['held'] == 76


def test_fd05_covers_three_sections_without_tianfu_or_tianxiang_recount():
    d = data()
    assert {r['source_anchor'] for r in d['records']} == {f'M{i:02}' for i in range(1, 10)} | {f'R{i:02}' for i in range(1, 10)} | {f'J{i:02}' for i in range(1, 8)}
    assert [(p['printed_page'], p['pdf_physical_page'], p['half']) for p in d['source_section_inventory']] == [(173, 87, 'LEFT'), (174, 87, 'RIGHT')]
    assert len(d['records']) + len(d['source_coverage_gaps']) + len(d['source_section_inventory']) == d['summary']['durable_review_object_count'] == 74
    assert '11 天相' in d['source_basis']['batch_end'] and '天相' in d['next_source_anchor']


def test_literal_pattern_and_scope_gaps_stay_held():
    d = data()
    rows = {r['projection_rule_id']: r for r in d['records']}
    held = [i for g in d['source_coverage_gaps'] for i in g['affected_record_ids']]
    assert len(held) == len(set(held)) == 21
    assert set(held) == {i for i, r in rows.items() if not r['canonical_promotion']}
    assert all(not rows[i]['normalization_verified'] and rows[i]['normalization_epistemic'] == 'UNRESOLVED' for i in held)
    assert all(not r['canonical_promotion'] for r in rows.values() if r['source_anchor'] == 'M05')
    assert any('陀岁' in r['source_span'] and not r['canonical_promotion'] for r in rows.values())
    assert any('迁移宫' in r['cross_palace_dependency'] and not r['canonical_promotion'] for r in rows.values())
    assert any(r['source_anchor'] == 'R04' and r['gap_id'] == 'P11-FD05-GAP-003' for r in rows.values())


def test_age_stage_is_not_invented_year_decade_or_age_threshold():
    d = data()
    timed = [r for r in d['records'] if r['source_time_expression']]
    assert len(timed) == 1
    r = timed[0]
    assert r['source_time_expression'] == '中年以后'
    assert r['time_layer'] is None and r['primary_time_layer'] is None
    assert not r['canonical_promotion'] and r['gap_id'] == 'P11-FD05-GAP-004'
    assert all(x['primary_time_layer'] in {None, 'NATAL'} for x in d['records'])


def test_source_subjects_negative_controls_and_case_boundaries_survive():
    d = data()
    rows = d['records']
    assert any(r['source_anchor'] == 'M09' and '不见煞' in r['condition'] for r in rows)
    assert any(r['source_anchor'] == 'R01' and '即使见吉星' in r['condition'] and r['case_support_only'] for r in rows)
    for k, star in [('J04', '太阳'), ('J05', '天机'), ('J06', '天同')]:
        assert any(r['source_anchor'] == k and star + '化忌' in r['condition'] for r in rows)
    for r in rows:
        if any(k in r['source_span'] for k in ['自闭症', '弱智', '贪酒色', '风流自赏', '痛苦的情网']):
            assert r['case_support_only']
        assert r['source_span_verified'] and r['review_status'] == 'SOURCE_SPAN_VERIFIED'
        assert r['reviewer_id'] and r['reviewed_at']
        assert not r['canonical_mapping_approved'] and not r['executable']
    assert all(d['execution_boundary'][k] == 0 for k in ['history_feedback', 'conditions_compiled', 'execution_unlocked', 'new_independent_time_scale', 'numeric_weight', 'probability', 'decay'])

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WP = ROOT / 'knowledge/palaces/P11_fortune/wp05'


def data():
    return json.loads((WP / 'FORTUNE_FD06_SOURCE_AUDIT_v0.1.json').read_text())


def test_fd06_ids_counts_and_all_prior_evidence_reconcile():
    d = data()
    assert [r['projection_rule_id'] for r in d['records']] == [f'P11S-{i:03}' for i in range(355, 411)]
    acc = [r for r in d['records'] if r['canonical_promotion']]
    assert len(acc) == d['summary']['source_records_added'] == 44
    assert sum(r['case_support_only'] for r in acc) == 6
    assert sum(not r['case_support_only'] for r in acc) == 38
    gaps = []
    for p in d['accepted_prior']:
        b = (ROOT / p['path']).read_bytes()
        assert hashlib.sha256(b).hexdigest() == p['sha256']
        assert p['gap_ids'] == [g['gap_id'] for g in json.loads(b)['source_coverage_gaps']]
        gaps += p['gap_ids']
    assert len(gaps) == len(set(gaps)) == 27
    old = json.loads((WP / 'FORTUNE_FD05_SOURCE_AUDIT_v0.1.json').read_text())
    for k in d['cumulative']:
        assert d['cumulative'][k] == old['cumulative'][k] + d['summary'][k]
    assert d['cumulative']['source_atoms_reviewed'] == 410
    assert d['cumulative']['held'] == 88


def test_fd06_two_sections_stop_before_qisha():
    d = data()
    assert {r['source_anchor'] for r in d['records']} == {f'X{i:02}' for i in range(1, 12)} | {f'B{i:02}' for i in range(1, 10)}
    assert [(p['printed_page'], p['pdf_physical_page'], p['half']) for p in d['source_section_inventory']] == [(174, 87, 'RIGHT'), (175, 88, 'LEFT')]
    assert len(d['records']) + len(d['source_coverage_gaps']) + len(d['source_section_inventory']) == d['summary']['durable_review_object_count'] == 61
    assert '13 七杀' in d['source_basis']['batch_end'] and '七杀' in d['next_source_anchor']


def test_fd06_unresolved_relations_and_literals_do_not_promote():
    d = data()
    rows = {r['projection_rule_id']: r for r in d['records']}
    ids = [i for g in d['source_coverage_gaps'] for i in g['affected_record_ids']]
    assert len(ids) == len(set(ids)) == 12
    assert set(ids) == {i for i, r in rows.items() if not r['canonical_promotion']}
    assert all(not rows[i]['normalization_verified'] and rows[i]['normalization_epistemic'] == 'UNRESOLVED' for i in ids)
    assert any('科文叶曜' in r['source_span'] and not r['canonical_promotion'] for r in rows.values())
    assert any('太阴天梁' in r['condition'] and r['case_support_only'] and not r['canonical_promotion'] for r in rows.values())
    assert all(not r['canonical_promotion'] for r in rows.values() if r['source_anchor'] == 'B02' and r['gap_id'])


def test_fd06_subjects_negatives_and_qualitative_amounts_remain_distinct():
    rows = data()['records']
    assert any(r['source_anchor'] == 'X01' and '相邻' in r['source_span'] for r in rows)
    assert any(r['source_anchor'] == 'X02' and '不见煞' in r['condition'] for r in rows)
    assert any(r['source_anchor'] == 'X03' and '廉贞吉化' in r['condition'] for r in rows)
    assert any(r['source_anchor'] == 'X03' and '破军吉化' in r['condition'] for r in rows)
    assert any(r['source_anchor'] == 'X06' and '见煞且少' in r['condition'] for r in rows)
    assert any(r['source_anchor'] == 'X06' and '见煞重' in r['condition'] for r in rows)
    assert any(r['source_anchor'] == 'B03' and '天梁不见吉化且会巨门化忌' in r['condition'] and r['case_support_only'] for r in rows)
    assert any(r['source_anchor'] == 'B04' and '天同化忌' in r['condition'] for r in rows)
    assert any(r['source_anchor'] == 'B06' and '天机化忌' in r['condition'] for r in rows)


def test_fd06_source_acceptance_is_not_runtime_or_empirical_validation():
    d = data()
    for r in d['records']:
        assert r['primary_time_layer'] == r['time_layer'] == 'NATAL'
        assert r['source_time_expression'] is None
        assert not r['canonical_mapping_approved'] and not r['executable']
        assert r['source_span_verified'] and r['review_status'] == 'SOURCE_SPAN_VERIFIED'
        assert r['reviewer_id'] and r['reviewed_at']
        if any(x in r['source_span'] for x in ['反对派', '伪善', '不良嗜好', '名士']):
            assert r['case_support_only']
    assert all(d['execution_boundary'][k] == 0 for k in ['history_feedback', 'conditions_compiled', 'execution_unlocked', 'new_independent_time_scale', 'probability', 'numeric_weight', 'decay'])

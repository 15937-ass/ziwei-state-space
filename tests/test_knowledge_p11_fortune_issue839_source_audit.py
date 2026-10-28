import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WP = ROOT / 'knowledge/palaces/P11_fortune/wp05'


def data():
    return json.loads((WP / 'FORTUNE_FD04_SOURCE_AUDIT_v0.1.json').read_text())


def test_counts_prior_hashes_and_gaps_reconcile():
    d = data()
    assert [r['projection_rule_id'] for r in d['records']] == [f'P11S-{i:03}' for i in range(222, 287)]
    acc = [r for r in d['records'] if r['canonical_promotion']]
    assert len(acc) == d['summary']['source_records_added'] == 50
    assert sum(r['case_support_only'] for r in acc) == 7
    assert sum(not r['case_support_only'] for r in acc) == 43
    prior_gaps = []
    for p in d['accepted_prior']:
        b = (ROOT / p['path']).read_bytes()
        assert hashlib.sha256(b).hexdigest() == p['sha256']
        assert p['gap_ids'] == [g['gap_id'] for g in json.loads(b)['source_coverage_gaps']]
        prior_gaps += p['gap_ids']
    assert len(prior_gaps) == len(set(prior_gaps)) == 19
    old = json.loads((WP / 'FORTUNE_FD03_SOURCE_AUDIT_v0.1.json').read_text())
    for key in d['cumulative']:
        assert d['cumulative'][key] == old['cumulative'][key] + d['summary'][key]
    assert d['cumulative']['source_atoms_reviewed'] == 286
    assert d['cumulative']['source_records_added'] == 231
    assert d['cumulative']['held'] == 55


def test_complete_lianzhen_tianfu_coverage_and_cross_page_span():
    d = data()
    assert {r['source_anchor'] for r in d['records']} == {f'L{i:02}' for i in range(1, 21)} | {f'T{i:02}' for i in range(1, 13)}
    assert [(p['printed_page'], p['pdf_physical_page'], p['half']) for p in d['source_section_inventory']] == [(171, 86, 'LEFT'), (172, 86, 'RIGHT'), (173, 87, 'LEFT')]
    cross = [r for r in d['records'] if r['printed_page_end'] > r['printed_page']]
    assert len(cross) == 1 and cross[0]['source_anchor'] == 'L06'
    assert cross[0]['printed_page_end'] == 172 and not cross[0]['canonical_promotion']
    assert len(d['records']) + len(d['source_coverage_gaps']) + len(d['source_section_inventory']) == d['summary']['durable_review_object_count'] == 72
    assert '8 太阴' in d['source_basis']['batch_end'] and '太阴' in d['next_source_anchor']


def test_held_scopes_literals_and_unspecified_transformation_subjects_fail_closed():
    d = data()
    rows = {r['projection_rule_id']: r for r in d['records']}
    affected = [i for g in d['source_coverage_gaps'] for i in g['affected_record_ids']]
    assert len(affected) == len(set(affected)) == 15
    assert set(affected) == {i for i, r in rows.items() if not r['canonical_promotion']}
    assert all(not rows[i]['normalization_verified'] and rows[i]['normalization_epistemic'] == 'UNRESOLVED' for i in affected)
    assert any(r['source_anchor'] == 'L07' and '计评' in r['source_span'] and not r['canonical_promotion'] for r in rows.values())
    assert any(r['source_anchor'] == 'L15' and r['gap_id'] == 'P11-FD04-GAP-004' for r in rows.values())
    assert any(r['source_anchor'] == 'T11' and '是否必须承接未定' in r['condition'] and not r['canonical_promotion'] for r in rows.values())


def test_negatives_comparisons_and_distinct_transformation_subjects_survive():
    rows = data()['records']
    assert any(r['source_anchor'] == 'L03' and '无科文' in r['condition'] for r in rows)
    assert any(r['source_anchor'] == 'L09' and '不加煞' in r['condition'] for r in rows)
    assert any(r['source_anchor'] == 'L18' and '无煞者始' in r['source_span'] for r in rows)
    assert any(r['source_anchor'] == 'L10' and '天府化科' in r['condition'] for r in rows)
    assert any(r['source_anchor'] == 'L17' and '破军吉化' in r['condition'] for r in rows)
    assert any(r['source_anchor'] == 'L17' and '廉贞化忌' in r['condition'] for r in rows)
    assert any(r['source_anchor'] == 'T09' and '相对卯酉' in r['condition'] for r in rows)
    assert any(r['source_anchor'] == 'T07' and '同度或相夹' in r['condition'] for r in rows)


def test_case_and_source_contracts_do_not_authorize_runtime_or_period_claims():
    d = data()
    for r in d['records']:
        if r['source_anchor'] in {'L04', 'L05', 'L06', 'T08'}:
            assert r['case_support_only'] and r['case_support_reason']
        assert r['review_status'] == 'SOURCE_SPAN_VERIFIED' and r['source_span_verified']
        assert r['reviewer_id'] and r['source_span'] and r['reviewed_at']
        assert r['primary_time_layer'] == r['time_layer'] == 'NATAL'
        assert r['source_time_expression'] is None
        assert not r['executable'] and not r['canonical_mapping_approved']
        assert r['condition_encoding'] == 'SOURCE_NATIVE_TEXT_NOT_BOOLEAN_IR'
    for k in ['history_feedback', 'conditions_compiled', 'execution_unlocked', 'canonical_mapping_promotions', 'probability', 'numeric_weight', 'decay']:
        assert d['execution_boundary'][k] == 0

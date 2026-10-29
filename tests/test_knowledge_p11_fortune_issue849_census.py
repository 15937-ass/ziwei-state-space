import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WP = ROOT / 'knowledge/palaces/P11_fortune/wp05'


def data():
    return json.loads((WP / 'FORTUNE_CENSUS_A_v0.1.json').read_text())


def test_census_reconciles_every_anchor_slice_from_the_four_source_pages():
    d = data()
    expected = {}
    for pin in d['accepted_ledger_pins']:
        b = (ROOT / pin['path']).read_bytes()
        assert hashlib.sha256(b).hexdigest() == pin['sha256']
        old = json.loads(b)
        assert pin['gap_ids'] == [g['gap_id'] for g in old['source_coverage_gaps']]
        for r in old['records']:
            if 166 <= r['printed_page'] <= 169:
                expected.setdefault((r['printed_page'], r['source_anchor'], pin['path']), []).append(r)
    actual = {(a['printed_page'], a['source_anchor'], a['ledger_path']): a for a in d['paragraph_inventory']}
    assert len(actual) == len(d['paragraph_inventory']) == len(expected) == 73
    assert set(actual) == set(expected)
    all_ids = []
    for key, records in expected.items():
        a = actual[key]
        assert a['record_ids'] == [r['projection_rule_id'] for r in records]
        assert a['held_ids'] == [r['projection_rule_id'] for r in records if not r['canonical_promotion']]
        assert a['accepted_source_ids'] == [r['projection_rule_id'] for r in records if r['canonical_promotion']]
        assert a['gap_ids'] == sorted({r['gap_id'] for r in records if r['gap_id']})
        all_ids += a['record_ids']
    assert len(all_ids) == len(set(all_ids)) == 152


def test_double_page_scan_coordinates_and_exact_partial_end():
    d = data()
    assert [(p['printed_page'], p['pdf_physical_page'], p['half'], p['paragraph_anchor_count']) for p in d['page_inventory']] == [(166,83,'RIGHT',15),(167,84,'LEFT',23),(168,84,'RIGHT',20),(169,85,'LEFT',15)]
    assert 'p170武曲不纳入' in d['source_basis']['scope_end']
    assert d['paragraph_inventory'][-1]['source_anchor'] == 'S15'
    assert d['source_basis']['attachment_sha256'] == '6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c'


def test_all_prior_residuals_preserved_and_census_cannot_promote():
    d = data()
    gaps = [g for p in d['accepted_ledger_pins'] for g in p['gap_ids']]
    assert len(gaps) == len(set(gaps)) == 34
    s = d['summary']
    assert s['durable_review_object_count'] == len(d['paragraph_inventory']) + len(d['page_inventory']) + len(d['accepted_ledger_pins']) == 84 <= 100
    assert s['new_source_records'] == s['new_held_records'] == 0
    assert s['previous_total_reviewed'] == 474
    assert s['previous_total_source_records'] + s['previous_total_held'] == 474
    assert s['history_feedback'] == s['conditions_compiled'] == s['execution_unlocked'] == 0
    assert not d['whole_chapter_complete']
    assert not d['formal_mapping_approved'] and not d['empirical_validity_claimed'] and not d['product_runtime_authorized']
    assert 'Census B' in d['next_source_anchor']
    assert all(a['no_new_record_or_gap_promotion'] for a in d['paragraph_inventory'])

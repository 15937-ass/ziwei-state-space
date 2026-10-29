import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WP = ROOT / 'knowledge/palaces/P11_fortune/wp05'


def data():
    return json.loads((WP / 'FORTUNE_CENSUS_B_v0.1.json').read_text())


def test_census_reconciles_every_anchor_slice_from_the_four_source_pages():
    d = data()
    expected = {}
    for pin in d['accepted_ledger_pins']:
        b = (ROOT / pin['path']).read_bytes()
        assert hashlib.sha256(b).hexdigest() == pin['sha256']
        old = json.loads(b)
        assert pin['gap_ids'] == [g['gap_id'] for g in old['source_coverage_gaps']]
        for r in old['records']:
            for page in range(r['printed_page'], r['printed_page_end'] + 1):
                if 170 <= page <= 173:
                    expected.setdefault((page, r['source_anchor'], pin['path']), []).append(r)
    actual = {(a['printed_page'], a['source_anchor'], a['ledger_path']): a for a in d['paragraph_inventory']}
    assert len(actual) == len(d['paragraph_inventory']) == len(expected) == 84
    assert set(actual) == set(expected)
    all_ids = []
    for key, records in expected.items():
        a = actual[key]
        assert a['record_ids'] == [r['projection_rule_id'] for r in records]
        assert a['held_ids'] == [r['projection_rule_id'] for r in records if not r['canonical_promotion']]
        assert a['accepted_source_ids'] == [r['projection_rule_id'] for r in records if r['canonical_promotion']]
        assert a['gap_ids'] == sorted({r['gap_id'] for r in records if r['gap_id']})
        all_ids += a['record_ids']
    assert len(all_ids) == 180
    assert len(set(all_ids)) == 179


def test_double_page_scan_coordinates_and_exact_partial_end():
    d = data()
    assert [(p['printed_page'], p['pdf_physical_page'], p['half'], p['paragraph_anchor_count']) for p in d['page_inventory']] == [(170,85,'RIGHT',21),(171,86,'LEFT',21),(172,86,'RIGHT',22),(173,87,'LEFT',20)]
    assert 'p174贪狼R07不纳入' in d['source_basis']['scope_end']
    assert d['paragraph_inventory'][-1]['source_anchor'] == 'R06'
    assert d['source_basis']['attachment_sha256'] == '6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c'


def test_all_prior_residuals_preserved_and_census_cannot_promote():
    d = data()
    gaps = [g for p in d['accepted_ledger_pins'] for g in p['gap_ids']]
    assert len(gaps) == len(set(gaps)) == 34
    s = d['summary']
    assert s['durable_review_object_count'] == len(d['paragraph_inventory']) + len(d['page_inventory']) + len(d['accepted_ledger_pins']) == 95 <= 100
    assert s['new_source_records'] == s['new_held_records'] == 0
    assert s['previous_total_reviewed'] == 474
    assert s['previous_total_source_records'] + s['previous_total_held'] == 474
    assert s['history_feedback'] == s['conditions_compiled'] == s['execution_unlocked'] == 0
    assert not d['whole_chapter_complete']
    assert not d['formal_mapping_approved'] and not d['empirical_validity_claimed'] and not d['product_runtime_authorized']
    assert 'Census C' in d['next_source_anchor']
    assert all(a['no_new_record_or_gap_promotion'] for a in d['paragraph_inventory'])


def test_continuation_slice_and_prior_census_are_preserved():
    d = data()
    pin = d['prior_census_a_pin']
    assert hashlib.sha256((ROOT / pin['path']).read_bytes()).hexdigest() == pin['sha256']
    continuations = [a for a in d['paragraph_inventory'] if a['cross_page_continuation']]
    assert len(continuations) == 1
    assert continuations[0]['printed_page'] == 172
    assert continuations[0]['record_ids'] == ['P11S-231']
    assert continuations[0]['held_ids'] == ['P11S-231']
    assert continuations[0]['gap_ids'] == ['P11-FD04-GAP-001']
    assert d['summary']['issue_estimated_anchor_count'] == 83
    assert all(a['printed_page'] != 174 for a in d['paragraph_inventory'])

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WP = ROOT / 'knowledge/palaces/P11_fortune/wp05'


def load():
    return json.loads((WP / 'FORTUNE_CENSUS_C_v0.1.json').read_text())


def test_every_source_slice_matches_pinned_records_and_scan_coordinates():
    d = load()
    expected = {}
    for pin in d['accepted_ledger_pins']:
        raw = (ROOT / pin['path']).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == pin['sha256']
        for r in json.loads(raw)['records']:
            for page in range(r['printed_page'], r['printed_page_end'] + 1):
                if 174 <= page <= 176:
                    expected.setdefault((page, r['source_anchor'], pin['path']), []).append(r)
    actual = {(a['printed_page'], a['source_anchor'], a['ledger_path']): a for a in d['paragraph_inventory']}
    assert len(actual) == len(d['paragraph_inventory']) == 49
    assert actual.keys() == expected.keys()
    for key, rows in expected.items():
        a = actual[key]
        assert a['record_ids'] == [r['projection_rule_id'] for r in rows]
        assert a['held_ids'] == [r['projection_rule_id'] for r in rows if not r['canonical_promotion']]
        assert a['gap_ids'] == sorted({r['gap_id'] for r in rows if r['gap_id']})
    assert [(p['printed_page'], p['pdf_physical_page'], p['half'], p['paragraph_anchor_count']) for p in d['page_inventory']] == [(174,87,'RIGHT',16),(175,88,'LEFT',19),(176,88,'RIGHT',14)]
    assert d['paragraph_inventory'][0]['source_anchor'] == 'R07'
    assert d['paragraph_inventory'][-1]['source_anchor'] == 'P10'


def test_all_retained_records_are_accounted_exactly_once_without_resolution():
    d = load()
    records, gaps = {}, {}
    for pin in d['accepted_ledger_pins']:
        old = json.loads((ROOT / pin['path']).read_bytes())
        records.update({r['projection_rule_id']: r for r in old['records']})
        gaps.update({g['gap_id']: g for g in old['source_coverage_gaps']})
    held = {rid for rid,r in records.items() if not r['canonical_promotion']}
    seen = []
    assert len(d['residual_dispositions']) == len(gaps) == 34
    for g in d['residual_dispositions']:
        assert g['original_gap'] == gaps[g['gap_id']]
        assert g['affected_record_ids'] == gaps[g['gap_id']]['affected_record_ids']
        assert [r['projection_rule_id'] for r in g['affected_sources']] == g['affected_record_ids']
        for snapshot in g['affected_sources']:
            old = records[snapshot['projection_rule_id']]
            assert all(old[k] == v for k,v in snapshot.items())
            assert old['gap_id'] == g['gap_id']
        assert not g['normalization_resolved'] and not g['semantic_resolution_claimed']
        assert g['disposition'] == 'RETAINED_FAIL_CLOSED_NO_PROMOTION'
        assert g['follow_up_dependency'] and g['prohibited_uses']
        seen.extend(g['affected_record_ids'])
    assert len(seen) == len(set(seen)) == len(held) == 109
    assert set(seen) == held


def test_chapter_union_covers_all_474_unique_ids_and_corrected_206_slices():
    d = load()
    previous = []
    for pin in d['prior_census_pins']:
        raw = (ROOT / pin['path']).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == pin['sha256']
        previous += json.loads(raw)['paragraph_inventory']
    anchors = previous + d['paragraph_inventory']
    assert len(anchors) == 206
    assert sorted({a['printed_page'] for a in anchors}) == list(range(166,177))
    ids = {rid for a in anchors for rid in a['record_ids']}
    assert ids == {f'P11S-{n:03d}' for n in range(1,475)}
    assert d['chapter_reconciliation']['unique_source_ids'] == sorted(ids)
    assert d['summary']['unique_record_count'] == len({rid for a in d['paragraph_inventory'] for rid in a['record_ids']}) == 143
    assert d['chapter_reconciliation']['previous_estimate'] == 205


def test_census_c_cannot_unlock_stage_mapping_or_runtime():
    d = load()
    s = d['summary']
    assert s['durable_review_object_count'] == len(d['paragraph_inventory']) + len(d['page_inventory']) + len(d['residual_dispositions']) + len(d['accepted_ledger_pins']) == 93 <= 100
    assert s['new_source_records'] == s['new_held_records'] == 0
    assert s['history_feedback'] == s['conditions_compiled'] == s['execution_unlocked'] == 0
    assert d['coverage_census_complete'] and d['residual_disposition_registered']
    assert not d['whole_chapter_complete'] and not d['stage_closure_accepted']
    assert not d['chapter_reconciliation']['all_semantics_resolved']
    assert not d['chapter_reconciliation']['independent_stage_closure_review_complete']
    assert not d['formal_mapping_approved'] and not d['empirical_validity_claimed'] and not d['product_runtime_authorized']
    assert 'R2' in d['next_source_anchor']

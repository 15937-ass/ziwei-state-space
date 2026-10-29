import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'knowledge/palaces/P02_siblings/wp05/SIBLINGS_SB01_SOURCE_AUDIT_v0.1.json'


def load():
    return json.loads(PATH.read_text())


def test_ids_source_boundaries_and_counts_do_not_blanket_promote_historical_index():
    d = load()
    rs = d['records']
    assert [r['projection_rule_id'] for r in rs] == [f'P02S-{i:03d}' for i in range(1, 41)]
    assert {r['source_anchor'] for r in rs} == {f'Z{i:02d}' for i in range(1, 16)}
    for r in rs:
        assert r['printed_page'] == r['printed_page_end'] == 25
        assert r['pdf_physical_page'] == 13 and r['palace_id'] == 'P02'
        assert r['source_id'] == 'SRC-ZZ-003' and r['source_span_verified']
        assert r['source_epistemic'] == 'EXPLICIT'
    assert len(rs) == 40
    assert sum(r['canonical_promotion'] for r in rs) == 27
    assert sum(r['canonical_promotion'] and r['case_support_only'] for r in rs) == 12
    assert sum(r['canonical_promotion'] and not r['case_support_only'] for r in rs) == 15
    history = d['historical_candidate_inventory']
    assert history['canonical_P02_records_before'] == 0
    assert not history['historical_row_by_row_reconciliation_claimed']
    assert sum(pin['historical_rows'] for pin in history['pins']) == history['total_rows'] == 461
    for pin in history['pins']:
        raw = (ROOT / pin['path']).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == pin['sha256']
        assert len(list(csv.DictReader(raw.decode().splitlines()))) == pin['historical_rows']
        assert pin['read_only'] and pin['role'] == 'HISTORICAL_INDEX_ONLY_NOT_CANONICAL'


def test_held_gaps_cover_exact_records_and_case_flags_are_conservative():
    d = load()
    rs = {r['projection_rule_id']: r for r in d['records']}
    held = {rid for rid, r in rs.items() if not r['canonical_promotion']}
    seen = []
    assert len(d['source_coverage_gaps']) == 3
    for g in d['source_coverage_gaps']:
        assert g['reason'] and g['normalized_term'] is None
        assert g['status'] == 'RETAINED_FAIL_CLOSED' and g['local_work_can_continue']
        for rid in g['affected_record_ids']:
            assert rid in held and rs[rid]['gap_id'] == g['gap_id']
            assert rs[rid]['normalization_epistemic'] == 'UNRESOLVED'
            assert not rs[rid]['normalization_verified']
        seen += g['affected_record_ids']
    assert len(seen) == len(set(seen)) == len(held) == 13
    assert set(seen) == held
    for r in rs.values():
        if r['case_support_only']:
            assert r['case_support_reason']
            if r['canonical_promotion']:
                assert r['disposition'] == 'CASE_SUPPORT_ONLY'
        if r['canonical_promotion']:
            assert r['gap_id'] is None and r['normalization_epistemic'] == 'SOURCE_PRESERVING'
        assert not r['canonical_mapping_approved'] and not r['executable']
        assert r['history_feedback'] == 0


def test_explicit_years_dual_layer_and_unspecified_periods_stay_separate():
    rs = {r['projection_rule_id']: r for r in load()['records']}
    dual = rs['P02S-005']
    assert dual['source_time_layers'] == ['DECADE', 'YEAR']
    assert dual['time_layer'] is None and not dual['canonical_promotion']
    assert '副手' in dual['condition'] and '见煞忌' in dual['condition']
    bad_year = rs['P02S-014']
    assert bad_year['time_layer'] == 'YEAR'
    assert '紫破或天相' in bad_year['condition']
    assert '武相' not in bad_year['condition']
    good_year = rs['P02S-015']
    assert '武曲七杀或天府独坐' in good_year['condition']
    assert '武曲天府' not in good_year['condition']
    assert good_year['time_layer'] == 'YEAR' and not good_year['canonical_promotion']
    for rid in ['P02S-019', 'P02S-020', 'P02S-039', 'P02S-040']:
        assert rs[rid]['time_layer'] is None and rs[rid]['source_time_layers'] == []
        assert not rs[rid]['canonical_promotion']
    for r in rs.values():
        assert r['time_layer'] in ('NATAL', 'YEAR', None)
        assert r['time_layer'] == r['primary_time_layer']


def test_scan_inventory_and_checkpoint_scope_cannot_close_whole_palace():
    d = load()
    assert [(p['printed_page'], p['pdf_physical_page'], p['half']) for p in d['source_section_inventory']] == [(n, (n + 1) // 2, 'LEFT' if n % 2 else 'RIGHT') for n in range(25, 33)]
    assert all(p['visual_inventory_verified'] for p in d['source_section_inventory'])
    assert all(p['content_status'] == 'INVENTORY_ONLY_NOT_SOURCE_REVIEWED' for p in d['source_section_inventory'][1:])
    assert d['summary']['durable_review_object_count'] == 40 + 8 + 5 == 53 <= 100
    assert all(b['count'] <= 50 for b in d['summary']['reasoning_sub_batches'])
    assert d['source_basis']['attachment_sha256'] == '6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c'
    assert not d['whole_chapter_complete'] and '2 天机' in d['next_source_anchor']
    b = d['execution_boundary']
    assert b['history_feedback'] == b['conditions_compiled'] == b['execution_unlocked'] == 0
    assert not b['formal_mapping_approved'] and not b['product_runtime_authorized']

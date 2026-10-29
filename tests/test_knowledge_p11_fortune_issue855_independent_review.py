"""Independently reconstruct P11 handoff relations; old evidence stays byte-pinned."""
import collections
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WP = ROOT / 'knowledge/palaces/P11_fortune/wp05'


def review():
    return json.loads((WP / 'FORTUNE_INDEPENDENT_STAGE_REVIEW_855_v0.1.json').read_text())


def inputs():
    ledgers = [(p, json.loads(p.read_text())) for p in sorted(WP.glob('*SOURCE_AUDIT*'))]
    records = {r['projection_rule_id']: r for _, d in ledgers for r in d['records']}
    gaps = {g['gap_id']: g for _, d in ledgers for g in d['source_coverage_gaps']}
    censuses = [json.loads(p.read_text()) for p in sorted(WP.glob('*CENSUS*'))]
    return ledgers, records, gaps, censuses


def test_input_hashes_and_full_page_slice_relation_including_two_addenda():
    d = review()
    assert len(d['input_pins']) == 10
    for pin in d['input_pins']:
        assert hashlib.sha256((ROOT / pin['path']).read_bytes()).hexdigest() == pin['sha256']
        assert pin['read_only']
    ledgers, records, _, censuses = inputs()
    expected = collections.defaultdict(list)
    for p, ledger in ledgers:
        for r in ledger['records']:
            for page in range(r['printed_page'], r['printed_page_end'] + 1):
                expected[(page, r['source_anchor'], str(p.relative_to(ROOT)))].append(r['projection_rule_id'])
    actual = {}
    for c in censuses:
        for a in c['paragraph_inventory']:
            key = (a['printed_page'], a['source_anchor'], a['ledger_path'])
            assert key not in actual
            actual[key] = a['record_ids']
    differences = {key for key in expected if expected[key] != actual[key]}
    corrections = set()
    for a in d['page_slice_addenda']:
        key = (a['printed_page'], a['source_anchor'], a['ledger_path'])
        assert actual[key] == a['existing_record_ids']
        assert set(a['effective_record_ids']) - set(actual[key]) == set(a['additional_continuation_record_ids'])
        assert a['effective_record_ids'] == expected[key]
        corrections.add(key)
        actual[key] = a['effective_record_ids']
    assert corrections == differences and len(corrections) == 2
    assert [(a['printed_page'], a['additional_continuation_record_ids']) for a in d['page_slice_addenda']] == [(167, ['P11S-029']), (168, ['P11S-076'])]
    assert actual == expected and len(actual) == 206
    assert {rid for ids in actual.values() for rid in ids} == set(records)
    assert sorted(records) == [f'P11S-{i:03d}' for i in range(1, 475)]
    counts = collections.Counter(key[0] for key in actual)
    assert d['structural_review']['page_anchor_counts'] == {str(k): v for k, v in counts.items()}
    for c in censuses:
        for p in c['page_inventory']:
            page = p['printed_page']
            assert p['paragraph_anchor_count'] == counts[page]
            assert p['pdf_physical_page'] == (page + 1) // 2
            assert p['half'] == ('LEFT' if page % 2 else 'RIGHT')


def test_all_retained_gaps_and_source_snapshots_have_exact_bijection():
    d = review()
    _, records, gaps, censuses = inputs()
    held = {rid for rid, r in records.items() if not r['canonical_promotion']}
    seen = []
    assert len(d['residual_reviews']) == len(gaps) == 34
    c = next(c for c in censuses if 'residual_dispositions' in c)
    dispositions = {g['gap_id']: g for g in c['residual_dispositions']}
    for r in d['residual_reviews']:
        g = gaps[r['gap_id']]
        assert r['affected_record_ids'] == g['affected_record_ids']
        assert r['original_reason'] == g['reason']
        assert r['independent_disposition'] == 'ACCEPT_RETAINED_FAIL_CLOSED'
        assert not r['semantic_resolution_claimed']
        old = dispositions[r['gap_id']]
        assert old['original_gap'] == g
        assert old['follow_up_dependency'] and old['prohibited_uses']
        assert not old['normalization_resolved'] and not old['semantic_resolution_claimed']
        for snapshot in old['affected_sources']:
            record = records[snapshot['projection_rule_id']]
            assert all(record[k] == v for k, v in snapshot.items())
        for rid in r['affected_record_ids']:
            assert rid in held and records[rid]['gap_id'] == r['gap_id']
            assert records[rid]['normalization_epistemic'] == 'UNRESOLVED'
        seen.extend(r['affected_record_ids'])
    assert len(seen) == len(set(seen)) == len(held) == 109
    assert set(seen) == held == set(d['structural_review']['held_ids'])


def test_case_restrictions_override_generic_source_verified_labels():
    d = review()['structural_review']
    _, records, _, _ = inputs()
    accepted = {rid for rid, r in records.items() if r['canonical_promotion']}
    cases = {rid for rid in accepted if records[rid]['case_support_only']}
    reusable = accepted - cases
    exceptions = sorted(rid for rid in cases if records[rid]['disposition'] != 'CASE_SUPPORT_ONLY')
    assert d['case_disposition_label_exceptions'] == exceptions
    assert len(exceptions) == 19
    assert set(d['case_ids']) == cases and len(cases) == 77
    assert set(d['reusable_ids']) == reusable and len(reusable) == 288
    assert cases.isdisjoint(reusable) and len(accepted) == 365
    assert all(records[rid]['case_support_reason'] for rid in cases)
    for r in records.values():
        assert r['source_id'] == 'SRC-ZZ-003' and r['palace_id'] == 'P11'
        assert r['source_epistemic'] == 'EXPLICIT'
        assert r['condition'] and r['normalized_claim'] and r['source_span_verified']
        assert r['time_layer'] in (None, 'NATAL')
        assert r['primary_time_layer'] == r['time_layer']
        assert not r['executable'] and not r['canonical_mapping_approved']
        assert r['history_feedback'] == 0
    assert d['record_fields_checked'] == sorted(set.union(*(set(r) for r in records.values())))


def test_named_visual_samples_are_traceable_and_bounded_not_whole_reaudit():
    d = review()
    _, records, _, _ = inputs()
    samples = d['visual_samples']
    assert len(samples) == len({s['sample_id'] for s in samples}) == 40
    assert {s['printed_page'] for s in samples[:-1]} == set(range(166, 177))
    for s in samples:
        assert s['method'] == 'DIRECT_SCAN_VISUAL_REVIEW'
        assert s['finding'] and not s['new_promotion']
        for rid in s['record_ids']:
            r = records[rid]
            assert r['printed_page'] <= s['printed_page'] <= r['printed_page_end']
            assert r['source_anchor'] == s['source_anchor']
    assert samples[-1]['printed_page'] == 177 and not samples[-1]['record_ids']
    assert samples[-1]['result'] == 'EXCLUDED_BOUNDARY_CONFIRMED'
    objects = d['structural_review']['objects']
    assert sum(objects.values()) == 55
    assert d['durable_review_object_count'] == 55 + len(samples) == 95 <= 100
    assert sum(b['count'] for b in d['reasoning_sub_batches']) == 95
    assert all(b['count'] <= 50 for b in d['reasoning_sub_batches'])
    assert '不声称逐条独立语义复审' in d['structural_review']['field_content_review_scope']


def test_stage_acceptance_never_resolves_semantics_or_enables_product():
    d = review()
    assert d['source_stage_handoff_accepted']
    assert not d['all_semantics_resolved'] and not d['empirical_validity_claimed']
    assert not d['formal_mapping_approved'] and not d['product_runtime_authorized']
    assert d['history_feedback'] == d['conditions_compiled'] == d['execution_unlocked'] == 0
    assert d['source_basis']['sha256'] == '6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c'
    assert len(d['critic_findings']) == 5
    state = (ROOT / 'knowledge/states/P11_FORTUNE_STATE.yaml').read_text()
    assert 'BOUNDED_SOURCE_STAGE_ONLY_NOT_SEMANTIC_OR_EMPIRICAL_COMPLETION' in state
    assert 'all_semantics_resolved: false' in state

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'knowledge/palaces/P02_siblings/wp05/SIBLINGS_SB02_TIANJI_SOURCE_AUDIT_v0.1.json'


def load():
    return json.loads(PATH.read_text())


def test_accepted_ziwei_input_is_byte_preserved_and_ids_are_disjoint():
    d = load()
    pin = d['accepted_input_pin']
    raw = (ROOT / pin['path']).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == pin['sha256']
    prev = json.loads(raw)
    assert len(prev['records']) == 40 and len(prev['source_coverage_gaps']) == 3
    assert [r['projection_rule_id'] for r in d['records']] == [f'P02S-{i:03d}' for i in range(41, 84)]
    assert not ({r['projection_rule_id'] for r in prev['records']} & {r['projection_rule_id'] for r in d['records']})
    for p in prev['historical_candidate_inventory']['pins']:
        assert hashlib.sha256((ROOT / p['path']).read_bytes()).hexdigest() == p['sha256']


def test_source_anchors_reconcile_and_every_unresolved_record_has_one_gap():
    d = load()
    rs = {r['projection_rule_id']: r for r in d['records']}
    assert {r['source_anchor'] for r in rs.values()} == {f'T{i:02d}' for i in range(1, 18)}
    held = {rid for rid, r in rs.items() if not r['canonical_promotion']}
    covered = []
    for g in d['source_coverage_gaps']:
        assert g['reason'] and g['normalized_term'] is None and g['local_work_can_continue']
        for rid in g['affected_record_ids']:
            assert rs[rid]['gap_id'] == g['gap_id']
            assert not rs[rid]['normalization_verified']
            assert rs[rid]['normalization_epistemic'] == 'UNRESOLVED'
        covered += g['affected_record_ids']
    assert len(covered) == len(set(covered)) == 15
    assert set(covered) == held
    assert sum(r['canonical_promotion'] for r in rs.values()) == 28
    assert sum(r['canonical_promotion'] and r['case_support_only'] for r in rs.values()) == 7
    assert sum(r['canonical_promotion'] and not r['case_support_only'] for r in rs.values()) == 21
    assert d['summary']['durable_review_object_count'] == len(rs) + 3 <= 100
    assert all(b['count'] <= 50 for b in d['summary']['reasoning_sub_batches'])


def test_explicit_year_is_not_borrowed_by_unspecified_movement_periods():
    rs = {r['projection_rule_id']: r for r in load()['records']}
    assert rs['P02S-054']['time_layer'] == 'YEAR'
    assert rs['P02S-054']['source_time_layers'] == ['YEAR']
    assert '太阳、巨门、天梁' in rs['P02S-054']['condition']
    for rid in ('P02S-046', 'P02S-069', 'P02S-075', 'P02S-076', 'P02S-083'):
        assert rs[rid]['time_layer'] is None and rs[rid]['source_time_layers'] == []
        assert rs[rid]['gap_id'].endswith('T01') and not rs[rid]['canonical_promotion']
    assert '巨阳、武贪' in rs['P02S-075']['condition']
    assert '巨阳、廉破、武贪' in rs['P02S-076']['condition']
    assert '同巨、武相、廉府' in rs['P02S-083']['condition']


def test_subjects_exceptions_and_case_boundaries_cannot_be_silently_normalized():
    rs = {r['projection_rule_id']: r for r in load()['records']}
    assert '太阳化忌、太阴化忌' in rs['P02S-046']['condition']
    assert rs['P02S-056']['gap_id'].endswith('C02')
    assert '未指定哪一星化忌' in rs['P02S-056']['normalized_claim']
    assert '见辅佐吉曜' in rs['P02S-062']['condition'] and '更见禄马交驰' in rs['P02S-062']['condition']
    assert '即使无煞' in rs['P02S-077']['condition']
    assert '字形未定' in rs['P02S-045']['source_literal_claim']
    for rid in ('P02S-041', 'P02S-049', 'P02S-050', 'P02S-051', 'P02S-053', 'P02S-070', 'P02S-081'):
        assert rs[rid]['case_support_only'] and rs[rid]['case_support_reason']
        assert rs[rid]['disposition'] == 'CASE_SUPPORT_ONLY'
    for r in rs.values():
        assert not r['canonical_mapping_approved'] and not r['executable'] and r['history_feedback'] == 0
        assert r['condition_encoding'] == 'SOURCE_NATIVE_TEXT_NOT_BOOLEAN_IR'
        assert r['printed_page'] in (25, 26) and r['pdf_physical_page'] == 13
    assert not load()['whole_chapter_complete']
    assert '3 太阳' in load()['next_source_anchor']


def test_palace_recovery_keeps_authority_and_execution_separate():
    state = (ROOT / 'knowledge/states/P02_SIBLINGS_STATE.yaml').read_text()
    assert 'authoritative_execution: "GITHUB_ISSUE"\n' in state
    assert 'canonical_branch: "main"\n' in state
    assert 'contract: "governance/KNOWLEDGE_SHARD_EXECUTION_v1.md"\n' in state
    assert '\nexecution:\n' in state

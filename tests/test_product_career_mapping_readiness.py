"""Audit completeness, blocked handoffs and no implicit activation."""
import copy
from pathlib import Path

import pytest

from validation.product.issue_359_mapping_readiness import audit_mapping_readiness as audit

ROOT=Path(__file__).resolve().parents[1]


def test_current_inventory_counts_each_mapping_once_and_reconciles_corpus():
    report=audit.audit(ROOT)
    c=report['counts']
    assert c['canonical_source_rows']==888
    assert c['unique_mapping_ids']==52
    assert c['compiled_product_rules']==43
    assert c['blocked_mapping_ids']==9
    assert c['static_candidates_not_selected']==0
    assert c['source_rows_without_scoped_mapping']==836
    assert sum(c['unmapped_source_groups'].values())==836
    assert c['unmapped_source_groups']=={'CASE_SUPPORT_ONLY':19,'NATAL_WITHOUT_SCOPED_MAPPING':809,'NON_NATAL_SOURCE_ONLY':8}
    assert len({e['source_rule_id'] for e in report['entries']})==52
    assert c['unique_mapping_ids']+c['source_rows_without_scoped_mapping']==888
    assert report['new_executable_rules_this_audit']==0
    assert report['automatic_activation_allowed'] is False


def test_blocked_records_keep_null_conditions_and_precise_requirements():
    entries={e['source_rule_id']:e for e in audit.audit(ROOT)['entries']}
    expected={'CA01-020','CA01-035','CA01-043','CA01-045','CA02-158','CA02-164','CA02-194','CA05-403','CA08-766'}
    assert {rid for rid,e in entries.items() if e['classification']=='BLOCKED'}==expected
    assert all(entries[rid]['next_requirement_zh'] for rid in expected)
    assert all(entries[rid]['condition_is_null'] for rid in ('CA01-035','CA01-043','CA01-045'))
    assert all(e['automatic_activation_allowed'] is False for e in entries.values())


def test_static_candidate_without_product_selection_is_reported_but_never_activated():
    registry=audit.read_json(ROOT/audit.REGISTRY_PATH)
    before=copy.deepcopy(registry)
    registry['additional_source_mappings'][0]['selected_rule_ids'].remove('CA03-285')
    del registry['rules']['CA03-285']
    candidate=copy.deepcopy(registry)
    report=audit.audit(ROOT,registry_document=registry)
    assert report['counts']['compiled_product_rules']==42
    assert report['counts']['static_candidates_not_selected']==1
    entry=next(e for e in report['entries'] if e['source_rule_id']=='CA03-285')
    assert entry['classification']=='STATIC_CANDIDATE_NOT_SELECTED'
    assert registry==candidate
    assert audit.read_json(ROOT/audit.REGISTRY_PATH)==before


def test_duplicate_artifact_cannot_inflate_mapped_count():
    with pytest.raises(ValueError,match='duplicate mapping ID'):
        audit.audit(ROOT,mapping_paths=(*audit.MAPPING_PATHS,audit.MAPPING_PATHS[0]))


def test_canonical_drift_in_blocked_mapping_is_rejected(monkeypatch):
    original=audit.read_json
    def altered(path):
        value=original(path)
        if Path(path).name=='CAREER_CONTEXT_MAP_CA01_020_v0.1.json':
            value['mappings'][0]['expected_projection']['projection_target']='unsupported_general_rule'
        return value
    monkeypatch.setattr(audit,'read_json',altered)
    with pytest.raises(ValueError,match='canonical drift in projection_target'):
        audit.audit(ROOT)


def test_blocked_mapping_cannot_be_smuggled_into_product_selection():
    registry=audit.read_json(ROOT/audit.REGISTRY_PATH)
    registry['additional_source_mappings'][0]['selected_rule_ids'].append('CA02-158')
    registry['rules']['CA02-158']=copy.deepcopy(registry['rules']['CA02-160'])
    with pytest.raises(ValueError,match='execution readiness'):
        audit.audit(ROOT,registry_document=registry)


def test_legacy_history_field_omission_is_visible_and_not_invented():
    report=audit.audit(ROOT)
    omitted=[e for e in report['entries'] if not e['history_feedback_field_present_in_mapping']]
    assert {e['source_rule_id'] for e in omitted}=={'CA04-347','CA04-349','CA09-852'}
    assert all(e['canonical_history_feedback']=='' and 'history_feedback' not in e['source_provenance'] for e in omitted)
    assert report['counts']['legacy_mapping_history_field_omissions']==3


def test_missing_legacy_field_cannot_hide_nonempty_canonical_history(monkeypatch):
    original=audit.read_rows
    def altered(path):
        rows=original(path)
        for row in rows:
            if row['projection_rule_id']=='CA04-347':row['history_feedback']='UNREVIEWED_HISTORY'
        return rows
    monkeypatch.setattr(audit,'read_rows',altered)
    with pytest.raises(ValueError,match='canonical drift in history_feedback'):
        audit.audit(ROOT)

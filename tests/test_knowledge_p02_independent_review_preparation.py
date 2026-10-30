"""Negative controls for the handoff preparation; no self-approval capability."""
import copy,importlib.util,json
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'validation/knowledge/palaces/P02_siblings/issue_928/verify_review_inputs.py'
spec=importlib.util.spec_from_file_location('p02_handoff_recompute',P);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
def inputs():
 lock=v.load(ROOT/v.LOCK_PATH)
 ds=[v.load(ROOT/p['path']) for p in lock['frozen_accepted_inputs'] if p['kind']=='SOURCE_LEDGER']
 cs=[v.load(ROOT/p['path']) for p in lock['frozen_accepted_inputs'] if p['kind']=='CENSUS_CHECKPOINT']
 return ds,[a for c in cs if 'owned_anchors' in c for a in c['owned_anchors']],[r for c in cs if c.get('role','').startswith('HELD_ACCOUNTING') for r in c['records']]
def test_mechanical_success_never_grants_independent_approval():
 result=v.verify()
 assert result['mechanical_checks_passed'] and result['recomputed_counts']['source_records']==424
 assert not result['independent_review_complete'] and not result['source_stage_can_close'] and not result['runtime_authorized']
 lock=v.load(ROOT/v.LOCK_PATH)
 assert lock['preparer']['participated_in_issue_921_production'] and not lock['preparer']['independent_approval_authorized']
 assert not lock['independent_review']['completed'] and lock['independent_review']['reviewer_identity'] is None
 assert len(lock['frozen_accepted_inputs'])==19 and lock['review_limits']['persistent_review_objects']==25
def test_duplicate_source_id_is_rejected_even_if_count_is_424():
 ds,a,h=inputs();ds[0]['records'][1]['projection_rule_id']=ds[0]['records'][0]['projection_rule_id']
 with pytest.raises(ValueError,match='SOURCE_IDS'):v.validate_accounting(ds,a,h)
def test_gap_reassignment_and_duplicate_held_index_are_rejected():
 ds,a,h=inputs();ds[0]['source_coverage_gaps'][0]['affected_record_ids'][0]=ds[0]['source_coverage_gaps'][0]['affected_record_ids'][1]
 with pytest.raises(ValueError,match='HELD_GAP_ASSIGNMENT'):v.validate_accounting(ds,a,h)
 ds,a,h=inputs();h[1]=copy.deepcopy(h[0])
 with pytest.raises(ValueError,match='HELD_INDEX'):v.validate_accounting(ds,a,h)
def test_secondary_notes_and_nonnull_text_cannot_be_ignored_or_promoted():
 ds,a,h=inputs();h[0]['original_notes']='silently removed uncertainty'
 with pytest.raises(ValueError,match='HELD_EVIDENCE_CHANGED'):v.validate_accounting(ds,a,h)
 ds,a,h=inputs();row=next(r for r in h if r['raw_unresolved_fields_nonnull']);row['effective_executable']=True
 with pytest.raises(ValueError,match='HELD_EXECUTION_OR_NORMALIZATION_PROMOTED'):v.validate_accounting(ds,a,h)
def test_duplicate_paragraph_owner_is_rejected():
 ds,a,h=inputs();a[1]['record_ids'].append(a[0]['record_ids'][0])
 with pytest.raises(ValueError,match='ATOM_PARAGRAPH_OWNERSHIP'):v.validate_accounting(ds,a,h)

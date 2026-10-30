"""A completed independent review with blockers is not an approval."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'knowledge/palaces/P02_siblings/handoff/issue_928'
def test_independent_first_verdict_blocks_closure_and_preserves_correct_source_record():
 v=json.loads((D/'INDEPENDENT_REVIEW_VERDICT_v0.1.json').read_text())
 assert v['independent_review_completed'] and not v['participated_in_issue_921_production']
 assert v['reviewer_task_identity']=='/root/p02_independent_review' and v['source_pdf_directly_inspected']
 assert v['verdict']=='NEEDS_BOUNDED_CENSUS_EVIDENCE_REPAIR'
 assert not v['approved'] and not v['stage_closure_authorized'] and not v['whole_chapter_complete']
 assert not v['runtime_authorized'] and not v['mapping_authorized']
 f=v['blocking_findings'][0];assert len(v['blocking_findings'])==1
 assert f['source_record_condition_correct'] and not f['requires_source_atom_rewrite']
 assert f['observed_left_tail']=='为武曲、破' and f['recorded_left_tail']=='天机、巨门、破'
 assert len(f['affected_frozen_fields'])==2 and f['affected_record_id']=='P02S-167'
 assert v['retained_holds']['held_count']==140 and v['retained_holds']['gap_count']==49
def test_independent_evidence_uses_the_original_frozen_bytes():
 lock=json.loads((D/'INDEPENDENT_REVIEW_INPUT_LOCK_v0.1.json').read_text())
 for p in lock['frozen_accepted_inputs']:
  assert hashlib.sha256((ROOT/p['path']).read_bytes()).hexdigest()==p['sha256']
 v=json.loads((D/'INDEPENDENT_REVIEW_VERDICT_v0.1.json').read_text())
 assert v['frozen_input_checks']['checked_count']==19 and v['frozen_input_checks']['sha256_all_match']
 assert (ROOT/v['frozen_input_checks']['evidence_path']).is_file()
 assert (ROOT/v['report_path']).is_file()

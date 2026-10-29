"""A census quote fix must never mutate the correct source atom or other coverage."""
import copy,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/'knowledge/palaces/P02_siblings/census/issue_921'
NEW=ROOT/'knowledge/palaces/P02_siblings/census/issue_934'
def read(p):return json.loads(p.read_text())
def test_w13_exact_source_tail_is_corrected_in_both_new_views():
 m=read(NEW/'P02_CHAPTER_CENSUS_MANIFEST_v0.2.json');p=read(NEW/'P02_SOURCE_COVERAGE_PHYSICAL_14_v0.2.json')
 for links in (m['cross_page_links'],p['continuations']):
  x=next(x for x in links if x['qualified_anchor_id']=='SB04:W13')
  assert x['left_tail']=='为武曲、破' and x['right_head']=='军、七杀躔兄弟宫之年'
  assert '天机' not in x['left_tail'] and '巨门' not in x['left_tail']
 assert m['evidence_erratum']['source_record_rewrites']==0 and not m['evidence_erratum']['stage_closure_authorized']
def test_original_nineteen_inputs_are_frozen_and_correct_record_stays_held():
 e=read(NEW/'W13_CENSUS_EVIDENCE_ERRATUM_v0.1.json');assert len(e['frozen_accepted_inputs'])==19
 for pin in e['frozen_accepted_inputs']:
  assert hashlib.sha256((ROOT/pin['path']).read_bytes()).hexdigest()==pin['sha256'] and pin['read_only']
 d=read(ROOT/'knowledge/palaces/P02_siblings/wp05/SIBLINGS_SB04_WUQU_SOURCE_AUDIT_v0.1.json')
 r=next(r for r in d['records'] if r['projection_rule_id']=='P02S-167')
 assert r['condition']=='不利之克应，为武曲、破军、七杀躔兄弟宫之年'
 assert not r['canonical_promotion'] and not r['executable'] and r['gap_id']=='P02-SB04-GAP-C01'
 assert r['time_layer']=='YEAR'
def test_physical14_revision_has_no_unrelated_semantic_changes():
 old=read(OLD/'P02_SOURCE_COVERAGE_PHYSICAL_14_v0.1.json');new=read(NEW/'P02_SOURCE_COVERAGE_PHYSICAL_14_v0.2.json')
 assert new.pop('supersedes')=={'path':str((OLD/'P02_SOURCE_COVERAGE_PHYSICAL_14_v0.1.json').relative_to(ROOT)),'sha256':hashlib.sha256((OLD/'P02_SOURCE_COVERAGE_PHYSICAL_14_v0.1.json').read_bytes()).hexdigest(),'read_only_preserved':True}
 assert new['review_object_count']==new['reasoning_batch_count']==50
 for k in ('schema_version','issue','checkpoint_id','review_object_count','reasoning_batch_count'):new[k]=old[k]
 next(x for x in new['continuations'] if x['qualified_anchor_id']=='SB04:W13')['left_tail']='天机、巨门、破'
 assert new==old
 defunct=read(OLD/'P02_SOURCE_COVERAGE_PHYSICAL_14_v0.1.json')
 assert next(x for x in defunct['continuations'] if x['qualified_anchor_id']=='SB04:W13')['left_tail']=='天机、巨门、破'
def test_manifest_revision_changes_only_evidence_pointer_and_version_metadata():
 old=read(OLD/'P02_CHAPTER_CENSUS_MANIFEST_v0.1.json');new=read(NEW/'P02_CHAPTER_CENSUS_MANIFEST_v0.2.json')
 assert new['counts']==old['counts'] and new['frozen_source_ledgers']==old['frozen_source_ledgers']
 assert not new['whole_chapter_complete'] and not new['independent_stage_handoff_review_complete']
 assert not any(new['execution_boundary'].values())
 assert new['review_limits']['manifest_persistent_review_objects']==96<=100
 assert new['review_limits']['manifest_provenance_structure_reasoning_batch']==47<=50
 diff=[(a,b) for a,b in zip(old['checkpoints'],new['checkpoints']) if a!=b];assert len(diff)==1
 a,b=diff[0];assert 'PHYSICAL_14' in a['path'] and 'PHYSICAL_14' in b['path']
 assert hashlib.sha256((ROOT/b['path']).read_bytes()).hexdigest()==b['sha256'] and b['review_object_count']==50
 new.pop('supersedes');new.pop('evidence_erratum')
 for k in ('schema_version','artifact_id','issue','base_main','status','review_limits','checkpoints'):new[k]=old[k]
 next(x for x in new['cross_page_links'] if x['qualified_anchor_id']=='SB04:W13')['left_tail']='天机、巨门、破'
 assert new==old

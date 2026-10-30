"""Recompute mechanical handoff facts; this script cannot grant independent approval."""
import hashlib,json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
LOCK_PATH=Path('knowledge/palaces/P02_siblings/handoff/issue_928/INDEPENDENT_REVIEW_INPUT_LOCK_v0.1.json')
def load(path):return json.loads(path.read_text())
def validate_accounting(ledgers,anchors,held_index):
 records=[r for d in ledgers for r in d['records']]
 ids=[r['projection_rule_id'] for r in records]
 if ids!=[f'P02S-{i:03}' for i in range(1,425)]:raise ValueError('SOURCE_IDS_NOT_EXACT_OR_UNIQUE')
 promoted=[r for r in records if r['canonical_promotion']]
 held={r['projection_rule_id']:r for r in records if not r['canonical_promotion']}
 gaps=[g for d in ledgers for g in d['source_coverage_gaps']]
 if len({g['gap_id'] for g in gaps})!=49:raise ValueError('GAP_ID_SET_INVALID')
 assignments=[rid for g in gaps for rid in g['affected_record_ids']]
 if Counter(assignments)!=Counter(held.keys()):raise ValueError('HELD_GAP_ASSIGNMENT_NOT_UNIQUE_OR_COMPLETE')
 gap_lookup={g['gap_id']:g for g in gaps}
 for rid,r in held.items():
  if rid not in gap_lookup[r['gap_id']]['affected_record_ids']:raise ValueError('PRIMARY_GAP_MISMATCH')
 if Counter(r['record_id'] for r in held_index)!=Counter(held.keys()):raise ValueError('HELD_INDEX_INCOMPLETE_OR_DUPLICATED')
 for indexed in held_index:
  old=held[indexed['record_id']]
  if indexed['primary_gap_id']!=old['gap_id'] or indexed['source_condition_verbatim']!=old['condition'] or indexed['source_claim_verbatim']!=old['literal_claim'] or indexed['original_notes']!=old['notes']:raise ValueError('HELD_EVIDENCE_CHANGED')
  if indexed['effective_executable'] or indexed['effective_normalization_authorized'] or indexed['canonical_promotion_by_census']:raise ValueError('HELD_EXECUTION_OR_NORMALIZATION_PROMOTED')
 ownership=[rid for a in anchors for rid in a['record_ids']]
 if Counter(ownership)!=Counter(ids):raise ValueError('ATOM_PARAGRAPH_OWNERSHIP_NOT_UNIQUE_OR_COMPLETE')
 if len({a['qualified_anchor_id'] for a in anchors})!=151:raise ValueError('PARAGRAPH_COUNT_NOT_151')
 if any(r['executable'] or r['canonical_mapping_approved'] or r['history_feedback'] for r in records):raise ValueError('SOURCE_ONLY_BOUNDARY_BROKEN')
 result={'source_records':len(records),'accepted_including_case':len(promoted),'accepted_reusable_source_method':sum(not r['case_support_only'] for r in promoted),'accepted_case_only':sum(r['case_support_only'] for r in promoted),'held':len(held),'gap_groups':len(gaps),'unique_paragraphs':len(anchors)}
 if result!={'source_records':424,'accepted_including_case':284,'accepted_reusable_source_method':180,'accepted_case_only':104,'held':140,'gap_groups':49,'unique_paragraphs':151}:raise ValueError('DISPOSITION_COUNTS_CHANGED')
 return result
def verify(root=ROOT):
 lock=load(root/LOCK_PATH)
 for pin in lock['frozen_accepted_inputs']:
  if hashlib.sha256((root/pin['path']).read_bytes()).hexdigest()!=pin['sha256']:raise ValueError('FROZEN_INPUT_HASH_CHANGED:'+pin['path'])
 source=[load(root/p['path']) for p in lock['frozen_accepted_inputs'] if p['kind']=='SOURCE_LEDGER']
 checkpoints=[load(root/p['path']) for p in lock['frozen_accepted_inputs'] if p['kind']=='CENSUS_CHECKPOINT']
 anchors=[a for c in checkpoints if 'owned_anchors' in c for a in c['owned_anchors']]
 held=[r for c in checkpoints if c.get('role','').startswith('HELD_ACCOUNTING') for r in c['records']]
 counts=validate_accounting(source,anchors,held)
 return {'issue':928,'input_base_main':lock['accepted_main'],'recomputed_counts':counts,'mechanical_checks_passed':True,'independent_review_complete':False,'source_stage_can_close':False,'independent_review_blocker':'SEPARATE_NON_PRODUCER_SOURCE_REVIEW_AND_RECORDED_VERDICT_REQUIRED','new_source_records':0,'gaps_resolved':0,'runtime_authorized':False}
if __name__=='__main__':print(json.dumps(verify(),ensure_ascii=False,indent=2))

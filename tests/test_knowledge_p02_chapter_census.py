"""P02 #921: pin, coverage and held accounting; never semantic promotion."""
import hashlib,json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DIR=ROOT/'knowledge/palaces/P02_siblings/census/issue_921'
def read(p):return json.loads(p.read_text())
def manifest():return read(DIR/'P02_CHAPTER_CENSUS_MANIFEST_v0.1.json')
def checkpoints():return [read(ROOT/p['path']) for p in manifest()['checkpoints']]
def source_records():return [r for pin in manifest()['frozen_source_ledgers'] for r in read(ROOT/pin['path'])['records']]
def held_rows():return [r for c in checkpoints() if c['role'].startswith('HELD_ACCOUNTING') for r in c['records']]
def owned_anchors():return [a for c in checkpoints() if 'owned_anchors' in c for a in c['owned_anchors']]
def test_all_eleven_accepted_ledgers_and_seven_checkpoint_hashes_are_pinned():
 m=manifest();assert len(m['frozen_source_ledgers'])==11 and len(m['checkpoints'])==7
 for p in m['frozen_source_ledgers']+m['checkpoints']:
  raw=(ROOT/p['path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==p['sha256']
 for pin in m['frozen_source_ledgers']:assert pin['read_only']
def test_exact_424_record_accounting_without_source_promotion():
 m=manifest();rs=source_records();accepted=[r for r in rs if r['canonical_promotion']]
 assert [r['projection_rule_id'] for r in rs]==[f'P02S-{i:03}' for i in range(1,425)]
 assert len(accepted)==284 and sum(r['case_support_only'] for r in accepted)==104
 assert sum(not r['case_support_only'] for r in accepted)==180
 assert m['counts']['source_atoms_reviewed']==424 and m['new_source_records']==0 and m['newly_resolved_gaps']==0
 assert len({(r['base_subject'],r['condition'],r['literal_claim']) for r in rs})==424
def test_each_source_atom_has_exactly_one_paragraph_owner_even_across_pages():
 m=manifest();anchors=owned_anchors();qids=[a['qualified_anchor_id'] for a in anchors]
 assert len(qids)==len(set(qids))==m['counts']['unique_paragraph_anchors']==151
 owners=[rid for a in anchors for rid in a['record_ids']]
 assert len(owners)==len(set(owners))==424
 assert set(owners)=={r['projection_rule_id'] for r in source_records()}
 for a in anchors:
  old=read(ROOT/a['source_ledger_path']);rs=[r for r in old['records'] if r['source_anchor']==a['anchor']]
  assert a['record_ids']==[r['projection_rule_id'] for r in rs]
  assert a['source_span_id']==rs[0]['source_span_id']
  assert a['printed_page_start']==min(r['printed_page'] for r in rs)
  assert a['printed_page_end']==max(r.get('printed_page_end',r['printed_page']) for r in rs)
  assert a['physical_page_owner']==(a['printed_page_start']+1)//2
  assert not a['new_source_assertion']
def test_all_eight_printed_pages_and_four_cross_page_slices_are_accounted():
 m=manifest();slices=[p for c in checkpoints() if 'page_slices' in c for p in c['page_slices']]
 assert [p['printed_page'] for p in slices]==list(range(25,33))
 assert sum(p['paragraph_slice_count'] for p in slices)==m['counts']['printed_page_slices']==155
 anchors=owned_anchors()
 for p in slices:
  pg=p['printed_page'];assert p['direct_visual_verified']
  assert p['pdf_physical_page']==(pg+1)//2 and p['half']==('LEFT' if pg%2 else 'RIGHT')
  assert set(p['qualified_anchor_refs'])=={a['qualified_anchor_id'] for a in anchors if a['printed_page_start']<=pg<=a['printed_page_end']}
 links=m['cross_page_links'];assert len(links)==4
 assert {(x['qualified_anchor_id'],x['from_page'],x['to_page']) for x in links}=={('SB03:S09',26,27),('SB04:W13',27,28),('SB05:T17',28,29),('SB09:J03',30,31)}
 assert all(x['direct_visual_verified'] and x['left_tail'] and x['right_head'] for x in links)
 assert {b['printed_page'] for b in m['source_basis']['negative_boundaries']}=={24,33}
def test_fourteen_section_paragraph_census_matches_owned_anchors():
 ss=manifest()['sections'];assert [s['section_number'] for s in ss]==list(range(1,15))
 assert [s['title'] for s in ss]==['紫微','天机','太阳','武曲','天同','廉贞','天府','太阴','贪狼','巨门','天相','天梁','七杀','破军']
 for s in ss:
  a=[a for a in owned_anchors() if a['source_ledger_path']==s['ledger_path'] and a['anchor'].startswith(s['anchor_prefix'])]
  assert len(a)==s['expected_paragraph_count']==s['visual_paragraph_count']
 assert sum(s['visual_paragraph_count'] for s in ss)==151
def test_140_held_rows_and_49_gaps_have_no_orphans_or_duplicate_assignment():
 m=manifest();rows=held_rows();rs={r['projection_rule_id']:r for r in source_records()};gaps=m['retained_gap_register']
 assert [c['review_object_count'] for c in checkpoints() if 'records' in c]==[45,48,47]
 assert len(rows)==len({r['record_id'] for r in rows})==140 and len(gaps)==49
 assert {r['record_id'] for r in rows}=={rid for rid,r in rs.items() if not r['canonical_promotion']}
 covered=[rid for g in gaps for rid in g['original_affected_record_ids']]
 assert len(covered)==len(set(covered))==140 and set(covered)=={r['record_id'] for r in rows}
 for r in rows:
  old=rs[r['record_id']];g=next(g for g in gaps if g['gap_id']==r['primary_gap_id'])
  assert old['gap_id']==r['primary_gap_id'] and r['record_id'] in g['original_affected_record_ids']
  assert r['source_condition_verbatim']==old['condition'] and r['source_claim_verbatim']==old['literal_claim']
  assert r['original_notes']==old['notes'] and r['original_disposition']==old['disposition']
  assert not r['effective_normalization_authorized'] and not r['effective_executable'] and not r['canonical_promotion_by_census']
  assert r['local_work_can_continue'] and not r['human_gate_now']
def test_core_holds_and_legacy_nonnull_text_never_unlock_from_a_census():
 m=manifest();gs=[g for g in m['retained_gap_register'] if g['core_gap']]
 assert {g['gap_id'] for g in gs}=={'P02-SB06-GAP-G01','P02-SB11-GAP-C04'}
 assert all(g['blocking_class']=='LOCAL_FAIL_CLOSED_NOT_D3' and not g['pi_gate_now'] for g in gs)
 r=next(r for r in held_rows() if r['record_id']=='P02S-261')
 assert 'Core #915 describes 冲起 only' in r['core_915_note'] and not r['effective_executable']
 legacy=[r for r in held_rows() if r['raw_unresolved_fields_nonnull']]
 assert len(legacy)==m['deterministic_accounting']['raw_legacy_held_with_nonnull_normalized_fields']==45
 assert all(not r['effective_normalization_authorized'] for r in legacy)
def test_review_checkpoint_limits_and_independent_handoff_remain_required():
 m=manifest();assert all(c['review_object_count']<=100 and c['reasoning_batch_count']<=50 for c in checkpoints())
 assert m['review_limits']['manifest_persistent_review_objects']==92<=100
 assert m['review_limits']['manifest_gap_reasoning_batch']==49<=50 and m['review_limits']['manifest_provenance_structure_reasoning_batch']==43<=50
 assert m['source_coverage_census_complete'] and m['held_gap_accounting_complete']
 assert not m['independent_stage_handoff_review_complete'] and not m['whole_chapter_complete']
 assert not any(m['execution_boundary'].values()) and '不得' in m['next_work']
 state=(ROOT/'knowledge/states/P02_SIBLINGS_STATE.yaml').read_text()
 assert 'whole_chapter_complete: false' in state and 'independent_stage_handoff_review_complete: false' in state

"""Source fidelity, old-ledger conservation and fail-closed scope for P02 #871."""
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'knowledge/palaces/P02_siblings/wp05/SIBLINGS_SB05_TIANTONG_SOURCE_AUDIT_v0.1.json'
def load():return json.loads(PATH.read_text())
def rows():return load()['records']
def test_old_four_ledgers_are_byte_pinned_and_new_ids_follow_without_overlap():
 d=load();old=[]
 assert len(d['accepted_input_pins'])==4
 for pin in d['accepted_input_pins']:
  raw=(ROOT/pin['path']).read_bytes()
  assert hashlib.sha256(raw).hexdigest()==pin['sha256'] and pin['read_only']
  old+=json.loads(raw)['records']
 assert len(old)==177
 assert [r['projection_rule_id'] for r in rows()]==[f'P02S-{i:03}' for i in range(178,229)]
 assert not {r['projection_rule_id'] for r in old}&{r['projection_rule_id'] for r in rows()}
def test_counts_coverage_and_one_to_one_gap_membership():
 d=load();rs=rows();s=d['summary']
 assert len(rs)==s['source_atoms_reviewed']==51
 assert {r['source_anchor'] for r in rs}=={f'T{i:02}' for i in range(1,18)}
 assert s['source_records_added']==37 and s['held']==14 and s['source_gap_count']==5
 assert s['reusable_projection_method_records']==20 and s['case_support_only']==17
 assert sum(r['canonical_promotion'] for r in rs)==37
 assert sum(r['canonical_promotion'] and r['case_support_only'] for r in rs)==17
 held={r['projection_rule_id'] for r in rs if not r['canonical_promotion']}
 covered=[rid for g in d['source_coverage_gaps'] for rid in g['affected_record_ids']]
 assert len(covered)==len(set(covered))==14 and set(covered)==held
 assert s['durable_review_object_count']==51+4+2<=100
 assert all(b['count']<=50 for b in s['reasoning_sub_batches'])
 for r in rs:
  if r['gap_id']:
   assert r['canonical_condition'] is None and r['normalized_claim'] is None
   assert not r['normalization_verified'] and r['normalization_epistemic']=='UNRESOLVED'
def test_periods_do_not_become_years_and_star_subjects_are_distinct():
 ts=[r for r in rows() if r['gap_id'] and r['gap_id'].endswith('T01')]
 assert len(ts)==3
 for r in ts:
  assert r['time_layer'] is None and r['primary_time_layer'] is None
  assert r['source_time_layers']==[] and not r['canonical_promotion']
 assert all(r['time_layer'] not in ('YEAR','DECADE') for r in rows())
 liang=next(r for r in ts if r['source_anchor']=='T09')
 sihai=next(r for r in ts if r['source_anchor']=='T16')
 assert '天相、巨门' in liang['condition']
 assert '[天机巨门]、天梁' in sihai['condition'] and '天相巨门' not in sihai['condition']
def test_anomalous_literals_and_unresolved_antecedents_stay_closed():
 rs=rows()
 ten=[r for r in rs if r['source_anchor']=='T10']
 assert len(ten)==4 and all('卯本' in r['condition'] and r['gap_id'].endswith('L01') for r in ten)
 for literal,gap in [('主各胞','L02'),('尤确','L03')]:
  r=next(r for r in rs if r['literal_claim']==literal)
  assert r['gap_id'].endswith(gap) and not r['canonical_promotion']
 corrected=next(r for r in rs if r['literal_claim']=='唯一般情形下姊妹多于兄弟')
 assert corrected['canonical_promotion'] and corrected['case_support_only']
 assert not any('唯一一般' in r['literal_claim'] for r in rs)
 for anchor,literal in [('T02','又主受友情拖累'),('T04','则易以终隙收束'),('T08','主有异母兄弟'),('T17','唯无太多实际助力')]:
  r=next(r for r in rs if r['source_anchor']==anchor and r['literal_claim']==literal)
  assert r['gap_id'].endswith('C01')
def test_cross_page_tail_and_modal_qualitative_counterexamples():
 rs=rows();cross=[r for r in rs if r['source_anchor']=='T17' and r['printed_page_end']==29]
 assert len(cross)==2
 assert all((r['printed_page'],r['pdf_physical_page'],r['pdf_physical_page_end'])==(28,14,15) for r in cross)
 assert any(r['literal_claim']=='且主为人能结交中下层的朋友' and r['case_support_only'] for r in cross)
 assert any(r['literal_claim']=='则和好而易离散' and '见吉' in r['condition'] for r in rs)
 assert any(r['literal_claim']=='仅主兄弟温驯' and '见吉' in r['condition'] for r in rs)
 assert any(r['literal_claim']=='友人亦助力薄弱' and '见吉' in r['condition'] for r in rs)
 assert any(r['literal_claim']=='但仍必须事事亲力亲为' and '合作的机会' in r['condition'] for r in rs)
 assert any(r['literal_claim']=='常有与人合资的冲动' and '倾向不等实际已合资' in r['notes'] for r in rs)
def test_case_only_and_runtime_boundaries():
 d=load()
 for r in rows():
  assert r['source_span_verified'] and r['source_epistemic']=='EXPLICIT'
  assert not r['canonical_mapping_approved'] and not r['executable'] and r['history_feedback']==0
  assert r['condition_encoding']=='SOURCE_NATIVE_TEXT_NOT_BOOLEAN_IR'
  if r['source_anchor'] in ('T01','T10'):
   assert r['case_support_only'] and r['case_support_reason']
  if any(t in r['literal_claim'] for t in ('弱智者','各怀鬼胎','先姊','兄弟五人')):
   assert r['case_support_only']
 assert not d['whole_chapter_complete'] and '6 廉贞' in d['next_source_anchor']
 assert all(d['execution_boundary'][k]==0 for k in ('history_feedback','conditions_compiled','execution_unlocked'))

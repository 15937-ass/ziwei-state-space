"""P02 Wuqu source fidelity, coverage and isolation checks."""
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'knowledge/palaces/P02_siblings/wp05/SIBLINGS_SB04_WUQU_SOURCE_AUDIT_v0.1.json'
def load():return json.loads(PATH.read_text())
def rows():return load()['records']
def test_accepted_inputs_are_byte_preserved_and_new_ids_are_disjoint():
 d=load(); old=[]
 for pin in d['accepted_input_pins']:
  raw=(ROOT/pin['path']).read_bytes()
  assert hashlib.sha256(raw).hexdigest()==pin['sha256'] and pin['read_only']
  old+=json.loads(raw)['records']
 assert len(old)==134
 assert [r['projection_rule_id'] for r in rows()]==[f'P02S-{i:03}' for i in range(135,178)]
 assert not {r['projection_rule_id'] for r in old}&{r['projection_rule_id'] for r in rows()}
def test_counts_unique_gaps_and_full_paragraph_coverage():
 d=load();rs=rows();s=d['summary']
 assert {r['source_anchor'] for r in rs}=={f'W{i:02}' for i in range(1,17)}
 assert len(rs)==s['source_atoms_reviewed']==43
 held={r['projection_rule_id'] for r in rs if not r['canonical_promotion']}
 coverage=[rid for g in d['source_coverage_gaps'] for rid in g['affected_record_ids']]
 assert len(coverage)==len(set(coverage))==len(held)==s['held']
 assert set(coverage)==held
 assert sum(r['canonical_promotion'] for r in rs)==s['source_records_added']
 assert sum(r['canonical_promotion'] and r['case_support_only'] for r in rs)==s['case_support_only']
 assert s['source_records_added']==s['reusable_projection_method_records']+s['case_support_only']
 assert len(rs)+5==s['durable_review_object_count']<=100
 assert all(b['count']<=50 for b in s['reasoning_sub_batches'])
 for r in rs:
  if r['gap_id']:
   assert r['normalization_epistemic']=='UNRESOLVED' and not r['normalization_verified']
   assert r['canonical_condition'] is None and r['normalized_claim'] is None
  assert not r['canonical_mapping_approved'] and not r['executable'] and r['history_feedback']==0
 assert not d['whole_chapter_complete'] and '5 天同' in d['next_source_anchor']
def test_exception_chains_direction_and_real_world_conditions_are_preserved():
 rs=rows()
 assert any('除非命宫见辅弼' in r['literal_claim'] and r['cross_palace_dependency']==['命宫见辅弼'] for r in rs)
 reverse=next(r for r in rs if r['literal_claim']=='则反主益荫兄弟及友人')
 assert reverse['canonical_promotion'] and '见煞忌刑曜' in reverse['condition']
 fire=next(r for r in rs if '横发' in r['literal_claim'])
 assert all(t in fire['condition'] for t in ['火铃同度','无刑忌','自身命宫又会吉曜吉化'])
 assert fire['gap_id'].endswith('L01')
 active=next(r for r in rs if '主动助友人' in r['literal_claim'])
 assert '刑忌夹印' in active['condition'] and '行为前提' in active['notes']
 assert any('即使见吉曜' in r['condition'] and '亦不主兄弟友人得力'==r['literal_claim'] for r in rs)
 assert any('若与人合作' in r['condition'] and r['case_support_only'] for r in rs)
def test_cross_page_year_and_case_boundaries():
 rs=rows();cross=next(r for r in rs if r['source_anchor']=='W13' and r['literal_claim']=='不利之克应')
 assert (cross['printed_page'],cross['printed_page_end'])==(27,28)
 assert cross['pdf_physical_page']==cross['pdf_physical_page_end']==14
 assert '武曲、破军、七杀躔兄弟宫之年' in cross['condition']
 for r in rs:
  if '之年' in r['condition']:
   assert r['time_layer']=='YEAR' and r['source_time_layers']==['YEAR']
  assert 'DECADE' not in r['source_time_layers']
 blood=next(r for r in rs if '血光之灾' in r['literal_claim'])
 assert blood['case_support_only'] and '廉贞化忌' in blood['condition'] and '又与火铃同躔' in blood['condition']
 method=next(r for r in rs if r['source_anchor']=='W15' and r['time_layer']=='YEAR')
 assert '前句血光语境' in method['condition']
 assert all(r['case_support_only'] for r in rs if any(t in r['literal_claim'] for t in ['输血','受伤','挑引','侵吞']))
def test_anomalous_literals_and_condition_scope_fail_closed():
 rs=rows()
 for literal,gap in [('主因兄弟可友人而横发','L01'),('一为友人输血','L02'),('兄弟明友稀少','L03')]:
  r=next(r for r in rs if r['literal_claim']==literal)
  assert r['gap_id'].endswith(gap) and not r['canonical_promotion']
 for r in rs:
  if r['source_anchor']=='W09' and '见辅佐吉曜' in r['condition']:
   assert r['gap_id'].endswith('C01')
 assert any(r['literal_claim']=='情形则较佳' and r['gap_id'].endswith('C01') for r in rs)

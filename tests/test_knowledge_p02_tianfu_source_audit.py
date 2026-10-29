"""P02 #879 source identity, temporal and input conservation checks."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'knowledge/palaces/P02_siblings/wp05/SIBLINGS_SB07_TIANFU_SOURCE_AUDIT_v0.1.json'
def data():return json.loads(PATH.read_text())
def test_six_prior_ledgers_and_new_ids_are_conserved():
 d=data();old=[]
 assert len(d['accepted_input_pins'])==6
 for p in d['accepted_input_pins']:
  raw=(ROOT/p['path']).read_bytes()
  assert hashlib.sha256(raw).hexdigest()==p['sha256'] and p['read_only']
  old+=json.loads(raw)['records']
 assert len(old)==279
 assert [r['projection_rule_id'] for r in d['records']]==[f'P02S-{i:03}' for i in range(280,295)]
 assert not {r['projection_rule_id'] for r in old}&{r['projection_rule_id'] for r in d['records']}
def test_complete_source_anchor_counts_and_unique_gap_coverage():
 d=data();rs=d['records'];s=d['summary']
 assert {r['source_anchor'] for r in rs}=={f'F{i:02}' for i in range(1,7)}
 assert len(rs)==s['source_atoms_reviewed']==15
 assert sum(r['canonical_promotion'] for r in rs)==s['source_records_added']==10
 assert sum(r['canonical_promotion'] and r['case_support_only'] for r in rs)==s['case_support_only']==8
 assert s['reusable_projection_method_records']==2 and s['source_gap_count']==4
 held={r['projection_rule_id'] for r in rs if not r['canonical_promotion']}
 covered=[rid for g in d['source_coverage_gaps'] for rid in g['affected_record_ids']]
 assert len(covered)==len(set(covered))==s['held']==5 and set(covered)==held
 assert s['durable_review_object_count']==15+6+2<=100
 assert all(b['count']<=50 for b in s['reasoning_sub_batches'])
def test_literal_anomalies_and_time_layers_fail_closed():
 rs=data()['records']
 glyph=next(r for r in rs if r['literal_claim']=='主兄弟各胞')
 assert glyph['gap_id'].endswith('L01') and not glyph['canonical_promotion']
 anomaly=next(r for r in rs if '[天同太阳]' in r['literal_claim'])
 assert anomaly['gap_id'].endswith('L02') and '[太阳巨门]' in anomaly['condition']
 assert '天同太阴' not in anomaly['condition'] and anomaly['time_layer'] is None
 methods=[r for r in rs if r['source_anchor']=='F06' and r['gap_id']]
 assert len(methods)==3
 assert all(r['time_layer'] is None and r['source_time_layers']==[] for r in methods)
 assert all(r['time_layer'] not in ('YEAR','DECADE') for r in rs)
 for r in rs:
  if r['gap_id']:
   assert not r['normalization_verified'] and r['normalization_epistemic']=='UNRESOLVED'
   assert r['canonical_condition'] is None and r['normalized_claim'] is None
def test_transformation_subjects_direction_and_case_scope_are_not_flattened():
 rs=data()['records']
 fight=next(r for r in rs if r['literal_claim']=='则为争财之兆')
 assert '武曲化忌，煞重' in fight['condition'] and '廉贞化忌' not in fight['condition']
 wealth=next(r for r in rs if r['literal_claim']=='主为兄弟或友人破财')
 assert wealth['case_support_only'] and '武曲化忌' in wealth['condition']
 feud=next(r for r in rs if r['literal_claim']=='恩反成仇')
 assert feud['case_support_only'] and '廉贞化忌' in feud['condition']
 moral=next(r for r in rs if '权术阴谋' in r['literal_claim'])
 assert moral['case_support_only'] and moral['case_support_reason']
 crowd=next(r for r in rs if r['literal_claim']=='始主兄弟众多')
 assert crowd['gap_id'].endswith('C01')
def test_source_methods_do_not_compile_or_activate_runtime():
 d=data()
 for r in d['records']:
  assert not r['canonical_mapping_approved'] and not r['executable'] and r['history_feedback']==0
  assert r['condition_encoding']=='SOURCE_NATIVE_TEXT_NOT_BOOLEAN_IR'
 advice=next(r for r in d['records'] if '须详原局' in r['literal_claim'])
 assert advice['canonical_promotion'] and not advice['case_support_only'] and advice['time_layer']=='NATAL'
 assert '不反灌' in advice['notes']
 assert not d['whole_chapter_complete'] and '8 太阴' in d['next_source_anchor']

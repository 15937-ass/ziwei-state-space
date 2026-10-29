"""P02 #877: source pinning, relative-time retention and unresolved literal safeguards."""
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'knowledge/palaces/P02_siblings/wp05/SIBLINGS_SB06_LIANZHEN_SOURCE_AUDIT_v0.1.json'
def load():return json.loads(PATH.read_text())
def rows():return load()['records']
def test_five_accepted_inputs_are_byte_preserved_with_contiguous_new_ids():
 d=load();old=[]
 assert len(d['accepted_input_pins'])==5
 for pin in d['accepted_input_pins']:
  raw=(ROOT/pin['path']).read_bytes()
  assert hashlib.sha256(raw).hexdigest()==pin['sha256'] and pin['read_only']
  old+=json.loads(raw)['records']
 assert len(old)==228
 assert [r['projection_rule_id'] for r in rows()]==[f'P02S-{i:03}' for i in range(229,280)]
 assert not {r['projection_rule_id'] for r in old}&{r['projection_rule_id'] for r in rows()}
def test_whole_section_counts_and_held_gap_coverage():
 d=load();rs=rows();s=d['summary']
 assert {r['source_anchor'] for r in rs}=={f'L{i:02}' for i in range(1,17)}
 assert len(rs)==s['source_atoms_reviewed']==51
 assert sum(r['canonical_promotion'] for r in rs)==s['source_records_added']==28
 assert sum(r['canonical_promotion'] and r['case_support_only'] for r in rs)==s['case_support_only']==9
 assert s['reusable_projection_method_records']==19
 held={r['projection_rule_id'] for r in rs if not r['canonical_promotion']}
 covered=[rid for g in d['source_coverage_gaps'] for rid in g['affected_record_ids']]
 assert len(covered)==len(set(covered))==s['held']==23 and set(covered)==held
 assert len(d['source_coverage_gaps'])==s['source_gap_count']==8
 assert s['durable_review_object_count']==51+5+1<=100
 assert all(b['count']<=50 for b in s['reasoning_sub_batches'])
 for r in rs:
  if r['gap_id']:
   assert r['canonical_condition'] is None and r['normalized_claim'] is None
   assert r['normalization_epistemic']=='UNRESOLVED' and not r['normalization_verified']
def test_anomalous_direction_and_glyphs_cannot_be_repaired_by_common_sense():
 rs=rows()
 for literal,gap in [('主兄弟各胞','L01'),('故以人合作事业为宜','L02'),('主受兄弟或合作伙伴支排差遣','L03')]:
  r=next(r for r in rs if r['literal_claim']==literal)
  assert r['gap_id'].endswith(gap) and not r['canonical_promotion']
 assert not any('不与' in r['literal_claim'] for r in rs if r['source_anchor']=='L13')
 power=next(r for r in rs if r['source_anchor']=='L04' and r['literal_claim']=='兄弟融洽')
 assert '权禄及吉曜' in power['condition'] and '魁钺' not in power['condition'] and power['gap_id'].endswith('C02')
def test_relative_three_year_window_is_not_a_decade_or_a_single_year():
 rs=rows();relative=[r for r in rs if r['gap_id'] and r['gap_id'].endswith('T02')]
 assert len(relative)==2
 for r in relative:
  assert '年份' in r['condition'] and '如见煞曜' in r['condition'] and '与友合作事业' in r['condition']
  assert r['time_layer'] is None and r['primary_time_layer'] is None
  assert r['source_time_layers']==['YEAR'] and '不出三年' in r['source_relative_time_expression']
  assert not r['canonical_promotion'] and not r['executable']
 assert any(r['literal_claim']=='则不出三年便干反目' for r in relative)
 trigger=next(r for r in rs if r['source_anchor']=='L07' and not r['gap_id'])
 assert trigger['time_layer']=='YEAR' and trigger['literal_claim']=='每易与友人合作事业'
 period=next(r for r in rs if r['gap_id'] and r['gap_id'].endswith('T01'))
 assert period['time_layer'] is None and period['source_time_layers']==[]
 assert all('DECADE' not in r['source_time_layers'] for r in rs)
def test_core_term_gap_preserves_unknown_subject_without_local_operator():
 d=load();g=next(g for g in d['source_coverage_gaps'] if g['core_gap'])
 assert g['gap_type']=='KNOWLEDGE_CORE_GAP' and g['source_palace']=='P02'
 assert g['unresolved_shared_term']=='冲起' and g['local_work_can_continue']
 assert g['current_shared_semantics_insufficient'] and g['human_gate_classification']
 assert g['normalized_term'] is None
 r=next(r for r in rows() if r['projection_rule_id'] in g['affected_record_ids'])
 assert '忌星冲起廉贞化忌之年' in r['condition']
 assert r['time_layer']=='YEAR' and not r['normalization_verified'] and not r['executable']
def test_star_transformation_subjects_advice_and_case_boundaries():
 rs=rows()
 l14=[r for r in rs if r['source_anchor']=='L14']
 assert all('贪狼化忌' in r['condition'] and '廉贞化忌' not in r['condition'] for r in l14)
 l15=next(r for r in rs if r['source_anchor']=='L15')
 assert '廉贞化忌，又见煞' in l15['condition']
 advice=next(r for r in rs if r['literal_claim']=='此时即应谋善处')
 assert advice['time_layer']=='NATAL' and advice['source_time_expression'] is None
 assert '不是克应' in advice['notes'] and advice['canonical_promotion']
 for r in rs:
  assert not r['executable'] and not r['canonical_mapping_approved'] and r['history_feedback']==0
  assert r['condition_encoding']=='SOURCE_NATIVE_TEXT_NOT_BOOLEAN_IR'
  if any(t in r['literal_claim'] for t in ('残疾者','暗恋','大祸','兄弟多','各胞','便干反目')):
   assert r['case_support_only']
 dark=next(r for r in rs if r['source_anchor']=='L12' and '暗恋' in r['literal_claim'])
 assert dark['cross_palace_dependency']==['命宫见红鸾天喜']
 assert all(k in dark['condition'] for k in ('咸池','大耗','天姚','沐浴','命宫见红鸾天喜'))
 assert not load()['whole_chapter_complete'] and '7 天府' in load()['next_source_anchor']

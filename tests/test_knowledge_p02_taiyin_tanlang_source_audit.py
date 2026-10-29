"""P02 #885 source, subject, time and continuation invariants."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'knowledge/palaces/P02_siblings/wp05/SIBLINGS_SB08_TAIYIN_TANLANG_SOURCE_AUDIT_v0.1.json'
def data():return json.loads(PATH.read_text())
def test_seven_old_ledgers_and_new_ids_are_byte_conserved():
 d=data();old=[]
 assert len(d['accepted_input_pins'])==7
 for p in d['accepted_input_pins']:
  raw=(ROOT/p['path']).read_bytes()
  assert hashlib.sha256(raw).hexdigest()==p['sha256'] and p['read_only']
  old+=json.loads(raw)['records']
 assert len(old)==294
 assert [r['projection_rule_id'] for r in d['records']]==[f'P02S-{i:03}' for i in range(295,332)]
 assert not {r['projection_rule_id'] for r in old}&{r['projection_rule_id'] for r in d['records']}
def test_counts_coverage_and_gap_membership():
 d=data();rs=d['records'];s=d['summary']
 assert {r['source_anchor'] for r in rs}=={f'{a}{i:02}' for a in ('Y','G') for i in range(1,7)}
 assert len(rs)==s['source_atoms_reviewed']==37
 assert sum(r['canonical_promotion'] for r in rs)==s['source_records_added']==23
 assert sum(r['canonical_promotion'] and r['case_support_only'] for r in rs)==s['case_support_only']==11
 assert s['reusable_projection_method_records']==12 and s['source_gap_count']==4
 held={r['projection_rule_id'] for r in rs if not r['canonical_promotion']}
 covered=[rid for g in d['source_coverage_gaps'] for rid in g['affected_record_ids']]
 assert len(covered)==len(set(covered))==s['held']==14 and set(covered)==held
 assert s['durable_review_object_count']==37+7+1<=100
 assert all(b['count']<=50 for b in s['reasoning_sub_batches'])
 for r in rs:
  if r['gap_id']:
   assert not r['normalization_verified'] and r['canonical_condition'] is None and r['normalized_claim'] is None
def test_day_night_temple_fall_and_solar_lunar_subjects_stay_separate():
 rs=data()['records']
 night=next(r for r in rs if r['literal_claim']=='最吉')
 assert '入庙，夜生人' in night['condition']
 fall=next(r for r in rs if r['literal_claim']=='始主兄弟和美')
 assert all(t in fall['condition'] for t in ('落陷','夜生人','见吉曜'))
 day=next(r for r in rs if r['literal_claim']=='亦不和美')
 assert '日生人' in day['condition'] and '入庙' in day['condition']
 anomaly=next(r for r in rs if r['gap_id'] and r['gap_id'].endswith('L01'))
 assert '太阳落陷' in anomaly['condition'] and '太阴落陷' not in anomaly['condition']
 lunar=next(r for r in rs if r['literal_claim']=='多主姊妹克应')
 solar=next(r for r in rs if r['literal_claim']=='则主兄弟克应')
 assert lunar['base_subject']=='太阴守兄弟宫' and solar['base_subject']=='太阳守兄弟宫（原书比较句）'
 assert lunar['case_support_only'] and solar['case_support_only']
def test_explicit_year_methods_and_unresolved_printed_words():
 rs=data()['records'];ys=[r for r in rs if r['source_anchor'] in ('Y06','G05')]
 assert len(ys)==6 and all(r['time_layer']=='YEAR' and r['source_time_layers']==['YEAR'] for r in ys)
 assert all('DECADE' not in r['source_time_layers'] for r in rs)
 glyph=next(r for r in rs if r['gap_id'] and r['gap_id'].endswith('L02'))
 assert '见寿' in glyph['condition'] and '见禄' not in glyph['condition'] and not glyph['canonical_promotion']
 typo=next(r for r in rs if r['gap_id'] and r['gap_id'].endswith('L03'))
 assert typo['literal_claim']=='其舍凶克应' and typo['time_layer']=='YEAR' and not typo['normalization_verified']
def test_exception_gender_case_and_both_pattern_antecedents():
 rs=data()['records'];byid={r['projection_rule_id']:r for r in rs}
 exception=next(r for r in rs if r['literal_claim']=='均主兄弟和睦')
 assert '除巳亥' in exception['condition'] and '一般情形下' in exception['condition']
 for r in rs:
  if r['source_anchor']=='Y05':
   assert r['case_support_only'] and '亥宫化忌' in r['condition'] and '男命' in r['condition']
 inherited=next(r for r in rs if r['source_anchor']=='G04' and r['literal_claim']=='亦然')
 assert len(inherited['source_antecedent_record_ids'])==2
 assert {byid[i]['literal_claim'] for i in inherited['source_antecedent_record_ids']}=={'生平多酒色之友','且因之受累'}
 assert all(byid[i]['case_support_only'] for i in inherited['source_antecedent_record_ids'])
def test_dual_transformations_opposition_and_runtime_boundary():
 d=data();rs=d['records']
 for r in rs:
  if r['source_anchor']=='G06' and r['case_support_only']:
   assert all(t in r['condition'] for t in ('武曲化忌','贪狼化忌','相照','若更见[铃昌陀武]'))
   assert '同度' not in r['condition']
  assert not r['canonical_mapping_approved'] and not r['executable'] and r['history_feedback']==0
  assert r['condition_encoding']=='SOURCE_NATIVE_TEXT_NOT_BOOLEAN_IR'
 assert not d['whole_chapter_complete'] and '10 巨门' in d['next_source_anchor']

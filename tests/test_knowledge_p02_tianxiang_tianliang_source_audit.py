"""P02 #893 source-gated exceptions, real-world premises and glyph preservation."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'knowledge/palaces/P02_siblings/wp05/SIBLINGS_SB10_TIANXIANG_TIANLIANG_SOURCE_AUDIT_v0.1.json'
def data():return json.loads(PATH.read_text())
def test_nine_old_ledgers_and_new_ids_are_byte_preserved():
 d=data();old=[]
 assert len(d['accepted_input_pins'])==9
 for p in d['accepted_input_pins']:
  raw=(ROOT/p['path']).read_bytes()
  assert hashlib.sha256(raw).hexdigest()==p['sha256'] and p['read_only']
  old+=json.loads(raw)['records']
 assert len(old)==349
 assert [r['projection_rule_id'] for r in d['records']]==[f'P02S-{i:03}' for i in range(350,391)]
 assert not {r['projection_rule_id'] for r in old}&{r['projection_rule_id'] for r in d['records']}
def test_source_counts_anchors_and_unique_gap_coverage():
 d=data();rs=d['records'];s=d['summary']
 assert {r['source_anchor'] for r in rs}=={f'S{i:02}' for i in range(1,6)}|{f'B{i:02}' for i in range(1,10)}
 assert len(rs)==s['source_atoms_reviewed']==41
 assert sum(r['canonical_promotion'] for r in rs)==s['source_records_added']==26
 assert sum(r['canonical_promotion'] and r['case_support_only'] for r in rs)==s['case_support_only']==4
 assert s['reusable_projection_method_records']==22 and s['source_gap_count']==6
 held={r['projection_rule_id'] for r in rs if not r['canonical_promotion']}
 covered=[rid for g in d['source_coverage_gaps'] for rid in g['affected_record_ids']]
 assert len(covered)==len(set(covered))==s['held']==15 and set(covered)==held
 assert s['durable_review_object_count']==41+9+1<=100
 assert all(b['count']<=50 for b in s['reasoning_sub_batches'])
 for r in rs:
  if r['gap_id']:
   assert r['canonical_condition'] is None and r['normalized_claim'] is None
   assert not r['normalization_verified'] and r['normalization_epistemic']=='UNRESOLVED'
def test_family_history_and_partner_actor_are_never_dropped():
 rs=data()['records'];twins=next(r for r in rs if r['literal_claim']=='主兄弟双胞')
 assert all(x in twins['condition'] for x in ('家族有双胞胎传统','无虚耗刑煞','昌曲','左右相夹','或同会'))
 assert twins['source_real_world_prerequisite']=='家族有双胞胎传统' and twins['case_support_only']
 cooperation=next(r for r in rs if '除非合作者完全退居幕后' in r['literal_claim'])
 assert '即使见吉曜' in cooperation['literal_claim'] and '作为自己的后台' in cooperation['literal_claim']
 assert cooperation['source_real_world_prerequisite'].startswith('合作者完全退居幕后')
 assert '合作人退居幕后，不是本人退居幕后' in cooperation['notes']
def test_glyphs_and_reference_subjects_fail_closed():
 rs=data()['records']
 for literal,gap in [('亦主有祀入之兄弟','L01'),('或主自身祀出','L01'),('则为各胞','L02')]:
  r=next(r for r in rs if r['literal_claim']==literal)
  assert r['gap_id'].endswith(gap) and r['case_support_only'] and not r['canonical_promotion']
 west=next(r for r in rs if '卯西' in r['condition'])
 fire=next(r for r in rs if '以火相' in r['condition'])
 assert all(r['gap_id'].endswith('L03') and r['time_layer']=='YEAR' for r in (west,fire))
 assert '卯酉' not in west['condition'] and '以天相' not in fire['condition']
 reference=next(r for r in rs if r['gap_id'] and r['gap_id'].endswith('C03'))
 assert '[夹印]之年' in reference['condition'] and reference['time_layer']=='YEAR'
 subjects=[r for r in rs if r['gap_id'] and r['gap_id'].endswith('C02')]
 assert len(subjects)==5 and all(not r['normalization_verified'] for r in subjects)
 intrigue=next(r for r in subjects if r['literal_claim']=='或有阴谋诡计')
 assert '化忌且见煞曜' in intrigue['condition'] and intrigue['case_support_only']
def test_tianyao_sun_and_scope_conditions_stay_complete():
 rs=data()['records']
 moral=next(r for r in rs if '深沉刁狡' in r['literal_claim'])
 assert moral['case_support_only'] and moral['canonical_promotion'] and '不狡' not in moral['literal_claim']
 lawsuit=next(r for r in rs if r['literal_claim']=='则主词讼纷争')
 assert all(x in lawsuit['condition'] for x in ('天姚同度','更见刑煞','太阳又落陷')) and lawsuit['case_support_only']
 scope=next(r for r in rs if r['condition']=='天梁见此星曜结构')
 assert scope['gap_id'].endswith('C01') and not scope['canonical_promotion']
def test_year_layers_and_source_only_runtime_boundary():
 d=data();rs=d['records'];ys=[r for r in rs if r['time_layer']=='YEAR']
 assert len(ys)==7 and all(r['source_time_layers']==['YEAR'] for r in ys)
 assert all('DECADE' not in r['source_time_layers'] for r in rs)
 assert {r['literal_claim'] for r in rs if r['source_anchor'] in ('B07','B08','B09') and r['time_layer']=='NATAL'}=={'子优于午','丑优于未','亥优于巳'}
 for r in rs:
  assert not r['canonical_mapping_approved'] and not r['executable'] and r['history_feedback']==0
  assert r['condition_encoding']=='SOURCE_NATIVE_TEXT_NOT_BOOLEAN_IR'
 assert not d['whole_chapter_complete'] and '13 七杀' in d['next_source_anchor']

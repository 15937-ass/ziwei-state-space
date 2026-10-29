"""P02 #887: preserve cross-page conditions, exceptions and source identities."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'knowledge/palaces/P02_siblings/wp05/SIBLINGS_SB09_JUMEN_SOURCE_AUDIT_v0.1.json'
def data():return json.loads(PATH.read_text())
def test_eight_old_ledgers_and_contiguous_new_ids_are_conserved():
 d=data();old=[]
 assert len(d['accepted_input_pins'])==8
 for p in d['accepted_input_pins']:
  raw=(ROOT/p['path']).read_bytes()
  assert hashlib.sha256(raw).hexdigest()==p['sha256'] and p['read_only']
  old+=json.loads(raw)['records']
 assert len(old)==331
 assert [r['projection_rule_id'] for r in d['records']]==[f'P02S-{i:03}' for i in range(332,350)]
 assert not {r['projection_rule_id'] for r in old}&{r['projection_rule_id'] for r in d['records']}
def test_complete_source_coverage_counts_and_gaps():
 d=data();rs=d['records'];s=d['summary']
 assert {r['source_anchor'] for r in rs}=={f'J{i:02}' for i in range(1,6)}
 assert len(rs)==s['source_atoms_reviewed']==18
 assert sum(r['canonical_promotion'] for r in rs)==s['source_records_added']==15
 assert sum(r['canonical_promotion'] and r['case_support_only'] for r in rs)==s['case_support_only']==6
 assert s['reusable_projection_method_records']==9 and s['source_gap_count']==1
 held={r['projection_rule_id'] for r in rs if not r['canonical_promotion']}
 covered=[rid for g in d['source_coverage_gaps'] for rid in g['affected_record_ids']]
 assert len(covered)==len(set(covered))==s['held']==3 and set(covered)==held
 assert s['durable_review_object_count']==18+8+2<=100
 assert all(b['count']<=50 for b in s['reasoning_sub_batches'])
def test_cross_page_qualification_keeps_all_scope_candidates_held():
 cross=[r for r in data()['records'] if r['source_anchor']=='J03']
 assert len(cross)==3
 for r in cross:
  assert (r['printed_page'],r['printed_page_end'],r['pdf_physical_page'],r['pdf_physical_page_end'])==(30,31,15,16)
  assert '以见煞忌刑曜者为确' in r['source_span']
  assert r['gap_id'].endswith('C01') and not r['canonical_promotion']
  assert r['canonical_condition'] is None and r['normalized_claim'] is None and not r['normalization_verified']
 assert any(r['literal_claim']=='或竟因此致祸' for r in cross)
def test_accomplishment_friendship_and_exception_chains_are_separate():
 rs=data()['records']
 success=next(r for r in rs if r['literal_claim']=='亦仅主兄弟有成')
 depth=next(r for r in rs if r['literal_claim']=='并不主兄弟感情深厚')
 assert success['condition']==depth['condition'] and '或见吉化' in success['condition']
 cooperation=next(r for r in rs if '绝不宜与人合作事业。唯' in r['literal_claim'])
 assert '[太阳巨门]' in cooperation['literal_claim'] and '可与异族人合作' in cooperation['literal_claim']
 assert cooperation['case_support_only']
 mutual=next(r for r in rs if '互相利用' in r['literal_claim'])
 assert '同宫或相对' in mutual['literal_claim'] and '太阳必须入庙' in mutual['literal_claim']
 assert '互利用不等合作事业' in mutual['notes'] and mutual['case_support_only']
 legal=next(r for r in rs if r['literal_claim']=='或致涉词讼、破耗')
 assert '并见' in legal['condition'] and legal['case_support_only']
def test_year_methods_and_case_only_runtime_boundary():
 d=data();rs=d['records'];ys=[r for r in rs if r['source_anchor']=='J04']
 assert len(ys)==3 and all(r['time_layer']=='YEAR' and r['source_time_layers']==['YEAR'] for r in ys)
 assert '[同梁]、天机、巨门' in ys[0]['condition']
 assert '巨门、天同、[机阴]' in ys[1]['condition']
 assert '天机、天梁' in ys[2]['condition']
 assert all('DECADE' not in r['source_time_layers'] for r in rs)
 for r in rs:
  assert not r['canonical_mapping_approved'] and not r['executable'] and r['history_feedback']==0
  assert r['condition_encoding']=='SOURCE_NATIVE_TEXT_NOT_BOOLEAN_IR'
  if '始善终恶' in r['literal_claim'] or '骨肉参商' in r['literal_claim']:
   assert r['case_support_only']
 assert not d['whole_chapter_complete'] and '11 天相' in d['next_source_anchor']

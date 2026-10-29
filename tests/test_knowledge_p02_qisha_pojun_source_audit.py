"""Source-boundary regressions for P02 #899, not empirical fortune validation."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'knowledge/palaces/P02_siblings/wp05/SIBLINGS_SB11_QISHA_POJUN_SOURCE_AUDIT_v0.1.json'
def data():return json.loads(PATH.read_text())
def test_accepted_ten_ledgers_are_unchanged_and_ids_are_disjoint():
 d=data();old=[]
 assert len(d['accepted_input_pins'])==10
 for p in d['accepted_input_pins']:
  raw=(ROOT/p['path']).read_bytes()
  assert hashlib.sha256(raw).hexdigest()==p['sha256'] and p['read_only']
  old+=json.loads(raw)['records']
 assert len(old)==390
 assert [r['projection_rule_id'] for r in d['records']]==[f'P02S-{i:03}' for i in range(391,425)]
 assert not {r['projection_rule_id'] for r in old}&{r['projection_rule_id'] for r in d['records']}
def test_complete_paragraphs_page_split_and_gap_census():
 d=data();rs=d['records'];s=d['summary'];ps=d['source_paragraphs']
 assert {p['anchor'] for p in ps}=={f'Q{i:02}' for i in range(1,6)}|{f'P{i:02}' for i in range(1,8)}
 assert len(ps)==12 and all(p['direct_visual_verified'] for p in ps)
 assert {r['source_anchor'] for r in rs}=={p['anchor'] for p in ps}
 for r in rs:
  p=next(p for p in ps if p['anchor']==r['source_anchor'])
  assert r['source_span']==p['literal_text']
  assert r['literal_claim'] in p['literal_text']
  assert r['printed_page']==r['printed_page_end']==(31 if r['source_anchor'] in ('Q01','Q02') else 32)
  assert r['pdf_physical_page']==r['pdf_physical_page_end']==16
 assert len(rs)==s['source_atoms_reviewed']==34
 assert sum(r['canonical_promotion'] for r in rs)==s['source_records_added']==24
 assert sum(r['case_support_only'] and r['canonical_promotion'] for r in rs)==s['case_support_only']==14
 assert s['reusable_projection_method_records']==10 and len(d['source_coverage_gaps'])==s['source_gap_count']==5
 held={r['projection_rule_id'] for r in rs if not r['canonical_promotion']}
 covered=[rid for g in d['source_coverage_gaps'] for rid in g['affected_record_ids']]
 assert len(covered)==len(set(covered))==s['held']==10 and set(covered)==held
 assert s['durable_review_object_count']==34+10+2+12<=100
 assert all(b['count']<=50 for b in s['reasoning_sub_batches'])
def test_qisha_cross_palace_and_conjunctive_premises_cannot_swap():
 rs=data()['records']
 cross=[r for r in rs if r['source_anchor']=='Q01' and r['canonical_promotion']]
 assert len(cross)==2 and all('命宫见辅弼' in r['condition'] and '七杀虽不会辅佐诸吉' in r['condition'] and r['cross_palace_dependency'] and r['case_support_only'] for r in cross)
 q3=[r for r in rs if r['source_anchor']=='Q03' and r['literal_claim']!='终身残疾者亦为刑克之应']
 assert all('兄弟宫有煞刑诸曜' in r['condition'] and '命宫又见辅弼诸吉' in r['condition'] for r in q3)
 sun=next(r for r in rs if r['literal_claim']=='命宫必有太阳相对')
 assert '不表示安星算法验证' in sun['notes'] and not sun['executable']
 method=next(r for r in rs if r['source_anchor']=='Q04' and r!=sun)
 assert '太阳庙陷' in method['condition'] and method['cross_palace_dependency']
def test_ambiguous_else_glyphs_and_fire_bell_operator_fail_closed():
 d=data();rs=d['records']
 for r in rs:
  if r['gap_id']:
   assert r['canonical_condition'] is None and r['normalized_claim'] is None
   assert not r['normalization_verified'] and r['normalization_epistemic']=='UNRESOLVED'
 assert {r['literal_claim'] for r in rs if r['gap_id'] and r['gap_id'].endswith('C02')}=={'兄弟自小分离','主一生分离异地'}
 glyphs=[r for r in rs if r['gap_id'] and r['gap_id'].endswith('L01')]
 assert len(glyphs)==2 and all('祀出' in r['literal_claim'] and '嗣出' not in r['literal_claim'] and r['case_support_only'] for r in glyphs)
 fire=[r for r in rs if r['gap_id'] and r['gap_id'].endswith('C04')]
 assert len(fire)==3 and all('火铃同度更见空劫' in r['condition'] for r in fire)
 g=d['knowledge_core_gaps'][0]
 assert g['type']=='KNOWLEDGE_CORE_GAP' and not g['blocks_this_source_batch'] and 'NOT_D3' in g['dependency_class']
 scope=[r for r in rs if r['gap_id'] and r['gap_id'].endswith('C03')]
 assert len(scope)==2 and all('此格局' in r['condition'] for r in scope)
def test_age_health_and_identity_are_case_only_and_process_is_not_income():
 rs=data()['records'];age=next(r for r in rs if r['source_anchor']=='P02')
 assert '除非孤单，否则' in age['condition'] and '八年至十二年以上不等' in age['literal_claim'] and age['case_support_only']
 assert age['numeric_expression_role']=='SOURCE_CASE_LITERAL_NOT_PROBABILITY_OR_CLOSED_INTERVAL'
 health=next(r for r in rs if r['literal_claim']=='终身残疾者亦为刑克之应')
 assert health['case_support_only'] and health['health_boundary']=='SOURCE_CASE_ONLY_NOT_DIAGNOSIS_OR_PROGNOSIS'
 eldest=next(r for r in rs if '独立负起长子或长女之责任' in r['literal_claim'])
 assert '禄存同度' in eldest['condition'] and eldest['case_support_only']
 process=next(r for r in rs if r['literal_claim']=='亦主开创而不主收成')
 assert not process['case_support_only'] and '过程限定' in process['notes'] and '与人合作' in process['condition']
 startup=next(r for r in rs if r['source_anchor']=='P04')
 assert '辅佐吉曜咸集' in startup['condition'] and '禄存同度时情形恰恰相反' in startup['literal_claim']
 assert '不定义独立布尔逆命题' in startup['source_exception_chain']
def test_all_six_timing_methods_keep_year_and_original_star_groups():
 rs=data()['records'];ys=[r for r in rs if r['time_layer']=='YEAR']
 assert len(ys)==6 and all(r['source_time_layers']==['YEAR'] for r in ys)
 assert {r['source_anchor'] for r in ys}=={'Q05','P05','P06','P07'}
 both=next(r for r in ys if '寅申七杀' in r['condition'])
 assert '除以[杀破狼]外，亦以[廉相]' in both['condition']
 expected={'P05':['破军','七杀','[廉相]'],'P06':['[武相]','破军','[廉府]'],'P07':['[紫相]','破军','七杀']}
 for a,names in expected.items():
  r=next(r for r in ys if r['source_anchor']==a)
  assert all(n in r['condition'] for n in names) and '兄弟宫' in r['condition']
def test_source_end_does_not_authorize_chapter_closure_or_runtime():
 d=data()
 assert not d['whole_chapter_complete'] and '独立全章' in d['next_source_anchor'] and '不启动P04' in d['next_source_anchor']
 assert d['execution_boundary']=={'history_feedback':0,'conditions_compiled':0,'execution_unlocked':0,'formal_mapping_approved':False,'product_runtime_authorized':False,'shared_core_semantics_changed':False}
 for r in d['records']:
  assert not r['canonical_mapping_approved'] and not r['executable'] and r['history_feedback']==0
  assert r['condition_encoding']=='SOURCE_NATIVE_TEXT_NOT_BOOLEAN_IR' and 'DECADE' not in r['source_time_layers']

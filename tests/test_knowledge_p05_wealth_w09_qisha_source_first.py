import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"knowledge/palaces/P05_wealth/w09"
STATE=ROOT/"knowledge/states/P05_WEALTH_STATE.yaml"
SOURCE=BASE/"WEALTH_W09_QISHA_SOURCE_READJUDICATION_P90_P91_v0.1.json"
TIME=BASE/"WEALTH_W09_QISHA_SOURCE_TIME_SCOPE_P90_P91_v0.1.json"
GAPS=BASE/"WEALTH_W09_QISHA_SOURCE_GAPS_P90_P91_v0.1.json"
SUMMARY=BASE/"WEALTH_W09_QISHA_CANONICAL_SUMMARY_P90_P91_v0.1.md"
PRIOR_GAPS={"W05-SG-002","W06-SG-001","W06-SG-002","W06-SG-003","W06-SG-004","W06-SG-005","W08-SG-001","W08-SG-002","W08-SG-003","W08-SG-004","W08-SG-005"}
def load(path): return json.loads(path.read_text(encoding="utf-8"))
def row(data,rid): return next(r for r in data["records"] if r["projection_rule_id"]==rid)
def test_source_hash_boundary_and_candidate_census():
 d=load(SOURCE); ids=[r["projection_rule_id"] for r in d["records"]]
 expected=[f"W09-{i}" for i in range(845,889)]+[f"W09-{i}" for i in range(901,905)]
 assert d["issue"]==765 and d["source_basis"]["sha256"]=="6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c"
 assert "90–91" in d["source_basis"]["printed_pages"] and "13 七杀" in d["source_basis"]["printed_pages"] and "14 破军" in d["source_basis"]["printed_pages"]
 assert ids==expected and len(ids)==len(set(ids))==48
 assert d["summary"]["historical_candidates_reviewed"]==44 and d["summary"]["new_source_atoms_reviewed"]==4
 assert d["summary"]["new_source_supported_atoms"]==3 and d["summary"]["canonical_promotions"]==44
 assert d["summary"]["cumulative_canonical_records_after_merge"]==765
 assert not any(r["projection_rule_id"] in {f"W09-{i}" for i in range(889,901)} for r in d["records"])
def test_uncertain_source_conditions_are_not_promoted():
 d=load(SOURCE); held={"W09-865","W09-881","W09-882","W09-904"}
 assert {r["projection_rule_id"] for r in d["records"] if not r["canonical_promotion"]}==held
 assert all(row(d,rid)["source_uncertainty"] for rid in held)
 assert "火铃遭到度" in row(d,"W09-865")["canonical_condition"]
 assert "谦贞化禄" in row(d,"W09-881")["canonical_condition"] and "谦贞化禄" in row(d,"W09-882")["canonical_condition"]
 assert "巳亥多" in row(d,"W09-904")["source_digest"] and d["summary"]["unresolved_candidate_ids"]==sorted(held)
def test_literal_anomalies_are_retained_and_clear_subclauses_are_scoped():
 d=load(SOURCE); g=load(GAPS)
 assert "主攻者亦有守势。主攻者亦有守势。" in row(d,"W09-847")["source_digest"] and "W09-SG-006" in row(d,"W09-847")["source_note"]
 assert "W09-SG-007" in row(d,"W09-848")["source_note"]
 assert "投机荷且" not in row(d,"W09-856")["source_digest"] and "W09-SG-008" in row(d,"W09-856")["source_note"]
 assert "则丰横发横破" in row(d,"W09-862")["source_digest"] and "W09-SG-010" in row(d,"W09-862")["source_note"]
 assert "W09-SG-009" in row(d,"W09-865")["source_note"] and "W09-SG-011" in row(d,"W09-879")["source_note"]
 assert "谦贞化禄" in row(d,"W09-881")["source_digest"] and "，’或常遭盗贼" in row(d,"W09-881")["source_digest"]
 assert "W09-SG-012" in row(d,"W09-881")["source_note"] and "W09-SG-013" in row(d,"W09-881")["source_note"]
 assert g["gap_count"]==9 and g["core_gap_count"]==0
 assert {x["gap_id"] for x in g["gaps"]}=={f"W09-SG-{i:03d}" for i in range(6,15)}
 assert all(x["status"]=="OPEN" and x["core_gap"] is False for x in g["gaps"])
 assert g["summary"]["unresolved_prior_gap_ids"]==sorted(PRIOR_GAPS)
def test_time_scope_does_not_invent_decade_or_year_triggers():
 t=load(TIME)
 assert t["counts"]=={"non_natal_rows":0,"year":0,"decade":0,"path_dependent_gate_rows":6,"source_time_phrase_rows":2,"source_life_course_qualifier_rows":3,"source_condition_qualifier_rows":0}
 assert t["exact_non_natal_ids"]==[] and t["decade_ids"]==[] and t["year_ids"]==[]
 assert t["path_dependent_gate_ids"]==["W09-852","W09-855","W09-871","W09-878","W09-886","W09-888"]
 assert [r["projection_rule_id"] for r in t["source_time_phrase_records"]]==["W09-885","W09-886"]
 assert [r["source_time_phrase"] for r in t["source_time_phrase_records"]]==["于运限吉时","但运限一过"]
 assert t["source_life_course_qualifier_ids"]==["W09-852","W09-877","W09-883"]
def test_prior_tianliang_and_tianxiang_artifacts_remain_immutable_and_counts_reconcile():
 b=ROOT/"knowledge/palaces/P05_wealth/w08"
 tl=load(b/"WEALTH_W08_TIANLIANG_SOURCE_READJUDICATION_P88_P90_v0.1.json")
 tx=load(b/"WEALTH_W08_TIANXIANG_SOURCE_READJUDICATION_P87_P88_v0.1.json"); d=load(SOURCE)
 assert tl["issue"]==760 and len(tl["records"])==38 and tl["summary"]["canonical_promotions"]==37
 assert tl["summary"]["cumulative_canonical_records_after_merge"]==721 and row(tl,"W08-820")["canonical_promotion"] is False
 assert tx["issue"]==746 and len(tx["records"])==45 and tx["summary"]["canonical_promotions"]==42 and tx["summary"]["cumulative_canonical_records_after_merge"]==684
 assert d["summary"]["cumulative_canonical_records_after_merge"]==721+d["summary"]["canonical_promotions"]
 assert "14 破军" in SUMMARY.read_text(encoding="utf-8")
def test_state_cache_tracks_active_qisha_and_inherited_gaps():
 s=STATE.read_text(encoding="utf-8")
 assert 'status: "ACTIVE"' in s and "active_issue: 770" in s
 assert 'active_branch: "knowledge/p05-770-source-first-pojun-p91-p92"' in s
 assert "active_pr: null" in s
 assert "merged_rule_count: 765" in s and "current_batch_rule_count: 29" in s and "source_first_records_added_current_batch: 30" in s
 assert "source_uncertainty_count_current_batch: 2" in s and "source_coverage_gap_count_current_batch: 2" in s
 assert "source_coverage_gaps_remaining: 22" in s and "path_dependent_gate_count_current_batch: 9" in s
 assert all(g in s for g in PRIOR_GAPS) and "13 七杀" in s and "14 破军" in s
 assert "No Product/runtime authorization is implied" in s

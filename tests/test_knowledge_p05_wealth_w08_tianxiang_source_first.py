import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"knowledge/palaces/P05_wealth/w08"
STATE=ROOT/"knowledge/states/P05_WEALTH_STATE.yaml"
SOURCE=BASE/"WEALTH_W08_TIANXIANG_SOURCE_READJUDICATION_P87_P88_v0.1.json"
TIME=BASE/"WEALTH_W08_TIANXIANG_SOURCE_TIME_SCOPE_P87_P88_v0.1.json"
GAPS=BASE/"WEALTH_W08_TIANXIANG_SOURCE_GAPS_P87_P88_v0.1.json"
SUMMARY=BASE/"WEALTH_W08_TIANXIANG_CANONICAL_SUMMARY_P87_P88_v0.1.md"
PRIOR={"W05-SG-002","W06-SG-001","W06-SG-002","W06-SG-003","W06-SG-004","W06-SG-005"}
def load(p): return json.loads(p.read_text(encoding="utf-8"))
def row(d,rid): return next(x for x in d["records"] if x["projection_rule_id"]==rid)
def test_candidate_census():
 d=load(SOURCE); rs=d["records"]
 assert d["issue"]==746 and d["source_basis"]["sha256"]=="6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c"
 assert "87–88" in d["source_basis"]["printed_pages"]
 assert "一四十以后始渐兴家" in d["source_basis"]["note"] and "丑来天相" in d["source_basis"]["note"]
 assert len(rs)==45 and [r["projection_rule_id"] for r in rs]==[f"W08-{i}" for i in range(743,788)]
 assert sum(r["canonical_promotion"] is True for r in rs)==42
 assert {r["projection_rule_id"] for r in rs if not r["canonical_promotion"]}=={"W08-761","W08-766","W08-767"}
 assert d["summary"]["cumulative_canonical_records_after_merge"]==684
def test_financial_seal_branches():
 d=load(SOURCE)
 assert "天府为财库" in row(d,"W08-743")["source_digest"] and "财印" in row(d,"W08-743")["source_digest"]
 assert "财荫夹印" in row(d,"W08-745")["canonical_condition"]
 assert "刑忌夹、火铃夹、空劫夹" in row(d,"W08-747")["canonical_condition"]
 assert "有煞同度又会煞" in row(d,"W08-747")["canonical_condition"] and "空劫同度会煞" in row(d,"W08-747")["canonical_condition"]
def test_temporal_scope_and_paths():
 d=load(SOURCE); t=load(TIME)
 assert t["counts"]=={"non_natal_rows":4,"year":2,"decade":2,"path_dependent_gate_rows":4,"source_age_qualifier_rows":1}
 assert t["exact_non_natal_ids"]==["W08-766","W08-767","W08-771","W08-772"]
 assert t["path_dependent_gate_ids"]==["W08-761","W08-763","W08-773","W08-777"]
 assert all(r["source_time_scope"]==["DECADE","YEAR"] for r in t["records"])
 assert "于此大限流年" in row(d,"W08-771")["source_digest"]
def test_ambiguities_and_prior_gaps():
 d=load(SOURCE); g=load(GAPS)
 for rid in ("W08-761","W08-766","W08-767"):
  assert row(d,rid)["canonical_promotion"] is False and row(d,rid)["source_uncertainty"]
 assert g["gap_count"]==2 and g["core_gap_count"]==0
 assert {x["gap_id"] for x in g["gaps"]}=={"W08-SG-001","W08-SG-002"}
 assert g["summary"]["unresolved_prior_gap_ids"]==sorted(PRIOR)
def test_state_and_handoff_counts():
 s=STATE.read_text(encoding="utf-8")
 assert 'status: "ACTIVE"' in s and "active_issue: 746" in s
 assert 'active_branch: "knowledge/p05-746-source-first-tianxiang-p87-p88-r3"' in s
 assert "merged_rule_count: 642" in s and "current_batch_rule_count: 42" in s
 assert "source_first_records_added_current_batch: 45" in s and "source_uncertainty_count_current_batch: 3" in s
 assert "source_coverage_gap_count_current_batch: 2" in s and "source_coverage_gaps_remaining: 8" in s
 assert "W05-SG-002 remains PARTIALLY_RESOLVED" in s and all(g in s for g in PRIOR)
 assert "12 天梁" in s and "Issue #746" in SUMMARY.read_text(encoding="utf-8")
def test_previous_jumen_artifact_is_immutable():
 j=load(BASE/"WEALTH_W08_SOURCE_READJUDICATION_P86_P87_v0.1.json")
 assert len(j["records"])==42 and j["summary"]["cumulative_canonical_records_after_merge"]==642

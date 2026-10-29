import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "validation/wp05/SP07_spouse_projection_review_601_700.csv"
READJ = ROOT / "knowledge/palaces/P03_spouse/wp05/SPOUSE_SP07_SOURCE_READJUDICATION_100_v0.1.json"
STATE = ROOT / "knowledge/states/P03_SPOUSE_STATE.yaml"
SOURCE_SHA = "6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c"
CANDIDATE_SHA = "7f2bc6ec32c5b5655d4266ccdb2914d019acc6b2"
HELD = {"SP07-631","SP07-632","SP07-633","SP07-637","SP07-638","SP07-639","SP07-644","SP07-645","SP07-646","SP07-647","SP07-672","SP07-673","SP07-674","SP07-675","SP07-680","SP07-681","SP07-682","SP07-688","SP07-689","SP07-690"}

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def candidate_rows():
    with CANDIDATE.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def dispositions_by_id(d):
    return {x["historical_candidate_id"]: x for x in d["candidate_batch"]["candidate_dispositions"]}

def records_by_id(d):
    return {x["projection_rule_id"]: x for x in d["records"]}

def test_exact_inventory_source_pin_and_physical_page_mapping():
    d=load(READJ); rows=candidate_rows()
    assert len(rows)==100
    assert [r["projection_rule_id"] for r in rows]==[f"SP07-{n}" for n in range(601,701)]
    assert d["candidate_batch"]["file"]=="validation/wp05/SP07_spouse_projection_review_601_700.csv"
    assert d["candidate_batch"]["sha"]==CANDIDATE_SHA and d["candidate_batch"]["rows"]==100
    assert d["source_basis"]["source_id"]=="SRC-ZZ-003" and d["source_basis"]["attachment_sha256"]==SOURCE_SHA
    assert d["source_basis"]["candidate_batch_verified_printed_pages"]==[45,46,47,48]
    assert d["source_basis"]["candidate_batch_verified_pdf_physical_pages"]==[23,24]
    assert d["source_basis"]["page_mapping"]["45"]==23 and d["source_basis"]["page_mapping"]["48"]==24
    assert "10 巨门" in d["source_basis"]["note"]
    assert d["historical_candidate_inventory"]["total_rows"]==836
    assert d["repair_reconciliation"]["historical_report_counts_reused"] is False

def test_candidate_accounting_and_source_record_counts_reconcile():
    d=load(READJ); disp=d["candidate_batch"]["candidate_dispositions"]; rec=d["records"]; s=d["summary"]
    assert len(disp)==100 and all(x["reason"] for x in disp)
    assert [x["historical_candidate_id"] for x in disp]==[r["projection_rule_id"] for r in candidate_rows()]
    assert (s["canonical_promoted"],s["held"],s["deduplicated"])==(78,20,2)
    assert s["canonical_promoted"]+s["held"]+s["deduplicated"]==100
    assert s["canonical_record_count"]==len(rec)==81
    assert s["reusable_projection_rules"]==53 and s["case_support_only"]==28
    assert sum(r["case_support_only"] is True for r in rec)==28
    assert sum(r["case_support_only"] is False for r in rec)==53
    assert s["source_resolution_change_count"]==sum(r["source_resolution_changed"] is True for r in rec)
    assert s["source_condition_normalization_count"]==sum(r["source_condition_normalized"] is True for r in rec)

def test_every_candidate_has_scan_evidence_and_valid_record_links():
    d=load(READJ); disp=d["candidate_batch"]["candidate_dispositions"]; rec=d["records"]; ids={r["projection_rule_id"] for r in rec}
    assert all(x["source_literal_claim"] and x["verified_source_location"] and x["verified_source_span_id"] for x in disp)
    assert all(r["source_literal_claim"] and r["source_note"] and r["source_location"] and r["source_span_id"] for r in rec)
    assert all(x["canonical_record_ids"]==[] for x in disp if x["direct_scan_disposition"].startswith("HOLD_"))
    assert all(len(x["canonical_record_ids"])==1 and x["canonical_record_ids"][0] in ids for x in disp if not x["direct_scan_disposition"].startswith("HOLD_"))
    assert {x["historical_candidate_id"] for x in disp if x["direct_scan_disposition"].startswith("HOLD_")}==HELD
    assert {x["historical_candidate_id"] for x in disp if x["direct_scan_disposition"]=="DEDUPLICATED"}=={"SP07-668","SP07-669"}
    assert {r["historical_candidate_id"] for r in rec if r["source_span_changed"]}=={"SP07-601","SP07-602","SP07-603","SP07-683","SP07-684","SP07-685","SP07-686","SP07-687"}
    dispositions = dispositions_by_id(d)
    assert dispositions["SP07-604"]["verified_source_location"]=="SRC-ZZ-003 printed pp45–46 / PDF physical p23"
    assert records_by_id(d)["P03S-604"]["source_span_id"]=="ZZ003-P45-P46"

def test_temporal_scope_fail_closed_and_or_branch_preserved():
    d=load(READJ); disp=dispositions_by_id(d); rec=records_by_id(d)
    assert {k for k,v in disp.items() if v["direct_scan_disposition"]=="HOLD_TEMPORAL_GRANULARITY_UNRESOLVED"}==HELD
    assert len(d["temporal_scope_residuals"])==53
    assert d["summary"]["temporal_scope_candidate_row_count"]==149
    assert len({x for g in d["temporal_scope_residuals"] for x in g["candidate_ids"]})==149
    assert "枢纽" in disp["SP07-631"]["source_literal_claim"] and "运限年限" in disp["SP07-644"]["source_literal_claim"]
    assert "OR 子分支" in disp["SP07-668"]["reason"]
    assert "大限夫妻宫见巨门或“同梁”守垣" in rec["P03S-667"]["canonical_condition"]

def test_corrections_case_only_and_no_history_feedback_leakage():
    d=load(READJ); rec=records_by_id(d)
    assert rec["P03S-607"]["canonical_projection_target"]=="small_issues_escalate"
    assert rec["P03S-613"]["case_support_only"] is True
    assert rec["P03S-616"]["canonical_projection_target"]=="traditional_spouse_absconding_case"
    assert rec["P03S-618"]["canonical_projection_target"]=="midcourse_separation"
    assert rec["P03S-620"]["case_support_only"] is True and rec["P03S-621"]["case_support_only"] is True
    assert rec["P03S-666"]["canonical_projection_target"]=="spousal_cooperation_required_if_business"
    assert rec["P03S-667"]["primary_time_layer"]=="DECADE"
    assert rec["P03S-670"]["case_support_only"] is True
    assert rec["P03S-695"]["archived_history_feedback"]=="ACQUIRED_DISPOSITION" and rec["P03S-695"]["history_feedback"] is None
    assert rec["P03S-699"]["archived_history_feedback"]=="PATH_DEPENDENT_GATE" and rec["P03S-699"]["history_feedback"] is None
    assert rec["P03S-699"]["source_sequence_not_history_gate"] is True
    assert d["summary"]["history_feedback"]==0
    assert all(r["history_feedback"] is None for r in d["records"] if r["historical_candidate_id"])

def test_supplements_gaps_and_execution_boundary():
    d=load(READJ); rec=records_by_id(d)
    assert {"P03S-SP07-SUP-001","P03S-SP07-SUP-002","P03S-SP07-SUP-003"}.issubset(rec)
    assert "若落陷、化忌、见煞" in rec["P03S-SP07-SUP-001"]["source_literal_claim"]
    assert "偏房继室" in rec["P03S-SP07-SUP-002"]["source_literal_claim"]
    assert "其他星曜见辅佐" in rec["P03S-SP07-SUP-003"]["source_literal_claim"]
    assert len(d["source_coverage_gaps"])==17 and d["summary"]["open_source_coverage_gap_count"]==4
    gaps={g["gap_id"]:g for g in d["source_coverage_gaps"] if g["gap_id"].startswith("P03-SP07-")}
    assert set(gaps)=={"P03-SP07-GAP-001","P03-SP07-GAP-002","P03-SP07-GAP-003"}
    assert all(g["status"].startswith("RESOLVED_BY_P03S-SP07-SUP-") for g in gaps.values())
    b=d["execution_boundary"]
    assert b["canonical_promotion_is_source_only"] is True and b["conditions_compiled"]==0 and b["execution_unlocked"]==0
    assert b["product_runtime_authorized"] is False and b["shared_core_semantics_changed"] is False and b["other_palace_changed"] is False and b["history_feedback"]==0

def test_cumulative_state_checkpoint_reconciles():
    d=load(READJ); state=STATE.read_text(encoding="utf-8")
    # The palace state is a moving cumulative checkpoint: later accepted batches
    # must not make an earlier batch's regression test require the stale SP07 snapshot.
    assert (
        "SP07_601_700_SOURCE_FIRST_REVIEW_COMPLETE" in state
        or "SP08_701_800_SOURCE_FIRST_REVIEW_COMPLETE" in state
        or "SP09_801_836_SOURCE_FIRST_REVIEW_COMPLETE" in state
    )
    minimums = {
        "historical_candidate_rows_reviewed": 700,
        "candidate_rows_promoted": 538,
        "source_records_added": 551,
        "reusable_projection_method_records_added": 397,
        "case_support_only_records_added": 154,
        "candidates_held": 157,
        "candidates_deduplicated": 5,
        "source_coverage_residuals_total_recorded": 17,
        "temporal_scope_residuals": 53,
        "temporal_scope_candidate_rows": 149,
    }
    for field, minimum in minimums.items():
        line = next(line for line in state.splitlines() if line.strip().startswith(field + ":"))
        actual = int(line.split(":", 1)[1].strip())
        assert actual >= minimum, (field, actual, minimum)
    assert "conditions_compiled=0" in state and "execution_unlocked=0" in state


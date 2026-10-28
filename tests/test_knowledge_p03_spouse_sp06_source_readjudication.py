import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "validation/wp05/SP06_spouse_projection_review_501_600.csv"
READJ = ROOT / "knowledge/palaces/P03_spouse/wp05/SPOUSE_SP06_SOURCE_READJUDICATION_100_v0.1.json"
STATE = ROOT / "knowledge/states/P03_SPOUSE_STATE.yaml"
SOURCE_SHA = "6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c"
CANDIDATE_SHA = "37f4539d8e1bc4b28dfe057756a28da71eabfbde"
TEMPORAL_HELD = {
    "SP06-520",
    "SP06-525", "SP06-526", "SP06-528", "SP06-529", "SP06-530",
    "SP06-540",
    "SP06-541", "SP06-542", "SP06-543", "SP06-544",
    "SP06-552", "SP06-553",
    "SP06-556", "SP06-557",
    "SP06-581", "SP06-582", "SP06-583", "SP06-584",
    "SP06-590", "SP06-591", "SP06-592",
    "SP06-600",
}
CONDITION_HELD = {"SP06-508", "SP06-509"}


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
    d = load(READJ)
    rows = candidate_rows()
    assert len(rows) == 100
    assert [r["projection_rule_id"] for r in rows] == [f"SP06-{n}" for n in range(501, 601)]
    assert d["candidate_batch"]["file"] == "validation/wp05/SP06_spouse_projection_review_501_600.csv"
    assert d["candidate_batch"]["sha"] == CANDIDATE_SHA
    assert d["candidate_batch"]["rows"] == 100
    assert d["source_basis"]["source_id"] == "SRC-ZZ-003"
    assert d["source_basis"]["attachment_sha256"] == SOURCE_SHA
    assert d["source_basis"]["candidate_batch_verified_printed_pages"] == [43, 44, 45]
    assert d["source_basis"]["candidate_batch_verified_pdf_physical_pages"] == [22, 23]
    assert d["source_basis"]["page_mapping"]["43"] == 22
    assert d["source_basis"]["page_mapping"]["44"] == 22
    assert d["source_basis"]["page_mapping"]["45"] == 23
    assert d["source_basis"]["note"].find("10 巨门") >= 0
    assert d["historical_candidate_inventory"]["total_rows"] == 836
    assert d["historical_candidate_inventory"]["unique_ids"] == 836
    assert d["repair_reconciliation"]["historical_report_counts_reused"] is False


def test_candidate_accounting_and_source_record_counts_reconcile():
    d = load(READJ)
    disp = d["candidate_batch"]["candidate_dispositions"]
    records = d["records"]
    s = d["summary"]
    assert len(disp) == 100
    assert [x["historical_candidate_id"] for x in disp] == [r["projection_rule_id"] for r in candidate_rows()]
    assert all(x["reason"] for x in disp)
    assert s["reviewed"] == 100
    assert s["canonical_promoted"] == 75
    assert s["held"] == 25
    assert s["deduplicated"] == 0
    assert s["canonical_promoted"] + s["held"] + s["deduplicated"] == s["reviewed"]
    assert s["canonical_record_count"] == len(records) == 78
    assert s["reusable_projection_rules"] == 46
    assert s["case_support_only"] == 32
    assert sum(r["case_support_only"] is True for r in records) == 32
    assert sum(r["case_support_only"] is False for r in records) == 46
    assert len({r["projection_rule_id"] for r in records}) == 78
    assert s["source_resolution_change_count"] == sum(r["source_resolution_changed"] is True for r in records)
    assert s["source_condition_normalization_count"] == sum(r["source_condition_normalized"] is True for r in records)


def test_every_candidate_has_direct_scan_evidence_and_valid_record_links():
    d = load(READJ)
    disp = d["candidate_batch"]["candidate_dispositions"]
    records = d["records"]
    record_ids = {r["projection_rule_id"] for r in records}
    assert all(x["source_literal_claim"] and x["verified_source_location"] and x["verified_source_span_id"] for x in disp)
    assert all(r["source_literal_claim"] and r["source_note"] and r["source_location"] and r["source_span_id"] for r in records)
    assert all(x["canonical_record_ids"] == [] for x in disp if x["direct_scan_disposition"].startswith("HOLD_"))
    assert all(len(x["canonical_record_ids"]) == 1 and x["canonical_record_ids"][0] in record_ids
               for x in disp if not x["direct_scan_disposition"].startswith("HOLD_"))
    assert {x["historical_candidate_id"] for x in disp if x["direct_scan_disposition"].startswith("HOLD_")} == TEMPORAL_HELD | CONDITION_HELD
    assert {r["historical_candidate_id"] for r in records if r["source_span_changed"]} == {"SP06-531", "SP06-532", "SP06-533", "SP06-534"}


def test_temporal_scope_and_condition_membership_fail_closed():
    d = load(READJ)
    disp = dispositions_by_id(d)
    assert {k for k, v in disp.items() if v["direct_scan_disposition"] == "HOLD_TEMPORAL_GRANULARITY_UNRESOLVED"} == TEMPORAL_HELD
    assert {k for k, v in disp.items() if v["direct_scan_disposition"] == "HOLD_SOURCE_SEMANTIC_AMBIGUITY"} == CONDITION_HELD
    assert "大限流年" in disp["SP06-520"]["source_literal_claim"]
    assert "大限流年" in disp["SP06-540"]["source_literal_claim"]
    assert "克应之期" in disp["SP06-525"]["source_literal_claim"]
    assert "吉凶之枢纽" in disp["SP06-528"]["source_literal_claim"]
    assert len(d["temporal_scope_residuals"]) == 47
    assert d["summary"]["temporal_scope_residual_count"] == 47
    assert d["summary"]["temporal_scope_candidate_row_count"] == 129
    assert len({candidate for residual in d["temporal_scope_residuals"] for candidate in residual["candidate_ids"]}) == 129
    assert "ANY" in disp["SP06-508"]["reason"] or "ALL/ANY" in disp["SP06-508"]["reason"]


def test_semantic_corrections_case_only_reclassification_and_source_locations():
    d = load(READJ)
    disp = dispositions_by_id(d)
    rec = records_by_id(d)
    assert rec["P03S-501"]["canonical_projection_target"] == "husband_benefits_from_wife_status"
    assert "现代已未必克应" in rec["P03S-502"]["source_literal_claim"]
    assert "行业为宜" in rec["P03S-507"]["canonical_condition"]
    assert "现代就业决策" in rec["P03S-507"]["source_condition_uncertainty"]
    assert rec["P03S-531"]["case_support_only"] is True
    assert "printed p43" in rec["P03S-531"]["source_location"]
    assert "printed p43" in rec["P03S-533"]["source_location"]
    assert rec["P03S-539"]["canonical_projection_target"] == "traditional_advice_avoid_early_marriage"
    assert rec["P03S-539"]["case_support_only"] is True
    assert rec["P03S-554"]["canonical_projection_target"] == "spouse_extramarital_relationship_claim"
    assert rec["P03S-559"]["case_support_only"] is True
    assert "见煞" in rec["P03S-559"]["canonical_condition"]
    assert rec["P03S-569"]["case_support_only"] is True
    assert rec["P03S-571"]["canonical_projection_target"] == "traditional_woman_extramarital_affair_case"
    assert rec["P03S-574"]["canonical_projection_target"] == "tianxing_kongyao_as_mitigating_condition_for_marital_turbulence"
    assert rec["P03S-578"]["case_support_only"] is True
    assert "泛水桃花" in rec["P03S-578"]["canonical_condition"]
    assert "年解、月解" in rec["P03S-580"]["canonical_condition"]
    assert "解神" not in rec["P03S-580"]["canonical_condition"]
    assert "贪狼又见煞" in rec["P03S-589"]["canonical_condition"]
    assert rec["P03S-595"]["case_support_only"] is True
    assert "不主离婚" in rec["P03S-595"]["source_literal_claim"]
    assert disp["SP06-600"]["canonical_record_ids"] == []


def test_supplemental_source_atoms_and_gap_reconciliation():
    d = load(READJ)
    rec = records_by_id(d)
    assert "P03S-SP06-SUP-001" in rec
    assert "P03S-SP06-SUP-002" in rec
    assert "P03S-SP06-SUP-003" in rec
    assert "配年长之妻" in rec["P03S-SP06-SUP-001"]["source_literal_claim"]
    assert "无闺房之乐" in rec["P03S-SP06-SUP-002"]["source_literal_claim"]
    assert "亦主迟婚" in rec["P03S-SP06-SUP-003"]["source_literal_claim"]
    assert len(d["source_coverage_gaps"]) == 14
    assert d["summary"]["source_coverage_gap_count"] == 14
    assert d["summary"]["open_source_coverage_gap_count"] == 4
    assert {x["gap_id"] for x in d["source_coverage_gaps"] if x["gap_id"].startswith("P03-SP06-")} == {
        "P03-SP06-GAP-001", "P03-SP06-GAP-002", "P03-SP06-GAP-003"
    }


def test_cumulative_state_and_execution_boundary_reconcile():
    d = load(READJ)
    boundary = d["execution_boundary"]
    state = STATE.read_text(encoding="utf-8")
    assert "SOURCE_FIRST_REVIEW_COMPLETE" in state
    state_values = {}
    for field in ("historical_candidate_rows_reviewed", "candidate_rows_promoted", "source_records_added", "reusable_projection_method_records_added", "case_support_only_records_added", "candidates_held", "candidates_deduplicated", "temporal_scope_residuals", "temporal_scope_candidate_rows", "source_coverage_residuals_total_recorded"):
        line = next(line for line in state.splitlines() if line.strip().startswith(f"{field}:"))
        state_values[field] = int(line.split(":", 1)[1].strip())
    assert state_values["historical_candidate_rows_reviewed"] >= 600
    assert state_values["candidate_rows_promoted"] >= 460
    assert state_values["source_records_added"] >= 470
    assert state_values["reusable_projection_method_records_added"] >= 344
    assert state_values["case_support_only_records_added"] >= 126
    assert state_values["candidates_held"] >= 137
    assert state_values["candidates_deduplicated"] >= 3
    assert state_values["temporal_scope_residuals"] >= 47
    assert state_values["temporal_scope_candidate_rows"] >= 129
    assert state_values["source_coverage_residuals_total_recorded"] >= 14
    assert "conditions_compiled=0" in state
    assert "execution_unlocked=0" in state
    assert boundary["canonical_promotion_is_source_only"] is True
    assert boundary["conditions_compiled"] == 0
    assert boundary["execution_unlocked"] == 0
    assert boundary["product_runtime_authorized"] is False
    assert boundary["shared_core_semantics_changed"] is False
    assert boundary["other_palace_changed"] is False
    assert boundary["history_feedback"] == 0

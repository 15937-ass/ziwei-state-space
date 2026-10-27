import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "validation/wp05/SP04_spouse_projection_review_301_400.csv"
READJ = ROOT / "knowledge/palaces/P03_spouse/wp05/SPOUSE_SP04_SOURCE_READJUDICATION_100_v0.1.json"
STATE = ROOT / "knowledge/states/P03_SPOUSE_STATE.yaml"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def rows():
    with CANDIDATE.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def by_id():
    return {r["historical_candidate_id"]: r for r in load(READJ)["candidate_batch"]["candidate_dispositions"]}


def records_by_id():
    return {r["projection_rule_id"]: r for r in load(READJ)["records"]}


def test_exact_inventory_source_pin_and_page_mapping():
    d = load(READJ)
    rs = rows()
    assert len(rs) == 100
    assert len({r["projection_rule_id"] for r in rs}) == 100
    assert rs[0]["projection_rule_id"] == "SP04-301"
    assert rs[-1]["projection_rule_id"] == "SP04-400"
    assert d["candidate_batch"]["rows"] == 100
    assert d["candidate_batch"]["sha"] == "d3b3afb1c795e9c9eda98fb91bbcdf303835593c"
    assert d["source_basis"]["source_id"] == "SRC-ZZ-003"
    assert d["source_basis"]["attachment_sha256"] == "6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c"
    assert d["source_basis"]["candidate_batch_verified_printed_pages"] == [39, 40, 41]
    assert d["source_basis"]["candidate_batch_verified_pdf_physical_pages"] == [20, 21]
    assert d["source_basis"]["page_mapping"]["39"] == 20
    assert d["source_basis"]["page_mapping"]["40"] == 20
    assert d["source_basis"]["page_mapping"]["41"] == 21
    assert d["historical_candidate_inventory"]["total_rows"] == 836
    assert d["historical_candidate_inventory"]["unique_ids"] == 836
    assert d["repair_reconciliation"]["historical_report_counts_reused"] is False


def test_all_candidate_dispositions_and_counts_reconcile():
    d = load(READJ)
    rs = rows()
    disp = d["candidate_batch"]["candidate_dispositions"]
    assert len(disp) == 100
    assert [x["historical_candidate_id"] for x in disp] == [x["projection_rule_id"] for x in rs]
    assert all(x["reason"] for x in disp)
    s = d["summary"]
    records = d["records"]
    assert s["reviewed"] == 100
    assert s["canonical_promoted"] == 68
    assert s["held"] == 32
    assert s["deduplicated"] == 0
    assert s["canonical_promoted"] + s["held"] + s["deduplicated"] == s["reviewed"]
    assert s["canonical_record_count"] == len(records) == 68
    assert s["reusable_projection_rules"] == 47
    assert s["case_support_only"] == 21
    assert sum(r["case_support_only"] is True for r in records) == 21
    assert sum(r["case_support_only"] is False for r in records) == 47
    assert len({r["projection_rule_id"] for r in records}) == 68
    assert s["source_resolution_change_count"] == sum(r["source_resolution_changed"] is True for r in records)
    held = {k for k, v in by_id().items() if v["direct_scan_disposition"] == "HOLD_TEMPORAL_GRANULARITY_UNRESOLVED"}
    assert held == {f"SP04-{n}" for n in [311,312,313,314,325,326,327,328,344,345,346,352,353,361,362,369,370,371,372,374,375,376,377,381,382,383,388,394,395,396,397,399]}
    known = set(records_by_id())
    for item in disp:
        if item["direct_scan_disposition"].startswith("HOLD_"):
            assert item["canonical_record_ids"] == []
        else:
            assert item["canonical_record_ids"]
            assert set(item["canonical_record_ids"]).issubset(known)


def test_temporal_layers_fail_closed_and_source_branches_preserved():
    d = load(READJ)
    rec = records_by_id()
    disp = by_id()
    residual_ids = {candidate for residual in d["temporal_scope_residuals"] for candidate in residual["candidate_ids"]}
    held = {k for k, v in disp.items() if v["direct_scan_disposition"].startswith("HOLD_")}
    assert held.issubset(residual_ids)
    assert len(d["temporal_scope_residuals"]) == 27
    assert d["summary"]["temporal_scope_candidate_row_count"] == 72
    assert "年限运限" in d["temporal_scope_residuals"][-1]["source_expression"]
    assert "克勤克俭应之期" in d["temporal_scope_residuals"][-1]["source_expression"]
    assert "贪狼火星或铃星" in rec["P03S-306"]["source_literal_claim"]
    assert "男命" in rec["P03S-322"]["canonical_condition"]
    assert "女命" in rec["P03S-323"]["canonical_condition"]
    assert "见化忌或化禄" in rec["P03S-347"]["canonical_condition"]
    assert "或" in rec["P03S-366"]["canonical_condition"]
    assert "OR" in rec["P03S-360"]["canonical_projection_target"]
    assert "OR" in rec["P03S-379"]["canonical_projection_target"]
    assert "或" in rec["P03S-393"]["canonical_condition"]
    assert "年限运限" in disp["SP04-399"]["reason"]
    assert rec["P03S-355"]["source_condition_membership_status"] == "SOURCE_COMPOUND_MEMBERSHIP_UNSPECIFIED"
    assert rec["P03S-367"]["source_condition_membership_status"] == "SOURCE_COMPOUND_MEMBERSHIP_UNSPECIFIED"
    assert rec["P03S-358"]["source_condition_membership_status"] == "SOURCE_LITERAL_ANOMALY_PRESERVED"
    assert "不擅自替换为“则主”" in rec["P03S-358"]["source_condition_uncertainty"]


def test_source_gaps_execution_boundary_and_state_reconcile():
    d = load(READJ)
    boundary = d["execution_boundary"]
    assert len(d["source_coverage_gaps"]) == 9
    assert d["summary"]["source_coverage_gap_count"] == 9
    assert d["summary"]["open_source_coverage_gap_count"] == 4
    assert boundary["canonical_promotion_is_source_only"] is True
    assert boundary["conditions_compiled"] == 0
    assert boundary["execution_unlocked"] == 0
    assert boundary["product_runtime_authorized"] is False
    assert boundary["shared_core_semantics_changed"] is False
    assert boundary["other_palace_changed"] is False
    assert boundary["history_feedback"] == 0
    state = STATE.read_text(encoding="utf-8")
    # The SP04 ledger remains batch-specific, but the shared state cache advances
    # as later accepted batches are merged. Do not freeze this regression test
    # at the SP04 cumulative checkpoint.
    assert "SOURCE_FIRST_REVIEW_COMPLETE" in state
    state_values = {}
    for field in (
        "historical_candidate_rows_reviewed",
        "candidate_rows_promoted",
        "source_records_added",
        "reusable_projection_method_records_added",
        "case_support_only_records_added",
        "candidates_held",
        "candidates_deduplicated",
        "source_coverage_residuals_total_recorded",
        "temporal_scope_residuals",
        "temporal_scope_candidate_rows",
    ):
        line = next(line for line in state.splitlines() if line.strip().startswith(f"{field}:"))
        state_values[field] = int(line.split(":", 1)[1].strip())
    assert state_values["historical_candidate_rows_reviewed"] >= 400
    assert state_values["candidate_rows_promoted"] >= 321
    assert state_values["source_records_added"] >= 326
    assert state_values["reusable_projection_method_records_added"] >= 252
    assert state_values["case_support_only_records_added"] >= 74
    assert state_values["candidates_held"] >= 77
    assert state_values["candidates_deduplicated"] >= 2
    assert state_values["source_coverage_residuals_total_recorded"] >= 9
    assert state_values["temporal_scope_residuals"] >= 27
    assert state_values["temporal_scope_candidate_rows"] >= 72
    assert "conditions_compiled=0" in state
    assert "execution_unlocked=0" in state

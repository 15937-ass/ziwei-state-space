import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "validation/wp05/SP05_spouse_projection_review_401_500.csv"
READJ = ROOT / "knowledge/palaces/P03_spouse/wp05/SPOUSE_SP05_SOURCE_READJUDICATION_100_v0.1.json"
STATE = ROOT / "knowledge/states/P03_SPOUSE_STATE.yaml"
SOURCE_SHA = "6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c"
CANDIDATE_SHA = "c47e7fd5757c5eea1fbe67f85b67f31958666acd"
TEMPORAL_HELD = {
    "SP05-405", "SP05-406", "SP05-407", "SP05-408", "SP05-409", "SP05-410",
    "SP05-418", "SP05-419", "SP05-420", "SP05-421", "SP05-422",
    "SP05-430", "SP05-431", "SP05-432", "SP05-433",
    "SP05-441", "SP05-442", "SP05-443", "SP05-444",
    "SP05-455", "SP05-456", "SP05-457", "SP05-458",
    "SP05-472", "SP05-473", "SP05-474", "SP05-475", "SP05-476",
    "SP05-485", "SP05-486", "SP05-487",
    "SP05-497", "SP05-498", "SP05-499",
}


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
    assert [r["projection_rule_id"] for r in rows] == [f"SP05-{n}" for n in range(401, 501)]
    assert d["candidate_batch"]["file"] == "validation/wp05/SP05_spouse_projection_review_401_500.csv"
    assert d["candidate_batch"]["sha"] == CANDIDATE_SHA
    assert d["candidate_batch"]["rows"] == 100
    assert d["source_basis"]["source_id"] == "SRC-ZZ-003"
    assert d["source_basis"]["attachment_sha256"] == SOURCE_SHA
    assert d["source_basis"]["candidate_batch_verified_printed_pages"] == [41, 42, 43]
    assert d["source_basis"]["candidate_batch_verified_pdf_physical_pages"] == [21, 22]
    assert d["source_basis"]["page_mapping"]["41"] == 21
    assert d["source_basis"]["page_mapping"]["42"] == 21
    assert d["source_basis"]["page_mapping"]["43"] == 22
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
    assert s["canonical_promoted"] == 64
    assert s["held"] == 35
    assert s["deduplicated"] == 1
    assert s["canonical_promoted"] + s["held"] + s["deduplicated"] == s["reviewed"]
    assert s["canonical_record_count"] == len(records) == 66
    assert s["reusable_projection_rules"] == 46
    assert s["case_support_only"] == 20
    assert sum(r["case_support_only"] is True for r in records) == 20
    assert sum(r["case_support_only"] is False for r in records) == 46
    assert len({r["projection_rule_id"] for r in records}) == 66
    assert s["source_resolution_change_count"] == sum(r["source_resolution_changed"] is True for r in records)
    assert s["source_condition_normalization_count"] == sum(r["source_condition_normalized"] is True for r in records)


def test_temporal_hold_set_and_fail_closed_behavior():
    d = load(READJ)
    disp = dispositions_by_id(d)
    held_temporal = {k for k, v in disp.items() if v["direct_scan_disposition"] == "HOLD_TEMPORAL_GRANULARITY_UNRESOLVED"}
    assert held_temporal == TEMPORAL_HELD
    assert all(disp[k]["canonical_record_ids"] == [] for k in held_temporal)
    assert "再婚克应之期" in disp["SP05-405"]["source_literal_claim"]
    residual_ids = {candidate for residual in d["temporal_scope_residuals"] for candidate in residual["candidate_ids"]}
    assert held_temporal.issubset(residual_ids)
    assert len(d["temporal_scope_residuals"]) == 37
    assert d["summary"]["temporal_scope_candidate_row_count"] == 106
    assert d["summary"]["temporal_scope_residual_count"] == 37
    assert "运限年限" in next(x["source_expression"] for x in d["temporal_scope_residuals"] if "SP05-497" in x["candidate_ids"])


def test_semantic_corrections_and_ambiguities_are_preserved():
    d = load(READJ)
    disp = dispositions_by_id(d)
    rec = records_by_id(d)
    assert disp["SP05-465"]["direct_scan_disposition"] == "HOLD_SOURCE_SEMANTIC_AMBIGUITY"
    assert disp["SP05-465"]["canonical_record_ids"] == []
    assert "唯府库『空露』则减其不利程度" in disp["SP05-465"]["source_literal_claim"]
    assert disp["SP05-500"]["direct_scan_disposition"] == "DEDUPLICATED_SOURCE_OVERLAP"
    assert disp["SP05-500"]["canonical_record_ids"] == ["P03S-464"]
    assert "printed p42" in disp["SP05-500"]["verified_source_location"]
    assert rec["P03S-459"]["canonical_projection_target"] == "not_prone_to_separation_or_bereavement"
    assert "不主生离，不主死别" in rec["P03S-459"]["source_literal_claim"]
    assert "辅佐单星" in rec["P03S-450"]["canonical_condition"]
    assert rec["P03S-450"]["case_support_only"] is True
    assert "借星安宫" in rec["P03S-451"]["source_literal_claim"]
    assert rec["P03S-448"]["canonical_projection_target"] == "nominal_union_OR_surface_harmony_with_hidden_distance"
    assert rec["P03S-494"]["canonical_projection_target"] == "self_generated_worry"
    assert "或" in rec["P03S-436"]["canonical_condition"]
    assert rec["P03S-477"]["source_condition_membership_status"] == "SOURCE_COMPOUND_MEMBERSHIP_UNSPECIFIED"
    assert "否定作用域" in rec["P03S-477"]["source_condition_uncertainty"]
    assert "printed p42" in rec["P03S-464"]["source_location"]


def test_supplemental_source_atoms_and_gap_reconciliation():
    d = load(READJ)
    rec = records_by_id(d)
    assert "P03S-SP05-SUP-001" in rec
    assert "P03S-SP05-SUP-002" in rec
    assert "煞忌刑曜始为不良" in rec["P03S-SP05-SUP-001"]["source_literal_claim"]
    assert "煞忌刑曜始为不良" not in rec["P03S-461"]["source_literal_claim"]
    assert "男命宜配年少之妻" in rec["P03S-SP05-SUP-002"]["source_literal_claim"]
    assert len(d["source_coverage_gaps"]) == 11
    assert d["summary"]["source_coverage_gap_count"] == 11
    assert d["summary"]["open_source_coverage_gap_count"] == 4
    assert {x["gap_id"] for x in d["source_coverage_gaps"] if x["gap_id"].startswith("P03-SP05-")} == {"P03-SP05-GAP-001", "P03-SP05-GAP-002"}


def test_cumulative_state_and_execution_boundary_reconcile():
    d = load(READJ)
    boundary = d["execution_boundary"]
    state = STATE.read_text(encoding="utf-8")
    # This ledger remains batch-specific, but the shared P03 state advances as
    # later accepted batches merge. Assert that its cumulative checkpoint is
    # at least as advanced as the SP05 handoff rather than freezing old counts.
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
        "temporal_scope_residuals",
        "temporal_scope_candidate_rows",
        "source_coverage_residuals_total_recorded",
    ):
        line = next(line for line in state.splitlines() if line.strip().startswith(f"{field}:"))
        state_values[field] = int(line.split(":", 1)[1].strip())
    assert state_values["historical_candidate_rows_reviewed"] >= 500
    assert state_values["candidate_rows_promoted"] >= 385
    assert state_values["source_records_added"] >= 392
    assert state_values["reusable_projection_method_records_added"] >= 298
    assert state_values["case_support_only_records_added"] >= 94
    assert state_values["candidates_held"] >= 112
    assert state_values["candidates_deduplicated"] >= 3
    assert state_values["temporal_scope_residuals"] >= 37
    assert state_values["temporal_scope_candidate_rows"] >= 106
    assert state_values["source_coverage_residuals_total_recorded"] >= 11
    assert "conditions_compiled=0" in state
    assert "execution_unlocked=0" in state
    assert boundary["canonical_promotion_is_source_only"] is True
    assert boundary["conditions_compiled"] == 0
    assert boundary["execution_unlocked"] == 0
    assert boundary["product_runtime_authorized"] is False
    assert boundary["shared_core_semantics_changed"] is False
    assert boundary["other_palace_changed"] is False
    assert boundary["history_feedback"] == 0

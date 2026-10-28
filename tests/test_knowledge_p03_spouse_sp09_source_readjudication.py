import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "validation/wp05/SP09_spouse_projection_final_tail.csv"
READJ = ROOT / "knowledge/palaces/P03_spouse/wp05/SPOUSE_SP09_SOURCE_READJUDICATION_36_v0.1.json"
STATE = ROOT / "knowledge/states/P03_SPOUSE_STATE.yaml"
SOURCE_SHA = "6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c"
CANDIDATE_SHA = "49c5803131eadc5f887a7d2ab476a900f5cb341f"
HELD = {"SP09-816", "SP09-817", "SP09-818", "SP09-824", "SP09-825"}
CASE_ONLY = {
    "P03S-802", "P03S-803", "P03S-806", "P03S-807",
    "P03S-808", "P03S-810", "P03S-811", "P03S-812",
    "P03S-815", "P03S-819", "P03S-820", "P03S-821",
    "P03S-827", "P03S-830", "P03S-832", "P03S-833",
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


def test_exact_inventory_source_pin_and_page_mapping():
    d = load(READJ)
    rows = candidate_rows()
    assert len(rows) == 36
    assert [r["projection_rule_id"] for r in rows] == [f"SP09-{n}" for n in range(801, 837)]
    assert d["candidate_batch"]["file"] == "validation/wp05/SP09_spouse_projection_final_tail.csv"
    assert d["candidate_batch"]["sha"] == CANDIDATE_SHA
    assert d["candidate_batch"]["rows"] == 36
    assert d["source_basis"]["source_id"] == "SRC-ZZ-003"
    assert d["source_basis"]["attachment_sha256"] == SOURCE_SHA
    assert d["source_basis"]["candidate_batch_verified_printed_pages"] == [50, 51]
    assert d["source_basis"]["candidate_batch_verified_pdf_physical_pages"] == [25, 26]
    assert d["source_basis"]["page_mapping"]["50"] == 25
    assert d["source_basis"]["page_mapping"]["51"] == 26
    assert "子女宫" in d["source_basis"]["boundary_note"]
    assert d["historical_candidate_inventory"]["total_rows"] == 836
    assert d["repair_reconciliation"]["historical_report_counts_reused"] is False


def test_candidate_accounting_and_record_counts_reconcile():
    d = load(READJ)
    disp = d["candidate_batch"]["candidate_dispositions"]
    rec = d["records"]
    s = d["summary"]
    assert len(disp) == 36
    assert len(rec) == 34
    assert (s["canonical_promoted"], s["held"], s["deduplicated"]) == (31, 5, 0)
    assert s["canonical_promoted"] + s["held"] + s["deduplicated"] == 36
    assert s["canonical_record_count"] == len(rec) == 34
    assert s["reusable_projection_rules"] == 18
    assert s["case_support_only"] == 16
    assert {r["projection_rule_id"] for r in rec if r["case_support_only"]} == CASE_ONLY
    assert sum(r["case_support_only"] is False for r in rec) == 18
    assert s["source_resolution_change_count"] == 34
    assert s["source_condition_normalization_count"] == 34


def test_every_candidate_has_scan_evidence_and_valid_record_links():
    d = load(READJ)
    disp = d["candidate_batch"]["candidate_dispositions"]
    rec = d["records"]
    record_ids = {r["projection_rule_id"] for r in rec}
    assert [x["historical_candidate_id"] for x in disp] == [r["projection_rule_id"] for r in candidate_rows()]
    assert all(x["source_literal_claim"] and x["verified_source_location"] and x["verified_source_span_id"] and x["reason"] for x in disp)
    assert all(r["source_literal_claim"] and r["source_note"] and r["source_location"] and r["source_span_id"] for r in rec)
    assert all(x["canonical_record_ids"] == [] for x in disp if x["historical_candidate_id"] in HELD)
    assert all(x["direct_scan_disposition"] == "HOLD_TEMPORAL_GRANULARITY_UNRESOLVED" for x in disp if x["historical_candidate_id"] in HELD)
    assert all(x["canonical_record_ids"] and set(x["canonical_record_ids"]).issubset(record_ids) for x in disp if x["historical_candidate_id"] not in HELD)
    assert len(record_ids) == len(rec)


def test_direct_scan_corrects_cross_page_locations():
    d = load(READJ)
    disp = dispositions_by_id(d)
    rec = d["records"]
    changed = {r["historical_candidate_id"] for r in rec if r["source_span_changed"]}
    assert changed == {"SP09-812", "SP09-813", "SP09-814"}
    assert disp["SP09-812"]["verified_source_location"] == "SRC-ZZ-003 printed pp50–51 / PDF physical pp25–26"
    assert disp["SP09-813"]["verified_source_location"] == "SRC-ZZ-003 printed p50 / PDF physical p25"
    assert disp["SP09-814"]["verified_source_location"] == "SRC-ZZ-003 printed p50 / PDF physical p25"
    assert disp["SP09-815"]["verified_source_location"] == "SRC-ZZ-003 printed pp50–51 / PDF physical pp25–26"
    assert records_by_id(d)["P03S-815"]["source_span_changed"] is False


def test_ambiguous_source_phrase_is_preserved_not_silently_normalized():
    d = load(READJ)
    r = records_by_id(d)["P03S-812"]
    assert "外向之克或灾病" in r["source_literal_claim"]
    assert "外向之克" in r["source_condition_uncertainty"]
    assert r["canonical_projection_target"] == "traditional_spouse_illness_or_affliction_case"
    assert r["canonical_projection_target"] != "spouse_outward_attention"
    assert r["case_support_only"] is True


def test_historical_path_dependent_gate_is_reclassified_as_source_sequence():
    d = load(READJ)
    r = records_by_id(d)["P03S-821"]
    assert r["archived_history_feedback"] == "PATH_DEPENDENT_GATE"
    assert r["history_feedback"] is None
    assert r["path_dependent_gate_reclassified"] is True
    assert r["source_sequence_not_history_gate"] is True
    assert d["summary"]["history_feedback"] == 0
    assert d["summary"]["path_dependent_gate_ids"] == []
    assert all(x["history_feedback"] is None for x in d["records"])


def test_temporal_scope_holds_and_explicit_decade_year_split():
    d = load(READJ)
    held = {x["historical_candidate_id"] for x in d["candidate_batch"]["candidate_dispositions"] if x["direct_scan_disposition"] == "HOLD_TEMPORAL_GRANULARITY_UNRESOLVED"}
    assert held == HELD
    assert d["summary"]["temporal_scope_residual_count"] == 63
    assert d["summary"]["temporal_scope_candidate_row_count"] == 175
    residuals = {tuple(x["candidate_ids"]): x for x in d["temporal_scope_residuals"]}
    assert ("SP09-816", "SP09-817", "SP09-818") in residuals
    assert ("SP09-824", "SP09-825") in residuals
    assert all("未指定" in residuals[ids]["reason"] for ids in [("SP09-816", "SP09-817", "SP09-818"), ("SP09-824", "SP09-825")])
    for n in (834, 835, 836):
        group = [r for r in d["records"] if r["historical_candidate_id"] == f"SP09-{n}"]
        assert {r["primary_time_layer"] for r in group} == {"DECADE", "YEAR"}
        assert {r["source_time_expression"] for r in group} == {"大运", "流年"}
        assert all(r["projection_mode"] == "TIMING_TRIGGER" for r in group)
        assert all(r["case_support_only"] is False for r in group)


def test_cumulative_checkpoint_and_execution_boundary():
    d = load(READJ)
    state = STATE.read_text(encoding="utf-8")
    assert "SP09_801_836_SOURCE_FIRST_REVIEW_COMPLETE" in state
    for field, value in {
        "historical_candidate_rows_reviewed": 836,
        "candidate_rows_promoted": 648,
        "source_records_added": 664,
        "reusable_projection_method_records_added": 462,
        "case_support_only_records_added": 202,
        "candidates_held": 183,
        "candidates_deduplicated": 5,
        "source_coverage_residuals_total_recorded": 17,
        "temporal_scope_residuals: 63": None,
    }.items():
        if value is None:
            assert field in state
        else:
            assert f"{field}: {value}" in state
    assert "temporal_scope_candidate_rows: 175" in state
    assert "next_source_anchor:" in state and "residual handoff" in state
    b = d["execution_boundary"]
    assert b["canonical_promotion_is_source_only"] is True
    assert b["conditions_compiled"] == 0 and b["execution_unlocked"] == 0
    assert b["product_runtime_authorized"] is False
    assert b["shared_semantics_core_changed"] is False
    assert b["other_palace_changed"] is False
    assert b["history_feedback"] == 0
    assert d["summary"]["source_coverage_gap_count"] == 17
    assert d["summary"]["open_source_coverage_gap_count"] == 4

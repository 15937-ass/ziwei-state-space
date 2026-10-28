import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "validation/wp05/SP08_spouse_projection_review_701_800.csv"
READJ = ROOT / "knowledge/palaces/P03_spouse/wp05/SPOUSE_SP08_SOURCE_READJUDICATION_100_v0.1.json"
STATE = ROOT / "knowledge/states/P03_SPOUSE_STATE.yaml"
SOURCE_SHA = "6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c"
CANDIDATE_SHA = "0561598eeae0dca29934ceff8fd6a9e6e487317c"
HELD = {
    "SP08-701", "SP08-706",
    "SP08-720", "SP08-721", "SP08-722",
    "SP08-731", "SP08-732", "SP08-733",
    "SP08-741", "SP08-742", "SP08-743",
    "SP08-768", "SP08-769", "SP08-770",
    "SP08-775", "SP08-776", "SP08-777", "SP08-778",
    "SP08-787", "SP08-788", "SP08-789",
}
CASE_ONLY = {
    "P03S-703", "P03S-709", "P03S-716", "P03S-725", "P03S-727",
    "P03S-734", "P03S-737", "P03S-745", "P03S-747", "P03S-750",
    "P03S-751", "P03S-752", "P03S-753", "P03S-754", "P03S-755",
    "P03S-756", "P03S-757", "P03S-758", "P03S-761", "P03S-762",
    "P03S-763", "P03S-764", "P03S-767", "P03S-771", "P03S-772",
    "P03S-774", "P03S-782", "P03S-783", "P03S-785", "P03S-786",
    "P03S-794", "P03S-796",
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
    assert [r["projection_rule_id"] for r in rows] == [f"SP08-{n}" for n in range(701, 801)]
    assert d["candidate_batch"]["file"] == "validation/wp05/SP08_spouse_projection_review_701_800.csv"
    assert d["candidate_batch"]["sha"] == CANDIDATE_SHA and d["candidate_batch"]["rows"] == 100
    assert d["source_basis"]["source_id"] == "SRC-ZZ-003"
    assert d["source_basis"]["attachment_sha256"] == SOURCE_SHA
    assert d["source_basis"]["candidate_batch_verified_printed_pages"] == [48, 49, 50]
    assert d["source_basis"]["candidate_batch_verified_pdf_physical_pages"] == [24, 25]
    assert d["source_basis"]["page_mapping"]["48"] == 24
    assert d["source_basis"]["page_mapping"]["49"] == 25
    assert d["source_basis"]["page_mapping"]["50"] == 25
    assert "六运流年" in d["source_basis"]["note"]
    assert "SP09-801" in d["source_basis"]["boundary_note"]
    assert d["historical_candidate_inventory"]["total_rows"] == 836
    assert d["repair_reconciliation"]["historical_report_counts_reused"] is False

def test_candidate_accounting_and_source_record_counts_reconcile():
    d = load(READJ)
    disp = d["candidate_batch"]["candidate_dispositions"]
    rec = d["records"]
    s = d["summary"]
    assert len(disp) == 100 and all(x["reason"] for x in disp)
    assert [x["historical_candidate_id"] for x in disp] == [r["projection_rule_id"] for r in candidate_rows()]
    assert (s["canonical_promoted"], s["held"], s["deduplicated"]) == (79, 21, 0)
    assert s["canonical_promoted"] + s["held"] + s["deduplicated"] == 100
    assert s["canonical_record_count"] == len(rec) == 79
    assert s["reusable_projection_rules"] == 47 and s["case_support_only"] == 32
    assert {r["projection_rule_id"] for r in rec if r["case_support_only"]} == CASE_ONLY
    assert sum(r["case_support_only"] is False for r in rec) == 47
    assert s["source_resolution_change_count"] == sum(r["source_resolution_changed"] is True for r in rec)
    assert s["source_condition_normalization_count"] == sum(r["source_condition_normalized"] is True for r in rec)

def test_every_candidate_has_direct_scan_evidence_and_valid_record_links():
    d = load(READJ)
    disp = d["candidate_batch"]["candidate_dispositions"]
    rec = d["records"]
    ids = {r["projection_rule_id"] for r in rec}
    assert all(x["source_literal_claim"] and x["verified_source_location"] and x["verified_source_span_id"] for x in disp)
    assert all(r["source_literal_claim"] and r["source_note"] and r["source_location"] and r["source_span_id"] for r in rec)
    assert all(x["canonical_record_ids"] == [] for x in disp if x["direct_scan_disposition"].startswith("HOLD_"))
    assert all(len(x["canonical_record_ids"]) == 1 and x["canonical_record_ids"][0] in ids
               for x in disp if not x["direct_scan_disposition"].startswith("HOLD_"))
    assert {x["historical_candidate_id"] for x in disp
            if x["direct_scan_disposition"].startswith("HOLD_")} == HELD
    assert not any(x["direct_scan_disposition"] == "DEDUPLICATED" for x in disp)
    by_id = dispositions_by_id(d)
    assert by_id["SP08-723"]["verified_source_location"] == "SRC-ZZ-003 printed p48 / PDF physical p24"
    assert records_by_id(d)["P03S-723"]["source_span_id"] == "ZZ003-P48"
    assert by_id["SP08-727"]["verified_source_location"] == "SRC-ZZ-003 printed pp48–49 / PDF physical pp24–25"
    assert records_by_id(d)["P03S-727"]["source_span_id"] == "ZZ003-P48-P49"
    assert by_id["SP08-765"]["verified_source_location"] == "SRC-ZZ-003 printed p49 / PDF physical p25"
    assert records_by_id(d)["P03S-765"]["source_span_id"] == "ZZ003-P49"
    assert by_id["SP08-800"]["source_literal_claim"].endswith("见煞即易分离。")
    assert {r["historical_candidate_id"] for r in rec if r["source_span_changed"]} == {
        "SP08-723", "SP08-724", "SP08-725", "SP08-726",
        "SP08-765", "SP08-766", "SP08-767",
    }
    assert by_id["SP08-707"]["source_literal_claim"].startswith("夫妻宫住酉")
    assert records_by_id(d)["P03S-707"]["canonical_condition"].startswith("夫妻宫住酉")
    assert "回除天马外" in by_id["SP08-702"]["source_literal_claim"]

def test_temporal_scope_fails_closed_without_guessing_or_compiling():
    d = load(READJ)
    disp = dispositions_by_id(d)
    held = {k for k, v in disp.items() if v["direct_scan_disposition"] == "HOLD_TEMPORAL_GRANULARITY_UNRESOLVED"}
    assert held == HELD
    assert len(d["temporal_scope_residuals"]) == 61
    assert d["summary"]["temporal_scope_candidate_row_count"] == 170
    residual_ids = {x for group in d["temporal_scope_residuals"] for x in group["candidate_ids"]}
    assert len(residual_ids) == 170
    assert "吉限" in disp["SP08-701"]["source_literal_claim"]
    assert "火运" in disp["SP08-706"]["source_literal_claim"]
    assert "六运流年" in disp["SP08-741"]["source_literal_claim"]
    assert "大运或流年" in disp["SP08-775"]["source_literal_claim"]
    assert "枢纽" in disp["SP08-787"]["source_literal_claim"]
    assert d["execution_boundary"]["conditions_compiled"] == 0
    assert d["execution_boundary"]["execution_unlocked"] == 0

def test_case_only_classification_and_no_history_feedback_leakage():
    d = load(READJ)
    rec = records_by_id(d)
    assert rec["P03S-709"]["case_support_only"] is True
    assert rec["P03S-725"]["case_support_only"] is True
    assert rec["P03S-758"]["case_support_only"] is True
    assert rec["P03S-782"]["case_support_only"] is True
    assert rec["P03S-796"]["case_support_only"] is True
    assert rec["P03S-710"]["archived_history_feedback"] == "PATH_DEPENDENT_GATE"
    assert rec["P03S-710"]["history_feedback"] is None
    assert rec["P03S-710"]["source_sequence_not_history_gate"] is True
    assert rec["P03S-786"]["archived_history_feedback"] == "PATH_DEPENDENT_GATE"
    assert rec["P03S-786"]["history_feedback"] is None
    assert rec["P03S-786"]["source_sequence_not_history_gate"] is True
    assert rec["P03S-793"]["archived_history_feedback"] == "PATH_DEPENDENT_GATE"
    assert rec["P03S-793"]["history_feedback"] is None
    assert rec["P03S-793"]["source_sequence_not_history_gate"] is True
    assert d["summary"]["history_feedback"] == 0
    assert d["summary"]["path_dependent_gate_ids"] == []
    assert all(r["history_feedback"] is None for r in d["records"])

def test_gaps_and_execution_boundary_are_preserved():
    d = load(READJ)
    assert len(d["source_coverage_gaps"]) == 17
    assert d["summary"]["source_coverage_gap_count"] == 17
    assert d["summary"]["open_source_coverage_gap_count"] == 4
    assert d["repair_reconciliation"]["source_gap_ids_added"] == []
    assert any(g["gap_id"] == "P03-SP01-GAP-001" for g in d["source_coverage_gaps"])
    b = d["execution_boundary"]
    assert b["canonical_promotion_is_source_only"] is True
    assert b["product_runtime_authorized"] is False
    assert b["shared_core_semantics_changed"] is False
    assert b["other_palace_changed"] is False
    assert b["history_feedback"] == 0
    assert b["no_new_primitives_or_quantitative_claims"] is True

def test_cumulative_state_checkpoint_reconciles():
    state = STATE.read_text(encoding="utf-8")
    # The shared palace state is a moving cumulative checkpoint. Batch-specific
    # assertions above remain pinned to SP08; cumulative totals must reconcile
    # across all accepted source-review ledgers plus the current SP09 candidate.
    assert any(marker in state for marker in (
        "SP08_701_800_SOURCE_FIRST_REVIEW_COMPLETE",
        "SP09_801_836_SOURCE_FIRST_REVIEW_COMPLETE",
    ))
    batches = [load(path) for path in sorted(READJ.parent.glob(
        "SPOUSE_SP*_SOURCE_READJUDICATION_*.json"
    ))]
    assert batches
    candidates = [
        row["historical_candidate_id"]
        for batch in batches
        for row in batch["candidate_batch"]["candidate_dispositions"]
    ]
    assert len(candidates) == len(set(candidates)) == 836
    fields = {
        "historical_candidate_rows_reviewed": "reviewed",
        "candidate_rows_promoted": "canonical_promoted",
        "source_records_added": "canonical_record_count",
        "reusable_projection_method_records_added": "reusable_projection_rules",
        "case_support_only_records_added": "case_support_only",
        "candidates_held": "held",
        "candidates_deduplicated": "deduplicated",
    }
    state_lines = set(state.splitlines())
    for field, summary_key in fields.items():
        total = sum(batch["summary"][summary_key] for batch in batches)
        assert f"  {field}: {total}" in state_lines
    assert len(candidates) == sum(batch["summary"]["reviewed"] for batch in batches)
    minimums = {
        "source_coverage_residuals_total_recorded": 17,
        "temporal_scope_residuals": 61,
        "temporal_scope_candidate_rows": 170,
    }
    for field, minimum in minimums.items():
        line = next(line for line in state.splitlines() if line.strip().startswith(field + ":"))
        actual = int(line.split(":", 1)[1].strip())
        assert actual >= minimum, (field, actual, minimum)
    assert "conditions_compiled=0" in state and "execution_unlocked=0" in state

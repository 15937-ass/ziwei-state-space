import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "validation/wp05/SP01_spouse_projection_review_001_100.csv"
READJ = ROOT / "knowledge/palaces/P03_spouse/wp05/SPOUSE_SP01_SOURCE_READJUDICATION_100_v0.1.json"
STATE = ROOT / "knowledge/states/P03_SPOUSE_STATE.yaml"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def candidate_rows():
    with CANDIDATE.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def by_candidate():
    return {r["historical_candidate_id"]: r for r in load(READJ)["candidate_batch"]["candidate_dispositions"]}


def records_by_id():
    return {r["projection_rule_id"]: r for r in load(READJ)["records"]}


def test_p03_historical_index_and_source_boundary_are_explicit():
    d = load(READJ)
    rows = candidate_rows()
    inv = d["historical_candidate_inventory"]
    assert len(rows) == 100
    assert len({r["projection_rule_id"] for r in rows}) == 100
    assert rows[0]["projection_rule_id"] == "SP01-001"
    assert rows[-1]["projection_rule_id"] == "SP01-100"
    assert inv["total_rows"] == inv["unique_ids"] == 836
    assert inv["first_id"] == "SP01-001"
    assert inv["last_id"] == "SP09-836"
    assert inv["case_support_only_flagged_total"] == 136
    assert inv["path_dependent_gate_flagged_total"] == 6
    assert all(f["role"] == "READ_ONLY_ACCELERATION_INPUT_NOT_CANONICAL" for f in inv["files"])
    src = d["source_basis"]
    assert src["source_id"] == "SRC-ZZ-003"
    assert src["attachment_sha256"] == "6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c"
    assert src["full_section_printed_pages"] == list(range(33, 52))
    assert src["full_section_pdf_physical_pages"] == list(range(17, 27))
    assert src["page_mapping"]["33"] == src["page_mapping"]["34"] == 17
    assert src["page_mapping"]["35"] == 18
    assert src["page_mapping"]["51"] == 26
    assert len(d["source_section_inventory"]) == 19


def test_exactly_100_candidate_dispositions_and_counts_reconcile():
    d = load(READJ)
    disp = d["candidate_batch"]["candidate_dispositions"]
    rows = candidate_rows()
    ids = [r["historical_candidate_id"] for r in disp]
    assert len(disp) == 100
    assert ids == [r["projection_rule_id"] for r in rows]
    assert all(r["reason"] for r in disp)
    s = d["summary"]
    records = d["records"]
    assert s["reviewed"] == 100
    assert s["canonical_promoted"] == 89
    assert s["canonical_record_count"] == len(records) == 90
    assert len({r["projection_rule_id"] for r in records}) == 90
    assert s["reusable_projection_rules"] == 75
    assert s["case_support_only"] == 15
    assert s["held"] == 9
    assert s["deduplicated"] == 2
    assert all(r["canonical_promotion"] is True for r in records)
    assert sum(r["case_support_only"] is True for r in records) == 15
    assert sum(r["case_support_only"] is False for r in records) == 75
    known = set(r["projection_rule_id"] for r in records)
    for row in disp:
        assert set(row["canonical_record_ids"]).issubset(known)
        if row["direct_scan_disposition"].startswith("HOLD_"):
            assert row["canonical_record_ids"] == []


def test_known_source_mismatches_are_held_corrected_or_deduplicated():
    d = load(READJ)
    disp = by_candidate()
    rec = records_by_id()
    expected_holds = {
        "SP01-023", "SP01-027", "SP01-034", "SP01-091", "SP01-092",
        "SP01-095", "SP01-096", "SP01-097", "SP01-098",
    }
    assert {k for k, v in disp.items() if v["direct_scan_disposition"].startswith("HOLD_")} == expected_holds
    assert disp["SP01-028"]["direct_scan_disposition"] == "DEDUPLICATE_SHARED_PREREQUISITE"
    assert disp["SP01-089"]["direct_scan_disposition"] == "DEDUPLICATE_TO_BROADER_SOURCE_CLAIM"
    assert disp["SP01-028"]["canonical_record_ids"] == ["P03S-029", "P03S-030", "P03S-031"]
    assert disp["SP01-089"]["canonical_record_ids"] == ["P03S-088"]
    assert "本质安定" in rec["P03S-019"]["canonical_condition"]
    assert "大运" in rec["P03S-029"]["canonical_condition"]
    assert "卯酉紫贪" in rec["P03S-057"]["canonical_condition"]
    assert rec["P03S-088"]["canonical_projection_target"] == "post_separation_partner_dissatisfaction"
    assert rec["P03S-054-DECADE"]["primary_time_layer"] == "DECADE"
    assert rec["P03S-054-YEAR"]["primary_time_layer"] == "YEAR"
    assert rec["P03S-025"]["case_support_only"] is True
    assert rec["P03S-053"]["case_support_only"] is True


def test_source_coverage_gaps_and_temporal_residuals_remain_explicit():
    d = load(READJ)
    gaps = d["source_coverage_gaps"]
    assert {g["gap_id"] for g in gaps} == {
        "P03-SP01-GAP-001", "P03-SP01-GAP-002",
        "P03-SP01-GAP-003", "P03-SP01-GAP-004",
    }
    assert all(g["status"] == "CARRIED_FORWARD" for g in gaps)
    claim_text = " ".join(g["source_literal_claim"] for g in gaps)
    for phrase in ["此等宫垣，见煞忌空劫，则更为生变之兆", "见煞忌亦主离异", "禄权科会", "巨门化忌", "丑未天机独坐"]:
        assert phrase in claim_text
    residuals = d["temporal_scope_residuals"]
    assert len(residuals) == 2
    assert {tuple(r["candidate_ids"]) for r in residuals} == {
        ("SP01-091", "SP01-092"), ("SP01-097", "SP01-098")
    }
    assert d["execution_boundary"]["conditions_compiled"] == 0
    assert d["execution_boundary"]["execution_unlocked"] == 0
    assert d["execution_boundary"]["product_runtime_authorized"] is False
    assert d["execution_boundary"]["shared_core_semantics_changed"] is False
    assert d["summary"]["history_feedback"] == 0
    for key in ["new_primitive_qi", "new_memory_type", "new_independent_time_scale",
                "new_shared_group_semantics", "numeric_weight", "probability", "decay",
                "product_runtime_change"]:
        assert d["summary"][key] == 0


def test_p03_state_cache_reconciles_all_source_review_batches():
    # Batch-specific source assertions above remain pinned to SP01. The shared
    # state advances as later batches arrive; reconcile it with every ledger
    # instead of requiring it to remain frozen at the first checkpoint.
    state = STATE.read_text(encoding="utf-8")
    assert 'status: "ACTIVE_NO_ACTIVE_WORK"' in state
    assert "active_issue: null" in state
    assert "active_branch: null" in state
    assert "active_pr: null" in state
    batches = [load(path) for path in sorted(READJ.parent.glob(
        "SPOUSE_SP*_SOURCE_READJUDICATION_*.json"
    ))]
    assert batches
    candidates = [row["historical_candidate_id"] for batch in batches
                  for row in batch["candidate_batch"]["candidate_dispositions"]]
    assert len(candidates) == len(set(candidates))
    fields = {
        "historical_candidate_rows_reviewed": "reviewed",
        "candidate_rows_promoted": "canonical_promoted",
        "source_records_added": "canonical_record_count",
        "reusable_projection_method_records_added": "reusable_projection_rules",
        "case_support_only_records_added": "case_support_only",
        "candidates_held": "held",
        "candidates_deduplicated": "deduplicated",
    }
    lines = set(state.splitlines())
    for field, summary_key in fields.items():
        total = sum(batch["summary"][summary_key] for batch in batches)
        assert f"  {field}: {total}" in lines
    assert len(candidates) == sum(batch["summary"]["reviewed"] for batch in batches)
    assert "P03-SP01-GAP-001" in state
    assert "conditions_compiled=0" in state
    assert "execution_unlocked=0" in state

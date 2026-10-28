import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "validation/wp05/SP03_spouse_projection_review_201_300.csv"
READJ = ROOT / "knowledge/palaces/P03_spouse/wp05/SPOUSE_SP03_SOURCE_READJUDICATION_100_v0.1.json"
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


def test_exact_inventory_source_pin_and_page_mapping():
    d = load(READJ)
    rows = candidate_rows()
    assert len(rows) == 100
    assert len({r["projection_rule_id"] for r in rows}) == 100
    assert rows[0]["projection_rule_id"] == "SP03-201"
    assert rows[-1]["projection_rule_id"] == "SP03-300"
    assert [r["historical_candidate_id"] for r in d["candidate_batch"]["candidate_dispositions"]] == [r["projection_rule_id"] for r in rows]
    assert d["candidate_batch"]["rows"] == 100
    assert d["candidate_batch"]["sha"] == "f28a3df5f4006f5a1069896514f565f9af8f86a0"
    src = d["source_basis"]
    assert src["source_id"] == "SRC-ZZ-003"
    assert src["attachment_sha256"] == "6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c"
    assert src["candidate_batch_verified_printed_pages"] == [37, 38, 39]
    assert src["candidate_batch_verified_pdf_physical_pages"] == [19, 20]
    assert src["page_mapping"]["37"] == 19
    assert src["page_mapping"]["38"] == 19
    assert src["page_mapping"]["39"] == 20
    assert d["historical_candidate_inventory"]["total_rows"] == 836
    assert d["historical_candidate_inventory"]["unique_ids"] == 836
    assert d["repair_reconciliation"]["historical_report_counts_reused"] is False


def test_all_candidate_dispositions_and_counts_reconcile():
    d = load(READJ)
    rows = candidate_rows()
    disp = d["candidate_batch"]["candidate_dispositions"]
    assert len(disp) == 100
    assert all(r["reason"] for r in disp)
    s = d["summary"]
    records = d["records"]
    assert s["reviewed"] == 100
    assert s["canonical_promoted"] == 87
    assert s["held"] == 13
    assert s["deduplicated"] == 0
    assert s["canonical_promoted"] + s["held"] + s["deduplicated"] == s["reviewed"]
    assert s["canonical_record_count"] == len(records) == 91
    assert len({r["projection_rule_id"] for r in records}) == 91
    assert s["reusable_projection_rules"] == 70
    assert s["case_support_only"] == 21
    assert sum(r["case_support_only"] is True for r in records) == 21
    assert sum(r["case_support_only"] is False for r in records) == 70
    expected_held = {
        "SP03-211", "SP03-212", "SP03-213",
        "SP03-224", "SP03-225", "SP03-226",
        "SP03-258", "SP03-259", "SP03-260", "SP03-261",
        "SP03-280", "SP03-281", "SP03-282",
    }
    actual_held = {k for k, v in by_candidate().items() if v["direct_scan_disposition"] == "HOLD_TEMPORAL_GRANULARITY_UNRESOLVED"}
    assert actual_held == expected_held
    known = set(r["projection_rule_id"] for r in records)
    for row in disp:
        if row["direct_scan_disposition"].startswith("HOLD_"):
            assert row["canonical_record_ids"] == []
        else:
            assert row["canonical_record_ids"]
            assert set(row["canonical_record_ids"]).issubset(known)
    assert len([r for r in records if r["historical_candidate_id"] is not None]) == 87
    assert {r["projection_rule_id"] for r in records if r["case_support_only"]} == set(s["case_support_only_ids"])


def test_temporal_layers_fail_closed_and_source_conditions_preserved():
    d = load(READJ)
    disp = by_candidate()
    rec = records_by_id()
    residual_ids = {candidate for residual in d["temporal_scope_residuals"] for candidate in residual["candidate_ids"]}
    held = {k for k, v in disp.items() if v["direct_scan_disposition"].startswith("HOLD_")}
    assert held == {f"SP03-{n}" for n in [211,212,213,224,225,226,258,259,260,261,280,281,282]}
    assert held.issubset(residual_ids)
    assert len(d["temporal_scope_residuals"]) == 16
    assert d["summary"]["temporal_scope_candidate_row_count"] == 40
    assert "流年大运" in d["temporal_scope_residuals"][-4]["source_expression"]
    assert "否则多是非" in rec["P03S-202"]["canonical_condition"]
    assert "或旧侣重逢" in rec["P03S-207"]["canonical_condition"]
    assert "婚前波折" in rec["P03S-209"]["canonical_condition"]
    assert "不主异族通婚" in rec["P03S-217"]["canonical_condition"]
    assert "武曲化禄" in rec["P03S-250"]["canonical_condition"]
    assert "男命" in rec["P03S-250"]["canonical_condition"]
    assert "或" in rec["P03S-275"]["canonical_condition"]
    assert rec["P03S-284"]["projection_mode"] == "CROSS_PALACE_CONSTRAINT"
    assert "太阳" in rec["P03S-284"]["canonical_condition"] and "太阴" in rec["P03S-284"]["canonical_condition"]
    assert rec["P03S-285"]["source_literal_claim"].count("或因配偶遭逢意外") == 1
    assert rec["P03S-300"]["case_support_only"] is True
    assert "肺病" in rec["P03S-300"]["source_literal_claim"]
    assert "现代临床预测" in rec["P03S-300"]["case_support_reason"]


def test_prior_source_gaps_reconciled_without_guessing():
    d = load(READJ)
    gaps = {g["gap_id"]: g for g in d["source_coverage_gaps"]}
    assert len(gaps) == 9
    assert gaps["P03-SP01-GAP-001"]["status"] == "CARRIED_FORWARD"
    assert gaps["P03-SP02-GAP-001"]["status"] == "PARTIALLY_RESOLVED_SOURCE_SPAN_VERIFIED_INTERPRETATION_HELD"
    assert gaps["P03-SP02-GAP-002"]["status"] == "RESOLVED_BY_SUPPLEMENTAL_SOURCE_RECORDS"
    assert gaps["P03-SP02-GAP-003"]["status"] == "RESOLVED_BY_SP03-201_AND_SP03-202"
    assert gaps["P03-SP02-GAP-004"]["status"] == "CARRIED_FORWARD"
    assert gaps["P03-SP02-GAP-005"]["status"] == "CARRIED_FORWARD"
    assert "机录像" in gaps["P03-SP02-GAP-001"]["source_literal_claim"]
    assert "机梁紫破" not in gaps["P03-SP02-GAP-001"]["source_literal_claim"]
    assert "P03S-GAP-002-FEMALE" in {r["projection_rule_id"] for r in d["records"]}
    assert "P03S-GAP-002-MALE" in {r["projection_rule_id"] for r in d["records"]}
    assert d["summary"]["source_coverage_gap_count"] == 9
    assert d["summary"]["open_source_coverage_gap_count"] == 4


def test_execution_boundary_and_cumulative_state_reconcile_all_ledgers():
    d = load(READJ)
    boundary = d["execution_boundary"]
    assert boundary["canonical_promotion_is_source_only"] is True
    assert boundary["conditions_compiled"] == 0
    assert boundary["execution_unlocked"] == 0
    assert boundary["product_runtime_authorized"] is False
    assert boundary["shared_core_semantics_changed"] is False
    assert boundary["other_palace_changed"] is False
    assert boundary["history_feedback"] == 0
    for key in ["new_primitive_qi", "new_memory_type", "new_independent_time_scale",
                "new_shared_group_semantics", "numeric_weight", "probability", "decay",
                "product_runtime_change"]:
        assert d["summary"][key] == 0
    state = STATE.read_text(encoding="utf-8")
    assert 'status: "ACTIVE"' in state or 'status: "ACTIVE_NO_ACTIVE_WORK"' in state
    if 'status: "ACTIVE"' in state:
        issue_match = re.search(r"(?m)^  active_issue: (\\d+)$", state)
        branch_match = re.search(r'(?m)^  active_branch: "([^"]+)"
    batches = [load(path) for path in sorted(READJ.parent.glob("SPOUSE_SP*_SOURCE_READJUDICATION_*.json"))]
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
    assert "P03-SP01-GAP-001" in state
    assert "conditions_compiled=0" in state
    assert "execution_unlocked=0" in state
, state)
        assert issue_match and branch_match
        assert f"p03-{issue_match.group(1)}-" in branch_match.group(1)
    else:
        assert "active_issue: null" in state
        assert "active_branch: null" in state
        assert "active_pr: null" in state
    assert "SOURCE_FIRST_REVIEW_COMPLETE" in state
    batches = [load(path) for path in sorted(READJ.parent.glob("SPOUSE_SP*_SOURCE_READJUDICATION_*.json"))]
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
    assert "P03-SP01-GAP-001" in state
    assert "conditions_compiled=0" in state
    assert "execution_unlocked=0" in state

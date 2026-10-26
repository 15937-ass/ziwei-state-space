import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "knowledge/states/P07_MIGRATION_STATE.yaml"
M05_READJ = ROOT / "knowledge/palaces/P07_migration/wp05/MIGRATION_M05_SOURCE_READJUDICATION_100_v0.1.json"
M06_READJ = ROOT / "knowledge/palaces/P07_migration/wp05/MIGRATION_M06_SOURCE_READJUDICATION_090_v0.1.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_p07_state_cache_matches_accepted_m06_checkpoint():
    state = STATE.read_text(encoding="utf-8")
    assert 'status: "ACTIVE"' in state
    assert "active_issue: 669" in state
    assert 'active_branch: "knowledge/p07-669-migration-residual-gaps-114-118"' in state
    assert "active_pr: null" in state
    assert "M06_501_590_SOURCE_FIRST_MERGED" in state
    assert "Issue #645 / PR #656" in state
    assert "590 cumulative candidates reviewed" in state
    assert "520 reusable projection/method records" in state
    assert "70 CASE_SUPPORT_ONLY" in state
    residual_gap_ids = {
        "P07-M05-GAP-001", "P07-M05-GAP-002",
        "P07-M05-GAP-003", "P07-M05-GAP-004",
        "P07-M03-GAP-001", "P07-M03-GAP-012",
    }
    assert all(gap_id in state for gap_id in residual_gap_ids)
    assert "printed pp114–118" in state
    assert "No Product runtime authorization is implied" in state


def test_p07_m05_accepted_batch_counts_and_gaps_remain_immutable():
    d = load(M05_READJ)
    s = d["summary"]
    assert s["reviewed"] == 100
    assert s["reusable_projection_rules"] == 90
    assert s["case_support_only"] == 10
    assert s["source_span_changed_count"] == 41
    assert s["m04_source_gaps_closed"] == 3
    assert s["new_source_coverage_gap_count"] == 4
    assert s["cumulative_reviewed_after_batch"] == 500
    assert s["cumulative_reusable_projection_rules_after_batch"] == 443
    assert s["cumulative_case_support_only_after_batch"] == 57
    assert s["history_feedback"] == 0
    assert s["canonical_path_dependent_gate_ids"] == []
    assert {g["gap_id"] for g in d["source_coverage_gaps"]} == {
        "P07-M05-GAP-001", "P07-M05-GAP-002",
        "P07-M05-GAP-003", "P07-M05-GAP-004",
    }
    assert {g["gap_id"] for g in d["carried_forward_source_gaps"]} == {
        "P07-M03-GAP-001", "P07-M03-GAP-012",
    }


def test_p07_m06_counts_and_six_residual_gaps_reconcile():
    m05 = load(M05_READJ)
    d = load(M06_READJ)
    m05_summary = m05["summary"]
    s = d["summary"]
    residual_gap_ids = {
        "P07-M05-GAP-001", "P07-M05-GAP-002",
        "P07-M05-GAP-003", "P07-M05-GAP-004",
        "P07-M03-GAP-001", "P07-M03-GAP-012",
    }

    assert s["reviewed"] == 90
    assert s["reusable_projection_rules"] == 77
    assert s["case_support_only"] == 13
    assert s["source_span_changed_count"] == 33
    assert s["source_resolution_change_count"] == 31
    assert s["canonical_path_dependent_gate_rows"] == []
    assert s["canonical_history_feedback_rows"] == 0

    # Reconcile the M06 accepted checkpoint against M05 cumulative totals.
    assert m05_summary["cumulative_reviewed_after_batch"] + s["reviewed"] == 590
    assert m05_summary["cumulative_reusable_projection_rules_after_batch"] + s["reusable_projection_rules"] == 520
    assert m05_summary["cumulative_case_support_only_after_batch"] + s["case_support_only"] == 70

    m05_gap_ids = {g["gap_id"] for g in m05["source_coverage_gaps"]}
    m05_carried_gap_ids = {g["gap_id"] for g in m05["carried_forward_source_gaps"]}
    assert m05_gap_ids | m05_carried_gap_ids == residual_gap_ids
    assert {g["gap_id"] for g in d["source_coverage_gaps"]} == residual_gap_ids

    state = STATE.read_text(encoding="utf-8")
    assert "M06_501_590_SOURCE_FIRST_MERGED" in state
    assert "590 cumulative candidates reviewed" in state
    assert "520 reusable projection/method records" in state
    assert "70 CASE_SUPPORT_ONLY" in state
    assert all(gap_id in state for gap_id in residual_gap_ids)

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "knowledge/states/P07_MIGRATION_STATE.yaml"
READJ = ROOT / "knowledge/palaces/P07_migration/wp05/MIGRATION_M05_SOURCE_READJUDICATION_100_v0.1.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_p07_state_cache_matches_accepted_m05_checkpoint():
    state = STATE.read_text(encoding="utf-8")
    assert 'status: "ACTIVE_NO_ACTIVE_WORK"' in state
    assert "active_issue: null" in state
    assert "active_branch: null" in state
    assert "active_pr: null" in state
    assert "M05_401_500_SOURCE_FIRST_MERGED" in state
    assert "Issue #619 / PR #622" in state
    assert "printed-p118 Tianxiang gaps remain explicit" in state
    assert "P07-M03-GAP-001" in state and "P07-M03-GAP-012" in state
    assert "M06-501…590" in state
    assert "No Product runtime authorization is implied" in state


def test_p07_m05_accepted_counts_and_remaining_gaps_reconcile():
    d = load(READJ)
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

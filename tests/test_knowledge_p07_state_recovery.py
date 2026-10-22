import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "knowledge/states/P07_MIGRATION_STATE.yaml"
M05 = ROOT / "knowledge/palaces/P07_migration/wp05/MIGRATION_M05_SOURCE_READJUDICATION_100_v0.1.json"


def test_p07_state_cache_matches_merged_m05_checkpoint():
    state = STATE.read_text(encoding="utf-8")
    assert 'status: "ACTIVE_NO_ACTIVE_WORK"' in state
    assert "active_issue: null" in state
    assert "active_branch: null" in state
    assert "active_pr: null" in state
    assert "M01_M05_500_CANDIDATES_REVIEWED" in state
    assert "M06_NOT_SOURCE_FIRST_CANONICALIZED" in state
    assert "PR #622 merged at d3eacc75fa745cef12a01ed29f899984ea10591a" in state
    assert "No Product runtime authorization" in state


def test_p07_m05_accepted_counts_and_residual_gaps_are_preserved():
    data = json.loads(M05.read_text(encoding="utf-8"))
    summary = data["summary"]
    assert data["issue"] == 619
    assert len(data["records"]) == 100
    assert summary["reviewed"] == 100
    assert summary["reusable_projection_rules"] == 90
    assert summary["case_support_only"] == 10
    assert summary["cumulative_reviewed_after_batch"] == 500
    assert summary["cumulative_reusable_projection_rules_after_batch"] == 443
    assert summary["cumulative_case_support_only_after_batch"] == 57
    assert summary["new_source_coverage_gap_count"] == 4
    assert summary["carried_forward_source_gap_count"] == 2
    assert summary["product_runtime_change"] == 0

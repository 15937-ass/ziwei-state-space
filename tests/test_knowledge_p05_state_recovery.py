import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "knowledge/states/P05_WEALTH_STATE.yaml"
W05 = ROOT / "knowledge/palaces/P05_wealth/w05/WEALTH_W05_SOURCE_READJUDICATION_100_v0.1.json"


def test_p05_state_cache_matches_merged_w05_checkpoint():
    state = STATE.read_text(encoding="utf-8")
    assert 'status: "ACTIVE_NO_ACTIVE_WORK"' in state
    assert "active_issue: null" in state
    assert "active_branch: null" in state
    assert "active_pr: null" in state
    assert "W01_W05_500_CANDIDATES_REVIEWED" in state
    assert "3_P05_SOURCE_GAPS_REMAIN" in state
    assert "PR #634 merged at 7bf664fc87db20bfe02ef0020785b91dd62cbbdf" in state
    assert "No Product runtime authorization" in state


def test_p05_w05_accepted_counts_and_fail_closed_boundaries_are_preserved():
    data = json.loads(W05.read_text(encoding="utf-8"))
    summary = data["summary"]
    assert data["issue"] == 591
    assert len(data["records"]) == 100
    assert summary["reviewed"] == 100
    assert summary["canonical_promoted"] == 100
    assert summary["reusable_projection_rules"] == 100
    assert summary["case_support_only"] == 0
    assert summary["source_resolution_change_count"] == 15
    assert summary["visually_resolved_extraction_count"] == 12
    assert summary["path_dependent_gate_count"] == 7
    assert summary["source_coverage_gap_count"] == 3
    assert summary["unresolved_source_uncertainty_count"] == 0
    assert summary["new_shared_primitive"] == 0
    assert summary["new_memory_type"] == 0
    assert summary["numeric_weight"] == 0
    assert summary["probability"] == 0
    assert summary["threshold"] == 0
    assert summary["decay"] == 0

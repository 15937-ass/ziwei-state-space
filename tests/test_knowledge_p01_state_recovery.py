from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "knowledge/states/P01_LIFE_STATE.yaml"


def test_p01_state_cache_matches_accepted_p04_checkpoint():
    state = STATE.read_text(encoding="utf-8")
    assert 'status: "ACTIVE_NO_ACTIVE_WORK"' in state
    assert "active_issue: null" in state
    assert "active_branch: null" in state
    assert "active_pr: null" in state
    assert "P01_P04_301_400_SOURCE_FIRST_MERGED" in state
    assert "canonical_source_records_on_main: 550" in state
    assert "cumulative_reusable_projection_rules_after_merge: 451" in state
    assert "cumulative_case_support_only_after_merge: 99" in state
    assert "P01-SRC-GAP-025" in state
    assert "P05-401…500" in state
    assert "No Product runtime authorization is implied" in state

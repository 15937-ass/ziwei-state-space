import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "knowledge/states/P01_LIFE_STATE.yaml"
SUMMARY = ROOT / "knowledge/palaces/P01_life/wp05/LIFE_P04_SOURCE_READJUDICATION_SUMMARY_v0.1.json"
GAP_LEDGER = ROOT / "knowledge/palaces/P01_life/wp05/LIFE_P03_SOURCE_GAP_LEDGER_v0.1.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_p01_state_cache_matches_accepted_p04_checkpoint():
    state = STATE.read_text(encoding="utf-8")
    assert 'status: "ACTIVE_NO_ACTIVE_WORK"' in state
    assert "active_issue: null" in state
    assert "active_branch: null" in state
    assert "active_pr: null" in state
    assert "P01_P04_301_400_SOURCE_FIRST_P12_P14_MERGED" in state
    assert "main commit 6472bdbf273ffbce4e9948f86969a4b84178b36b" in state
    assert "P01-SRC-GAP-025" in state
    assert "No Product/runtime authorization is implied" in state


def test_p01_accepted_p04_counts_reconcile():
    s = load(SUMMARY)["summary"]
    assert s["historical_candidates_reviewed"] == 100
    assert s["canonical_promoted"] == 100
    assert s["new_source_gap_supplement_records"] == 28
    assert s["new_canonical_records"] == 128
    assert s["reusable_projection_rules"] == 109
    assert s["case_support_only"] == 19
    assert s["registered_gaps_closed"] == ["P01-SRC-GAP-023", "P01-SRC-GAP-024"]
    assert s["cumulative_canonical_records_after_merge"] == 550
    assert s["cumulative_reusable_projection_rules_after_merge"] == 451
    assert s["cumulative_case_support_only_after_merge"] == 99


def test_p01_source_gap_025_remains_explicit_for_next_checkpoint():
    ledger = load(GAP_LEDGER)
    gap = next(g for g in ledger["next_checkpoint_gaps"] if g["gap_id"] == "P01-SRC-GAP-025")
    assert gap["status"] == "OPEN_FOR_NEXT_SOURCE_CHECKPOINT"
    assert "printed p15 onward" in gap["source_location"]
    assert gap["next_source_anchor"] == ledger["next_source_anchor"]
    assert gap["next_source_anchor"] in STATE.read_text(encoding="utf-8")

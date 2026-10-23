import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "knowledge/states/P01_LIFE_STATE.yaml"
SUMMARY_P04 = ROOT / "knowledge/palaces/P01_life/wp05/LIFE_P04_SOURCE_READJUDICATION_SUMMARY_v0.1.json"
SUMMARY_P05 = ROOT / "knowledge/palaces/P01_life/wp05/LIFE_P05_SOURCE_READJUDICATION_SUMMARY_v0.1.json"
SUMMARY_P06 = ROOT / "knowledge/palaces/P01_life/wp05/LIFE_P06_SOURCE_READJUDICATION_SUMMARY_v0.1.json"
GAP_LEDGER = ROOT / "knowledge/palaces/P01_life/wp05/LIFE_P03_SOURCE_GAP_LEDGER_v0.1.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_p01_state_cache_matches_accepted_p06_checkpoint():
    state = STATE.read_text(encoding="utf-8")
    assert 'status: "ACTIVE_NO_ACTIVE_WORK"' in state
    assert "active_issue: null" in state
    assert "active_branch: null" in state
    assert "active_pr: null" in state
    assert 'canonical_checkpoint: "P01_P06_501_600_SOURCE_FIRST_P17_P20_MERGED"' in state
    assert "canonical_source_records_on_main: 788" in state
    assert "canonical_source_records_ready_on_branch" not in state
    assert "cumulative_after_merge: 788" in state
    assert "cumulative_reusable_projection_rules_after_merge: 655" in state
    assert "cumulative_case_support_only_after_merge: 133" in state
    assert "P01-SRC-GAP-026" in state and "P01-SRC-GAP-027" in state
    assert "P01-601…P01-700" in state
    assert "No Product/runtime authorization is implied" in state


def test_p01_accepted_p04_counts_remain_historically_reconciled():
    s = load(SUMMARY_P04)["summary"]
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


def test_p01_accepted_p05_counts_remain_historically_reconciled():
    s = load(SUMMARY_P05)["summary"]
    assert s["historical_candidates_reviewed"] == 100
    assert s["canonical_promoted"] == 82
    assert s["deduplicated_scope_metadata_rows"] == 18
    assert s["new_source_gap_supplement_records"] == 15
    assert s["new_canonical_records"] == 97
    assert s["reusable_projection_rules"] == 79
    assert s["case_support_only"] == 18
    assert s["cumulative_canonical_records_after_merge"] == 647
    assert s["cumulative_reusable_projection_rules_after_merge"] == 530
    assert s["cumulative_case_support_only_after_merge"] == 117
    assert s["new_primitive_qi"] == s["new_memory_type"] == s["new_independent_time_scale"] == 0
    assert s["numeric_weight"] == s["probability"] == s["decay"] == 0
    assert load(SUMMARY_P05)["human_gate_required"] is False


def test_p01_accepted_p06_counts_reconcile():
    s = load(SUMMARY_P06)["summary"]
    assert s["historical_candidates_reviewed"] == 100
    assert s["canonical_promoted"] == 100
    assert s["deduplicated_scope_metadata_rows"] == 0
    assert s["new_source_gap_supplement_records"] == 41
    assert s["new_canonical_records"] == 141
    assert s["reusable_projection_rules"] == 125
    assert s["case_support_only"] == 16
    assert s["cumulative_canonical_records_after_merge"] == 788
    assert s["cumulative_reusable_projection_rules_after_merge"] == 655
    assert s["cumulative_case_support_only_after_merge"] == 133
    assert s["new_primitive_qi"] == s["new_memory_type"] == s["new_independent_time_scale"] == 0
    assert s["numeric_weight"] == s["probability"] == s["decay"] == 0
    assert load(SUMMARY_P06)["human_gate_required"] is False


def test_p01_source_gap_026_closed_and_027_is_next():
    ledger = load(GAP_LEDGER)
    entries = {g["gap_id"]: g for g in ledger["entries"]}
    assert entries["P01-SRC-GAP-025"]["status"] == "CLOSED_BY_SOURCE_RECHECK_AND_CANONICAL_RULES"
    assert len(entries["P01-SRC-GAP-025"]["rule_ids"]) == 91
    assert "P01-419" in entries["P01-SRC-GAP-025"]["rule_ids"]
    assert "P01-SG-167" in entries["P01-SRC-GAP-025"]["rule_ids"]
    gap = entries["P01-SRC-GAP-026"]
    assert gap["status"] == "CLOSED_BY_SOURCE_RECHECK_AND_CANONICAL_RULES"
    assert len(gap["rule_ids"]) == 141
    assert "P01-501" in gap["rule_ids"] and "P01-SG-208" in gap["rule_ids"]
    next_gaps = ledger["next_checkpoint_gaps"]
    assert len(next_gaps) == 1
    next_gap = next_gaps[0]
    assert next_gap["gap_id"] == "P01-SRC-GAP-027"
    assert next_gap["status"] == "OPEN_FOR_NEXT_SOURCE_CHECKPOINT"
    assert "printed p21" in next_gap["source_location"]
    assert "七杀" in next_gap["source_claim"]
    assert next_gap["next_source_anchor"] == ledger["next_source_anchor"]
    assert "P01-601" in ledger["next_source_anchor"]
    assert ledger["next_source_anchor"] in STATE.read_text(encoding="utf-8")

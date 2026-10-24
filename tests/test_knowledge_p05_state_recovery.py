import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "knowledge/states/P05_WEALTH_STATE.yaml"
READJ = ROOT / "knowledge/palaces/P05_wealth/w05/WEALTH_W05_SOURCE_READJUDICATION_100_v0.1.json"
TIME = ROOT / "knowledge/palaces/P05_wealth/w05/WEALTH_W05_SOURCE_TIME_SCOPE_v0.1.json"
GAPS = ROOT / "knowledge/palaces/P05_wealth/w05/WEALTH_W05_SOURCE_GAPS_v0.1.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_p05_state_cache_matches_current_jumen_checkpoint_and_preserves_w05_baseline():
    state = STATE.read_text(encoding="utf-8")
    assert 'status: "ACTIVE"' in state
    assert "active_issue: 737" in state
    assert 'active_branch: "knowledge/p05-737-source-first-jumen-p86-p87-r2"' in state
    assert "active_pr: 744" in state
    assert "W05_401_500_SOURCE_FIRST_MERGED" in state
    assert "main commit 7bf664fc87db20bfe02ef0020785b91dd62cbbdf" in state
    assert "current main commit 74087c97afffc5afa4821f8edb21ff42aea6eb6b" in state
    assert "after Product PR #640 merged" in state
    assert "merged_rule_count: 642" in state
    assert "reviewed_rule_count: 500" in state
    assert "current_batch_rule_count: 42" in state
    assert "source_first_records_added_current_batch: 42" in state
    assert "W05-SG-001" in state and "W05-SG-003" in state
    assert "W06-SG-001" in state and "W06-SG-004" in state and "W06-SG-005" in state
    assert "source_uncertainty_count_current_batch: 0" in state
    assert "path_dependent_gate_count_current_batch: 4" in state
    assert "source_coverage_gap_count_current_batch: 0" in state
    assert "source_coverage_gaps_remaining: 6" in state
    assert "printed p87" in state and "11 天相" in state
    assert "No Product/runtime authorization is implied" in state


def test_w05_accepted_batch_summary_reconciles():
    summary = load(READJ)["summary"]
    assert summary["reviewed"] == 100
    assert summary["canonical_promoted"] == 100
    assert summary["reusable_projection_rules"] == 100
    assert summary["case_support_only"] == 0
    assert summary["source_resolution_change_count"] == 15
    assert summary["unresolved_source_uncertainty_count"] == 0
    assert summary["visually_resolved_extraction_count"] == 12
    assert summary["non_natal_source_rows"] == 0
    assert summary["path_dependent_gate_count"] == 7
    assert summary["source_coverage_gap_count"] == 3


def test_w05_state_preserves_all_three_local_gaps_and_no_core_gap():
    gaps = load(GAPS)
    assert gaps["gap_count"] == 3
    assert gaps["core_gap_count"] == 0
    assert {g["gap_id"] for g in gaps["gaps"]} == {"W05-SG-001", "W05-SG-002", "W05-SG-003"}
    assert all(g["status"] == "OPEN" and g["core_gap"] is False for g in gaps["gaps"])


def test_w05_time_scope_and_ordered_path_gates_are_preserved():
    sidecar = load(TIME)
    assert sidecar["counts"]["non_natal_rows"] == 0
    assert sidecar["counts"]["year"] == 0
    assert sidecar["counts"]["decade"] == 0
    assert sidecar["counts"]["path_dependent_gate_rows"] == 7
    assert set(sidecar["path_dependent_gate_ids"]) == {
        "W05-403", "W05-410", "W05-411", "W05-414", "W05-416", "W05-429", "W05-434"
    }

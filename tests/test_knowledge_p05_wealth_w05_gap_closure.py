import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "knowledge/palaces/P05_wealth/w05"
STATE = ROOT / "knowledge/states/P05_WEALTH_STATE.yaml"
SUPPLEMENT = BASE / "WEALTH_W05_SOURCE_GAP_SUPPLEMENT_v0.1.csv"
LEDGER = BASE / "WEALTH_W05_SOURCE_GAP_CLOSURE_LEDGER_v0.1.json"
SUMMARY = BASE / "WEALTH_W05_SOURCE_GAP_SUMMARY_v0.1.json"
TIME = BASE / "WEALTH_W05_SOURCE_GAP_TIME_SCOPE_v0.1.json"
ORIGINAL_GAPS = BASE / "WEALTH_W05_SOURCE_GAPS_v0.1.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def rows():
    with SUPPLEMENT.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def test_supplement_ids_provenance_and_canonical_scope():
    data = rows()
    assert len(data) == 4
    ids = {r["projection_rule_id"] for r in data}
    assert ids == {"P05-SG-001", "P05-SG-002", "P05-SG-003", "P05-SG-004"}
    assert len(ids) == len(data)
    assert all(r["projection_rule_id"].startswith("P05-SG-") for r in data)
    assert all(r["source_id"] == "SRC-ZZ-003" for r in data)
    assert all(r["source_location"].endswith("printed_p81") for r in data)
    assert all(r["archived_primary_time_layer"] == "NATAL" for r in data)
    assert all(r["canonical_promotion"] == "true" for r in data)
    assert all(r["case_support_only"] == "false" for r in data)
    assert all(r["source_epistemic"] == "EXPLICIT" for r in data)
    assert {r["projection_domain"] for r in data} <= {"spending", "risk", "retention", "volatility"}
    assert {r["projection_target"] for r in data} <= {
        "financial_harm", "dispute_risk", "wealth_hard_to_accumulate", "financial_source_fluctuation"
    }
    assert all(r["projection_mode"] == "FUNCTIONAL_PROJECTION" for r in data)
    assert {r["direction_or_state"] for r in data} <= {"adverse", "conditional", "source_bounded"}
    assert all(r["source_gap_id"] in {"W05-SG-001", "W05-SG-002", "W05-SG-003"} for r in data)
    litigation = next(r for r in data if r["projection_rule_id"] == "P05-SG-002")
    assert "有煞曜空劫" in litigation["canonical_condition"]
    assert "煞曜空劫" in litigation["canonical_normalization"]
    assert "刑忌夹印" not in litigation["canonical_condition"]
    assert "廉贞化忌" not in litigation["canonical_condition"]
    assert not ids.intersection({"W05-499", "W05-500", "W05-SG-001", "W05-SG-002", "W05-SG-003"})


def test_gap_ledger_closes_only_supported_claims():
    ledger = load(LEDGER)
    entries = {e["gap_id"]: e for e in ledger["entries"]}
    assert set(entries) == {"W05-SG-001", "W05-SG-002", "W05-SG-003"}
    assert entries["W05-SG-001"]["status"] == "CLOSED_BY_NEW_CANONICAL_RULES"
    assert entries["W05-SG-001"]["rule_ids"] == ["P05-SG-001", "P05-SG-002"]
    assert entries["W05-SG-002"]["status"] == "PARTIALLY_RESOLVED"
    assert entries["W05-SG-002"]["rule_ids"] == ["P05-SG-003"]
    assert len(entries["W05-SG-002"]["unresolved_claims"]) == 2
    assert "有是非词不达意讼" in entries["W05-SG-002"]["unresolved_claims"][0]
    assert "有是非词讼" in entries["W05-SG-002"]["unresolved_claims"][0]
    assert "prior_image_resolution_reconciliation" in entries["W05-SG-002"]
    assert "not treated as the canonical literal quotation" in entries["W05-SG-002"]["prior_image_resolution_reconciliation"]
    assert entries["W05-SG-003"]["status"] == "CLOSED_BY_NEW_CANONICAL_RULES"
    assert entries["W05-SG-003"]["rule_ids"] == ["P05-SG-004"]
    assert ledger["rule_count"] == 4
    assert ledger["unresolved_prior_gap_ids"] == ["W05-SG-002"]
    assert ledger["shared_semantic_gaps"] == []


def test_original_w05_batch_gap_ledger_remains_historical_and_unchanged():
    original = load(ORIGINAL_GAPS)
    assert original["gap_count"] == 3
    assert original["core_gap_count"] == 0
    assert {g["gap_id"] for g in original["gaps"]} == {"W05-SG-001", "W05-SG-002", "W05-SG-003"}
    assert all(g["status"] == "OPEN" for g in original["gaps"])


def test_time_scope_and_cumulative_summary_reconcile():
    sidecar = load(TIME)
    assert len(sidecar["records"]) == 4
    assert all(r["source_time_layers"] == ["NATAL"] for r in sidecar["records"])
    assert all(r["scope_status"] == "SOURCE_SCOPE_MATCHES_PRIMARY_LAYER" for r in sidecar["records"])
    summary = load(SUMMARY)
    s = summary["summary"]
    assert s["prior_gap_ids"] == 3
    assert s["new_canonical_records"] == 4
    assert s["reusable_projection_rules"] == 4
    assert s["case_support_only"] == 0
    assert s["prior_gaps_closed_by_new_rules"] == 2
    assert s["prior_gaps_partially_resolved"] == 1
    assert s["unresolved_prior_gap_ids"] == ["W05-SG-002"]
    assert s["cumulative_canonical_records_after_merge"] == 504
    assert s["cumulative_reusable_projection_rules_after_merge"] == 504
    assert s["cumulative_case_support_only_after_merge"] == 0
    assert s["new_primitive_qi"] == s["new_memory_type"] == s["new_independent_time_scale"] == 0
    assert s["numeric_weight"] == s["probability"] == s["threshold"] == s["frequency_parameter"] == s["decay"] == 0
    assert summary["shared_semantic_gaps"] == []
    assert summary["human_gate_required"] is False


def test_p05_state_cache_tracks_tianxiang_and_preserves_historical_w05_gap():
    state = STATE.read_text(encoding="utf-8")
    assert 'status: "ACTIVE"' in state
    assert "active_issue: 746" in state
    assert 'active_branch: "knowledge/p05-746-source-first-tianxiang-p87-p88"' in state
    assert "W05_401_500_SOURCE_FIRST_MERGED" in state
    assert "Post-merge P05 total is 563 canonical reusable rules." in state
    assert "P05 canonical reusable rule count after this checkpoint is 642" in state
    assert "source_gap_supplement_record_count: 4" in state
    assert "source_coverage_gaps_closed_by_supplement: 2" in state
    assert "source_coverage_gaps_partially_resolved_by_supplement: 1" in state
    assert "source_coverage_gaps_remaining: 6" in state
    assert "W06-SG-001" in state and "W06-SG-004" in state and "W06-SG-005" in state
    assert "W05-SG-002 remains PARTIALLY_RESOLVED" in state
    assert "12 天梁" in state
    assert "No Product/runtime authorization is implied" in state

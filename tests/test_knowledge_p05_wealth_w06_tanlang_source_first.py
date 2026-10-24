import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "knowledge/palaces/P05_wealth/w06"
STATE = ROOT / "knowledge/states/P05_WEALTH_STATE.yaml"
SUMMARY = BASE / "WEALTH_W06_CANONICAL_SUMMARY_v0.1.md"
SOURCE = BASE / "WEALTH_W06_TANLANG_SOURCE_READJUDICATION_P85_P86_v0.1.json"
TIME = BASE / "WEALTH_W06_TANLANG_SOURCE_TIME_SCOPE_P85_P86_v0.1.json"
GAPS = BASE / "WEALTH_W06_TANLANG_SOURCE_GAPS_P85_P86_v0.1.json"
LEDGER = BASE / "WEALTH_W06_TANLANG_SOURCE_GAP_CLOSURE_LEDGER_P85_P86_v0.1.json"
PREVIOUS = BASE / "WEALTH_W06_SOURCE_READJUDICATION_501_600_v0.1.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_tanlang_batch_has_exact_source_scope_and_unique_ids():
    data = load(SOURCE)
    rows = data["records"]
    assert data["issue"] == 733
    assert data["source_basis"]["sha256"] == "6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c"
    assert "printed p85" in data["source_basis"]["note"]
    assert "9 贪狼" in data["source_basis"]["note"]
    assert "printed p86" in data["source_basis"]["note"]
    assert "10 巨门" in data["source_basis"]["note"]
    assert len(rows) == 38
    assert [r["projection_rule_id"] for r in rows] == [f"W06-{i}" for i in range(563, 601)]
    assert len({r["projection_rule_id"] for r in rows}) == 38
    assert all(r["source_location"] in {"财帛宫printed_p85", "财帛宫printed_p86"} for r in rows)
    assert all("10 巨门" not in r["source_digest"] and "巨门守财帛宫" not in r["source_digest"] for r in rows)
    assert rows[0]["source_digest"].startswith("贪狼守财帛宫，手段阔绰大方")
    assert rows[-1]["source_digest"].startswith("辰戌贪狼落罗网")
    assert data["summary"]["current_batch_records_created"] == 38
    assert data["summary"]["current_batch_canonical_promotions"] == 37
    assert data["summary"]["current_batch_source_uncertainty_count"] == 1
    assert data["summary"]["cumulative_canonical_records_after_merge"] == 600
    assert data["summary"]["cumulative_reusable_projection_rules_after_merge"] == 600


def test_tanlang_named_setup_is_literal_and_not_promoted():
    data = load(SOURCE)
    row = next(r for r in data["records"] if r["projection_rule_id"] == "W06-596")
    assert "『风流采杖』" in row["source_digest"]
    assert row["canonical_promotion"] is False
    assert row["source_uncertainty"] is not None
    assert row["disposition"] == "SOURCE_TEXT_UNRESOLVED_RETAINED_FOR_AUDIT"
    gaps = load(GAPS)
    assert gaps["gap_count"] == 1
    assert gaps["core_gap_count"] == 0
    assert gaps["gaps"][0]["gap_id"] == "W06-SG-005"
    assert gaps["gaps"][0]["status"] == "OPEN"
    assert gaps["gaps"][0]["rule_ids"] == ["W06-596"]
    ledger = load(LEDGER)
    assert ledger["rule_count"] == 0
    assert ledger["open_gap_count"] == 1
    assert "W05-SG-002" in ledger["unresolved_prior_gap_ids"]
    assert "W06-SG-001" in ledger["unresolved_prior_gap_ids"]
    assert "W06-SG-004" in ledger["unresolved_prior_gap_ids"]


def test_tanlang_temporal_sidecar_does_not_invent_year_or_decade_rules():
    data = load(TIME)
    assert data["counts"] == {"non_natal_rows": 0, "year": 0, "decade": 0, "path_dependent_gate_rows": 0, "source_age_qualifier_rows": 0}
    assert data["exact_non_natal_ids"] == []
    assert data["year_ids"] == []
    assert data["decade_ids"] == []
    assert data["path_dependent_gate_ids"] == []
    assert data["records"] == []
    assert data["path_records"] == []
    assert data["source_age_qualifier_records"] == []


def test_tanlang_batch_preserves_prior_audit_and_reconciles_current_state():
    previous = load(PREVIOUS)
    assert len(previous["records"]) == 62
    assert previous["records"][-1]["projection_rule_id"] == "W06-562"
    assert previous["summary"]["cumulative_canonical_records_after_merge"] == 563
    state = STATE.read_text(encoding="utf-8")
    assert "merged_rule_count: 642" in state
    assert "current_batch_rule_count: 42" in state
    assert "source_first_records_added_current_batch: 42" in state
    assert "source_uncertainty_count_current_batch: 0" in state
    assert "path_dependent_gate_count_current_batch: 4" in state
    assert "source_coverage_gap_count_current_batch: 0" in state
    assert "source_coverage_gaps_remaining: 6" in state
    assert "W06-SG-001" in state and "W06-SG-005" in state
    assert "W05-SG-002" in state and "PARTIALLY_RESOLVED" in state
    assert "10 巨门" in state
    assert "No Product/runtime authorization is implied" in state
    summary = SUMMARY.read_text(encoding="utf-8")
    assert "Issue #733" in summary
    assert "W06-563…W06-600" in summary
    assert "W06-SG-005" in summary
    assert "10 巨门" in summary

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "knowledge/palaces/P05_wealth/w08"
STATE = ROOT / "knowledge/states/P05_WEALTH_STATE.yaml"
SOURCE = BASE / "WEALTH_W08_TIANLIANG_SOURCE_READJUDICATION_P88_P90_v0.1.json"
TIME = BASE / "WEALTH_W08_TIANLIANG_SOURCE_TIME_SCOPE_P88_P90_v0.1.json"
GAPS = BASE / "WEALTH_W08_TIANLIANG_SOURCE_GAPS_P88_P90_v0.1.json"
SUMMARY = BASE / "WEALTH_W08_TIANLIANG_CANONICAL_SUMMARY_P88_P90_v0.1.md"
PRIOR = {"W05-SG-002", "W06-SG-001", "W06-SG-002", "W06-SG-003", "W06-SG-004", "W06-SG-005", "W08-SG-001", "W08-SG-002"}

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def row(data, rid):
    return next(r for r in data["records"] if r["projection_rule_id"] == rid)

def test_source_hash_boundary_and_candidate_census():
    data = load(SOURCE)
    assert data["issue"] == 760
    assert data["source_basis"]["sha256"] == "6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c"
    assert "88–90" in data["source_basis"]["printed_pages"]
    assert "12 天梁" in data["source_basis"]["printed_pages"]
    assert "13 七杀" in data["source_basis"]["printed_pages"]
    ids = [r["projection_rule_id"] for r in data["records"]]
    assert ids == [f"W08-{i}" for i in range(788, 826)]
    assert len(ids) == len(set(ids)) == 38
    assert data["summary"]["historical_candidates_reviewed"] == 13
    assert data["summary"]["new_source_supported_atoms"] == 24
    assert data["summary"]["new_source_atoms_reviewed"] == 25
    assert data["summary"]["new_atoms_not_promoted_due_uncertainty"] == 1
    assert data["summary"]["canonical_promotions"] == 37
    assert data["summary"]["cumulative_canonical_records_after_merge"] == 721
    assert data["summary"]["unresolved_candidate_ids"] == ["W08-820"]

def test_historical_candidate_reconciliation_and_correction():
    data = load(SOURCE)
    assert data["candidate_inputs"][0]["count"] == 13
    assert data["summary"]["candidate_condition_or_scope_correction_ids"] == ["W08-798"]
    assert row(data, "W08-798")["archived_candidate_condition"] == "天梁荫星"
    assert "does not require" in row(data, "W08-798")["source_note"]
    assert "或主有现成事业生财" in row(data, "W08-798")["source_digest"]
    assert row(data, "W08-788")["canonical_promotion"] is True
    assert row(data, "W08-825")["source_location"] == "财帛宫printed_p90"

def test_source_text_anomalies_are_literal_and_not_silently_repaired():
    data = load(SOURCE)
    gaps = load(GAPS)
    assert row(data, "W08-812")["source_digest"].startswith("子午宫天梁，。亦可成")
    assert "W08-SG-004" in row(data, "W08-812")["source_note"]
    assert "为本星生活费居财帛宫的最大缺点" not in row(data, "W08-823")["source_digest"]
    assert "丑来天梁" in row(data, "W08-820")["canonical_condition"]
    assert "W08-SG-005" in row(data, "W08-820")["source_note"]
    assert row(data, "W08-820")["canonical_promotion"] is False
    assert row(data, "W08-820")["disposition"] == "NEW_SOURCE_ATOM_HELD_UNPROMOTED_SOURCE_UNCERTAINTY"
    assert "W08-SG-003" in row(data, "W08-823")["source_note"]
    assert gaps["gap_count"] == 3 and gaps["core_gap_count"] == 0
    assert {g["gap_id"] for g in gaps["gaps"]} == {"W08-SG-003", "W08-SG-004", "W08-SG-005"}
    assert all(g["status"] == "OPEN" and g["core_gap"] is False for g in gaps["gaps"])
    assert gaps["summary"]["unresolved_prior_gap_ids"] == sorted(PRIOR)

def test_time_scope_does_not_invent_decade_or_year_triggers():
    time = load(TIME)
    assert time["counts"] == {
        "non_natal_rows": 0,
        "year": 0,
        "decade": 0,
        "path_dependent_gate_rows": 5,
        "source_time_phrase_rows": 1,
        "source_life_course_qualifier_rows": 3,
        "source_condition_qualifier_rows": 1,
    }
    assert time["exact_non_natal_ids"] == []
    assert time["decade_ids"] == [] and time["year_ids"] == []
    assert time["path_dependent_gate_ids"] == ["W08-799", "W08-803", "W08-814", "W08-819", "W08-824"]
    assert time["source_time_phrase_records"][0]["source_time_phrase"] == "交入不佳岁运"
    assert time["source_time_phrase_records"][0]["scope_status"] == "SOURCE_EXPLICIT_FORTUNE_PERIOD_NOT_DISAMBIGUATED"

def test_prior_tianxiang_artifact_is_immutable_and_cumulative_counts_reconcile():
    prior = load(BASE / "WEALTH_W08_TIANXIANG_SOURCE_READJUDICATION_P87_P88_v0.1.json")
    data = load(SOURCE)
    assert prior["issue"] == 746 and len(prior["records"]) == 45
    assert prior["summary"]["canonical_promotions"] == 42
    assert prior["summary"]["cumulative_canonical_records_after_merge"] == 684
    assert data["summary"]["cumulative_canonical_records_after_merge"] == 684 + data["summary"]["canonical_promotions"]
    assert "13 七杀" in SUMMARY.read_text(encoding="utf-8")

def test_state_preserves_tianliang_gap_handoff_without_pinning_old_active_batch():
    state = STATE.read_text(encoding="utf-8")
    assert "source_coverage_gaps_remaining: 26" in state
    assert "P05-COV-GAP-001" in state
    assert "W05-SG-002 remains PARTIALLY_RESOLVED" in state
    assert all(g in state for g in {"W06-SG-001", "W06-SG-005", "W08-SG-001", "W08-SG-005", "W09-SG-006", "W09-SG-016"})
    assert "No Product/runtime authorization is implied" in state


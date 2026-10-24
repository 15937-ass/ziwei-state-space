import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "knowledge/palaces/P05_wealth/w08"
STATE = ROOT / "knowledge/states/P05_WEALTH_STATE.yaml"
SOURCE = BASE / "WEALTH_W08_SOURCE_READJUDICATION_P86_P87_v0.1.json"
TIME = BASE / "WEALTH_W08_SOURCE_TIME_SCOPE_P86_P87_v0.1.json"
GAPS = BASE / "WEALTH_W08_SOURCE_GAPS_P86_P87_v0.1.json"
SUMMARY = BASE / "WEALTH_W08_CANONICAL_SUMMARY_v0.1.md"
PREVIOUS_TANLANG = ROOT / "knowledge/palaces/P05_wealth/w06/WEALTH_W06_TANLANG_SOURCE_READJUDICATION_P85_P86_v0.1.json"

SOURCE_SHA = "6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c"
PRIOR_GAPS = {"W05-SG-002", "W06-SG-001", "W06-SG-002", "W06-SG-003", "W06-SG-004", "W06-SG-005"}


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def by_id(data, rule_id):
    return next(row for row in data["records"] if row["projection_rule_id"] == rule_id)


def test_jumen_batch_has_exact_source_boundary_and_candidate_reconciliation():
    data = load(SOURCE)
    rows = data["records"]
    assert data["issue"] == 737
    assert data["source_basis"]["sha256"] == SOURCE_SHA
    assert "printed p86" in data["source_basis"]["printed_pages"]
    assert "printed p87" in data["source_basis"]["printed_pages"]
    assert "10 巨门" in data["source_basis"]["note"]
    assert "11 天相" in data["source_basis"]["note"]
    assert len(rows) == 42
    assert [r["projection_rule_id"] for r in rows] == [f"W08-{i}" for i in range(701, 743)]
    assert len({r["projection_rule_id"] for r in rows}) == 42
    assert all(r["source_id"] == "SRC-ZZ-003" and r["palace_id"] == "P05" for r in rows)
    assert all(r["canonical_promotion"] is True for r in rows)
    assert all(r["source_uncertainty"] is None for r in rows)
    assert all("11 天相" not in r["source_digest"] and "天相坐财帛宫" not in r["source_digest"] for r in rows)
    assert rows[0]["source_digest"].startswith("巨门守财帛宫，基本性质为劳心费神")
    assert rows[-1]["source_digest"].startswith("巳亥巨门见禄马交驰")
    assert data["summary"]["historical_candidates_reviewed"] == 42
    assert data["summary"]["canonical_promotions"] == 42
    assert data["summary"]["cumulative_canonical_records_after_merge"] == 642


def test_jumen_preserves_inherited_conditions_and_corrects_candidate_overreach():
    data = load(SOURCE)
    assert "阴煞" in by_id(data, "W08-709")["canonical_condition"]
    assert "蜚廉" in by_id(data, "W08-709")["canonical_condition"]
    assert "太阳化忌" in by_id(data, "W08-713")["canonical_condition"]
    assert "天刑" in by_id(data, "W08-713")["canonical_condition"]
    assert "刑法纪律行业" in by_id(data, "W08-713")["canonical_condition"]
    assert "化禄、化忌皆然" in by_id(data, "W08-726")["canonical_condition"]
    assert "辰戌" in by_id(data, "W08-735")["canonical_condition"]
    assert "辰宫巨门化忌反格" not in by_id(data, "W08-735")["canonical_condition"]
    assert "且会天机化忌" in by_id(data, "W08-740")["canonical_condition"]
    assert "或会天机化忌" not in by_id(data, "W08-740")["canonical_condition"]
    assert "局部" in by_id(data, "W08-738")["source_note"]
    assert "不将该句泛化" in by_id(data, "W08-738")["source_note"]
    assert by_id(data, "W08-713")["history_feedback"] is None


def test_jumen_temporal_sidecar_preserves_paths_without_inventing_time_triggers():
    data = load(TIME)
    assert data["counts"] == {
        "non_natal_rows": 0,
        "year": 0,
        "decade": 0,
        "path_dependent_gate_rows": 4,
        "source_age_qualifier_rows": 2,
    }
    assert data["exact_non_natal_ids"] == []
    assert data["year_ids"] == []
    assert data["decade_ids"] == []
    assert data["path_dependent_gate_ids"] == ["W08-720", "W08-721", "W08-723", "W08-725"]
    assert data["source_age_qualifier_ids"] == ["W08-719", "W08-720"]
    assert data["records"] == []
    assert data["dependent_outcome_ids"] == ["W08-720", "W08-721", "W08-723", "W08-725"]
    assert data["path_records"] and len(data["path_records"]) == 4
    assert all(record["time_layer"] == "NATAL" and record["no_numeric_generalization"] for record in data["path_records"])
    assert all(row["classification"] == "SOURCE_LIFE_STAGE_QUALIFIER_NOT_DECADE_YEAR_TRIGGER" for row in data["source_age_qualifier_records"])


def test_jumen_gap_ledger_carries_prior_gaps_without_false_closure():
    gaps = load(GAPS)
    assert gaps["gap_count"] == 0
    assert gaps["core_gap_count"] == 0
    assert gaps["gaps"] == []
    assert set(gaps["summary"]["unresolved_prior_gap_ids"]) == PRIOR_GAPS
    state = STATE.read_text(encoding="utf-8")
    assert "W05-SG-002 remains PARTIALLY_RESOLVED" in state
    for gap_id in sorted(PRIOR_GAPS - {"W05-SG-002"}):
        assert gap_id in state
    assert "source_coverage_gaps_remaining: 6" in state


def test_jumen_state_and_summary_counts_reconcile_and_prior_source_is_preserved():
    data = load(SOURCE)
    state = STATE.read_text(encoding="utf-8")
    assert "merged_rule_count: 642" in state
    assert "current_batch_rule_count: 42" in state
    assert "source_first_records_added_current_batch: 42" in state
    assert "source_uncertainty_count_current_batch: 0" in state
    assert "path_dependent_gate_count_current_batch: 4" in state
    assert "source_coverage_gap_count_current_batch: 0" in state
    assert "source_coverage_gaps_remaining: 6" in state
    assert "11 天相" in state
    assert "Issue #737" in SUMMARY.read_text(encoding="utf-8")
    assert "W08-701…W08-742" in SUMMARY.read_text(encoding="utf-8")
    previous = load(PREVIOUS_TANLANG)
    assert by_id(previous, "W06-596")["canonical_promotion"] is False
    assert "W06-SG-005" in previous["source_basis"]["note"] or "风流采杖" in by_id(previous, "W06-596")["source_digest"]
    assert data["summary"]["unresolved_prior_gap_ids"] == sorted(PRIOR_GAPS) or set(data["summary"]["unresolved_prior_gap_ids"]) == PRIOR_GAPS

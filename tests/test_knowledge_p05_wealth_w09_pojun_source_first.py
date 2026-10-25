import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "knowledge/palaces/P05_wealth/w09"
STATE = ROOT / "knowledge/states/P05_WEALTH_STATE.yaml"
SOURCE = BASE / "WEALTH_W09_POJUN_SOURCE_READJUDICATION_P91_P92_v0.1.json"
TIME = BASE / "WEALTH_W09_POJUN_SOURCE_TIME_SCOPE_P91_P92_v0.1.json"
GAPS = BASE / "WEALTH_W09_POJUN_SOURCE_GAPS_P91_P92_v0.1.json"
SUMMARY = BASE / "WEALTH_W09_POJUN_CANONICAL_SUMMARY_P91_P92_v0.1.md"
PRIOR_GAPS = {"W05-SG-002", "W06-SG-001", "W06-SG-002", "W06-SG-003", "W06-SG-004", "W06-SG-005", "W08-SG-001", "W08-SG-002", "W08-SG-003", "W08-SG-004", "W08-SG-005", *{f"W09-SG-{i:03d}" for i in range(6, 15)}}


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def row(data, rid):
    return next(r for r in data["records"] if r["projection_rule_id"] == rid)


def test_source_hash_boundary_and_candidate_census():
    data = load(SOURCE)
    ids = [r["projection_rule_id"] for r in data["records"]]
    expected = [f"W09-{i}" for i in range(889, 901)] + [f"W09-{i}" for i in range(905, 923)]
    assert data["issue"] == 770
    assert data["source_basis"]["sha256"] == "6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c"
    assert "91–92" in data["source_basis"]["printed_pages"]
    assert "14 破军" in data["source_basis"]["printed_pages"]
    assert "疾厄宫" in data["source_basis"]["printed_pages"]
    assert ids == expected and len(ids) == len(set(ids)) == 30
    assert data["summary"]["historical_candidates_reviewed"] == 12
    assert data["summary"]["new_source_atoms_reviewed"] == 18
    assert data["summary"]["new_source_supported_atoms"] == 17
    assert data["summary"]["canonical_promotions"] == 29
    assert data["summary"]["cumulative_canonical_records_after_merge"] == 765 + data["summary"]["canonical_promotions"]
    assert data["summary"]["candidate_condition_or_scope_correction_ids"] == ["W09-897", "W09-900"]
    assert not any(f"W09-{i}" in ids for i in range(901, 905))


def test_uncertain_source_conditions_are_not_promoted():
    data = load(SOURCE)
    assert {r["projection_rule_id"] for r in data["records"] if not r["canonical_promotion"]} == {"W09-909"}
    assert row(data, "W09-909")["source_uncertainty"]
    assert "同破财损耗极大" in row(data, "W09-909")["source_digest"]
    assert row(data, "W09-917")["canonical_promotion"] is True
    assert "纵会占化吉曜者亦然" in row(data, "W09-917")["source_digest"]
    assert "W09-SG-016" in row(data, "W09-917")["source_note"]


def test_literal_source_anomalies_and_clear_subclauses_are_scoped():
    data = load(SOURCE)
    gaps = load(GAPS)
    assert "W09-SG-015" in row(data, "W09-909")["source_note"]
    assert "而且往往功败垂成" in row(data, "W09-910")["source_digest"]
    assert "纵会占化吉曜者亦然" in row(data, "W09-917")["source_note"]
    assert gaps["gap_count"] == 2 and gaps["core_gap_count"] == 0
    assert {g["gap_id"] for g in gaps["gaps"]} == {"W09-SG-015", "W09-SG-016"}
    assert all(g["status"] == "OPEN" and g["core_gap"] is False for g in gaps["gaps"])
    assert gaps["summary"]["unresolved_prior_gap_ids"] == sorted(PRIOR_GAPS)


def test_time_scope_does_not_invent_decade_or_year_triggers():
    time = load(TIME)
    assert time["counts"] == {
        "non_natal_rows": 0,
        "year": 0,
        "decade": 0,
        "path_dependent_gate_rows": 9,
        "source_time_phrase_rows": 1,
        "source_life_course_qualifier_rows": 1,
        "source_condition_qualifier_rows": 1,
    }
    assert time["exact_non_natal_ids"] == []
    assert time["decade_ids"] == [] and time["year_ids"] == []
    assert time["path_dependent_gate_ids"] == ["W09-895", "W09-900", "W09-906", "W09-908", "W09-910", "W09-913", "W09-916", "W09-917", "W09-919"]
    assert time["source_time_phrase_records"][0]["projection_rule_id"] == "W09-919"
    assert time["source_time_phrase_records"][0]["source_time_phrase"] == "大运流年"
    assert time["source_time_phrase_records"][0]["scope_status"] == "TIMING_ADVICE_NOT_EVENT_TRIGGER"
    assert time["source_life_course_qualifier_ids"] == ["W09-918"]
    assert time["source_condition_qualifier_ids"] == ["W09-915"]


def test_prior_qisha_and_tianliang_artifacts_remain_immutable():
    qisha = load(BASE / "WEALTH_W09_QISHA_SOURCE_READJUDICATION_P90_P91_v0.1.json")
    tianliang = load(ROOT / "knowledge/palaces/P05_wealth/w08/WEALTH_W08_TIANLIANG_SOURCE_READJUDICATION_P88_P90_v0.1.json")
    data = load(SOURCE)
    assert qisha["issue"] == 765 and len(qisha["records"]) == 48
    assert qisha["summary"]["canonical_promotions"] == 44
    assert qisha["summary"]["cumulative_canonical_records_after_merge"] == 765
    assert tianliang["issue"] == 760 and len(tianliang["records"]) == 38
    assert tianliang["summary"]["canonical_promotions"] == 37
    assert tianliang["summary"]["cumulative_canonical_records_after_merge"] == 721
    assert data["summary"]["cumulative_canonical_records_after_merge"] == 765 + data["summary"]["canonical_promotions"]
    assert "疾厄宫" in SUMMARY.read_text(encoding="utf-8")


def test_state_cache_tracks_active_pojun_and_inherited_gaps():
    state = STATE.read_text(encoding="utf-8")
    assert 'status: "ACTIVE"' in state
    assert "active_issue: 770" in state
    assert 'active_branch: "knowledge/p05-770-source-first-pojun-p91-p92"' in state
    assert "active_pr: 771" in state
    assert "merged_rule_count: 765" in state
    assert "current_batch_rule_count: 29" in state
    assert "source_first_records_added_current_batch: 30" in state
    assert "source_uncertainty_count_current_batch: 2" in state
    assert "path_dependent_gate_count_current_batch: 9" in state
    assert "source_coverage_gap_count_current_batch: 2" in state
    assert "source_coverage_gaps_remaining: 22" in state
    assert all(g in state for g in PRIOR_GAPS)
    assert "No Product/runtime authorization is implied" in state

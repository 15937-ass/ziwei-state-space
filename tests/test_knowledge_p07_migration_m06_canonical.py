import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READJ = ROOT / "knowledge/palaces/P07_migration/wp05/MIGRATION_M06_SOURCE_READJUDICATION_090_v0.1.json"
TIME = ROOT / "knowledge/palaces/P07_migration/wp05/MIGRATION_M06_SOURCE_TIME_SCOPE_v0.1.json"
STATE = ROOT / "knowledge/states/P07_MIGRATION_STATE.yaml"

EXPECTED_CASE_ONLY = {
    "M06-521", "M06-522", "M06-523", "M06-529", "M06-530", "M06-531",
    "M06-542", "M06-560", "M06-572", "M06-579", "M06-580", "M06-583", "M06-586",
}


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_m06_census_and_unique_ids():
    data = load(READJ)
    ids = [r["projection_rule_id"] for r in data["records"]]
    assert data["summary"]["reviewed"] == 90
    assert data["summary"]["canonical_promoted"] == 90
    assert ids == [f"M06-{n}" for n in range(501, 591)]
    assert len(set(ids)) == 90
    assert data["summary"]["source_condition_normalization_count"] == 90
    assert all(r["source_condition_normalized"] for r in data["records"])
    assert all("前格" not in r["canonical_condition"] for r in data["records"])
    rows = {r["projection_rule_id"]: r for r in data["records"]}
    assert rows["M06-557"]["canonical_condition"].endswith("不与羊陀分支混并。")
    assert rows["M06-506"]["archived_projection_mode"] == "SCENE_TRANSLATION"
    assert rows["M06-506"]["projection_mode"] == "FUNCTIONAL_PROJECTION"
    assert data["summary"]["source_resolution_change_count"] == 31


def test_m06_source_pages_are_reconciled():
    data = load(READJ)
    rows = {r["projection_rule_id"]: r for r in data["records"]}
    for n in range(501, 519):
        assert rows[f"M06-{n}"]["source_location"] == "SRC-ZZ-003 printed p119"
    for n in range(519, 579):
        assert rows[f"M06-{n}"]["source_location"] == "SRC-ZZ-003 printed p120"
    for n in range(579, 590):
        assert rows[f"M06-{n}"]["source_location"] == "SRC-ZZ-003 printed p121"
    assert rows["M06-590"]["source_location"] == "SRC-ZZ-003 printed p122"
    changed = [r["projection_rule_id"] for r in data["records"] if r["source_span_changed"]]
    assert len(changed) == 33
    assert data["summary"]["source_span_changed_count"] == 33


def test_m06_case_only_reasons_are_row_level():
    data = load(READJ)
    actual = {r["projection_rule_id"] for r in data["records"] if r["case_support_only"]}
    assert actual == EXPECTED_CASE_ONLY
    for r in data["records"]:
        if r["case_support_only"]:
            assert r["case_support_reason"]
        else:
            assert r["case_support_reason"] is None
    assert data["summary"]["reusable_projection_rules"] == 77
    assert data["summary"]["case_support_only"] == 13


def test_historical_gate_is_not_promoted_to_history_feedback():
    data = load(READJ)
    rows = {r["projection_rule_id"]: r for r in data["records"]}
    assert rows["M06-579"]["archived_history_feedback"] == "PATH_DEPENDENT_GATE"
    assert rows["M06-579"]["history_feedback"] is None
    assert rows["M06-579"]["path_dependent_gate_reclassified"] is True
    assert rows["M06-579"]["source_sequence_not_history_gate"] is True
    assert rows["M06-580"]["source_sequence_not_history_gate"] is True
    assert data["summary"]["canonical_path_dependent_gate_rows"] == []
    assert data["summary"]["canonical_history_feedback_rows"] == 0
    assert rows["M06-579"]["case_support_only"] and rows["M06-580"]["case_support_only"]


def test_m06_temporal_scope_is_bounded():
    readj = load(READJ)
    time = load(TIME)
    assert time["source_basis"]["printed_pages"] == "119–122"
    assert time["chapter_scope"]["source_layers"] == ["NATAL", "DECADE", "YEAR", "MONTH"]
    assert time["event_relative_overlay"]["overlay_id"] == "MIGRATION_FIRST_THREE_YEARS"
    assert time["event_relative_overlay"]["human_gate"] == "HG-P07-TEMPORAL-01-A"
    assert time["event_relative_overlay"]["seventh_calendar_layer"] is False
    assert time["event_relative_overlay"]["generic_event_timer"] is False
    time_rows = {r["projection_rule_id"]: r for r in time["records"]}
    for n in range(501, 591):
        expected = ["YEAR"] if n in (540, 541, 542) else ["NATAL"]
        assert time_rows[f"M06-{n}"]["source_time_layers"] == expected
        assert time_rows[f"M06-{n}"]["runtime_eligibility_granted"] is False
    assert time["path_dependent_gate_audit"]["history_feedback_rows"] == 0
    assert time["quantitative_semantics"] == {"new_time_scale": 0, "weight": 0, "probability": 0, "decay": 0}
    assert readj["temporal_and_governance_boundary"]["product_runtime_authorized"] is False


def test_residual_p07_gaps_remain_open():
    data = load(READJ)
    gap_ids = {g["gap_id"] for g in data["source_coverage_gaps"]}
    assert {
        "P07-M05-GAP-001", "P07-M05-GAP-002", "P07-M05-GAP-003", "P07-M05-GAP-004",
        "P07-M03-GAP-001", "P07-M03-GAP-012",
    } <= gap_ids
    assert "not yet fully source-closed" in data["source_coverage_note"]

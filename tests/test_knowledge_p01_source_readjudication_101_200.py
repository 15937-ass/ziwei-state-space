import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "knowledge" / "palaces" / "P01_life" / "wp05"


def _rows():
    with (BASE / "LIFE_P02_SOURCE_READJUDICATION_101_200_v0.1.csv").open(
        encoding="utf-8", newline=""
    ) as f:
        return list(csv.DictReader(f))


def test_life_101_200_census_and_ids():
    rows = _rows()
    assert len(rows) == 100
    expected = [f"P02-{i:03d}" for i in range(101, 201)]
    assert [r["projection_rule_id"] for r in rows] == expected
    assert len({r["projection_rule_id"] for r in rows}) == 100
    assert all(r["source_id"] == "SRC-ZZ-003" for r in rows)
    assert all(r["canonical_promotion"] == "true" for r in rows)


def test_life_101_200_case_support_boundary():
    rows = _rows()
    case_ids = {
        r["projection_rule_id"] for r in rows if r["case_support_only"] == "true"
    }
    assert len(case_ids) == 30
    assert {
        "P02-113",
        "P02-135",
        "P02-137",
        "P02-153",
        "P02-186",
    } <= case_ids
    assert {r["projection_rule_id"] for r in rows if r["case_support_only"] == ""} == set()


def test_life_101_200_source_repairs():
    by_id = {r["projection_rule_id"]: r for r in _rows()}
    assert by_id["P02-125"]["cross_palace_dependency"] == ""
    assert by_id["P02-130"]["cross_palace_dependency"] == ""
    assert by_id["P02-164"]["case_support_only"] == "false"
    assert by_id["P02-190"]["opposite_palace_dependency"] == "对宫天马"
    assert by_id["P02-190"]["cross_palace_dependency"] == ""
    assert by_id["P02-199"]["cross_palace_dependency"] == "兄弟宫"
    assert "多是非动荡" in by_id["P02-200"]["source_literal_claim"]
    assert by_id["P02-112"]["source_text_uncertainty"]
    assert by_id["P02-164"]["source_text_uncertainty"]
    assert by_id["P02-182"]["source_text_uncertainty"]
    assert by_id["P02-170"]["history_dependency"].startswith(
        "EXISTING_HISTORY_SCHEMA_"
    )


def test_life_101_200_time_scope_sidecar():
    data = json.loads(
        (BASE / "LIFE_P02_SOURCE_TIME_SCOPE_v0.1.json").read_text(
            encoding="utf-8"
        )
    )
    records = data["records"]
    assert len(records) == 100
    by_id = {r["projection_rule_id"]: r for r in records}

    assert by_id["P02-148"]["source_time_layers"] == []
    assert by_id["P02-148"]["scope_status"] == "SOURCE_GENERIC_PERIOD_NOT_NARROWED"
    assert by_id["P02-168"]["source_time_layers"] == []
    assert by_id["P02-168"]["scope_status"] == "SOURCE_LIFE_HINGE_LAYER_UNSPECIFIED"
    assert by_id["P02-170"]["source_time_layers"] == []
    assert by_id["P02-170"]["scope_status"] == "SOURCE_CROSS_PERIOD_GENERIC_STAGE"
    assert by_id["P02-147"]["source_time_layers"] == ["NATAL", "DECADE", "YEAR"]
    assert by_id["P02-138"]["scope_status"] == (
        "SOURCE_LIFE_STAGE_SEQUENCE_NOT_NEW_TIME_PRIMITIVE"
    )


def test_life_101_200_summary_and_boundaries():
    data = json.loads(
        (
            BASE / "LIFE_P02_SOURCE_READJUDICATION_SUMMARY_v0.1.json"
        ).read_text(encoding="utf-8")
    )
    s = data["summary"]
    assert s["reviewed"] == 100
    assert s["canonical_promoted"] == 100
    assert s["reusable_projection_rules"] == 70
    assert s["case_support_only"] == 30
    assert s["cumulative_canonical_records_after_merge"] == 200
    assert s["cumulative_reusable_projection_rules_after_merge"] == 149
    assert s["cumulative_case_support_only_after_merge"] == 51
    assert s["new_primitive_qi"] == 0
    assert s["new_memory_type"] == 0
    assert s["numeric_weight"] == 0
    assert s["probability"] == 0
    assert len(data["source_coverage_gaps_next_checkpoint"]) == 18
    assert data["shared_semantic_gaps"] == []
    assert data["human_gate_required"] is False

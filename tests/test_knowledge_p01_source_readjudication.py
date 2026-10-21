import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "knowledge" / "palaces" / "P01_life" / "wp05"


def _rows():
    with (BASE / "LIFE_P01_SOURCE_READJUDICATION_100_v0.1.csv").open(
        encoding="utf-8", newline=""
    ) as f:
        return list(csv.DictReader(f))


def test_p01_source_readjudication_census():
    rows = _rows()
    assert len(rows) == 100
    expected = [f"P01-{i:03d}" for i in range(1, 101)]
    assert [r["projection_rule_id"] for r in rows] == expected
    assert len({r["projection_rule_id"] for r in rows}) == 100
    assert all(r["source_id"] == "SRC-ZZ-003" for r in rows)
    assert all(r["canonical_promotion"] == "true" for r in rows)


def test_p01_case_support_boundary_preserved():
    rows = _rows()
    case_ids = {
        r["projection_rule_id"] for r in rows if r["case_support_only"] == "true"
    }
    assert len(case_ids) == 21
    assert {
        "P01-052",
        "P01-053",
        "P01-072",
        "P01-073",
        "P01-094",
        "P01-098",
    } <= case_ids


def test_p01_source_repairs_are_fail_closed():
    by_id = {r["projection_rule_id"]: r for r in _rows()}
    assert "运限或流年" in by_id["P01-007"]["canonical_condition"]
    assert "大运或流年" in by_id["P01-049"]["canonical_condition"]
    assert by_id["P01-054"]["cross_palace_dependency"] == ""
    assert by_id["P01-055"]["cross_palace_dependency"] == ""
    assert "武越破军" in by_id["P01-046"]["canonical_condition"]
    assert by_id["P01-046"]["source_text_uncertainty"]
    assert by_id["P01-017"]["source_text_uncertainty"]
    assert by_id["P01-056"]["history_dependency"].startswith(
        "EXISTING_HISTORY_SCHEMA_"
    )


def test_p01_time_scope_sidecar():
    data = json.loads(
        (BASE / "LIFE_P01_SOURCE_TIME_SCOPE_v0.1.json").read_text(encoding="utf-8")
    )
    records = data["records"]
    assert len(records) == 100
    by_id = {r["projection_rule_id"]: r for r in records}
    assert by_id["P01-007"]["source_time_layers"] == ["DECADE", "YEAR"]
    assert by_id["P01-049"]["source_time_layers"] == ["DECADE", "YEAR"]
    assert by_id["P01-010"]["source_time_layers"] == []
    assert (
        by_id["P01-010"]["scope_status"]
        == "SOURCE_GENERIC_PERIOD_NOT_NARROWED"
    )
    assert (
        by_id["P01-056"]["scope_status"]
        == "SOURCE_EXPLICIT_NEXT_PERIOD_DEPENDENCY"
    )
    assert "specific_next_period" in by_id["P01-056"]["dependencies"][0]


def test_p01_summary_boundaries():
    data = json.loads(
        (
            BASE
            / "LIFE_P01_SOURCE_READJUDICATION_SUMMARY_v0.1.json"
        ).read_text(encoding="utf-8")
    )
    s = data["summary"]
    assert s["reviewed"] == 100
    assert s["canonical_promoted"] == 100
    assert s["reusable_projection_rules"] == 79
    assert s["case_support_only"] == 21
    assert s["new_primitive_qi"] == 0
    assert s["new_memory_type"] == 0
    assert s["numeric_weight"] == 0
    assert s["probability"] == 0
    assert len(data["source_coverage_gaps_next_checkpoint"]) >= 3
    assert data["shared_semantic_gaps"] == []
    assert data["human_gate_required"] is False

from pathlib import Path

import pytest

from src.product.wealth_pilot import (
    build_w01_coverage_ledger,
    compile_wealth_pilot,
    load_pilot_registry,
    load_projection_rows,
    run_wealth_pilot,
    summarize_ledger,
)

ROOT = Path(__file__).resolve().parents[1]
W01 = ROOT / "validation/wp05/W01_wealth_projection_review_001_100.csv"
REGISTRY = ROOT / "product/PL2C_WEALTH_PILOT_v0.1.json"


def _star(name, mutagen=None):
    return {
        "name": name,
        "brightness": None,
        "mutagen": mutagen,
        "type": None,
        "scope": None,
    }


def _snapshot(wealth_stars):
    palaces = {}
    for i in range(11):
        palaces[f"测试宫{i}"] = {
            "stem": "甲",
            "branch": "子",
            "is_body_palace": False,
            "major_stars": [],
            "minor_stars": [],
            "adjective_stars": [],
        }
    palaces["财帛"] = {
        "stem": "乙",
        "branch": "丑",
        "is_body_palace": False,
        "major_stars": wealth_stars,
        "minor_stars": [],
        "adjective_stars": [],
    }
    return {
        "schema_version": "0.1",
        "engine": {"name": "test", "version": "1", "adapter_version": "0.1"},
        "input": {"solar_date": "2000-01-01"},
        "chart": {"palaces": palaces},
    }


def test_registry_compiles_exactly_13_rules():
    rows = load_projection_rows(W01)
    registry = load_pilot_registry(REGISTRY)
    report = compile_wealth_pilot(rows, registry)
    assert report.issues == ()
    assert len(report.executable) == 13
    assert [r.rule_id for r in report.executable] == sorted(registry["rules"])


def test_w01_coverage_is_bounded_not_auto_promoted():
    rows = load_projection_rows(W01)
    registry = load_pilot_registry(REGISTRY)
    summary = summarize_ledger(build_w01_coverage_ledger(rows, registry))
    assert summary == {
        "EXECUTABLE": 13,
        "NORMALIZATION_PENDING": 87,
        "PATH_DEPENDENT_HOLD": 0,
        "EXCLUDED": 0,
    }


def test_canonical_source_drift_fails_closed():
    rows = load_projection_rows(W01)
    registry = load_pilot_registry(REGISTRY)
    changed = [dict(row) for row in rows]
    row = next(item for item in changed if item["projection_rule_id"] == "W01-025")
    row["condition"] = "被意外改写"
    with pytest.raises(ValueError, match="canonical source drift"):
        compile_wealth_pilot(changed, registry)


def test_snapshot_activates_literal_wealth_rules():
    rows = load_projection_rows(W01)
    registry = load_pilot_registry(REGISTRY)
    graph = run_wealth_pilot(
        _snapshot(
            [
                _star("武曲", "禄"),
                _star("紫微", "科"),
                _star("擎羊"),
            ]
        ),
        rows,
        registry,
    )
    active = {node.rule_id for node in graph.nodes}
    assert {
        "W01-025",
        "W01-028",
        "W01-038",
        "W01-058",
        "W01-090",
        "W01-091",
        "W01-092",
        "W01-097",
    }.issubset(active)
    assert "W01-040" not in active
    assert "W01-042" not in active


def test_lucun_without_tianma_uses_negative_condition():
    rows = load_projection_rows(W01)
    registry = load_pilot_registry(REGISTRY)

    no_tianma = run_wealth_pilot(
        _snapshot([_star("禄存")]),
        rows,
        registry,
    )
    assert "W01-026" in {node.rule_id for node in no_tianma.nodes}

    with_tianma = run_wealth_pilot(
        _snapshot([_star("禄存"), _star("天马")]),
        rows,
        registry,
    )
    assert "W01-026" not in {node.rule_id for node in with_tianma.nodes}


def test_wenqu_huaji_requires_star_specific_transformation():
    rows = load_projection_rows(W01)
    registry = load_pilot_registry(REGISTRY)

    graph = run_wealth_pilot(
        _snapshot([_star("文曲", "忌")]),
        rows,
        registry,
    )
    active = {node.rule_id for node in graph.nodes}
    assert "W01-040" in active
    assert "W01-042" in active

    other_ji = run_wealth_pilot(
        _snapshot([_star("武曲", "忌")]),
        rows,
        registry,
    )
    active = {node.rule_id for node in other_ji.nodes}
    assert "W01-040" in active
    assert "W01-042" not in active

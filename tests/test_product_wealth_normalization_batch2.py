from pathlib import Path

import pytest

from src.product.wealth_pilot import (
    build_w01_coverage_ledger,
    build_wealth_structure_report,
    compose_wealth_registries,
    compile_wealth_pilot,
    load_pilot_registry,
    load_projection_rows,
    run_wealth_pilot,
    summarize_ledger,
)
from src.product.wealth_semantics import (
    compose_wealth_semantic_registries,
    load_wealth_semantic_overlay,
    load_wealth_semantic_registry,
)

ROOT = Path(__file__).resolve().parents[1]
W01 = ROOT / "validation/wp05/W01_wealth_projection_review_001_100.csv"
B01 = ROOT / "product/PL2C_WEALTH_PILOT_v0.1.json"
B02 = ROOT / "product/PL2F_WEALTH_NORMALIZATION_BATCH2_v0.1.json"
SEM_BASE = ROOT / "product/PL2E_WEALTH_SEMANTIC_REGISTRY_v0.1.json"
SEM_B02 = ROOT / "product/PL2F_WEALTH_SEMANTIC_BATCH2_v0.1.json"


def _star(name, mutagen=None):
    return {
        "name": name,
        "brightness": None,
        "mutagen": mutagen,
        "type": None,
        "scope": None,
    }


def _snapshot(stars):
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
        "major_stars": stars,
        "minor_stars": [],
        "adjective_stars": [],
    }
    return {
        "schema_version": "0.1",
        "engine": {"name": "test", "version": "1", "adapter_version": "0.1"},
        "input": {"solar_date": "2000-01-01"},
        "chart": {"palaces": palaces},
    }


def _load():
    rows = load_projection_rows(W01)
    registry = compose_wealth_registries(
        load_pilot_registry(B01),
        load_pilot_registry(B02),
    )
    semantic = compose_wealth_semantic_registries(
        load_wealth_semantic_registry(SEM_BASE),
        load_wealth_semantic_overlay(SEM_B02),
    )
    return rows, registry, semantic


def test_batch2_expands_executable_coverage_to_22():
    rows, registry, _ = _load()
    report = compile_wealth_pilot(rows, registry)
    assert report.issues == ()
    assert len(report.executable) == 22
    assert summarize_ledger(build_w01_coverage_ledger(rows, registry)) == {
        "EXECUTABLE": 22,
        "NORMALIZATION_PENDING": 78,
        "PATH_DEPENDENT_HOLD": 0,
        "EXCLUDED": 0,
    }


def test_transformation_and_named_pair_aliases_are_explicit():
    rows, registry, _ = _load()
    graph = run_wealth_pilot(
        _snapshot([
            _star("武曲", "权"),
            _star("文昌", "科"),
            _star("天魁"),
            _star("火星"),
        ]),
        rows,
        registry,
    )
    active = {node.rule_id for node in graph.nodes}
    assert {"W01-037", "W01-039", "W01-047", "W01-048", "W01-049", "W01-066"}.issubset(active)


def test_w01_061_negative_fire_bell_gate_is_fail_closed():
    rows, registry, _ = _load()
    base = [_star("擎羊"), _star("廉贞"), _star("贪狼")]

    graph = run_wealth_pilot(_snapshot(base), rows, registry)
    assert "W01-061" in {node.rule_id for node in graph.nodes}

    blocked = run_wealth_pilot(_snapshot(base + [_star("铃星")]), rows, registry)
    assert "W01-061" not in {node.rule_id for node in blocked.nodes}


def test_tianfu_shared_trigger_adds_structural_boundary():
    rows, registry, _ = _load()
    graph = run_wealth_pilot(_snapshot([_star("天府")]), rows, registry)
    active = {node.rule_id for node in graph.nodes}
    assert "W01-031" in active
    assert "W01-032" in active


def test_semantic_report_gains_effort_and_reputation_sections():
    rows, registry, semantic = _load()
    report = build_wealth_structure_report(
        _snapshot([_star("文昌", "科"), _star("火星")]),
        rows,
        registry,
        semantic,
    )
    sections = {section.section_id for section in report.sections}
    assert "earning_mode" in sections
    assert "reputation_income" in sections
    assert "effort" in sections
    assert report.coverage["EXECUTABLE"] == 22
    assert report.coverage["NORMALIZATION_PENDING"] == 78
    assert report.confidence_band == "LOW_CONFIDENCE"


def test_duplicate_batch_rule_is_rejected():
    base = load_pilot_registry(B01)
    with pytest.raises(ValueError, match="duplicate executable wealth rule"):
        compose_wealth_registries(base, base)

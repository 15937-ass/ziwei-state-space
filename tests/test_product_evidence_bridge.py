from pathlib import Path

from src.product.evidence_package import ConfidenceBand
from src.product.wealth_pilot import (
    build_wealth_evidence_package,
    load_pilot_registry,
    load_projection_rows,
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


def test_bridge_builds_traceable_low_confidence_package():
    rows = load_projection_rows(W01)
    registry = load_pilot_registry(REGISTRY)
    package = build_wealth_evidence_package(
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

    active = {item.rule_id for item in package.active_rules}
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
    assert package.coverage == {
        "EXECUTABLE": 13,
        "NORMALIZATION_PENDING": 87,
        "PATH_DEPENDENT_HOLD": 0,
        "EXCLUDED": 0,
    }
    assert package.confidence_band is ConfidenceBand.LOW_CONFIDENCE
    assert package.confidence_rationale == (
        "bounded_executable_coverage_with_unresolved_rules"
    )
    assert all(
        item.review_status == "SOURCE_SPAN_VERIFIED"
        for item in package.active_rules
    )
    assert all(item.source_id == "SRC-ZZ-003" for item in package.active_rules)


def test_no_active_rule_is_insufficient_evidence():
    rows = load_projection_rows(W01)
    registry = load_pilot_registry(REGISTRY)
    package = build_wealth_evidence_package(_snapshot([]), rows, registry)
    assert package.active_rules == []
    assert package.confidence_band is ConfidenceBand.INSUFFICIENT_EVIDENCE
    assert package.confidence_rationale == "no_executable_rule_activated"


def test_contrastive_exposes_negative_gate_without_predicting():
    rows = load_projection_rows(W01)
    registry = load_pilot_registry(REGISTRY)
    package = build_wealth_evidence_package(
        _snapshot([_star("禄存"), _star("天马")]),
        rows,
        registry,
    )

    item = next(x for x in package.contrastive if x.rule_id == "W01-026")
    assert item.missing_all_of == ()
    assert item.unsatisfied_any_of == ()
    assert len(item.blocked_by) == 1
    assert "天马" in item.blocked_by[0]


def test_evidence_package_is_deterministic():
    rows = load_projection_rows(W01)
    registry = load_pilot_registry(REGISTRY)
    snapshot = _snapshot([_star("文曲", "忌"), _star("太阴")])
    a = build_wealth_evidence_package(snapshot, rows, registry).to_dict()
    b = build_wealth_evidence_package(snapshot, rows, registry).to_dict()
    assert a == b

from pathlib import Path

import pytest

from src.product.wealth_pilot import (
    build_wealth_evidence_package,
    build_wealth_structure_report,
    load_pilot_registry,
    load_projection_rows,
)
from src.product.wealth_semantics import (
    aggregate_wealth_evidence,
    load_wealth_semantic_registry,
    render_wealth_structure_report,
)

ROOT = Path(__file__).resolve().parents[1]
W01 = ROOT / "validation/wp05/W01_wealth_projection_review_001_100.csv"
PILOT = ROOT / "product/PL2C_WEALTH_PILOT_v0.1.json"
SEMANTIC = ROOT / "product/PL2E_WEALTH_SEMANTIC_REGISTRY_v0.1.json"


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
    return (
        load_projection_rows(W01),
        load_pilot_registry(PILOT),
        load_wealth_semantic_registry(SEMANTIC),
    )


def test_semantic_report_groups_active_rules_by_source_supported_dimensions():
    rows, pilot, semantic = _load()
    report = build_wealth_structure_report(
        _snapshot([_star("武曲", "禄"), _star("紫微", "科"), _star("擎羊")]),
        rows,
        pilot,
        semantic,
    )
    sections = {section.section_id: section for section in report.sections}

    assert "acquisition" in sections
    assert "earning_mode" in sections
    assert "flow" in sections
    assert "retention" in sections
    assert "risk_competition" in sections
    assert "structural_interpretation" in sections

    active = {
        finding.rule_id
        for section in report.sections
        for finding in section.findings
    }
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


def test_report_preserves_low_confidence_and_no_scalar_score():
    rows, pilot, semantic = _load()
    report = build_wealth_structure_report(
        _snapshot([_star("武曲", "禄")]),
        rows,
        pilot,
        semantic,
    )
    payload = report.to_dict()
    assert payload["confidence_band"] == "LOW_CONFIDENCE"
    assert payload["coverage"]["NORMALIZATION_PENDING"] == 87
    assert "score" not in payload
    assert any("不计算单一财富分数" in item for item in payload["limitations"])


def test_shared_trigger_group_is_structural_not_conflict():
    rows, pilot, semantic = _load()
    report = build_wealth_structure_report(
        _snapshot([_star("紫微")]),
        rows,
        pilot,
        semantic,
    )
    groups = [set(group.rule_ids) for group in report.shared_trigger_groups]
    assert {"W01-090", "W01-091", "W01-092"} in groups
    assert report.conflicts == ()


def test_renderer_is_deterministic_and_contains_provenance():
    rows, pilot, semantic = _load()
    report = build_wealth_structure_report(
        _snapshot([_star("文曲", "忌"), _star("太阴")]),
        rows,
        pilot,
        semantic,
    )
    a = render_wealth_structure_report(report)
    b = render_wealth_structure_report(report)
    assert a == b
    assert "W01-042" in a
    assert "SRC-ZZ-003::财帛宫printed_p70" in a
    assert "【损失与竞争风险】" in a


def test_unknown_active_rule_fails_closed():
    rows, pilot, semantic = _load()
    package = build_wealth_evidence_package(
        _snapshot([_star("武曲")]),
        rows,
        pilot,
    )
    altered = dict(semantic)
    altered["rules"] = dict(semantic["rules"])
    altered["rules"].pop("W01-028")
    with pytest.raises(ValueError, match="active rule missing"):
        aggregate_wealth_evidence(package, altered)

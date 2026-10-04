from pathlib import Path

import pytest

from src.product.palace_structure import load_palace_ontology
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
B03 = ROOT / "product/PL2H_WEALTH_CROSS_PALACE_BATCH_v0.1.json"
SEM_BASE = ROOT / "product/PL2E_WEALTH_SEMANTIC_REGISTRY_v0.1.json"
SEM_B02 = ROOT / "product/PL2F_WEALTH_SEMANTIC_BATCH2_v0.1.json"
SEM_B03 = ROOT / "product/PL2H_WEALTH_SEMANTIC_BATCH3_v0.1.json"
ONTOLOGY = ROOT / "knowledge/wp05/palace_ontology_v0.1.csv"

BRANCH = {
    "命宫": "酉",
    "兄弟宫": "戌",
    "夫妻宫": "未",
    "子女宫": "申",
    "财帛宫": "巳",
    "疾厄宫": "午",
    "迁移宫": "卯",
    "交友宫": "辰",
    "事业宫": "丑",
    "田宅宫": "寅",
    "福德宫": "亥",
    "父母宫": "子",
}


def _star(name, mutagen=None):
    return {
        "name": name,
        "brightness": None,
        "mutagen": mutagen,
        "type": None,
        "scope": None,
    }


def _snapshot(stars_by_palace=None):
    stars_by_palace = stars_by_palace or {}
    palaces = {}
    for palace_name, branch in BRANCH.items():
        palaces[branch] = {
            "name": palace_name[:-1],
            "stem": "甲",
            "branch": branch,
            "is_body_palace": False,
            "major_stars": list(stars_by_palace.get(palace_name, [])),
            "minor_stars": [],
            "adjective_stars": [],
        }
    return {
        "schema_version": "0.2",
        "engine": {"name": "test", "version": "1", "adapter_version": "0.2"},
        "input": {},
        "natal": {"palaces": palaces},
    }


def _load():
    rows = load_projection_rows(W01)
    executable = compose_wealth_registries(
        load_pilot_registry(B01),
        load_pilot_registry(B02),
        load_pilot_registry(B03),
    )
    semantic = compose_wealth_semantic_registries(
        load_wealth_semantic_registry(SEM_BASE),
        load_wealth_semantic_overlay(SEM_B02),
        load_wealth_semantic_overlay(SEM_B03),
    )
    ontology = load_palace_ontology(ONTOLOGY)
    return rows, executable, semantic, ontology


def test_cross_palace_batch_expands_w01_to_28_executable():
    rows, executable, _, _ = _load()
    report = compile_wealth_pilot(rows, executable)
    assert report.issues == ()
    assert len(report.executable) == 28
    assert summarize_ledger(build_w01_coverage_ledger(rows, executable)) == {
        "EXECUTABLE": 28,
        "NORMALIZATION_PENDING": 72,
        "PATH_DEPENDENT_HOLD": 0,
        "EXCLUDED": 0,
    }
    assert executable["requires_palace_structure"] is True


def test_structure_dependency_fails_closed_when_ontology_missing():
    rows, executable, _, _ = _load()
    with pytest.raises(ValueError, match="requires PL2-G palace structure"):
        run_wealth_pilot(_snapshot(), rows, executable)


def test_topology_boundary_rules_activate_from_approved_ontology():
    rows, executable, _, ontology = _load()
    graph = run_wealth_pilot(
        _snapshot(),
        rows,
        executable,
        palace_ontology=ontology,
    )
    active = {node.rule_id for node in graph.nodes}
    assert "W01-001" in active
    assert "W01-013" in active


def test_w01_006_requires_both_wealth_and_fortune_conditions():
    rows, executable, _, ontology = _load()
    snapshot = _snapshot(
        {
            "财帛宫": [_star("武曲", "忌"), _star("七杀")],
            "福德宫": [_star("天府", "科")],
        }
    )
    graph = run_wealth_pilot(
        snapshot, rows, executable, palace_ontology=ontology
    )
    assert "W01-006" in {node.rule_id for node in graph.nodes}

    missing_ke = _snapshot(
        {
            "财帛宫": [_star("武曲", "忌"), _star("七杀")],
            "福德宫": [_star("天府")],
        }
    )
    graph = run_wealth_pilot(
        missing_ke, rows, executable, palace_ontology=ontology
    )
    assert "W01-006" not in {node.rule_id for node in graph.nodes}


def test_w01_014_uses_branch_star_and_triad_structure():
    rows, executable, _, ontology = _load()
    snapshot = _snapshot(
        {
            "财帛宫": [_star("太阳")],
            "事业宫": [_star("天梁")],
        }
    )
    graph = run_wealth_pilot(
        snapshot, rows, executable, palace_ontology=ontology
    )
    assert "W01-014" in {node.rule_id for node in graph.nodes}


def test_w01_083_requires_tianyao_yinsha_and_context_relations():
    rows, executable, _, ontology = _load()
    graph = run_wealth_pilot(
        _snapshot({"财帛宫": [_star("天姚"), _star("阴煞")]}),
        rows,
        executable,
        palace_ontology=ontology,
    )
    assert "W01-083" in {node.rule_id for node in graph.nodes}


def test_w01_100_accepts_opposite_lucun_or_hualu():
    rows, executable, _, ontology = _load()
    graph = run_wealth_pilot(
        _snapshot(
            {
                "财帛宫": [_star("紫微")],
                "福德宫": [_star("禄存")],
            }
        ),
        rows,
        executable,
        palace_ontology=ontology,
    )
    assert "W01-100" in {node.rule_id for node in graph.nodes}


def test_report_adds_career_income_relation_section():
    rows, executable, semantic, ontology = _load()
    report = build_wealth_structure_report(
        _snapshot(
            {
                "财帛宫": [_star("太阳")],
                "事业宫": [_star("天梁")],
            }
        ),
        rows,
        executable,
        semantic,
        palace_ontology=ontology,
    )
    sections = {section.section_id for section in report.sections}
    assert "career_income_relation" in sections
    assert report.coverage["EXECUTABLE"] == 28
    assert report.coverage["NORMALIZATION_PENDING"] == 72
    assert report.confidence_band == "LOW_CONFIDENCE"

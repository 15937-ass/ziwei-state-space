from pathlib import Path

from src.product.palace_structure import load_palace_ontology
from src.product.wealth_gap_audit import load_wealth_gap_audit
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
B04 = ROOT / "product/PL2J_WEALTH_READY_BATCH1_v0.1.json"
B05 = ROOT / "product/PL2J2_WEALTH_READY_BATCH2_v0.1.json"
GAP = ROOT / "product/PL2I_WEALTH_STRUCTURE_COVERAGE_GAP_AUDIT_v0.1.csv"
SEM_BASE = ROOT / "product/PL2E_WEALTH_SEMANTIC_REGISTRY_v0.1.json"
SEM_B02 = ROOT / "product/PL2F_WEALTH_SEMANTIC_BATCH2_v0.1.json"
SEM_B03 = ROOT / "product/PL2H_WEALTH_SEMANTIC_BATCH3_v0.1.json"
SEM_B04 = ROOT / "product/PL2J_WEALTH_SEMANTIC_BATCH4_v0.1.json"
SEM_B05 = ROOT / "product/PL2J2_WEALTH_SEMANTIC_BATCH5_v0.1.json"
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


def _snapshot(stars=None):
    stars = stars or {}
    palaces = {}
    for palace_name, branch in BRANCH.items():
        palaces[branch] = {
            "name": palace_name[:-1],
            "stem": "甲",
            "branch": branch,
            "is_body_palace": False,
            "major_stars": list(stars.get(palace_name, [])),
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
    registry = compose_wealth_registries(
        load_pilot_registry(B01),
        load_pilot_registry(B02),
        load_pilot_registry(B03),
        load_pilot_registry(B04),
        load_pilot_registry(B05),
    )
    semantic = compose_wealth_semantic_registries(
        load_wealth_semantic_registry(SEM_BASE),
        load_wealth_semantic_overlay(SEM_B02),
        load_wealth_semantic_overlay(SEM_B03),
        load_wealth_semantic_overlay(SEM_B04),
        load_wealth_semantic_overlay(SEM_B05),
    )
    ontology = load_palace_ontology(ONTOLOGY)
    return rows, registry, semantic, ontology


def test_b05_consumes_all_remaining_pl2i_ready_rows():
    b04 = set(load_pilot_registry(B04)["rules"])
    b05 = set(load_pilot_registry(B05)["rules"])
    gap = load_wealth_gap_audit(GAP)
    ready = {
        row.projection_rule_id
        for row in gap
        if row.readiness_class in {"LOCAL_ATOM_READY", "CROSS_PALACE_READY"}
        and not row.secondary_blockers
    }
    assert len(ready) == 21
    assert len(b05) == 11
    assert b04 | b05 == ready
    assert not b04.intersection(b05)


def test_b05_expands_w01_executable_coverage_to_49():
    rows, registry, _, _ = _load()
    report = compile_wealth_pilot(rows, registry)
    assert report.issues == ()
    assert len(report.executable) == 49
    assert summarize_ledger(build_w01_coverage_ledger(rows, registry)) == {
        "EXECUTABLE": 49,
        "NORMALIZATION_PENDING": 51,
        "PATH_DEPENDENT_HOLD": 0,
        "EXCLUDED": 0,
    }


def test_new_consumption_and_support_sections_are_valid():
    rows, registry, semantic, ontology = _load()
    report = build_wealth_structure_report(
        _snapshot({"财帛宫": [_star("左辅")]}),
        rows,
        registry,
        semantic,
        palace_ontology=ontology,
    )
    sections = {section.section_id for section in report.sections}
    assert "consumption" in sections
    assert "support" in sections


def test_w01_056_requires_lu_in_at_least_two_triad_palaces():
    rows, registry, _, ontology = _load()

    one_palace = run_wealth_pilot(
        _snapshot({"财帛宫": [_star("禄存")]}),
        rows,
        registry,
        palace_ontology=ontology,
    )
    assert "W01-056" not in {node.rule_id for node in one_palace.nodes}

    two_palaces = run_wealth_pilot(
        _snapshot({
            "财帛宫": [_star("禄存")],
            "命宫": [_star("武曲", "禄")],
        }),
        rows,
        registry,
        palace_ontology=ontology,
    )
    assert "W01-056" in {node.rule_id for node in two_palaces.nodes}


def test_w01_060_requires_qingyang_plus_one_named_companion():
    rows, registry, _, ontology = _load()

    qingyang_only = run_wealth_pilot(
        _snapshot({"财帛宫": [_star("擎羊")]}),
        rows,
        registry,
        palace_ontology=ontology,
    )
    assert "W01-060" not in {node.rule_id for node in qingyang_only.nodes}

    with_dijie = run_wealth_pilot(
        _snapshot({"财帛宫": [_star("擎羊"), _star("地劫")]}),
        rows,
        registry,
        palace_ontology=ontology,
    )
    assert "W01-060" in {node.rule_id for node in with_dijie.nodes}


def test_w01_075_requires_wuqu_ji_and_kong_jie():
    rows, registry, _, ontology = _load()

    only_wuqu_ji = run_wealth_pilot(
        _snapshot({"财帛宫": [_star("武曲", "忌")]}),
        rows,
        registry,
        palace_ontology=ontology,
    )
    assert "W01-075" not in {node.rule_id for node in only_wuqu_ji.nodes}

    with_dikong = run_wealth_pilot(
        _snapshot({"财帛宫": [_star("武曲", "忌"), _star("地空")]}),
        rows,
        registry,
        palace_ontology=ontology,
    )
    assert "W01-075" in {node.rule_id for node in with_dikong.nodes}


def test_paired_local_stars_use_explicit_or_expansion():
    rows, registry, _, ontology = _load()
    graph = run_wealth_pilot(
        _snapshot({
            "财帛宫": [
                _star("地劫"),
                _star("凤阁"),
                _star("天喜"),
                _star("蜚廉"),
                _star("阴煞"),
            ]
        }),
        rows,
        registry,
        palace_ontology=ontology,
    )
    active = {node.rule_id for node in graph.nodes}
    assert {"W01-072", "W01-078", "W01-080", "W01-081", "W01-082"}.issubset(active)


def test_w01_079_requires_tianchu_fire_alone_is_not_enough():
    rows, registry, _, ontology = _load()
    fire_only = run_wealth_pilot(
        _snapshot({"财帛宫": [_star("火星")]}),
        rows,
        registry,
        palace_ontology=ontology,
    )
    assert "W01-079" not in {node.rule_id for node in fire_only.nodes}

    tianchu = run_wealth_pilot(
        _snapshot({"财帛宫": [_star("天厨")]}),
        rows,
        registry,
        palace_ontology=ontology,
    )
    assert "W01-079" in {node.rule_id for node in tianchu.nodes}


def test_report_remains_low_confidence_at_49_of_100():
    rows, registry, semantic, ontology = _load()
    report = build_wealth_structure_report(
        _snapshot({"财帛宫": [_star("左辅"), _star("天厨")]}),
        rows,
        registry,
        semantic,
        palace_ontology=ontology,
    )
    assert report.coverage["EXECUTABLE"] == 49
    assert report.coverage["NORMALIZATION_PENDING"] == 51
    assert report.confidence_band == "LOW_CONFIDENCE"

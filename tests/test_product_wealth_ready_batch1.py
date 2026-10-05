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
GAP = ROOT / "product/PL2I_WEALTH_STRUCTURE_COVERAGE_GAP_AUDIT_v0.1.csv"
SEM_BASE = ROOT / "product/PL2E_WEALTH_SEMANTIC_REGISTRY_v0.1.json"
SEM_B02 = ROOT / "product/PL2F_WEALTH_SEMANTIC_BATCH2_v0.1.json"
SEM_B03 = ROOT / "product/PL2H_WEALTH_SEMANTIC_BATCH3_v0.1.json"
SEM_B04 = ROOT / "product/PL2J_WEALTH_SEMANTIC_BATCH4_v0.1.json"
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
    )
    semantic = compose_wealth_semantic_registries(
        load_wealth_semantic_registry(SEM_BASE),
        load_wealth_semantic_overlay(SEM_B02),
        load_wealth_semantic_overlay(SEM_B03),
        load_wealth_semantic_overlay(SEM_B04),
    )
    ontology = load_palace_ontology(ONTOLOGY)
    return rows, registry, semantic, ontology


def test_b04_consumes_only_pl2i_ready_rows_without_secondary_blockers():
    b04 = load_pilot_registry(B04)
    gap = {row.projection_rule_id: row for row in load_wealth_gap_audit(GAP)}
    assert len(b04["rules"]) == 10
    for rule_id in b04["rules"]:
        row = gap[rule_id]
        assert row.readiness_class in {"LOCAL_ATOM_READY", "CROSS_PALACE_READY"}
        assert row.secondary_blockers == ()


def test_b04_expands_w01_executable_coverage_to_38():
    rows, registry, _, _ = _load()
    report = compile_wealth_pilot(rows, registry)
    assert report.issues == ()
    assert len(report.executable) == 38
    assert summarize_ledger(build_w01_coverage_ledger(rows, registry)) == {
        "EXECUTABLE": 38,
        "NORMALIZATION_PENDING": 62,
        "PATH_DEPENDENT_HOLD": 0,
        "EXCLUDED": 0,
    }


def test_semantic_boundary_rules_activate_on_complete_palace_topology():
    rows, registry, _, ontology = _load()
    graph = run_wealth_pilot(
        _snapshot(),
        rows,
        registry,
        palace_ontology=ontology,
    )
    active = {node.rule_id for node in graph.nodes}
    assert {"W01-002", "W01-003", "W01-005", "W01-020", "W01-021", "W01-036"}.issubset(active)


def test_fubi_scene_rule_accepts_left_or_right_assistant():
    rows, registry, _, ontology = _load()
    left = run_wealth_pilot(
        _snapshot({"财帛宫": [_star("左辅")]}),
        rows,
        registry,
        palace_ontology=ontology,
    )
    right = run_wealth_pilot(
        _snapshot({"财帛宫": [_star("右弼")]}),
        rows,
        registry,
        palace_ontology=ontology,
    )
    assert "W01-046" in {node.rule_id for node in left.nodes}
    assert "W01-046" in {node.rule_id for node in right.nodes}


def test_lu_star_expansion_requires_lucun_or_hualu():
    rows, registry, _, ontology = _load()
    no_lu = run_wealth_pilot(
        _snapshot({"财帛宫": [_star("火星"), _star("天机"), _star("破军"), _star("地空")]}),
        rows,
        registry,
        palace_ontology=ontology,
    )
    no_lu_active = {node.rule_id for node in no_lu.nodes}
    assert not {"W01-068", "W01-069", "W01-070"}.intersection(no_lu_active)

    with_lucun = run_wealth_pilot(
        _snapshot({"财帛宫": [_star("火星"), _star("天机"), _star("破军"), _star("地空"), _star("禄存")]}),
        rows,
        registry,
        palace_ontology=ontology,
    )
    assert {"W01-068", "W01-069", "W01-070"}.issubset(
        {node.rule_id for node in with_lucun.nodes}
    )


def test_hualu_also_satisfies_explicit_lu_star_disjunction():
    rows, registry, _, ontology = _load()
    graph = run_wealth_pilot(
        _snapshot({"财帛宫": [_star("火星"), _star("天机"), _star("武曲", "禄")]}),
        rows,
        registry,
        palace_ontology=ontology,
    )
    assert "W01-068" in {node.rule_id for node in graph.nodes}


def test_report_preserves_low_confidence_at_38_of_100():
    rows, registry, semantic, ontology = _load()
    report = build_wealth_structure_report(
        _snapshot({"财帛宫": [_star("火星"), _star("天机"), _star("禄存")]}),
        rows,
        registry,
        semantic,
        palace_ontology=ontology,
    )
    assert report.coverage["EXECUTABLE"] == 38
    assert report.coverage["NORMALIZATION_PENDING"] == 62
    assert report.confidence_band == "LOW_CONFIDENCE"
    sections = {section.section_id for section in report.sections}
    assert "acquisition" in sections
    assert "effort" in sections
    assert "structural_interpretation" in sections
    assert "career_income_relation" in sections

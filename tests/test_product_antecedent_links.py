from pathlib import Path

import pytest

from src.product.antecedent_links import (
    load_antecedent_links,
    validate_antecedent_links,
)
from src.product.condition_atoms import fact_from_atom
from src.product.evidence_bridge import graph_to_evidence_package
from src.product.palace_structure import load_palace_ontology
from src.product.rule_runtime import RuleRuntime, RuntimeState, compile_rule_row
from src.product.wealth_pilot import (
    build_w01_coverage_ledger,
    compose_wealth_registries,
    compile_wealth_pilot,
    load_pilot_registry,
    load_projection_rows,
    run_wealth_pilot,
    summarize_ledger,
)

ROOT = Path(__file__).resolve().parents[1]
W01 = ROOT / "validation/wp05/W01_wealth_projection_review_001_100.csv"
LINKS = ROOT / "product/PL2M_WEALTH_ANTECEDENT_LINKS_v0.1.json"
BATCHES = [
    ROOT / "product/PL2C_WEALTH_PILOT_v0.1.json",
    ROOT / "product/PL2F_WEALTH_NORMALIZATION_BATCH2_v0.1.json",
    ROOT / "product/PL2H_WEALTH_CROSS_PALACE_BATCH_v0.1.json",
    ROOT / "product/PL2J_WEALTH_READY_BATCH1_v0.1.json",
    ROOT / "product/PL2J2_WEALTH_READY_BATCH2_v0.1.json",
    ROOT / "product/PL2M_WEALTH_ANTECEDENT_EXECUTABLE_BATCH_v0.1.json",
]
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


def _row(rule_id, *, antecedents=(), condition="无"):
    return {
        "rule_id": rule_id,
        "school": "中州派",
        "source_work": "TEST",
        "source_location": "p1",
        "subject": "财帛宫",
        "context": "wealth",
        "condition": condition,
        "time_scope": '["NATAL"]',
        "palace_scope": '["P05"]',
        "topic_scope": '["财帛"]',
        "operator": "projection",
        "target_type": "test",
        "target_normalized": f"target_{rule_id}",
        "state_change": "define",
        "valence": "",
        "source_epistemic": "EXPLICIT",
        "normalization_epistemic": "IMPLEMENTATION",
        "review_status": "SOURCE_SPAN_VERIFIED",
        "source_span_verified": "true",
        "normalization_verified": "true",
        "evidence_text": "test",
        "antecedent_rule_ids": list(antecedents),
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


def _registry():
    return compose_wealth_registries(
        *(load_pilot_registry(path) for path in BATCHES)
    )


def test_runtime_activates_dependency_only_after_antecedent_is_active():
    base, issue = compile_rule_row(_row("A"))
    assert issue is None
    dep, issue = compile_rule_row(_row("B", antecedents=("A",)))
    assert issue is None
    runtime = RuleRuntime([dep, base])
    graph = runtime.match(
        RuntimeState(
            facts=frozenset({"subject:财帛宫"}),
            latent_states={},
            time_scope="NATAL",
            palace_scope="P05",
        ),
        question_scope="财帛",
    )
    assert [node.rule_id for node in graph.nodes] == ["A", "B"]
    assert graph.nodes[1].matched_antecedents == ("A",)


def test_runtime_rejects_missing_antecedent_and_cycles():
    dep, _ = compile_rule_row(_row("B", antecedents=("A",)))
    with pytest.raises(ValueError, match="missing antecedent"):
        RuleRuntime([dep])

    a, _ = compile_rule_row(_row("A", antecedents=("B",)))
    b, _ = compile_rule_row(_row("B", antecedents=("A",)))
    with pytest.raises(ValueError, match="antecedent cycle"):
        RuleRuntime([a, b])


def test_contrastive_evidence_reports_missing_antecedent():
    base, _ = compile_rule_row(
        _row("A", condition="需要标签"),
        condition_atoms=(fact_from_atom("TAG_PRESENT", tag="BASE"),),
    )
    dep, _ = compile_rule_row(_row("B", antecedents=("A",)))
    runtime = RuleRuntime([base, dep])
    state = RuntimeState(
        facts=frozenset({"subject:财帛宫"}),
        latent_states={},
        time_scope="NATAL",
        palace_scope="P05",
    )
    graph = runtime.match(state, question_scope="财帛")
    package = graph_to_evidence_package(
        graph,
        [base, dep],
        facts=state.facts,
        question="test",
        coverage={"NORMALIZATION_PENDING": 1},
    )
    by_id = {item.rule_id: item for item in package.contrastive}
    assert by_id["B"].missing_antecedents == ("A",)


def test_link_registry_classifies_all_ten_antecedent_rows():
    rows = load_projection_rows(W01)
    known = {row["projection_rule_id"] for row in rows}
    registry = _registry()
    executable_before = set(registry["rules"]) - {
        "W01-007", "W01-008", "W01-009", "W01-015", "W01-062"
    }
    links = load_antecedent_links(LINKS)
    counts = validate_antecedent_links(
        links,
        known_rule_ids=known,
        executable_rule_ids=executable_before,
    )
    assert counts == {
        "EXECUTABLE_NOW": 5,
        "REFERENCE_ONLY": 2,
        "UPSTREAM_AND_LOCAL_BLOCKED": 1,
        "UPSTREAM_BLOCKED": 2,
    }


def test_compare_reference_rows_are_not_promoted_to_chart_triggers():
    registry = _registry()
    assert "W01-027" not in registry["rules"]
    assert "W01-030" not in registry["rules"]


def test_pl2m_expands_wealth_executable_coverage_to_54():
    rows = load_projection_rows(W01)
    registry = _registry()
    report = compile_wealth_pilot(rows, registry)
    assert report.issues == ()
    assert len(report.executable) == 54
    assert summarize_ledger(build_w01_coverage_ledger(rows, registry)) == {
        "EXECUTABLE": 54,
        "NORMALIZATION_PENDING": 46,
        "PATH_DEPENDENT_HOLD": 0,
        "EXCLUDED": 0,
    }


def test_w01_006_activates_three_inherited_scene_rules():
    rows = load_projection_rows(W01)
    registry = _registry()
    ontology = load_palace_ontology(ONTOLOGY)
    graph = run_wealth_pilot(
        _snapshot({
            "财帛宫": [_star("武曲", "忌"), _star("七杀")],
            "福德宫": [_star("天府", "科")],
        }),
        rows,
        registry,
        palace_ontology=ontology,
    )
    active = {node.rule_id for node in graph.nodes}
    assert {"W01-006", "W01-007", "W01-008", "W01-009"}.issubset(active)
    node = next(node for node in graph.nodes if node.rule_id == "W01-007")
    assert node.matched_antecedents == ("W01-006",)


def test_w01_014_activates_inherited_scene_translation():
    rows = load_projection_rows(W01)
    registry = _registry()
    ontology = load_palace_ontology(ONTOLOGY)
    graph = run_wealth_pilot(
        _snapshot({
            "财帛宫": [_star("太阳")],
            "事业宫": [_star("天梁")],
        }),
        rows,
        registry,
        palace_ontology=ontology,
    )
    active = {node.rule_id for node in graph.nodes}
    assert {"W01-014", "W01-015"}.issubset(active)


def test_w01_061_activates_retention_follow_on():
    rows = load_projection_rows(W01)
    registry = _registry()
    ontology = load_palace_ontology(ONTOLOGY)
    graph = run_wealth_pilot(
        _snapshot({
            "财帛宫": [_star("擎羊"), _star("廉贞"), _star("贪狼")],
        }),
        rows,
        registry,
        palace_ontology=ontology,
    )
    active = {node.rule_id for node in graph.nodes}
    assert {"W01-061", "W01-062"}.issubset(active)

from pathlib import Path

from src.product.condition_atoms import fact_from_atom
from src.product.dignity import load_dignity_table
from src.product.palace_structure import load_palace_ontology, resolve_palace_structure
from src.product.structure_primitives import (
    adjacent_palaces,
    has_lu_ma_jiao_chi,
    has_lu_stack,
    is_flanked_by,
    source_backed_structure_facts,
)
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
ONTOLOGY = ROOT / "knowledge/wp05/palace_ontology_v0.1.csv"
DIGNITY = ROOT / "validation/wp04_source_closure/DG01_dignity_tables_v0.1.csv"
BATCHES = [
    ROOT / "product/PL2C_WEALTH_PILOT_v0.1.json",
    ROOT / "product/PL2F_WEALTH_NORMALIZATION_BATCH2_v0.1.json",
    ROOT / "product/PL2H_WEALTH_CROSS_PALACE_BATCH_v0.1.json",
    ROOT / "product/PL2J_WEALTH_READY_BATCH1_v0.1.json",
    ROOT / "product/PL2J2_WEALTH_READY_BATCH2_v0.1.json",
    ROOT / "product/PL2M_WEALTH_ANTECEDENT_EXECUTABLE_BATCH_v0.1.json",
    ROOT / "product/PL2L_WEALTH_SOURCE_BACKED_BATCH_v0.1.json",
]

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


def _star(name, mutagen=None, brightness=None):
    return {
        "name": name,
        "brightness": brightness,
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


def _load_registry():
    return compose_wealth_registries(
        *(load_pilot_registry(path) for path in BATCHES)
    )


def _resolved(snapshot):
    return resolve_palace_structure(snapshot, load_palace_ontology(ONTOLOGY))


def test_pl2l_expands_w01_to_57_executable_and_holds_w01_043():
    rows = load_projection_rows(W01)
    registry = _load_registry()
    report = compile_wealth_pilot(rows, registry)
    assert report.issues == ()
    assert len(report.executable) == 57
    assert "W01-043" not in registry["rules"]
    assert summarize_ledger(build_w01_coverage_ledger(rows, registry)) == {
        "EXECUTABLE": 57,
        "NORMALIZATION_PENDING": 43,
        "PATH_DEPENDENT_HOLD": 0,
        "EXCLUDED": 0,
    }


def test_flanking_uses_the_two_branch_adjacent_palaces_only():
    snapshot = _snapshot({
        "交友宫": [_star("天魁")],  # 辰, left of 财帛巳
        "疾厄宫": [_star("天钺")],  # 午, right of 财帛巳
    })
    structure = _resolved(snapshot)
    left, right = adjacent_palaces(structure, "P05")
    assert {left.branch, right.branch} == {"辰", "午"}
    assert is_flanked_by(structure, "P05", "天魁", "天钺")

    same_side = _resolved(_snapshot({
        "交友宫": [_star("天魁"), _star("天钺")],
    }))
    assert not is_flanked_by(same_side, "P05", "天魁", "天钺")


def test_w01_050_accepts_each_explicit_flanking_pair():
    rows = load_projection_rows(W01)
    registry = _load_registry()
    ontology = load_palace_ontology(ONTOLOGY)
    pairs = [
        ("天魁", "天钺"),
        ("左辅", "右弼"),
        ("文昌", "文曲"),
    ]
    for first, second in pairs:
        graph = run_wealth_pilot(
            _snapshot({
                "交友宫": [_star(first)],
                "疾厄宫": [_star(second)],
            }),
            rows,
            registry,
            palace_ontology=ontology,
        )
        assert "W01-050" in {node.rule_id for node in graph.nodes}


def test_lu_ma_jiao_chi_is_same_palace_or_target_opposite_split():
    same = _resolved(_snapshot({
        "财帛宫": [_star("禄存"), _star("天马")],
    }))
    assert has_lu_ma_jiao_chi(same, "P05")

    split = _resolved(_snapshot({
        "财帛宫": [_star("禄存")],
        "福德宫": [_star("天马")],
    }))
    assert has_lu_ma_jiao_chi(split, "P05")

    opposite_only = _resolved(_snapshot({
        "福德宫": [_star("禄存"), _star("天马")],
    }))
    assert not has_lu_ma_jiao_chi(opposite_only, "P05")


def test_w01_024_activates_for_source_defined_lu_ma_structure():
    rows = load_projection_rows(W01)
    registry = _load_registry()
    graph = run_wealth_pilot(
        _snapshot({
            "财帛宫": [_star("禄存")],
            "福德宫": [_star("天马")],
        }),
        rows,
        registry,
        palace_ontology=load_palace_ontology(ONTOLOGY),
    )
    assert "W01-024" in {node.rule_id for node in graph.nodes}


def test_lu_stack_and_yang_tuo_flank_both_required_for_w01_057():
    rows = load_projection_rows(W01)
    registry = _load_registry()
    ontology = load_palace_ontology(ONTOLOGY)

    no_flank_snapshot = _snapshot({
        "财帛宫": [_star("武曲", "禄")],
        "福德宫": [_star("禄存")],
    })
    structure = _resolved(no_flank_snapshot)
    assert has_lu_stack(structure, "P05")
    graph = run_wealth_pilot(
        no_flank_snapshot, rows, registry, palace_ontology=ontology
    )
    assert "W01-057" not in {node.rule_id for node in graph.nodes}

    with_flank = _snapshot({
        "财帛宫": [_star("武曲", "禄")],
        "福德宫": [_star("禄存")],
        "交友宫": [_star("擎羊")],
        "疾厄宫": [_star("陀罗")],
    })
    facts = source_backed_structure_facts(_resolved(with_flank))
    assert fact_from_atom(
        "STRUCTURE_PRESENT", palace="P05", structure="LU_STACK"
    ) in facts
    assert fact_from_atom(
        "STRUCTURE_PRESENT", palace="P05", structure="YANG_TUO_FLANK"
    ) in facts

    graph = run_wealth_pilot(
        with_flank, rows, registry, palace_ontology=ontology
    )
    assert "W01-057" in {node.rule_id for node in graph.nodes}


def test_dignity_lookup_preserves_source_categories_without_numeric_score():
    table = load_dignity_table(DIGNITY)
    assert table.category("子", "天梁") == "庙"
    assert table.is_ru_miao("子", "天梁")
    assert table.category("巳", "天梁") == "陷"
    evidence = table.lookup("子", "天梁")
    assert evidence is not None
    assert evidence.source_id == "SRC-ZZ-002"


def test_no_baiguan_structure_is_emitted_without_human_gate():
    facts = source_backed_structure_facts(_resolved(_snapshot()))
    assert not any("BAIGUAN" in fact or "百官" in fact for fact in facts)

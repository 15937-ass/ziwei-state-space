import copy
import json
from pathlib import Path

import pytest

from src.product.palace_structure import load_palace_ontology
from src.product.response_condition_evaluator import (
    EFFECT_BINDING_REGISTRY_PATH,
    build_career_effect_binding_registry,
    evaluate_career_conditions,
    load_career_condition_registry,
)


ROOT = Path(__file__).resolve().parents[1]
ONTOLOGY_PATH = ROOT / "knowledge/wp05/palace_ontology_v0.1.csv"

CANONICAL = [
    ("P01", "命宫"),
    ("P02", "兄弟宫"),
    ("P03", "夫妻宫"),
    ("P04", "子女宫"),
    ("P05", "财帛宫"),
    ("P06", "疾厄宫"),
    ("P07", "迁移宫"),
    ("P08", "交友宫"),
    ("P09", "事业宫"),
    ("P10", "田宅宫"),
    ("P11", "福德宫"),
    ("P12", "父母宫"),
]
BRANCHES = list("子丑寅卯辰巳午未申酉戌亥")


def _star(name, mutagen=None):
    return {
        "name": name,
        "brightness": None,
        "mutagen": mutagen,
        "type": None,
        "scope": None,
    }


def _snapshot(*, p09_branch="子", stars_by_palace=None):
    stars_by_palace = stars_by_palace or {}
    p09_index = next(
        index for index, (palace_id, _) in enumerate(CANONICAL)
        if palace_id == "P09"
    )
    offset = (BRANCHES.index(p09_branch) - p09_index) % len(BRANCHES)

    palaces = {}
    for index, (palace_id, palace_name) in enumerate(CANONICAL):
        branch = BRANCHES[(index + offset) % len(BRANCHES)]
        stars = []
        for item in stars_by_palace.get(palace_id, []):
            if isinstance(item, tuple):
                stars.append(_star(item[0], item[1]))
            else:
                stars.append(_star(item))
        palaces[branch] = {
            "name": palace_name,
            "stem": "甲",
            "branch": branch,
            "is_body_palace": False,
            "major_stars": stars,
            "minor_stars": [],
            "adjective_stars": [],
        }

    return {
        "schema_version": "0.2",
        "engine": {
            "name": "product-526-test",
            "version": "1",
            "adapter_version": "0.2",
        },
        "input": {},
        "natal": {"palaces": palaces},
    }


def _by_id(result):
    return {
        row["source_rule_id"]: row
        for row in result["evaluations"]
    }


def _evaluate(snapshot, *, condition_registry=None):
    return evaluate_career_conditions(
        snapshot,
        load_palace_ontology(ONTOLOGY_PATH),
        condition_registry=condition_registry,
    )


def test_effect_binding_registry_matches_deterministic_builder():
    stored = json.loads(EFFECT_BINDING_REGISTRY_PATH.read_text(encoding="utf-8"))
    generated = build_career_effect_binding_registry()
    assert generated == stored
    assert generated["summary"] == {
        "compiled_conditions": 12,
        "semantic_effect_bindings": 12,
        "runtime_effects_authorized": 0,
        "response_profile_tau_generated": 0,
    }
    assert len(generated["bindings"]) == 12
    assert all(
        row["binding_status"] == "BOUND_SOURCE_PROJECTION_SEMANTIC_ONLY"
        and row["runtime_effect_allowed"] is False
        for row in generated["bindings"]
    )


def test_same_palace_pair_requires_both_members():
    positive = _evaluate(
        _snapshot(stars_by_palace={
            "P09": ["天机", "龙池", "凤阁"],
        })
    )
    row = _by_id(positive)["CA02-181"]
    assert row["matched"] is True
    assert row["response_effect_bound"] is True
    assert row["effect_binding"]["projection_target"] == (
        "technical_or_artisanal_skill_strengthened"
    )
    assert row["runtime_effect_allowed"] is False

    negative = _evaluate(
        _snapshot(stars_by_palace={
            "P09": ["天机", "龙池"],
        })
    )
    row = _by_id(negative)["CA02-181"]
    assert row["matched"] is False
    assert row["effect_binding"] is None
    assert row["response_effect_bound"] is False


def test_star_system_and_source_local_any_are_bounded_and_deterministic():
    fire = _evaluate(
        _snapshot(stars_by_palace={
            "P09": ["天机", "巨门", "火星"],
        })
    )
    assert _by_id(fire)["CA03-228"]["matched"] is True

    bell = _evaluate(
        _snapshot(stars_by_palace={
            "P09": ["天机", "巨门", "铃星"],
        })
    )
    assert _by_id(bell)["CA03-228"]["matched"] is True

    none = _evaluate(
        _snapshot(stars_by_palace={
            "P09": ["天机", "巨门"],
        })
    )
    assert _by_id(none)["CA03-228"]["matched"] is False


def test_transform_plus_any_member_same_palace():
    result = _evaluate(
        _snapshot(stars_by_palace={
            "P09": [("天同", "忌"), "铃星"],
        })
    )
    assert _by_id(result)["CA05-411"]["matched"] is True

    no_transform = _evaluate(
        _snapshot(stars_by_palace={
            "P09": ["天同", "铃星"],
        })
    )
    assert _by_id(no_transform)["CA05-411"]["matched"] is False


def test_four_directions_requires_both_explicit_members_within_scope():
    ontology = load_palace_ontology(ONTOLOGY_PATH)
    visible = {
        "P09",
        *ontology.entry("P09").triad_palace_ids,
        ontology.entry("P09").opposite_palace_id,
    }
    triad = ontology.entry("P09").triad_palace_ids[0]
    opposite = ontology.entry("P09").opposite_palace_id
    outside = next(pid for pid, _ in CANONICAL if pid not in visible)

    positive = _evaluate(
        _snapshot(stars_by_palace={
            "P09": [("天同", "忌")],
            triad: ["左辅"],
            opposite: ["右弼"],
        })
    )
    assert _by_id(positive)["CA05-419"]["matched"] is True

    missing_one = _evaluate(
        _snapshot(stars_by_palace={
            "P09": [("天同", "忌")],
            triad: ["左辅"],
        })
    )
    assert _by_id(missing_one)["CA05-419"]["matched"] is False

    outside_scope = _evaluate(
        _snapshot(stars_by_palace={
            "P09": [("天同", "忌")],
            triad: ["左辅"],
            outside: ["右弼"],
        })
    )
    assert _by_id(outside_scope)["CA05-419"]["matched"] is False


def test_dependency_rows_mirror_parent_truth_but_bind_child_projection():
    positive = _evaluate(
        _snapshot(stars_by_palace={
            "P09": ["贪狼", "左辅", "右弼"],
        })
    )
    rows = _by_id(positive)
    assert rows["CA07-638"]["matched"] is True
    assert rows["CA07-639"]["matched"] is True
    assert rows["CA07-638"]["effect_binding"]["projection_target"] == (
        "subordinate_base_is_large"
    )
    assert rows["CA07-639"]["effect_binding"]["projection_target"] == (
        "career_operation_tends_to_have_visible_scale_or_presence"
    )
    assert rows["CA07-639"]["matched_evidence"] == [
        "PARENT_CONDITION:PRODUCT_CONDITION:CA07-638:MATCHED"
    ]

    negative = _evaluate(_snapshot(stars_by_palace={"P09": ["贪狼", "左辅"]}))
    rows = _by_id(negative)
    assert rows["CA07-638"]["matched"] is False
    assert rows["CA07-639"]["matched"] is False


def test_source_local_pair_is_not_rewritten_to_any():
    positive = _evaluate(
        _snapshot(stars_by_palace={
            "P09": ["天同", "巨门", "天厨", "火星"],
        })
    )
    assert _by_id(positive)["CA05-433"]["matched"] is True

    missing = _evaluate(
        _snapshot(stars_by_palace={
            "P09": ["天同", "巨门", "天厨"],
        })
    )
    assert _by_id(missing)["CA05-433"]["matched"] is False


def test_branch_gate_and_local_or_for_jumen_delu():
    lucun = _evaluate(
        _snapshot(
            p09_branch="子",
            stars_by_palace={"P09": ["巨门", "禄存"]},
        )
    )
    rows = _by_id(lucun)
    assert rows["CA07-681"]["matched"] is True
    assert rows["CA07-682"]["matched"] is True
    assert rows["CA07-682"]["effect_binding"]["projection_target"] == "avoid_showing_off"

    transformed = _evaluate(
        _snapshot(
            p09_branch="午",
            stars_by_palace={"P09": [("巨门", "禄")]},
        )
    )
    assert _by_id(transformed)["CA07-681"]["matched"] is True

    wrong_branch = _evaluate(
        _snapshot(
            p09_branch="辰",
            stars_by_palace={"P09": ["巨门", "禄存"]},
        )
    )
    assert _by_id(wrong_branch)["CA07-681"]["matched"] is False


def test_qisha_local_or_accepts_only_explicit_promoted_alternatives():
    result = _evaluate(
        _snapshot(
            p09_branch="午",
            stars_by_palace={"P09": ["七杀", "禄存"]},
        )
    )
    row = _by_id(result)["CA09-820"]
    assert row["matched"] is True
    assert row["effect_binding"]["projection_target"] == (
        "financial_institution_employment_scene"
    )

    no_delu = _evaluate(
        _snapshot(
            p09_branch="午",
            stars_by_palace={"P09": ["七杀"]},
        )
    )
    assert _by_id(no_delu)["CA09-820"]["matched"] is False


def test_unsupported_star_system_fails_closed_instead_of_parsing_name():
    registry = load_career_condition_registry()
    mutated = copy.deepcopy(registry)
    row = next(
        item for item in mutated["compiled_conditions"]
        if item["source_rule_id"] == "CA03-228"
    )
    row["subject_terms"] = [{"term_type": "STAR_SYSTEM", "args": ["未知星系"]}]

    with pytest.raises(ValueError, match="unsupported bounded STAR_SYSTEM"):
        _evaluate(
            _snapshot(stars_by_palace={"P09": ["天机", "巨门", "火星"]}),
            condition_registry=mutated,
        )


def test_evaluation_is_natal_semantic_only_and_contains_no_probability_fields():
    result = _evaluate(
        _snapshot(stars_by_palace={
            "P09": ["天机", "龙池", "凤阁"],
        })
    )
    assert result["scope"] == {
        "domain": "career",
        "palace_id": "P09",
        "time_layer": "NATAL",
        "temporal_environment_consumed": False,
    }
    assert result["summary"]["conditions_evaluated"] == 12
    assert result["summary"]["runtime_effects_authorized"] == 0
    assert result["summary"]["response_profile_tau_generated"] == 0

    serialized = json.dumps(result, ensure_ascii=False).lower()
    for forbidden in (
        '"probability"',
        '"posterior"',
        '"numeric_gain"',
        '"learned_weight"',
        '"effect_weight"',
        '"confidence_score"',
        '"reward"',
    ):
        assert forbidden not in serialized

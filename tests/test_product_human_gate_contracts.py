import csv
import json
from pathlib import Path

import pytest

from src.product.human_gate_contracts import (
    BAIGUAN_EXPLICIT_EXCLUSIONS,
    ContextualValence,
    PatternAssessment,
    build_baiguan_support_profile,
)
from src.product.palace_structure import load_palace_ontology, resolve_palace_structure
from src.product.structure_primitives import source_backed_structure_facts


ROOT = Path(__file__).resolve().parents[1]
ONTOLOGY = ROOT / "knowledge/wp05/palace_ontology_v0.1.csv"
REGISTRY = ROOT / "product/PL2Q_HUMAN_GATE_CONTRACT_REGISTRY_v0.1.json"
REFRESH = ROOT / "product/PL2Q_WEALTH_HUMAN_GATE_REFRESH_v0.1.csv"

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


def _resolved(stars_by_palace=None):
    return resolve_palace_structure(
        _snapshot(stars_by_palace),
        load_palace_ontology(ONTOLOGY),
    )


def test_pattern_contract_separates_status_scale_and_integrity_without_numbers():
    assessment = PatternAssessment(
        pattern_id="TEST_PATTERN",
        status="BROKEN",
        scale="LARGE",
        integrity_direction="DEGRADED",
        evidence_rule_ids=("R1",),
    )
    assert assessment.status == "BROKEN"
    assert assessment.scale == "LARGE"
    assert assessment.integrity_direction == "DEGRADED"
    assert assessment.magnitude_status == "UNIDENTIFIED"

    with pytest.raises(ValueError):
        PatternAssessment(
            pattern_id="TEST_PATTERN",
            magnitude_status="0.7",
        )


def test_contextual_valence_requires_question_scope_and_rule_evidence():
    valence = ContextualValence(
        palace_id="P05",
        domain="resource",
        target="resource_retention",
        state="UNFAVORABLE",
        evidence_rule_ids=("W01-X",),
        confidence="MEDIUM",
    )
    assert valence.target == "resource_retention"

    with pytest.raises(ValueError):
        ContextualValence(
            palace_id="P05",
            domain="resource",
            target="resource_retention",
            state="UNFAVORABLE",
            evidence_rule_ids=(),
            confidence="MEDIUM",
        )


def test_baiguan_profile_is_component_evidence_not_complete_structure():
    structure = _resolved({
        "命宫": [_star("紫微")],
        "事业宫": [_star("左辅"), _star("天魁")],
        "迁移宫": [_star("天钺")],
    })
    profile = build_baiguan_support_profile(structure, "P01")

    assert profile.anchor_star == "紫微"
    assert profile.activation_status == "PARTIAL_SUPPORT"
    assert profile.activation_criterion == "DEFERRED_NO_UNIVERSAL_THRESHOLD"
    assert {item.star for item in profile.components} >= {"左辅", "天魁", "天钺"}

    facts = source_backed_structure_facts(structure)
    assert not any("BAIGUAN" in fact or "百官" in fact for fact in facts)


def test_baiguan_profile_tracks_explicit_quality_guard_conflict():
    structure = _resolved({
        "命宫": [_star("紫微")],
        "事业宫": [_star("天府"), _star("地空")],
    })
    profile = build_baiguan_support_profile(structure, "P01")

    assert profile.activation_status == "CONFLICTED"
    assert any(
        item.guard_id == "TIANFU_EMPTY_TREASURY_SAME_PALACE"
        for item in profile.quality_guards
    )


def test_non_ziwei_anchor_fails_closed_as_unknown():
    profile = build_baiguan_support_profile(_resolved(), "P01")
    assert profile.activation_status == "UNKNOWN"
    assert profile.components == ()


def test_transformations_are_not_baiguan_members():
    assert BAIGUAN_EXPLICIT_EXCLUSIONS == {"化禄", "化权", "化科"}


def test_contract_registry_forbids_numeric_score_and_template_match():
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    assert registry["palace_valence_contract"]["universal_numeric_score"] is False
    assert registry["palace_valence_contract"]["numeric_magnitude_in_pl2"] is False
    assert (
        registry["baiguan_contract"]["runtime_v0_1_may_emit_explicit_template_match"]
        is False
    )
    assert (
        registry["baiguan_contract"]["activation_criterion"]
        == "DEFERRED_NO_UNIVERSAL_THRESHOLD"
    )


def test_eight_human_gate_rows_remain_non_executable_after_gate_approval():
    with REFRESH.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    assert {row["projection_rule_id"] for row in rows} == {
        "W01-016",
        "W01-017",
        "W01-022",
        "W01-023",
        "W01-035",
        "W01-095",
        "W01-096",
        "W01-098",
    }
    assert all(row["post_gate_status"] != "EXECUTABLE" for row in rows)
    assert all(row["remaining_blocker"] for row in rows)

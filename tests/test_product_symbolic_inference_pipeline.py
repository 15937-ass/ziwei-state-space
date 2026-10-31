import copy
import json
from pathlib import Path

import pytest

from src.product.natal_domain_registry import load_default_natal_domain_registry
from src.product.symbolic_inference_pipeline import run_symbolic_inference

ROOT = Path(__file__).resolve().parents[1]
ASSET = ROOT / "product/PL3T_TEMPORAL_ASSET_FIXTURE_v0.2.json"
PRODUCTION_REGISTRY = ROOT / "product/PL3T_TEMPORAL_REACTION_REGISTRY_v0.1.json"
TEST_REGISTRY = ROOT / "product/PL3T_TEMPORAL_REACTION_FIXTURE_v0.1.json"

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
    full = json.loads(ASSET.read_text(encoding="utf-8"))
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
    full["natal"] = {"palaces": palaces}
    return full


def _run(
    *,
    registry_path=PRODUCTION_REGISTRY,
    stars_by_palace=None,
    target_id="T-DEMO",
    snapshot=None,
    temporal_conflicts=(),
    selected_temporal_layers=None,
):
    normalized_snapshot = snapshot if snapshot is not None else _snapshot(stars_by_palace)
    domain_registry = load_default_natal_domain_registry(ROOT)
    reaction_document = json.loads(registry_path.read_text(encoding="utf-8"))
    return run_symbolic_inference(
        normalized_snapshot,
        target_id=target_id,
        question="本命结构与目标时间层的关系",
        domain_registry=domain_registry,
        reaction_registry_document=reaction_document,
        selected_domains=("wealth",),
        selected_temporal_layers=selected_temporal_layers,
        temporal_conflicts=temporal_conflicts,
    )


def test_empty_production_registry_is_reported_as_partial_not_success():
    result = _run()
    assert result.status == "PARTIAL_TEMPORAL_REGISTRY_EMPTY"
    assert result.blockers == ("PRODUCTION_TEMPORAL_REACTION_REGISTRY_EMPTY",)
    assert result.reaction_rule_count == 0
    assert result.reaction_report.matched == ()
    assert result.temporal_profile.reactions == ()
    payload = result.evidence_package.to_dict()
    assert payload["personal"] == {}
    assert payload["empirical"] == {}


def test_structured_conclusion_is_embedded_and_empty_registry_stays_unknown():
    result = _run(
        stars_by_palace={
            "财帛宫": [_star("火星"), _star("地空"), _star("武曲", "忌")],
        },
        temporal_conflicts=("FIXTURE_CONFLICT",),
    )
    conclusion = result.evidence_package.to_dict()["conclusion"]

    assert conclusion["status"] == "PARTIAL"
    assert conclusion["target_id"] == "T-DEMO"
    assert conclusion["selected_domains"] == ["wealth"]
    assert "PRODUCTION_TEMPORAL_REACTION_REGISTRY_EMPTY" in conclusion["unknowns"]
    assert "FIXTURE_CONFLICT" in conclusion["conflicts"]
    assert "NO_REAL_WORLD_EVENT_CLAIM" in conclusion["limitations"]
    assert "NO_NUMERIC_PROBABILITY_OR_MAGNITUDE_ESTIMATED" in conclusion["limitations"]

    active_ids = sorted(
        {
            rule.rule_id
            for domain in result.natal_profile.domains
            for rule in domain.active_rules
        }
    )
    assert conclusion["canonical_rule_ids"] == active_ids
    canonical_refs = [
        item for item in conclusion["evidence_refs"] if item["namespace"] == "CANONICAL"
    ]
    assert {item["rule_id"] for item in canonical_refs} == set(active_ids)
    assert all(
        item["source_id"] and item["source_location"] and item["review_status"]
        for item in canonical_refs
    )
    assert conclusion["temporal_reaction_rule_ids"] == []


def test_changing_target_time_preserves_natal_profile_and_changes_only_temporal_namespace():
    snapshot = _snapshot(
        stars_by_palace={
            "财帛宫": [_star("火星"), _star("地空"), _star("武曲", "忌")],
        }
    )
    alternate = copy.deepcopy(snapshot["temporal"][0])
    alternate["target"]["target_id"] = "T-ALT"
    alternate["target"]["time_index"] = 7
    alternate["target"]["solar_date"] = "2034-08-03"
    alternate["solar_date"] = "2034-08-03"
    alternate["lunar_date"] = "二〇三四年七月初九"
    alternate["scopes"]["yearly"]["branch"] = "酉"
    alternate["scopes"]["yearly"]["mutagen"] = ["忌"]
    alternate["scopes"]["yearly"]["stars"] = [[_star("破军", "禄")], []]
    snapshot["temporal"].append(alternate)

    first = _run(snapshot=snapshot, target_id="T-DEMO")
    second = _run(snapshot=snapshot, target_id="T-ALT")

    assert first.natal_profile.to_dict() == second.natal_profile.to_dict()
    assert first.natal_profile.profile_id == second.natal_profile.profile_id
    assert first.evidence_package.to_dict()["canonical"] == second.evidence_package.to_dict()["canonical"]
    assert first.temporal_profile.profile_id != second.temporal_profile.profile_id
    assert first.temporal_profile.target_label != second.temporal_profile.target_label
    assert first.temporal_bundle.condition_facts != second.temporal_bundle.condition_facts
    assert first.evidence_package.to_dict()["temporal"] != second.evidence_package.to_dict()["temporal"]
    assert first.status == second.status == "PARTIAL_TEMPORAL_REGISTRY_EMPTY"
    assert first.run_id != second.run_id


def test_same_snapshot_and_versions_produce_same_run_id_and_payload():
    first = _run()
    second = _run()
    assert first.run_id == second.run_id
    assert first.to_dict() == second.to_dict()


def test_test_fixture_can_exercise_match_path_but_is_never_canonical_ready():
    result = _run(
        registry_path=TEST_REGISTRY,
        stars_by_palace={"事业宫": [_star("紫微")]},
    )
    assert result.status == "TEST_FIXTURE_ONLY"
    assert result.blockers == ("NON_CANONICAL_TEMPORAL_REACTION_REGISTRY",)
    assert len(result.reaction_report.matched) == 1
    assert result.temporal_profile.reactions == result.reaction_report.matched
    assert result.temporal_profile.reactions[0].magnitude_status == "UNIDENTIFIED"


def test_unknown_domain_fails_closed_before_inference():
    snapshot = _snapshot()
    with pytest.raises(ValueError, match="unknown natal domain provider"):
        run_symbolic_inference(
            snapshot,
            target_id="T-DEMO",
            question="事业分析",
            domain_registry=load_default_natal_domain_registry(ROOT),
            reaction_registry_document=json.loads(
                PRODUCTION_REGISTRY.read_text(encoding="utf-8")
            ),
            selected_domains=("career",),
        )


def test_explicit_decade_year_selection_filters_temporal_facts_and_evidence():
    result = _run(selected_temporal_layers=("DECADE", "YEAR"))

    assert result.selected_temporal_layers == ("DECADE", "YEAR")
    assert {item.layer for item in result.temporal_bundle.temporal_facts} == {
        "DECADE",
        "YEAR",
    }
    assert result.temporal_profile.active_layers == ("DECADE", "YEAR")
    assert result.evidence_package.to_dict()["temporal"]["active_layers"] == (
        "DECADE",
        "YEAR",
    )
    conclusion = result.evidence_package.to_dict()["conclusion"]
    assert conclusion["selected_temporal_layers"] == ["DECADE", "YEAR"]
    assert all(
        any(f'"layer":"{layer}"' in fact for layer in ("DECADE", "YEAR"))
        for fact in result.temporal_bundle.condition_facts
    )


def test_unsupported_or_empty_temporal_layer_selection_fails_closed():
    with pytest.raises(ValueError, match="unsupported selected temporal layer"):
        _run(selected_temporal_layers=("LIFETIME",))
    with pytest.raises(ValueError, match="at least one selected temporal layer"):
        _run(selected_temporal_layers=())
    with pytest.raises(ValueError, match="must be an array"):
        _run(selected_temporal_layers="YEAR")


def test_missing_temporal_target_fails_closed():
    with pytest.raises(ValueError, match="target_id not found"):
        _run(target_id="T-NOT-PRESENT")


def test_symbolic_inference_rejects_noncanonical_chart_before_rule_matching():
    snapshot = _snapshot()
    snapshot["engine"]["name"] = "x-iztro-rust"
    with pytest.raises(ValueError, match="non-canonical production chart snapshot"):
        _run(snapshot=snapshot)

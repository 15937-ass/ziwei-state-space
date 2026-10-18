import json
from pathlib import Path

import pytest

from src.product.natal_domain_registry import load_default_natal_domain_registry
from src.product.symbolic_inference_pipeline import run_symbolic_inference

ROOT = Path(__file__).resolve().parents[1]
ASSET = ROOT / "product/PL3T_TEMPORAL_ASSET_FIXTURE_v0.1.json"
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


def _run(*, registry_path=PRODUCTION_REGISTRY, stars_by_palace=None, target_id="T-DEMO"):
    snapshot = _snapshot(stars_by_palace)
    domain_registry = load_default_natal_domain_registry(ROOT)
    reaction_document = json.loads(registry_path.read_text(encoding="utf-8"))
    return run_symbolic_inference(
        snapshot,
        target_id=target_id,
        question="本命结构与目标时间层的关系",
        domain_registry=domain_registry,
        reaction_registry_document=reaction_document,
        selected_domains=("wealth",),
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


def test_missing_temporal_target_fails_closed():
    with pytest.raises(ValueError, match="target_id not found"):
        _run(target_id="T-NOT-PRESENT")

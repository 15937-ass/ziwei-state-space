from pathlib import Path

import pytest

from src.product.evidence_package import ConfidenceBand, EvidencePackage
from src.product.natal_prior import (
    NatalDomainEvidence,
    build_natal_state_profile,
)
from src.product.palace_structure import load_palace_ontology


ROOT = Path(__file__).resolve().parents[1]
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


def _snapshot(stars_by_palace=None, reverse=False):
    stars_by_palace = stars_by_palace or {}
    items = list(BRANCH.items())
    if reverse:
        items = list(reversed(items))
    palaces = {}
    for palace_name, branch in items:
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
        "engine": {
            "name": "test",
            "version": "1",
            "adapter_version": "0.2",
        },
        "input": {},
        "natal": {"palaces": palaces},
    }


def _package(history=None):
    return EvidencePackage(
        question="财帛结构",
        chart_facts={"palace_id": "P05", "time_layer": "NATAL"},
        history_state=history or {},
        confidence_band=ConfidenceBand.INSUFFICIENT_EVIDENCE,
        knowledge_version="TEST-W01",
    )


def test_same_chart_and_version_produce_same_profile_id():
    ontology = load_palace_ontology(ONTOLOGY)
    a = build_natal_state_profile(
        _snapshot({"命宫": [_star("紫微")]}),
        ontology,
        knowledge_version="KB-TEST",
    )
    b = build_natal_state_profile(
        _snapshot({"命宫": [_star("紫微")]}),
        ontology,
        knowledge_version="KB-TEST",
    )
    assert a == b
    assert a.profile_id == b.profile_id


def test_mapping_order_does_not_change_natal_prior():
    ontology = load_palace_ontology(ONTOLOGY)
    stars = {
        "命宫": [_star("紫微")],
        "财帛宫": [_star("禄存"), _star("天马")],
    }
    a = build_natal_state_profile(
        _snapshot(stars),
        ontology,
        knowledge_version="KB-TEST",
    )
    b = build_natal_state_profile(
        _snapshot(stars, reverse=True),
        ontology,
        knowledge_version="KB-TEST",
    )
    assert a.profile_id == b.profile_id
    assert a.canonical_facts == b.canonical_facts
    assert a.named_structure_facts == b.named_structure_facts


def test_knowledge_version_is_part_of_natal_identity():
    ontology = load_palace_ontology(ONTOLOGY)
    snapshot = _snapshot()
    a = build_natal_state_profile(snapshot, ontology, knowledge_version="KB-A")
    b = build_natal_state_profile(snapshot, ontology, knowledge_version="KB-B")
    assert a.profile_id != b.profile_id


def test_baiguan_remains_profile_evidence_not_structure_truth():
    ontology = load_palace_ontology(ONTOLOGY)
    profile = build_natal_state_profile(
        _snapshot({
            "命宫": [_star("紫微")],
            "事业宫": [_star("左辅"), _star("天魁")],
        }),
        ontology,
        knowledge_version="KB-TEST",
    )
    assert len(profile.baiguan_profiles) == 1
    assert profile.baiguan_profiles[0].activation_status == "PARTIAL_SUPPORT"
    assert not any("BAIGUAN" in fact for fact in profile.named_structure_facts)


def test_natal_domain_rejects_history_feedback():
    package = _package(history={"relationship_status": "single"})
    with pytest.raises(ValueError, match="history/acquired-state"):
        NatalDomainEvidence.from_evidence_package("wealth", package)


def test_natal_domain_rejects_non_natal_package():
    package = EvidencePackage(
        question="流年财帛",
        chart_facts={"palace_id": "P05", "time_layer": "YEAR"},
        confidence_band=ConfidenceBand.INSUFFICIENT_EVIDENCE,
        knowledge_version="TEST",
    )
    with pytest.raises(ValueError, match="NATAL packages only"):
        NatalDomainEvidence.from_evidence_package("wealth", package)


def test_natal_profile_has_no_feedback_or_empirical_calibration():
    ontology = load_palace_ontology(ONTOLOGY)
    domain = NatalDomainEvidence.from_evidence_package("wealth", _package())
    profile = build_natal_state_profile(
        _snapshot(),
        ontology,
        knowledge_version="KB-TEST",
        domain_evidence=(domain,),
    )
    payload = profile.to_dict()
    assert payload["feedback_used"] is False
    assert payload["empirical_calibration_used"] is False
    assert "probability" not in str(payload).lower()
    assert payload["domains"][0]["domain_id"] == "wealth"

import json
from dataclasses import dataclass
from pathlib import Path

import pytest

from src.product.natal_domain_registry import (
    NatalDomainProviderRegistry,
    load_default_natal_domain_registry,
)
from src.product.natal_prior import NatalDomainEvidence
from src.product.palace_structure import load_palace_ontology


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "product/PL3N_DOMAIN_PROVIDER_REGISTRY_v0.1.json"
ONTOLOGY_PATH = ROOT / "knowledge/wp05/palace_ontology_v0.1.csv"

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


def test_default_registry_has_only_wealth_active():
    registry = load_default_natal_domain_registry(ROOT)
    assert registry.domain_ids == ("wealth",)
    assert registry.knowledge_version == "PL3N[wealth=W01+WEALTH_EXECUTABLE_59]"


def test_registry_builds_wealth_enabled_natal_profile():
    registry = load_default_natal_domain_registry(ROOT)
    profile = registry.build_profile(
        _snapshot({
            "财帛宫": [_star("火星"), _star("地空"), _star("武曲", "忌")],
        })
    )
    assert profile.knowledge_version == "PL3N[wealth=W01+WEALTH_EXECUTABLE_59]"
    assert len(profile.domains) == 1
    assert profile.domains[0].domain_id == "wealth"
    assert "W01-067" in {rule.rule_id for rule in profile.domains[0].active_rules}


def test_unknown_domain_fails_closed():
    registry = load_default_natal_domain_registry(ROOT)
    with pytest.raises(ValueError, match="unknown natal domain provider"):
        registry.build_profile(_snapshot(), selected_domains=("career",))


def test_registry_document_keeps_career_planned_not_active():
    payload = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    assert [item["domain_id"] for item in payload["active_providers"]] == ["wealth"]
    assert payload["planned_providers"][0]["domain_id"] == "career"
    assert payload["planned_providers"][0]["status"] == "PENDING_EXECUTABLE_REGISTRY"


@dataclass
class _FakeProvider:
    domain_id: str
    knowledge_version: str = "X"

    @property
    def palace_ontology(self):
        return load_palace_ontology(ONTOLOGY_PATH)

    def build_domain_evidence(self, snapshot, *, question=""):
        return NatalDomainEvidence(
            domain_id=self.domain_id,
            active_rules=(),
            projection_payloads=(),
            latent_state_payload="{}",
            conflict_payloads=(),
            confidence_band="INSUFFICIENT_EVIDENCE",
            confidence_rationale="test",
            knowledge_version=self.knowledge_version,
        )


def test_duplicate_domain_provider_is_rejected():
    with pytest.raises(ValueError, match="duplicate natal domain provider id"):
        NatalDomainProviderRegistry(
            providers=(_FakeProvider("wealth"), _FakeProvider("wealth"))
        )


def test_selected_domain_subset_controls_profile_knowledge_version():
    registry = NatalDomainProviderRegistry(
        providers=(_FakeProvider("alpha", "A"), _FakeProvider("beta", "B"))
    )
    profile = registry.build_profile(
        _snapshot(),
        selected_domains=("beta",),
    )
    assert profile.knowledge_version == "PL3N[beta=B]"
    assert [item.domain_id for item in profile.domains] == ["beta"]

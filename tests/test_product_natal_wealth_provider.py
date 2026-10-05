import json
from pathlib import Path

from src.product.natal_domain_providers import (
    DEFAULT_WEALTH_BATCH_PATHS,
    WEALTH_HUMAN_GATE_RULE_IDS,
    load_default_wealth_natal_provider,
)


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "product/PL3N_WEALTH_DOMAIN_PROVIDER_v0.1.json"

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


def test_default_wealth_provider_freezes_executable_59_and_excludes_human_gate_rows():
    provider = load_default_wealth_natal_provider(ROOT)
    assert provider.executable_rule_count == 59
    assert provider.knowledge_version == "W01+WEALTH_EXECUTABLE_59"
    assert set(provider.registry["rules"]).isdisjoint(WEALTH_HUMAN_GATE_RULE_IDS)


def test_provider_registry_matches_runtime_batch_list():
    payload = json.loads(REGISTRY.read_text(encoding="utf-8"))
    assert tuple(payload["batch_paths"]) == DEFAULT_WEALTH_BATCH_PATHS
    assert payload["expected_executable_rules"] == 59
    assert set(payload["excluded_human_gate_rules"]) == WEALTH_HUMAN_GATE_RULE_IDS
    assert payload["policy"]["feedback_allowed"] is False
    assert payload["policy"]["empirical_probability_allowed"] is False


def test_wealth_provider_activates_w01_067_inside_natal_profile():
    provider = load_default_wealth_natal_provider(ROOT)
    profile = provider.build_profile(
        _snapshot({
            "财帛宫": [_star("火星"), _star("地空"), _star("武曲", "忌")],
        })
    )
    assert len(profile.domains) == 1
    wealth = profile.domains[0]
    assert wealth.domain_id == "wealth"
    assert "W01-067" in {rule.rule_id for rule in wealth.active_rules}
    assert profile.feedback_used is False
    assert profile.empirical_calibration_used is False


def test_wealth_provider_preserves_source_backed_lu_ma_structure_and_rule():
    provider = load_default_wealth_natal_provider(ROOT)
    profile = provider.build_profile(
        _snapshot({
            "财帛宫": [_star("禄存")],
            "福德宫": [_star("天马")],
        })
    )
    assert any("LU_MA_JIAO_CHI" in fact for fact in profile.named_structure_facts)
    assert "W01-024" in {
        rule.rule_id
        for domain in profile.domains
        for rule in domain.active_rules
    }


def test_profile_identity_is_stable_for_same_wealth_input():
    provider = load_default_wealth_natal_provider(ROOT)
    snapshot = _snapshot({
        "财帛宫": [_star("火星"), _star("地空"), _star("武曲", "忌")],
    })
    a = provider.build_profile(snapshot)
    b = provider.build_profile(snapshot)
    assert a.profile_id == b.profile_id
    assert a.to_dict() == b.to_dict()

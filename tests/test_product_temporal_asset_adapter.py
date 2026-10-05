import json
from pathlib import Path

import pytest

from src.product.natal_prior import NatalStateProfile
from src.product.temporal_asset_adapter import (
    SCOPE_TO_LAYER,
    adapt_target_from_full_snapshot,
    build_temporal_environment_from_assets,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "product/PL3T_TEMPORAL_ASSET_FIXTURE_v0.1.json"


def _snapshot():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def _natal():
    return NatalStateProfile(
        schema_version="0.1",
        profile_id="NATAL-ASSET-TEST",
        engine_version="iztro-js:2.6.1:0.2",
        knowledge_version="KB-TEST",
        canonical_facts=(),
        named_structure_facts=(),
        baiguan_profiles=(),
        pattern_assessments=(),
        contextual_valences=(),
        domains=(),
    )


def test_scope_mapping_covers_six_pl1_temporal_scopes():
    assert SCOPE_TO_LAYER == {
        "decadal": "DECADE",
        "age": "SMALL_LIMIT",
        "yearly": "YEAR",
        "monthly": "MONTH",
        "daily": "DAY",
        "hourly": "HOUR",
    }


def test_adapter_preserves_six_layers_and_engine_provenance():
    bundle = adapt_target_from_full_snapshot(_snapshot(), target_id="T-DEMO")
    layers = {item.layer for item in bundle.temporal_facts}
    assert layers == {"DECADE", "SMALL_LIMIT", "YEAR", "MONTH", "DAY", "HOUR"}
    assert bundle.engine_name == "iztro-js"
    assert bundle.engine_version == "2.6.1"
    assert bundle.adapter_version == "0.2"
    assert all("target=T-DEMO" in item.provenance for item in bundle.temporal_facts)


def test_adapter_preserves_direct_scope_payload_as_atomic_facts():
    bundle = adapt_target_from_full_snapshot(_snapshot(), target_id="T-DEMO")
    facts = {(item.layer, item.fact) for item in bundle.temporal_facts}
    assert ("DECADE", 'scope.branch="寅"') in facts
    assert ("SMALL_LIMIT", "scope.nominal_age=33") in facts
    assert ("YEAR", 'mutagen[0]="科"') in facts
    assert (
        "YEAR",
        'stars[0][0]={"name":"天马","type":"tianma"}',
    ) in facts
    assert ("YEAR", 'yearly_dec.suiqian12[0]="岁建"') in facts


def test_build_profile_from_assets_is_deterministic():
    bundle = adapt_target_from_full_snapshot(_snapshot(), target_id="T-DEMO")
    first = build_temporal_environment_from_assets(_natal(), bundle)
    second = build_temporal_environment_from_assets(_natal(), bundle)
    assert first.profile_id == second.profile_id
    assert first.active_layers == (
        "DAY",
        "DECADE",
        "HOUR",
        "MONTH",
        "SMALL_LIMIT",
        "YEAR",
    )


def test_missing_scope_fails_closed():
    bad = _snapshot()
    del bad["temporal"][0]["scopes"]["daily"]
    with pytest.raises(ValueError, match="missing object: daily"):
        adapt_target_from_full_snapshot(bad, target_id="T-DEMO")


def test_duplicate_target_id_fails_closed():
    bad = _snapshot()
    bad["temporal"].append(dict(bad["temporal"][0]))
    with pytest.raises(ValueError, match="not unique"):
        adapt_target_from_full_snapshot(bad, target_id="T-DEMO")

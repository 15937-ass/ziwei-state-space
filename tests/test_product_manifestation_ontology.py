import json
from pathlib import Path

import pytest

from src.product.manifestation_ontology import (
    compile_manifestation_ontology_registry,
)

ROOT = Path(__file__).resolve().parents[1]
PRODUCTION = ROOT / "product/PL3M_MANIFESTATION_ONTOLOGY_REGISTRY_v0.1.json"
FIXTURE = ROOT / "product/PL3M_MANIFESTATION_ONTOLOGY_FIXTURE_v0.1.json"


def _fixture():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_production_registry_is_fail_closed_until_kb_wp06b():
    registry = compile_manifestation_ontology_registry(
        json.loads(PRODUCTION.read_text(encoding="utf-8"))
    )
    assert registry.registry_status == "EMPTY_PENDING_KB_WP06B"
    assert registry.is_empty
    assert not registry.canonical_ready


def test_test_fixture_validates_topology_without_canonical_claim():
    registry = compile_manifestation_ontology_registry(_fixture())
    assert registry.registry_status == "TEST_ONLY"
    assert registry.by_id()["MFX-CHILD"].parent_id == "MFX-ROOT"
    assert all(
        node.probability_status == "UNKNOWN" for node in registry.nodes
    )


def test_probability_field_is_rejected_from_ontology():
    payload = _fixture()
    payload["nodes"][0]["probability"] = 0.8
    with pytest.raises(ValueError, match="empirical numeric fields"):
        compile_manifestation_ontology_registry(payload)


def test_non_unknown_probability_status_is_rejected():
    payload = _fixture()
    payload["nodes"][0]["probability_status"] = "CALIBRATED"
    with pytest.raises(ValueError, match="probability_status=UNKNOWN"):
        compile_manifestation_ontology_registry(payload)


def test_unknown_parent_fails_closed():
    payload = _fixture()
    payload["nodes"][1]["parent_id"] = "MFX-MISSING"
    with pytest.raises(ValueError, match="unknown parent_id"):
        compile_manifestation_ontology_registry(payload)


def test_cycle_fails_closed():
    payload = _fixture()
    payload["nodes"][0]["parent_id"] = "MFX-CHILD"
    with pytest.raises(ValueError, match="cycle detected"):
        compile_manifestation_ontology_registry(payload)


def test_canonical_ready_requires_verified_source_refs():
    payload = _fixture()
    payload["registry_status"] = "CANONICAL_READY"
    payload["knowledge_artifact_version"] = "KB-WP06B-TEST"
    with pytest.raises(ValueError, match="canonical source refs require"):
        compile_manifestation_ontology_registry(payload)

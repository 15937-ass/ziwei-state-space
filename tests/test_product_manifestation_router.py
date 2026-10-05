import json
from pathlib import Path

import pytest

from src.product.manifestation_ontology import (
    compile_manifestation_ontology_registry,
)
from src.product.manifestation_router import (
    SymbolicActivationContext,
    compile_manifestation_mapping_registry,
    route_source_supported_possibilities,
)

ROOT = Path(__file__).resolve().parents[1]
ONTOLOGY = ROOT / "product/PL3M_MANIFESTATION_ONTOLOGY_FIXTURE_v0.1.json"
PROD_ONTOLOGY = ROOT / "product/PL3M_MANIFESTATION_ONTOLOGY_REGISTRY_v0.1.json"
MAPPING = ROOT / "product/PL3M_MANIFESTATION_MAPPING_FIXTURE_v0.1.json"
PROD_MAPPING = ROOT / "product/PL3M_MANIFESTATION_MAPPING_REGISTRY_v0.1.json"


def _ontology():
    return compile_manifestation_ontology_registry(
        json.loads(ONTOLOGY.read_text(encoding="utf-8"))
    )


def _mappings():
    return compile_manifestation_mapping_registry(
        json.loads(MAPPING.read_text(encoding="utf-8"))
    )


def _context():
    return SymbolicActivationContext(
        active_activation_ids=("ACT-FX-001",),
        active_rule_ids=("RULE-FX-001",),
        evidence_refs=("EVIDENCE-FX-001",),
    )


def test_explicit_mapping_routes_source_supported_possibility_only():
    result = route_source_supported_possibilities(
        _ontology(), _mappings(), _context()
    )
    assert result.disposition == "ROUTED"
    assert len(result.possibilities) == 1
    possibility = result.possibilities[0]
    assert possibility.mapping_id == "MAP-FX-EXPLICIT"
    assert possibility.possibility_status == "SOURCE_SUPPORTED_POSSIBILITY"
    assert possibility.probability_status == "UNKNOWN"
    assert result.held_mappings[0].mapping_id == "MAP-FX-HYPOTHESIS"


def test_hypothesis_never_routes_as_source_supported():
    result = route_source_supported_possibilities(
        _ontology(),
        _mappings(),
        SymbolicActivationContext(
            active_activation_ids=("ACT-FX-001",),
            active_rule_ids=("OTHER-RULE",),
        ),
    )
    assert result.possibilities == ()
    assert result.disposition == "NO_ACTIVE_MAPPING"
    assert result.held_mappings[0].evidence_tier == "HYPOTHESIS"


def test_production_mapping_registry_is_empty_until_kb_wp06c():
    registry = compile_manifestation_mapping_registry(
        json.loads(PROD_MAPPING.read_text(encoding="utf-8"))
    )
    assert registry.registry_status == "EMPTY_PENDING_KB_WP06C"
    assert registry.is_empty


def test_pending_ontology_fails_closed_before_routing():
    ontology = compile_manifestation_ontology_registry(
        json.loads(PROD_ONTOLOGY.read_text(encoding="utf-8"))
    )
    result = route_source_supported_possibilities(
        ontology,
        compile_manifestation_mapping_registry(
            json.loads(PROD_MAPPING.read_text(encoding="utf-8"))
        ),
        _context(),
    )
    assert result.disposition == "ONTOLOGY_NOT_READY"
    assert result.possibilities == ()


def test_probability_or_ranking_field_is_rejected():
    payload = json.loads(MAPPING.read_text(encoding="utf-8"))
    payload["mappings"][0]["weight"] = 0.9
    with pytest.raises(ValueError, match="empirical/ranking"):
        compile_manifestation_mapping_registry(payload)


def test_mapping_target_must_exist_in_ontology():
    payload = json.loads(MAPPING.read_text(encoding="utf-8"))
    payload["mappings"][0]["manifestation_id"] = "MFX-NOT-FOUND"
    mappings = compile_manifestation_mapping_registry(payload)
    with pytest.raises(ValueError, match="not present in ontology"):
        route_source_supported_possibilities(
            _ontology(), mappings, _context()
        )

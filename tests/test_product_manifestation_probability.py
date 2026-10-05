import json
from pathlib import Path

from src.product.manifestation_context import ManifestationRoutingContext
from src.product.manifestation_ontology import (
    compile_manifestation_ontology_registry,
)
from src.product.manifestation_probability import (
    compile_probability_model_registry,
    evaluate_empirical_manifestation_probability,
)
from src.product.manifestation_router import (
    SymbolicActivationContext,
    compile_manifestation_mapping_registry,
    route_source_supported_possibilities,
)

ROOT = Path(__file__).resolve().parents[1]
ONTOLOGY = ROOT / "product/PL3M_MANIFESTATION_ONTOLOGY_FIXTURE_v0.1.json"
MAPPING = ROOT / "product/PL3M_MANIFESTATION_MAPPING_FIXTURE_v0.1.json"
PROD = ROOT / "product/PL3M_PROBABILITY_MODEL_REGISTRY_v0.1.json"
FIXTURE = ROOT / "product/PL3M_PROBABILITY_MODEL_FIXTURE_v0.1.json"


def _possibility():
    ontology = compile_manifestation_ontology_registry(
        json.loads(ONTOLOGY.read_text(encoding="utf-8"))
    )
    mappings = compile_manifestation_mapping_registry(
        json.loads(MAPPING.read_text(encoding="utf-8"))
    )
    routed = route_source_supported_possibilities(
        ontology,
        mappings,
        SymbolicActivationContext(
            active_activation_ids=("ACT-FX-001",),
            active_rule_ids=("RULE-FX-001",),
        ),
    )
    return routed.possibilities[0]


def _context(mode="BLIND", readiness="NOT_REQUESTED"):
    personal = mode == "PERSONALIZED"
    return ManifestationRoutingContext(
        schema_version="0.1",
        context_id="MCTX-PROB-FX",
        mode=mode,
        natal_profile_id="NATAL-FX",
        temporal_profile_id="TEMP-FX",
        knowledge_version="KB-FX",
        target_label="2030",
        person_key="PERSON-FX" if personal else None,
        acquired_state_id="ASTATE-FX" if personal else None,
        state_as_of_date="2030-01-01" if personal else None,
        active_natal_rule_ids=("RULE-FX-001",),
        active_temporal_reaction_ids=(),
        active_temporal_rule_ids=(),
        state_assertions=(),
        actions=(),
        exposures=(),
        external_factors=(),
        counterparty_factors=(),
        state_quality_readiness="READY" if personal else None,
        personalization_readiness=readiness,
        abstention_reasons=(),
    )


class ConstantPlugin:
    def __init__(self, value):
        self.value = value

    def predict(self, model, context, possibility):
        return self.value


def test_production_registry_returns_not_calibrated_and_null_probability():
    registry = compile_probability_model_registry(
        json.loads(PROD.read_text(encoding="utf-8"))
    )
    result = evaluate_empirical_manifestation_probability(
        _possibility(), _context(), registry
    )
    assert result.status == "NOT_CALIBRATED"
    assert result.probability is None
    assert result.namespace == "EMPIRICALLY_CALIBRATED_PROBABILITY"


def test_test_plugin_can_exercise_interface_without_canonical_claim():
    registry = compile_probability_model_registry(
        json.loads(FIXTURE.read_text(encoding="utf-8"))
    )
    result = evaluate_empirical_manifestation_probability(
        _possibility(),
        _context(),
        registry,
        plugin=ConstantPlugin(0.42),
    )
    assert result.status == "ESTIMATED"
    assert result.probability == 0.42
    assert result.parameter_layer == "TEST_FIXTURE"
    assert not result.is_personalized_posterior


def test_ready_model_without_plugin_abstains():
    registry = compile_probability_model_registry(
        json.loads(FIXTURE.read_text(encoding="utf-8"))
    )
    result = evaluate_empirical_manifestation_probability(
        _possibility(), _context(), registry
    )
    assert result.status == "PLUGIN_NOT_AVAILABLE"
    assert result.probability is None


def test_personal_context_requirement_enforces_quality_gate():
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    payload["models"][0]["requires_personal_context"] = True
    registry = compile_probability_model_registry(payload)
    result = evaluate_empirical_manifestation_probability(
        _possibility(),
        _context(mode="PERSONALIZED", readiness="ABSTAIN_MISSING"),
        registry,
        plugin=ConstantPlugin(0.42),
    )
    assert result.status == "ABSTAIN_CONTEXT_QUALITY"
    assert result.probability is None


def test_invalid_plugin_probability_is_rejected():
    import pytest
    registry = compile_probability_model_registry(
        json.loads(FIXTURE.read_text(encoding="utf-8"))
    )
    with pytest.raises(ValueError, match=r"finite in \[0,1\]"):
        evaluate_empirical_manifestation_probability(
            _possibility(),
            _context(),
            registry,
            plugin=ConstantPlugin(1.2),
        )


def test_calibrated_model_requires_real_empirical_provenance():
    import pytest
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    payload["registry_status"] = "CALIBRATED_READY"
    payload["models"][0]["model_status"] = "CALIBRATED"
    with pytest.raises(ValueError, match="TEST_FIXTURE"):
        compile_probability_model_registry(payload)

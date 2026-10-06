import copy
import json
from pathlib import Path

import pytest

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
from src.product.personalized_posterior import (
    compile_personalized_posterior_registry,
    evaluate_personalized_manifestation_posterior,
)


ROOT = Path(__file__).resolve().parents[1]
ONTOLOGY = ROOT / "product/PL3M_MANIFESTATION_ONTOLOGY_FIXTURE_v0.1.json"
MAPPING = ROOT / "product/PL3M_MANIFESTATION_MAPPING_FIXTURE_v0.1.json"
POP_PROD = ROOT / "product/PL3M_PROBABILITY_MODEL_REGISTRY_v0.1.json"
POP_FIXTURE = ROOT / "product/PL3M_PROBABILITY_MODEL_FIXTURE_v0.1.json"
PERSONAL_PROD = ROOT / "product/PL3M_PERSONALIZED_POSTERIOR_REGISTRY_v0.1.json"
PERSONAL_FIXTURE = ROOT / "product/PL3M_PERSONALIZED_POSTERIOR_FIXTURE_v0.1.json"


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


def _context(mode="PERSONALIZED", readiness="READY"):
    personal = mode == "PERSONALIZED"
    return ManifestationRoutingContext(
        schema_version="0.1",
        context_id="MCTX-PP-FX",
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
        personalization_readiness=readiness if personal else "NOT_REQUESTED",
        abstention_reasons=(),
    )


class ConstantPopulationPlugin:
    def __init__(self, value):
        self.value = value

    def predict(self, model, context, possibility):
        return self.value


class ConstantPersonalPlugin:
    def __init__(self, value):
        self.value = value

    def predict(self, model, context, possibility, population_baseline):
        return self.value


def _population_baseline(context, *, value=0.42, production=False):
    path = POP_PROD if production else POP_FIXTURE
    registry = compile_probability_model_registry(
        json.loads(path.read_text(encoding="utf-8"))
    )
    return evaluate_empirical_manifestation_probability(
        _possibility(),
        context,
        registry,
        plugin=None if production else ConstantPopulationPlugin(value),
    )


def _personal_registry(production=False):
    path = PERSONAL_PROD if production else PERSONAL_FIXTURE
    return compile_personalized_posterior_registry(
        json.loads(path.read_text(encoding="utf-8"))
    )


def test_production_registry_keeps_personal_posterior_unavailable():
    context = _context()
    result = evaluate_personalized_manifestation_posterior(
        _possibility(),
        context,
        _population_baseline(context),
        _personal_registry(production=True),
    )
    assert result.status == "NOT_CALIBRATED"
    assert result.namespace == "PERSONALIZED_POSTERIOR"
    assert result.posterior_probability is None
    assert not result.uses_individual_history


def test_test_plugin_exercises_separate_personal_namespace():
    context = _context()
    result = evaluate_personalized_manifestation_posterior(
        _possibility(),
        context,
        _population_baseline(context, value=0.42),
        _personal_registry(),
        plugin=ConstantPersonalPlugin(0.61),
    )
    assert result.status == "ESTIMATED"
    assert result.namespace == "PERSONALIZED_POSTERIOR"
    assert result.population_probability == 0.42
    assert result.posterior_probability == 0.61
    assert result.population_model_id == "PM-FX-001"
    assert result.personalization_model_id == "PPM-FX-001"
    assert result.parameter_layer == "TEST_FIXTURE"
    assert result.uses_individual_history


def test_blind_context_cannot_receive_personalized_posterior():
    context = _context(mode="BLIND")
    result = evaluate_personalized_manifestation_posterior(
        _possibility(),
        context,
        _population_baseline(context),
        _personal_registry(),
        plugin=ConstantPersonalPlugin(0.61),
    )
    assert result.status == "ABSTAIN_CONTEXT_MODE"
    assert result.posterior_probability is None


def test_personal_quality_gate_is_preserved():
    context = _context(readiness="ABSTAIN_MISSING")
    result = evaluate_personalized_manifestation_posterior(
        _possibility(),
        context,
        _population_baseline(context),
        _personal_registry(),
        plugin=ConstantPersonalPlugin(0.61),
    )
    assert result.status == "ABSTAIN_CONTEXT_QUALITY"
    assert result.posterior_probability is None


def test_personal_model_requires_estimated_population_baseline():
    context = _context()
    result = evaluate_personalized_manifestation_posterior(
        _possibility(),
        context,
        _population_baseline(context, production=True),
        _personal_registry(),
        plugin=ConstantPersonalPlugin(0.61),
    )
    assert result.status == "POPULATION_BASELINE_NOT_AVAILABLE"
    assert result.posterior_probability is None


def test_population_model_identity_must_match_personal_model():
    payload = json.loads(PERSONAL_FIXTURE.read_text(encoding="utf-8"))
    payload["models"][0]["population_model_id"] = "PM-OTHER"
    registry = compile_personalized_posterior_registry(payload)
    context = _context()
    result = evaluate_personalized_manifestation_posterior(
        _possibility(),
        context,
        _population_baseline(context),
        registry,
        plugin=ConstantPersonalPlugin(0.61),
    )
    assert result.status == "POPULATION_MODEL_MISMATCH"
    assert result.posterior_probability is None


def test_invalid_personal_plugin_probability_is_rejected():
    context = _context()
    with pytest.raises(ValueError, match=r"finite in \[0,1\]"):
        evaluate_personalized_manifestation_posterior(
            _possibility(),
            context,
            _population_baseline(context),
            _personal_registry(),
            plugin=ConstantPersonalPlugin(1.2),
        )


def test_calibrated_personal_model_requires_non_fixture_parameters():
    payload = copy.deepcopy(
        json.loads(PERSONAL_FIXTURE.read_text(encoding="utf-8"))
    )
    payload["registry_status"] = "CALIBRATED_READY"
    payload["models"][0]["model_status"] = "CALIBRATED"
    payload["models"][0]["calibration_dataset_version"] = "DATA-1"
    payload["models"][0]["calibration_metrics_ref"] = "METRICS-1"
    with pytest.raises(ValueError, match="TEST_FIXTURE"):
        compile_personalized_posterior_registry(payload)

import json
from pathlib import Path

import pytest

from src.product.acquired_state import compile_acquired_state
from src.product.state_belief import (
    bayesian_state_update,
    compile_discrete_state_prior,
    compile_observation_likelihood,
)
from src.product.state_quality import (
    audit_acquired_state_quality,
    compile_state_requirements,
)

ROOT = Path(__file__).resolve().parents[1]
STATE_FIXTURE = ROOT / "product/PL3S_ACQUIRED_STATE_FIXTURE_v0.1.json"


def _quality_report():
    state = compile_acquired_state(
        json.loads(STATE_FIXTURE.read_text(encoding="utf-8"))
    )
    requirements = compile_state_requirements(
        {
            "schema_version": "0.1",
            "requirements": [
                {
                    "requirement_id": "REQ-CAREER",
                    "domain": "CAREER",
                    "key": "employment_status",
                    "accepted_confidences": ["HIGH", "MEDIUM"],
                }
            ],
        }
    )
    return audit_acquired_state_quality(state, requirements)


def _prior(allow_test_only=True):
    return compile_discrete_state_prior(
        {
            "belief_id": "PRIOR-SYNTHETIC-001",
            "domain": "CAREER",
            "key": "employment_status",
            "distribution": {
                "EMPLOYED": "0.5",
                "UNEMPLOYED": "0.5",
            },
            "provenance": {
                "provenance_type": "TEST_ONLY_SYNTHETIC",
                "artifact_id": "TEST-ONLY-PRIOR",
                "artifact_version": "0",
                "parameter_set_id": "SYNTH-PRIOR-001",
            },
        },
        allow_test_only=allow_test_only,
    )


def _likelihood(allow_test_only=True):
    return compile_observation_likelihood(
        {
            "evidence_id": "EVIDENCE-SYNTHETIC-001",
            "domain": "CAREER",
            "key": "employment_status",
            "likelihood_by_hypothesis": {
                "EMPLOYED": "0.8",
                "UNEMPLOYED": "0.2",
            },
            "provenance": {
                "provenance_type": "TEST_ONLY_SYNTHETIC",
                "artifact_id": "TEST-ONLY-LIKELIHOOD",
                "artifact_version": "0",
                "parameter_set_id": "SYNTH-LIKE-001",
            },
        },
        allow_test_only=allow_test_only,
    )


def test_synthetic_parameters_fail_closed_in_normal_product_mode():
    with pytest.raises(ValueError, match="test-only"):
        _prior(allow_test_only=False)
    with pytest.raises(ValueError, match="test-only"):
        _likelihood(allow_test_only=False)


def test_bayes_math_works_only_with_explicit_test_gate_for_synthetic_fixture():
    posterior = bayesian_state_update(
        prior=_prior(),
        evidence=_likelihood(),
        quality_report=_quality_report(),
        requirement_id="REQ-CAREER",
    )
    assert posterior.status == "CALIBRATED_POSTERIOR"
    assert posterior.to_dict()["distribution"] == {
        "EMPLOYED": "0.8",
        "UNEMPLOYED": "0.2",
    }


def test_no_default_prior_is_created_by_engine():
    with pytest.raises(ValueError, match="prior provenance is required"):
        compile_discrete_state_prior(
            {
                "belief_id": "NO-PROVENANCE",
                "domain": "CAREER",
                "key": "employment_status",
                "distribution": {"EMPLOYED": "1"},
            }
        )


def test_prior_must_sum_exactly_to_one():
    with pytest.raises(ValueError, match="sum exactly to 1"):
        compile_discrete_state_prior(
            {
                "belief_id": "BAD",
                "domain": "CAREER",
                "key": "employment_status",
                "distribution": {"EMPLOYED": "0.6", "UNEMPLOYED": "0.5"},
                "provenance": {
                    "provenance_type": "EMPIRICAL_CALIBRATION",
                    "artifact_id": "CAL-1",
                    "artifact_version": "1",
                    "parameter_set_id": "P-1",
                },
            }
        )


def test_quality_gate_blocks_missing_requirement():
    state = compile_acquired_state(
        json.loads(STATE_FIXTURE.read_text(encoding="utf-8"))
    )
    requirements = compile_state_requirements(
        {
            "schema_version": "0.1",
            "requirements": [
                {
                    "requirement_id": "REQ-MISSING",
                    "domain": "RESOURCE",
                    "key": "liquid_asset_level",
                    "accepted_confidences": ["HIGH", "MEDIUM"],
                }
            ],
        }
    )
    report = audit_acquired_state_quality(state, requirements)
    prior = compile_discrete_state_prior(
        {
            "belief_id": "P",
            "domain": "RESOURCE",
            "key": "liquid_asset_level",
            "distribution": {"LOW": "0.5", "HIGH": "0.5"},
            "provenance": {
                "provenance_type": "TEST_ONLY_SYNTHETIC",
                "artifact_id": "TEST-P",
                "artifact_version": "0",
                "parameter_set_id": "P",
            },
        },
        allow_test_only=True,
    )
    likelihood = compile_observation_likelihood(
        {
            "evidence_id": "E",
            "domain": "RESOURCE",
            "key": "liquid_asset_level",
            "likelihood_by_hypothesis": {"LOW": "0.5", "HIGH": "0.5"},
            "provenance": {
                "provenance_type": "TEST_ONLY_SYNTHETIC",
                "artifact_id": "TEST-E",
                "artifact_version": "0",
                "parameter_set_id": "E",
            },
        },
        allow_test_only=True,
    )
    with pytest.raises(ValueError, match="quality gate"):
        bayesian_state_update(
            prior=prior,
            evidence=likelihood,
            quality_report=report,
            requirement_id="REQ-MISSING",
        )


def test_hypothesis_sets_must_match():
    likelihood = compile_observation_likelihood(
        {
            "evidence_id": "E2",
            "domain": "CAREER",
            "key": "employment_status",
            "likelihood_by_hypothesis": {"EMPLOYED": "0.8", "OTHER": "0.2"},
            "provenance": {
                "provenance_type": "TEST_ONLY_SYNTHETIC",
                "artifact_id": "TEST-E2",
                "artifact_version": "0",
                "parameter_set_id": "E2",
            },
        },
        allow_test_only=True,
    )
    with pytest.raises(ValueError, match="hypothesis sets"):
        bayesian_state_update(
            prior=_prior(),
            evidence=likelihood,
            quality_report=_quality_report(),
            requirement_id="REQ-CAREER",
        )


def test_same_calibrated_inputs_produce_same_belief_id():
    kwargs = dict(
        prior=_prior(),
        evidence=_likelihood(),
        quality_report=_quality_report(),
        requirement_id="REQ-CAREER",
    )
    first = bayesian_state_update(**kwargs)
    second = bayesian_state_update(**kwargs)
    assert first.belief_id == second.belief_id

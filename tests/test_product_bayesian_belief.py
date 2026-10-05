import copy
import json
from pathlib import Path

from src.product.acquired_state import compile_acquired_state
from src.product.bayesian_belief import (
    compile_discrete_belief_model,
    update_discrete_belief,
)

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "product/PL3S_ACQUIRED_STATE_FIXTURE_v0.1.json"
MODEL = ROOT / "product/PL3S_BELIEF_MODEL_FIXTURE_v0.1.json"
REGISTRY = ROOT / "product/PL3S_BELIEF_MODEL_REGISTRY_v0.1.json"


def _state():
    return compile_acquired_state(
        json.loads(STATE.read_text(encoding="utf-8"))
    )


def _model():
    return compile_discrete_belief_model(
        json.loads(MODEL.read_text(encoding="utf-8"))
    )


def test_bayesian_update_uses_explicit_state_evidence_only():
    result = update_discrete_belief(_state(), _model())
    posterior = result.posterior_dict()
    assert result.status == "UPDATED"
    assert posterior["STABLE"] == 0.8
    assert posterior["TRANSITIONING"] == 0.2
    assert result.evidence_use[0].status == "USED"


def test_missing_evidence_is_skipped_without_imputation():
    payload = json.loads(STATE.read_text(encoding="utf-8"))
    payload["assertions"] = [
        item
        for item in payload["assertions"]
        if not (
            item["domain"] == "CAREER"
            and item["key"] == "employment_status"
        )
    ]
    payload["missingness"].append(
        {
            "domain": "CAREER",
            "key": "employment_status",
            "reason": "NOT_OBSERVED",
            "last_observed_date": None,
        }
    )
    state = compile_acquired_state(payload)
    result = update_discrete_belief(state, _model())
    assert result.status == "NO_USABLE_EVIDENCE"
    assert result.posterior_dict() == {"STABLE": 0.5, "TRANSITIONING": 0.5}
    assert result.evidence_use[0].status == "SKIPPED_MISSING"


def test_conflict_is_skipped_without_auto_resolution():
    payload = json.loads(STATE.read_text(encoding="utf-8"))
    alt = copy.deepcopy(payload["assertions"][0])
    alt["fact_id"] = "SF-CAREER-ALT"
    alt["value"] = "UNEMPLOYED"
    payload["assertions"].append(alt)
    payload["conflicts"] = [
        {
            "conflict_id": "CF-CAREER-001",
            "domain": "CAREER",
            "key": "employment_status",
            "fact_ids": ["SF-CAREER-001", "SF-CAREER-ALT"],
            "status": "UNRESOLVED",
        }
    ]
    state = compile_acquired_state(payload)
    result = update_discrete_belief(state, _model())
    assert result.status == "NO_USABLE_EVIDENCE"
    assert result.evidence_use[0].status == "SKIPPED_CONFLICT"


def test_low_confidence_can_be_rejected_by_model_contract():
    payload = json.loads(STATE.read_text(encoding="utf-8"))
    payload["assertions"][0]["confidence"] = "LOW"
    state = compile_acquired_state(payload)
    result = update_discrete_belief(state, _model())
    assert result.evidence_use[0].status == "SKIPPED_CONFIDENCE"


def test_likelihood_tables_must_be_normalized_per_hypothesis():
    payload = json.loads(MODEL.read_text(encoding="utf-8"))
    payload["evidence_channels"][0]["likelihoods"]["EMPLOYED"]["STABLE"] = 0.7
    import pytest
    with pytest.raises(ValueError, match="must sum to 1"):
        compile_discrete_belief_model(payload)


def test_production_registry_is_empty_until_empirical_calibration():
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    assert registry["models"] == []
    assert registry["status"] == "EMPTY_PENDING_EMPIRICAL_CALIBRATION"

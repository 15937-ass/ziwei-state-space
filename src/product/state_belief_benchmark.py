"""PL3-S StateBelief deterministic benchmark v0.1.

This benchmark freezes interface behavior only. It uses TEST_FIXTURE parameters
and must never be interpreted as predictive accuracy or empirical calibration.
"""

from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from .acquired_state import compile_acquired_state
from .bayesian_belief import (
    BeliefUpdateResult,
    compile_discrete_belief_model,
    update_discrete_belief,
)


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_STATE_FIXTURE = ROOT / "product" / "PL3S_ACQUIRED_STATE_FIXTURE_v0.1.json"
DEFAULT_MODEL_FIXTURE = ROOT / "product" / "PL3S_BELIEF_MODEL_FIXTURE_v0.1.json"
DEFAULT_PRODUCTION_REGISTRY = ROOT / "product" / "PL3S_BELIEF_MODEL_REGISTRY_v0.1.json"

BENCHMARK_CASES = (
    "AVAILABLE_EMPLOYED",
    "MISSING_EMPLOYMENT",
    "CONFLICTING_EMPLOYMENT",
    "LOW_CONFIDENCE_EMPLOYMENT",
    "UNMODELLED_EMPLOYMENT_VALUE",
)


@dataclass(frozen=True)
class StateBeliefBenchmarkCase:
    case_id: str
    expected_status: str
    expected_evidence_status: str
    state_id: str
    posterior: tuple[tuple[str, float], ...]
    result_digest: str


@dataclass(frozen=True)
class StateBeliefBenchmarkReport:
    schema_version: str
    benchmark_id: str
    model_id: str
    model_version: str
    parameter_layer: str
    cases: tuple[StateBeliefBenchmarkCase, ...]
    production_registry_status: str
    production_registry_model_count: int
    empirical_accuracy_claimed: bool = False
    production_calibration_claimed: bool = False

    def __post_init__(self) -> None:
        if self.schema_version != "0.1":
            raise ValueError("StateBeliefBenchmarkReport schema_version must be 0.1")
        if self.parameter_layer != "TEST_FIXTURE":
            raise ValueError("v0.1 benchmark must use TEST_FIXTURE parameter layer")
        if self.empirical_accuracy_claimed or self.production_calibration_claimed:
            raise ValueError("state-belief benchmark cannot claim empirical accuracy/calibration")

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "benchmark_id": self.benchmark_id,
            "model_id": self.model_id,
            "model_version": self.model_version,
            "parameter_layer": self.parameter_layer,
            "cases": [
                {
                    "case_id": item.case_id,
                    "expected_status": item.expected_status,
                    "expected_evidence_status": item.expected_evidence_status,
                    "state_id": item.state_id,
                    "posterior": dict(item.posterior),
                    "result_digest": item.result_digest,
                }
                for item in self.cases
            ],
            "production_registry_status": self.production_registry_status,
            "production_registry_model_count": self.production_registry_model_count,
            "empirical_accuracy_claimed": self.empirical_accuracy_claimed,
            "production_calibration_claimed": self.production_calibration_claimed,
        }


def _read_json(path: Path | str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _digest_result(result: BeliefUpdateResult) -> str:
    raw = json.dumps(
        result.to_dict(),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _state_for_case(base: Mapping[str, Any], case_id: str):
    payload = copy.deepcopy(dict(base))
    career = next(
        item
        for item in payload["assertions"]
        if item["domain"] == "CAREER" and item["key"] == "employment_status"
    )

    if case_id == "AVAILABLE_EMPLOYED":
        pass
    elif case_id == "MISSING_EMPLOYMENT":
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
    elif case_id == "CONFLICTING_EMPLOYMENT":
        alt = copy.deepcopy(career)
        alt["fact_id"] = "SF-CAREER-BENCH-CONFLICT"
        alt["value"] = "UNEMPLOYED"
        alt["status"] = "REPORTED"
        alt["confidence"] = "MEDIUM"
        payload["assertions"].append(alt)
        payload["conflicts"].append(
            {
                "conflict_id": "CF-BENCH-CAREER",
                "domain": "CAREER",
                "key": "employment_status",
                "fact_ids": [career["fact_id"], alt["fact_id"]],
                "status": "UNRESOLVED",
            }
        )
    elif case_id == "LOW_CONFIDENCE_EMPLOYMENT":
        career["confidence"] = "LOW"
    elif case_id == "UNMODELLED_EMPLOYMENT_VALUE":
        career["value"] = "SABBATICAL"
    else:
        raise ValueError(f"unsupported benchmark case: {case_id}")

    payload["state_id"] = None
    return compile_acquired_state(payload)


def _expectation(case_id: str) -> tuple[str, str]:
    if case_id == "AVAILABLE_EMPLOYED":
        return "UPDATED", "USED"
    if case_id == "MISSING_EMPLOYMENT":
        return "NO_USABLE_EVIDENCE", "SKIPPED_MISSING"
    if case_id == "CONFLICTING_EMPLOYMENT":
        return "NO_USABLE_EVIDENCE", "SKIPPED_CONFLICT"
    if case_id == "LOW_CONFIDENCE_EMPLOYMENT":
        return "NO_USABLE_EVIDENCE", "SKIPPED_CONFIDENCE"
    if case_id == "UNMODELLED_EMPLOYMENT_VALUE":
        return "NO_USABLE_EVIDENCE", "SKIPPED_UNMODELLED_VALUE"
    raise ValueError(f"unsupported benchmark case: {case_id}")


def run_state_belief_benchmark(
    *,
    state_fixture_path: Path | str = DEFAULT_STATE_FIXTURE,
    model_fixture_path: Path | str = DEFAULT_MODEL_FIXTURE,
    production_registry_path: Path | str = DEFAULT_PRODUCTION_REGISTRY,
) -> StateBeliefBenchmarkReport:
    """Run frozen contract cases for PL3-S belief behavior."""

    base_state = _read_json(state_fixture_path)
    model_doc = _read_json(model_fixture_path)
    registry = _read_json(production_registry_path)

    model = compile_discrete_belief_model(model_doc)
    if model.parameter_layer != "TEST_FIXTURE" or model.model_status != "TEST_ONLY":
        raise ValueError("benchmark model must remain TEST_FIXTURE / TEST_ONLY")

    registry_models = registry.get("models")
    if not isinstance(registry_models, list):
        raise ValueError("production belief registry models must be an array")
    if registry_models:
        raise ValueError(
            "PL3-S v0.1 benchmark expects production belief registry to remain empty"
        )
    registry_status = str(registry.get("status") or "").strip()
    if registry_status != "EMPTY_PENDING_EMPIRICAL_CALIBRATION":
        raise ValueError("unexpected production belief registry status")

    cases: list[StateBeliefBenchmarkCase] = []
    for case_id in BENCHMARK_CASES:
        state = _state_for_case(base_state, case_id)
        result = update_discrete_belief(state, model)
        expected_status, expected_evidence_status = _expectation(case_id)
        if result.status != expected_status:
            raise ValueError(
                f"{case_id}: result status {result.status} != {expected_status}"
            )
        if len(result.evidence_use) != 1:
            raise ValueError(f"{case_id}: expected exactly one evidence channel")
        if result.evidence_use[0].status != expected_evidence_status:
            raise ValueError(
                f"{case_id}: evidence status {result.evidence_use[0].status} "
                f"!= {expected_evidence_status}"
            )
        cases.append(
            StateBeliefBenchmarkCase(
                case_id=case_id,
                expected_status=expected_status,
                expected_evidence_status=expected_evidence_status,
                state_id=state.state_id,
                posterior=result.posterior,
                result_digest=_digest_result(result),
            )
        )

    benchmark_payload = {
        "model_id": model.model_id,
        "model_version": model.model_version,
        "cases": [
            {
                "case_id": case.case_id,
                "result_digest": case.result_digest,
            }
            for case in cases
        ],
        "production_registry_status": registry_status,
    }
    benchmark_id = "SBENCH-" + hashlib.sha256(
        json.dumps(
            benchmark_payload,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()[:24]

    return StateBeliefBenchmarkReport(
        schema_version="0.1",
        benchmark_id=benchmark_id,
        model_id=model.model_id,
        model_version=model.model_version,
        parameter_layer=model.parameter_layer,
        cases=tuple(cases),
        production_registry_status=registry_status,
        production_registry_model_count=0,
    )

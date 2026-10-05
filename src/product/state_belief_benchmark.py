"""PL3-S state belief fixture benchmark v0.1.

This benchmark checks deterministic posterior math and abstention contracts.
It is not an external predictive-accuracy benchmark.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from .acquired_state import compile_acquired_state
from .bayesian_belief import (
    compile_discrete_belief_model,
    update_discrete_belief,
)


_POSTERIOR_TOL = 1e-12


@dataclass(frozen=True)
class BeliefBenchmarkCaseResult:
    case_id: str
    passed: bool
    expected_status: str
    actual_status: str
    expected_posterior: tuple[tuple[str, float], ...]
    actual_posterior: tuple[tuple[str, float], ...]
    expected_evidence_statuses: tuple[str, ...]
    actual_evidence_statuses: tuple[str, ...]
    errors: tuple[str, ...]


@dataclass(frozen=True)
class BeliefBenchmarkReport:
    schema_version: str
    total: int
    passed: int
    failed: int
    results: tuple[BeliefBenchmarkCaseResult, ...]

    @property
    def all_passed(self) -> bool:
        return self.failed == 0


def _required_text(value: Any, field: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise ValueError(f"{field} is required")
    return text


def _posterior_tuple(value: Mapping[str, Any], field: str) -> tuple[tuple[str, float], ...]:
    out = []
    for key, raw in value.items():
        try:
            number = float(raw)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"{field}.{key} must be numeric") from exc
        out.append((str(key).strip(), number))
    return tuple(sorted(out))


def _posterior_close(
    expected: tuple[tuple[str, float], ...],
    actual: tuple[tuple[str, float], ...],
) -> bool:
    if [key for key, _ in expected] != [key for key, _ in actual]:
        return False
    return all(
        abs(exp - got) <= _POSTERIOR_TOL
        for (_, exp), (_, got) in zip(expected, actual)
    )


def run_state_belief_benchmark(
    document: Mapping[str, Any],
) -> BeliefBenchmarkReport:
    if str(document.get("schema_version", "")).strip() != "0.1":
        raise ValueError("belief benchmark schema_version must be 0.1")
    raw_cases = document.get("cases")
    if not isinstance(raw_cases, Sequence) or isinstance(raw_cases, (str, bytes)):
        raise ValueError("belief benchmark cases must be an array")

    results: list[BeliefBenchmarkCaseResult] = []
    seen: set[str] = set()

    for index, item in enumerate(raw_cases):
        if not isinstance(item, Mapping):
            raise ValueError(f"cases[{index}] must be an object")
        case_id = _required_text(item.get("case_id"), f"cases[{index}].case_id")
        if case_id in seen:
            raise ValueError(f"duplicate benchmark case_id: {case_id}")
        seen.add(case_id)

        state_payload = item.get("state")
        model_payload = item.get("model")
        expected = item.get("expected")
        if not isinstance(state_payload, Mapping):
            raise ValueError(f"{case_id}: state must be an object")
        if not isinstance(model_payload, Mapping):
            raise ValueError(f"{case_id}: model must be an object")
        if not isinstance(expected, Mapping):
            raise ValueError(f"{case_id}: expected must be an object")

        state = compile_acquired_state(state_payload)
        model = compile_discrete_belief_model(model_payload)

        first = update_discrete_belief(state, model)
        second = update_discrete_belief(state, model)

        expected_status = _required_text(
            expected.get("status"), f"{case_id}.expected.status"
        )
        expected_posterior_raw = expected.get("posterior")
        if not isinstance(expected_posterior_raw, Mapping):
            raise ValueError(f"{case_id}.expected.posterior must be an object")
        expected_posterior = _posterior_tuple(
            expected_posterior_raw, f"{case_id}.expected.posterior"
        )

        evidence_raw = expected.get("evidence_statuses", [])
        if not isinstance(evidence_raw, Sequence) or isinstance(
            evidence_raw, (str, bytes)
        ):
            raise ValueError(
                f"{case_id}.expected.evidence_statuses must be an array"
            )
        expected_evidence = tuple(str(value).strip() for value in evidence_raw)

        actual_evidence = tuple(item.status for item in first.evidence_use)
        errors: list[str] = []

        if first.to_dict() != second.to_dict():
            errors.append("NON_DETERMINISTIC_REPEAT")
        if first.status != expected_status:
            errors.append("STATUS_MISMATCH")
        if not _posterior_close(expected_posterior, first.posterior):
            errors.append("POSTERIOR_MISMATCH")
        if actual_evidence != expected_evidence:
            errors.append("EVIDENCE_STATUS_MISMATCH")

        results.append(
            BeliefBenchmarkCaseResult(
                case_id=case_id,
                passed=not errors,
                expected_status=expected_status,
                actual_status=first.status,
                expected_posterior=expected_posterior,
                actual_posterior=first.posterior,
                expected_evidence_statuses=expected_evidence,
                actual_evidence_statuses=actual_evidence,
                errors=tuple(errors),
            )
        )

    ordered = tuple(sorted(results, key=lambda item: item.case_id))
    passed = sum(1 for item in ordered if item.passed)
    return BeliefBenchmarkReport(
        schema_version="0.1",
        total=len(ordered),
        passed=passed,
        failed=len(ordered) - passed,
        results=ordered,
    )

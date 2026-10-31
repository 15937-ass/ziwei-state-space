"""Fail-closed production chart contract for canonical Zhongzhou/iztro snapshots."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping


CANONICAL_CHART_CONTRACT_ID = "ZHONGZHOU_IZTRO_JS_2_6_1_V1"

CONTRACT_PATH = (
    Path(__file__).resolve().parents[2]
    / "product"
    / "CANONICAL_CHART_CONTRACT_v1.0.json"
)


@dataclass(frozen=True)
class CanonicalChartValidation:
    ok: bool
    errors: tuple[str, ...] = ()


def load_canonical_chart_contract() -> Mapping[str, Any]:
    """Load the versioned machine-readable production chart contract."""
    with CONTRACT_PATH.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, Mapping):
        raise ValueError("canonical chart contract must be a JSON object")
    return payload


def validate_canonical_production_chart_snapshot(
    snapshot: Any,
) -> CanonicalChartValidation:
    """Validate production provenance/config; never repairs or defaults a chart."""
    errors: list[str] = []
    if not isinstance(snapshot, Mapping):
        return CanonicalChartValidation(
            False, ("production chart snapshot must be an object",)
        )

    try:
        contract = load_canonical_chart_contract()
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        return CanonicalChartValidation(
            False, (f"canonical chart contract unavailable: {exc}",)
        )

    expected_id = contract.get("contract_id")
    if expected_id != CANONICAL_CHART_CONTRACT_ID:
        errors.append("machine-readable canonical chart contract ID does not match code contract")
    if snapshot.get("chart_contract_id") != expected_id:
        errors.append(f"chart_contract_id must equal {expected_id}")

    if snapshot.get("test_only") is True:
        errors.append("test-only chart snapshots are not allowed in production")

    engine = snapshot.get("engine")
    if not isinstance(engine, Mapping):
        errors.append("engine must be an object for canonical production")
        engine = {}

    expected_engine = contract.get("production_engine", {})
    if not isinstance(expected_engine, Mapping):
        errors.append("canonical production_engine contract is malformed")
        expected_engine = {}

    for field in ("name", "version", "adapter_version"):
        expected = expected_engine.get(field)
        if engine.get(field) != expected:
            errors.append(f"engine.{field} must equal {expected}")

    if not isinstance(engine.get("source_revision"), str) or not engine.get(
        "source_revision", ""
    ).strip():
        errors.append("engine.source_revision must be a non-empty pinned provenance value")

    input_payload = snapshot.get("input")
    if not isinstance(input_payload, Mapping):
        errors.append("input must be an object for canonical production")
        input_payload = {}

    if input_payload.get("test_only") is True:
        errors.append("input.test_only chart snapshots are not allowed in production")

    expected_config = contract.get("chart_config", {})
    actual_config = input_payload.get("chart_config")
    if not isinstance(expected_config, Mapping):
        errors.append("canonical chart_config contract is malformed")
        expected_config = {}
    if not isinstance(actual_config, Mapping):
        errors.append("input.chart_config must be an explicit object")
        actual_config = {}

    for field, expected in expected_config.items():
        actual = actual_config.get(field)
        if isinstance(expected, bool):
            matches = actual is expected
        else:
            matches = actual == expected
        if not matches:
            errors.append(f"input.chart_config.{field} must equal {expected}")

    input_calendar = input_payload.get("input_calendar")
    entrypoint = input_payload.get("entrypoint")
    routes = contract.get("input_routes", {})
    route = routes.get(input_calendar) if isinstance(routes, Mapping) else None
    if not isinstance(route, Mapping):
        errors.append("input.input_calendar must be an explicitly supported calendar")
    elif entrypoint != route.get("entrypoint"):
        errors.append(
            f"input.entrypoint must equal {route.get('entrypoint')} "
            f"for {input_calendar} input"
        )

    return CanonicalChartValidation(not errors, tuple(errors))

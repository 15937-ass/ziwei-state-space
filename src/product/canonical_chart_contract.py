"""Fail-closed production chart contract for canonical Zhongzhou/iztro snapshots."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping


CANONICAL_CHART_CONTRACT_ID = "ZHONGZHOU_IZTRO_JS_2_6_1_V1"
CANONICAL_CHART_CONTRACT_VERSION = "1.0.0"
CANONICAL_SCHOOL = "zhongzhou"
CANONICAL_PRODUCTION_ENGINE = {
    "name": "iztro-js",
    "version": "2.6.1",
    "source_revision": "2c7ef9be669df7b19d1799f4dce335fed3794f78",
    "adapter_version": "0.2",
}
CANONICAL_CHART_CONFIG = {
    "algorithm": "zhongzhou",
    "astro_type": "heaven",
    "fix_leap": True,
    "day_divide": "forward",
    "year_divide": "normal",
    "horoscope_divide": "normal",
    "language": "zh-CN",
}
CANONICAL_INPUT_ROUTES = {
    "solar": {"input_calendar": "solar", "entrypoint": "astro.withOptions"},
    "lunar": {"input_calendar": "lunar", "entrypoint": "astro.byLunar"},
}

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
    expected_fields = {
        "contract_id": CANONICAL_CHART_CONTRACT_ID,
        "contract_version": CANONICAL_CHART_CONTRACT_VERSION,
        "status": "CANONICAL_PRODUCTION",
        "school": CANONICAL_SCHOOL,
        "production_engine": CANONICAL_PRODUCTION_ENGINE,
        "chart_config": CANONICAL_CHART_CONFIG,
        "input_routes": CANONICAL_INPUT_ROUTES,
        "temporal_scopes": [
            "decadal", "age", "yearly", "monthly", "daily", "hourly"
        ],
    }
    for field, expected in expected_fields.items():
        if payload.get(field) != expected:
            raise ValueError(
                f"canonical chart contract field drift: {field} does not match frozen v1.0"
            )
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

    if "test_only" in snapshot and snapshot.get("test_only") is not False:
        errors.append("test-only chart snapshots are not allowed in production")

    engine = snapshot.get("engine")
    if not isinstance(engine, Mapping):
        errors.append("engine must be an object for canonical production")
        engine = {}

    expected_engine = contract.get("production_engine", {})
    if not isinstance(expected_engine, Mapping):
        errors.append("canonical production_engine contract is malformed")
        expected_engine = {}

    for field in ("name", "version", "source_revision", "adapter_version"):
        expected = expected_engine.get(field)
        if engine.get(field) != expected:
            errors.append(f"engine.{field} must equal {expected}")

    input_payload = snapshot.get("input")
    if not isinstance(input_payload, Mapping):
        errors.append("input must be an object for canonical production")
        input_payload = {}

    if "test_only" in input_payload and input_payload.get("test_only") is not False:
        errors.append("input.test_only chart snapshots are not allowed in production")

    if input_payload.get("school") != contract.get("school"):
        errors.append(f"input.school must equal {contract.get('school')}")

    expected_config = contract.get("chart_config", {})
    actual_config = input_payload.get("chart_config")
    if not isinstance(expected_config, Mapping):
        errors.append("canonical chart_config contract is malformed")
        expected_config = {}
    if not isinstance(actual_config, Mapping):
        errors.append("input.chart_config must be an explicit object")
        actual_config = {}

    extra_config_fields = sorted(str(field) for field in actual_config if field not in expected_config)
    if extra_config_fields:
        errors.append("input.chart_config contains unsupported field(s): " + ", ".join(extra_config_fields))

    for field, expected in expected_config.items():
        actual = actual_config.get(field)
        if isinstance(expected, bool):
            matches = actual is expected
        else:
            matches = actual == expected
        if not matches:
            errors.append(f"input.chart_config.{field} must equal {expected}")

    # The legacy flattened fields must not contradict the canonical nested config.
    flattened_fields = {
        "algorithm": "algorithm",
        "astro_type": "astro_type",
        "fix_leap": "fix_leap",
        "day_divide": "day_divide",
        "year_divide": "year_divide",
        "horoscope_divide": "horoscope_divide",
        "language": "language",
    }
    for input_field, config_field in flattened_fields.items():
        if input_field in input_payload:
            if input_payload[input_field] != expected_config.get(config_field):
                errors.append(
                    f"input.{input_field} must equal canonical chart_config.{config_field}"
                )

    input_calendar = input_payload.get("input_calendar")
    entrypoint = input_payload.get("entrypoint")
    routes = contract.get("input_routes", {})
    route = (
        routes.get(input_calendar)
        if isinstance(routes, Mapping) and isinstance(input_calendar, str)
        else None
    )
    if not isinstance(route, Mapping):
        errors.append("input.input_calendar must be an explicitly supported calendar")
    else:
        if entrypoint != route.get("entrypoint"):
            errors.append(
                f"input.entrypoint must equal {route.get('entrypoint')} "
                f"for {input_calendar} input"
            )
        date_field = "solar_date" if input_calendar == "solar" else "lunar_date"
        if not isinstance(input_payload.get(date_field), str) or not input_payload.get(date_field, "").strip():
            errors.append(f"input.{date_field} is required for {input_calendar} input")

    return CanonicalChartValidation(not errors, tuple(errors))

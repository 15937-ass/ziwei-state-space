"""Fail-closed production chart contract for canonical Zhongzhou/iztro snapshots."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping


CANONICAL_CHART_CONTRACT_ID = "ZHONGZHOU_IZTRO_JS_2_6_1_V1_1"
CANONICAL_CHART_CONTRACT_VERSION = "1.1.0"
CANONICAL_SCHOOL = "zhongzhou"
CANONICAL_PRODUCTION_ENGINE = {
    "name": "iztro-js",
    "version": "2.6.1",
    "source_revision": "2c7ef9be669df7b19d1799f4dce335fed3794f78",
    "adapter_version": "0.3",
}
CANONICAL_CHART_CONFIG = {
    "algorithm": "zhongzhou",
    "astro_type": "heaven",
    "fix_leap": True,
    "day_divide": "current",
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
    / "CANONICAL_CHART_CONTRACT_v1.1.json"
)


def zhongzhou_time_index_from_true_solar_time(hour: int, minute: int) -> int:
    """Map an already-true-solar clock time to the canonical Zhongzhou time index.

    00:00-00:59 is early Zi (index 0); 23:00-23:59 is late Zi (index 12).
    The supplied calendar date is never advanced by this conversion.
    """
    if isinstance(hour, bool) or not isinstance(hour, int) or not 0 <= hour <= 23:
        raise ValueError("hour must be an integer from 0 through 23")
    if isinstance(minute, bool) or not isinstance(minute, int) or not 0 <= minute <= 59:
        raise ValueError("minute must be an integer from 0 through 59")
    if hour == 0:
        return 0
    if hour == 23:
        return 12
    return (hour + 1) // 2


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
        "time_input_policy": {
            "required_time_basis": "true_solar_time",
            "location_correction_applied_in_chart_engine": False,
            "birthplace_required_for_chart_generation": False,
            "future_location_conversion": "upstream_preprocessing_only",
        },
        "zi_day_boundary": {
            "late_zi_time_index": 12,
            "late_zi_clock_range": "23:00-23:59",
            "late_zi_date_attribution": "same_input_date",
            "early_zi_time_index": 0,
            "early_zi_clock_range": "00:00-00:59",
            "early_zi_date_attribution": "new_input_date",
            "engine_day_divide": "current",
        },
        "production_rules": {
            "chart_facts_generated_by": "iztro-js",
            "temporal_facts_generated_from_same_chart_instance": True,
            "llm_may_compute_or_modify_chart_facts": False,
            "manual_chart_edits_allowed": False,
            "fallback_production_engine_allowed": False,
            "differential_engines_are_production_fallbacks": False,
            "test_only_snapshots_allowed_in_production": False,
            "input_time_is_already_true_solar_time": True,
            "chart_engine_may_apply_location_correction": False,
        },
        "change_control": {
            "requires_explicit_pi_approval": True,
            "requires_new_contract_version": True,
            "requires_migration_plan": True,
            "requires_full_p1_chart_and_temporal_regression": True,
        },
    }
    for field, expected in expected_fields.items():
        if payload.get(field) != expected:
            raise ValueError(
                "canonical chart contract field drift: "
                f"{field} does not match frozen v1.1"
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

    time_policy = contract.get("time_input_policy", {})
    required_time_basis = (
        time_policy.get("required_time_basis")
        if isinstance(time_policy, Mapping)
        else None
    )
    if input_payload.get("time_basis") != required_time_basis:
        errors.append(f"input.time_basis must equal {required_time_basis}")
    if input_payload.get("location_correction_applied") is not False:
        errors.append("input.location_correction_applied must be false; v1.1 input is already true solar time")

    expected_config = contract.get("chart_config", {})
    actual_config = input_payload.get("chart_config")
    if not isinstance(expected_config, Mapping):
        errors.append("canonical chart_config contract is malformed")
        expected_config = {}
    if not isinstance(actual_config, Mapping):
        errors.append("input.chart_config must be an explicit object")
        actual_config = {}

    extra_config_fields = sorted(
        str(field) for field in actual_config if field not in expected_config
    )
    if extra_config_fields:
        errors.append(
            "input.chart_config contains unsupported field(s): "
            + ", ".join(extra_config_fields)
        )

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
        date_value = input_payload.get(date_field)
        if not isinstance(date_value, str) or not date_value.strip():
            errors.append(f"input.{date_field} is required for {input_calendar} input")

    return CanonicalChartValidation(not errors, tuple(errors))

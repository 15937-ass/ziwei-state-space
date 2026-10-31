import copy
import json
from pathlib import Path

import pytest

import src.product.career_inference_service as career_service
from src.product.canonical_chart_contract import (
    CANONICAL_CHART_CONTRACT_ID,
    validate_canonical_production_chart_snapshot,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "product" / "PL3T_TEMPORAL_ASSET_FIXTURE_v0.1.json"


def valid_snapshot():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_canonical_zhongzhou_iztro_snapshot_is_accepted():
    result = validate_canonical_production_chart_snapshot(valid_snapshot())
    assert result.ok is True
    assert result.errors == ()


@pytest.mark.parametrize(
    ("path", "value", "message"),
    [
        (("chart_contract_id",), "OTHER_CONTRACT", "chart_contract_id"),
        (("engine", "name"), "x-iztro-rust", "engine.name"),
        (("engine", "version"), "0.6.1", "engine.version"),
        (("engine", "adapter_version"), "0.1", "engine.adapter_version"),
        (("input", "chart_config", "algorithm"), "default", "algorithm"),
        (("input", "chart_config", "astro_type"), "earth", "astro_type"),
        (("input", "chart_config", "day_divide"), "current", "day_divide"),
        (("input", "chart_config", "year_divide"), "exact", "year_divide"),
        (("input", "chart_config", "horoscope_divide"), "exact", "horoscope_divide"),
        (("input", "chart_config", "language"), "en-US", "language"),
        (("input", "input_calendar"), "unknown", "input_calendar"),
        (("input", "entrypoint"), "astro.bySolar", "entrypoint"),
    ],
)
def test_noncanonical_chart_contract_is_rejected(path, value, message):
    snapshot = valid_snapshot()
    target = snapshot
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    result = validate_canonical_production_chart_snapshot(snapshot)
    assert result.ok is False
    assert any(message in error for error in result.errors)


def test_false_fix_leap_is_rejected():
    snapshot = valid_snapshot()
    snapshot["input"]["chart_config"]["fix_leap"] = False
    result = validate_canonical_production_chart_snapshot(snapshot)
    assert not result.ok
    assert any("fix_leap" in error for error in result.errors)


def test_missing_contract_metadata_fails_closed():
    snapshot = valid_snapshot()
    del snapshot["chart_contract_id"]
    del snapshot["input"]["chart_config"]
    del snapshot["input"]["entrypoint"]
    del snapshot["input"]["input_calendar"]
    result = validate_canonical_production_chart_snapshot(snapshot)
    assert not result.ok
    assert any("chart_contract_id" in error for error in result.errors)
    assert any("input.chart_config" in error for error in result.errors)


def test_test_only_artifacts_are_rejected():
    snapshot = valid_snapshot()
    snapshot["test_only"] = True
    result = validate_canonical_production_chart_snapshot(snapshot)
    assert not result.ok
    assert any("test-only" in error for error in result.errors)


def test_production_service_rejects_noncanonical_chart_before_loading_providers(monkeypatch):
    def unexpected_provider_load(*args, **kwargs):
        raise AssertionError("provider must not load before canonical chart validation")

    monkeypatch.setattr(
        career_service,
        "load_default_career_natal_provider",
        unexpected_provider_load,
    )
    snapshot = valid_snapshot()
    snapshot["input"]["chart_config"]["algorithm"] = "default"

    with pytest.raises(ValueError, match="non-canonical production chart snapshot"):
        career_service.run_career_inference(
            ROOT,
            snapshot,
            target_id="T-DEMO",
            question="canonical chart fail-closed test",
        )


def test_canonical_contract_id_is_stable():
    assert CANONICAL_CHART_CONTRACT_ID == "ZHONGZHOU_IZTRO_JS_2_6_1_V1"

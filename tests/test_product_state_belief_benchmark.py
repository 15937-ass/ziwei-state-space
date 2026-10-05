import json
from pathlib import Path

import pytest

from src.product.state_belief_benchmark import (
    BENCHMARK_CASES,
    run_state_belief_benchmark,
)

ROOT = Path(__file__).resolve().parents[1]
BENCH_FIXTURE = ROOT / "product/PL3S_STATE_BELIEF_BENCHMARK_FIXTURES_v0.1.json"
REGISTRY = ROOT / "product/PL3S_BELIEF_MODEL_REGISTRY_v0.1.json"


def test_frozen_benchmark_cases_match_contract_fixture():
    document = json.loads(BENCH_FIXTURE.read_text(encoding="utf-8"))
    fixture_cases = tuple(item["case_id"] for item in document["cases"])
    assert fixture_cases == BENCHMARK_CASES
    assert document["parameter_policy"] == "TEST_FIXTURE_ONLY"
    assert document["empirical_accuracy_claimed"] is False


def test_benchmark_reproduces_all_expected_abstention_boundaries():
    report = run_state_belief_benchmark()
    by_case = {item.case_id: item for item in report.cases}

    assert by_case["AVAILABLE_EMPLOYED"].expected_status == "UPDATED"
    assert by_case["AVAILABLE_EMPLOYED"].expected_evidence_status == "USED"

    assert by_case["MISSING_EMPLOYMENT"].expected_status == "NO_USABLE_EVIDENCE"
    assert by_case["MISSING_EMPLOYMENT"].expected_evidence_status == "SKIPPED_MISSING"

    assert by_case["CONFLICTING_EMPLOYMENT"].expected_evidence_status == "SKIPPED_CONFLICT"
    assert by_case["LOW_CONFIDENCE_EMPLOYMENT"].expected_evidence_status == "SKIPPED_CONFIDENCE"
    assert by_case["UNMODELLED_EMPLOYMENT_VALUE"].expected_evidence_status == "SKIPPED_UNMODELLED_VALUE"


def test_available_case_uses_test_fixture_math_only():
    report = run_state_belief_benchmark()
    case = next(item for item in report.cases if item.case_id == "AVAILABLE_EMPLOYED")
    assert dict(case.posterior) == {"STABLE": 0.8, "TRANSITIONING": 0.2}
    assert report.parameter_layer == "TEST_FIXTURE"
    assert report.empirical_accuracy_claimed is False
    assert report.production_calibration_claimed is False


def test_no_usable_evidence_cases_preserve_prior():
    report = run_state_belief_benchmark()
    for item in report.cases:
        if item.expected_status == "NO_USABLE_EVIDENCE":
            assert dict(item.posterior) == {"STABLE": 0.5, "TRANSITIONING": 0.5}


def test_same_inputs_produce_same_benchmark_id_and_digests():
    first = run_state_belief_benchmark()
    second = run_state_belief_benchmark()
    assert first.benchmark_id == second.benchmark_id
    assert [item.result_digest for item in first.cases] == [
        item.result_digest for item in second.cases
    ]


def test_production_registry_must_stay_empty_for_this_benchmark(tmp_path):
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    registry["models"] = [{"model_id": "NOT-ALLOWED-HERE"}]
    bad = tmp_path / "registry.json"
    bad.write_text(json.dumps(registry), encoding="utf-8")
    with pytest.raises(ValueError, match="remain empty"):
        run_state_belief_benchmark(production_registry_path=bad)


def test_benchmark_report_is_not_accuracy_claim():
    report = run_state_belief_benchmark()
    payload = report.to_dict()
    assert payload["empirical_accuracy_claimed"] is False
    assert payload["production_calibration_claimed"] is False
    assert payload["production_registry_model_count"] == 0

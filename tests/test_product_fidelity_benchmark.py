import copy
import json
from pathlib import Path

import pytest

from src.product.fidelity_benchmark import (
    build_canonical_and_method_fidelity_benchmark,
    validate_fidelity_benchmark_report,
)

ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = (
    ROOT
    / "product"
    / "benchmarks"
    / "CANONICAL_AND_METHOD_FIDELITY_BENCHMARK_V0_1.json"
)


def _read_report():
    return json.loads(REPORT_PATH.read_text(encoding="utf-8"))


def test_committed_benchmark_report_matches_pinned_deterministic_build():
    assert _read_report() == build_canonical_and_method_fidelity_benchmark()


def test_canonical_and_expert_method_scores_remain_separate_and_unscored():
    report = _read_report()
    assert report["overall"]["combined_fidelity_score"] is None
    assert report["canonical_fidelity"]["score"] is None
    assert report["expert_method_fidelity"]["score"] is None
    assert report["overall"]["predictive_validity"] == "NOT_EVALUATED"


def test_empty_production_registries_are_blocked_not_covered_or_passed():
    report = _read_report()
    assets = report["canonical_fidelity"]["asset_accounting"]
    blocked = [
        asset
        for asset in assets
        if asset.get("blocked_by_empty_registry") is True
    ]
    assert len(blocked) == 3
    for asset in blocked:
        assert asset["disposition"] == "BLOCKED"
        assert asset["covered_assets"] == 0
        assert asset["registered_assets"] == 0
        assert asset["blocked_by_knowledge_dependency"] is True


def test_zero_ready_expert_replay_cannot_receive_a_method_fidelity_score():
    report = _read_report()
    assert report["expert_method_fidelity"]["replay_readiness"][
        "full_expert_replay_ready_cases"
    ] == 0
    invalid = copy.deepcopy(report)
    invalid["expert_method_fidelity"]["score"] = 0.95
    with pytest.raises(ValueError, match="expert-method fidelity score"):
        validate_fidelity_benchmark_report(invalid)


def test_empty_registry_cannot_be_relabelled_as_a_fidelity_pass():
    report = _read_report()
    invalid = copy.deepcopy(report)
    temporal = next(
        item
        for item in invalid["canonical_fidelity"]["asset_accounting"]
        if item["metric_id"] == "production_temporal_response_coverage"
    )
    temporal["disposition"] = "MEASURED"
    temporal["status"] = "PASS"
    with pytest.raises(ValueError, match="empty production registry"):
        validate_fidelity_benchmark_report(invalid)


def test_target_anchor_verification_is_not_full_chart_equivalence():
    report = _read_report()
    chart = report["canonical_fidelity"]["asset_accounting"][0]
    assert chart["eligible_assets"] == 24
    assert chart["covered_assets"] == 11
    assert chart["blocked_assets"] == 13
    assert chart["status"] == "TARGET_ANCHOR_ONLY"
    assert chart["full_source_chart_equivalence_verified"] is False

    invalid = copy.deepcopy(report)
    invalid["canonical_fidelity"]["asset_accounting"][0][
        "full_source_chart_equivalence_verified"
    ] = True
    with pytest.raises(ValueError, match="full-source-chart equivalence"):
        validate_fidelity_benchmark_report(invalid)


def test_method_readiness_and_scope_review_counts_reconcile():
    report = _read_report()
    method = report["expert_method_fidelity"]
    assert method["case_count"] == 24
    assert method["method_pattern_count"] == 6
    assert method["assessment_count"] == 144
    assert method["scope_review"]["justified_bindings"] == 0
    assert method["replay_readiness"]["retrieval_ready_cases"] == 24
    assert method["replay_readiness"]["action_selection_ready_cases"] == 24
    assert method["replay_readiness"]["full_expert_replay_ready_cases"] == 0
    assert sum(method["scope_review"]["assessment_outcomes"].values()) == 144


def test_unknown_canonical_runtime_count_is_not_silently_zero():
    report = _read_report()
    metric = report["canonical_fidelity"]["dimensions"][
        "unknown_or_insufficient_evidence_count"
    ]
    assert metric["disposition"] == "NOT_MEASURED"
    assert metric["value"] is None


def test_method_insufficient_evidence_counts_are_assessment_level_only():
    report = _read_report()
    metric = report["expert_method_fidelity"]["score_dimensions"][
        "unknown_or_insufficient_evidence_count"
    ]
    assert metric["disposition"] == "MEASURED"
    assert metric["assessment_count"] == 144
    assert metric["insufficient_source_evidence_assessments"] == 64
    assert metric["missing_context_binding_assessments"] == 24
    assert metric["deferred_symbolic_interpretation_assessments"] == 48
    assert metric["semantic_only_relevance_assessments"] == 8

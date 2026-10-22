"""Versioned, fail-closed baseline for canonical and expert-method fidelity.

This module reports coverage/readiness from pinned Product artifacts. It deliberately
does not manufacture fidelity scores, canonical meaning, probabilities, or predictions.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
OUTPUT_PATH = ROOT / "product" / "benchmarks" / "CANONICAL_AND_METHOD_FIDELITY_BENCHMARK_V0_1.json"

INPUTS: tuple[tuple[str, str, str], ...] = (
    (
        "case_inventory",
        "product/expert_cases/wang_tingzhi/CASE_SOURCE_INVENTORY_v0.1.json",
        "804b3163b40ed19c8626427ce988fb12b6f85763",
    ),
    (
        "method_patterns",
        "product/expert_cases/wang_tingzhi/METHOD_PATTERNS_v0.1.json",
        "f81cd49e74bd7fb0a960d40b63f7d014c839f287",
    ),
    (
        "full_chart_materialization",
        "product/expert_cases/wang_tingzhi/FULL_CHART_MATERIALIZATION_V0_1B.json",
        "3778e5f3d66c1e5ab44461360b6d9f71b3f8be56",
    ),
    (
        "scope_review",
        "product/WANG_METHOD_SCOPE_REVIEW_V0_1C.json",
        "73b020a161fce8076481316a34f053e422f4270e",
    ),
    (
        "readiness",
        "product/WANG_METHOD_POLICY_READINESS_v0.3.json",
        "a4f6d395f736a393955320aeef15f0ade2019409",
    ),
    (
        "temporal_reaction_registry",
        "product/PL3T_TEMPORAL_REACTION_REGISTRY_v0.1.json",
        "6749bd569dca1f593a7e437bd6a86c81a7d578c8",
    ),
    (
        "manifestation_ontology_registry",
        "product/PL3M_MANIFESTATION_ONTOLOGY_REGISTRY_v0.1.json",
        "d1f5f5035ff7e5b51431fc2abc43ac844c84e2bf",
    ),
    (
        "manifestation_mapping_registry",
        "product/PL3M_MANIFESTATION_MAPPING_REGISTRY_v0.1.json",
        "367bc603b33d24bda7c66023c7e386f8cd0528eb",
    ),
)

METRIC_DEFINITIONS: dict[str, dict[str, Any]] = {
    "chart_materialization_coverage": {
        "definition": "Cases with a separate pinned-engine chart artifact and reviewed target-anchor verification; this is not full-source-chart equivalence.",
        "source_roles": ["case_inventory", "full_chart_materialization", "scope_review", "readiness"],
    },
    "production_temporal_response_coverage": {
        "definition": "Source-reviewed temporal-reaction rules available in the production reaction registry.",
        "source_roles": ["temporal_reaction_registry"],
    },
    "production_manifestation_ontology_coverage": {
        "definition": "Canonical manifestation ontology nodes available to Product.",
        "source_roles": ["manifestation_ontology_registry"],
    },
    "production_manifestation_mapping_coverage": {
        "definition": "Canonical manifestation mappings available to Product.",
        "source_roles": ["manifestation_mapping_registry"],
    },
    "expert_replay_readiness": {
        "definition": "Wang cases for which the current runtime can perform a full source-grounded expert replay, not merely retrieval or action selection.",
        "source_roles": ["readiness", "scope_review"],
    },
    "method_scope_binding": {
        "definition": "Case-to-MethodPattern bindings justified by exact target scope and explicit source linkage.",
        "source_roles": ["scope_review"],
    },
    "trace_completeness": {
        "definition": "Completeness of an executed canonical or expert replay trace against its eligible evidence and expected partial order.",
        "source_roles": ["scope_review", "readiness"],
    },
    "deterministic_reproducibility": {
        "definition": "Repeatability of the Product behavior under identical pinned inputs; report-builder determinism is not a substitute for runtime fidelity.",
        "source_roles": ["case_inventory", "method_patterns", "scope_review", "readiness", "temporal_reaction_registry", "manifestation_ontology_registry", "manifestation_mapping_registry"],
    },
    "contradiction_preservation": {
        "definition": "Whether conflicting source-supported claims remain separately represented through the canonical runtime and evidence package.",
        "source_roles": ["scope_review"],
    },
    "unknown_or_insufficient_evidence_count": {
        "definition": "Explicit count of source-insufficient or context-blocked benchmark assessments; it is not a count of real-world prediction errors.",
        "source_roles": ["scope_review"],
    },
    "method_fidelity_score": {
        "definition": "A comparison score between eligible blind machine InferenceTrace outputs and source-demonstrated expert reasoning graphs.",
        "source_roles": ["readiness", "scope_review"],
    },
    "critical_evidence_recall": {
        "definition": "Recall of source-supported expert-critical evidence in an eligible blind machine trace.",
        "source_roles": ["scope_review", "readiness"],
    },
    "wrong_evidence_selection": {
        "definition": "Rate or count of selected evidence that is not supported by the held-out case's permitted input evidence.",
        "source_roles": ["scope_review", "readiness"],
    },
    "next_action_and_branch_choice": {
        "definition": "Compatibility of the machine's next action and branch choice with the source-demonstrated expert reasoning graph under its permitted partial order.",
        "source_roles": ["scope_review", "readiness"],
    },
    "time_depth_choice": {
        "definition": "Compatibility of the selected natal/decade/year time depth with the source-demonstrated expert reasoning graph.",
        "source_roles": ["scope_review", "readiness"],
    },
    "stop_abstention_and_partial_order_compatibility": {
        "definition": "Compatibility of terminal STOP/ABSTAIN decisions and trace ordering with the source-demonstrated expert reasoning graph.",
        "source_roles": ["scope_review", "readiness"],
    },
}

def _git_blob_sha(raw: bytes) -> str:
    header = b"blob " + str(len(raw)).encode("ascii") + b"\0"
    return hashlib.sha1(header + raw).hexdigest()


def _load_pinned_inputs(root: Path) -> tuple[dict[str, Any], list[dict[str, str]]]:
    payloads: dict[str, Any] = {}
    sources: list[dict[str, str]] = []
    for role, relative_path, expected_sha in INPUTS:
        path = root / relative_path
        raw = path.read_bytes()
        observed_sha = _git_blob_sha(raw)
        if observed_sha != expected_sha:
            raise ValueError(
                f"{relative_path}: pinned benchmark input changed; expected Git blob "
                f"{expected_sha}, observed {observed_sha}. Create a new benchmark version."
            )
        payloads[role] = json.loads(raw.decode("utf-8"))
        sources.append(
            {"role": role, "path": relative_path, "git_blob_sha": expected_sha}
        )
    return payloads, sources


def _build_report(
    payloads: Mapping[str, Mapping[str, Any]],
    source_artifacts: Sequence[Mapping[str, str]],
) -> dict[str, Any]:
    inventory = payloads["case_inventory"]
    patterns = payloads["method_patterns"]
    charts = payloads["full_chart_materialization"]
    review = payloads["scope_review"]
    readiness = payloads["readiness"]
    reaction = payloads["temporal_reaction_registry"]
    ontology = payloads["manifestation_ontology_registry"]
    mapping = payloads["manifestation_mapping_registry"]

    case_count = len(inventory.get("cases", []))
    pattern_rows = patterns.get("method_patterns", [])
    pattern_count = len(pattern_rows)
    review_summary = review.get("summary", {})
    readiness_summary = readiness.get("summary", {})
    chart_summary = charts.get("summary", {})
    outcome_counts = dict(review_summary.get("review_outcome_counts", {}))
    assessment_count = review_summary.get("assessment_count")

    if case_count != 24 or pattern_count != 6:
        raise ValueError("benchmark v0.1 is pinned to 24 Wang cases and six MethodPatterns")
    if review_summary.get("case_count") != case_count:
        raise ValueError("scope-review case count does not match the source inventory")
    if review_summary.get("method_pattern_count") != pattern_count:
        raise ValueError("scope-review MethodPattern count does not match the method corpus")
    if assessment_count != case_count * pattern_count:
        raise ValueError("scope-review assessment matrix is incomplete")
    if sum(outcome_counts.values()) != assessment_count:
        raise ValueError("scope-review outcome counts do not reconcile to the assessment total")
    if readiness_summary.get("fold_count") != case_count:
        raise ValueError("LOCO readiness fold count does not match the case inventory")
    if (
        chart_summary.get("source_cases_total"),
        chart_summary.get("full_chart_materialized"),
        chart_summary.get("not_materialized"),
    ) != (case_count, 11, 13):
        raise ValueError("benchmark v0.1 expects the reviewed 11/13 chart-materialization split")
    if (
        review_summary.get("full_chart_materialized_case_count"),
        review_summary.get("full_chart_unmaterialized_case_count"),
    ) != (11, 13):
        raise ValueError("scope review does not preserve the 11/13 materialization split")
    if (
        readiness_summary.get("full_chart_materialized_fold_count"),
        readiness_summary.get("full_chart_blocked_fold_count"),
        readiness_summary.get("full_expert_replay_ready"),
    ) != (11, 13, 0):
        raise ValueError("readiness v0.3 no longer matches the pinned replay-readiness baseline")
    if (
        review_summary.get("exact_target_domain_matches"),
        review_summary.get("explicit_case_to_pattern_source_links"),
        review_summary.get("proposed_binding_count"),
    ) != (0, 0, 0):
        raise ValueError("benchmark v0.1 requires the accepted zero-binding scope review")
    if any(row.get("allowed_use") != "SEMANTIC_ONLY" for row in pattern_rows):
        raise ValueError("source MethodPattern allowed_use changed; create a new benchmark version")
    if reaction.get("rules") != [] or "EMPTY" not in str(reaction.get("status", "")):
        raise ValueError("temporal reaction registry changed; create a new benchmark version")
    if ontology.get("nodes") != [] or not str(ontology.get("registry_status", "")).startswith("EMPTY"):
        raise ValueError("manifestation ontology registry changed; create a new benchmark version")
    if mapping.get("mappings") != [] or not str(mapping.get("registry_status", "")).startswith("EMPTY"):
        raise ValueError("manifestation mapping registry changed; create a new benchmark version")

    temporal_status = str(reaction.get("status", ""))
    ontology_status = str(ontology.get("registry_status", ""))
    mapping_status = str(mapping.get("registry_status", ""))
    materialized_cases = chart_summary["full_chart_materialized"]
    unmaterialized_cases = chart_summary["not_materialized"]
    replay_ready = readiness_summary["full_expert_replay_ready"]

    report: dict[str, Any] = {
        "schema_version": "0.1",
        "artifact_id": "CANONICAL_AND_METHOD_FIDELITY_BENCHMARK_V0_1",
        "benchmark_type": "VERSIONED_COVERAGE_AND_READINESS_BASELINE",
        "overall": {
            "status": "BASELINE_ONLY_WITH_BLOCKERS",
            "combined_fidelity_score": None,
            "predictive_validity": "NOT_EVALUATED",
            "claim_boundary": "This artifact reports current coverage/readiness and explicit blockers; it does not establish full canonical fidelity, expert-method fidelity, or real-world predictive validity.",
        },
        "source_artifacts": [dict(item) for item in source_artifacts],
        "canonical_fidelity": {
            "disposition": "BLOCKED",
            "status": "PARTIAL_COVERAGE_WITH_BLOCKED_DYNAMIC_CONTENT",
            "score": None,
            "asset_accounting": [
                {
                    "metric_id": "chart_materialization_coverage",
                    "asset_kind": "Wang source-case chart reconstruction",
                    "eligible_assets": case_count,
                    "covered_assets": materialized_cases,
                    "blocked_assets": unmaterialized_cases,
                    "disposition": "MEASURED",
                    "status": "TARGET_ANCHOR_ONLY",
                    "coverage_definition": "A covered case has a separate pinned-engine chart artifact and a reviewed target-palace identity plus fourteen-major-star anchor. This is not full-source-chart equivalence.",
                    "full_source_chart_equivalence_verified": False,
                    "evidence_refs": [
                        "product/expert_cases/wang_tingzhi/FULL_CHART_MATERIALIZATION_V0_1B.json",
                        "product/WANG_METHOD_SCOPE_REVIEW_V0_1C.json",
                        "product/WANG_METHOD_POLICY_READINESS_v0.3.json",
                    ],
                },
                {
                    "metric_id": "production_temporal_response_coverage",
                    "asset_kind": "Production temporal-reaction rules",
                    "eligible_assets": None,
                    "covered_assets": 0,
                    "blocked_assets": None,
                    "registered_assets": len(reaction.get("rules", [])),
                    "disposition": "BLOCKED",
                    "status": "EMPTY_PRODUCTION_REGISTRY",
                    "blocked_by_empty_registry": True,
                    "blocked_by_knowledge_dependency": True,
                    "registry_status": temporal_status,
                    "evidence_refs": ["product/PL3T_TEMPORAL_REACTION_REGISTRY_v0.1.json"],
                },
                {
                    "metric_id": "production_manifestation_ontology_coverage",
                    "asset_kind": "Production manifestation ontology nodes",
                    "eligible_assets": None,
                    "covered_assets": 0,
                    "blocked_assets": None,
                    "registered_assets": len(ontology.get("nodes", [])),
                    "disposition": "BLOCKED",
                    "status": "EMPTY_PRODUCTION_REGISTRY",
                    "blocked_by_empty_registry": True,
                    "blocked_by_knowledge_dependency": True,
                    "registry_status": ontology_status,
                    "blocked_reason": ontology.get("blocked_reason"),
                    "evidence_refs": ["product/PL3M_MANIFESTATION_ONTOLOGY_REGISTRY_v0.1.json"],
                },
                {
                    "metric_id": "production_manifestation_mapping_coverage",
                    "asset_kind": "Production manifestation mappings",
                    "eligible_assets": None,
                    "covered_assets": 0,
                    "blocked_assets": None,
                    "registered_assets": len(mapping.get("mappings", [])),
                    "disposition": "BLOCKED",
                    "status": "EMPTY_PRODUCTION_REGISTRY",
                    "blocked_by_empty_registry": True,
                    "blocked_by_knowledge_dependency": True,
                    "registry_status": mapping_status,
                    "blocked_reason": mapping.get("blocked_reason"),
                    "evidence_refs": ["product/PL3M_MANIFESTATION_MAPPING_REGISTRY_v0.1.json"],
                },
            ],
            "dimensions": {
                "source_to_runtime_trace_completeness": {
                    "metric_id": "trace_completeness",
                    "disposition": "NOT_MEASURED",
                    "value": None,
                    "reason": "This baseline does not execute an end-to-end source-to-rule-to-runtime-to-evidence trace audit.",
                    "evidence_refs": [],
                },
                "deterministic_reproducibility": {
                    "metric_id": "deterministic_reproducibility",
                    "disposition": "NOT_MEASURED",
                    "value": None,
                    "reason": "The report builder is regression-tested for determinism; canonical runtime-wide reproducibility is not measured by this artifact.",
                    "evidence_refs": ["tests/test_product_fidelity_benchmark.py"],
                },
                "contradiction_preservation": {
                    "metric_id": "contradiction_preservation",
                    "disposition": "NOT_MEASURED",
                    "value": None,
                    "reason": "No benchmark-wide contradiction/counterevidence trace comparison is executed in this baseline.",
                    "evidence_refs": [],
                },
                "unknown_or_insufficient_evidence_count": {
                    "metric_id": "unknown_or_insufficient_evidence_count",
                    "disposition": "NOT_MEASURED",
                    "value": None,
                    "reason": "A canonical-runtime-wide count is not available from the pinned artifacts; it is not silently treated as zero.",
                    "evidence_refs": [],
                },
            },
        },
        "expert_method_fidelity": {
            "disposition": "BLOCKED",
            "status": "NOT_SCORABLE_FULL_EXPERT_REPLAY_NOT_READY",
            "score": None,
            "case_count": case_count,
            "method_pattern_count": pattern_count,
            "assessment_count": assessment_count,
            "asset_accounting": [
                {
                    "metric_id": "expert_replay_readiness",
                    "asset_kind": "Wang expert replay cases",
                    "eligible_assets": case_count,
                    "covered_assets": replay_ready,
                    "blocked_assets": case_count - replay_ready,
                    "disposition": "BLOCKED",
                    "status": "FULL_EXPERT_REPLAY_NOT_READY",
                    "coverage_definition": "A case counts as covered only when the runtime can emit a source-grounded blind InferenceTrace eligible for comparison with its ExpertReasoningGraph; retrieval/action-selection readiness alone does not count.",
                    "evidence_refs": ["product/WANG_METHOD_POLICY_READINESS_v0.3.json"],
                },
                {
                    "metric_id": "method_scope_binding",
                    "asset_kind": "Case × MethodPattern source-scope assessments",
                    "eligible_assets": assessment_count,
                    "covered_assets": assessment_count,
                    "blocked_assets": 0,
                    "disposition": "MEASURED",
                    "status": "SOURCE_SCOPE_REVIEW_COMPLETE_NOT_METHOD_FIDELITY_SCORE",
                    "coverage_definition": "Coverage means the source-bounded scope review assessed every case-pattern pair; it does not mean a binding was justified or expert-method fidelity was measured.",
                    "evidence_refs": ["product/WANG_METHOD_SCOPE_REVIEW_V0_1C.json"],
                },
            ],
            "blocker_accounting": {
                "empty_registry_blockers": {
                    "disposition": "NOT_APPLICABLE",
                    "count": 0,
                    "reason": "Temporal-response and manifestation registries are reported under Canonical Fidelity; they are not the direct blocker for the current Wang method replay.",
                },
                "knowledge_dependency_blockers": {
                    "disposition": "NOT_APPLICABLE",
                    "count": 0,
                    "reason": "The current expert replay is blocked by chart materialization, case-target method scope, and runtime evidence status rather than the Kr/M0 registry dependencies.",
                },
                "replay_blocker_classes": readiness_summary["remaining_blocker_classes"],
            },
            "scope_review": {
                "exact_target_domain_matches": review_summary["exact_target_domain_matches"],
                "explicit_case_to_pattern_source_links": review_summary["explicit_case_to_pattern_source_links"],
                "justified_bindings": review_summary["proposed_binding_count"],
                "all_source_patterns_remain_semantic_only": True,
                "assessment_outcomes": outcome_counts,
            },
            "replay_readiness": {
                "retrieval_ready_cases": readiness_summary["retrieval_ready"],
                "action_selection_ready_cases": readiness_summary["action_selection_ready"],
                "full_expert_replay_ready_cases": replay_ready,
                "full_expert_replay_blocked_cases": case_count - replay_ready,
                "target_palace_materialized_cases": readiness_summary["materialized_target_palace_fold_count"],
                "runtime_target_chart_blocked_cases": readiness_summary["method_policy_runtime_target_chart_blocked_fold_count"],
                "full_chart_materialized_cases": readiness_summary["full_chart_materialized_fold_count"],
                "full_chart_unmaterialized_cases": readiness_summary["full_chart_blocked_fold_count"],
            },
            "score_dimensions": {
                "critical_evidence_recall": {
                    "metric_id": "critical_evidence_recall",
                    "disposition": "BLOCKED",
                    "value": None,
                    "reason": "No eligible full expert replay traces are available for comparison.",
                    "evidence_refs": ["product/WANG_METHOD_POLICY_READINESS_v0.3.json"],
                },
                "wrong_evidence_selection": {
                    "metric_id": "wrong_evidence_selection",
                    "disposition": "BLOCKED",
                    "value": None,
                    "reason": "No eligible full expert replay traces are available for comparison.",
                    "evidence_refs": ["product/WANG_METHOD_POLICY_READINESS_v0.3.json"],
                },
                "next_action_and_branch_choice": {
                    "metric_id": "next_action_and_branch_choice",
                    "disposition": "BLOCKED",
                    "value": None,
                    "reason": "No justified case-target MethodPattern bindings exist in the accepted scope review.",
                    "evidence_refs": ["product/WANG_METHOD_SCOPE_REVIEW_V0_1C.json"],
                },
                "time_depth_choice": {
                    "metric_id": "time_depth_choice",
                    "disposition": "BLOCKED",
                    "value": None,
                    "reason": "No eligible full expert replay traces are available for comparison.",
                    "evidence_refs": ["product/WANG_METHOD_POLICY_READINESS_v0.3.json"],
                },
                "stop_abstention_and_partial_order_compatibility": {
                    "metric_id": "stop_abstention_and_partial_order_compatibility",
                    "disposition": "BLOCKED",
                    "value": None,
                    "reason": "Current INSPECT-to-ABSTAIN traces demonstrate fail-closed behavior only; they do not measure fidelity to a fully replayable expert graph.",
                    "evidence_refs": ["product/WANG_METHOD_POLICY_READINESS_v0.3.json"],
                },
                "trace_completeness": {
                    "metric_id": "trace_completeness",
                    "disposition": "BLOCKED",
                    "value": None,
                    "reason": "FULL_EXPERT_REPLAY_READY is 0/24, so expert trace completeness cannot be scored.",
                    "evidence_refs": ["product/WANG_METHOD_POLICY_READINESS_v0.3.json"],
                },
                "deterministic_reproducibility": {
                    "metric_id": "deterministic_reproducibility",
                    "disposition": "NOT_MEASURED",
                    "value": None,
                    "reason": "Determinism of the replayed expert method is not measured without eligible replay traces.",
                    "evidence_refs": [],
                },
                "contradiction_preservation": {
                    "metric_id": "contradiction_preservation",
                    "disposition": "NOT_MEASURED",
                    "value": None,
                    "reason": "No eligible replay trace comparison is available.",
                    "evidence_refs": [],
                },
                "unknown_or_insufficient_evidence_count": {
                    "metric_id": "unknown_or_insufficient_evidence_count",
                    "disposition": "MEASURED",
                    "assessment_count": assessment_count,
                    "insufficient_source_evidence_assessments": outcome_counts["INSUFFICIENT_SOURCE_EVIDENCE"],
                    "missing_context_binding_assessments": outcome_counts["MISSING_CONTEXT_BINDING"],
                    "deferred_symbolic_interpretation_assessments": outcome_counts["DEFERRED_SYMBOLIC_INTERPRETATION"],
                    "semantic_only_relevance_assessments": outcome_counts["SEMANTIC_ONLY_RELEVANCE"],
                    "reason": "These are scope-review disposition counts across case-pattern assessments, not real-world event outcomes or predictive errors.",
                    "evidence_refs": ["product/WANG_METHOD_SCOPE_REVIEW_V0_1C.json"],
                },
            },
        },
        "metric_definitions": METRIC_DEFINITIONS,
        "claim_boundaries": [
            "Readiness is not expert-method fidelity.",
            "Target-anchor verification is not full-source-chart equivalence.",
            "An empty production registry is blocked/uncovered, never fidelity PASS.",
            "SEMANTIC_ONLY source MethodPatterns do not create runtime effects.",
            "Textbook conclusions and outcomes are not real-world predictive ground truth.",
            "No empirical probability, numeric weight, causal effect, or predictive-validity claim is made.",
        ],
    }
    validate_fidelity_benchmark_report(report)
    return report


def validate_fidelity_benchmark_report(report: Mapping[str, Any]) -> None:
    overall = report.get("overall", {})
    canonical = report.get("canonical_fidelity", {})
    method = report.get("expert_method_fidelity", {})
    if overall.get("combined_fidelity_score") is not None:
        raise ValueError("baseline report must not emit a combined fidelity score")
    definitions = report.get("metric_definitions", {})
    for asset in canonical.get("asset_accounting", []):
        if asset.get("metric_id") not in definitions:
            raise ValueError("every canonical asset metric must have a definition")
    for dimension in canonical.get("dimensions", {}).values():
        if dimension.get("metric_id") not in definitions:
            raise ValueError("every canonical dimension must have a definition")
    for asset in method.get("asset_accounting", []):
        if asset.get("metric_id") not in definitions:
            raise ValueError("every expert-method asset metric must have a definition")
    for dimension in method.get("score_dimensions", {}).values():
        if dimension.get("metric_id") not in definitions:
            raise ValueError("every expert-method score dimension must have a definition")
    if canonical.get("score") is not None:
        raise ValueError("canonical fidelity score is not produced by this readiness baseline")
    if method.get("score") is not None:
        raise ValueError("expert-method fidelity score requires eligible trace comparisons")
    readiness = method.get("replay_readiness", {})
    if readiness.get("full_expert_replay_ready_cases") == 0 and method.get("score") is not None:
        raise ValueError("zero-ready replay corpus cannot receive a method-fidelity score")
    for asset in canonical.get("asset_accounting", []):
        if asset.get("blocked_by_empty_registry"):
            if asset.get("disposition") != "BLOCKED" or asset.get("covered_assets") != 0:
                raise ValueError("empty production registry cannot be counted as fidelity PASS or covered")
        if asset.get("full_source_chart_equivalence_verified") is True:
            raise ValueError("target-anchor verification cannot be promoted to full-source-chart equivalence")
    if method.get("scope_review", {}).get("justified_bindings") == 0:
        if method.get("scope_review", {}).get("all_source_patterns_remain_semantic_only") is not True:
            raise ValueError("zero-binding baseline must preserve SEMANTIC_ONLY source patterns")
    if method.get("replay_readiness", {}).get("full_expert_replay_ready_cases") == 0:
        for dimension in method.get("score_dimensions", {}).values():
            if dimension.get("metric_id") == "method_fidelity_score" and dimension.get("value") is not None:
                raise ValueError("zero-ready replay corpus cannot receive a method-fidelity score")


def build_canonical_and_method_fidelity_benchmark(
    root: Path = ROOT,
) -> dict[str, Any]:
    payloads, source_artifacts = _load_pinned_inputs(root)
    return _build_report(payloads, source_artifacts)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write",
        action="store_true",
        help="write the deterministic report to the versioned output path",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=OUTPUT_PATH,
        help="output path used with --write",
    )
    args = parser.parse_args(argv)
    report = build_canonical_and_method_fidelity_benchmark()
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.write:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

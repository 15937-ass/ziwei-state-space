"""Source-bounded review of Wang case-target to MethodPattern scope.

This module records review findings only. It does not alter MethodPattern allowed_use,
Method Policy execution dispositions, canonical knowledge, or runtime authorization.
"""
from __future__ import annotations

from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
from typing import Any, Mapping
import hashlib

ROOT = Path(__file__).resolve().parents[2]
CASE_ROOT = ROOT / "product" / "expert_cases" / "wang_tingzhi"
CASE_DIR = CASE_ROOT / "cases"
REVIEW_PATH = ROOT / "product" / "WANG_METHOD_SCOPE_REVIEW_V0_1C.json"
READINESS_V02_PATH = ROOT / "product" / "WANG_METHOD_POLICY_READINESS_v0.2.json"
READINESS_V03_PATH = ROOT / "product" / "WANG_METHOD_POLICY_READINESS_v0.3.json"
CHART_PATH = CASE_ROOT / "FULL_CHART_MATERIALIZATION_V0_1B.json"
CHART_READINESS_PATH = CASE_ROOT / "FULL_CHART_RECONSTRUCTION_READINESS_V0_1.json"
INVENTORY_PATH = CASE_ROOT / "CASE_SOURCE_INVENTORY_v0.1.json"
PATTERNS_PATH = CASE_ROOT / "METHOD_PATTERNS_v0.1.json"
POLICY_PATH = ROOT / "product" / "METHOD_POLICY_EXECUTION_RULES_v0.1.json"
METHOD_POLICY_CODE_PATH = ROOT / "src" / "product" / "method_policy.py"
CASE_CORPUS_CODE_PATH = ROOT / "src" / "product" / "expert_case_corpus.py"

EXPECTED_CASE_IDS = tuple(f"WANG-CASE-{index:03d}" for index in range(1, 25))
EXPECTED_PATTERN_IDS = tuple(f"WT-METHOD-{index:03d}" for index in range(1, 7))
CHART_MATERIALIZATION_CLAIM = "SOURCE_INPUT_RECONSTRUCTED_TARGET_ANCHOR_VERIFIED"

# Git blob IDs pin the exact review inputs. A changed source requires a new review
# artifact instead of silently changing the meaning of this one.
EXPECTED_INPUT_BLOBS = {
    "inventory": "804b3163b40ed19c8626427ce988fb12b6f85763",
    "patterns": "f81cd49e74bd7fb0a960d40b63f7d014c839f287",
    "policy": "2321ad7d59542d272f97e58c338921a424ba0f9f",
    "readiness_v02": "375d438346b9dd696b336a39311b60bd5568d2fb",
    "charts": "3778e5f3d66c1e5ab44461360b6d9f71b3f8be56",
    "chart_readiness": "a0ec93c5a17859a64d02eb029837c787c7b12bdf",
    "method_policy_code": "90a1a84cd7b18a3e218ea9575692fc7e8f542d29",
    "case_corpus_code": "3f9b582e1ef27bc8c7e09d147209053db84f7929",
}

SOURCE_PATHS = {
    "inventory": INVENTORY_PATH,
    "patterns": PATTERNS_PATH,
    "policy": POLICY_PATH,
    "readiness_v02": READINESS_V02_PATH,
    "charts": CHART_PATH,
    "chart_readiness": CHART_READINESS_PATH,
    "method_policy_code": METHOD_POLICY_CODE_PATH,
    "case_corpus_code": CASE_CORPUS_CODE_PATH,
}


def _git_blob_sha(raw: bytes) -> str:
    header = b"blob " + str(len(raw)).encode("ascii") + b"\0"
    return hashlib.sha1(header + raw).hexdigest()


def _read_pinned(name: str) -> bytes:
    path = SOURCE_PATHS[name]
    raw = path.read_bytes()
    observed = _git_blob_sha(raw)
    expected = EXPECTED_INPUT_BLOBS[name]
    if observed != expected:
        raise ValueError(
            f"{path.relative_to(ROOT).as_posix()}: source revision changed; "
            f"expected Git blob {expected}, observed {observed}; create a new review version"
        )
    return raw


def _load_json_bytes(raw: bytes, path: Path) -> dict[str, Any]:
    payload = json.loads(raw.decode("utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path.relative_to(ROOT).as_posix()} must contain a JSON object")
    return payload


def _load_inputs() -> dict[str, Any]:
    raw = {name: _read_pinned(name) for name in SOURCE_PATHS}
    payloads = {
        name: _load_json_bytes(raw[name], SOURCE_PATHS[name])
        for name in ("inventory", "patterns", "policy", "readiness_v02", "charts", "chart_readiness")
    }
    payloads["raw"] = raw
    return payloads


def _source_artifacts(inputs: Mapping[str, Any]) -> list[dict[str, str]]:
    ids = {
        "inventory": "WANG_TINGZHI_ANXING_TUIDUAN_24_V0_1",
        "patterns": "WANG_METHOD_PATTERNS_V0_1",
        "policy": "METHOD_POLICY_EXECUTION_RULES_V0_1",
        "readiness_v02": "WANG_METHOD_POLICY_READINESS_V0_2",
        "charts": "WANG_FULL_CHART_MATERIALIZATION_V0_1B",
        "chart_readiness": "WANG_FULL_CHART_RECONSTRUCTION_READINESS_V0_1",
        "method_policy_code": "METHOD_POLICY_RUNTIME_SCOPE_CONTRACT",
        "case_corpus_code": "CASE_TARGET_DOMAIN_CONTRACT",
    }
    return [
        {
            "role": name,
            "artifact_id": ids[name],
            "path": SOURCE_PATHS[name].relative_to(ROOT).as_posix(),
            "git_blob_sha": EXPECTED_INPUT_BLOBS[name],
        }
        for name in SOURCE_PATHS
    ]


def _case_chart_status(
    case_id: str,
    chart_by_id: Mapping[str, dict[str, Any]],
    chart_readiness_by_id: Mapping[str, dict[str, Any]],
    engine: Mapping[str, Any],
) -> dict[str, Any]:
    row = chart_by_id.get(case_id)
    if row is not None:
        anchor = row["target_anchor_verification"]
        if (
            row.get("materialization_status") != "FULL_CHART_MATERIALIZED"
            or row.get("materialization_claim") != CHART_MATERIALIZATION_CLAIM
            or row.get("full_source_chart_equivalence_verified") is not False
            or anchor.get("status") != "UNIQUE_ANCHOR_MATCH_RECONFIRMED"
            or anchor.get("matched") is not True
        ):
            raise ValueError(f"{case_id}: full-chart materialization contract mismatch")
        candidate_set = row["source_candidate_set"]
        return {
            "status": "MATERIALIZED",
            "chart_specific_analysis_status": "LIMITED_ENGINE_RECONSTRUCTION_AVAILABLE",
            "artifact_ref": CHART_PATH.relative_to(ROOT).as_posix(),
            "materialization_claim": row["materialization_claim"],
            "engine": {
                "name": engine["name"],
                "version": engine["version"],
                "entrypoint": engine["entrypoint"],
                "algorithm": engine["algorithm"],
            },
            "target_anchor_verification": {
                "status": anchor["status"],
                "matched": anchor["matched"],
                "target_palace_identity_match": anchor["target_palace_identity_match"],
            },
            "full_source_chart_equivalence_verified": False,
            "source_candidate_provenance": {
                "source_input_candidate_id": row["source_provenance"]["source_input_candidate_id"],
                "readiness_status": row["source_provenance"]["readiness_status"],
                "source_candidate_count": candidate_set["source_candidate_count"],
                "evaluated_candidate_count": candidate_set["evaluated_candidate_count"],
                "anchor_match_count": candidate_set["anchor_match_count"],
                "selection_basis": candidate_set["selection_basis"],
                "source_time_ambiguity_preserved": candidate_set["source_time_ambiguity_preserved"],
                "source_time_label": candidate_set.get("source_time_label"),
                "time_index_candidates": candidate_set["time_index_candidates"],
            },
        }

    readiness = chart_readiness_by_id.get(case_id)
    if readiness is None:
        raise ValueError(f"{case_id}: missing reconstruction-readiness row")
    if readiness.get("status") == "UNIQUE_ANCHOR_MATCH":
        raise ValueError(f"{case_id}: unique-anchor case is missing its materialized chart")
    return {
        "status": "NOT_MATERIALIZED",
        "chart_specific_analysis_status": "BLOCKED_UNMATERIALIZED",
        "artifact_ref": CHART_PATH.relative_to(ROOT).as_posix(),
        "reconstruction_readiness_status": readiness["status"],
        "source_candidate_count": readiness["source_candidate_count"],
        "evaluated_candidate_count": readiness["evaluated_candidate_count"],
        "anchor_match_count": readiness["anchor_match_count"],
        "target_anchor_verified": False,
        "full_source_chart_equivalence_verified": False,
    }


def _assessment(
    case: Mapping[str, Any],
    pattern: Mapping[str, Any],
    policy_rule: Mapping[str, Any],
    chart_status: Mapping[str, Any],
) -> dict[str, Any]:
    case_id = case["case_id"]
    domain = case["target"]["domains"][0]
    pattern_id = pattern["pattern_id"]
    source_case_refs = set(
        ref
        for node in case["expert_reasoning_graph"]["nodes"]
        for ref in node.get("source_span_refs", [])
    )
    explicit_span_links = sorted(source_case_refs.intersection(pattern["source_span_refs"]))
    explicit_pattern_ids = case.get("method_pattern_refs", [])
    exact_scope_match = bool(set(case["target"]["domains"]).intersection(pattern["target_domains"]))
    if exact_scope_match:
        # No current Wang case should reach this branch: the MethodPattern contract
        # uses GLOBAL_PROFILE / TEMPORAL_INFERENCE / SYMBOLIC_INFERENCE, not case domains.
        raise ValueError(f"{case_id}/{pattern_id}: unexpected exact target-scope match")

    if pattern_id == "WT-METHOD-001":
        if domain in {"PARENTS", "PROPERTY"}:
            status = "SEMANTIC_ONLY_RELEVANCE"
            rationale = (
                "The method source names parents/property palace evidence, so this case has "
                "limited topical relevance. Its MethodPattern target scope remains GLOBAL_PROFILE, "
                "allowed_use remains SEMANTIC_ONLY, and no case-specific source link authorizes binding."
            )
            missing = [
                "EXACT_CASE_TARGET_SCOPE_MATCH",
                "EXPLICIT_CASE_TO_METHOD_SOURCE_LINK",
                "SEMANTIC_ONLY_PROMOTION_AUTHORIZATION",
            ]
        else:
            status = "INSUFFICIENT_SOURCE_EVIDENCE"
            rationale = (
                "The case target is not one of this pattern's named parents/property evidence kinds. "
                "The GLOBAL_PROFILE scope does not bind the pattern to this specific case target."
            )
            missing = ["EXACT_CASE_TARGET_SCOPE_MATCH", "EXPLICIT_CASE_TO_METHOD_SOURCE_LINK"]
    elif pattern_id == "WT-METHOD-002":
        if domain in {"LIFE", "FORTUNE_VIRTUE"}:
            status = "SEMANTIC_ONLY_RELEVANCE"
            rationale = (
                "The method source names life/fortune-virtue palace evidence, so this case has "
                "limited topical relevance. Its MethodPattern target scope remains GLOBAL_PROFILE, "
                "allowed_use remains SEMANTIC_ONLY, and no case-specific source link authorizes binding."
            )
            missing = [
                "EXACT_CASE_TARGET_SCOPE_MATCH",
                "EXPLICIT_CASE_TO_METHOD_SOURCE_LINK",
                "SEMANTIC_ONLY_PROMOTION_AUTHORIZATION",
            ]
        else:
            status = "INSUFFICIENT_SOURCE_EVIDENCE"
            rationale = (
                "The case target is not one of this pattern's named life/fortune-virtue evidence kinds. "
                "The GLOBAL_PROFILE scope does not bind the pattern to this specific case target."
            )
            missing = ["EXACT_CASE_TARGET_SCOPE_MATCH", "EXPLICIT_CASE_TO_METHOD_SOURCE_LINK"]
    elif pattern_id == "WT-METHOD-003":
        status = "MISSING_CONTEXT_BINDING"
        rationale = (
            "The pattern requires a TARGET_PALACE plus an explicitly bound RELATED_PALACE. "
            "The case target identifies only its target domain/palace; the existing policy blocker "
            "RELATED_PALACE_BINDING_REQUIRED remains unresolved."
        )
        missing = ["RELATED_PALACE_BINDING_REQUIRED", "EXPLICIT_CASE_TO_METHOD_SOURCE_LINK"]
    elif pattern_id == "WT-METHOD-004":
        status = "INSUFFICIENT_SOURCE_EVIDENCE"
        rationale = (
            "The case has no target_time_label and its source-demonstrated reasoning graph is natal-only. "
            "The pattern's TEMPORAL_INFERENCE scope requires NATAL, DECADE, and YEAR evidence and "
            "does not explicitly target this case question."
        )
        missing = [
            "CASE_TARGET_TIME_LABEL",
            "MATERIALIZED_NATAL_DECADE_YEAR_METHOD_EVIDENCE",
            "EXACT_CASE_TARGET_SCOPE_MATCH",
        ]
    elif pattern_id in {"WT-METHOD-005", "WT-METHOD-006"}:
        status = "DEFERRED_SYMBOLIC_INTERPRETATION"
        if chart_status["status"] == "MATERIALIZED":
            chart_missing = ["FULL_SOURCE_CHART_EQUIVALENCE_NOT_VERIFIED"]
        else:
            chart_missing = ["FULL_CHART_NOT_MATERIALIZED"]
        if pattern_id == "WT-METHOD-005":
            symbolic_need = "BORROWED_PALACE_OPPOSITE_PALACE_STAR_SYSTEM"
        else:
            symbolic_need = "PAIRED_STAR_IDENTITY_AND_RELATIVE_POSITION"
        rationale = (
            f"The required {symbolic_need} belongs to symbolic interpretation and the current "
            "Method Policy disposition is DEFER_TO_SYMBOLIC_ADAPTER. A reconstructed chart, even "
            "when present, cannot by itself establish a case-target MethodPattern binding."
        )
        missing = [*chart_missing, "EXPLICIT_CASE_TARGET_METHOD_BINDING", "SYMBOLIC_ADAPTER_AUTHORIZATION"]
    else:
        raise ValueError(f"unsupported MethodPattern: {pattern_id}")

    return {
        "pattern_id": pattern_id,
        "method_source_span_refs": list(pattern["source_span_refs"]),
        "method_source_case_refs": list(pattern["source_case_refs"]),
        "pattern_maturity": pattern["maturity"],
        "pattern_allowed_use": pattern["allowed_use"],
        "pattern_target_domains": list(pattern["target_domains"]),
        "required_evidence_kinds": list(pattern["required_evidence_kinds"]),
        "action_sequence": list(pattern["action_sequence"]),
        "policy_disposition": policy_rule["disposition"],
        "policy_target_domains": list(policy_rule["target_domains"]),
        "policy_required_evidence_kinds": list(policy_rule["required_evidence_kinds"]),
        "policy_allowed_actions": list(policy_rule["allowed_actions"]),
        "review_outcome": status,
        "exact_target_domain_match": exact_scope_match,
        "case_source_span_overlap_with_method_source": explicit_span_links,
        "explicit_case_method_pattern_refs": list(explicit_pattern_ids),
        "explicit_case_to_pattern_source_link": bool(explicit_span_links or explicit_pattern_ids),
        "case_source_basis_refs": [case["source"]["source_span_refs"][1]],
        "proposed_binding": None,
        "binding_status": "NOT_BOUND_FAIL_CLOSED",
        "missing_requirements": missing,
        "rationale": rationale,
    }


def build_wang_method_scope_review() -> dict[str, Any]:
    inputs = _load_inputs()
    inventory = inputs["inventory"]
    patterns_doc = inputs["patterns"]
    policy_doc = inputs["policy"]
    charts_doc = inputs["charts"]
    chart_readiness_doc = inputs["chart_readiness"]

    if inventory.get("corpus_id") != "WANG_TINGZHI_ANXING_TUIDUAN_24_V0_1":
        raise ValueError("unexpected Wang case corpus")
    if [row["case_id"] for row in inventory["cases"]] != list(EXPECTED_CASE_IDS):
        raise ValueError("case inventory must contain the canonical 24-case sequence")
    patterns = patterns_doc["method_patterns"]
    if tuple(pattern["pattern_id"] for pattern in patterns) != EXPECTED_PATTERN_IDS:
        raise ValueError("MethodPattern set/order changed; create a new review version")
    if any(pattern.get("allowed_use") != "SEMANTIC_ONLY" for pattern in patterns):
        raise ValueError("source MethodPattern allowed_use must remain SEMANTIC_ONLY")

    policy_by_id = {row["pattern_id"]: row for row in policy_doc["dispositions"]}
    if tuple(policy_by_id) != EXPECTED_PATTERN_IDS:
        # JSON object ordering is not an execution contract; compare the set below.
        if set(policy_by_id) != set(EXPECTED_PATTERN_IDS):
            raise ValueError("Method Policy disposition coverage changed")
    for pattern in patterns:
        rule = policy_by_id[pattern["pattern_id"]]
        if (
            rule["target_domains"] != pattern["target_domains"]
            or rule["required_evidence_kinds"] != pattern["required_evidence_kinds"]
        ):
            raise ValueError(f"{pattern['pattern_id']}: existing target-domain contract mismatch")

    case_paths = sorted(CASE_DIR.glob("wang_case_*.json"))
    if len(case_paths) != 24:
        raise ValueError(f"expected 24 source case files, observed {len(case_paths)}")
    cases_by_id = {
        json.loads(path.read_text(encoding="utf-8"))["case_id"]:
        json.loads(path.read_text(encoding="utf-8"))
        for path in case_paths
    }
    if tuple(sorted(cases_by_id)) != EXPECTED_CASE_IDS:
        raise ValueError("source case files do not match the canonical 24-case set")

    inventory_by_id = {row["case_id"]: row for row in inventory["cases"]}
    chart_by_id = {row["case_id"]: row for row in charts_doc["cases"]}
    chart_readiness_by_id = {row["case_id"]: row for row in chart_readiness_doc["cases"]}
    if set(chart_readiness_by_id) != set(EXPECTED_CASE_IDS):
        raise ValueError("reconstruction-readiness rows must cover all 24 cases")
    unique_ids = {
        row["case_id"] for row in chart_readiness_doc["cases"]
        if row["status"] == "UNIQUE_ANCHOR_MATCH"
    }
    if set(chart_by_id) != unique_ids or len(chart_by_id) != 11:
        raise ValueError("materialized chart set must equal the 11 unique anchor matches")
    engine = charts_doc["engine"]

    case_rows: list[dict[str, Any]] = []
    outcome_counter: Counter[str] = Counter()
    for case_id in EXPECTED_CASE_IDS:
        case = cases_by_id[case_id]
        index_row = inventory_by_id[case_id]
        source_spans = {
            "chart": index_row["chart_span_ref"],
            "reasoning": index_row["reasoning_span_ref"],
            "conclusion": index_row["conclusion_span_ref"],
            "outcome": index_row["outcome_span_ref"],
        }
        ordered_spans = list(source_spans.values())
        if case["source"]["source_span_refs"] != ordered_spans:
            raise ValueError(f"{case_id}: source span lineage differs from inventory")
        if case["target"]["domains"] != [index_row["domain"]]:
            raise ValueError(f"{case_id}: case target domain differs from inventory")
        if case["allowed_use"] != inventory["extraction_policy"]["case_allowed_use"]:
            raise ValueError(f"{case_id}: case allowed_use changed")
        graph_nodes = case["expert_reasoning_graph"]["nodes"]
        graph_allowed_uses = {node.get("allowed_use") for node in graph_nodes}
        canonical_refs = sorted({
            ref for node in graph_nodes for ref in node.get("canonical_rule_refs", [])
        })
        if graph_allowed_uses != {"CASE_SUPPORT_ONLY"} or canonical_refs:
            raise ValueError(f"{case_id}: case graph must remain CASE_SUPPORT_ONLY without canonical refs")
        temporal_layers = {
            node.get("temporal_layer") for node in graph_nodes if node.get("temporal_layer")
        }
        if case["target"].get("target_time_label") is not None or temporal_layers - {"NATAL"}:
            raise ValueError(f"{case_id}: unexpected temporal target/evidence in source case v0.1")

        chart_status = _case_chart_status(case_id, chart_by_id, chart_readiness_by_id, engine)
        assessments = [
            _assessment(case, pattern, policy_by_id[pattern["pattern_id"]], chart_status)
            for pattern in patterns
        ]
        if len(assessments) != 6 or len({item["pattern_id"] for item in assessments}) != 6:
            raise ValueError(f"{case_id}: expected exactly one assessment per MethodPattern")
        outcome_counter.update(item["review_outcome"] for item in assessments)
        case_rows.append({
            "case_id": case_id,
            "target": {
                "domain": case["target"]["domains"][0],
                "palace": index_row["palace"],
                "target_time_label": case["target"].get("target_time_label"),
            },
            "source_span_refs": source_spans,
            "source_pages": [index_row["source_page_start"], index_row["source_page_end"]],
            "source_review_status": case["source"]["review_status"],
            "case_epistemic_status": case["epistemic_status"],
            "case_allowed_use": case["allowed_use"],
            "case_graph_status": index_row["graph_status"],
            "case_graph_allowed_use": sorted(graph_allowed_uses),
            "case_graph_canonical_rule_refs": canonical_refs,
            "chart_materialization": chart_status,
            "method_pattern_assessments": assessments,
        })

    assessment_count = sum(outcome_counter.values())
    if assessment_count != 24 * 6:
        raise ValueError("review matrix must contain exactly 144 case-pattern assessments")
    proposed_bindings = sum(
        item["proposed_binding"] is not None
        for row in case_rows for item in row["method_pattern_assessments"]
    )
    exact_matches = sum(
        item["exact_target_domain_match"]
        for row in case_rows for item in row["method_pattern_assessments"]
    )
    if proposed_bindings or exact_matches:
        raise ValueError("review must fail closed when no exact target-domain binding exists")

    materialized_ids = [row["case_id"] for row in case_rows
                        if row["chart_materialization"]["status"] == "MATERIALIZED"]
    unmaterialized_ids = [row["case_id"] for row in case_rows
                          if row["chart_materialization"]["status"] == "NOT_MATERIALIZED"]
    if len(materialized_ids) != 11 or len(unmaterialized_ids) != 13:
        raise ValueError("expected 11 materialized charts and 13 unmaterialized cases")
    case_021 = next(row for row in case_rows if row["case_id"] == "WANG-CASE-021")
    provenance_021 = case_021["chart_materialization"]["source_candidate_provenance"]
    if (
        provenance_021["source_time_ambiguity_preserved"] is not True
        or provenance_021["time_index_candidates"] != [0, 12]
        or provenance_021["anchor_match_count"] != 1
    ):
        raise ValueError("WANG-CASE-021 unqualified 子时 ambiguity must remain explicit")

    return {
        "schema_version": "0.1C",
        "artifact_id": "WANG_METHOD_SCOPE_REVIEW_V0_1C",
        "issue": 615,
        "corpus_id": inventory["corpus_id"],
        "review_status": "SOURCE_BOUND_SCOPE_REVIEW_COMPLETE_FAIL_CLOSED",
        "source_artifacts": _source_artifacts(inputs),
        "review_contract": {
            "target_domain_contract": "Exact case target domain must intersect MethodPattern.target_domains before any target-specific binding can be proposed.",
            "target_domain_contract_source_refs": [
                "src/product/expert_case_corpus.py",
                "src/product/method_policy.py::assess_pattern",
                "product/METHOD_POLICY_EXECUTION_RULES_v0.1.json",
            ],
            "positive_binding_basis_required": [
                "EXACT_CASE_TARGET_SCOPE_MATCH",
                "EXPLICIT_CASE_TO_METHOD_SOURCE_LINK",
                "SOURCE_SPAN_VERIFIED",
            ],
            "prohibited_binding_basis": [
                "CASE_CONCLUSION_OR_OUTCOME",
                "CHART_STRUCTURE_ALONE",
                "GLOBAL_PROFILE_RELEVANCE_ALONE",
                "SEMANTIC_ONLY_METHOD_PATTERN_WITHOUT_EXPLICIT_AUTHORIZATION",
            ],
            "case_conclusion_or_outcome_content_used_for_binding": False,
            "chart_structure_used_as_binding_basis": False,
            "source_span_refs_preserved_without_copying_conclusion_or_outcome_text": True,
            "case_allowed_use_unchanged": True,
            "method_pattern_allowed_use_unchanged": True,
            "method_policy_dispositions_unchanged": True,
            "canonical_rules_added": False,
            "numeric_weights_or_probabilities_added": False,
            "predictive_claim_added": False,
        },
        "summary": {
            "case_count": 24,
            "method_pattern_count": 6,
            "assessment_count": assessment_count,
            "exact_target_domain_matches": exact_matches,
            "explicit_case_to_pattern_source_links": 0,
            "proposed_binding_count": proposed_bindings,
            "full_chart_materialized_case_count": len(materialized_ids),
            "full_chart_unmaterialized_case_count": len(unmaterialized_ids),
            "full_expert_replay_ready": 0,
            "review_outcome_counts": dict(sorted(outcome_counter.items())),
            "materialized_case_ids": materialized_ids,
            "unmaterialized_case_ids": unmaterialized_ids,
        },
        "case_reviews": case_rows,
        "conclusion": {
            "case_target_method_bindings": "NONE_JUSTIFIED_BY_CURRENT_EXPLICIT_SOURCE_LINKS",
            "runtime_action": "FAIL_CLOSED",
            "full_expert_replay_ready": "0/24",
            "readiness_successor": "product/WANG_METHOD_POLICY_READINESS_v0.3.json",
            "historical_readiness_v0_2_mutated": False,
            "next_product_work_unit": "CANONICAL_AND_METHOD_FIDELITY_BENCHMARK",
            "claim_boundary": (
                "This review evaluates source-bounded scope compatibility only. It does not establish "
                "canonical Zhongzhou rule truth, expert-method fidelity, outcome ground truth, or predictive validity."
            ),
        },
    }


def build_wang_method_policy_readiness_v03(
    review: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    inputs = _load_inputs()
    base = inputs["readiness_v02"]
    review_payload = dict(review) if review is not None else build_wang_method_scope_review()
    if review_payload.get("artifact_id") != "WANG_METHOD_SCOPE_REVIEW_V0_1C":
        raise ValueError("readiness v0.3 requires the v0.1C scope-review artifact")

    review_by_id = {row["case_id"]: row for row in review_payload["case_reviews"]}
    materialized_count = sum(
        row["chart_materialization"]["status"] == "MATERIALIZED"
        for row in review_payload["case_reviews"]
    )
    unmaterialized_count = sum(
        row["chart_materialization"]["status"] == "NOT_MATERIALIZED"
        for row in review_payload["case_reviews"]
    )
    if (materialized_count, unmaterialized_count) != (11, 13):
        raise ValueError("readiness v0.3 requires the 11/13 materialization split")

    payload = deepcopy(base)
    payload["artifact_id"] = "WANG_METHOD_POLICY_READINESS_V0_3"
    payload["issue"] = 615
    payload["supersedes_artifact"] = READINESS_V02_PATH.relative_to(ROOT).as_posix()
    payload["generated_from"] = [
        REVIEW_PATH.relative_to(ROOT).as_posix(),
        CHART_PATH.relative_to(ROOT).as_posix(),
        CHART_READINESS_PATH.relative_to(ROOT).as_posix(),
        POLICY_PATH.relative_to(ROOT).as_posix(),
    ]
    payload["scope_review_artifact_id"] = review_payload["artifact_id"]
    payload["summary"] = {
        **payload["summary"],
        "full_chart_materialized_fold_count": materialized_count,
        "full_chart_blocked_fold_count": unmaterialized_count,
        "method_policy_runtime_target_chart_blocked_fold_count": 24,
        "case_target_scope_binding_count": 0,
        "full_expert_replay_ready": 0,
        "remaining_blocker_classes": [
            "FULL_CHART_NOT_MATERIALIZED",
            "NO_EXECUTABLE_PATTERN_FOR_CASE_TARGET_SCOPE",
            "METHOD_POLICY_RUNTIME_TARGET_CHART_EVIDENCE_REMAINS_BLOCKED",
        ],
        "recommended_next_dependency": "CANONICAL_AND_METHOD_FIDELITY_BENCHMARK",
    }
    payload["interpretation"] = {
        "materialization_gain": (
            "11/24 cases now have a real pinned-engine full-chart materialization artifact; "
            "13/24 remain unmaterialized. The artifact verifies the reviewed target-palace identity "
            "and fourteen-major-star anchor only."
        ),
        "runtime_boundary": (
            "The existing Method Policy runtime still marks TARGET_CHART evidence BLOCKED for all 24 "
            "cases. The separate full-chart artifact is not silently promoted into runtime evidence. "
            "All 24 cases remain unbound to an executable case-target MethodPattern."
        ),
        "benchmark_claim": (
            "This artifact measures source-bounded replay readiness only; it is not expert-method "
            "fidelity or predictive-validity evidence."
        ),
    }
    payload["metric_definitions"] = {
        "full_chart_materialized_fold_count": "Cases with a separate committed full-chart materialization artifact.",
        "full_chart_blocked_fold_count": "Cases still lacking a full-chart materialization artifact; 13/24.",
        "method_policy_runtime_target_chart_blocked_fold_count": (
            "Cases for which the unchanged Method Policy runtime emits TARGET_CHART=BLOCKED; 24/24 "
            "until an explicitly authorized runtime integration work unit changes that behavior."
        ),
    }

    new_folds = []
    for fold in payload["folds"]:
        case_id = fold["held_out_case_id"]
        reviewed_case = review_by_id[case_id]
        chart_status = reviewed_case["chart_materialization"]
        fold["full_chart_materialization"] = {
            "status": chart_status["status"],
            "chart_specific_analysis_status": chart_status["chart_specific_analysis_status"],
            "artifact_ref": chart_status["artifact_ref"],
            "materialization_claim": chart_status.get("materialization_claim"),
            "target_anchor_verified": chart_status.get(
                "target_anchor_verification", {}
            ).get("matched", False),
            "full_source_chart_equivalence_verified": False,
        }
        fold["method_scope_review"] = {
            "artifact_ref": REVIEW_PATH.relative_to(ROOT).as_posix(),
            "assessment_count": len(reviewed_case["method_pattern_assessments"]),
            "explicit_binding_count": 0,
            "case_target_scope_binding_status": "NOT_BOUND_FAIL_CLOSED",
            "full_expert_replay_ready": False,
        }
        fold["full_chart_materialization_blocker"] = (
            "FULL_CHART_NOT_MATERIALIZED"
            if chart_status["status"] == "NOT_MATERIALIZED"
            else None
        )
        # Preserve the historical runtime evidence statuses, blockers, and abstention
        # trace: this successor records external artifact availability, not runtime promotion.
        new_folds.append(fold)
    payload["folds"] = new_folds
    return payload


def validate_wang_method_scope_review(payload: Mapping[str, Any] | None = None) -> dict[str, Any]:
    expected = build_wang_method_scope_review()
    observed = dict(payload) if payload is not None else expected
    if observed != expected:
        raise ValueError("Wang Method Scope Review v0.1C differs from the source-locked deterministic build")
    return expected


def validate_wang_method_policy_readiness_v03(
    payload: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    expected = build_wang_method_policy_readiness_v03()
    observed = dict(payload) if payload is not None else expected
    if observed != expected:
        raise ValueError("Wang Method Policy Readiness v0.3 differs from the deterministic successor build")
    return expected

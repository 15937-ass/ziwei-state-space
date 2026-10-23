"""Validated Wang blind-evidence materialization for Product Benchmark B.

This module is intentionally conservative.  The v0.1 artifact materializes only
source-visible target-palace identity and the fourteen-major-star system.  It
must not reconstruct a full chart, leak source subject identity, import expert
reasoning/conclusions/outcomes, or promote case evidence into canonical Ziwei
truth.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_PATH = (
    ROOT / "product" / "expert_cases" / "wang_tingzhi" / "BLIND_EVIDENCE_V0_1.json"
)
LOCK_PATH = ROOT / "product" / "PRODUCT_KNOWLEDGE.lock.json"
INVENTORY_PATH = ROOT / "product" / "expert_cases" / "wang_tingzhi" / "CASE_SOURCE_INVENTORY_v0.1.json"

MAJOR_STARS = frozenset(
    {
        "紫微",
        "天机",
        "太阳",
        "武曲",
        "天同",
        "廉贞",
        "天府",
        "太阴",
        "贪狼",
        "巨门",
        "天相",
        "天梁",
        "七杀",
        "破军",
    }
)

FORBIDDEN_BLIND_KEYS = frozenset(
    {
        "source_subject_label",
        "expert_reasoning_graph",
        "expert_conclusion_refs",
        "outcome_refs",
        "reasoning_span_ref",
        "conclusion_span_ref",
        "outcome_span_ref",
        "expert_prose",
        "biography",
    }
)


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _walk_keys(value: Any) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, dict):
        for key, nested in value.items():
            keys.add(str(key))
            keys.update(_walk_keys(nested))
    elif isinstance(value, list):
        for nested in value:
            keys.update(_walk_keys(nested))
    return keys


def _k_method_component(bundle: Mapping[str, Any]) -> Mapping[str, Any]:
    component = next(
        (
            item
            for item in bundle.get("components", [])
            if item.get("component_id") == "K_method"
        ),
        None,
    )
    if not isinstance(component, dict):
        raise ValueError("Product Knowledge bundle lacks K_method")
    return component


def _find_historical_bundle(bundle_id: str) -> Mapping[str, Any]:
    matches: list[Mapping[str, Any]] = []
    for path in sorted((ROOT / "product").glob("PRODUCT_KNOWLEDGE_BUNDLE_V*.json")):
        payload = _read_json(path)
        if isinstance(payload, dict) and payload.get("bundle_id") == bundle_id:
            matches.append(payload)
    if len(matches) != 1:
        raise ValueError(
            "blind evidence historical Product Knowledge bundle is missing or ambiguous"
        )
    return matches[0]


def _validate_lineage(payload: Mapping[str, Any]) -> None:
    """Validate creation-time lineage without invalidating unrelated promotions.

    Blind evidence is historically bound to the Product Knowledge bundle that
    existed when it was materialized.  Later K_response-only promotions must
    not rewrite that history or invalidate K_method-derived evidence.  Runtime
    reuse is permitted only while the active K_method semantic digest remains
    identical to the creation-time K_method digest.
    """

    lock = _read_json(LOCK_PATH)
    lineage = payload.get("lineage")
    if not isinstance(lineage, dict):
        raise ValueError("blind evidence lineage must be an object")

    lineage_lock_id = str(lineage.get("product_knowledge_lock_id") or "").strip()
    lineage_bundle_id = str(
        lineage.get("active_product_knowledge_bundle_id") or ""
    ).strip()
    lineage_k_method_digest = str(
        lineage.get("k_method_component_semantic_digest") or ""
    ).strip()
    if not lineage_lock_id or not lineage_bundle_id or not lineage_k_method_digest:
        raise ValueError("blind evidence lineage fields are required")
    if lock.get("auto_refresh") is not False:
        raise ValueError("active Product Knowledge lock must not auto-refresh")

    historical_bundle = _find_historical_bundle(lineage_bundle_id)
    historical_k_method = _k_method_component(historical_bundle)
    if (
        historical_k_method.get("component_semantic_digest")
        != lineage_k_method_digest
    ):
        raise ValueError(
            "blind evidence creation-time K_method semantic digest mismatch"
        )

    active_bundle_path = ROOT / str(lock.get("active_bundle_path") or "")
    active_bundle = _read_json(active_bundle_path)
    if active_bundle.get("bundle_id") != lock.get("active_bundle_id"):
        raise ValueError("active Product Knowledge lock/bundle id mismatch")
    active_k_method = _k_method_component(active_bundle)
    if (
        active_k_method.get("component_semantic_digest")
        != lineage_k_method_digest
    ):
        raise ValueError(
            "blind evidence K_method lineage is incompatible with active K_method"
        )


def validate_wang_blind_evidence(payload: Mapping[str, Any]) -> None:
    if payload.get("schema_version") != "0.1":
        raise ValueError("Wang blind evidence schema_version must be 0.1")
    if payload.get("artifact_id") != "WANG_BLIND_EVIDENCE_V0_1":
        raise ValueError("unexpected Wang blind evidence artifact_id")

    leaked = sorted(FORBIDDEN_BLIND_KEYS.intersection(_walk_keys(payload)))
    if leaked:
        raise ValueError(f"blind evidence contains forbidden leakage keys: {leaked}")

    scope = payload.get("scope")
    if not isinstance(scope, dict):
        raise ValueError("blind evidence scope must be an object")
    if scope.get("case_count") != 24 or scope.get("materialized_case_count") != 24:
        raise ValueError("Wang blind evidence must cover 24/24 cases")
    if scope.get("materialization_level") != "TARGET_PALACE_MAJOR_STAR_SYSTEM_ONLY":
        raise ValueError("unsupported Wang blind evidence materialization level")
    if scope.get("full_chart_materialized") is not False:
        raise ValueError("v0.1 must not claim full-chart materialization")

    guardrails = payload.get("guardrails")
    if not isinstance(guardrails, dict) or any(
        guardrails.get(key) is not False
        for key in (
            "unreadable_fields_are_guessed",
            "auxiliary_stars_materialized",
            "transformations_materialized",
            "palace_stem_branch_materialized",
            "age_ranges_materialized",
            "full_chart_claimed",
        )
    ):
        raise ValueError("Wang blind evidence guardrails are not fail-closed")

    cases = payload.get("cases")
    if not isinstance(cases, list) or len(cases) != 24:
        raise ValueError("Wang blind evidence cases must contain exactly 24 rows")

    expected_ids = [f"WANG-CASE-{index:03d}" for index in range(1, 25)]
    actual_ids = [str(item.get("case_id") or "") for item in cases]
    if actual_ids != expected_ids:
        raise ValueError("Wang blind evidence case IDs/order mismatch")

    inventory = _read_json(INVENTORY_PATH)
    inventory_rows = {
        str(item["case_id"]): item for item in inventory.get("cases", [])
    }
    if list(inventory_rows) != expected_ids:
        raise ValueError("Wang source inventory case IDs/order mismatch")

    for row in cases:
        case_id = str(row["case_id"])
        source_row = inventory_rows[case_id]
        if row.get("target_domain") != source_row.get("domain"):
            raise ValueError(f"{case_id}: target domain disagrees with source inventory")
        if row.get("target_palace") != source_row.get("palace"):
            raise ValueError(f"{case_id}: target palace disagrees with source inventory")
        if row.get("source_chart_span_ref") != source_row.get("chart_span_ref"):
            raise ValueError(f"{case_id}: chart span disagrees with source inventory")
        expected_pages = (
            [source_row["source_page_start"]]
            if source_row["source_page_start"] == source_row["source_page_end"]
            else [source_row["source_page_start"], source_row["source_page_end"]]
        )
        if row.get("source_pages") != expected_pages:
            raise ValueError(f"{case_id}: source page range disagrees with inventory")

        direct = row.get("target_palace_main_stars")
        borrowed = row.get("borrowed_from_opposite_main_stars")
        if not isinstance(direct, list) or not isinstance(borrowed, list):
            raise ValueError(f"{case_id}: star-system fields must be arrays")
        if not direct and not borrowed:
            raise ValueError(f"{case_id}: no source-visible major-star system")
        if direct and borrowed:
            raise ValueError(
                f"{case_id}: direct and borrowed major-star systems cannot both be set"
            )
        if bool(row.get("target_palace_empty_main_star")) != (not direct):
            raise ValueError(f"{case_id}: empty-main-star flag mismatch")

        stars = [str(item) for item in direct + borrowed]
        unknown = sorted(set(stars) - MAJOR_STARS)
        if unknown:
            raise ValueError(f"{case_id}: unsupported major stars: {unknown}")
        if len(stars) != len(set(stars)):
            raise ValueError(f"{case_id}: duplicate major-star token")

        span = str(row.get("source_chart_span_ref") or "")
        if not span.startswith("WANG-ANXING-TUIDUAN:") or not span.endswith(":CHART"):
            raise ValueError(f"{case_id}: invalid source chart span ref")

        refs = row.get("fact_refs")
        if not isinstance(refs, list) or len(refs) < 2:
            raise ValueError(f"{case_id}: materialized fact refs missing")
        prefix = f"MATERIALIZED_FACT:{case_id}:TARGET_PALACE:"
        if not all(str(ref).startswith(prefix) for ref in refs):
            raise ValueError(f"{case_id}: materialized fact ref namespace mismatch")

        if row.get("materialization_status") != "PARTIAL_TARGET_PALACE_MATERIALIZED":
            raise ValueError(f"{case_id}: unsupported materialization status")
        if row.get("full_chart_status") != "NOT_MATERIALIZED":
            raise ValueError(f"{case_id}: v0.1 full chart must remain not materialized")

    _validate_lineage(payload)


def load_wang_blind_evidence(
    path: Path = EVIDENCE_PATH,
) -> dict[str, Any]:
    payload = _read_json(path)
    if not isinstance(payload, dict):
        raise ValueError("Wang blind evidence must be a JSON object")
    validate_wang_blind_evidence(payload)
    return payload


def wang_blind_evidence_by_case(
    path: Path = EVIDENCE_PATH,
) -> dict[str, dict[str, Any]]:
    payload = load_wang_blind_evidence(path)
    return {str(item["case_id"]): item for item in payload["cases"]}


def wang_blind_evidence_for_case(
    case_id: str,
    path: Path = EVIDENCE_PATH,
) -> dict[str, Any]:
    by_case = wang_blind_evidence_by_case(path)
    try:
        return by_case[case_id]
    except KeyError as exc:
        raise ValueError(f"unknown Wang blind evidence case: {case_id}") from exc

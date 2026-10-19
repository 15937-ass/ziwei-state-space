"""Auditable Product presentation for a canonical Career inference run.

This module reformats existing rule/evidence records. It does not add Zi Wei
semantics, infer outcomes, or estimate probabilities.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any, Mapping

from .career_natal_domain_provider import (
    load_career_source_mappings,
    load_default_career_natal_provider,
)
from .symbolic_inference_pipeline import SymbolicInferenceRun


_STATUS_MESSAGES = {
    "PARTIAL_TEMPORAL_REGISTRY_EMPTY": (
        "部分完成：本命事业规则已运行，所选大限与流年事实已载入；"
        "但正式时间反应规则库为空，因此不能输出基于时间反应规则的结论。"
    ),
    "PARTIAL_NO_EXECUTABLE_TEMPORAL_RULES": (
        "部分完成：已载入本命和时间层事实，但没有可执行的正式时间反应规则。"
    ),
    "NO_TEMPORAL_REACTION_MATCHED": (
        "没有匹配到时间反应规则；这不代表现实中不会发生相关事件。"
    ),
    "STRUCTURED_TRACE_READY": (
        "已形成可追溯的结构化规则匹配结果；这不代表现实预测准确性已获验证。"
    ),
    "TEST_FIXTURE_ONLY": "当前结果使用测试规则或测试数据，不能作为正式推理结果。",
    "BLOCKED_TEMPORAL_REGISTRY_STATUS": "时间反应规则库状态不符合正式执行要求，时序推理已阻止。",
}


def _load_temporal_blocker_diagnostics(
    path: str | Path,
) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    with Path(path).open("r", encoding="utf-8") as handle:
        diagnostics_document = json.load(handle)
    if not isinstance(diagnostics_document, Mapping):
        raise ValueError("temporal blocker diagnostics must be a JSON object")
    if str(diagnostics_document.get("schema_version", "")).strip() != "0.1":
        raise ValueError("temporal blocker diagnostics schema_version must be 0.1")
    policy = diagnostics_document.get("policy")
    raw_diagnostics = diagnostics_document.get("items")
    if not isinstance(policy, Mapping) or not isinstance(raw_diagnostics, list):
        raise ValueError("temporal blocker diagnostics requires policy and items")
    if policy.get("new_temporal_rule_activation_allowed") is not False:
        raise ValueError("temporal blocker diagnostics must fail closed on activation")
    diagnostic_by_code: dict[str, dict[str, Any]] = {}
    for item in raw_diagnostics:
        if not isinstance(item, Mapping):
            raise ValueError("each temporal blocker diagnostic must be an object")
        code = str(item.get("code", "")).strip()
        if not code or code in diagnostic_by_code:
            raise ValueError("temporal blocker diagnostic code is empty or duplicated")
        if item.get("activation_allowed") is not False:
            raise ValueError(f"{code}: activation_allowed must remain false")
        for required in ("status", "message_zh", "unblock_requirement"):
            if not str(item.get(required, "")).strip():
                raise ValueError(f"{code}: diagnostic {required} is required")
        diagnostic_by_code[code] = dict(item)
    return dict(diagnostics_document), diagnostic_by_code


def build_career_inference_report(
    repository_root: str | Path,
    run: SymbolicInferenceRun,
) -> dict[str, Any]:
    """Build a Chinese-facing report while preserving exact source and status data."""

    if tuple(run.selected_domains) != ("career",):
        raise ValueError("Career report requires exactly the career domain")

    root = Path(repository_root)
    provider = load_default_career_natal_provider(root)
    registry = provider.registry
    mappings = load_career_source_mappings(root, registry)
    product_rules = registry["rules"]
    career_domains = [
        item for item in run.natal_profile.domains if item.domain_id == "career"
    ]
    if len(career_domains) != 1:
        raise ValueError("Career inference run must contain exactly one Career domain")
    domain = career_domains[0]

    projection_by_id: dict[str, dict[str, Any]] = {}
    for raw in domain.projection_payloads:
        payload = json.loads(raw)
        if not isinstance(payload, Mapping):
            raise ValueError("Career projection payload must be a JSON object")
        rule_id = str(payload.get("rule_id", "")).strip()
        if not rule_id or rule_id in projection_by_id:
            raise ValueError("Career projection payload has an empty or duplicate rule_id")
        projection_by_id[rule_id] = dict(payload)

    active_natal_rules: list[dict[str, Any]] = []
    for evidence in domain.active_rules:
        rule_id = evidence.rule_id
        product_rule = product_rules.get(rule_id)
        source_mapping = mappings.get(rule_id)
        projection = projection_by_id.get(rule_id)
        if not isinstance(product_rule, Mapping) or not isinstance(source_mapping, Mapping):
            raise ValueError(f"{rule_id}: active rule lacks registry or mapping provenance")
        if projection is None:
            raise ValueError(f"{rule_id}: active rule lacks its projection payload")
        if (
            evidence.source_id != product_rule.get("expected_source_id")
            or evidence.source_location != product_rule.get("expected_source_location")
            or evidence.review_status != product_rule.get("expected_review_status")
        ):
            raise ValueError(f"{rule_id}: active evidence source does not match Product registry")
        if (
            projection.get("projection_domain") != product_rule.get("expected_projection_domain")
            or projection.get("projection_target") != product_rule.get("expected_projection_target")
            or projection.get("projection_mode") != product_rule.get("expected_projection_mode")
        ):
            raise ValueError(f"{rule_id}: active projection does not match Product registry")

        active_natal_rules.append(
            {
                "rule_id": rule_id,
                "condition": str(product_rule["expected_condition"]),
                "source_summary": str(source_mapping["source_span_summary"]),
                "projection": {
                    "domain": projection["projection_domain"],
                    "target": projection["projection_target"],
                    "mode": projection["projection_mode"],
                },
                "source": {
                    "source_id": evidence.source_id,
                    "source_location": evidence.source_location,
                    "review_status": evidence.review_status,
                    "epistemic": evidence.epistemic,
                },
                "matched_conditions": list(projection.get("matched_conditions", [])),
            }
        )

    active_natal_rules.sort(key=lambda item: item["rule_id"])
    conclusion = run.evidence_package.to_dict().get("conclusion") or {}
    temporal_rule_ids = sorted(item.rule_id for item in run.reaction_report.matched)
    temporal_fact_counts = Counter(item.layer for item in run.temporal_bundle.temporal_facts)

    diagnostics_path = root / "product/PL3T_TEMPORAL_BLOCKERS_v0.1.json"
    diagnostics_document, diagnostic_by_code = _load_temporal_blocker_diagnostics(
        diagnostics_path
    )

    diagnostic_items = []
    for code in sorted(diagnostic_by_code):
        item = dict(diagnostic_by_code[code])
        item["blocks_current_run"] = code in set(run.blockers)
        diagnostic_items.append(item)
    active_diagnostics = [
        item for item in diagnostic_items if item["blocks_current_run"]
    ]

    return {
        "schema_version": "0.1",
        "run_id": run.run_id,
        "question": run.question,
        "target_id": run.target_id,
        "status": run.status,
        "status_message_zh": _STATUS_MESSAGES.get(
            run.status,
            "推理结果已生成；请同时检查状态、阻塞项和限制条件。",
        ),
        "selected_domains": list(run.selected_domains),
        "selected_temporal_layers": list(run.selected_temporal_layers),
        "natal": {
            "profile_id": run.natal_profile.profile_id,
            "knowledge_version": run.natal_profile.knowledge_version,
            "active_rule_count": len(active_natal_rules),
            "active_rules": active_natal_rules,
            "confidence_band": domain.confidence_band,
            "confidence_rationale": domain.confidence_rationale,
        },
        "temporal": {
            "profile_id": run.temporal_profile.profile_id,
            "target_label": run.temporal_profile.target_label,
            "active_layers": list(run.temporal_profile.active_layers),
            "fact_count_by_layer": {
                layer: temporal_fact_counts[layer]
                for layer in sorted(temporal_fact_counts)
            },
            "reaction_registry_status": run.reaction_registry_status,
            "reaction_rule_count": run.reaction_rule_count,
            "matched_reaction_rule_ids": temporal_rule_ids,
            "has_temporal_reaction_evidence": bool(temporal_rule_ids),
            "external_event_trigger_used": run.temporal_profile.external_event_trigger_used,
            "event_relative_context": [
                {
                    "context_id": item.context_id,
                    "status": item.status,
                    "source": {
                        "source_id": item.source_id,
                        "source_location": item.source_location,
                        "review_status": item.review_status,
                    },
                    "trigger_provenance": item.trigger_provenance,
                    "routing_facts": list(item.routing_facts),
                }
                for item in run.temporal_profile.event_relative_context
            ],
            "readiness_diagnostics": {
                "diagnostic_set_id": diagnostics_document.get("diagnostic_set_id"),
                "status": diagnostics_document.get("status"),
                "active_blockers": active_diagnostics,
                "unresolved_gaps": diagnostic_items,
                "new_temporal_rule_activation_allowed": False,
            },
        },
        "blockers": list(run.blockers),
        "unknowns": list(conclusion.get("unknowns", [])),
        "conflicts": list(conclusion.get("conflicts", [])),
        "limitations": sorted(
            set(conclusion.get("limitations", []))
            | {
                "REAL_WORLD_EVENT_PREDICTION_NOT_ESTABLISHED",
                "SOURCE_RULES_NOT_EMPIRICALLY_CALIBRATED",
            }
            | (
                {"EVENT_RELATIVE_CONTEXT_IS_NOT_A_TEMPORAL_REACTION"}
                if run.temporal_profile.event_relative_context
                else set()
            )
        ),
        "real_world_event_prediction_supported": False,
    }

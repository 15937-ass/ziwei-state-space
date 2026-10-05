"""Deterministic bridge from ActiveRuleGraph to EvidencePackage.

The bridge does not choose rules and does not create new Zi Wei semantics.
It serializes already-compiled RuleIR and runtime match results into a stable
product-facing evidence contract.
"""

from __future__ import annotations

from typing import Any, Iterable, Mapping

from .evidence_package import (
    ConfidenceBand,
    ConflictItem,
    ContrastiveItem,
    EvidenceItem,
    EvidencePackage,
)
from .rule_runtime import ActiveRuleGraph, RuleIR


def _rule_index(rules: Iterable[RuleIR]) -> dict[str, RuleIR]:
    out: dict[str, RuleIR] = {}
    for rule in rules:
        if rule.rule_id in out:
            raise ValueError(f"duplicate RuleIR id in evidence bridge: {rule.rule_id}")
        out[rule.rule_id] = rule
    return out


def _contrastive_item(
    rule: RuleIR,
    facts: frozenset[str],
    active_rule_ids: frozenset[str],
) -> ContrastiveItem:
    missing = tuple(sorted(set(rule.required_facts) - set(facts)))
    unsatisfied_any: list[tuple[str, ...]] = []
    for group in rule.any_of_facts:
        if not set(group).intersection(facts):
            unsatisfied_any.append(tuple(group))
    blocked = tuple(sorted(set(rule.forbidden_facts).intersection(facts)))
    return ContrastiveItem(
        rule_id=rule.rule_id,
        candidate_claim=rule.target_state,
        missing_all_of=missing,
        unsatisfied_any_of=tuple(unsatisfied_any),
        blocked_by=blocked,
        missing_antecedents=tuple(
            sorted(set(rule.antecedent_rule_ids) - set(active_rule_ids))
        ),
    )


def determine_confidence(
    *,
    active_count: int,
    conflicts: int,
    coverage: Mapping[str, Any],
) -> tuple[ConfidenceBand, str]:
    """Conservative deterministic confidence for the symbolic layer.

    HIGH_CONFIDENCE is intentionally unreachable here. It is reserved for a
    later calibrated product layer with external evaluation.
    """

    if conflicts:
        return (
            ConfidenceBand.CONFLICTED,
            "explicit_rule_conflict_present",
        )
    if active_count == 0:
        return (
            ConfidenceBand.INSUFFICIENT_EVIDENCE,
            "no_executable_rule_activated",
        )

    pending = int(coverage.get("NORMALIZATION_PENDING", 0) or 0)
    holds = int(coverage.get("PATH_DEPENDENT_HOLD", 0) or 0)
    if pending > 0 or holds > 0:
        return (
            ConfidenceBand.LOW_CONFIDENCE,
            "bounded_executable_coverage_with_unresolved_rules",
        )

    return (
        ConfidenceBand.MEDIUM_CONFIDENCE,
        "complete_symbolic_coverage_without_external_calibration",
    )


def graph_to_evidence_package(
    graph: ActiveRuleGraph,
    rules: Iterable[RuleIR],
    *,
    facts: frozenset[str],
    question: str,
    coverage: Mapping[str, Any] | None = None,
    chart_facts: Mapping[str, Any] | None = None,
    engine_version: str = "",
    knowledge_version: str = "",
) -> EvidencePackage:
    """Convert an already-resolved graph to an auditable EvidencePackage."""

    rule_by_id = _rule_index(rules)
    active_ids = {node.rule_id for node in graph.nodes}
    missing_nodes = sorted(active_ids - set(rule_by_id))
    if missing_nodes:
        raise ValueError(
            "ActiveRuleGraph contains rule ids absent from RuleIR set: "
            + ", ".join(missing_nodes)
        )

    active_rules: list[EvidenceItem] = []
    projections: list[dict[str, Any]] = []

    for node in sorted(graph.nodes, key=lambda item: item.rule_id):
        rule = rule_by_id[node.rule_id]
        active_rules.append(
            EvidenceItem(
                rule_id=rule.rule_id,
                claim=rule.target_state,
                source_id=rule.source_work,
                source_location=rule.source_location,
                epistemic=rule.source_epistemic,
                review_status=rule.review_status,
            )
        )
        projections.append(
            {
                "rule_id": rule.rule_id,
                "projection_domain": rule.target_type,
                "projection_target": rule.target_state,
                "projection_mode": rule.state_change,
                "operator": rule.operator,
                "matched_conditions": list(node.matched_conditions),
                "matched_antecedents": list(node.matched_antecedents),
                "source_pointer": rule.source_pointer,
                "evidence_status": node.evidence_status,
            }
        )

    conflicts = [
        ConflictItem(
            conflict_id=group,
            description="multiple active rules share an explicit conflict group",
            rule_ids=tuple(rule_ids),
        )
        for group, rule_ids in sorted(graph.conflict_groups.items())
    ]

    contrastive = [
        _contrastive_item(rule, facts, frozenset(active_ids))
        for rule in sorted(rule_by_id.values(), key=lambda item: item.rule_id)
        if rule.rule_id not in active_ids
    ]

    coverage_payload = dict(coverage or {})
    band, rationale = determine_confidence(
        active_count=len(active_rules),
        conflicts=len(conflicts),
        coverage=coverage_payload,
    )

    payload_facts = dict(chart_facts or {})
    payload_facts.setdefault("facts", sorted(facts))

    package = EvidencePackage(
        question=question,
        chart_facts=payload_facts,
        active_rules=active_rules,
        projections=projections,
        conflicts=conflicts,
        contrastive=contrastive,
        coverage=coverage_payload,
        confidence_band=band,
        confidence_rationale=rationale,
        engine_version=engine_version,
        knowledge_version=knowledge_version,
    )
    package.validate()
    return package

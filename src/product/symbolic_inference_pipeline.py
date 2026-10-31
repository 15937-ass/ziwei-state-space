"""End-to-end deterministic PL3 symbolic inference orchestration.

This module composes approved components; it does not infer new traditional
semantics, select rules with an LLM, or estimate real-world event probabilities.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, replace
from typing import Any, Iterable, Mapping

from .canonical_chart_contract import validate_canonical_production_chart_snapshot
from .layered_evidence_package import (
    EvidenceReference,
    LayeredEvidencePackage,
    StructuredInferenceConclusion,
    build_layered_evidence_package,
)
from .natal_domain_registry import NatalDomainProviderRegistry
from .natal_prior import NatalStateProfile
from .temporal_asset_adapter import (
    TemporalAssetBundle,
    adapt_target_from_full_snapshot,
    build_temporal_environment_from_assets,
)
from .temporal_environment import (
    TEMPORAL_LAYERS,
    EventRelativeContextEvidence,
    TemporalEnvironmentProfile,
)
from .temporal_reaction_compiler import (
    TemporalReactionMatchReport,
    compile_temporal_reaction_registry,
    match_temporal_reactions,
)


EMPTY_REACTION_REGISTRY_STATUS = "EMPTY_UNTIL_KB_WP07B_STRUCTURED_NORMALIZATION"
TEST_ONLY_REACTION_REGISTRY_STATUS = "TEST_FIXTURE_ONLY_NOT_CANONICAL"
CANONICAL_REACTION_REGISTRY_STATUS = "CANONICAL_READY"

RUN_STATUSES = frozenset(
    {
        "STRUCTURED_TRACE_READY",
        "NO_TEMPORAL_REACTION_MATCHED",
        "PARTIAL_TEMPORAL_REGISTRY_EMPTY",
        "PARTIAL_NO_EXECUTABLE_TEMPORAL_RULES",
        "BLOCKED_TEMPORAL_REGISTRY_STATUS",
        "TEST_FIXTURE_ONLY",
    }
)


@dataclass(frozen=True)
class SymbolicInferenceRun:
    """One deterministic, source-traceable inference execution."""

    schema_version: str
    run_id: str
    question: str
    target_id: str
    selected_domains: tuple[str, ...]
    selected_temporal_layers: tuple[str, ...]
    status: str
    blockers: tuple[str, ...]
    reaction_registry_status: str
    reaction_rule_count: int
    natal_profile: NatalStateProfile
    temporal_bundle: TemporalAssetBundle
    temporal_profile: TemporalEnvironmentProfile
    reaction_report: TemporalReactionMatchReport
    evidence_package: LayeredEvidencePackage

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "run_id": self.run_id,
            "question": self.question,
            "target_id": self.target_id,
            "selected_domains": list(self.selected_domains),
            "selected_temporal_layers": list(self.selected_temporal_layers),
            "status": self.status,
            "blockers": list(self.blockers),
            "reaction_registry": {
                "status": self.reaction_registry_status,
                "rule_count": self.reaction_rule_count,
            },
            "natal_profile": self.natal_profile.to_dict(),
            "temporal_bundle": {
                "target_id": self.temporal_bundle.target_id,
                "solar_date": self.temporal_bundle.solar_date,
                "lunar_date": self.temporal_bundle.lunar_date,
                "time_index": self.temporal_bundle.time_index,
                "engine_name": self.temporal_bundle.engine_name,
                "engine_version": self.temporal_bundle.engine_version,
                "adapter_version": self.temporal_bundle.adapter_version,
                "temporal_facts": [
                    asdict(item) for item in self.temporal_bundle.temporal_facts
                ],
                "condition_facts": list(self.temporal_bundle.condition_facts),
            },
            "temporal_profile": self.temporal_profile.to_dict(),
            "reaction_report": {
                "matched": [asdict(item) for item in self.reaction_report.matched],
                "issues": [asdict(item) for item in self.reaction_report.issues],
                "counts": self.reaction_report.counts(),
            },
            "evidence_package": self.evidence_package.to_dict(),
        }


def _stable_run_id(payload: Mapping[str, Any]) -> str:
    raw = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return "INFER-" + hashlib.sha256(raw).hexdigest()[:24]


def _build_structured_conclusion(
    *,
    question: str,
    target_id: str,
    selected_domains: tuple[str, ...],
    selected_temporal_layers: tuple[str, ...],
    run_status: str,
    blockers: tuple[str, ...],
    natal_profile: NatalStateProfile,
    temporal_profile: TemporalEnvironmentProfile,
    reaction_report: TemporalReactionMatchReport,
) -> StructuredInferenceConclusion:
    canonical_rules = tuple(
        sorted(
            (
                rule
                for domain in natal_profile.domains
                for rule in domain.active_rules
            ),
            key=lambda item: (item.rule_id, item.source_id, item.source_location),
        )
    )
    temporal_rules = tuple(
        sorted(
            reaction_report.matched,
            key=lambda item: (item.rule_id, item.source_id, item.source_location),
        )
    )
    canonical_rule_ids = tuple(sorted({item.rule_id for item in canonical_rules}))
    temporal_rule_ids = tuple(sorted({item.rule_id for item in temporal_rules}))

    evidence_refs = tuple(
        sorted(
            [
                EvidenceReference(
                    namespace="CANONICAL",
                    rule_id=item.rule_id,
                    source_id=item.source_id,
                    source_location=item.source_location,
                    review_status=item.review_status,
                )
                for item in canonical_rules
            ]
            + [
                EvidenceReference(
                    namespace="TEMPORAL",
                    rule_id=item.rule_id,
                    source_id=item.source_id,
                    source_location=item.source_location,
                    review_status=item.review_status,
                )
                for item in temporal_rules
            ],
            key=lambda item: (
                item.namespace,
                item.rule_id,
                item.source_id,
                item.source_location,
            ),
        )
    )

    unknowns = list(blockers)
    unknowns.extend(
        f"TEMPORAL_RULE_UNRESOLVED:{item.rule_id}:{item.reason}"
        for item in reaction_report.issues
    )
    if not canonical_rule_ids:
        unknowns.append("NO_ACTIVE_NATAL_RULES_MATCHED")
    if run_status == "NO_TEMPORAL_REACTION_MATCHED":
        unknowns.append("NO_TEMPORAL_REACTION_MATCHED_FOR_TARGET")

    if blockers:
        conclusion_status = "PARTIAL"
    elif temporal_rule_ids:
        conclusion_status = "TRACEABLE"
    elif canonical_rule_ids:
        conclusion_status = "NO_TEMPORAL_MATCH"
    else:
        conclusion_status = "INSUFFICIENT_EVIDENCE"

    limitations = [
        "NO_REAL_WORLD_EVENT_CLAIM",
        "NO_NUMERIC_PROBABILITY_OR_MAGNITUDE_ESTIMATED",
    ]
    if run_status != "STRUCTURED_TRACE_READY":
        limitations.append("TEMPORAL_CONCLUSION_NOT_FULLY_RESOLVED")
    if not canonical_rule_ids:
        limitations.append("NO_ACTIVE_CANONICAL_RULE_EVIDENCE")

    return StructuredInferenceConclusion(
        schema_version="0.1",
        status=conclusion_status,
        question=question,
        target_id=target_id,
        selected_domains=selected_domains,
        selected_temporal_layers=selected_temporal_layers,
        canonical_rule_ids=canonical_rule_ids,
        temporal_reaction_rule_ids=temporal_rule_ids,
        evidence_refs=evidence_refs,
        conflicts=tuple(temporal_profile.conflicts),
        unknowns=tuple(sorted(set(unknowns))),
        limitations=tuple(sorted(set(limitations))),
    )


def _condition_fact_layer(condition_fact: str) -> str | None:
    if not condition_fact.startswith("atom:"):
        return None
    try:
        payload = json.loads(condition_fact[len("atom:"):])
    except (TypeError, ValueError, json.JSONDecodeError):
        return None
    args = payload.get("args") if isinstance(payload, Mapping) else None
    if not isinstance(args, Mapping):
        return None
    layer = str(args.get("layer", "")).strip()
    return layer or None


def _select_temporal_layers(
    bundle: TemporalAssetBundle,
    selected_layers: tuple[str, ...],
) -> TemporalAssetBundle:
    selected = frozenset(selected_layers)
    temporal_facts = tuple(
        item for item in bundle.temporal_facts if item.layer in selected
    )
    condition_facts = tuple(
        sorted(
            fact
            for fact in bundle.condition_facts
            if _condition_fact_layer(fact) in selected
        )
    )
    observed_layers = {item.layer for item in temporal_facts}
    if observed_layers != selected:
        missing = sorted(selected - observed_layers)
        raise ValueError(
            "selected temporal layer(s) have no adapted facts: " + ", ".join(missing)
        )
    return replace(
        bundle,
        temporal_facts=temporal_facts,
        condition_facts=condition_facts,
    )


def run_symbolic_inference(
    normalized_snapshot: Mapping[str, Any],
    *,
    target_id: str,
    question: str,
    domain_registry: NatalDomainProviderRegistry,
    reaction_registry_document: Mapping[str, Any],
    selected_domains: Iterable[str] | None = None,
    selected_temporal_layers: Iterable[str] | None = None,
    domain_questions: Mapping[str, str] | None = None,
    temporal_conflicts: Iterable[str] = (),
    event_relative_context: Iterable[EventRelativeContextEvidence] = (),
) -> SymbolicInferenceRun:
    """Run the deterministic chart -> natal -> temporal -> evidence path.

    The same normalized snapshot is used for both natal and temporal processing,
    preventing accidental mixing of chart engines or people. Empty or test-only
    reaction registries are surfaced as explicit blockers, never as success.
    """

    normalized_question = str(question or "").strip()
    normalized_target_id = str(target_id or "").strip()
    if not normalized_question:
        raise ValueError("question is required")
    if not normalized_target_id:
        raise ValueError("target_id is required")
    if not isinstance(normalized_snapshot, Mapping):
        raise ValueError("normalized_snapshot must be an object")
    canonical_validation = validate_canonical_production_chart_snapshot(
        normalized_snapshot
    )
    if not canonical_validation.ok:
        raise ValueError(
            "non-canonical production chart snapshot: "
            + "; ".join(canonical_validation.errors)
        )
    if not isinstance(reaction_registry_document, Mapping):
        raise ValueError("reaction_registry_document must be an object")

    if selected_domains is None:
        domains = tuple(domain_registry.domain_ids)
    else:
        domains = tuple(
            sorted({str(item).strip() for item in selected_domains if str(item).strip()})
        )
    if not domains:
        raise ValueError("at least one selected domain is required")

    provided_questions = dict(domain_questions or {})
    unknown_question_domains = sorted(set(provided_questions) - set(domains))
    if unknown_question_domains:
        raise ValueError(
            "domain question supplied for unselected domain(s): "
            + ", ".join(unknown_question_domains)
        )
    questions = {
        domain: str(provided_questions.get(domain, normalized_question)).strip()
        or normalized_question
        for domain in domains
    }

    natal_profile = domain_registry.build_profile(
        normalized_snapshot,
        selected_domains=domains,
        questions=questions,
    )
    temporal_bundle = adapt_target_from_full_snapshot(
        normalized_snapshot,
        target_id=normalized_target_id,
    )
    available_layers = {item.layer for item in temporal_bundle.temporal_facts}
    if selected_temporal_layers is None:
        temporal_layers = tuple(sorted(available_layers))
    else:
        if isinstance(selected_temporal_layers, (str, bytes)):
            raise ValueError("selected_temporal_layers must be an array of layer IDs")
        temporal_layers = tuple(
            sorted(
                {
                    str(item).strip()
                    for item in selected_temporal_layers
                    if str(item).strip()
                }
            )
        )
        if not temporal_layers:
            raise ValueError("at least one selected temporal layer is required")
        unsupported_layers = sorted(set(temporal_layers) - TEMPORAL_LAYERS)
        if unsupported_layers:
            raise ValueError(
                "unsupported selected temporal layer(s): "
                + ", ".join(unsupported_layers)
            )
        unavailable_layers = sorted(set(temporal_layers) - available_layers)
        if unavailable_layers:
            raise ValueError(
                "selected temporal layer(s) not present in target: "
                + ", ".join(unavailable_layers)
            )
        temporal_bundle = _select_temporal_layers(temporal_bundle, temporal_layers)

    expected_engine = ":".join(
        value
        for value in (
            temporal_bundle.engine_name,
            temporal_bundle.engine_version,
            temporal_bundle.adapter_version,
        )
        if value
    )
    if natal_profile.engine_version != expected_engine:
        raise ValueError(
            "natal and temporal engine provenance mismatch: "
            f"{natal_profile.engine_version!r} != {expected_engine!r}"
        )

    registry_status = str(reaction_registry_document.get("status") or "").strip()
    rules = compile_temporal_reaction_registry(reaction_registry_document)
    reaction_report = match_temporal_reactions(natal_profile, temporal_bundle, rules)

    temporal_profile = build_temporal_environment_from_assets(
        natal_profile,
        temporal_bundle,
        reactions=reaction_report.matched,
        conflicts=temporal_conflicts,
        event_relative_context=event_relative_context,
    )
    if registry_status == TEST_ONLY_REACTION_REGISTRY_STATUS:
        status = "TEST_FIXTURE_ONLY"
        blockers = ("NON_CANONICAL_TEMPORAL_REACTION_REGISTRY",)
    elif registry_status == EMPTY_REACTION_REGISTRY_STATUS and not rules:
        status = "PARTIAL_TEMPORAL_REGISTRY_EMPTY"
        blockers = ("PRODUCTION_TEMPORAL_REACTION_REGISTRY_EMPTY",)
    elif registry_status != CANONICAL_REACTION_REGISTRY_STATUS:
        status = "BLOCKED_TEMPORAL_REGISTRY_STATUS"
        blockers = ("TEMPORAL_REACTION_REGISTRY_NOT_CANONICAL_READY",)
    elif not rules:
        status = "PARTIAL_NO_EXECUTABLE_TEMPORAL_RULES"
        blockers = ("CANONICAL_TEMPORAL_REACTION_REGISTRY_EMPTY",)
    elif reaction_report.matched:
        status = "STRUCTURED_TRACE_READY"
        blockers = ()
    else:
        status = "NO_TEMPORAL_REACTION_MATCHED"
        blockers = ()

    selected_test_only_domains = set(domains).intersection(
        domain_registry.test_only_domain_ids
    )
    if selected_test_only_domains:
        status = "TEST_FIXTURE_ONLY"
        blockers = tuple(
            sorted(set(blockers) | {"NON_CANONICAL_NATAL_DOMAIN_PROVIDER"})
        )

    conclusion = _build_structured_conclusion(
        question=normalized_question,
        target_id=normalized_target_id,
        selected_domains=domains,
        selected_temporal_layers=temporal_layers,
        run_status=status,
        blockers=blockers,
        natal_profile=natal_profile,
        temporal_profile=temporal_profile,
        reaction_report=reaction_report,
    )
    evidence_package = build_layered_evidence_package(
        question=normalized_question,
        natal_profile=natal_profile,
        temporal_profile=temporal_profile,
        conclusion=conclusion,
    )

    run_identity = {
        "schema_version": "0.1",
        "question": normalized_question,
        "target_id": normalized_target_id,
        "selected_domains": list(domains),
        "selected_temporal_layers": list(temporal_layers),
        "natal_profile_id": natal_profile.profile_id,
        "temporal_profile_id": temporal_profile.profile_id,
        "reaction_registry_status": registry_status,
        "reaction_rule_ids": [item.rule_id for item in rules],
        "matched_rule_ids": [item.rule_id for item in reaction_report.matched],
        "reaction_issues": [
            {"rule_id": item.rule_id, "reason": item.reason}
            for item in reaction_report.issues
        ],
        "status": status,
        "blockers": list(blockers),
        "structured_conclusion": conclusion.to_dict(),
    }
    run_id = _stable_run_id(run_identity)

    return SymbolicInferenceRun(
        schema_version="0.1",
        run_id=run_id,
        question=normalized_question,
        target_id=normalized_target_id,
        selected_domains=domains,
        selected_temporal_layers=temporal_layers,
        status=status,
        blockers=blockers,
        reaction_registry_status=registry_status,
        reaction_rule_count=len(rules),
        natal_profile=natal_profile,
        temporal_bundle=temporal_bundle,
        temporal_profile=temporal_profile,
        reaction_report=reaction_report,
        evidence_package=evidence_package,
    )

"""PL3-M0 canonical manifestation candidate integration v0.1.

M0 is the first source-supported manifestation layer after ResponseProfile tau.
It is deliberately weaker than a prediction:

    tau + source-reviewed manifestation ontology/mappings -> possible M0

This module never infers manifestation meaning from projection prose, raw chart
facts, or reaction effect names. Only symbolic rule IDs present in actual tau
entries are exposed to the existing manifestation router. No activation IDs
are invented.

Production remains fail-closed while the canonical manifestation ontology and
mapping registries are pending Knowledge WP06B/WP06C.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any

from .manifestation_ontology import ManifestationOntologyRegistry, ManifestationSourceRef
from .manifestation_router import (
    HeldManifestationMapping,
    ManifestationMappingRegistry,
    SourceSupportedPossibility,
    SymbolicActivationContext,
    route_source_supported_possibilities,
)
from .response_profile import CareerResponseEntry, CareerResponseProfile


M0_SCHEMA_VERSION = "0.1"
M0_COMPILER_VERSION = "PL3M0_CANONICAL_MANIFESTATION_CANDIDATES_V0_1"
M0_DISPOSITIONS = frozenset(
    {
        "ROUTED",
        "UPSTREAM_RESPONSE_NOT_READY",
        "ONTOLOGY_NOT_READY",
        "MAPPING_REGISTRY_NOT_READY",
        "NO_ACTIVE_MAPPING",
    }
)


@dataclass(frozen=True)
class M0ResponseSupport:
    response_entry_ref: str
    natal_rule_id: str
    temporal_rule_id: str
    temporal_reaction_id: str
    effect: str
    effect_target: str
    natal_source_location: str
    natal_source_span_ids: tuple[str, ...]
    temporal_source_id: str
    temporal_source_location: str

    def __post_init__(self) -> None:
        required = {
            "response_entry_ref": self.response_entry_ref,
            "natal_rule_id": self.natal_rule_id,
            "temporal_rule_id": self.temporal_rule_id,
            "temporal_reaction_id": self.temporal_reaction_id,
            "effect": self.effect,
            "effect_target": self.effect_target,
            "natal_source_location": self.natal_source_location,
            "temporal_source_id": self.temporal_source_id,
            "temporal_source_location": self.temporal_source_location,
        }
        missing = [name for name, value in required.items() if not str(value).strip()]
        if missing:
            raise ValueError("M0ResponseSupport missing: " + ", ".join(missing))
        if not self.natal_source_span_ids:
            raise ValueError("M0ResponseSupport requires natal source spans")


@dataclass(frozen=True)
class CareerManifestationCandidate:
    candidate_id: str
    possibility_status: str
    mapping_id: str
    manifestation_id: str
    domain: str
    abstraction_level: str
    event_specificity: str
    source_supported_labels: tuple[str, ...]
    evidence_tier: str
    matched_rule_ids: tuple[str, ...]
    response_support: tuple[M0ResponseSupport, ...]
    mapping_source_refs: tuple[ManifestationSourceRef, ...]
    ontology_source_refs: tuple[ManifestationSourceRef, ...]
    probability_status: str = "UNKNOWN"

    def __post_init__(self) -> None:
        if not self.candidate_id.strip():
            raise ValueError("CareerManifestationCandidate.candidate_id is required")
        if self.possibility_status != "SOURCE_SUPPORTED_POSSIBILITY":
            raise ValueError("M0 candidate must remain SOURCE_SUPPORTED_POSSIBILITY")
        if self.probability_status != "UNKNOWN":
            raise ValueError("M0 candidate probability_status must remain UNKNOWN")
        if not self.matched_rule_ids:
            raise ValueError("M0 candidate requires matched rule IDs")
        if not self.response_support:
            raise ValueError("M0 candidate requires tau response support")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CareerManifestationCandidatesM0:
    schema_version: str
    result_id: str
    compiler_version: str
    response_profile_id: str
    knowledge_version: str
    target_label: str
    disposition: str
    candidates: tuple[CareerManifestationCandidate, ...]
    held_mappings: tuple[HeldManifestationMapping, ...]
    ontology_status: str
    mapping_registry_status: str
    upstream_unknowns: tuple[str, ...]
    blockers: tuple[str, ...]
    probability_status: str = "UNKNOWN"
    empirical_probability_used: bool = False
    ranking_used: bool = False
    personalized_context_used: bool = False

    def __post_init__(self) -> None:
        if self.schema_version != M0_SCHEMA_VERSION:
            raise ValueError("M0 schema_version must be 0.1")
        for value, name in (
            (self.result_id, "result_id"),
            (self.compiler_version, "compiler_version"),
            (self.response_profile_id, "response_profile_id"),
            (self.knowledge_version, "knowledge_version"),
            (self.target_label, "target_label"),
            (self.disposition, "disposition"),
            (self.ontology_status, "ontology_status"),
            (self.mapping_registry_status, "mapping_registry_status"),
        ):
            if not str(value).strip():
                raise ValueError(f"CareerManifestationCandidatesM0.{name} is required")
        if self.disposition not in M0_DISPOSITIONS:
            raise ValueError(f"unsupported M0 disposition: {self.disposition}")
        if self.probability_status != "UNKNOWN":
            raise ValueError("M0 probability_status must remain UNKNOWN")
        forbidden = {
            "empirical_probability_used": self.empirical_probability_used,
            "ranking_used": self.ranking_used,
            "personalized_context_used": self.personalized_context_used,
        }
        active = [name for name, value in forbidden.items() if value]
        if active:
            raise ValueError(
                "M0 is canonical source-supported possibility only; forbidden: "
                + ", ".join(active)
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "result_id": self.result_id,
            "compiler_version": self.compiler_version,
            "response_profile_id": self.response_profile_id,
            "knowledge_version": self.knowledge_version,
            "target_label": self.target_label,
            "disposition": self.disposition,
            "candidates": [item.to_dict() for item in self.candidates],
            "held_mappings": [asdict(item) for item in self.held_mappings],
            "ontology_status": self.ontology_status,
            "mapping_registry_status": self.mapping_registry_status,
            "upstream_unknowns": list(self.upstream_unknowns),
            "blockers": list(self.blockers),
            "probability_status": self.probability_status,
            "empirical_probability_used": self.empirical_probability_used,
            "ranking_used": self.ranking_used,
            "personalized_context_used": self.personalized_context_used,
        }


def _entry_ref(entry: CareerResponseEntry) -> str:
    return (
        f"TAU_ENTRY:{entry.natal_rule_id}:"
        f"{entry.temporal_rule_id}:{entry.temporal_reaction_id}"
    )


def _support_from_entry(entry: CareerResponseEntry) -> M0ResponseSupport:
    return M0ResponseSupport(
        response_entry_ref=_entry_ref(entry),
        natal_rule_id=entry.natal_rule_id,
        temporal_rule_id=entry.temporal_rule_id,
        temporal_reaction_id=entry.temporal_reaction_id,
        effect=entry.effect,
        effect_target=entry.effect_target,
        natal_source_location=entry.natal_source_location,
        natal_source_span_ids=entry.natal_source_span_ids,
        temporal_source_id=entry.temporal_source_id,
        temporal_source_location=entry.temporal_source_location,
    )


def _candidate_id(
    response_profile_id: str,
    possibility: SourceSupportedPossibility,
) -> str:
    raw = json.dumps(
        {
            "response_profile_id": response_profile_id,
            "mapping_id": possibility.mapping_id,
            "manifestation_id": possibility.manifestation_id,
            "matched_rule_ids": list(possibility.matched_rule_ids),
        },
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return "M0C-" + hashlib.sha256(raw).hexdigest()[:20]


def _candidate_from_possibility(
    response_profile: CareerResponseProfile,
    possibility: SourceSupportedPossibility,
) -> CareerManifestationCandidate:
    matched = set(possibility.matched_rule_ids)
    support_by_ref: dict[str, M0ResponseSupport] = {}

    for entry in response_profile.entries:
        if entry.natal_rule_id in matched or entry.temporal_rule_id in matched:
            support = _support_from_entry(entry)
            support_by_ref[support.response_entry_ref] = support

    support = tuple(
        support_by_ref[key]
        for key in sorted(support_by_ref)
    )
    if not support:
        raise ValueError(
            f"{possibility.mapping_id}: routed possibility has no actual tau support"
        )

    return CareerManifestationCandidate(
        candidate_id=_candidate_id(response_profile.profile_id, possibility),
        possibility_status=possibility.possibility_status,
        mapping_id=possibility.mapping_id,
        manifestation_id=possibility.manifestation_id,
        domain=possibility.domain,
        abstraction_level=possibility.abstraction_level,
        event_specificity=possibility.event_specificity,
        source_supported_labels=possibility.source_supported_labels,
        evidence_tier=possibility.evidence_tier,
        matched_rule_ids=possibility.matched_rule_ids,
        response_support=support,
        mapping_source_refs=possibility.mapping_source_refs,
        ontology_source_refs=possibility.ontology_source_refs,
        probability_status=possibility.probability_status,
    )


def _readiness_blockers(
    ontology: ManifestationOntologyRegistry,
    mappings: ManifestationMappingRegistry,
) -> tuple[str, ...]:
    blockers: list[str] = []
    if ontology.registry_status == "EMPTY_PENDING_KB_WP06B":
        blockers.append("ONTOLOGY_NOT_READY")
    if mappings.registry_status == "EMPTY_PENDING_KB_WP06C":
        blockers.append("MAPPING_REGISTRY_NOT_READY")
    return tuple(sorted(blockers))


def _result_id(
    *,
    response_profile: CareerResponseProfile,
    disposition: str,
    candidates: tuple[CareerManifestationCandidate, ...],
    held_mappings: tuple[HeldManifestationMapping, ...],
    ontology_status: str,
    mapping_registry_status: str,
    upstream_unknowns: tuple[str, ...],
    blockers: tuple[str, ...],
) -> str:
    payload = {
        "response_profile_id": response_profile.profile_id,
        "knowledge_version": response_profile.knowledge_version,
        "target_label": response_profile.target_label,
        "disposition": disposition,
        "candidates": [item.to_dict() for item in candidates],
        "held_mappings": [asdict(item) for item in held_mappings],
        "ontology_status": ontology_status,
        "mapping_registry_status": mapping_registry_status,
        "upstream_unknowns": list(upstream_unknowns),
        "blockers": list(blockers),
    }
    raw = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return "M0-" + hashlib.sha256(raw).hexdigest()[:24]


def build_career_manifestation_candidates_m0(
    response_profile: CareerResponseProfile,
    ontology: ManifestationOntologyRegistry,
    mappings: ManifestationMappingRegistry,
) -> CareerManifestationCandidatesM0:
    """Route tau into source-supported M0 without inventing manifestation semantics."""

    upstream_unknowns = tuple(sorted(set(response_profile.unknowns)))
    readiness = _readiness_blockers(ontology, mappings)

    if not response_profile.entries:
        blockers = tuple(
            sorted(
                set(readiness)
                | {"UPSTREAM_RESPONSE_PROFILE_HAS_NO_DYNAMIC_ENTRIES"}
            )
        )
        disposition = "UPSTREAM_RESPONSE_NOT_READY"
        candidates: tuple[CareerManifestationCandidate, ...] = ()
        held: tuple[HeldManifestationMapping, ...] = ()
    else:
        # Intentional: tau v0.1 carries explicit rule IDs but no canonical
        # activation ontology. Do not synthesize activation IDs from effect names.
        active_rule_ids = tuple(
            sorted(
                {
                    rule_id
                    for entry in response_profile.entries
                    for rule_id in (entry.natal_rule_id, entry.temporal_rule_id)
                    if rule_id
                }
            )
        )
        context = SymbolicActivationContext(
            active_activation_ids=(),
            active_rule_ids=active_rule_ids,
            evidence_refs=tuple(
                sorted(_entry_ref(entry) for entry in response_profile.entries)
            ),
        )
        routed = route_source_supported_possibilities(ontology, mappings, context)
        disposition = routed.disposition
        held = routed.held_mappings
        candidates = tuple(
            sorted(
                (
                    _candidate_from_possibility(response_profile, possibility)
                    for possibility in routed.possibilities
                ),
                key=lambda item: (item.manifestation_id, item.mapping_id),
            )
        )

        blocker_set = set(readiness)
        if disposition == "NO_ACTIVE_MAPPING":
            blocker_set.add("NO_ACTIVE_SOURCE_SUPPORTED_MAPPING")
        elif disposition == "ONTOLOGY_NOT_READY":
            blocker_set.add("ONTOLOGY_NOT_READY")
        elif disposition == "MAPPING_REGISTRY_NOT_READY":
            blocker_set.add("MAPPING_REGISTRY_NOT_READY")
        blockers = tuple(sorted(blocker_set))

    result_id = _result_id(
        response_profile=response_profile,
        disposition=disposition,
        candidates=candidates,
        held_mappings=held,
        ontology_status=ontology.registry_status,
        mapping_registry_status=mappings.registry_status,
        upstream_unknowns=upstream_unknowns,
        blockers=blockers,
    )

    return CareerManifestationCandidatesM0(
        schema_version=M0_SCHEMA_VERSION,
        result_id=result_id,
        compiler_version=M0_COMPILER_VERSION,
        response_profile_id=response_profile.profile_id,
        knowledge_version=response_profile.knowledge_version,
        target_label=response_profile.target_label,
        disposition=disposition,
        candidates=candidates,
        held_mappings=held,
        ontology_status=ontology.registry_status,
        mapping_registry_status=mappings.registry_status,
        upstream_unknowns=upstream_unknowns,
        blockers=blockers,
    )

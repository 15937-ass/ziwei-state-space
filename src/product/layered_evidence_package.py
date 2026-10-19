"""Layered EvidencePackage vNext.

PL3-T serializes source-traceable CANONICAL and TEMPORAL evidence. PERSONAL
and EMPIRICAL remain empty until their owning product stages are implemented.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Mapping

from .evidence_package import EvidencePackage
from .natal_prior import NatalStateProfile
from .temporal_environment import TemporalEnvironmentProfile


CONCLUSION_STATUSES = frozenset(
    {"PARTIAL", "TRACEABLE", "NO_TEMPORAL_MATCH", "INSUFFICIENT_EVIDENCE"}
)


@dataclass(frozen=True)
class EvidenceReference:
    """Minimal source pointer for a rule that actually contributed to a run."""

    namespace: str
    rule_id: str
    source_id: str
    source_location: str
    review_status: str

    def __post_init__(self) -> None:
        if self.namespace not in {"CANONICAL", "TEMPORAL"}:
            raise ValueError(f"unsupported evidence reference namespace: {self.namespace}")
        for value, name in (
            (self.rule_id, "rule_id"),
            (self.source_id, "source_id"),
            (self.source_location, "source_location"),
            (self.review_status, "review_status"),
        ):
            if not str(value).strip():
                raise ValueError(f"EvidenceReference.{name} is required")


@dataclass(frozen=True)
class StructuredInferenceConclusion:
    """Machine-readable conclusion contract; it makes no unsupported outcome claim."""

    schema_version: str
    status: str
    question: str
    target_id: str
    selected_domains: tuple[str, ...]
    selected_temporal_layers: tuple[str, ...]
    canonical_rule_ids: tuple[str, ...]
    temporal_reaction_rule_ids: tuple[str, ...]
    evidence_refs: tuple[EvidenceReference, ...]
    conflicts: tuple[str, ...]
    unknowns: tuple[str, ...]
    limitations: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.schema_version != "0.1":
            raise ValueError("StructuredInferenceConclusion schema_version must be 0.1")
        if self.status not in CONCLUSION_STATUSES:
            raise ValueError(f"unsupported structured conclusion status: {self.status}")
        if not self.question.strip():
            raise ValueError("StructuredInferenceConclusion.question is required")
        if not self.target_id.strip():
            raise ValueError("StructuredInferenceConclusion.target_id is required")
        if not self.selected_domains:
            raise ValueError("StructuredInferenceConclusion.selected_domains is required")
        if not self.selected_temporal_layers:
            raise ValueError(
                "StructuredInferenceConclusion.selected_temporal_layers is required"
            )
        if len(set(self.canonical_rule_ids)) != len(self.canonical_rule_ids):
            raise ValueError("canonical_rule_ids must be unique")
        if len(set(self.temporal_reaction_rule_ids)) != len(
            self.temporal_reaction_rule_ids
        ):
            raise ValueError("temporal_reaction_rule_ids must be unique")
        canonical_refs = {
            item.rule_id for item in self.evidence_refs if item.namespace == "CANONICAL"
        }
        temporal_refs = {
            item.rule_id for item in self.evidence_refs if item.namespace == "TEMPORAL"
        }
        if not canonical_refs.issubset(set(self.canonical_rule_ids)):
            raise ValueError("canonical evidence references must be listed in canonical_rule_ids")
        if not temporal_refs.issubset(set(self.temporal_reaction_rule_ids)):
            raise ValueError(
                "temporal evidence references must be listed in temporal_reaction_rule_ids"
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "status": self.status,
            "question": self.question,
            "target_id": self.target_id,
            "selected_domains": list(self.selected_domains),
            "selected_temporal_layers": list(self.selected_temporal_layers),
            "canonical_rule_ids": list(self.canonical_rule_ids),
            "temporal_reaction_rule_ids": list(self.temporal_reaction_rule_ids),
            "evidence_refs": [asdict(item) for item in self.evidence_refs],
            "conflicts": list(self.conflicts),
            "unknowns": list(self.unknowns),
            "limitations": list(self.limitations),
        }


@dataclass(frozen=True)
class CanonicalEvidenceNamespace:
    natal_profile_id: str
    knowledge_version: str
    canonical_facts: tuple[str, ...]
    named_structure_facts: tuple[str, ...]
    domain_rule_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.natal_profile_id.strip():
            raise ValueError("canonical.natal_profile_id is required")
        if not self.knowledge_version.strip():
            raise ValueError("canonical.knowledge_version is required")


@dataclass(frozen=True)
class TemporalEvidenceNamespace:
    temporal_profile_id: str
    natal_profile_id: str
    knowledge_version: str
    target_label: str
    active_layers: tuple[str, ...]
    temporal_facts: tuple[Mapping[str, Any], ...]
    temporal_reactions: tuple[Mapping[str, Any], ...]
    event_relative_context: tuple[Mapping[str, Any], ...]
    conflicts: tuple[str, ...]
    external_event_trigger_used: bool

    def __post_init__(self) -> None:
        if not self.temporal_profile_id.strip():
            raise ValueError("temporal.temporal_profile_id is required")
        if not self.natal_profile_id.strip():
            raise ValueError("temporal.natal_profile_id is required")
        if not self.knowledge_version.strip():
            raise ValueError("temporal.knowledge_version is required")
        if not self.target_label.strip():
            raise ValueError("temporal.target_label is required")


@dataclass(frozen=True)
class LayeredEvidencePackage:
    schema_version: str
    question: str
    canonical: CanonicalEvidenceNamespace
    temporal: TemporalEvidenceNamespace
    personal: Mapping[str, Any] = field(default_factory=dict)
    empirical: Mapping[str, Any] = field(default_factory=dict)
    legacy_symbolic: Mapping[str, Any] = field(default_factory=dict)
    conclusion: StructuredInferenceConclusion | None = None

    def __post_init__(self) -> None:
        if self.schema_version != "0.1":
            raise ValueError("LayeredEvidencePackage schema_version must be 0.1")
        if not self.question.strip():
            raise ValueError("LayeredEvidencePackage.question is required")
        if self.canonical.natal_profile_id != self.temporal.natal_profile_id:
            raise ValueError(
                "canonical and temporal namespaces must reference the same natal profile"
            )
        if self.canonical.knowledge_version != self.temporal.knowledge_version:
            raise ValueError(
                "canonical and temporal namespaces must use the same knowledge version"
            )
        if self.personal:
            raise ValueError(
                "PL3-T EvidencePackage integration must not populate PERSONAL namespace"
            )
        if self.empirical:
            raise ValueError(
                "PL3-T EvidencePackage integration must not populate EMPIRICAL namespace"
            )
        if self.conclusion is not None and self.conclusion.question != self.question:
            raise ValueError(
                "structured conclusion question must match EvidencePackage.question"
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "question": self.question,
            "canonical": asdict(self.canonical),
            "temporal": asdict(self.temporal),
            "personal": dict(self.personal),
            "empirical": dict(self.empirical),
            "legacy_symbolic": dict(self.legacy_symbolic),
            "conclusion": self.conclusion.to_dict() if self.conclusion else None,
        }


def _domain_rule_ids(natal_profile: NatalStateProfile) -> tuple[str, ...]:
    return tuple(
        sorted(
            {
                rule.rule_id
                for domain in natal_profile.domains
                for rule in domain.active_rules
            }
        )
    )


def build_layered_evidence_package(
    *,
    question: str,
    natal_profile: NatalStateProfile,
    temporal_profile: TemporalEnvironmentProfile,
    legacy_symbolic_package: EvidencePackage | None = None,
    conclusion: StructuredInferenceConclusion | None = None,
) -> LayeredEvidencePackage:
    """Serialize computed evidence without selecting rules or creating probabilities."""

    if temporal_profile.natal_profile_id != natal_profile.profile_id:
        raise ValueError(
            "TemporalEnvironmentProfile does not belong to the supplied NatalStateProfile"
        )
    if temporal_profile.knowledge_version != natal_profile.knowledge_version:
        raise ValueError("temporal/natal knowledge_version mismatch")

    canonical = CanonicalEvidenceNamespace(
        natal_profile_id=natal_profile.profile_id,
        knowledge_version=natal_profile.knowledge_version,
        canonical_facts=tuple(natal_profile.canonical_facts),
        named_structure_facts=tuple(natal_profile.named_structure_facts),
        domain_rule_ids=_domain_rule_ids(natal_profile),
    )

    temporal = TemporalEvidenceNamespace(
        temporal_profile_id=temporal_profile.profile_id,
        natal_profile_id=temporal_profile.natal_profile_id,
        knowledge_version=temporal_profile.knowledge_version,
        target_label=temporal_profile.target_label,
        active_layers=tuple(temporal_profile.active_layers),
        temporal_facts=tuple(asdict(item) for item in temporal_profile.temporal_facts),
        temporal_reactions=tuple(asdict(item) for item in temporal_profile.reactions),
        event_relative_context=tuple(
            asdict(item) for item in temporal_profile.event_relative_context
        ),
        conflicts=tuple(temporal_profile.conflicts),
        external_event_trigger_used=temporal_profile.external_event_trigger_used,
    )

    legacy_payload: Mapping[str, Any] = {}
    if legacy_symbolic_package is not None:
        legacy_symbolic_package.validate()
        if (
            legacy_symbolic_package.knowledge_version
            and legacy_symbolic_package.knowledge_version
            != natal_profile.knowledge_version
        ):
            raise ValueError(
                "legacy EvidencePackage knowledge_version mismatches natal profile"
            )
        legacy_payload = legacy_symbolic_package.to_dict()

    return LayeredEvidencePackage(
        schema_version="0.1",
        question=str(question or "").strip(),
        canonical=canonical,
        temporal=temporal,
        legacy_symbolic=legacy_payload,
        conclusion=conclusion,
    )

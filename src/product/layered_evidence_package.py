"""Layered EvidencePackage vNext.

This module adds explicit CANONICAL / TEMPORAL / PERSONAL / EMPIRICAL
namespaces without breaking the legacy EvidencePackage contract.  PL3-T only
populates CANONICAL + TEMPORAL.  PERSONAL and EMPIRICAL remain empty until
their owning product stages are implemented.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Mapping

from .evidence_package import EvidencePackage
from .natal_prior import NatalStateProfile
from .temporal_environment import TemporalEnvironmentProfile


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

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "question": self.question,
            "canonical": asdict(self.canonical),
            "temporal": asdict(self.temporal),
            "personal": dict(self.personal),
            "empirical": dict(self.empirical),
            "legacy_symbolic": dict(self.legacy_symbolic),
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
) -> LayeredEvidencePackage:
    """Build the PL3-T layered evidence package.

    The function serializes already-computed objects only.  It does not select
    rules, infer new temporal semantics, or create probabilities.
    """

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
    )

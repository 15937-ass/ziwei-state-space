"""PL3-N deterministic Natal Prior profile.

The natal layer consumes only chart facts plus canonical/source-reviewed
knowledge. It has no API for user feedback, empirical probabilities, acquired
state, actions, or target-period outcomes.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any, Iterable, Mapping

from .evidence_package import EvidencePackage
from .human_gate_contracts import (
    BaiguanSupportProfile,
    ContextualValence,
    PatternAssessment,
    find_baiguan_support_profiles,
)
from .palace_structure import PalaceOntology, resolve_palace_structure
from .structure_primitives import source_backed_structure_facts


@dataclass(frozen=True)
class NatalRuleEvidence:
    rule_id: str
    claim: str
    source_id: str
    source_location: str
    epistemic: str
    review_status: str


@dataclass(frozen=True)
class NatalDomainEvidence:
    domain_id: str
    active_rules: tuple[NatalRuleEvidence, ...]
    projection_payloads: tuple[str, ...]
    latent_state_payload: str
    conflict_payloads: tuple[str, ...]
    confidence_band: str
    confidence_rationale: str
    knowledge_version: str

    def __post_init__(self) -> None:
        if not self.domain_id.strip():
            raise ValueError("domain_id is required")

    @classmethod
    def from_evidence_package(
        cls,
        domain_id: str,
        package: EvidencePackage,
    ) -> "NatalDomainEvidence":
        """Freeze one NATAL EvidencePackage into a feedback-free domain record."""

        package.validate()
        time_layer = str(package.chart_facts.get("time_layer", "")).strip()
        if time_layer and time_layer != "NATAL":
            raise ValueError(
                f"NatalDomainEvidence accepts NATAL packages only, got {time_layer}"
            )
        if package.history_state:
            raise ValueError(
                "NatalDomainEvidence cannot consume history/acquired-state feedback"
            )

        active_rules = tuple(
            sorted(
                (
                    NatalRuleEvidence(
                        rule_id=item.rule_id,
                        claim=item.claim,
                        source_id=item.source_id,
                        source_location=item.source_location,
                        epistemic=item.epistemic,
                        review_status=item.review_status,
                    )
                    for item in package.active_rules
                ),
                key=lambda item: item.rule_id,
            )
        )

        projections = tuple(
            sorted(
                json.dumps(
                    value,
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                )
                for value in package.projections
            )
        )
        conflicts = tuple(
            sorted(
                json.dumps(
                    asdict(value),
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                )
                for value in package.conflicts
            )
        )
        latent = json.dumps(
            package.latent_states,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )

        return cls(
            domain_id=domain_id,
            active_rules=active_rules,
            projection_payloads=projections,
            latent_state_payload=latent,
            conflict_payloads=conflicts,
            confidence_band=package.confidence_band.value,
            confidence_rationale=package.confidence_rationale,
            knowledge_version=package.knowledge_version,
        )


@dataclass(frozen=True)
class NatalStateProfile:
    schema_version: str
    profile_id: str
    engine_version: str
    knowledge_version: str
    canonical_facts: tuple[str, ...]
    named_structure_facts: tuple[str, ...]
    baiguan_profiles: tuple[BaiguanSupportProfile, ...]
    pattern_assessments: tuple[PatternAssessment, ...]
    contextual_valences: tuple[ContextualValence, ...]
    domains: tuple[NatalDomainEvidence, ...]
    feedback_used: bool = False
    empirical_calibration_used: bool = False

    def __post_init__(self) -> None:
        if self.schema_version != "0.1":
            raise ValueError("NatalStateProfile schema_version must be 0.1")
        if not self.profile_id.strip():
            raise ValueError("NatalStateProfile.profile_id is required")
        if not self.knowledge_version.strip():
            raise ValueError("NatalStateProfile.knowledge_version is required")
        if self.feedback_used:
            raise ValueError("PL3-N NatalStateProfile must be feedback-free")
        if self.empirical_calibration_used:
            raise ValueError("PL3-N NatalStateProfile cannot use empirical calibration")

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "profile_id": self.profile_id,
            "engine_version": self.engine_version,
            "knowledge_version": self.knowledge_version,
            "canonical_facts": list(self.canonical_facts),
            "named_structure_facts": list(self.named_structure_facts),
            "baiguan_profiles": [asdict(item) for item in self.baiguan_profiles],
            "pattern_assessments": [asdict(item) for item in self.pattern_assessments],
            "contextual_valences": [asdict(item) for item in self.contextual_valences],
            "domains": [
                {
                    "domain_id": item.domain_id,
                    "active_rules": [asdict(rule) for rule in item.active_rules],
                    "projection_payloads": list(item.projection_payloads),
                    "latent_state_payload": item.latent_state_payload,
                    "conflict_payloads": list(item.conflict_payloads),
                    "confidence_band": item.confidence_band,
                    "confidence_rationale": item.confidence_rationale,
                    "knowledge_version": item.knowledge_version,
                }
                for item in self.domains
            ],
            "feedback_used": self.feedback_used,
            "empirical_calibration_used": self.empirical_calibration_used,
        }


def _engine_version(snapshot: Mapping[str, Any]) -> str:
    engine = snapshot.get("engine", {})
    if not isinstance(engine, Mapping):
        return ""
    values = (
        str(engine.get("name", "")).strip(),
        str(engine.get("version", "")).strip(),
        str(engine.get("adapter_version", "")).strip(),
    )
    return ":".join(value for value in values if value)


def _profile_id(
    *,
    engine_version: str,
    knowledge_version: str,
    canonical_facts: Iterable[str],
    named_structure_facts: Iterable[str],
    domains: Iterable[NatalDomainEvidence],
) -> str:
    payload = {
        "engine_version": engine_version,
        "knowledge_version": knowledge_version,
        "canonical_facts": sorted(canonical_facts),
        "named_structure_facts": sorted(named_structure_facts),
        "domains": [
            {
                "domain_id": domain.domain_id,
                "active_rule_ids": [rule.rule_id for rule in domain.active_rules],
                "projection_payloads": list(domain.projection_payloads),
                "latent_state_payload": domain.latent_state_payload,
                "conflict_payloads": list(domain.conflict_payloads),
                "confidence_band": domain.confidence_band,
                "knowledge_version": domain.knowledge_version,
            }
            for domain in sorted(domains, key=lambda item: item.domain_id)
        ],
    }
    raw = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return "NATAL-" + hashlib.sha256(raw).hexdigest()[:24]


def build_natal_state_profile(
    snapshot: Mapping[str, Any],
    palace_ontology: PalaceOntology,
    *,
    knowledge_version: str,
    domain_evidence: Iterable[NatalDomainEvidence] = (),
    pattern_assessments: Iterable[PatternAssessment] = (),
    contextual_valences: Iterable[ContextualValence] = (),
) -> NatalStateProfile:
    """Build one deterministic, feedback-free natal profile.

    Pattern assessments and contextual valences are accepted only as already
    source-backed PL2-Q products. This function does not infer them.
    """

    if not knowledge_version.strip():
        raise ValueError("knowledge_version is required")

    structure = resolve_palace_structure(snapshot, palace_ontology)
    canonical_facts = tuple(sorted(structure.runtime_facts()))
    named_structure_facts = tuple(sorted(source_backed_structure_facts(structure)))
    baiguan_profiles = tuple(
        sorted(
            find_baiguan_support_profiles(structure),
            key=lambda item: item.anchor_palace_id,
        )
    )
    domains = tuple(sorted(domain_evidence, key=lambda item: item.domain_id))
    patterns = tuple(sorted(pattern_assessments, key=lambda item: item.pattern_id))
    valences = tuple(
        sorted(
            contextual_valences,
            key=lambda item: (item.palace_id, item.domain, item.target),
        )
    )

    engine_version = _engine_version(snapshot)
    profile_id = _profile_id(
        engine_version=engine_version,
        knowledge_version=knowledge_version,
        canonical_facts=canonical_facts,
        named_structure_facts=named_structure_facts,
        domains=domains,
    )

    return NatalStateProfile(
        schema_version="0.1",
        profile_id=profile_id,
        engine_version=engine_version,
        knowledge_version=knowledge_version,
        canonical_facts=canonical_facts,
        named_structure_facts=named_structure_facts,
        baiguan_profiles=baiguan_profiles,
        pattern_assessments=patterns,
        contextual_valences=valences,
        domains=domains,
    )

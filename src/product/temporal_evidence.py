"""PL3-T bridge from TemporalEnvironmentProfile to EvidencePackage TEMPORAL namespace.

This adapter serializes already-computed temporal environment evidence. It does
not select rules, infer events, compute probabilities, or create personal state.
"""

from __future__ import annotations

from dataclasses import asdict, replace

from .evidence_package import EvidencePackage, TemporalEvidenceNamespace
from .temporal_environment import TemporalEnvironmentProfile


def temporal_profile_to_evidence_namespace(
    profile: TemporalEnvironmentProfile,
) -> TemporalEvidenceNamespace:
    """Serialize one PL3-T profile into the typed TEMPORAL namespace."""

    namespace = TemporalEvidenceNamespace(
        profile_id=profile.profile_id,
        natal_profile_id=profile.natal_profile_id,
        target_label=profile.target_label,
        active_layers=tuple(profile.active_layers),
        temporal_facts=tuple(asdict(item) for item in profile.temporal_facts),
        temporal_reactions=tuple(asdict(item) for item in profile.reactions),
        environment_states=tuple(
            sorted(
                {
                    *(f"layer:{layer}:active" for layer in profile.active_layers),
                    *(
                        f"event_relative:{item.context_id}:{item.status}"
                        for item in profile.event_relative_context
                    ),
                }
            )
        ),
        event_relative_context=tuple(
            asdict(item) for item in profile.event_relative_context
        ),
        conflicts=tuple(profile.conflicts),
        external_event_trigger_used=profile.external_event_trigger_used,
    )
    namespace.validate()
    return namespace


def attach_temporal_profile_to_evidence_package(
    package: EvidencePackage,
    profile: TemporalEnvironmentProfile,
) -> EvidencePackage:
    """Return a copy of EvidencePackage with a TEMPORAL namespace attached.

    The canonical/top-level package payload is preserved. If the package already
    declares a knowledge version, it must match the PL3-T profile.
    """

    package_version = str(package.knowledge_version or "").strip()
    if package_version and package_version != profile.knowledge_version:
        raise ValueError(
            "EvidencePackage knowledge_version must match TemporalEnvironmentProfile"
        )

    namespace = temporal_profile_to_evidence_namespace(profile)
    updated = replace(
        package,
        temporal=namespace,
        knowledge_version=package_version or profile.knowledge_version,
    )
    updated.validate()
    return updated

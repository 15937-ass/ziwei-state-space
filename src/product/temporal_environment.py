"""PL3-T deterministic Temporal Environment profile core.

This layer combines already-normalized temporal chart facts with source-backed
reaction evidence. It represents time-varying astrological context only; it has
no API for user feedback, acquired state, empirical probabilities, or outcomes.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any, Iterable

from .natal_prior import NatalStateProfile


TEMPORAL_LAYERS = frozenset(
    {"DECADE", "SMALL_LIMIT", "YEAR", "MONTH", "DAY", "HOUR"}
)

REACTION_EFFECTS = frozenset(
    {"ACTIVATE", "STRENGTHEN", "WEAKEN", "TRANSFORM", "ROUTE", "PRESERVE"}
)

MAGNITUDE_STATUSES = frozenset({"UNIDENTIFIED", "SOURCE_ORDINAL_ONLY"})


@dataclass(frozen=True)
class TemporalFact:
    layer: str
    fact: str
    provenance: str

    def __post_init__(self) -> None:
        if self.layer not in TEMPORAL_LAYERS:
            raise ValueError(f"unsupported temporal layer: {self.layer}")
        if not self.fact.strip():
            raise ValueError("TemporalFact.fact is required")
        if not self.provenance.strip():
            raise ValueError("TemporalFact.provenance is required")


@dataclass(frozen=True)
class TemporalReactionEvidence:
    reaction_id: str
    rule_id: str
    layer: str
    domain: str
    target: str
    effect: str
    source_id: str
    source_location: str
    review_status: str
    magnitude_status: str = "UNIDENTIFIED"
    matched_natal_facts: tuple[str, ...] = ()
    matched_temporal_facts: tuple[str, ...] = ()
    matched_natal_rule_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for value, name in (
            (self.reaction_id, "reaction_id"),
            (self.rule_id, "rule_id"),
            (self.domain, "domain"),
            (self.target, "target"),
            (self.source_id, "source_id"),
            (self.source_location, "source_location"),
            (self.review_status, "review_status"),
        ):
            if not str(value).strip():
                raise ValueError(f"TemporalReactionEvidence.{name} is required")
        if self.layer not in TEMPORAL_LAYERS:
            raise ValueError(f"unsupported temporal layer: {self.layer}")
        if self.effect not in REACTION_EFFECTS:
            raise ValueError(f"unsupported temporal reaction effect: {self.effect}")
        if self.magnitude_status not in MAGNITUDE_STATUSES:
            raise ValueError(
                f"unsupported magnitude_status: {self.magnitude_status}"
            )


@dataclass(frozen=True)
class EventRelativeContextEvidence:
    context_id: str
    status: str
    source_id: str
    source_location: str
    review_status: str
    trigger_provenance: str = ""
    routing_facts: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for value, name in (
            (self.context_id, "context_id"),
            (self.status, "status"),
            (self.source_id, "source_id"),
            (self.source_location, "source_location"),
            (self.review_status, "review_status"),
        ):
            if not str(value).strip():
                raise ValueError(
                    f"EventRelativeContextEvidence.{name} is required"
                )


@dataclass(frozen=True)
class TemporalEnvironmentProfile:
    schema_version: str
    profile_id: str
    natal_profile_id: str
    knowledge_version: str
    target_label: str
    active_layers: tuple[str, ...]
    temporal_facts: tuple[TemporalFact, ...]
    reactions: tuple[TemporalReactionEvidence, ...]
    conflicts: tuple[str, ...]
    event_relative_context: tuple[EventRelativeContextEvidence, ...]
    feedback_used: bool = False
    acquired_state_used: bool = False
    outcome_used: bool = False
    empirical_calibration_used: bool = False
    external_event_trigger_used: bool = False

    def __post_init__(self) -> None:
        if self.schema_version != "0.1":
            raise ValueError("TemporalEnvironmentProfile schema_version must be 0.1")
        if not self.profile_id.strip():
            raise ValueError("TemporalEnvironmentProfile.profile_id is required")
        if not self.natal_profile_id.strip():
            raise ValueError("TemporalEnvironmentProfile.natal_profile_id is required")
        if not self.knowledge_version.strip():
            raise ValueError("TemporalEnvironmentProfile.knowledge_version is required")
        if not self.target_label.strip():
            raise ValueError("TemporalEnvironmentProfile.target_label is required")

        forbidden = {
            "feedback_used": self.feedback_used,
            "acquired_state_used": self.acquired_state_used,
            "outcome_used": self.outcome_used,
            "empirical_calibration_used": self.empirical_calibration_used,
        }
        active = [name for name, value in forbidden.items() if value]
        if active:
            raise ValueError(
                "PL3-T TemporalEnvironmentProfile must be environment-only; "
                f"forbidden flags: {', '.join(active)}"
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "profile_id": self.profile_id,
            "natal_profile_id": self.natal_profile_id,
            "knowledge_version": self.knowledge_version,
            "target_label": self.target_label,
            "active_layers": list(self.active_layers),
            "temporal_facts": [asdict(item) for item in self.temporal_facts],
            "reactions": [asdict(item) for item in self.reactions],
            "conflicts": list(self.conflicts),
            "event_relative_context": [
                asdict(item) for item in self.event_relative_context
            ],
            "feedback_used": self.feedback_used,
            "acquired_state_used": self.acquired_state_used,
            "outcome_used": self.outcome_used,
            "empirical_calibration_used": self.empirical_calibration_used,
            "external_event_trigger_used": self.external_event_trigger_used,
        }


def _profile_id(
    *,
    natal_profile_id: str,
    knowledge_version: str,
    target_label: str,
    temporal_facts: Iterable[TemporalFact],
    reactions: Iterable[TemporalReactionEvidence],
    conflicts: Iterable[str],
    event_relative_context: Iterable[EventRelativeContextEvidence],
) -> str:
    payload = {
        "natal_profile_id": natal_profile_id,
        "knowledge_version": knowledge_version,
        "target_label": target_label,
        "temporal_facts": [
            asdict(item)
            for item in sorted(
                temporal_facts,
                key=lambda value: (value.layer, value.fact, value.provenance),
            )
        ],
        "reactions": [
            asdict(item)
            for item in sorted(
                reactions,
                key=lambda value: (
                    value.layer,
                    value.domain,
                    value.target,
                    value.reaction_id,
                ),
            )
        ],
        "conflicts": sorted(str(item) for item in conflicts),
        "event_relative_context": [
            asdict(item)
            for item in sorted(
                event_relative_context,
                key=lambda value: value.context_id,
            )
        ],
    }
    raw = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return "TEMP-" + hashlib.sha256(raw).hexdigest()[:24]


def build_temporal_environment_profile(
    natal_profile: NatalStateProfile,
    *,
    target_label: str,
    temporal_facts: Iterable[TemporalFact],
    reactions: Iterable[TemporalReactionEvidence] = (),
    conflicts: Iterable[str] = (),
    event_relative_context: Iterable[EventRelativeContextEvidence] = (),
    knowledge_version: str | None = None,
) -> TemporalEnvironmentProfile:
    """Build one deterministic environment-only temporal profile.

    This function preserves already-reviewed temporal facts and reaction
    evidence. It does not infer new rules, probabilities or real-world events.
    """

    target = str(target_label or "").strip()
    if not target:
        raise ValueError("target_label is required")

    version = str(knowledge_version or natal_profile.knowledge_version).strip()
    if version != natal_profile.knowledge_version:
        raise ValueError(
            "PL3-T knowledge_version must match the NatalStateProfile version"
        )

    facts = tuple(
        sorted(
            temporal_facts,
            key=lambda value: (value.layer, value.fact, value.provenance),
        )
    )
    reaction_items = tuple(
        sorted(
            reactions,
            key=lambda value: (
                value.layer,
                value.domain,
                value.target,
                value.reaction_id,
            ),
        )
    )
    conflict_items = tuple(sorted(str(item).strip() for item in conflicts if str(item).strip()))
    relative_items = tuple(
        sorted(event_relative_context, key=lambda value: value.context_id)
    )
    active_layers = tuple(sorted({item.layer for item in facts} | {item.layer for item in reaction_items}))

    profile_id = _profile_id(
        natal_profile_id=natal_profile.profile_id,
        knowledge_version=version,
        target_label=target,
        temporal_facts=facts,
        reactions=reaction_items,
        conflicts=conflict_items,
        event_relative_context=relative_items,
    )

    return TemporalEnvironmentProfile(
        schema_version="0.1",
        profile_id=profile_id,
        natal_profile_id=natal_profile.profile_id,
        knowledge_version=version,
        target_label=target,
        active_layers=active_layers,
        temporal_facts=facts,
        reactions=reaction_items,
        conflicts=conflict_items,
        event_relative_context=relative_items,
        external_event_trigger_used=any(
            item.status == "ACTIVE" for item in relative_items
        ),
    )

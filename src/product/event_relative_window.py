"""PL3-T product adapter for the single approved event-relative window.

This module deliberately does not implement a generic event timer. It consumes
only the frozen HG-P07-TEMPORAL-01-A knowledge artifact and delegates the actual
window semantics to the source-bounded WP05 migration resolver.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from src.wp05_event_relative_time import (
    EVENT_TYPE,
    WINDOW_ID,
    MigrationEventRelativeContext,
    MigrationTemporalResolution,
    resolve_migration_event_window,
)

from .natal_prior import NatalStateProfile
from .temporal_environment import (
    EventRelativeContextEvidence,
    TemporalFact,
    TemporalReactionEvidence,
    TemporalEnvironmentProfile,
    build_temporal_environment_profile,
)


DEFAULT_WINDOW_REGISTRY_PATH = (
    Path(__file__).resolve().parents[2]
    / "knowledge"
    / "temporal"
    / "event_relative_windows_v0.1.csv"
)

APPROVED_HUMAN_GATE = "HG-P07-TEMPORAL-01-A"
APPROVED_REVIEW_STATUS = "HUMAN_VERIFIED"
APPROVED_COUNTER = "years_since_distant_relocation"
APPROVED_MIN_INDEX = 1
APPROVED_MAX_INDEX = 3
APPROVED_TRIGGER = "confirmed_distant_settlement_and_not_travel_only"
APPROVED_ACTIVE_CONTEXT = "migration_palace_primary"
APPROVED_PRESERVED_CONTEXTS = (
    "annual_life_palace_rotation_and_other_palace_rotation"
)


@dataclass(frozen=True)
class ApprovedMigrationWindowSpec:
    window_id: str
    event_type: str
    counter_name: str
    min_index: int
    max_index: int
    trigger_requirement: str
    active_projection_context: str
    preserved_contexts: str
    source_id: str
    source_location: str
    review_status: str
    human_gate: str


@dataclass(frozen=True)
class ProductMigrationWindowResolution:
    spec: ApprovedMigrationWindowSpec
    source_resolution: MigrationTemporalResolution
    context_evidence: EventRelativeContextEvidence
    routing_facts: tuple[str, ...]

    @property
    def active(self) -> bool:
        return self.source_resolution.active


def _required_text(row: dict[str, str], key: str) -> str:
    value = str(row.get(key) or "").strip()
    if not value:
        raise ValueError(f"event-relative registry field {key} is required")
    return value


def _required_int(row: dict[str, str], key: str) -> int:
    value = _required_text(row, key)
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(f"event-relative registry field {key} must be an int") from exc


def load_approved_migration_window_spec(
    path: Path | str = DEFAULT_WINDOW_REGISTRY_PATH,
) -> ApprovedMigrationWindowSpec:
    """Load and strictly validate the one Human-Gate-approved window."""

    registry_path = Path(path)
    rows = list(csv.DictReader(registry_path.open("r", encoding="utf-8-sig", newline="")))
    if len(rows) != 1:
        raise ValueError(
            "PL3-T v0.1 permits exactly one approved event-relative window"
        )

    row = rows[0]
    spec = ApprovedMigrationWindowSpec(
        window_id=_required_text(row, "window_id"),
        event_type=_required_text(row, "event_type"),
        counter_name=_required_text(row, "counter_name"),
        min_index=_required_int(row, "min_index"),
        max_index=_required_int(row, "max_index"),
        trigger_requirement=_required_text(row, "trigger_requirement"),
        active_projection_context=_required_text(row, "active_projection_context"),
        preserved_contexts=_required_text(row, "preserved_contexts"),
        source_id=_required_text(row, "source_id"),
        source_location=_required_text(row, "source_location"),
        review_status=_required_text(row, "review_status"),
        human_gate=_required_text(row, "human_gate"),
    )

    expected = {
        "window_id": WINDOW_ID,
        "event_type": EVENT_TYPE,
        "counter_name": APPROVED_COUNTER,
        "min_index": APPROVED_MIN_INDEX,
        "max_index": APPROVED_MAX_INDEX,
        "trigger_requirement": APPROVED_TRIGGER,
        "active_projection_context": APPROVED_ACTIVE_CONTEXT,
        "preserved_contexts": APPROVED_PRESERVED_CONTEXTS,
        "review_status": APPROVED_REVIEW_STATUS,
        "human_gate": APPROVED_HUMAN_GATE,
    }
    for key, expected_value in expected.items():
        if getattr(spec, key) != expected_value:
            raise ValueError(
                f"event-relative registry drift for {key}: "
                f"{getattr(spec, key)!r} != {expected_value!r}"
            )

    return spec


def _status_for(
    context: MigrationEventRelativeContext,
    source_resolution: MigrationTemporalResolution,
) -> str:
    if source_resolution.active:
        return "ACTIVE"
    if context.travel_only:
        return "INACTIVE_TRAVEL_ONLY"
    if not context.confirmed_distant_settlement:
        return "INACTIVE_EVENT_UNCONFIRMED"
    return "INACTIVE_OUTSIDE_APPROVED_WINDOW"


def resolve_approved_migration_window(
    context: MigrationEventRelativeContext,
    *,
    registry_path: Path | str = DEFAULT_WINDOW_REGISTRY_PATH,
) -> ProductMigrationWindowResolution:
    """Resolve the approved migration window without generalizing it."""

    spec = load_approved_migration_window_spec(registry_path)
    source_resolution = resolve_migration_event_window(context)

    evidence = EventRelativeContextEvidence(
        context_id=spec.window_id,
        status=_status_for(context, source_resolution),
        source_id=spec.source_id,
        source_location=spec.source_location,
        review_status=spec.review_status,
    )

    return ProductMigrationWindowResolution(
        spec=spec,
        source_resolution=source_resolution,
        context_evidence=evidence,
        routing_facts=source_resolution.facts,
    )


def build_temporal_environment_with_migration_window(
    natal_profile: NatalStateProfile,
    *,
    target_label: str,
    temporal_facts: Iterable[TemporalFact],
    migration_context: MigrationEventRelativeContext,
    reactions: Iterable[TemporalReactionEvidence] = (),
    conflicts: Iterable[str] = (),
    knowledge_version: str | None = None,
    registry_path: Path | str = DEFAULT_WINDOW_REGISTRY_PATH,
) -> TemporalEnvironmentProfile:
    """Attach the one approved event-relative evidence item to PL3-T.

    The relative counter must already be supplied by an upstream confirmed
    event/history layer. This helper does not derive relocation, elapsed years,
    or outcomes from chart facts.
    """

    resolved = resolve_approved_migration_window(
        migration_context,
        registry_path=registry_path,
    )
    return build_temporal_environment_profile(
        natal_profile,
        target_label=target_label,
        temporal_facts=temporal_facts,
        reactions=reactions,
        conflicts=conflicts,
        event_relative_context=(resolved.context_evidence,),
        knowledge_version=knowledge_version,
    )

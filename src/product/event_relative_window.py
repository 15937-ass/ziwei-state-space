"""Source-bounded PL3-T event-relative temporal overlay.

Only HG-P07-TEMPORAL-01-A / MIGRATION_FIRST_THREE_YEARS is implemented here.
This module is intentionally not a generic event timer.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .temporal_environment import EventRelativeContextEvidence


MIGRATION_WINDOW_ID = "MIGRATION_FIRST_THREE_YEARS"
MIGRATION_WINDOW_SOURCE_ID = "SRC-ZZ-003"
MIGRATION_WINDOW_SOURCE_LOCATION = "迁移宫 printed p109"
MIGRATION_WINDOW_REVIEW_STATUS = "HUMAN_VERIFIED"

EVENT_RELATIVE_STATUSES = frozenset({"ACTIVE", "INACTIVE", "INSUFFICIENT"})


@dataclass(frozen=True)
class MigrationFirstThreeYearsInput:
    confirmed_distant_settlement: bool
    years_since_distant_relocation: int | None
    travel_only: bool
    trigger_provenance: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.confirmed_distant_settlement, bool):
            raise ValueError("confirmed_distant_settlement must be bool")
        if not isinstance(self.travel_only, bool):
            raise ValueError("travel_only must be bool")

        value = self.years_since_distant_relocation
        if value is not None:
            if isinstance(value, bool) or not isinstance(value, int):
                raise ValueError("years_since_distant_relocation must be int or null")
            if value < 0:
                raise ValueError("years_since_distant_relocation cannot be negative")

        if self.confirmed_distant_settlement and not self.trigger_provenance.strip():
            raise ValueError(
                "confirmed distant settlement requires explicit trigger_provenance"
            )


@dataclass(frozen=True)
class EventRelativeWindowResolution:
    window_id: str
    status: str
    reason: str
    evidence: EventRelativeContextEvidence

    def __post_init__(self) -> None:
        if self.status not in EVENT_RELATIVE_STATUSES:
            raise ValueError(f"unsupported event-relative status: {self.status}")


def _evidence(
    *,
    status: str,
    trigger_provenance: str,
    routing_facts: tuple[str, ...],
) -> EventRelativeContextEvidence:
    return EventRelativeContextEvidence(
        context_id=MIGRATION_WINDOW_ID,
        status=status,
        source_id=MIGRATION_WINDOW_SOURCE_ID,
        source_location=MIGRATION_WINDOW_SOURCE_LOCATION,
        review_status=MIGRATION_WINDOW_REVIEW_STATUS,
        trigger_provenance=trigger_provenance,
        routing_facts=tuple(sorted(routing_facts)),
    )


def resolve_migration_first_three_years(
    value: MigrationFirstThreeYearsInput,
) -> EventRelativeWindowResolution:
    """Resolve exactly the approved first-three-years relocation overlay."""

    if not value.confirmed_distant_settlement:
        evidence = _evidence(
            status="INACTIVE",
            trigger_provenance=value.trigger_provenance,
            routing_facts=(),
        )
        return EventRelativeWindowResolution(
            window_id=MIGRATION_WINDOW_ID,
            status="INACTIVE",
            reason="NO_CONFIRMED_DISTANT_SETTLEMENT",
            evidence=evidence,
        )

    if value.travel_only:
        evidence = _evidence(
            status="INACTIVE",
            trigger_provenance=value.trigger_provenance,
            routing_facts=(
                "event:distant_relocation_settlement:confirmed",
                "gate:migration_first_three_years:inactive_travel_only",
            ),
        )
        return EventRelativeWindowResolution(
            window_id=MIGRATION_WINDOW_ID,
            status="INACTIVE",
            reason="TRAVEL_ONLY_EXCLUDED",
            evidence=evidence,
        )

    years = value.years_since_distant_relocation
    if years is None:
        evidence = _evidence(
            status="INSUFFICIENT",
            trigger_provenance=value.trigger_provenance,
            routing_facts=(
                "event:distant_relocation_settlement:confirmed",
            ),
        )
        return EventRelativeWindowResolution(
            window_id=MIGRATION_WINDOW_ID,
            status="INSUFFICIENT",
            reason="YEARS_SINCE_RELOCATION_REQUIRED",
            evidence=evidence,
        )

    if 1 <= years <= 3:
        evidence = _evidence(
            status="ACTIVE",
            trigger_provenance=value.trigger_provenance,
            routing_facts=(
                "event:distant_relocation_settlement:confirmed",
                f"event_relative:distant_relocation_year:{years}",
                "gate:migration_first_three_years:active",
                "projection_priority:migration_palace:primary",
                "rotation:annual_life_palace:preserved",
                "rotation:other_palace:preserved",
            ),
        )
        return EventRelativeWindowResolution(
            window_id=MIGRATION_WINDOW_ID,
            status="ACTIVE",
            reason="SOURCE_EXPLICIT_YEAR_1_TO_3_WINDOW",
            evidence=evidence,
        )

    evidence = _evidence(
        status="INACTIVE",
        trigger_provenance=value.trigger_provenance,
        routing_facts=(
            "event:distant_relocation_settlement:confirmed",
            f"event_relative:distant_relocation_year:{years}",
            "gate:migration_first_three_years:inactive_outside_window",
        ),
    )
    return EventRelativeWindowResolution(
        window_id=MIGRATION_WINDOW_ID,
        status="INACTIVE",
        reason="OUTSIDE_SOURCE_EXPLICIT_YEAR_1_TO_3_WINDOW",
        evidence=evidence,
    )

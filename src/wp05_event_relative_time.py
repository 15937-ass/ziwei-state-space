"""Source-bounded event-relative temporal resolver for WP05 Migration Palace.

HG-P07-TEMPORAL-01 Option A authorizes one finite event-relative clock only:
the first three years after a confirmed distant relocation/settlement.

This module intentionally does not provide a generic event-timer abstraction.
"""

from __future__ import annotations

from dataclasses import dataclass


WINDOW_ID = "MIGRATION_FIRST_THREE_YEARS"
EVENT_TYPE = "DISTANT_RELOCATION_SETTLEMENT"


@dataclass(frozen=True)
class MigrationEventRelativeContext:
    """Minimal input for the approved relocation-relative window.

    `years_since_distant_relocation` is supplied by an upstream event/history
    layer. This resolver does not infer it from dates or chart facts.
    """

    confirmed_distant_settlement: bool
    years_since_distant_relocation: int | None = None
    travel_only: bool = False

    def __post_init__(self) -> None:
        if self.confirmed_distant_settlement and self.travel_only:
            raise ValueError("distant settlement and travel_only cannot both be true")
        if self.years_since_distant_relocation is not None:
            value = self.years_since_distant_relocation
            if isinstance(value, bool) or not isinstance(value, int):
                raise TypeError("years_since_distant_relocation must be an int or None")
            if value < 0:
                raise ValueError("years_since_distant_relocation cannot be negative")
        if self.confirmed_distant_settlement and self.years_since_distant_relocation is None:
            raise ValueError(
                "confirmed distant settlement requires years_since_distant_relocation"
            )


@dataclass(frozen=True)
class MigrationTemporalResolution:
    window_id: str
    active: bool
    migration_palace_priority: str
    annual_life_palace_rotation: str
    other_palace_rotation: str
    years_since_distant_relocation: int | None
    facts: tuple[str, ...]


def resolve_migration_event_window(
    context: MigrationEventRelativeContext,
) -> MigrationTemporalResolution:
    """Resolve the exact source-bounded first-three-years migration window."""

    years = context.years_since_distant_relocation
    active = bool(
        context.confirmed_distant_settlement
        and not context.travel_only
        and years is not None
        and 1 <= years <= 3
    )

    facts: list[str] = []
    if context.confirmed_distant_settlement:
        facts.append("event:distant_relocation_settlement:confirmed")
        if years is not None:
            facts.append(f"event_relative:distant_relocation_year:{years}")
    if active:
        facts.extend(
            [
                "gate:migration_first_three_years:active",
                "projection_priority:migration_palace:primary",
                "rotation:annual_life_palace:preserved",
            ]
        )

    return MigrationTemporalResolution(
        window_id=WINDOW_ID,
        active=active,
        migration_palace_priority="PRIMARY" if active else "BASELINE",
        annual_life_palace_rotation="PRESERVED",
        other_palace_rotation="PRESERVED",
        years_since_distant_relocation=years,
        facts=tuple(facts),
    )


def migration_runtime_facts(
    context: MigrationEventRelativeContext,
) -> frozenset[str]:
    """Adapter for deterministic rule runtimes that consume fact atoms."""

    return frozenset(resolve_migration_event_window(context).facts)

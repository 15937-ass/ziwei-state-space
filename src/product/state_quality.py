"""PL3-S missingness / contradiction audit model v0.1.

This module audits AcquiredStateProfile quality without imputing missing values,
resolving conflicts, or converting ordinal confidence into probabilities.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Iterable

from .acquired_state import AcquiredStateProfile


SLOT_STATUSES = frozenset({"OBSERVED", "MISSING", "CONFLICTED"})
BELIEF_INPUT_DISPOSITIONS = frozenset(
    {"READY_OBSERVED", "HOLD_MISSING", "HOLD_CONFLICT"}
)


@dataclass(frozen=True)
class StateSlotAudit:
    domain: str
    key: str
    status: str
    disposition: str
    fact_ids: tuple[str, ...] = ()
    values: tuple[Any, ...] = ()
    confidence_labels: tuple[str, ...] = ()
    missingness_reason: str | None = None
    conflict_ids: tuple[str, ...] = ()
    observation_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.status not in SLOT_STATUSES:
            raise ValueError(f"unsupported slot audit status: {self.status}")
        if self.disposition not in BELIEF_INPUT_DISPOSITIONS:
            raise ValueError(
                f"unsupported belief-input disposition: {self.disposition}"
            )


@dataclass(frozen=True)
class StateQualityReport:
    state_id: str
    person_key: str
    as_of_date: str
    slots: tuple[StateSlotAudit, ...]
    observed_count: int
    missing_count: int
    conflicted_count: int
    has_blockers: bool
    probability_calibration_used: bool = False
    imputation_used: bool = False
    conflict_resolution_used: bool = False

    def __post_init__(self) -> None:
        if not self.state_id.strip():
            raise ValueError("StateQualityReport.state_id is required")
        if self.probability_calibration_used:
            raise ValueError("PL3-S quality audit cannot use probability calibration")
        if self.imputation_used:
            raise ValueError("PL3-S quality audit cannot impute missing state")
        if self.conflict_resolution_used:
            raise ValueError("PL3-S quality audit cannot resolve conflicts")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def audit_acquired_state_quality(
    state: AcquiredStateProfile,
) -> StateQualityReport:
    """Audit each reality-state domain/key as observed, missing, or conflicted."""

    facts_by_slot: dict[tuple[str, str], list[Any]] = {}
    for fact in state.assertions:
        facts_by_slot.setdefault((fact.domain, fact.key), []).append(fact)

    missing_by_slot = {
        (item.domain, item.key): item for item in state.missingness
    }
    conflicts_by_slot: dict[tuple[str, str], list[Any]] = {}
    for conflict in state.conflicts:
        conflicts_by_slot.setdefault((conflict.domain, conflict.key), []).append(
            conflict
        )

    all_slots = set(facts_by_slot) | set(missing_by_slot) | set(conflicts_by_slot)
    rows: list[StateSlotAudit] = []

    for domain, key in sorted(all_slots):
        facts = sorted(
            facts_by_slot.get((domain, key), []), key=lambda item: item.fact_id
        )
        missing = missing_by_slot.get((domain, key))
        conflicts = sorted(
            conflicts_by_slot.get((domain, key), []),
            key=lambda item: item.conflict_id,
        )

        if facts and missing is not None:
            raise ValueError(
                f"inconsistent acquired state: {domain}:{key} is both observed and missing"
            )

        fact_ids = tuple(item.fact_id for item in facts)
        values = tuple(item.value for item in facts)
        confidence = tuple(sorted({item.confidence for item in facts}))
        refs = tuple(
            sorted(
                {
                    ref
                    for item in facts
                    for ref in item.observation_refs
                }
            )
        )

        if conflicts:
            conflict_ids = tuple(item.conflict_id for item in conflicts)
            referenced = {
                fact_id
                for conflict in conflicts
                for fact_id in conflict.fact_ids
            }
            if not referenced.issubset(set(fact_ids)):
                raise ValueError(
                    f"{domain}:{key} conflict references facts outside its slot"
                )
            if len(set(values)) < 2:
                raise ValueError(
                    f"{domain}:{key} conflict does not contain distinct values"
                )
            rows.append(
                StateSlotAudit(
                    domain=domain,
                    key=key,
                    status="CONFLICTED",
                    disposition="HOLD_CONFLICT",
                    fact_ids=fact_ids,
                    values=values,
                    confidence_labels=confidence,
                    conflict_ids=conflict_ids,
                    observation_refs=refs,
                )
            )
            continue

        if missing is not None:
            rows.append(
                StateSlotAudit(
                    domain=domain,
                    key=key,
                    status="MISSING",
                    disposition="HOLD_MISSING",
                    missingness_reason=missing.reason,
                )
            )
            continue

        if len(set(values)) > 1:
            raise ValueError(
                f"{domain}:{key} has contradictory values without StateConflict"
            )

        rows.append(
            StateSlotAudit(
                domain=domain,
                key=key,
                status="OBSERVED",
                disposition="READY_OBSERVED",
                fact_ids=fact_ids,
                values=values,
                confidence_labels=confidence,
                observation_refs=refs,
            )
        )

    observed_count = sum(row.status == "OBSERVED" for row in rows)
    missing_count = sum(row.status == "MISSING" for row in rows)
    conflicted_count = sum(row.status == "CONFLICTED" for row in rows)

    return StateQualityReport(
        state_id=state.state_id,
        person_key=state.person_key,
        as_of_date=state.as_of_date.isoformat(),
        slots=tuple(rows),
        observed_count=observed_count,
        missing_count=missing_count,
        conflicted_count=conflicted_count,
        has_blockers=(missing_count + conflicted_count) > 0,
    )


def select_ready_observed_slots(
    report: StateQualityReport,
) -> tuple[StateSlotAudit, ...]:
    """Return only structurally observed slots; no confidence-to-weight mapping."""

    return tuple(
        row for row in report.slots if row.disposition == "READY_OBSERVED"
    )

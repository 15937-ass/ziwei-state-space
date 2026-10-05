"""PL7 longitudinal observation schema v0.2 with interval event time.

v0.2 preserves all v0.1 observation semantics while replacing exact-only
event_date with a bounded event_time representation.
"""

from __future__ import annotations

import calendar
import copy
from dataclasses import dataclass
from datetime import date
from typing import Any, Mapping

from .longitudinal_observation import (
    LongitudinalObservationRecord,
    compile_longitudinal_observation,
)


EVENT_TIME_PRECISIONS = frozenset({"DAY", "MONTH", "YEAR", "INTERVAL"})


def _iso_date(value: Any, field: str) -> date:
    text = str(value or "").strip()
    if not text:
        raise ValueError(f"{field} is required")
    try:
        return date.fromisoformat(text)
    except ValueError as exc:
        raise ValueError(f"{field} must be ISO YYYY-MM-DD") from exc


@dataclass(frozen=True)
class EventTimeInterval:
    precision: str
    lower_bound: date
    upper_bound: date

    def __post_init__(self) -> None:
        if self.precision not in EVENT_TIME_PRECISIONS:
            raise ValueError(f"unsupported event-time precision: {self.precision}")
        if self.upper_bound < self.lower_bound:
            raise ValueError("event-time upper bound cannot predate lower bound")

        if self.precision == "DAY":
            if self.lower_bound != self.upper_bound:
                raise ValueError("DAY precision requires equal lower/upper bounds")
        elif self.precision == "MONTH":
            if (
                self.lower_bound.year != self.upper_bound.year
                or self.lower_bound.month != self.upper_bound.month
                or self.lower_bound.day != 1
            ):
                raise ValueError("MONTH precision must cover one normalized calendar month")
            last_day = calendar.monthrange(
                self.lower_bound.year, self.lower_bound.month
            )[1]
            if self.upper_bound.day != last_day:
                raise ValueError("MONTH precision upper bound must be calendar month end")
        elif self.precision == "YEAR":
            if self.lower_bound != date(self.lower_bound.year, 1, 1):
                raise ValueError("YEAR precision lower bound must be Jan 1")
            if self.upper_bound != date(self.lower_bound.year, 12, 31):
                raise ValueError("YEAR precision upper bound must be Dec 31")

    def fully_within(self, start: date, end: date) -> bool:
        return start <= self.lower_bound <= self.upper_bound <= end

    def overlaps(self, start: date, end: date) -> bool:
        return not (self.upper_bound < start or self.lower_bound > end)


@dataclass(frozen=True)
class LongitudinalObservationRecordV02:
    base: LongitudinalObservationRecord
    event_time: EventTimeInterval | None

    @property
    def event_status(self) -> str:
        return self.base.event_status

    @property
    def calibration_usable(self) -> bool:
        return self.base.calibration_usable

    @property
    def blind_benchmark_eligible(self) -> bool:
        return self.base.blind_benchmark_eligible


def _compile_event_time(value: Any) -> EventTimeInterval | None:
    if value is None:
        return None
    if not isinstance(value, Mapping):
        raise ValueError("outcome.event_time must be an object or null")
    precision = str(value.get("precision") or "").strip()
    lower = _iso_date(value.get("lower_bound_date"), "outcome.event_time.lower_bound_date")
    upper = _iso_date(value.get("upper_bound_date"), "outcome.event_time.upper_bound_date")
    return EventTimeInterval(
        precision=precision,
        lower_bound=lower,
        upper_bound=upper,
    )


def compile_longitudinal_observation_v02(
    payload: Mapping[str, Any],
) -> LongitudinalObservationRecordV02:
    if str(payload.get("schema_version", "")).strip() != "0.2":
        raise ValueError("schema_version must be 0.2")

    outcome = payload.get("outcome")
    window = payload.get("window")
    if not isinstance(outcome, Mapping):
        raise ValueError("outcome must be an object")
    if not isinstance(window, Mapping):
        raise ValueError("window must be an object")

    status = str(outcome.get("status") or "").strip()
    event_time = _compile_event_time(outcome.get("event_time"))
    window_start = _iso_date(window.get("start_date"), "window.start_date")
    window_end = _iso_date(window.get("end_date"), "window.end_date")
    observed_through = _iso_date(
        window.get("observed_through"), "window.observed_through"
    )

    if status == "EVENT_OCCURRED":
        if event_time is None:
            raise ValueError("EVENT_OCCURRED requires outcome.event_time")
        if not event_time.fully_within(window_start, window_end):
            if event_time.overlaps(window_start, window_end):
                raise ValueError(
                    "TEMPORAL_ASSIGNMENT_AMBIGUOUS: event-time interval only "
                    "partially overlaps target window"
                )
            raise ValueError("event-time interval lies outside target window")
        if observed_through < event_time.upper_bound:
            raise ValueError(
                "observed_through cannot predate event-time upper bound"
            )
    else:
        if event_time is not None:
            raise ValueError(
                f"{status or 'non-event status'} requires outcome.event_time=null"
            )

    surrogate = copy.deepcopy(dict(payload))
    surrogate["schema_version"] = "0.1"
    surrogate_outcome = dict(surrogate["outcome"])
    surrogate_outcome.pop("event_time", None)
    surrogate_outcome["event_date"] = (
        event_time.lower_bound.isoformat() if event_time is not None else None
    )
    surrogate["outcome"] = surrogate_outcome

    base = compile_longitudinal_observation(surrogate)
    return LongitudinalObservationRecordV02(base=base, event_time=event_time)


def migrate_longitudinal_observation_v01_to_v02(
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    """Losslessly migrate a v0.1 exact-date payload to v0.2."""

    if str(payload.get("schema_version", "")).strip() != "0.1":
        raise ValueError("migration input schema_version must be 0.1")

    migrated = copy.deepcopy(dict(payload))
    outcome = dict(migrated.get("outcome") or {})
    event_date = outcome.pop("event_date", None)
    outcome["event_time"] = (
        {
            "precision": "DAY",
            "lower_bound_date": event_date,
            "upper_bound_date": event_date,
        }
        if event_date
        else None
    )
    migrated["outcome"] = outcome
    migrated["schema_version"] = "0.2"

    compile_longitudinal_observation_v02(migrated)
    return migrated

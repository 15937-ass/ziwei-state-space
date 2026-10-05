"""Prospective check-in protocol for PL7 longitudinal collection.

The plan freezes targets before the outcome window. It deliberately contains no
outcome truth and cannot promote a mid-window "NO" into a negative sample.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any, Mapping, Sequence


COLLECTION_PURPOSES = frozenset(
    {"BLIND_BENCHMARK", "PERSONALIZED_FOLLOWUP", "CALIBRATION_ONLY"}
)
PREDICTION_EXPOSURES = frozenset({"HIDDEN", "VISIBLE", "NO_FORECAST"})
CHECKPOINT_TYPES = frozenset({"MID_WINDOW", "WINDOW_CLOSE"})
CHECKIN_ANSWERS = frozenset({"YES", "NO", "UNSURE", "NO_RESPONSE"})

FORBIDDEN_PLAN_KEYS = frozenset(
    {
        "outcome",
        "event_status",
        "event_date",
        "observed_through",
        "severity",
        "duration_days",
        "censor_reason",
    }
)

ANSWER_MAPPING = {
    "MID_WINDOW": {
        "YES": "EVENT_OCCURRED_CANDIDATE",
        "NO": "NO_EVENT_YET",
        "UNSURE": "UNKNOWN_CANDIDATE",
        "NO_RESPONSE": "NO_OBSERVATION",
    },
    "WINDOW_CLOSE": {
        "YES": "EVENT_OCCURRED_CANDIDATE",
        "NO": "EVENT_NOT_OCCURRED_CANDIDATE",
        "UNSURE": "UNKNOWN_CANDIDATE",
        "NO_RESPONSE": "NO_OBSERVATION",
    },
}


def _required_text(value: Any, field: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise ValueError(f"{field} is required")
    return text


def _optional_text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _iso_date(value: Any, field: str) -> date:
    text = _required_text(value, field)
    try:
        return date.fromisoformat(text)
    except ValueError as exc:
        raise ValueError(f"{field} must be ISO YYYY-MM-DD") from exc


def _reject_forbidden_keys(value: Any, path: str = "plan") -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            if str(key) in FORBIDDEN_PLAN_KEYS:
                raise ValueError(
                    f"{path}.{key} is outcome leakage and is forbidden in a "
                    "prospective check-in plan"
                )
            _reject_forbidden_keys(child, f"{path}.{key}")
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        for index, child in enumerate(value):
            _reject_forbidden_keys(child, f"{path}[{index}]")


@dataclass(frozen=True)
class CheckinTarget:
    target_id: str
    domain: str
    manifestation_family: str
    event_type: str
    ontology_version: str


@dataclass(frozen=True)
class ScheduledCheckpoint:
    checkpoint_id: str
    checkpoint_type: str
    scheduled_date: date


@dataclass(frozen=True)
class ProspectiveCheckinPlan:
    plan_id: str
    person_key: str
    collection_purpose: str
    prediction_exposure: str
    plan_created_date: date
    target_lock_date: date
    window_start: date
    window_end: date
    targets: tuple[CheckinTarget, ...]
    schedule: tuple[ScheduledCheckpoint, ...]
    forecast_id: str | None
    model_version: str | None
    forecast_locked_date: date | None
    raw: Mapping[str, Any]

    @property
    def blind_benchmark_plan(self) -> bool:
        return (
            self.collection_purpose == "BLIND_BENCHMARK"
            and self.prediction_exposure == "HIDDEN"
            and self.forecast_id is not None
            and self.model_version is not None
            and self.forecast_locked_date is not None
            and self.forecast_locked_date <= self.target_lock_date <= self.window_start
        )


def compile_prospective_checkin_plan(
    payload: Mapping[str, Any],
) -> ProspectiveCheckinPlan:
    if str(payload.get("schema_version", "")).strip() != "0.1":
        raise ValueError("schema_version must be 0.1")

    _reject_forbidden_keys(payload)

    plan_id = _required_text(payload.get("plan_id"), "plan_id")
    person_key = _required_text(payload.get("person_key"), "person_key")

    purpose = _required_text(payload.get("collection_purpose"), "collection_purpose")
    if purpose not in COLLECTION_PURPOSES:
        raise ValueError(f"unsupported collection_purpose: {purpose}")

    exposure = _required_text(
        payload.get("prediction_exposure"), "prediction_exposure"
    )
    if exposure not in PREDICTION_EXPOSURES:
        raise ValueError(f"unsupported prediction_exposure: {exposure}")

    plan_created = _iso_date(payload.get("plan_created_date"), "plan_created_date")
    target_lock = _iso_date(payload.get("target_lock_date"), "target_lock_date")

    window = payload.get("window")
    if not isinstance(window, Mapping):
        raise ValueError("window must be an object")
    start = _iso_date(window.get("start_date"), "window.start_date")
    end = _iso_date(window.get("end_date"), "window.end_date")
    if end < start:
        raise ValueError("window.end_date must be on/after start_date")
    if not (plan_created <= target_lock <= start):
        raise ValueError(
            "plan_created_date <= target_lock_date <= window.start_date is required"
        )

    raw_targets = payload.get("targets")
    if not isinstance(raw_targets, Sequence) or isinstance(raw_targets, (str, bytes)):
        raise ValueError("targets must be an array")
    if not raw_targets:
        raise ValueError("at least one target is required")

    targets = []
    target_ids: set[str] = set()
    for index, item in enumerate(raw_targets):
        if not isinstance(item, Mapping):
            raise ValueError(f"targets[{index}] must be an object")
        target_id = _required_text(item.get("target_id"), f"targets[{index}].target_id")
        if target_id in target_ids:
            raise ValueError(f"duplicate target_id: {target_id}")
        target_ids.add(target_id)
        targets.append(
            CheckinTarget(
                target_id=target_id,
                domain=_required_text(item.get("domain"), f"targets[{index}].domain"),
                manifestation_family=_required_text(
                    item.get("manifestation_family"),
                    f"targets[{index}].manifestation_family",
                ),
                event_type=_required_text(
                    item.get("event_type"), f"targets[{index}].event_type"
                ),
                ontology_version=_required_text(
                    item.get("ontology_version"),
                    f"targets[{index}].ontology_version",
                ),
            )
        )

    raw_schedule = payload.get("schedule")
    if not isinstance(raw_schedule, Sequence) or isinstance(
        raw_schedule, (str, bytes)
    ):
        raise ValueError("schedule must be an array")
    if not raw_schedule:
        raise ValueError("schedule requires a WINDOW_CLOSE checkpoint")

    schedule = []
    checkpoint_ids: set[str] = set()
    close_count = 0
    for index, item in enumerate(raw_schedule):
        if not isinstance(item, Mapping):
            raise ValueError(f"schedule[{index}] must be an object")
        checkpoint_id = _required_text(
            item.get("checkpoint_id"), f"schedule[{index}].checkpoint_id"
        )
        if checkpoint_id in checkpoint_ids:
            raise ValueError(f"duplicate checkpoint_id: {checkpoint_id}")
        checkpoint_ids.add(checkpoint_id)

        checkpoint_type = _required_text(
            item.get("type"), f"schedule[{index}].type"
        )
        if checkpoint_type not in CHECKPOINT_TYPES:
            raise ValueError(f"unsupported checkpoint type: {checkpoint_type}")
        scheduled_date = _iso_date(
            item.get("scheduled_date"), f"schedule[{index}].scheduled_date"
        )
        if not (start <= scheduled_date <= end):
            raise ValueError("scheduled checkpoints must lie inside target window")
        if checkpoint_type == "WINDOW_CLOSE":
            close_count += 1
            if scheduled_date != end:
                raise ValueError(
                    "WINDOW_CLOSE checkpoint must be scheduled on window.end_date"
                )
        schedule.append(
            ScheduledCheckpoint(
                checkpoint_id=checkpoint_id,
                checkpoint_type=checkpoint_type,
                scheduled_date=scheduled_date,
            )
        )

    if close_count != 1:
        raise ValueError("exactly one WINDOW_CLOSE checkpoint is required")

    forecast = payload.get("forecast")
    if not isinstance(forecast, Mapping):
        raise ValueError("forecast must be an object")
    forecast_id = _optional_text(forecast.get("forecast_id"))
    model_version = _optional_text(forecast.get("model_version"))
    forecast_locked = (
        _iso_date(forecast.get("locked_date"), "forecast.locked_date")
        if forecast.get("locked_date")
        else None
    )

    if exposure == "NO_FORECAST":
        if any((forecast_id, model_version, forecast_locked)):
            raise ValueError(
                "NO_FORECAST requires forecast_id/model_version/locked_date to be null"
            )
    else:
        if not all((forecast_id, model_version, forecast_locked)):
            raise ValueError(
                "VISIBLE/HIDDEN prediction exposure requires complete forecast linkage"
            )
        if forecast_locked > target_lock:
            raise ValueError("forecast must be locked on/before target_lock_date")

    if purpose == "BLIND_BENCHMARK" and exposure != "HIDDEN":
        raise ValueError("BLIND_BENCHMARK requires prediction_exposure=HIDDEN")

    return ProspectiveCheckinPlan(
        plan_id=plan_id,
        person_key=person_key,
        collection_purpose=purpose,
        prediction_exposure=exposure,
        plan_created_date=plan_created,
        target_lock_date=target_lock,
        window_start=start,
        window_end=end,
        targets=tuple(targets),
        schedule=tuple(sorted(schedule, key=lambda item: item.scheduled_date)),
        forecast_id=forecast_id,
        model_version=model_version,
        forecast_locked_date=forecast_locked,
        raw=dict(payload),
    )


def classify_checkin_answer(checkpoint_type: str, answer: str) -> str:
    checkpoint = str(checkpoint_type or "").strip()
    normalized = str(answer or "").strip()
    if checkpoint not in CHECKPOINT_TYPES:
        raise ValueError(f"unsupported checkpoint type: {checkpoint}")
    if normalized not in CHECKIN_ANSWERS:
        raise ValueError(f"unsupported check-in answer: {normalized}")
    return ANSWER_MAPPING[checkpoint][normalized]

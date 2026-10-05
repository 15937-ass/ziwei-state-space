"""PL7 longitudinal observation contract and validation.

The record is deliberately independent of canonical Zi Wei rule truth.
It captures real-world longitudinal observations used later for calibration,
benchmarking and personal-state estimation.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any, Mapping, Sequence


EVENT_STATUSES = frozenset(
    {"EVENT_OCCURRED", "EVENT_NOT_OCCURRED", "UNKNOWN", "CENSORED"}
)
OBSERVATION_DESIGNS = frozenset({"PROSPECTIVE", "RETROSPECTIVE"})
FORECAST_MODES = frozenset({"NONE", "BLIND", "PERSONALIZED"})
CONFIDENCE_LEVELS = frozenset({"HIGH", "MEDIUM", "LOW", "INSUFFICIENT"})
ACTION_STATUSES = frozenset(
    {"INTENDED", "PLANNED", "ACTUAL", "ABANDONED", "UNKNOWN"}
)
SOURCE_TYPES = frozenset(
    {
        "USER_SELF_REPORT",
        "DOCUMENTED_RECORD",
        "RESEARCH_INTERVIEW",
        "PUBLIC_RECORD",
        "OTHER",
    }
)


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


@dataclass(frozen=True)
class LongitudinalObservationRecord:
    record_id: str
    person_key: str
    observation_design: str
    window_start: date
    window_end: date
    observed_through: date
    target_id: str
    domain: str
    manifestation_family: str
    event_type: str
    ontology_version: str
    event_status: str
    event_date: date | None
    censor_reason: str | None
    observation_source: str
    observation_confidence: str
    collected_date: date
    forecast_mode: str
    forecast_id: str | None
    model_version: str | None
    forecast_locked_date: date | None
    actions: tuple[Mapping[str, Any], ...]
    exposures: tuple[str, ...]
    external_factors: tuple[str, ...]
    counterparty_factors: tuple[str, ...]
    raw: Mapping[str, Any]

    @property
    def is_closed_negative(self) -> bool:
        return (
            self.event_status == "EVENT_NOT_OCCURRED"
            and self.observed_through >= self.window_end
            and self.observation_confidence != "INSUFFICIENT"
        )

    @property
    def is_survival_usable_censoring(self) -> bool:
        return (
            self.event_status == "CENSORED"
            and self.observed_through < self.window_end
            and self.observation_confidence != "INSUFFICIENT"
        )

    @property
    def calibration_usable(self) -> bool:
        if self.observation_confidence == "INSUFFICIENT":
            return False
        if self.event_status == "EVENT_OCCURRED":
            return True
        if self.event_status == "EVENT_NOT_OCCURRED":
            return self.is_closed_negative
        if self.event_status == "CENSORED":
            return self.is_survival_usable_censoring
        return False

    @property
    def blind_benchmark_eligible(self) -> bool:
        return (
            self.observation_design == "PROSPECTIVE"
            and self.forecast_mode == "BLIND"
            and self.forecast_id is not None
            and self.model_version is not None
            and self.forecast_locked_date is not None
            and self.forecast_locked_date <= self.window_start
            and self.calibration_usable
        )


def _validate_actions(actions: Any) -> tuple[Mapping[str, Any], ...]:
    if not isinstance(actions, Sequence) or isinstance(actions, (str, bytes)):
        raise ValueError("actions must be an array")
    out = []
    ids: set[str] = set()
    for index, item in enumerate(actions):
        if not isinstance(item, Mapping):
            raise ValueError(f"actions[{index}] must be an object")
        action_id = _required_text(item.get("action_id"), f"actions[{index}].action_id")
        if action_id in ids:
            raise ValueError(f"duplicate action_id: {action_id}")
        ids.add(action_id)
        status = _required_text(item.get("status"), f"actions[{index}].status")
        if status not in ACTION_STATUSES:
            raise ValueError(f"unsupported action status: {status}")
        _required_text(item.get("label"), f"actions[{index}].label")
        confidence = _required_text(
            item.get("confidence"), f"actions[{index}].confidence"
        )
        if confidence not in CONFIDENCE_LEVELS:
            raise ValueError(f"unsupported action confidence: {confidence}")
        if item.get("date"):
            _iso_date(item["date"], f"actions[{index}].date")
        out.append(dict(item))
    return tuple(out)


def _text_tuple(value: Any, field: str) -> tuple[str, ...]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise ValueError(f"{field} must be an array")
    return tuple(str(item).strip() for item in value if str(item).strip())


def compile_longitudinal_observation(
    payload: Mapping[str, Any],
) -> LongitudinalObservationRecord:
    if str(payload.get("schema_version", "")).strip() != "0.1":
        raise ValueError("schema_version must be 0.1")

    record_id = _required_text(payload.get("record_id"), "record_id")
    person_key = _required_text(payload.get("person_key"), "person_key")

    design = _required_text(payload.get("observation_design"), "observation_design")
    if design not in OBSERVATION_DESIGNS:
        raise ValueError(f"unsupported observation_design: {design}")

    window = payload.get("window")
    target = payload.get("target")
    outcome = payload.get("outcome")
    observation = payload.get("observation")
    linkage = payload.get("model_linkage")
    context = payload.get("context")
    for value, name in (
        (window, "window"),
        (target, "target"),
        (outcome, "outcome"),
        (observation, "observation"),
        (linkage, "model_linkage"),
        (context, "context"),
    ):
        if not isinstance(value, Mapping):
            raise ValueError(f"{name} must be an object")

    window_start = _iso_date(window.get("start_date"), "window.start_date")
    window_end = _iso_date(window.get("end_date"), "window.end_date")
    observed_through = _iso_date(
        window.get("observed_through"), "window.observed_through"
    )
    if window_end < window_start:
        raise ValueError("window.end_date must be on/after start_date")
    if observed_through < window_start:
        raise ValueError("window.observed_through cannot predate start_date")

    target_id = _required_text(target.get("target_id"), "target.target_id")
    domain = _required_text(target.get("domain"), "target.domain")
    manifestation_family = _required_text(
        target.get("manifestation_family"), "target.manifestation_family"
    )
    event_type = _required_text(target.get("event_type"), "target.event_type")
    ontology_version = _required_text(
        target.get("ontology_version"), "target.ontology_version"
    )

    event_status = _required_text(outcome.get("status"), "outcome.status")
    if event_status not in EVENT_STATUSES:
        raise ValueError(f"unsupported event status: {event_status}")

    event_date = (
        _iso_date(outcome.get("event_date"), "outcome.event_date")
        if outcome.get("event_date")
        else None
    )
    censor_reason = _optional_text(outcome.get("censor_reason"))

    source_type = _required_text(
        observation.get("source_type"), "observation.source_type"
    )
    if source_type not in SOURCE_TYPES:
        raise ValueError(f"unsupported observation source: {source_type}")
    observation_confidence = _required_text(
        observation.get("confidence"), "observation.confidence"
    )
    if observation_confidence not in CONFIDENCE_LEVELS:
        raise ValueError(
            f"unsupported observation confidence: {observation_confidence}"
        )
    collected_date = _iso_date(
        observation.get("collected_date"), "observation.collected_date"
    )

    forecast = linkage.get("forecast")
    if not isinstance(forecast, Mapping):
        raise ValueError("model_linkage.forecast must be an object")
    forecast_mode = _required_text(forecast.get("mode"), "model_linkage.forecast.mode")
    if forecast_mode not in FORECAST_MODES:
        raise ValueError(f"unsupported forecast mode: {forecast_mode}")
    forecast_id = _optional_text(forecast.get("forecast_id"))
    model_version = _optional_text(forecast.get("model_version"))
    locked_date = (
        _iso_date(
            forecast.get("locked_date"),
            "model_linkage.forecast.locked_date",
        )
        if forecast.get("locked_date")
        else None
    )

    if forecast_mode == "NONE":
        if any((forecast_id, model_version, locked_date)):
            raise ValueError("forecast metadata must be null when forecast mode is NONE")
    else:
        if not all((forecast_id, model_version, locked_date)):
            raise ValueError(
                "forecast_id, model_version and locked_date are required "
                "for BLIND/PERSONALIZED forecast linkage"
            )

    if event_status == "EVENT_OCCURRED":
        if event_date is None:
            raise ValueError("EVENT_OCCURRED requires outcome.event_date")
        if not (window_start <= event_date <= window_end):
            raise ValueError("outcome.event_date must lie inside the target window")
        if observed_through < event_date:
            raise ValueError("observed_through cannot predate the occurred event")
        if censor_reason is not None:
            raise ValueError("EVENT_OCCURRED cannot carry censor_reason")
    elif event_status == "EVENT_NOT_OCCURRED":
        if event_date is not None:
            raise ValueError("EVENT_NOT_OCCURRED cannot carry event_date")
        if observed_through < window_end:
            raise ValueError(
                "EVENT_NOT_OCCURRED requires observation through the full window; "
                "use CENSORED or UNKNOWN otherwise"
            )
        if observation_confidence == "INSUFFICIENT":
            raise ValueError(
                "EVENT_NOT_OCCURRED requires sufficient observation confidence"
            )
        if censor_reason is not None:
            raise ValueError("EVENT_NOT_OCCURRED cannot carry censor_reason")
    elif event_status == "CENSORED":
        if event_date is not None:
            raise ValueError("CENSORED cannot carry event_date")
        if observed_through >= window_end:
            raise ValueError(
                "CENSORED requires observed_through before window end; "
                "use EVENT_NOT_OCCURRED if the full window was observed"
            )
        if censor_reason is None:
            raise ValueError("CENSORED requires censor_reason")
    else:
        if event_date is not None:
            raise ValueError("UNKNOWN cannot carry event_date")

    if (
        design == "PROSPECTIVE"
        and forecast_mode != "NONE"
        and locked_date is not None
        and locked_date > window_start
    ):
        raise ValueError(
            "prospective forecast must be locked on/before target window start"
        )

    actions = _validate_actions(payload.get("actions"))
    exposures = _text_tuple(context.get("exposures"), "context.exposures")
    external_factors = _text_tuple(
        context.get("external_factors"), "context.external_factors"
    )
    counterparty_factors = _text_tuple(
        context.get("counterparty_factors"), "context.counterparty_factors"
    )

    return LongitudinalObservationRecord(
        record_id=record_id,
        person_key=person_key,
        observation_design=design,
        window_start=window_start,
        window_end=window_end,
        observed_through=observed_through,
        target_id=target_id,
        domain=domain,
        manifestation_family=manifestation_family,
        event_type=event_type,
        ontology_version=ontology_version,
        event_status=event_status,
        event_date=event_date,
        censor_reason=censor_reason,
        observation_source=source_type,
        observation_confidence=observation_confidence,
        collected_date=collected_date,
        forecast_mode=forecast_mode,
        forecast_id=forecast_id,
        model_version=model_version,
        forecast_locked_date=locked_date,
        actions=actions,
        exposures=exposures,
        external_factors=external_factors,
        counterparty_factors=counterparty_factors,
        raw=dict(payload),
    )

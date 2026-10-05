"""PL7 prospective check-in -> observation bridge v0.2.

This bridge accepts bounded event-time reports (DAY / MONTH / YEAR / INTERVAL)
and produces LongitudinalObservationRecord v0.2 payloads without fabricating
precision.
"""

from __future__ import annotations

import calendar
from dataclasses import dataclass
from datetime import date
from typing import Any, Mapping

from .checkin_observation_bridge import BRIDGE_DISPOSITIONS
from .longitudinal_observation_v02 import (
    EventTimeInterval,
    compile_longitudinal_observation_v02,
)
from .prospective_checkin import (
    ProspectiveCheckinPlan,
    classify_checkin_answer,
)


BRIDGE_V02_DISPOSITIONS = frozenset(
    set(BRIDGE_DISPOSITIONS)
    | {
        "NEEDS_EVENT_TIME_DETAIL",
        "TEMPORAL_ASSIGNMENT_AMBIGUOUS",
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


def _target(plan: ProspectiveCheckinPlan, target_id: str):
    for target in plan.targets:
        if target.target_id == target_id:
            return target
    raise ValueError(f"target_id not present in locked plan: {target_id}")


def _checkpoint(plan: ProspectiveCheckinPlan, checkpoint_id: str):
    for checkpoint in plan.schedule:
        if checkpoint.checkpoint_id == checkpoint_id:
            return checkpoint
    raise ValueError(f"checkpoint_id not present in locked plan: {checkpoint_id}")


def _forecast_mode(plan: ProspectiveCheckinPlan) -> str:
    if plan.prediction_exposure == "NO_FORECAST":
        return "NONE"
    if plan.collection_purpose == "BLIND_BENCHMARK":
        return "BLIND"
    return "PERSONALIZED"


@dataclass(frozen=True)
class CheckinBridgeResultV02:
    disposition: str
    candidate_status: str
    observation_payload: Mapping[str, Any] | None
    normalized_event_time: Mapping[str, Any] | None = None

    def __post_init__(self) -> None:
        if self.disposition not in BRIDGE_V02_DISPOSITIONS:
            raise ValueError(f"unsupported bridge disposition: {self.disposition}")


def normalize_event_time_report(report: Mapping[str, Any]) -> dict[str, str]:
    """Normalize an explicitly reported event time into bounded v0.2 form."""

    if not isinstance(report, Mapping):
        raise ValueError("event_time_report must be an object")

    precision = _required_text(report.get("precision"), "event_time_report.precision")

    if precision == "DAY":
        value = _required_text(report.get("value"), "event_time_report.value")
        day = _iso_date(value, "event_time_report.value")
        lower = upper = day

    elif precision == "MONTH":
        value = _required_text(report.get("value"), "event_time_report.value")
        parts = value.split("-")
        if len(parts) != 2:
            raise ValueError("MONTH precision value must be YYYY-MM")
        try:
            year = int(parts[0])
            month = int(parts[1])
            if not 1 <= month <= 12:
                raise ValueError
        except ValueError as exc:
            raise ValueError("MONTH precision value must be YYYY-MM") from exc
        lower = date(year, month, 1)
        upper = date(year, month, calendar.monthrange(year, month)[1])

    elif precision == "YEAR":
        value = _required_text(report.get("value"), "event_time_report.value")
        if len(value) != 4 or not value.isdigit():
            raise ValueError("YEAR precision value must be YYYY")
        year = int(value)
        lower = date(year, 1, 1)
        upper = date(year, 12, 31)

    elif precision == "INTERVAL":
        lower = _iso_date(
            report.get("lower_bound_date"),
            "event_time_report.lower_bound_date",
        )
        upper = _iso_date(
            report.get("upper_bound_date"),
            "event_time_report.upper_bound_date",
        )
        if upper < lower:
            raise ValueError("event_time_report interval upper bound predates lower bound")

    else:
        raise ValueError(f"unsupported event-time precision: {precision}")

    EventTimeInterval(
        precision=precision,
        lower_bound=lower,
        upper_bound=upper,
    )

    return {
        "precision": precision,
        "lower_bound_date": lower.isoformat(),
        "upper_bound_date": upper.isoformat(),
    }


def bridge_checkin_response_v02(
    plan: ProspectiveCheckinPlan,
    response: Mapping[str, Any],
    *,
    linkage: Mapping[str, Any] | None = None,
) -> CheckinBridgeResultV02:
    if str(response.get("schema_version", "")).strip() != "0.2":
        raise ValueError("response schema_version must be 0.2")

    if _required_text(response.get("plan_id"), "plan_id") != plan.plan_id:
        raise ValueError("response plan_id does not match locked plan")

    target_id = _required_text(response.get("target_id"), "target_id")
    checkpoint_id = _required_text(response.get("checkpoint_id"), "checkpoint_id")
    answer = _required_text(response.get("answer"), "answer")
    response_date = _iso_date(response.get("response_date"), "response_date")

    target = _target(plan, target_id)
    checkpoint = _checkpoint(plan, checkpoint_id)
    candidate_status = classify_checkin_answer(checkpoint.checkpoint_type, answer)

    if not bool(response.get("user_confirmed", False)):
        return CheckinBridgeResultV02(
            disposition="NEEDS_USER_CONFIRMATION",
            candidate_status=candidate_status,
            observation_payload=None,
        )

    if candidate_status == "NO_EVENT_YET":
        return CheckinBridgeResultV02(
            disposition="NO_EVENT_YET",
            candidate_status=candidate_status,
            observation_payload=None,
        )

    if candidate_status == "NO_OBSERVATION":
        return CheckinBridgeResultV02(
            disposition="NO_OBSERVATION",
            candidate_status=candidate_status,
            observation_payload=None,
        )

    event_time = None
    event_status: str
    observed_through: date

    if candidate_status == "EVENT_OCCURRED_CANDIDATE":
        report = response.get("event_time_report")
        if report is None:
            return CheckinBridgeResultV02(
                disposition="NEEDS_EVENT_TIME_DETAIL",
                candidate_status=candidate_status,
                observation_payload=None,
            )
        event_time = normalize_event_time_report(report)
        interval = EventTimeInterval(
            precision=event_time["precision"],
            lower_bound=_iso_date(
                event_time["lower_bound_date"],
                "event_time.lower_bound_date",
            ),
            upper_bound=_iso_date(
                event_time["upper_bound_date"],
                "event_time.upper_bound_date",
            ),
        )

        if interval.upper_bound > response_date:
            raise ValueError("reported event-time interval cannot end after response_date")

        if not interval.fully_within(plan.window_start, plan.window_end):
            if interval.overlaps(plan.window_start, plan.window_end):
                return CheckinBridgeResultV02(
                    disposition="TEMPORAL_ASSIGNMENT_AMBIGUOUS",
                    candidate_status=candidate_status,
                    observation_payload=None,
                    normalized_event_time=event_time,
                )
            raise ValueError("reported event-time interval lies outside locked target window")

        event_status = "EVENT_OCCURRED"
        observed_through = response_date

    elif candidate_status == "EVENT_NOT_OCCURRED_CANDIDATE":
        if response_date < plan.window_end:
            raise ValueError("window-close negative cannot finalize before window end")
        if response.get("event_time_report") is not None:
            raise ValueError("negative response cannot carry event_time_report")
        event_status = "EVENT_NOT_OCCURRED"
        observed_through = plan.window_end

    else:
        if response.get("event_time_report") is not None:
            raise ValueError("UNSURE response cannot carry event_time_report")
        event_status = "UNKNOWN"
        observed_through = min(response_date, plan.window_end)

    observation = response.get("observation")
    if not isinstance(observation, Mapping):
        raise ValueError("observation must be an object")

    source_type = _required_text(
        observation.get("source_type"), "observation.source_type"
    )
    confidence = _required_text(
        observation.get("confidence"), "observation.confidence"
    )
    notes_ref = _optional_text(observation.get("notes_ref"))

    actions = response.get("actions", [])
    context = response.get(
        "context",
        {"exposures": [], "external_factors": [], "counterparty_factors": []},
    )
    if not isinstance(context, Mapping):
        raise ValueError("context must be an object")

    link = dict(linkage or {})
    forecast_mode = _forecast_mode(plan)
    if forecast_mode == "NONE":
        forecast = {
            "mode": "NONE",
            "forecast_id": None,
            "model_version": None,
            "locked_date": None,
        }
    else:
        forecast = {
            "mode": forecast_mode,
            "forecast_id": plan.forecast_id,
            "model_version": plan.model_version,
            "locked_date": (
                plan.forecast_locked_date.isoformat()
                if plan.forecast_locked_date
                else None
            ),
        }

    payload = {
        "schema_version": "0.2",
        "record_id": _required_text(response.get("record_id"), "record_id"),
        "person_key": plan.person_key,
        "observation_design": "PROSPECTIVE",
        "window": {
            "start_date": plan.window_start.isoformat(),
            "end_date": plan.window_end.isoformat(),
            "observed_through": observed_through.isoformat(),
            "timezone": link.get("timezone"),
            "precision": str(link.get("precision") or "DAY"),
        },
        "target": {
            "target_id": target.target_id,
            "domain": target.domain,
            "manifestation_family": target.manifestation_family,
            "event_type": target.event_type,
            "ontology_version": target.ontology_version,
        },
        "actions": list(actions),
        "context": {
            "exposures": list(context.get("exposures", [])),
            "external_factors": list(context.get("external_factors", [])),
            "counterparty_factors": list(context.get("counterparty_factors", [])),
        },
        "outcome": {
            "status": event_status,
            "event_time": event_time,
            "severity": _optional_text(response.get("severity")),
            "duration_days": response.get("duration_days"),
            "censor_reason": None,
        },
        "observation": {
            "source_type": source_type,
            "confidence": confidence,
            "collected_date": response_date.isoformat(),
            "notes_ref": notes_ref,
        },
        "model_linkage": {
            "chart_version": link.get("chart_version"),
            "knowledge_version": link.get("knowledge_version"),
            "natal_state_ref": link.get("natal_state_ref"),
            "temporal_environment_ref": link.get("temporal_environment_ref"),
            "state_before_ref": link.get("state_before_ref"),
            "forecast": forecast,
        },
    }

    compile_longitudinal_observation_v02(payload)

    return CheckinBridgeResultV02(
        disposition="OBSERVATION_READY",
        candidate_status=candidate_status,
        observation_payload=payload,
        normalized_event_time=event_time,
    )

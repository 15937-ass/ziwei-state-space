"""Bridge prospective check-in responses into longitudinal observation candidates.

The bridge is intentionally deterministic. It cannot finalize an observation
unless the response is explicitly user-confirmed and satisfies the locked plan.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any, Mapping

from .longitudinal_observation import compile_longitudinal_observation
from .prospective_checkin import (
    ProspectiveCheckinPlan,
    classify_checkin_answer,
)


BRIDGE_DISPOSITIONS = frozenset(
    {
        "OBSERVATION_READY",
        "NO_EVENT_YET",
        "NO_OBSERVATION",
        "NEEDS_USER_CONFIRMATION",
        "NEEDS_EVENT_DATE_DETAIL",
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
class CheckinBridgeResult:
    disposition: str
    candidate_status: str
    observation_payload: Mapping[str, Any] | None

    def __post_init__(self) -> None:
        if self.disposition not in BRIDGE_DISPOSITIONS:
            raise ValueError(f"unsupported bridge disposition: {self.disposition}")


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


def bridge_checkin_response(
    plan: ProspectiveCheckinPlan,
    response: Mapping[str, Any],
    *,
    linkage: Mapping[str, Any] | None = None,
) -> CheckinBridgeResult:
    """Convert one locked-plan response into a validated observation candidate.

    linkage carries optional chart/state refs that do not alter the locked
    target definition.
    """

    if str(response.get("schema_version", "")).strip() != "0.1":
        raise ValueError("response schema_version must be 0.1")

    if _required_text(response.get("plan_id"), "plan_id") != plan.plan_id:
        raise ValueError("response plan_id does not match locked plan")

    target_id = _required_text(response.get("target_id"), "target_id")
    checkpoint_id = _required_text(response.get("checkpoint_id"), "checkpoint_id")
    answer = _required_text(response.get("answer"), "answer")
    response_date = _iso_date(response.get("response_date"), "response_date")

    target = _target(plan, target_id)
    checkpoint = _checkpoint(plan, checkpoint_id)
    candidate_status = classify_checkin_answer(checkpoint.checkpoint_type, answer)

    confirmed = bool(response.get("user_confirmed", False))
    if not confirmed:
        return CheckinBridgeResult(
            disposition="NEEDS_USER_CONFIRMATION",
            candidate_status=candidate_status,
            observation_payload=None,
        )

    if candidate_status == "NO_EVENT_YET":
        return CheckinBridgeResult(
            disposition="NO_EVENT_YET",
            candidate_status=candidate_status,
            observation_payload=None,
        )

    if candidate_status == "NO_OBSERVATION":
        return CheckinBridgeResult(
            disposition="NO_OBSERVATION",
            candidate_status=candidate_status,
            observation_payload=None,
        )

    event_date = (
        _iso_date(response.get("event_date"), "event_date")
        if response.get("event_date")
        else None
    )

    if candidate_status == "EVENT_OCCURRED_CANDIDATE":
        if event_date is None:
            return CheckinBridgeResult(
                disposition="NEEDS_EVENT_DATE_DETAIL",
                candidate_status=candidate_status,
                observation_payload=None,
            )
        if event_date > response_date:
            raise ValueError("event_date cannot be after response_date")
        event_status = "EVENT_OCCURRED"
        observed_through = response_date
    elif candidate_status == "EVENT_NOT_OCCURRED_CANDIDATE":
        if response_date < plan.window_end:
            raise ValueError(
                "window-close negative cannot finalize before window end"
            )
        if event_date is not None:
            raise ValueError("negative response cannot carry event_date")
        event_status = "EVENT_NOT_OCCURRED"
        observed_through = plan.window_end
    else:
        if event_date is not None:
            raise ValueError("UNSURE response cannot carry event_date")
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
        "schema_version": "0.1",
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
            "event_date": event_date.isoformat() if event_date else None,
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

    compile_longitudinal_observation(payload)

    return CheckinBridgeResult(
        disposition="OBSERVATION_READY",
        candidate_status=candidate_status,
        observation_payload=payload,
    )

"""Deterministic lifecycle management for PL7 prospective cohort windows.

This module tracks collection lifecycle and follow-up completeness separately
from event truth. It is pure/in-memory and never creates observations or
infers a negative outcome from missing follow-up.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import date
import hashlib
import json
from typing import Any, Mapping, Sequence

from .longitudinal_data_quality_audit import audit_longitudinal_data_quality
from .prospective_checkin import compile_prospective_checkin_plan


WINDOW_STATES = frozenset(
    {"PLANNED", "OPEN", "CLOSED", "CANCELLED", "TERMINATED_EARLY"}
)
FOLLOWUP_STATES = frozenset(
    {
        "NOT_STARTED",
        "IN_PROGRESS",
        "COMPLETE",
        "INCOMPLETE",
        "WITHDRAWN",
        "LOST_TO_FOLLOW_UP",
    }
)
EARLY_TERMINATION_DISPOSITIONS = frozenset({"WITHDRAWN", "LOST_TO_FOLLOW_UP"})


def _text(value: Any) -> str:
    return str(value or "").strip()


def _required_text(value: Any, field: str) -> str:
    text = _text(value)
    if not text:
        raise ValueError(f"{field} is required")
    return text


def _iso_date(value: Any, field: str) -> date:
    text = _required_text(value, field)
    try:
        return date.fromisoformat(text)
    except ValueError as exc:
        raise ValueError(f"{field} must be ISO YYYY-MM-DD") from exc


def _is_sequence(value: Any) -> bool:
    return isinstance(value, Sequence) and not isinstance(
        value, (str, bytes, bytearray)
    )


def _plan_digest(plan_payload: Mapping[str, Any]) -> str:
    try:
        canonical = json.dumps(
            dict(plan_payload),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ValueError("plan must be JSON-serializable for immutable provenance") from exc
    return hashlib.sha256(canonical).hexdigest()


def _validate_state(state: Mapping[str, Any]):
    if not isinstance(state, Mapping):
        raise ValueError("cohort window state must be an object")
    if str(state.get("schema_version", "")) != "0.1":
        raise ValueError("schema_version must be 0.1")
    plan = state.get("plan")
    if not isinstance(plan, Mapping):
        raise ValueError("state.plan must be an object")
    compiled = compile_prospective_checkin_plan(plan)
    expected_digest = _plan_digest(plan)
    if _text(state.get("plan_digest")) != expected_digest:
        raise ValueError("locked plan digest mismatch; plan provenance is immutable")
    if _text(state.get("plan_id")) != compiled.plan_id:
        raise ValueError("state.plan_id must match the compiled plan")
    if _text(state.get("person_key")) != compiled.person_key:
        raise ValueError("state.person_key must match the compiled plan")
    expected_window = {
        "start_date": compiled.window_start.isoformat(),
        "end_date": compiled.window_end.isoformat(),
    }
    if state.get("window") != expected_window:
        raise ValueError("state.window must match the locked plan window")
    if state.get("window_status") not in WINDOW_STATES:
        raise ValueError("unsupported window_status")
    if state.get("followup_status") not in FOLLOWUP_STATES:
        raise ValueError("unsupported followup_status")
    return compiled


def register_prospective_cohort_window(
    plan_payload: Mapping[str, Any],
) -> dict[str, Any]:
    """Register a validated, outcome-free prospective plan as a planned window."""
    if not isinstance(plan_payload, Mapping):
        raise ValueError("plan_payload must be an object")
    plan = compile_prospective_checkin_plan(plan_payload)
    return {
        "schema_version": "0.1",
        "plan_id": plan.plan_id,
        "person_key": plan.person_key,
        "plan": deepcopy(dict(plan_payload)),
        "plan_digest": _plan_digest(plan_payload),
        "window": {
            "start_date": plan.window_start.isoformat(),
            "end_date": plan.window_end.isoformat(),
        },
        "window_status": "PLANNED",
        "followup_status": "NOT_STARTED",
        "opened_date": None,
        "closed_date": None,
        "cancellation": None,
        "termination": None,
        "followup_summary": None,
    }


def open_prospective_cohort_window(
    state: Mapping[str, Any], *, on_date: str
) -> dict[str, Any]:
    """Open a planned window on/after its start and never after its end."""
    plan = _validate_state(state)
    action_date = _iso_date(on_date, "on_date")
    if state["window_status"] != "PLANNED":
        raise ValueError("only a PLANNED window can be opened")
    if action_date < plan.window_start:
        raise ValueError("window cannot open before window.start_date")
    if action_date > plan.window_end:
        raise ValueError("window cannot open after window.end_date; close it as due instead")

    updated = deepcopy(dict(state))
    updated["window_status"] = "OPEN"
    updated["followup_status"] = "IN_PROGRESS"
    updated["opened_date"] = action_date.isoformat()
    return updated


def cancel_prospective_cohort_window(
    state: Mapping[str, Any], *, on_date: str, reason: str
) -> dict[str, Any]:
    """Cancel a planned window before its start with an explicit reason."""
    plan = _validate_state(state)
    action_date = _iso_date(on_date, "on_date")
    cancellation_reason = _required_text(reason, "reason")
    if state["window_status"] != "PLANNED":
        raise ValueError("only a PLANNED window can be cancelled")
    if action_date >= plan.window_start:
        raise ValueError("window can only be cancelled before window.start_date")

    updated = deepcopy(dict(state))
    updated["window_status"] = "CANCELLED"
    updated["followup_status"] = "NOT_STARTED"
    updated["cancellation"] = {
        "cancelled_date": action_date.isoformat(),
        "reason": cancellation_reason,
    }
    return updated


def terminate_prospective_cohort_followup(
    state: Mapping[str, Any],
    *,
    on_date: str,
    disposition: str,
    reason: str,
    observed_through: str,
) -> dict[str, Any]:
    """Terminate follow-up early and preserve explicit censoring metadata only."""
    plan = _validate_state(state)
    action_date = _iso_date(on_date, "on_date")
    observed_date = _iso_date(observed_through, "observed_through")
    normalized_disposition = _required_text(disposition, "disposition")
    termination_reason = _required_text(reason, "reason")

    if state["window_status"] != "OPEN":
        raise ValueError("early follow-up termination requires an OPEN window")
    if normalized_disposition not in EARLY_TERMINATION_DISPOSITIONS:
        raise ValueError("disposition must be WITHDRAWN or LOST_TO_FOLLOW_UP")
    if not (plan.window_start <= action_date < plan.window_end):
        raise ValueError("early termination date must be inside the target window and before its end")
    if not (plan.window_start <= observed_date <= action_date):
        raise ValueError(
            "observed_through must be inside the observed window and no later than on_date"
        )

    updated = deepcopy(dict(state))
    updated["window_status"] = "TERMINATED_EARLY"
    updated["followup_status"] = normalized_disposition
    updated["termination"] = {
        "disposition": normalized_disposition,
        "termination_date": action_date.isoformat(),
        "observed_through": observed_date.isoformat(),
        "censor_reason": termination_reason,
    }
    updated["followup_summary"] = None
    return updated


def close_prospective_cohort_window(
    state: Mapping[str, Any],
    *,
    on_date: str,
    checkin_responses: Sequence[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    """Close a window on/after its end and audit completeness without imputing outcomes.

    A missed window may be administratively closed after its end while remaining
    INCOMPLETE. The returned state contains no event_status or inferred outcome.
    """
    plan = _validate_state(state)
    action_date = _iso_date(on_date, "on_date")
    if state["window_status"] not in {"PLANNED", "OPEN"}:
        raise ValueError("only a PLANNED or OPEN window can be closed")
    if action_date < plan.window_end:
        raise ValueError("window cannot close before window.end_date")
    if not _is_sequence(checkin_responses):
        raise ValueError("checkin_responses must be an array")
    responses = []
    for index, response in enumerate(checkin_responses):
        if not isinstance(response, Mapping):
            raise ValueError(f"checkin_responses[{index}] must be an object")
        response_plan_id = _text(response.get("plan_id"))
        if response_plan_id and response_plan_id != plan.plan_id:
            raise ValueError("all supplied check-in responses must match this plan_id")
        responses.append(dict(response))

    audit = audit_longitudinal_data_quality(
        plans=[dict(state["plan"])],
        checkin_responses=responses,
    )
    counts = audit["counts"]
    expected = counts["expected_window_close_responses"]
    complete = counts["complete_window_close_responses"]
    missing = counts["missing_window_close_responses"]
    unresolved = counts["unresolved_window_close_responses"]
    is_complete = expected == complete and missing == 0 and unresolved == 0
    finding_codes = sorted({str(item.get("code", "")) for item in audit["findings"]})

    updated = deepcopy(dict(state))
    updated["window_status"] = "CLOSED"
    updated["followup_status"] = "COMPLETE" if is_complete else "INCOMPLETE"
    updated["closed_date"] = action_date.isoformat()
    updated["followup_summary"] = {
        "status": updated["followup_status"],
        "audit_status": audit["status"],
        "expected_window_close_responses": expected,
        "matched_window_close_responses": counts["matched_window_close_responses"],
        "complete_window_close_responses": complete,
        "missing_window_close_responses": missing,
        "window_close_no_response": counts["window_close_no_response"],
        "unresolved_window_close_responses": unresolved,
        "finding_codes": finding_codes,
    }
    return updated


def build_prospective_cohort_queue(
    windows: Sequence[Mapping[str, Any]], *, as_of_date: str
) -> list[dict[str, Any]]:
    """Return a stable queue snapshot for a caller-supplied date; do not mutate inputs."""
    if not _is_sequence(windows):
        raise ValueError("windows must be an array")
    snapshot_date = _iso_date(as_of_date, "as_of_date")
    entries: list[dict[str, Any]] = []
    seen_plan_ids: set[str] = set()

    for state in windows:
        plan = _validate_state(state)
        if plan.plan_id in seen_plan_ids:
            raise ValueError(f"duplicate plan_id in queue: {plan.plan_id}")
        seen_plan_ids.add(plan.plan_id)

        lifecycle = state["window_status"]
        if lifecycle == "PLANNED":
            if snapshot_date < plan.window_start:
                queue_status, next_action = "SCHEDULED", "WAIT_FOR_WINDOW_START"
            elif snapshot_date <= plan.window_end:
                queue_status, next_action = "OPEN_DUE", "OPEN_WINDOW"
            else:
                queue_status, next_action = "CLOSE_DUE", "CLOSE_WINDOW_AND_AUDIT_FOLLOW_UP"
        elif lifecycle == "OPEN":
            if snapshot_date <= plan.window_end:
                queue_status, next_action = "OPEN", "COLLECT_CHECKPOINTS"
            else:
                queue_status, next_action = "CLOSE_DUE", "CLOSE_WINDOW_AND_AUDIT_FOLLOW_UP"
        elif lifecycle == "CLOSED":
            queue_status, next_action = "CLOSED", "NONE"
        elif lifecycle == "CANCELLED":
            queue_status, next_action = "CANCELLED", "NONE"
        else:
            queue_status, next_action = "TERMINATED_EARLY", "REVIEW_CENSORING_METADATA"

        entries.append(
            {
                "plan_id": plan.plan_id,
                "person_key": plan.person_key,
                "window_start": plan.window_start.isoformat(),
                "window_end": plan.window_end.isoformat(),
                "window_status": lifecycle,
                "followup_status": state["followup_status"],
                "queue_status": queue_status,
                "next_action": next_action,
                "followup_summary": deepcopy(state.get("followup_summary")),
            }
        )

    return sorted(
        entries,
        key=lambda item: (
            item["window_start"],
            item["window_end"],
            item["plan_id"],
        ),
    )

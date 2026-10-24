"""PL7-Q3 in-memory gate for LLM-proposed observation candidates.

This module does not call an LLM, access the network, or persist input. An
upstream model may propose a candidate, but the candidate remains untrusted
until a separate caller-supplied user confirmation and the existing
deterministic v0.2 check-in bridge both accept it.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any, Mapping

from .checkin_observation_bridge_v02 import (
    bridge_checkin_response_v02,
    normalize_event_time_report,
)
from .longitudinal_observation import CONFIDENCE_LEVELS
from .prospective_checkin import (
    CHECKIN_ANSWERS,
    classify_checkin_answer,
    ProspectiveCheckinPlan,
)


CANDIDATE_SCHEMA_VERSION = "0.1"
CANDIDATE_DISPOSITIONS = frozenset(
    {
        "NEEDS_USER_CONFIRMATION",
        "OBSERVATION_READY",
        "NO_EVENT_YET",
        "NO_OBSERVATION",
        "NEEDS_EVENT_TIME_DETAIL",
        "TEMPORAL_ASSIGNMENT_AMBIGUOUS",
    }
)
_ALLOWED_CANDIDATE_KEYS = frozenset(
    {
        "schema_version",
        "candidate_id",
        "plan_id",
        "target_id",
        "checkpoint_id",
        "answer",
        "response_date",
        "event_time_report",
        "evidence_span",
        # These untrusted model fields are accepted for compatibility but ignored.
        "user_confirmed",
        "model_confidence",
    }
)
_FORBIDDEN_TEXT_KEYS = frozenset(
    {"raw_text", "source_text", "narrative", "evidence_text", "quote_text"}
)


def _required_text(value: Any, field: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise ValueError(f"{field} is required")
    return text


def _iso_date(value: Any, field: str) -> date:
    text = _required_text(value, field)
    try:
        parsed = date.fromisoformat(text)
    except ValueError as exc:
        raise ValueError(f"{field} must be ISO YYYY-MM-DD") from exc
    if parsed.isoformat() != text:
        raise ValueError(f"{field} must use canonical ISO YYYY-MM-DD")
    return parsed


def _locked_target(plan: ProspectiveCheckinPlan, target_id: str):
    for target in plan.targets:
        if target.target_id == target_id:
            return target
    raise ValueError(f"target_id not present in locked plan: {target_id}")


def _locked_checkpoint(plan: ProspectiveCheckinPlan, checkpoint_id: str):
    for checkpoint in plan.schedule:
        if checkpoint.checkpoint_id == checkpoint_id:
            return checkpoint
    raise ValueError(f"checkpoint_id not present in locked plan: {checkpoint_id}")


def _validate_evidence_span(
    source_text: str, evidence_span: Any
) -> tuple[int, int]:
    if not isinstance(evidence_span, Mapping):
        raise ValueError("evidence_span must be an object")
    if set(evidence_span) != {"start", "end", "quote"}:
        raise ValueError("evidence_span must contain exactly start, end, and quote")

    start = evidence_span.get("start")
    end = evidence_span.get("end")
    quote = evidence_span.get("quote")
    if isinstance(start, bool) or not isinstance(start, int):
        raise ValueError("evidence_span.start must be an integer")
    if isinstance(end, bool) or not isinstance(end, int):
        raise ValueError("evidence_span.end must be an integer")
    if start < 0 or end <= start or end > len(source_text):
        raise ValueError("evidence_span offsets are outside source_text")
    if not isinstance(quote, str) or not quote.strip():
        raise ValueError("evidence_span.quote is required")
    if source_text[start:end] != quote:
        raise ValueError("evidence_span.quote must exactly match source_text offsets")
    return start, end


@dataclass(frozen=True)
class RawTextObservationCandidate:
    """Normalized candidate with no narrative text or quoted span retained."""

    candidate_id: str
    plan_id: str
    target_id: str
    checkpoint_id: str
    answer: str
    candidate_status: str
    response_date: str
    event_time: Mapping[str, str] | None
    evidence_start: int
    evidence_end: int

    def as_dict(self) -> dict[str, Any]:
        """Return a review-safe view; source text and quoted evidence are omitted."""
        return {
            "schema_version": CANDIDATE_SCHEMA_VERSION,
            "candidate_id": self.candidate_id,
            "plan_id": self.plan_id,
            "target_id": self.target_id,
            "checkpoint_id": self.checkpoint_id,
            "answer": self.answer,
            "candidate_status": self.candidate_status,
            "response_date": self.response_date,
            "event_time": dict(self.event_time) if self.event_time is not None else None,
            "evidence_span": {
                "start": self.evidence_start,
                "end": self.evidence_end,
            },
        }


@dataclass(frozen=True)
class RawTextCandidateGateResult:
    disposition: str
    candidate: RawTextObservationCandidate
    observation_payload: Mapping[str, Any] | None = None
    normalized_event_time: Mapping[str, str] | None = None

    def __post_init__(self) -> None:
        if self.disposition not in CANDIDATE_DISPOSITIONS:
            raise ValueError(f"unsupported candidate gate disposition: {self.disposition}")

    def as_dict(self) -> dict[str, Any]:
        return {
            "disposition": self.disposition,
            "candidate": self.candidate.as_dict(),
            "observation_payload": (
                dict(self.observation_payload)
                if self.observation_payload is not None
                else None
            ),
            "normalized_event_time": (
                dict(self.normalized_event_time)
                if self.normalized_event_time is not None
                else None
            ),
        }


def review_raw_text_candidate(
    plan: ProspectiveCheckinPlan,
    source_text: str,
    candidate_payload: Mapping[str, Any],
) -> RawTextCandidateGateResult:
    """Validate an upstream candidate and return it pending user confirmation.

    source_text is used only in this call to verify an exact quoted span. It is
    not copied into the result, logged, or persisted by this pure function.
    A model-provided user_confirmed flag is intentionally ignored.
    """
    if not isinstance(source_text, str) or not source_text.strip():
        raise ValueError("source_text is required for transient span verification")
    if not isinstance(candidate_payload, Mapping):
        raise ValueError("candidate_payload must be an object")
    forbidden = _FORBIDDEN_TEXT_KEYS.intersection(candidate_payload)
    if forbidden:
        raise ValueError(
            "candidate_payload must not duplicate raw narrative fields: "
            + ", ".join(sorted(forbidden))
        )
    unknown = set(candidate_payload).difference(_ALLOWED_CANDIDATE_KEYS)
    if unknown:
        raise ValueError(
            "unsupported candidate fields: " + ", ".join(sorted(str(x) for x in unknown))
        )
    if str(candidate_payload.get("schema_version", "")).strip() != CANDIDATE_SCHEMA_VERSION:
        raise ValueError(f"schema_version must be {CANDIDATE_SCHEMA_VERSION}")

    candidate_id = _required_text(candidate_payload.get("candidate_id"), "candidate_id")
    plan_id = _required_text(candidate_payload.get("plan_id"), "plan_id")
    if plan_id != plan.plan_id:
        raise ValueError("candidate plan_id does not match locked plan")

    target_id = _required_text(candidate_payload.get("target_id"), "target_id")
    checkpoint_id = _required_text(
        candidate_payload.get("checkpoint_id"), "checkpoint_id"
    )
    _locked_target(plan, target_id)
    checkpoint = _locked_checkpoint(plan, checkpoint_id)

    answer = _required_text(candidate_payload.get("answer"), "answer")
    if answer not in CHECKIN_ANSWERS:
        raise ValueError(f"unsupported check-in answer: {answer}")
    candidate_status = classify_checkin_answer(checkpoint.checkpoint_type, answer)

    response_date = _required_text(candidate_payload.get("response_date"), "response_date")
    _iso_date(response_date, "response_date")

    evidence_start, evidence_end = _validate_evidence_span(
        source_text, candidate_payload.get("evidence_span")
    )

    raw_event_time = candidate_payload.get("event_time_report")
    normalized_event_time: dict[str, str] | None = None
    if raw_event_time is not None:
        if candidate_status != "EVENT_OCCURRED_CANDIDATE":
            raise ValueError("only an event-occurred candidate may carry event_time_report")
        normalized_event_time = normalize_event_time_report(raw_event_time)

    candidate = RawTextObservationCandidate(
        candidate_id=candidate_id,
        plan_id=plan_id,
        target_id=target_id,
        checkpoint_id=checkpoint_id,
        answer=answer,
        candidate_status=candidate_status,
        response_date=response_date,
        event_time=normalized_event_time,
        evidence_start=evidence_start,
        evidence_end=evidence_end,
    )
    return RawTextCandidateGateResult(
        disposition="NEEDS_USER_CONFIRMATION",
        candidate=candidate,
        observation_payload=None,
        normalized_event_time=normalized_event_time,
    )


def _bridge_event_time_report(
    event_time: Mapping[str, str] | None,
) -> dict[str, str] | None:
    if event_time is None:
        return None
    precision = event_time["precision"]
    lower = event_time["lower_bound_date"]
    upper = event_time["upper_bound_date"]
    if precision == "DAY":
        return {"precision": "DAY", "value": lower}
    if precision == "MONTH":
        return {"precision": "MONTH", "value": lower[:7]}
    if precision == "YEAR":
        return {"precision": "YEAR", "value": lower[:4]}
    if precision == "INTERVAL":
        return {
            "precision": "INTERVAL",
            "lower_bound_date": lower,
            "upper_bound_date": upper,
        }
    raise ValueError(f"unsupported normalized event-time precision: {precision}")


def confirm_raw_text_candidate(
    plan: ProspectiveCheckinPlan,
    source_text: str,
    candidate_payload: Mapping[str, Any],
    *,
    user_confirmed: bool,
    record_id: str | None = None,
    observation_confidence: str | None = None,
) -> RawTextCandidateGateResult:
    """Apply an explicit confirmation and delegate conversion to the v0.2 bridge.

    Confirmation is a separate argument, never a field trusted from model output.
    A confirmed result still cannot bypass the locked plan, event-time checks,
    window semantics, or confidence vocabulary enforced by deterministic code.
    """
    reviewed = review_raw_text_candidate(plan, source_text, candidate_payload)
    candidate = reviewed.candidate
    if not user_confirmed:
        return reviewed

    resolved_record_id = _required_text(record_id, "record_id")
    resolved_confidence = _required_text(
        observation_confidence, "observation_confidence"
    )
    if resolved_confidence not in CONFIDENCE_LEVELS:
        raise ValueError(
            "observation_confidence must be one of: "
            + ", ".join(sorted(CONFIDENCE_LEVELS))
        )

    response = {
        "schema_version": "0.2",
        "record_id": resolved_record_id,
        "plan_id": candidate.plan_id,
        "target_id": candidate.target_id,
        "checkpoint_id": candidate.checkpoint_id,
        "answer": candidate.answer,
        "response_date": candidate.response_date,
        "user_confirmed": True,
        "event_time_report": _bridge_event_time_report(candidate.event_time),
        "severity": None,
        "duration_days": None,
        "actions": [],
        "context": {
            "exposures": [],
            "external_factors": [],
            "counterparty_factors": [],
        },
        "observation": {
            "source_type": "USER_SELF_REPORT",
            "confidence": resolved_confidence,
            "notes_ref": None,
        },
    }
    bridge_result = bridge_checkin_response_v02(plan, response)
    return RawTextCandidateGateResult(
        disposition=bridge_result.disposition,
        candidate=candidate,
        observation_payload=bridge_result.observation_payload,
        normalized_event_time=bridge_result.normalized_event_time,
    )

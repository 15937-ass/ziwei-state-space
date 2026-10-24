import json
from pathlib import Path

import pytest

from src.product.prospective_checkin import compile_prospective_checkin_plan
from src.product.raw_text_candidate_gate import (
    confirm_raw_text_candidate,
    review_raw_text_candidate,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "product" / "PL7_PROSPECTIVE_CHECKIN_FIXTURES_v0.1.json"


def _plan():
    payload = json.loads(FIXTURES.read_text(encoding="utf-8"))["fixtures"][0]
    return compile_prospective_checkin_plan(payload)


def _mid_checkpoint(plan):
    return next(item for item in plan.schedule if item.checkpoint_type == "MID_WINDOW")


def _candidate(plan, source_text="I changed jobs in May 2027.", **overrides):
    quote = "changed jobs in May 2027"
    start = source_text.index(quote)
    checkpoint = _mid_checkpoint(plan)
    payload = {
        "schema_version": "0.1",
        "candidate_id": "CANDIDATE-001",
        "plan_id": plan.plan_id,
        "target_id": plan.targets[0].target_id,
        "checkpoint_id": checkpoint.checkpoint_id,
        "answer": "YES",
        "response_date": checkpoint.scheduled_date.isoformat(),
        "event_time_report": {"precision": "MONTH", "value": "2027-05"},
        "evidence_span": {"start": start, "end": start + len(quote), "quote": quote},
        # Neither field is trusted or copied into the normalized candidate.
        "user_confirmed": True,
        "model_confidence": 0.99,
    }
    payload.update(overrides)
    return payload, source_text


def test_candidate_stays_pending_even_if_model_claims_user_confirmation():
    plan = _plan()
    payload, source_text = _candidate(plan)

    result = review_raw_text_candidate(plan, source_text, payload)

    assert result.disposition == "NEEDS_USER_CONFIRMATION"
    assert result.observation_payload is None
    normalized = json.dumps(result.as_dict(), ensure_ascii=False)
    assert source_text not in normalized
    assert "changed jobs in May 2027" not in normalized
    assert "user_confirmed" not in normalized
    assert "model_confidence" not in normalized


def test_explicit_confirmation_uses_existing_bridge_and_produces_bounded_observation():
    plan = _plan()
    payload, source_text = _candidate(plan)

    result = confirm_raw_text_candidate(
        plan,
        source_text,
        payload,
        user_confirmed=True,
        record_id="OBS-RAW-TEXT-001",
        observation_confidence="MEDIUM",
    )

    assert result.disposition == "OBSERVATION_READY"
    assert result.observation_payload["schema_version"] == "0.2"
    assert result.observation_payload["outcome"]["event_time"]["precision"] == "MONTH"
    assert result.observation_payload["record_id"] == "OBS-RAW-TEXT-001"
    normalized = json.dumps(result.as_dict(), ensure_ascii=False)
    assert source_text not in normalized
    assert "changed jobs in May 2027" not in normalized


def test_separate_confirmation_argument_is_required():
    plan = _plan()
    payload, source_text = _candidate(plan)

    result = confirm_raw_text_candidate(
        plan, source_text, payload, user_confirmed=False
    )

    assert result.disposition == "NEEDS_USER_CONFIRMATION"
    assert result.observation_payload is None


def test_missing_event_time_remains_unresolved_after_confirmation():
    plan = _plan()
    payload, source_text = _candidate(plan, event_time_report=None)

    result = confirm_raw_text_candidate(
        plan,
        source_text,
        payload,
        user_confirmed=True,
        record_id="OBS-RAW-TEXT-NO-TIME",
        observation_confidence="MEDIUM",
    )

    assert result.disposition == "NEEDS_EVENT_TIME_DETAIL"
    assert result.observation_payload is None


def test_partial_interval_overlap_remains_ambiguous():
    plan = _plan()
    object.__setattr__(plan, "window_start", __import__("datetime").date(2027, 4, 1))
    object.__setattr__(plan, "window_end", __import__("datetime").date(2027, 6, 30))
    source_text = "My job changed sometime in the first half of 2027."
    quote = "changed sometime in the first half of 2027"
    start = source_text.index(quote)
    checkpoint = _mid_checkpoint(plan)
    payload, _ = _candidate(
        plan,
        source_text=source_text,
        event_time_report={
            "precision": "INTERVAL",
            "lower_bound_date": "2027-01-01",
            "upper_bound_date": "2027-06-30",
        },
        response_date="2027-06-30",
        evidence_span={"start": start, "end": start + len(quote), "quote": quote},
    )

    result = confirm_raw_text_candidate(
        plan,
        source_text,
        payload,
        user_confirmed=True,
        record_id="OBS-RAW-TEXT-AMBIGUOUS",
        observation_confidence="MEDIUM",
    )

    assert result.disposition == "TEMPORAL_ASSIGNMENT_AMBIGUOUS"
    assert result.observation_payload is None


def test_mid_window_no_does_not_become_a_closed_negative():
    plan = _plan()
    source_text = "No, the event has not happened yet."
    quote = "the event has not happened yet"
    start = source_text.index(quote)
    checkpoint = _mid_checkpoint(plan)
    payload, _ = _candidate(
        plan,
        source_text=source_text,
        answer="NO",
        response_date=checkpoint.scheduled_date.isoformat(),
        event_time_report=None,
        evidence_span={"start": start, "end": start + len(quote), "quote": quote},
    )

    result = confirm_raw_text_candidate(
        plan,
        source_text,
        payload,
        user_confirmed=True,
        record_id="OBS-RAW-TEXT-MID-NO",
        observation_confidence="INSUFFICIENT",
    )

    assert result.disposition == "NO_EVENT_YET"
    assert result.observation_payload is None


def test_no_response_is_not_converted_to_event_not_occurred():
    plan = _plan()
    source_text = "No response was received for this check-in."
    quote = "No response was received"
    start = source_text.index(quote)
    checkpoint = _mid_checkpoint(plan)
    payload, _ = _candidate(
        plan,
        source_text=source_text,
        answer="NO_RESPONSE",
        response_date=checkpoint.scheduled_date.isoformat(),
        event_time_report=None,
        evidence_span={"start": start, "end": start + len(quote), "quote": quote},
    )

    result = confirm_raw_text_candidate(
        plan,
        source_text,
        payload,
        user_confirmed=True,
        record_id="OBS-RAW-TEXT-NO-RESPONSE",
        observation_confidence="INSUFFICIENT",
    )

    assert result.disposition == "NO_OBSERVATION"
    assert result.observation_payload is None


def test_window_close_no_before_window_end_is_rejected_by_existing_bridge():
    plan = _plan()
    source_text = "No, the event did not happen during the window."
    quote = "the event did not happen during the window"
    start = source_text.index(quote)
    close = next(item for item in plan.schedule if item.checkpoint_type == "WINDOW_CLOSE")
    payload, _ = _candidate(
        plan,
        source_text=source_text,
        checkpoint_id=close.checkpoint_id,
        answer="NO",
        response_date="2027-06-30",
        event_time_report=None,
        evidence_span={"start": start, "end": start + len(quote), "quote": quote},
    )

    with pytest.raises(ValueError, match="window end"):
        confirm_raw_text_candidate(
            plan,
            source_text,
            payload,
            user_confirmed=True,
            record_id="OBS-RAW-TEXT-EARLY-NEGATIVE",
            observation_confidence="MEDIUM",
        )


def test_exact_evidence_span_is_required_and_never_returned():
    plan = _plan()
    payload, source_text = _candidate(plan)
    payload["evidence_span"]["quote"] = "invented evidence"

    with pytest.raises(ValueError, match="exactly match"):
        review_raw_text_candidate(plan, source_text, payload)


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("target_id", "NOT-IN-PLAN", "target_id not present"),
        ("checkpoint_id", "NOT-IN-PLAN", "checkpoint_id not present"),
        ("answer", "MAYBE", "unsupported check-in answer"),
        ("response_date", "2027-6-30", "ISO YYYY-MM-DD"),
    ],
)
def test_invalid_candidate_fields_fail_closed(field, value, message):
    plan = _plan()
    payload, source_text = _candidate(plan)
    payload[field] = value

    with pytest.raises(ValueError, match=message):
        review_raw_text_candidate(plan, source_text, payload)


def test_plan_mismatch_and_narrative_duplication_are_rejected():
    plan = _plan()
    payload, source_text = _candidate(plan)
    payload["plan_id"] = "OTHER-PLAN"
    with pytest.raises(ValueError, match="does not match locked plan"):
        review_raw_text_candidate(plan, source_text, payload)

    payload, source_text = _candidate(plan)
    payload["raw_text"] = source_text
    with pytest.raises(ValueError, match="must not duplicate raw narrative"):
        review_raw_text_candidate(plan, source_text, payload)


def test_event_time_cannot_be_attached_to_non_event_answer():
    plan = _plan()
    payload, source_text = _candidate(plan, answer="NO")
    with pytest.raises(ValueError, match="only an event-occurred candidate"):
        review_raw_text_candidate(plan, source_text, payload)


def test_observation_confidence_must_come_from_confirmation_and_allowed_vocabulary():
    plan = _plan()
    payload, source_text = _candidate(plan)
    with pytest.raises(ValueError, match="observation_confidence must be one of"):
        confirm_raw_text_candidate(
            plan,
            source_text,
            payload,
            user_confirmed=True,
            record_id="OBS-RAW-TEXT-BAD-CONFIDENCE",
            observation_confidence="0.99",
        )


def test_candidate_without_evidence_or_candidate_payload_never_defaults_to_no_event():
    plan = _plan()
    payload, source_text = _candidate(plan)
    payload.pop("evidence_span")
    with pytest.raises(ValueError, match="evidence_span"):
        review_raw_text_candidate(plan, source_text, payload)

    with pytest.raises(ValueError, match="candidate_payload must be an object"):
        review_raw_text_candidate(plan, source_text, None)

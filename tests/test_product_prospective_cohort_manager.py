import copy
import json
from pathlib import Path

import pytest

from src.product.prospective_cohort_manager import (
    build_prospective_cohort_queue,
    cancel_prospective_cohort_window,
    close_prospective_cohort_window,
    open_prospective_cohort_window,
    register_prospective_cohort_window,
    terminate_prospective_cohort_followup,
)

ROOT = Path(__file__).resolve().parents[1]
PLANS_PATH = ROOT / "product" / "PL7_PROSPECTIVE_CHECKIN_FIXTURES_v0.1.json"


def _plans():
    return json.loads(PLANS_PATH.read_text(encoding="utf-8"))["fixtures"]


def _response(plan, target_id, answer="NO", *, record_id=None, **overrides):
    payload = {
        "schema_version": "0.2",
        "record_id": record_id or f"RESP-{plan['plan_id']}-{target_id}-CLOSE",
        "plan_id": plan["plan_id"],
        "target_id": target_id,
        "checkpoint_id": "CLOSE",
        "answer": answer,
        "response_date": plan["window"]["end_date"],
        "user_confirmed": True,
        "event_time_report": None,
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
            "confidence": "HIGH",
            "notes_ref": None,
        },
    }
    payload.update(overrides)
    return payload


def _complete_responses(plan):
    return [
        _response(plan, target["target_id"])
        for target in plan["targets"]
    ]


def test_register_validates_and_preserves_locked_plan_without_outcome_fields():
    plan = copy.deepcopy(_plans()[0])
    state = register_prospective_cohort_window(plan)

    assert state["schema_version"] == "0.1"
    assert state["plan_id"] == plan["plan_id"]
    assert state["window_status"] == "PLANNED"
    assert state["followup_status"] == "NOT_STARTED"
    assert state["window"] == plan["window"]
    assert "event_status" not in state
    assert "outcome" not in state
    assert state["plan"] == plan


def test_registration_rejects_outcome_leakage():
    plan = copy.deepcopy(_plans()[0])
    plan["outcome"] = {"event_status": "EVENT_OCCURRED"}
    with pytest.raises(ValueError, match="outcome leakage"):
        register_prospective_cohort_window(plan)


def test_locked_plan_provenance_cannot_be_silently_rewritten():
    plan = copy.deepcopy(_plans()[0])
    state = register_prospective_cohort_window(plan)
    changed = copy.deepcopy(state)
    changed["plan"]["targets"][0]["event_type"] = "silently_rewritten_event"

    with pytest.raises(ValueError, match="locked plan digest mismatch"):
        open_prospective_cohort_window(changed, on_date=plan["window"]["start_date"])


def test_open_window_requires_date_inside_locked_window_and_does_not_mutate_input():
    plan = _plans()[0]
    state = register_prospective_cohort_window(plan)
    original = copy.deepcopy(state)
    opened = open_prospective_cohort_window(state, on_date=plan["window"]["start_date"])

    assert opened["window_status"] == "OPEN"
    assert opened["followup_status"] == "IN_PROGRESS"
    assert opened["opened_date"] == plan["window"]["start_date"]
    assert state == original

    with pytest.raises(ValueError, match="before window.start_date"):
        open_prospective_cohort_window(state, on_date="2026-12-31")
    with pytest.raises(ValueError, match="after window.end_date"):
        open_prospective_cohort_window(state, on_date="2028-01-01")
    with pytest.raises(ValueError, match="only a PLANNED"):
        open_prospective_cohort_window(opened, on_date=plan["window"]["start_date"])


def test_close_window_requires_end_date_and_records_complete_followup():
    plan = _plans()[0]
    state = register_prospective_cohort_window(plan)
    opened = open_prospective_cohort_window(state, on_date=plan["window"]["start_date"])

    with pytest.raises(ValueError, match="before window.end_date"):
        close_prospective_cohort_window(
            opened, on_date="2027-12-30", checkin_responses=_complete_responses(plan)
        )

    closed = close_prospective_cohort_window(
        opened, on_date=plan["window"]["end_date"], checkin_responses=_complete_responses(plan)
    )
    assert closed["window_status"] == "CLOSED"
    assert closed["followup_status"] == "COMPLETE"
    assert closed["followup_summary"]["expected_window_close_responses"] == 2
    assert closed["followup_summary"]["complete_window_close_responses"] == 2
    assert closed["followup_summary"]["missing_window_close_responses"] == 0
    assert "event_status" not in closed
    assert "outcome" not in closed


def test_missed_window_can_be_closed_administratively_but_remains_incomplete():
    plan = _plans()[0]
    state = register_prospective_cohort_window(plan)
    closed = close_prospective_cohort_window(state, on_date="2028-01-02")

    assert closed["window_status"] == "CLOSED"
    assert closed["opened_date"] is None
    assert closed["followup_status"] == "INCOMPLETE"
    assert closed["followup_summary"]["missing_window_close_responses"] == 2
    assert "EVENT_NOT_OCCURRED" not in closed["followup_summary"]["finding_codes"]


def test_no_response_and_duplicate_closeouts_remain_incomplete_not_negative():
    plan = _plans()[1]
    state = register_prospective_cohort_window(plan)
    opened = open_prospective_cohort_window(state, on_date=plan["window"]["start_date"])
    no_response = _response(plan, plan["targets"][0]["target_id"], answer="NO_RESPONSE")
    closed = close_prospective_cohort_window(
        opened, on_date=plan["window"]["end_date"], checkin_responses=[no_response]
    )
    assert closed["followup_status"] == "INCOMPLETE"
    assert closed["followup_summary"]["window_close_no_response"] == 1
    assert closed["followup_summary"]["unresolved_window_close_responses"] == 1
    assert "EVENT_NOT_OCCURRED" not in closed["followup_summary"]["finding_codes"]

    first = _response(plan, plan["targets"][0]["target_id"], record_id="RESP-DUP-1")
    second = _response(plan, plan["targets"][0]["target_id"], record_id="RESP-DUP-2")
    duplicate_close = close_prospective_cohort_window(
        opened, on_date=plan["window"]["end_date"], checkin_responses=[first, second]
    )
    assert duplicate_close["followup_status"] == "INCOMPLETE"
    assert "DUPLICATE_PLAN_TARGET_CHECKPOINT_RESPONSE" in duplicate_close["followup_summary"]["finding_codes"]


def test_early_dropout_requires_reason_and_observed_through_within_observed_period():
    plan = _plans()[0]
    state = register_prospective_cohort_window(plan)
    opened = open_prospective_cohort_window(state, on_date=plan["window"]["start_date"])
    termination_date = "2027-03-01"

    with pytest.raises(ValueError, match="reason is required"):
        terminate_prospective_cohort_followup(
            opened,
            on_date=termination_date,
            disposition="LOST_TO_FOLLOW_UP",
            reason=" ",
            observed_through="2027-02-20",
        )
    with pytest.raises(ValueError, match="no later than on_date"):
        terminate_prospective_cohort_followup(
            opened,
            on_date=termination_date,
            disposition="WITHDRAWN",
            reason="participant withdrew",
            observed_through="2027-03-02",
        )

    terminated = terminate_prospective_cohort_followup(
        opened,
        on_date=termination_date,
        disposition="LOST_TO_FOLLOW_UP",
        reason="no response after repeated follow-up",
        observed_through="2027-02-20",
    )
    assert terminated["window_status"] == "TERMINATED_EARLY"
    assert terminated["followup_status"] == "LOST_TO_FOLLOW_UP"
    assert terminated["termination"]["observed_through"] == "2027-02-20"
    assert terminated["termination"]["censor_reason"] == "no response after repeated follow-up"
    assert "event_status" not in terminated
    assert "outcome" not in terminated


def test_cancellation_is_only_allowed_before_window_start():
    plan = _plans()[0]
    state = register_prospective_cohort_window(plan)
    cancelled = cancel_prospective_cohort_window(
        state, on_date="2026-12-25", reason="cohort launch postponed"
    )
    assert cancelled["window_status"] == "CANCELLED"
    assert cancelled["cancellation"]["reason"] == "cohort launch postponed"
    with pytest.raises(ValueError, match="before window.start_date"):
        cancel_prospective_cohort_window(
            state, on_date=plan["window"]["start_date"], reason="too late"
        )


def test_queue_snapshot_is_sorted_deterministic_and_does_not_mutate_states():
    plans = _plans()
    first = register_prospective_cohort_window(plans[0])
    second = register_prospective_cohort_window(plans[1])
    opened_second = open_prospective_cohort_window(
        second, on_date=plans[1]["window"]["start_date"]
    )
    states = [first, opened_second]
    before = copy.deepcopy(states)

    queue = build_prospective_cohort_queue(states, as_of_date="2027-07-01")
    repeated = build_prospective_cohort_queue(states, as_of_date="2027-07-01")

    assert queue == repeated
    assert states == before
    assert [item["plan_id"] for item in queue] == [
        "CP-FX-PERS-001",
        "CP-FX-BLIND-001",
    ]
    assert queue[0]["queue_status"] == "CLOSE_DUE"
    assert queue[0]["next_action"] == "CLOSE_WINDOW_AND_AUDIT_FOLLOW_UP"
    assert queue[1]["queue_status"] == "OPEN_DUE"
    assert queue[1]["next_action"] == "OPEN_WINDOW"


def test_queue_rejects_duplicate_plan_ids():
    state = register_prospective_cohort_window(_plans()[0])
    with pytest.raises(ValueError, match="duplicate plan_id"):
        build_prospective_cohort_queue([state, copy.deepcopy(state)], as_of_date="2027-01-01")

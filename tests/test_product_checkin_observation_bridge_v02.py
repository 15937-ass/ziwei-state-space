import json
from pathlib import Path

from src.product.prospective_checkin import compile_prospective_checkin_plan
from src.product.checkin_observation_bridge_v02 import (
    bridge_checkin_response_v02,
    normalize_event_time_report,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "product/PL7_PROSPECTIVE_CHECKIN_FIXTURES_v0.1.json"


def _plan():
    payload = json.loads(FIXTURES.read_text(encoding="utf-8"))["fixtures"][0]
    return compile_prospective_checkin_plan(payload)


def _response(answer, checkpoint_id, response_date):
    return {
        "schema_version": "0.2",
        "record_id": "LO-BRIDGE-V02-1",
        "plan_id": "CP-FX-BLIND-001",
        "target_id": "T-CAR-CHANGE",
        "checkpoint_id": checkpoint_id,
        "answer": answer,
        "response_date": response_date,
        "user_confirmed": True,
        "event_time_report": None,
        "severity": None,
        "duration_days": None,
        "actions": [],
        "context": {"exposures": [], "external_factors": [], "counterparty_factors": []},
        "observation": {"source_type": "USER_SELF_REPORT", "confidence": "HIGH", "notes_ref": None},
    }


def test_month_report_normalizes_to_calendar_bounds():
    normalized = normalize_event_time_report({"precision": "MONTH", "value": "2027-05"})
    assert normalized == {"precision": "MONTH", "lower_bound_date": "2027-05-01", "upper_bound_date": "2027-05-31"}


def test_year_report_normalizes_without_fabricated_day():
    normalized = normalize_event_time_report({"precision": "YEAR", "value": "2027"})
    assert normalized["lower_bound_date"] == "2027-01-01"
    assert normalized["upper_bound_date"] == "2027-12-31"


def test_month_event_creates_v02_observation():
    response = _response("YES", "Q2", "2027-06-30")
    response["event_time_report"] = {"precision": "MONTH", "value": "2027-05"}
    result = bridge_checkin_response_v02(_plan(), response)
    assert result.disposition == "OBSERVATION_READY"
    assert result.observation_payload["schema_version"] == "0.2"
    assert result.observation_payload["outcome"]["event_time"]["precision"] == "MONTH"


def test_year_event_is_valid_for_full_year_target():
    response = _response("YES", "CLOSE", "2028-01-02")
    response["event_time_report"] = {"precision": "YEAR", "value": "2027"}
    result = bridge_checkin_response_v02(_plan(), response)
    assert result.disposition == "OBSERVATION_READY"


def test_partial_overlap_returns_ambiguous_instead_of_positive_truth():
    plan = _plan()
    # Build a 2027-year report but narrow the locked plan locally by replacing dates.
    object.__setattr__(plan, "window_start", __import__("datetime").date(2027, 4, 1))
    object.__setattr__(plan, "window_end", __import__("datetime").date(2027, 6, 30))
    response = _response("YES", "Q2", "2027-06-30")
    response["event_time_report"] = {"precision": "YEAR", "value": "2027"}
    result = bridge_checkin_response_v02(plan, response)
    assert result.disposition == "TEMPORAL_ASSIGNMENT_AMBIGUOUS"
    assert result.observation_payload is None


def test_midwindow_no_stays_nonnegative():
    result = bridge_checkin_response_v02(_plan(), _response("NO", "Q2", "2027-06-30"))
    assert result.disposition == "NO_EVENT_YET"


def test_unconfirmed_month_report_cannot_enter_ground_truth():
    response = _response("YES", "Q2", "2027-06-30")
    response["event_time_report"] = {"precision": "MONTH", "value": "2027-05"}
    response["user_confirmed"] = False
    result = bridge_checkin_response_v02(_plan(), response)
    assert result.disposition == "NEEDS_USER_CONFIRMATION"

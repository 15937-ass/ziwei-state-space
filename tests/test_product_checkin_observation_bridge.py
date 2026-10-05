import json
from pathlib import Path

from src.product.prospective_checkin import compile_prospective_checkin_plan
from src.product.checkin_observation_bridge import bridge_checkin_response

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "product/PL7_PROSPECTIVE_CHECKIN_FIXTURES_v0.1.json"


def _plan(index=0):
    payload = json.loads(FIXTURES.read_text(encoding="utf-8"))["fixtures"][index]
    return compile_prospective_checkin_plan(payload)


def _base_response(answer, checkpoint_id, response_date):
    return {
        "schema_version": "0.1",
        "record_id": "LO-BRIDGE-1",
        "plan_id": "CP-FX-BLIND-001",
        "target_id": "T-CAR-CHANGE",
        "checkpoint_id": checkpoint_id,
        "answer": answer,
        "response_date": response_date,
        "user_confirmed": True,
        "event_date": None,
        "severity": None,
        "duration_days": None,
        "actions": [],
        "context": {"exposures": [], "external_factors": [], "counterparty_factors": []},
        "observation": {"source_type": "USER_SELF_REPORT", "confidence": "HIGH", "notes_ref": None},
    }


def test_midwindow_no_does_not_create_observation():
    result = bridge_checkin_response(_plan(), _base_response("NO", "Q2", "2027-06-30"))
    assert result.disposition == "NO_EVENT_YET"
    assert result.observation_payload is None


def test_window_close_no_creates_closed_negative():
    result = bridge_checkin_response(_plan(), _base_response("NO", "CLOSE", "2028-01-02"))
    assert result.disposition == "OBSERVATION_READY"
    assert result.observation_payload["outcome"]["status"] == "EVENT_NOT_OCCURRED"
    assert result.observation_payload["model_linkage"]["forecast"]["mode"] == "BLIND"


def test_yes_without_event_date_is_not_fabricated():
    result = bridge_checkin_response(_plan(), _base_response("YES", "Q2", "2027-06-30"))
    assert result.disposition == "NEEDS_EVENT_DATE_DETAIL"
    assert result.observation_payload is None


def test_yes_with_event_date_creates_event_observation():
    response = _base_response("YES", "Q2", "2027-06-30")
    response["event_date"] = "2027-05-12"
    result = bridge_checkin_response(_plan(), response)
    assert result.disposition == "OBSERVATION_READY"
    assert result.observation_payload["outcome"]["status"] == "EVENT_OCCURRED"
    assert result.observation_payload["outcome"]["event_date"] == "2027-05-12"


def test_unconfirmed_parser_candidate_cannot_enter_ground_truth():
    response = _base_response("YES", "Q2", "2027-06-30")
    response["event_date"] = "2027-05-12"
    response["user_confirmed"] = False
    result = bridge_checkin_response(_plan(), response)
    assert result.disposition == "NEEDS_USER_CONFIRMATION"
    assert result.observation_payload is None


def test_unsure_becomes_unknown_not_negative():
    result = bridge_checkin_response(_plan(), _base_response("UNSURE", "CLOSE", "2028-01-02"))
    assert result.disposition == "OBSERVATION_READY"
    assert result.observation_payload["outcome"]["status"] == "UNKNOWN"

import copy
import json
from pathlib import Path

import pytest

from src.product.acquired_state import compile_acquired_state
from src.product.longitudinal_observation_v02 import compile_longitudinal_observation_v02
from src.product.state_updater import (
    compile_state_update_request,
    update_acquired_state,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "product/PL3S_STATE_UPDATE_FIXTURE_v0.1.json"
STATE_FIXTURE = ROOT / "product/PL3S_ACQUIRED_STATE_FIXTURE_v0.1.json"


def _doc():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def _observation():
    return compile_longitudinal_observation_v02(_doc()["observation"])


def _request():
    return compile_state_update_request(_doc()["update_request"])


def test_event_label_alone_does_not_create_hidden_state_assertion():
    doc = _doc()
    doc["update_request"]["directives"] = []
    report = update_acquired_state(
        None,
        compile_longitudinal_observation_v02(doc["observation"]),
        compile_state_update_request(doc["update_request"]),
    )
    assert report.state.assertions == ()
    assert report.state.actions[0].action_id == "ACT-JOB-SEARCH"
    kinds = {item.kind for item in report.state.context_items}
    assert kinds == {"EXPOSURE", "EXTERNAL", "COUNTERPARTY"}


def test_confirmed_directive_creates_state_assertion():
    report = update_acquired_state(None, _observation(), _request())
    assert len(report.state.assertions) == 1
    fact = report.state.assertions[0]
    assert fact.domain == "CAREER"
    assert fact.key == "employment_status"
    assert fact.value == "EMPLOYED"
    assert report.applied_directive_ids == ("DIR-CAREER-001",)


def test_unconfirmed_directive_is_rejected():
    doc = _doc()
    doc["update_request"]["directives"][0]["user_confirmed"] = False
    with pytest.raises(ValueError, match="user_confirmed=true"):
        compile_state_update_request(doc["update_request"])


def test_different_value_without_supersede_creates_conflict():
    previous = compile_acquired_state(
        json.loads(STATE_FIXTURE.read_text(encoding="utf-8"))
    )
    doc = _doc()
    doc["observation"]["person_key"] = previous.person_key
    doc["update_request"]["directives"][0]["value"] = "UNEMPLOYED"
    doc["update_request"]["directives"][0]["supersedes_existing"] = False

    report = update_acquired_state(
        previous,
        compile_longitudinal_observation_v02(doc["observation"]),
        compile_state_update_request(doc["update_request"]),
    )
    assert len(
        [
            item
            for item in report.state.assertions
            if item.domain == "CAREER" and item.key == "employment_status"
        ]
    ) == 2
    assert len(report.state.conflicts) == 1
    assert report.generated_conflict_ids


def test_explicit_supersede_replaces_previous_value():
    previous = compile_acquired_state(
        json.loads(STATE_FIXTURE.read_text(encoding="utf-8"))
    )
    doc = _doc()
    doc["observation"]["person_key"] = previous.person_key
    doc["update_request"]["directives"][0]["value"] = "UNEMPLOYED"
    doc["update_request"]["directives"][0]["supersedes_existing"] = True

    report = update_acquired_state(
        previous,
        compile_longitudinal_observation_v02(doc["observation"]),
        compile_state_update_request(doc["update_request"]),
    )
    values = [
        item.value
        for item in report.state.assertions
        if item.domain == "CAREER" and item.key == "employment_status"
    ]
    assert values == ["UNEMPLOYED"]
    assert not report.state.conflicts


def test_mark_missing_replaces_current_value_with_explicit_missingness():
    previous = compile_acquired_state(
        json.loads(STATE_FIXTURE.read_text(encoding="utf-8"))
    )
    doc = _doc()
    doc["observation"]["person_key"] = previous.person_key
    doc["update_request"]["directives"] = [
        {
            "directive_id": "DIR-MISS-001",
            "observation_ref": "OBS-PL3S-UPDATER-001",
            "operation": "MARK_MISSING",
            "user_confirmed": True,
            "domain": "CAREER",
            "key": "employment_status",
            "value": None,
            "assertion_status": None,
            "confidence": None,
            "valid_from": None,
            "valid_through": None,
            "supersedes_existing": False,
            "missingness_reason": "UNKNOWN",
            "source_note": None,
        }
    ]

    report = update_acquired_state(
        previous,
        compile_longitudinal_observation_v02(doc["observation"]),
        compile_state_update_request(doc["update_request"]),
    )
    assert not [
        item
        for item in report.state.assertions
        if item.domain == "CAREER" and item.key == "employment_status"
    ]
    assert any(
        item.domain == "CAREER"
        and item.key == "employment_status"
        and item.reason == "UNKNOWN"
        for item in report.state.missingness
    )


def test_backdated_observation_requires_replay_not_silent_reordering():
    previous = compile_acquired_state(
        json.loads(STATE_FIXTURE.read_text(encoding="utf-8"))
    )
    doc = _doc()
    doc["observation"]["person_key"] = previous.person_key
    doc["observation"]["observation"]["collected_date"] = "2027-01-01"
    with pytest.raises(ValueError, match="backdated"):
        update_acquired_state(
            previous,
            compile_longitudinal_observation_v02(doc["observation"]),
            compile_state_update_request(doc["update_request"]),
        )


def test_updater_is_deterministic_for_same_input():
    first = update_acquired_state(None, _observation(), _request())
    second = update_acquired_state(None, _observation(), _request())
    assert first.state.state_id == second.state.state_id
    assert first.state.to_dict() == second.state.to_dict()

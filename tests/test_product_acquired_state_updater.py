import json
from pathlib import Path

import pytest

from src.product.acquired_state import compile_acquired_state
from src.product.acquired_state_updater import (
    StateUpdateCommand,
    update_acquired_state,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "product/PL3S_ACQUIRED_STATE_FIXTURE_v0.1.json"


def _previous():
    return compile_acquired_state(json.loads(FIXTURE.read_text(encoding="utf-8")))


def _command(command_id, operation, payload, refs=("OBS-NEW-001",)):
    return StateUpdateCommand(
        command_id=command_id,
        operation=operation,
        payload=payload,
        observation_refs=refs,
    )


def test_add_assertion_preserves_unmodified_previous_state():
    previous = _previous()
    result = update_acquired_state(
        previous,
        as_of_date="2027-07-01",
        new_source_observation_ids=("OBS-NEW-001",),
        commands=(
            _command(
                "CMD-1",
                "ADD_ASSERTION",
                {
                    "fact_id": "SF-REL-001",
                    "domain": "RELATIONSHIP",
                    "key": "relationship_status",
                    "value": "PARTNERED",
                    "status": "CONFIRMED",
                    "confidence": "HIGH",
                    "valid_from": "2027-07-01",
                    "valid_through": None,
                    "observation_refs": ["OBS-NEW-001"],
                    "source_note": None,
                },
            ),
        ),
    )
    assert result.next_state.previous_state_id == previous.state_id
    assert result.next_state.person_key == previous.person_key
    assert "SF-CAREER-001" in result.preserved_assertion_ids
    assert "SF-REL-001" in {item.fact_id for item in result.next_state.assertions}


def test_replace_current_state_requires_explicit_close_then_add():
    previous = _previous()
    result = update_acquired_state(
        previous,
        as_of_date="2027-07-01",
        new_source_observation_ids=("OBS-NEW-001",),
        commands=(
            _command(
                "CMD-CLOSE",
                "CLOSE_ASSERTION",
                {"fact_id": "SF-CAREER-001", "valid_through": "2027-06-30"},
            ),
            _command(
                "CMD-ADD",
                "ADD_ASSERTION",
                {
                    "fact_id": "SF-CAREER-002",
                    "domain": "CAREER",
                    "key": "employment_status",
                    "value": "UNEMPLOYED",
                    "status": "CONFIRMED",
                    "confidence": "HIGH",
                    "valid_from": "2027-07-01",
                    "valid_through": None,
                    "observation_refs": ["OBS-NEW-001"],
                    "source_note": "confirmed transition",
                },
            ),
        ),
    )
    old = next(item for item in result.next_state.assertions if item.fact_id == "SF-CAREER-001")
    new = next(item for item in result.next_state.assertions if item.fact_id == "SF-CAREER-002")
    assert old.valid_through.isoformat() == "2027-06-30"
    assert new.value == "UNEMPLOYED"


def test_conflicting_active_value_fails_without_explicit_conflict():
    previous = _previous()
    with pytest.raises(ValueError, match="explicit ADD_CONFLICT"):
        update_acquired_state(
            previous,
            as_of_date="2027-07-01",
            new_source_observation_ids=("OBS-NEW-001",),
            commands=(
                _command(
                    "CMD-ADD",
                    "ADD_ASSERTION",
                    {
                        "fact_id": "SF-CAREER-X",
                        "domain": "CAREER",
                        "key": "employment_status",
                        "value": "UNEMPLOYED",
                        "status": "REPORTED",
                        "confidence": "MEDIUM",
                        "valid_from": "2027-07-01",
                        "valid_through": None,
                        "observation_refs": ["OBS-NEW-001"],
                        "source_note": None,
                    },
                ),
            ),
        )


def test_explicit_conflict_preserves_both_reports_without_auto_resolution():
    previous = _previous()
    result = update_acquired_state(
        previous,
        as_of_date="2027-07-01",
        new_source_observation_ids=("OBS-NEW-001",),
        commands=(
            _command(
                "CMD-ADD",
                "ADD_ASSERTION",
                {
                    "fact_id": "SF-CAREER-X",
                    "domain": "CAREER",
                    "key": "employment_status",
                    "value": "UNEMPLOYED",
                    "status": "REPORTED",
                    "confidence": "MEDIUM",
                    "valid_from": "2027-07-01",
                    "valid_through": None,
                    "observation_refs": ["OBS-NEW-001"],
                    "source_note": None,
                },
            ),
            _command(
                "CMD-CONFLICT",
                "ADD_CONFLICT",
                {
                    "conflict_id": "CF-CAREER-001",
                    "domain": "CAREER",
                    "key": "employment_status",
                    "fact_ids": ["SF-CAREER-001", "SF-CAREER-X"],
                    "status": "UNRESOLVED",
                },
            ),
        ),
    )
    assert len(result.next_state.conflicts) == 1
    values = {
        item.value
        for item in result.next_state.assertions
        if item.domain == "CAREER" and item.key == "employment_status"
        and item.valid_through is None
    }
    assert values == {"EMPLOYED", "UNEMPLOYED"}


def test_missingness_changes_only_by_explicit_commands():
    previous = _previous()
    result = update_acquired_state(
        previous,
        as_of_date="2027-07-01",
        new_source_observation_ids=("OBS-NEW-001",),
        commands=(
            _command(
                "CMD-CLEAR",
                "CLEAR_MISSINGNESS",
                {"domain": "RESOURCE", "key": "liquid_asset_level"},
            ),
            _command(
                "CMD-SET",
                "SET_MISSINGNESS",
                {
                    "domain": "RELATIONSHIP",
                    "key": "relationship_status",
                    "reason": "NOT_ASKED",
                    "last_observed_date": None,
                },
            ),
        ),
    )
    slots = {(item.domain, item.key) for item in result.next_state.missingness}
    assert ("RESOURCE", "liquid_asset_level") not in slots
    assert ("RELATIONSHIP", "relationship_status") in slots


def test_action_and_context_are_append_only_in_v01():
    previous = _previous()
    result = update_acquired_state(
        previous,
        as_of_date="2027-07-01",
        new_source_observation_ids=("OBS-NEW-001",),
        commands=(
            _command(
                "CMD-ACTION",
                "ADD_ACTION",
                {
                    "action_id": "ACT-NEW",
                    "label": "accepted interview",
                    "status": "ACTUAL",
                    "confidence": "HIGH",
                    "date": "2027-07-01",
                    "observation_refs": ["OBS-NEW-001"],
                },
            ),
            _command(
                "CMD-CONTEXT",
                "ADD_CONTEXT",
                {
                    "context_id": "CTX-NEW",
                    "kind": "EXTERNAL",
                    "label": "hiring freeze",
                    "status": "ACTIVE",
                    "confidence": "HIGH",
                    "observation_refs": ["OBS-NEW-001"],
                },
            ),
        ),
    )
    assert "ACT-NEW" in {item.action_id for item in result.next_state.actions}
    assert "CTX-NEW" in {item.context_id for item in result.next_state.context_items}


def test_every_command_requires_known_observation_provenance():
    previous = _previous()
    with pytest.raises(ValueError, match="unknown observations"):
        update_acquired_state(
            previous,
            as_of_date="2027-07-01",
            commands=(
                _command(
                    "CMD-1",
                    "SET_MISSINGNESS",
                    {
                        "domain": "CAREER",
                        "key": "salary_band",
                        "reason": "NOT_ASKED",
                        "last_observed_date": None,
                    },
                    refs=("OBS-NOT-REGISTERED",),
                ),
            ),
        )


def test_update_time_cannot_move_backwards():
    previous = _previous()
    with pytest.raises(ValueError, match="cannot predate"):
        update_acquired_state(
            previous,
            as_of_date="2027-01-01",
            commands=(),
        )


def test_duplicate_command_ids_fail_closed():
    previous = _previous()
    command = _command(
        "CMD-X",
        "SET_MISSINGNESS",
        {
            "domain": "CAREER",
            "key": "salary_band",
            "reason": "NOT_ASKED",
            "last_observed_date": None,
        },
        refs=("OBS-STATE-001",),
    )
    with pytest.raises(ValueError, match="duplicate"):
        update_acquired_state(
            previous,
            as_of_date="2027-07-01",
            commands=(command, command),
        )


def test_empty_update_creates_new_version_without_inferred_change():
    previous = _previous()
    result = update_acquired_state(
        previous,
        as_of_date="2027-07-01",
        commands=(),
    )
    assert result.next_state.previous_state_id == previous.state_id
    assert result.next_state.assertions == previous.assertions
    assert result.next_state.actions == previous.actions
    assert result.next_state.context_items == previous.context_items

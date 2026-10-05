"""Deterministic PL3-S AcquiredState updater v0.1.

The updater applies only explicit, typed commands to a previous
AcquiredStateProfile. It never parses free text, infers a hidden state, resolves
conflicts probabilistically, or modifies natal/temporal truth.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import date
from typing import Any, Iterable, Mapping, Sequence

from .acquired_state import (
    AcquiredAction,
    AcquiredContextItem,
    AcquiredStateAssertion,
    AcquiredStateProfile,
    StateConflict,
    StateMissingness,
    compile_acquired_state,
)


UPDATE_OPERATIONS = frozenset(
    {
        "ADD_ASSERTION",
        "CLOSE_ASSERTION",
        "ADD_ACTION",
        "ADD_CONTEXT",
        "SET_MISSINGNESS",
        "CLEAR_MISSINGNESS",
        "ADD_CONFLICT",
        "CLEAR_CONFLICT",
    }
)


@dataclass(frozen=True)
class StateUpdateCommand:
    command_id: str
    operation: str
    payload: Mapping[str, Any]
    observation_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        if not str(self.command_id or "").strip():
            raise ValueError("StateUpdateCommand.command_id is required")
        if self.operation not in UPDATE_OPERATIONS:
            raise ValueError(f"unsupported state update operation: {self.operation}")
        if not isinstance(self.payload, Mapping):
            raise ValueError("StateUpdateCommand.payload must be an object")
        refs = tuple(str(item).strip() for item in self.observation_refs)
        if not refs or any(not item for item in refs):
            raise ValueError(
                "StateUpdateCommand requires non-empty observation_refs"
            )


@dataclass(frozen=True)
class StateUpdateResult:
    previous_state_id: str
    next_state: AcquiredStateProfile
    applied_command_ids: tuple[str, ...]
    preserved_assertion_ids: tuple[str, ...]
    preserved_action_ids: tuple[str, ...]
    preserved_context_ids: tuple[str, ...]


def _date_text(value: date | None) -> str | None:
    return value.isoformat() if value is not None else None


def _assertion_dict(item: AcquiredStateAssertion) -> dict[str, Any]:
    return {
        "fact_id": item.fact_id,
        "domain": item.domain,
        "key": item.key,
        "value": item.value,
        "status": item.status,
        "confidence": item.confidence,
        "valid_from": _date_text(item.valid_from),
        "valid_through": _date_text(item.valid_through),
        "observation_refs": list(item.observation_refs),
        "source_note": item.source_note,
    }


def _action_dict(item: AcquiredAction) -> dict[str, Any]:
    return {
        "action_id": item.action_id,
        "label": item.label,
        "status": item.status,
        "confidence": item.confidence,
        "date": _date_text(item.action_date),
        "observation_refs": list(item.observation_refs),
    }


def _context_dict(item: AcquiredContextItem) -> dict[str, Any]:
    return {
        "context_id": item.context_id,
        "kind": item.kind,
        "label": item.label,
        "status": item.status,
        "confidence": item.confidence,
        "observation_refs": list(item.observation_refs),
    }


def _missingness_dict(item: StateMissingness) -> dict[str, Any]:
    return {
        "domain": item.domain,
        "key": item.key,
        "reason": item.reason,
        "last_observed_date": _date_text(item.last_observed_date),
    }


def _conflict_dict(item: StateConflict) -> dict[str, Any]:
    return {
        "conflict_id": item.conflict_id,
        "domain": item.domain,
        "key": item.key,
        "fact_ids": list(item.fact_ids),
        "status": item.status,
    }


def _required_payload_text(payload: Mapping[str, Any], key: str) -> str:
    value = str(payload.get(key) or "").strip()
    if not value:
        raise ValueError(f"update command payload.{key} is required")
    return value


def _parse_iso_date(value: Any, field: str) -> date:
    text = str(value or "").strip()
    if not text:
        raise ValueError(f"{field} is required")
    try:
        return date.fromisoformat(text)
    except ValueError as exc:
        raise ValueError(f"{field} must be ISO YYYY-MM-DD") from exc


def _active_assertions_by_slot(
    assertions: Sequence[Mapping[str, Any]],
) -> dict[tuple[str, str], list[Mapping[str, Any]]]:
    active: dict[tuple[str, str], list[Mapping[str, Any]]] = {}
    for item in assertions:
        if item.get("valid_through") not in (None, ""):
            continue
        slot = (str(item.get("domain")), str(item.get("key")))
        active.setdefault(slot, []).append(item)
    return active


def _assert_explicit_conflict_or_single_value(
    assertions: Sequence[Mapping[str, Any]],
    conflicts: Sequence[Mapping[str, Any]],
) -> None:
    conflict_slots = {
        (str(item.get("domain")), str(item.get("key"))): set(item.get("fact_ids") or ())
        for item in conflicts
    }
    for slot, items in _active_assertions_by_slot(assertions).items():
        values = {repr(item.get("value")) for item in items}
        if len(values) <= 1:
            continue
        fact_ids = {str(item.get("fact_id")) for item in items}
        declared = conflict_slots.get(slot, set())
        if not fact_ids.issubset(declared):
            raise ValueError(
                "conflicting active assertions require an explicit ADD_CONFLICT "
                f"command for {slot[0]}:{slot[1]}"
            )


def update_acquired_state(
    previous: AcquiredStateProfile,
    *,
    as_of_date: str,
    commands: Iterable[StateUpdateCommand],
    new_source_observation_ids: Iterable[str] = (),
    state_confidence: str | None = None,
) -> StateUpdateResult:
    """Apply an explicit deterministic patch to a prior reality-state snapshot."""

    next_date = _parse_iso_date(as_of_date, "as_of_date")
    if next_date < previous.as_of_date:
        raise ValueError("next acquired-state as_of_date cannot predate previous state")

    command_items = tuple(commands)
    command_ids = [item.command_id for item in command_items]
    if len(command_ids) != len(set(command_ids)):
        raise ValueError("duplicate StateUpdateCommand.command_id")

    assertions = [_assertion_dict(item) for item in previous.assertions]
    actions = [_action_dict(item) for item in previous.actions]
    contexts = [_context_dict(item) for item in previous.context_items]
    missingness = [_missingness_dict(item) for item in previous.missingness]
    conflicts = [_conflict_dict(item) for item in previous.conflicts]

    original_assertions = {item["fact_id"] for item in assertions}
    original_actions = {item["action_id"] for item in actions}
    original_contexts = {item["context_id"] for item in contexts}

    observation_ids = set(previous.source_observation_ids)
    observation_ids.update(
        str(value).strip() for value in new_source_observation_ids if str(value).strip()
    )

    unknown_command_refs = sorted({
        ref
        for command in command_items
        for ref in command.observation_refs
        if ref not in observation_ids
    })
    if unknown_command_refs:
        raise ValueError(
            "state update command references unknown observations: "
            + ", ".join(unknown_command_refs)
        )

    for command in command_items:
        payload = dict(command.payload)

        if command.operation == "ADD_ASSERTION":
            fact_id = _required_payload_text(payload, "fact_id")
            if any(item["fact_id"] == fact_id for item in assertions):
                raise ValueError(f"ADD_ASSERTION fact_id already exists: {fact_id}")
            assertions.append(payload)

        elif command.operation == "CLOSE_ASSERTION":
            fact_id = _required_payload_text(payload, "fact_id")
            valid_through = _parse_iso_date(
                payload.get("valid_through"), "CLOSE_ASSERTION.valid_through"
            )
            found = False
            for index, item in enumerate(assertions):
                if item["fact_id"] != fact_id:
                    continue
                found = True
                if item.get("valid_through") not in (None, ""):
                    raise ValueError(f"assertion already closed: {fact_id}")
                valid_from = (
                    _parse_iso_date(item["valid_from"], "assertion.valid_from")
                    if item.get("valid_from")
                    else None
                )
                if valid_from and valid_through < valid_from:
                    raise ValueError("CLOSE_ASSERTION cannot predate assertion valid_from")
                assertions[index] = {**item, "valid_through": valid_through.isoformat()}
                break
            if not found:
                raise ValueError(f"CLOSE_ASSERTION unknown fact_id: {fact_id}")

        elif command.operation == "ADD_ACTION":
            action_id = _required_payload_text(payload, "action_id")
            if any(item["action_id"] == action_id for item in actions):
                raise ValueError(f"ADD_ACTION action_id already exists: {action_id}")
            actions.append(payload)

        elif command.operation == "ADD_CONTEXT":
            context_id = _required_payload_text(payload, "context_id")
            if any(item["context_id"] == context_id for item in contexts):
                raise ValueError(f"ADD_CONTEXT context_id already exists: {context_id}")
            contexts.append(payload)

        elif command.operation == "SET_MISSINGNESS":
            domain = _required_payload_text(payload, "domain")
            key = _required_payload_text(payload, "key")
            missingness = [
                item
                for item in missingness
                if (item["domain"], item["key"]) != (domain, key)
            ]
            missingness.append(payload)

        elif command.operation == "CLEAR_MISSINGNESS":
            domain = _required_payload_text(payload, "domain")
            key = _required_payload_text(payload, "key")
            before = len(missingness)
            missingness = [
                item
                for item in missingness
                if (item["domain"], item["key"]) != (domain, key)
            ]
            if len(missingness) == before:
                raise ValueError(f"CLEAR_MISSINGNESS target not found: {domain}:{key}")

        elif command.operation == "ADD_CONFLICT":
            conflict_id = _required_payload_text(payload, "conflict_id")
            if any(item["conflict_id"] == conflict_id for item in conflicts):
                raise ValueError(f"ADD_CONFLICT conflict_id already exists: {conflict_id}")
            conflicts.append(payload)

        elif command.operation == "CLEAR_CONFLICT":
            conflict_id = _required_payload_text(payload, "conflict_id")
            before = len(conflicts)
            conflicts = [
                item for item in conflicts if item["conflict_id"] != conflict_id
            ]
            if len(conflicts) == before:
                raise ValueError(f"CLEAR_CONFLICT target not found: {conflict_id}")

    _assert_explicit_conflict_or_single_value(assertions, conflicts)

    payload = {
        "schema_version": "0.1",
        "state_id": None,
        "person_key": previous.person_key,
        "as_of_date": next_date.isoformat(),
        "previous_state_id": previous.state_id,
        "assertions": assertions,
        "actions": actions,
        "context_items": contexts,
        "missingness": missingness,
        "conflicts": conflicts,
        "source_observation_ids": sorted(observation_ids),
        "state_confidence": state_confidence or previous.state_confidence,
    }
    next_state = compile_acquired_state(payload)

    return StateUpdateResult(
        previous_state_id=previous.state_id,
        next_state=next_state,
        applied_command_ids=tuple(command_ids),
        preserved_assertion_ids=tuple(
            sorted(original_assertions.intersection(
                item.fact_id for item in next_state.assertions
            ))
        ),
        preserved_action_ids=tuple(
            sorted(original_actions.intersection(
                item.action_id for item in next_state.actions
            ))
        ),
        preserved_context_ids=tuple(
            sorted(original_contexts.intersection(
                item.context_id for item in next_state.context_items
            ))
        ),
    )

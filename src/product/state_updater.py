"""PL3-S deterministic state updater v0.1.

The updater consumes one already-validated longitudinal observation plus
explicit, user-confirmed state directives.  It never infers a state transition
from an event label, manifestation family, or free-form narrative.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, replace
from datetime import date
from typing import Any, Mapping, Sequence

from .acquired_state import (
    ACQUIRED_STATE_DOMAINS,
    ASSERTION_STATUSES,
    MISSINGNESS_REASONS,
    AcquiredAction,
    AcquiredContextItem,
    AcquiredStateAssertion,
    AcquiredStateProfile,
    StateConflict,
    StateMissingness,
    compile_acquired_state,
)
from .longitudinal_observation import CONFIDENCE_LEVELS
from .longitudinal_observation_v02 import LongitudinalObservationRecordV02


STATE_UPDATE_OPERATIONS = frozenset({"UPSERT_ASSERTION", "MARK_MISSING"})


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


def _optional_date(value: Any, field: str) -> date | None:
    if value in (None, ""):
        return None
    try:
        return date.fromisoformat(str(value))
    except ValueError as exc:
        raise ValueError(f"{field} must be ISO YYYY-MM-DD") from exc


def _scalar(value: Any, field: str) -> str | int | float | bool | None:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    raise ValueError(f"{field} must be a JSON scalar")


def _stable_hash(prefix: str, payload: Mapping[str, Any]) -> str:
    raw = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return prefix + hashlib.sha256(raw).hexdigest()[:20]


@dataclass(frozen=True)
class StateUpdateDirective:
    directive_id: str
    observation_ref: str
    operation: str
    user_confirmed: bool
    domain: str
    key: str
    value: str | int | float | bool | None
    assertion_status: str | None
    confidence: str | None
    valid_from: date | None
    valid_through: date | None
    supersedes_existing: bool
    missingness_reason: str | None
    source_note: str | None

    def __post_init__(self) -> None:
        if self.operation not in STATE_UPDATE_OPERATIONS:
            raise ValueError(f"unsupported state update operation: {self.operation}")
        if not self.user_confirmed:
            raise ValueError(
                f"{self.directive_id}: state update directive requires user_confirmed=true"
            )
        if self.domain not in ACQUIRED_STATE_DOMAINS:
            raise ValueError(f"unsupported acquired-state domain: {self.domain}")
        if not self.observation_ref.strip():
            raise ValueError("state update directive observation_ref is required")
        if not self.key.strip():
            raise ValueError("state update directive key is required")

        if self.operation == "UPSERT_ASSERTION":
            if self.value is None:
                raise ValueError("UPSERT_ASSERTION requires non-null value")
            if self.assertion_status not in ASSERTION_STATUSES:
                raise ValueError(
                    "UPSERT_ASSERTION requires CONFIRMED/REPORTED assertion_status"
                )
            if self.confidence not in CONFIDENCE_LEVELS:
                raise ValueError("UPSERT_ASSERTION requires valid confidence")
            if self.missingness_reason is not None:
                raise ValueError(
                    "UPSERT_ASSERTION cannot carry missingness_reason"
                )
            if (
                self.valid_from
                and self.valid_through
                and self.valid_through < self.valid_from
            ):
                raise ValueError("valid_through cannot predate valid_from")
        else:
            if self.value is not None:
                raise ValueError("MARK_MISSING cannot carry value")
            if self.assertion_status is not None:
                raise ValueError("MARK_MISSING cannot carry assertion_status")
            if self.confidence is not None:
                raise ValueError("MARK_MISSING cannot carry confidence")
            if self.missingness_reason not in MISSINGNESS_REASONS:
                raise ValueError("MARK_MISSING requires valid missingness_reason")
            if self.supersedes_existing:
                raise ValueError(
                    "MARK_MISSING does not use supersedes_existing; it always "
                    "replaces the current value for that key with missingness"
                )


@dataclass(frozen=True)
class StateUpdateRequest:
    schema_version: str
    observation_ref: str
    state_confidence: str
    directives: tuple[StateUpdateDirective, ...]

    def __post_init__(self) -> None:
        if self.schema_version != "0.1":
            raise ValueError("StateUpdateRequest schema_version must be 0.1")
        if not self.observation_ref.strip():
            raise ValueError("StateUpdateRequest.observation_ref is required")
        if self.state_confidence not in CONFIDENCE_LEVELS:
            raise ValueError(
                f"unsupported state_confidence: {self.state_confidence}"
            )
        ids = [item.directive_id for item in self.directives]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate state update directive_id")
        for item in self.directives:
            if item.observation_ref != self.observation_ref:
                raise ValueError(
                    f"{item.directive_id}: observation_ref does not match request"
                )


@dataclass(frozen=True)
class StateUpdateReport:
    previous_state_id: str | None
    observation_ref: str
    applied_directive_ids: tuple[str, ...]
    generated_conflict_ids: tuple[str, ...]
    state: AcquiredStateProfile


def compile_state_update_request(payload: Mapping[str, Any]) -> StateUpdateRequest:
    if str(payload.get("schema_version", "")).strip() != "0.1":
        raise ValueError("state update request schema_version must be 0.1")

    observation_ref = _required_text(
        payload.get("observation_ref"), "observation_ref"
    )
    state_confidence = _required_text(
        payload.get("state_confidence"), "state_confidence"
    )
    if state_confidence not in CONFIDENCE_LEVELS:
        raise ValueError(f"unsupported state_confidence: {state_confidence}")

    raw_directives = payload.get("directives", [])
    if not isinstance(raw_directives, Sequence) or isinstance(
        raw_directives, (str, bytes)
    ):
        raise ValueError("directives must be an array")

    directives: list[StateUpdateDirective] = []
    for index, item in enumerate(raw_directives):
        if not isinstance(item, Mapping):
            raise ValueError(f"directives[{index}] must be an object")
        operation = _required_text(
            item.get("operation"), f"directives[{index}].operation"
        )
        directives.append(
            StateUpdateDirective(
                directive_id=_required_text(
                    item.get("directive_id"),
                    f"directives[{index}].directive_id",
                ),
                observation_ref=_required_text(
                    item.get("observation_ref"),
                    f"directives[{index}].observation_ref",
                ),
                operation=operation,
                user_confirmed=bool(item.get("user_confirmed", False)),
                domain=_required_text(
                    item.get("domain"), f"directives[{index}].domain"
                ),
                key=_required_text(item.get("key"), f"directives[{index}].key"),
                value=_scalar(
                    item.get("value"), f"directives[{index}].value"
                ),
                assertion_status=(
                    _optional_text(item.get("assertion_status"))
                    if operation == "UPSERT_ASSERTION"
                    else None
                ),
                confidence=(
                    _optional_text(item.get("confidence"))
                    if operation == "UPSERT_ASSERTION"
                    else None
                ),
                valid_from=_optional_date(
                    item.get("valid_from"), f"directives[{index}].valid_from"
                ),
                valid_through=_optional_date(
                    item.get("valid_through"),
                    f"directives[{index}].valid_through",
                ),
                supersedes_existing=bool(
                    item.get("supersedes_existing", False)
                ),
                missingness_reason=(
                    _optional_text(item.get("missingness_reason"))
                    if operation == "MARK_MISSING"
                    else None
                ),
                source_note=_optional_text(item.get("source_note")),
            )
        )

    return StateUpdateRequest(
        schema_version="0.1",
        observation_ref=observation_ref,
        state_confidence=state_confidence,
        directives=tuple(sorted(directives, key=lambda item: item.directive_id)),
    )


def _make_fact(
    directive: StateUpdateDirective,
) -> AcquiredStateAssertion:
    payload = {
        "directive_id": directive.directive_id,
        "observation_ref": directive.observation_ref,
        "domain": directive.domain,
        "key": directive.key,
        "value": directive.value,
        "status": directive.assertion_status,
        "valid_from": (
            directive.valid_from.isoformat() if directive.valid_from else None
        ),
        "valid_through": (
            directive.valid_through.isoformat() if directive.valid_through else None
        ),
    }
    return AcquiredStateAssertion(
        fact_id=_stable_hash("SFU-", payload),
        domain=directive.domain,
        key=directive.key,
        value=directive.value,
        status=str(directive.assertion_status),
        confidence=str(directive.confidence),
        valid_from=directive.valid_from,
        valid_through=directive.valid_through,
        observation_refs=(directive.observation_ref,),
        source_note=directive.source_note,
    )


def _context_id(kind: str, label: str) -> str:
    return _stable_hash("CTX-", {"kind": kind, "label": label})


def _observation_actions(
    observation: LongitudinalObservationRecordV02,
) -> tuple[AcquiredAction, ...]:
    base = observation.base
    out = []
    for item in base.actions:
        out.append(
            AcquiredAction(
                action_id=_required_text(item.get("action_id"), "action.action_id"),
                label=_required_text(item.get("label"), "action.label"),
                status=_required_text(item.get("status"), "action.status"),
                confidence=_required_text(
                    item.get("confidence"), "action.confidence"
                ),
                action_date=(
                    date.fromisoformat(str(item["date"]))
                    if item.get("date")
                    else None
                ),
                observation_refs=(base.record_id,),
            )
        )
    return tuple(sorted(out, key=lambda item: item.action_id))


def _observation_context(
    observation: LongitudinalObservationRecordV02,
) -> tuple[AcquiredContextItem, ...]:
    base = observation.base
    rows: list[AcquiredContextItem] = []

    for kind, values in (
        ("EXPOSURE", base.exposures),
        ("EXTERNAL", base.external_factors),
        ("COUNTERPARTY", base.counterparty_factors),
    ):
        for label in values:
            rows.append(
                AcquiredContextItem(
                    context_id=_context_id(kind, label),
                    kind=kind,
                    label=label,
                    status="ACTIVE",
                    confidence=base.observation_confidence,
                    observation_refs=(base.record_id,),
                )
            )
    return tuple(sorted(rows, key=lambda item: item.context_id))


def _merge_actions(
    old: Sequence[AcquiredAction],
    new: Sequence[AcquiredAction],
) -> tuple[AcquiredAction, ...]:
    merged = {item.action_id: item for item in old}
    for item in new:
        prior = merged.get(item.action_id)
        refs = tuple(
            sorted(
                set(item.observation_refs)
                | (set(prior.observation_refs) if prior else set())
            )
        )
        merged[item.action_id] = replace(item, observation_refs=refs)
    return tuple(merged[key] for key in sorted(merged))


def _merge_context(
    old: Sequence[AcquiredContextItem],
    new: Sequence[AcquiredContextItem],
) -> tuple[AcquiredContextItem, ...]:
    merged = {item.context_id: item for item in old}
    for item in new:
        prior = merged.get(item.context_id)
        refs = tuple(
            sorted(
                set(item.observation_refs)
                | (set(prior.observation_refs) if prior else set())
            )
        )
        merged[item.context_id] = replace(item, observation_refs=refs)
    return tuple(merged[key] for key in sorted(merged))


def _drop_invalid_conflicts(
    conflicts: Sequence[StateConflict],
    facts: Sequence[AcquiredStateAssertion],
) -> list[StateConflict]:
    ids = {item.fact_id for item in facts}
    return [
        conflict
        for conflict in conflicts
        if set(conflict.fact_ids).issubset(ids)
    ]


def _new_conflict(
    *,
    domain: str,
    key: str,
    fact_ids: Sequence[str],
) -> StateConflict:
    unique_ids = tuple(sorted(set(fact_ids)))
    return StateConflict(
        conflict_id=_stable_hash(
            "SCF-",
            {"domain": domain, "key": key, "fact_ids": list(unique_ids)},
        ),
        domain=domain,
        key=key,
        fact_ids=unique_ids,
        status="UNRESOLVED",
    )


def update_acquired_state(
    previous: AcquiredStateProfile | None,
    observation: LongitudinalObservationRecordV02,
    request: StateUpdateRequest,
) -> StateUpdateReport:
    """Apply one deterministic state update.

    Observation event labels do not mutate assertions by themselves.  Only
    explicit confirmed directives may add/change/mask state assertions.
    """

    base = observation.base
    if request.observation_ref != base.record_id:
        raise ValueError("state update request does not match observation record_id")

    if previous is not None:
        if previous.person_key != base.person_key:
            raise ValueError("observation person_key does not match previous state")
        if base.collected_date < previous.as_of_date:
            raise ValueError(
                "v0.1 does not apply backdated observations; replay from an "
                "earlier state snapshot instead"
            )

    assertions = list(previous.assertions if previous else ())
    actions = _merge_actions(
        previous.actions if previous else (),
        _observation_actions(observation),
    )
    context_items = _merge_context(
        previous.context_items if previous else (),
        _observation_context(observation),
    )
    missingness = list(previous.missingness if previous else ())
    conflicts = list(previous.conflicts if previous else ())

    # Expiry is explicit only: no generic decay or stale-time threshold.
    expired = [
        item
        for item in assertions
        if item.valid_through is not None
        and item.valid_through < base.collected_date
    ]
    if expired:
        expired_ids = {item.fact_id for item in expired}
        assertions = [
            item for item in assertions if item.fact_id not in expired_ids
        ]
        for item in expired:
            missingness = [
                miss
                for miss in missingness
                if not (miss.domain == item.domain and miss.key == item.key)
            ]
            missingness.append(
                StateMissingness(
                    domain=item.domain,
                    key=item.key,
                    reason="OUTDATED",
                    last_observed_date=item.valid_through,
                )
            )

    generated_conflict_ids: list[str] = []
    applied_ids: list[str] = []

    for directive in request.directives:
        if directive.observation_ref != base.record_id:
            raise ValueError(
                f"{directive.directive_id}: observation_ref mismatch"
            )

        same_key = [
            item
            for item in assertions
            if item.domain == directive.domain and item.key == directive.key
        ]

        if directive.operation == "MARK_MISSING":
            assertions = [
                item
                for item in assertions
                if not (
                    item.domain == directive.domain
                    and item.key == directive.key
                )
            ]
            missingness = [
                item
                for item in missingness
                if not (
                    item.domain == directive.domain
                    and item.key == directive.key
                )
            ]
            missingness.append(
                StateMissingness(
                    domain=directive.domain,
                    key=directive.key,
                    reason=str(directive.missingness_reason),
                    last_observed_date=base.collected_date,
                )
            )
            conflicts = _drop_invalid_conflicts(conflicts, assertions)
            applied_ids.append(directive.directive_id)
            continue

        new_fact = _make_fact(directive)

        # Any explicit value makes same-key missingness obsolete.
        missingness = [
            item
            for item in missingness
            if not (
                item.domain == directive.domain and item.key == directive.key
            )
        ]

        if not same_key:
            assertions.append(new_fact)
            applied_ids.append(directive.directive_id)
            continue

        same_value = [item for item in same_key if item.value == directive.value]
        different_value = [
            item for item in same_key if item.value != directive.value
        ]

        if directive.supersedes_existing:
            removed_ids = {item.fact_id for item in same_key}
            assertions = [
                item for item in assertions if item.fact_id not in removed_ids
            ]
            assertions.append(new_fact)
            conflicts = _drop_invalid_conflicts(conflicts, assertions)
            applied_ids.append(directive.directive_id)
            continue

        if same_value and not different_value:
            refs = tuple(
                sorted(
                    {
                        directive.observation_ref,
                        *(
                            ref
                            for item in same_value
                            for ref in item.observation_refs
                        ),
                    }
                )
            )
            removed_ids = {item.fact_id for item in same_value}
            assertions = [
                item for item in assertions if item.fact_id not in removed_ids
            ]
            assertions.append(replace(new_fact, observation_refs=refs))
            conflicts = _drop_invalid_conflicts(conflicts, assertions)
            applied_ids.append(directive.directive_id)
            continue

        assertions.append(new_fact)
        conflict = _new_conflict(
            domain=directive.domain,
            key=directive.key,
            fact_ids=[item.fact_id for item in same_key] + [new_fact.fact_id],
        )
        conflicts = [
            item
            for item in conflicts
            if not (
                item.domain == directive.domain and item.key == directive.key
            )
        ]
        conflicts.append(conflict)
        generated_conflict_ids.append(conflict.conflict_id)
        applied_ids.append(directive.directive_id)

    assertions = sorted(assertions, key=lambda item: item.fact_id)
    missingness = sorted(missingness, key=lambda item: (item.domain, item.key))
    conflicts = _drop_invalid_conflicts(conflicts, assertions)
    conflicts = sorted(conflicts, key=lambda item: item.conflict_id)

    source_observation_ids = tuple(
        sorted(
            set(previous.source_observation_ids if previous else ())
            | {base.record_id}
        )
    )

    payload = {
        "schema_version": "0.1",
        "state_id": None,
        "person_key": base.person_key,
        "as_of_date": base.collected_date.isoformat(),
        "previous_state_id": previous.state_id if previous else None,
        "assertions": [
            {
                "fact_id": item.fact_id,
                "domain": item.domain,
                "key": item.key,
                "value": item.value,
                "status": item.status,
                "confidence": item.confidence,
                "valid_from": item.valid_from.isoformat() if item.valid_from else None,
                "valid_through": (
                    item.valid_through.isoformat() if item.valid_through else None
                ),
                "observation_refs": list(item.observation_refs),
                "source_note": item.source_note,
            }
            for item in assertions
        ],
        "actions": [
            {
                "action_id": item.action_id,
                "label": item.label,
                "status": item.status,
                "confidence": item.confidence,
                "date": item.action_date.isoformat() if item.action_date else None,
                "observation_refs": list(item.observation_refs),
            }
            for item in actions
        ],
        "context_items": [
            {
                "context_id": item.context_id,
                "kind": item.kind,
                "label": item.label,
                "status": item.status,
                "confidence": item.confidence,
                "observation_refs": list(item.observation_refs),
            }
            for item in context_items
        ],
        "missingness": [
            {
                "domain": item.domain,
                "key": item.key,
                "reason": item.reason,
                "last_observed_date": (
                    item.last_observed_date.isoformat()
                    if item.last_observed_date
                    else None
                ),
            }
            for item in missingness
        ],
        "conflicts": [
            {
                "conflict_id": item.conflict_id,
                "domain": item.domain,
                "key": item.key,
                "fact_ids": list(item.fact_ids),
                "status": item.status,
            }
            for item in conflicts
        ],
        "source_observation_ids": list(source_observation_ids),
        "state_confidence": request.state_confidence,
    }

    state = compile_acquired_state(payload)
    return StateUpdateReport(
        previous_state_id=previous.state_id if previous else None,
        observation_ref=base.record_id,
        applied_directive_ids=tuple(sorted(applied_ids)),
        generated_conflict_ids=tuple(sorted(generated_conflict_ids)),
        state=state,
    )

"""PL3-S AcquiredState schema v0.1.

This module represents the user's real-world, time-varying state.  It is
deliberately separate from NatalStateProfile, TemporalEnvironmentProfile,
empirical probability, and canonical rule truth.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import date
from typing import Any, Mapping, Sequence

from .longitudinal_observation import ACTION_STATUSES, CONFIDENCE_LEVELS


ACQUIRED_STATE_DOMAINS = frozenset(
    {
        "RELATIONSHIP",
        "CAREER",
        "RESOURCE",
        "RELOCATION",
        "COMMITMENT",
        "SOCIAL_EXPOSURE",
        "HEALTH_CONTEXT",
        "EDUCATION_CONTEXT",
        "FAMILY_CONTEXT",
        "HOUSING_CONTEXT",
        "OTHER",
    }
)

ASSERTION_STATUSES = frozenset({"CONFIRMED", "REPORTED"})
CONTEXT_KINDS = frozenset({"EXPOSURE", "EXTERNAL", "COUNTERPARTY"})
CONTEXT_STATUSES = frozenset({"ACTIVE", "INACTIVE", "UNKNOWN"})
MISSINGNESS_REASONS = frozenset(
    {"UNKNOWN", "NOT_OBSERVED", "NOT_ASKED", "OUTDATED", "WITHHELD"}
)

FORBIDDEN_CANONICAL_KEYS = frozenset(
    {
        "canonical_facts",
        "natal_state",
        "natal_profile",
        "natal_profile_id",
        "temporal_environment",
        "temporal_rules",
        "canonical_rules",
        "rule_truth",
        "manifestation_probability",
        "population_probability",
        "personalized_posterior",
    }
)


JsonScalar = str | int | float | bool | None


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


def _iso_date(value: Any, field: str) -> date:
    text = _required_text(value, field)
    try:
        return date.fromisoformat(text)
    except ValueError as exc:
        raise ValueError(f"{field} must be ISO YYYY-MM-DD") from exc


def _optional_date(value: Any, field: str) -> date | None:
    if value in (None, ""):
        return None
    return _iso_date(value, field)


def _scalar(value: Any, field: str) -> JsonScalar:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    raise ValueError(f"{field} must be a JSON scalar in v0.1")


def _text_tuple(value: Any, field: str) -> tuple[str, ...]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise ValueError(f"{field} must be an array")
    return tuple(sorted({str(item).strip() for item in value if str(item).strip()}))


@dataclass(frozen=True)
class AcquiredStateAssertion:
    fact_id: str
    domain: str
    key: str
    value: JsonScalar
    status: str
    confidence: str
    valid_from: date | None
    valid_through: date | None
    observation_refs: tuple[str, ...]
    source_note: str | None

    def __post_init__(self) -> None:
        if self.domain not in ACQUIRED_STATE_DOMAINS:
            raise ValueError(f"unsupported acquired-state domain: {self.domain}")
        if self.status not in ASSERTION_STATUSES:
            raise ValueError(f"unsupported assertion status: {self.status}")
        if self.confidence not in CONFIDENCE_LEVELS:
            raise ValueError(f"unsupported assertion confidence: {self.confidence}")
        if self.valid_from and self.valid_through and self.valid_through < self.valid_from:
            raise ValueError("assertion valid_through cannot predate valid_from")
        if not self.observation_refs:
            raise ValueError("acquired-state assertion requires observation_refs")


@dataclass(frozen=True)
class AcquiredAction:
    action_id: str
    label: str
    status: str
    confidence: str
    action_date: date | None
    observation_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.status not in ACTION_STATUSES:
            raise ValueError(f"unsupported action status: {self.status}")
        if self.confidence not in CONFIDENCE_LEVELS:
            raise ValueError(f"unsupported action confidence: {self.confidence}")
        if not self.observation_refs:
            raise ValueError("acquired action requires observation_refs")


@dataclass(frozen=True)
class AcquiredContextItem:
    context_id: str
    kind: str
    label: str
    status: str
    confidence: str
    observation_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.kind not in CONTEXT_KINDS:
            raise ValueError(f"unsupported context kind: {self.kind}")
        if self.status not in CONTEXT_STATUSES:
            raise ValueError(f"unsupported context status: {self.status}")
        if self.confidence not in CONFIDENCE_LEVELS:
            raise ValueError(f"unsupported context confidence: {self.confidence}")
        if not self.observation_refs:
            raise ValueError("acquired context item requires observation_refs")


@dataclass(frozen=True)
class StateMissingness:
    domain: str
    key: str
    reason: str
    last_observed_date: date | None = None

    def __post_init__(self) -> None:
        if self.domain not in ACQUIRED_STATE_DOMAINS:
            raise ValueError(f"unsupported missingness domain: {self.domain}")
        if self.reason not in MISSINGNESS_REASONS:
            raise ValueError(f"unsupported missingness reason: {self.reason}")


@dataclass(frozen=True)
class StateConflict:
    conflict_id: str
    domain: str
    key: str
    fact_ids: tuple[str, ...]
    status: str = "UNRESOLVED"

    def __post_init__(self) -> None:
        if self.domain not in ACQUIRED_STATE_DOMAINS:
            raise ValueError(f"unsupported conflict domain: {self.domain}")
        if self.status != "UNRESOLVED":
            raise ValueError("PL3-S v0.1 only stores unresolved state conflicts")
        if len(set(self.fact_ids)) < 2:
            raise ValueError("state conflict requires at least two distinct fact_ids")


@dataclass(frozen=True)
class AcquiredStateProfile:
    schema_version: str
    state_id: str
    person_key: str
    as_of_date: date
    previous_state_id: str | None
    assertions: tuple[AcquiredStateAssertion, ...]
    actions: tuple[AcquiredAction, ...]
    context_items: tuple[AcquiredContextItem, ...]
    missingness: tuple[StateMissingness, ...]
    conflicts: tuple[StateConflict, ...]
    source_observation_ids: tuple[str, ...]
    state_confidence: str

    def __post_init__(self) -> None:
        if self.schema_version != "0.1":
            raise ValueError("AcquiredStateProfile schema_version must be 0.1")
        if not self.state_id.strip():
            raise ValueError("AcquiredStateProfile.state_id is required")
        if not self.person_key.strip():
            raise ValueError("AcquiredStateProfile.person_key is required")
        if self.state_confidence not in CONFIDENCE_LEVELS:
            raise ValueError(f"unsupported state_confidence: {self.state_confidence}")
        if not self.source_observation_ids:
            raise ValueError("AcquiredStateProfile requires source_observation_ids")

        fact_ids = [item.fact_id for item in self.assertions]
        if len(fact_ids) != len(set(fact_ids)):
            raise ValueError("duplicate acquired-state fact_id")
        action_ids = [item.action_id for item in self.actions]
        if len(action_ids) != len(set(action_ids)):
            raise ValueError("duplicate acquired action_id")
        context_ids = [item.context_id for item in self.context_items]
        if len(context_ids) != len(set(context_ids)):
            raise ValueError("duplicate acquired context_id")
        conflict_ids = [item.conflict_id for item in self.conflicts]
        if len(conflict_ids) != len(set(conflict_ids)):
            raise ValueError("duplicate state conflict_id")

        known_fact_ids = set(fact_ids)
        for conflict in self.conflicts:
            missing = sorted(set(conflict.fact_ids) - known_fact_ids)
            if missing:
                raise ValueError(
                    f"{conflict.conflict_id}: unknown fact_ids: {', '.join(missing)}"
                )

    def to_dict(self) -> dict[str, Any]:
        def serialize(value: Any) -> Any:
            if isinstance(value, date):
                return value.isoformat()
            if isinstance(value, tuple):
                return [serialize(item) for item in value]
            if hasattr(value, "__dataclass_fields__"):
                return {key: serialize(item) for key, item in asdict(value).items()}
            if isinstance(value, dict):
                return {key: serialize(item) for key, item in value.items()}
            return value

        return serialize(self)


def _compile_assertions(raw: Any) -> tuple[AcquiredStateAssertion, ...]:
    if not isinstance(raw, Sequence) or isinstance(raw, (str, bytes)):
        raise ValueError("assertions must be an array")
    out = []
    for index, item in enumerate(raw):
        if not isinstance(item, Mapping):
            raise ValueError(f"assertions[{index}] must be an object")
        domain = _required_text(item.get("domain"), f"assertions[{index}].domain")
        if domain not in ACQUIRED_STATE_DOMAINS:
            raise ValueError(f"unsupported acquired-state domain: {domain}")
        value = _scalar(item.get("value"), f"assertions[{index}].value")
        if value is None:
            raise ValueError(
                f"assertions[{index}].value cannot be null; use missingness instead"
            )
        out.append(
            AcquiredStateAssertion(
                fact_id=_required_text(item.get("fact_id"), f"assertions[{index}].fact_id"),
                domain=domain,
                key=_required_text(item.get("key"), f"assertions[{index}].key"),
                value=value,
                status=_required_text(item.get("status"), f"assertions[{index}].status"),
                confidence=_required_text(
                    item.get("confidence"), f"assertions[{index}].confidence"
                ),
                valid_from=_optional_date(
                    item.get("valid_from"), f"assertions[{index}].valid_from"
                ),
                valid_through=_optional_date(
                    item.get("valid_through"), f"assertions[{index}].valid_through"
                ),
                observation_refs=_text_tuple(
                    item.get("observation_refs"),
                    f"assertions[{index}].observation_refs",
                ),
                source_note=_optional_text(item.get("source_note")),
            )
        )
    return tuple(sorted(out, key=lambda item: item.fact_id))


def _compile_actions(raw: Any) -> tuple[AcquiredAction, ...]:
    if not isinstance(raw, Sequence) or isinstance(raw, (str, bytes)):
        raise ValueError("actions must be an array")
    out = []
    for index, item in enumerate(raw):
        if not isinstance(item, Mapping):
            raise ValueError(f"actions[{index}] must be an object")
        out.append(
            AcquiredAction(
                action_id=_required_text(item.get("action_id"), f"actions[{index}].action_id"),
                label=_required_text(item.get("label"), f"actions[{index}].label"),
                status=_required_text(item.get("status"), f"actions[{index}].status"),
                confidence=_required_text(
                    item.get("confidence"), f"actions[{index}].confidence"
                ),
                action_date=_optional_date(
                    item.get("date"), f"actions[{index}].date"
                ),
                observation_refs=_text_tuple(
                    item.get("observation_refs"),
                    f"actions[{index}].observation_refs",
                ),
            )
        )
    return tuple(sorted(out, key=lambda item: item.action_id))


def _compile_context(raw: Any) -> tuple[AcquiredContextItem, ...]:
    if not isinstance(raw, Sequence) or isinstance(raw, (str, bytes)):
        raise ValueError("context_items must be an array")
    out = []
    for index, item in enumerate(raw):
        if not isinstance(item, Mapping):
            raise ValueError(f"context_items[{index}] must be an object")
        out.append(
            AcquiredContextItem(
                context_id=_required_text(
                    item.get("context_id"), f"context_items[{index}].context_id"
                ),
                kind=_required_text(item.get("kind"), f"context_items[{index}].kind"),
                label=_required_text(item.get("label"), f"context_items[{index}].label"),
                status=_required_text(item.get("status"), f"context_items[{index}].status"),
                confidence=_required_text(
                    item.get("confidence"), f"context_items[{index}].confidence"
                ),
                observation_refs=_text_tuple(
                    item.get("observation_refs"),
                    f"context_items[{index}].observation_refs",
                ),
            )
        )
    return tuple(sorted(out, key=lambda item: item.context_id))


def _compile_missingness(raw: Any) -> tuple[StateMissingness, ...]:
    if not isinstance(raw, Sequence) or isinstance(raw, (str, bytes)):
        raise ValueError("missingness must be an array")
    out = []
    for index, item in enumerate(raw):
        if not isinstance(item, Mapping):
            raise ValueError(f"missingness[{index}] must be an object")
        out.append(
            StateMissingness(
                domain=_required_text(item.get("domain"), f"missingness[{index}].domain"),
                key=_required_text(item.get("key"), f"missingness[{index}].key"),
                reason=_required_text(item.get("reason"), f"missingness[{index}].reason"),
                last_observed_date=_optional_date(
                    item.get("last_observed_date"),
                    f"missingness[{index}].last_observed_date",
                ),
            )
        )
    return tuple(sorted(out, key=lambda item: (item.domain, item.key)))


def _compile_conflicts(raw: Any) -> tuple[StateConflict, ...]:
    if not isinstance(raw, Sequence) or isinstance(raw, (str, bytes)):
        raise ValueError("conflicts must be an array")
    out = []
    for index, item in enumerate(raw):
        if not isinstance(item, Mapping):
            raise ValueError(f"conflicts[{index}] must be an object")
        out.append(
            StateConflict(
                conflict_id=_required_text(
                    item.get("conflict_id"), f"conflicts[{index}].conflict_id"
                ),
                domain=_required_text(item.get("domain"), f"conflicts[{index}].domain"),
                key=_required_text(item.get("key"), f"conflicts[{index}].key"),
                fact_ids=_text_tuple(
                    item.get("fact_ids"), f"conflicts[{index}].fact_ids"
                ),
                status=_required_text(item.get("status"), f"conflicts[{index}].status"),
            )
        )
    return tuple(sorted(out, key=lambda item: item.conflict_id))


def _state_id_payload(
    *,
    person_key: str,
    as_of_date: date,
    previous_state_id: str | None,
    assertions: tuple[AcquiredStateAssertion, ...],
    actions: tuple[AcquiredAction, ...],
    context_items: tuple[AcquiredContextItem, ...],
    missingness: tuple[StateMissingness, ...],
    conflicts: tuple[StateConflict, ...],
    source_observation_ids: tuple[str, ...],
    state_confidence: str,
) -> Mapping[str, Any]:
    def serial(value: Any) -> Any:
        if isinstance(value, date):
            return value.isoformat()
        if isinstance(value, tuple):
            return [serial(item) for item in value]
        if hasattr(value, "__dataclass_fields__"):
            return {key: serial(item) for key, item in asdict(value).items()}
        return value

    return {
        "person_key": person_key,
        "as_of_date": as_of_date.isoformat(),
        "previous_state_id": previous_state_id,
        "assertions": serial(assertions),
        "actions": serial(actions),
        "context_items": serial(context_items),
        "missingness": serial(missingness),
        "conflicts": serial(conflicts),
        "source_observation_ids": list(source_observation_ids),
        "state_confidence": state_confidence,
    }


def _compute_state_id(payload: Mapping[str, Any]) -> str:
    raw = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return "ASTATE-" + hashlib.sha256(raw).hexdigest()[:24]


def compile_acquired_state(payload: Mapping[str, Any]) -> AcquiredStateProfile:
    """Validate and normalize one acquired-state snapshot.

    No inference occurs here.  Every state assertion/action/context item must
    already have explicit real-world provenance.
    """

    if str(payload.get("schema_version", "")).strip() != "0.1":
        raise ValueError("acquired-state schema_version must be 0.1")

    forbidden_present = sorted(
        key for key in FORBIDDEN_CANONICAL_KEYS if key in payload
    )
    if forbidden_present:
        raise ValueError(
            "AcquiredState payload cannot contain canonical/empirical fields: "
            + ", ".join(forbidden_present)
        )

    person_key = _required_text(payload.get("person_key"), "person_key")
    as_of_date = _iso_date(payload.get("as_of_date"), "as_of_date")
    previous_state_id = _optional_text(payload.get("previous_state_id"))

    assertions = _compile_assertions(payload.get("assertions", []))
    actions = _compile_actions(payload.get("actions", []))
    context_items = _compile_context(payload.get("context_items", []))
    missingness = _compile_missingness(payload.get("missingness", []))
    conflicts = _compile_conflicts(payload.get("conflicts", []))
    source_observation_ids = _text_tuple(
        payload.get("source_observation_ids"), "source_observation_ids"
    )
    if not source_observation_ids:
        raise ValueError("source_observation_ids cannot be empty")

    state_confidence = _required_text(
        payload.get("state_confidence"), "state_confidence"
    )
    if state_confidence not in CONFIDENCE_LEVELS:
        raise ValueError(f"unsupported state_confidence: {state_confidence}")

    all_item_refs = {
        ref
        for assertion in assertions
        for ref in assertion.observation_refs
    } | {
        ref
        for action in actions
        for ref in action.observation_refs
    } | {
        ref
        for item in context_items
        for ref in item.observation_refs
    }
    unknown_refs = sorted(all_item_refs - set(source_observation_ids))
    if unknown_refs:
        raise ValueError(
            "item observation_refs must be included in source_observation_ids: "
            + ", ".join(unknown_refs)
        )

    normalized = _state_id_payload(
        person_key=person_key,
        as_of_date=as_of_date,
        previous_state_id=previous_state_id,
        assertions=assertions,
        actions=actions,
        context_items=context_items,
        missingness=missingness,
        conflicts=conflicts,
        source_observation_ids=source_observation_ids,
        state_confidence=state_confidence,
    )
    computed_id = _compute_state_id(normalized)
    supplied_id = _optional_text(payload.get("state_id"))
    if supplied_id is not None and supplied_id != computed_id:
        raise ValueError("supplied state_id does not match deterministic state content")

    return AcquiredStateProfile(
        schema_version="0.1",
        state_id=computed_id,
        person_key=person_key,
        as_of_date=as_of_date,
        previous_state_id=previous_state_id,
        assertions=assertions,
        actions=actions,
        context_items=context_items,
        missingness=missingness,
        conflicts=conflicts,
        source_observation_ids=source_observation_ids,
        state_confidence=state_confidence,
    )

"""PL3-S AcquiredState schema v0.1.

This module models confirmed/declared real-world state separately from natal
truth and temporal astrological environment. It is a typed transport/state
contract only: no transition inference, no Bayesian update, no manifestation
probability, and no mutation of NatalStateProfile or TemporalEnvironmentProfile.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any, Iterable, Mapping


ACQUIRED_STATE_DOMAINS = frozenset(
    {"RELATIONSHIP", "CAREER", "RESOURCE", "RELOCATION", "COMMITMENT", "EXPOSURE"}
)
STATE_VALUE_STATUSES = frozenset({"KNOWN", "UNKNOWN", "CONFLICTED"})
STATE_CONFIDENCE_LEVELS = frozenset(
    {"CONFIRMED", "SUPPORTED", "LOW_CONFIDENCE", "UNKNOWN"}
)
PROVENANCE_SOURCE_TYPES = frozenset(
    {"USER_CONFIRMED", "STRUCTURED_RECORD", "ACTION_LOG", "EXPOSURE_LOG", "PREVIOUS_STATE"}
)
REALITY_RECORD_TYPES = frozenset({"ACTION", "INTENTION", "EXPOSURE"})
MISSINGNESS_STATUSES = frozenset({"UNKNOWN", "NOT_COLLECTED", "NOT_APPLICABLE"})


def _required_text(value: Any, field: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise ValueError(f"{field} is required")
    return text


def _normalized_json_value(value: Any, field: str) -> Any:
    if isinstance(value, (str, int, float, bool)) or value is None:
        if isinstance(value, str):
            text = value.strip()
            if len(text) > 256:
                raise ValueError(
                    f"{field} string is too long for normalized state; "
                    "store raw narrative outside AcquiredState"
                )
            return text
        return value
    if isinstance(value, (list, tuple)):
        if len(value) > 32:
            raise ValueError(f"{field} array is too large for normalized state")
        return [_normalized_json_value(item, field) for item in value]
    if isinstance(value, Mapping):
        if len(value) > 32:
            raise ValueError(f"{field} object is too large for normalized state")
        return {
            str(key): _normalized_json_value(item, field)
            for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))
        }
    raise ValueError(f"{field} must be JSON-compatible normalized state")


@dataclass(frozen=True)
class ObservationProvenance:
    observation_ref: str
    source_type: str
    observed_at: str
    confirmed: bool
    source_ref: str = ""

    def __post_init__(self) -> None:
        _required_text(self.observation_ref, "ObservationProvenance.observation_ref")
        _required_text(self.observed_at, "ObservationProvenance.observed_at")
        if self.source_type not in PROVENANCE_SOURCE_TYPES:
            raise ValueError(f"unsupported provenance source_type: {self.source_type}")
        if not isinstance(self.confirmed, bool):
            raise ValueError("ObservationProvenance.confirmed must be bool")


@dataclass(frozen=True)
class AcquiredStateEntry:
    domain: str
    state_key: str
    value: Any
    status: str
    confidence: str
    provenance_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.domain not in ACQUIRED_STATE_DOMAINS:
            raise ValueError(f"unsupported acquired-state domain: {self.domain}")
        _required_text(self.state_key, "AcquiredStateEntry.state_key")
        if self.status not in STATE_VALUE_STATUSES:
            raise ValueError(f"unsupported acquired-state status: {self.status}")
        if self.confidence not in STATE_CONFIDENCE_LEVELS:
            raise ValueError(f"unsupported acquired-state confidence: {self.confidence}")
        _normalized_json_value(self.value, "AcquiredStateEntry.value")
        refs = tuple(str(item).strip() for item in self.provenance_refs)
        if any(not item for item in refs):
            raise ValueError("AcquiredStateEntry provenance_refs cannot contain blanks")
        if self.status == "KNOWN" and not refs:
            raise ValueError("KNOWN acquired state requires observation provenance")
        if self.status == "UNKNOWN" and self.value is not None:
            raise ValueError("UNKNOWN acquired state must use value=None")


@dataclass(frozen=True)
class RealityContextRecord:
    record_id: str
    record_type: str
    domain: str
    key: str
    value: Any
    status: str
    provenance_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _required_text(self.record_id, "RealityContextRecord.record_id")
        if self.record_type not in REALITY_RECORD_TYPES:
            raise ValueError(f"unsupported reality record_type: {self.record_type}")
        if self.domain not in ACQUIRED_STATE_DOMAINS:
            raise ValueError(f"unsupported reality record domain: {self.domain}")
        _required_text(self.key, "RealityContextRecord.key")
        if self.status not in {"CONFIRMED", "PLANNED", "UNKNOWN"}:
            raise ValueError(f"unsupported reality record status: {self.status}")
        _normalized_json_value(self.value, "RealityContextRecord.value")


@dataclass(frozen=True)
class MissingStateDimension:
    domain: str
    state_key: str
    status: str

    def __post_init__(self) -> None:
        if self.domain not in ACQUIRED_STATE_DOMAINS:
            raise ValueError(f"unsupported missing-state domain: {self.domain}")
        _required_text(self.state_key, "MissingStateDimension.state_key")
        if self.status not in MISSINGNESS_STATUSES:
            raise ValueError(f"unsupported missingness status: {self.status}")


@dataclass(frozen=True)
class StateContradiction:
    contradiction_id: str
    domain: str
    state_key: str
    provenance_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        _required_text(self.contradiction_id, "StateContradiction.contradiction_id")
        if self.domain not in ACQUIRED_STATE_DOMAINS:
            raise ValueError(f"unsupported contradiction domain: {self.domain}")
        _required_text(self.state_key, "StateContradiction.state_key")
        if len(tuple(self.provenance_refs)) < 2:
            raise ValueError("StateContradiction requires at least two provenance refs")


@dataclass(frozen=True)
class AcquiredStateProfile:
    schema_version: str
    state_id: str
    person_key: str
    as_of: str
    entries: tuple[AcquiredStateEntry, ...]
    reality_context: tuple[RealityContextRecord, ...]
    missingness: tuple[MissingStateDimension, ...]
    contradictions: tuple[StateContradiction, ...]
    provenance: tuple[ObservationProvenance, ...]
    previous_state_id: str = ""
    natal_truth_mutated: bool = False
    temporal_environment_mutated: bool = False
    empirical_probability_used: bool = False
    outcome_prediction_used: bool = False

    def __post_init__(self) -> None:
        if self.schema_version != "0.1":
            raise ValueError("AcquiredStateProfile schema_version must be 0.1")
        _required_text(self.state_id, "AcquiredStateProfile.state_id")
        _required_text(self.person_key, "AcquiredStateProfile.person_key")
        _required_text(self.as_of, "AcquiredStateProfile.as_of")
        forbidden = {
            "natal_truth_mutated": self.natal_truth_mutated,
            "temporal_environment_mutated": self.temporal_environment_mutated,
            "empirical_probability_used": self.empirical_probability_used,
            "outcome_prediction_used": self.outcome_prediction_used,
        }
        active = [key for key, value in forbidden.items() if value]
        if active:
            raise ValueError(
                "PL3-S AcquiredState cannot mutate natal/temporal truth or "
                f"perform probability/outcome prediction: {', '.join(active)}"
            )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _state_id_payload(
    *, person_key: str, as_of: str, entries: tuple[AcquiredStateEntry, ...],
    reality_context: tuple[RealityContextRecord, ...],
    missingness: tuple[MissingStateDimension, ...],
    contradictions: tuple[StateContradiction, ...],
    provenance: tuple[ObservationProvenance, ...], previous_state_id: str,
) -> str:
    payload = {
        "person_key": person_key, "as_of": as_of,
        "entries": [asdict(item) for item in entries],
        "reality_context": [asdict(item) for item in reality_context],
        "missingness": [asdict(item) for item in missingness],
        "contradictions": [asdict(item) for item in contradictions],
        "provenance": [asdict(item) for item in provenance],
        "previous_state_id": previous_state_id,
    }
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "STATE-" + hashlib.sha256(raw).hexdigest()[:24]


def build_acquired_state_profile(
    *, person_key: str, as_of: str,
    entries: Iterable[AcquiredStateEntry] = (),
    reality_context: Iterable[RealityContextRecord] = (),
    missingness: Iterable[MissingStateDimension] = (),
    contradictions: Iterable[StateContradiction] = (),
    provenance: Iterable[ObservationProvenance] = (),
    previous_state_id: str = "",
) -> AcquiredStateProfile:
    """Build a deterministic normalized real-world state snapshot."""

    key = _required_text(person_key, "person_key")
    timestamp = _required_text(as_of, "as_of")
    entry_items = tuple(sorted(entries, key=lambda item: (item.domain, item.state_key, item.status)))
    context_items = tuple(sorted(reality_context, key=lambda item: (item.record_type, item.domain, item.key, item.record_id)))
    missing_items = tuple(sorted(missingness, key=lambda item: (item.domain, item.state_key, item.status)))
    contradiction_items = tuple(sorted(contradictions, key=lambda item: item.contradiction_id))
    provenance_items = tuple(sorted(provenance, key=lambda item: item.observation_ref))

    provenance_ids = [item.observation_ref for item in provenance_items]
    if len(set(provenance_ids)) != len(provenance_ids):
        raise ValueError("duplicate ObservationProvenance.observation_ref")
    known_refs = set(provenance_ids)
    used_refs = {ref for entry in entry_items for ref in entry.provenance_refs}
    used_refs |= {ref for item in context_items for ref in item.provenance_refs}
    used_refs |= {ref for item in contradiction_items for ref in item.provenance_refs}
    missing_refs = sorted(used_refs - known_refs)
    if missing_refs:
        raise ValueError("AcquiredState references unknown observation provenance: " + ", ".join(missing_refs))

    seen: set[tuple[str, str]] = set()
    dup: set[tuple[str, str]] = set()
    for item in entry_items:
        k = (item.domain, item.state_key)
        if k in seen:
            dup.add(k)
        seen.add(k)
    if dup:
        values = ", ".join(f"{domain}:{key}" for domain, key in sorted(dup))
        raise ValueError(
            "AcquiredStateProfile allows one normalized entry per domain/state_key; "
            f"route disagreement through contradictions: {values}"
        )

    previous = str(previous_state_id or "").strip()
    state_id = _state_id_payload(
        person_key=key, as_of=timestamp, entries=entry_items,
        reality_context=context_items, missingness=missing_items,
        contradictions=contradiction_items, provenance=provenance_items,
        previous_state_id=previous,
    )
    return AcquiredStateProfile(
        schema_version="0.1", state_id=state_id, person_key=key, as_of=timestamp,
        entries=entry_items, reality_context=context_items,
        missingness=missing_items, contradictions=contradiction_items,
        provenance=provenance_items, previous_state_id=previous,
    )

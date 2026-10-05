"""PL3-S state quality / missingness / contradiction audit v0.1.

This layer does not estimate probability.  It deterministically answers whether
a supplied AcquiredStateProfile contains enough unambiguous, sufficiently
confident real-world state information for a declared downstream requirement.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping, Sequence

from .acquired_state import (
    ACQUIRED_STATE_DOMAINS,
    AcquiredStateProfile,
)
from .longitudinal_observation import CONFIDENCE_LEVELS


QUALITY_ITEM_STATUSES = frozenset(
    {
        "AVAILABLE",
        "MISSING",
        "CONFLICTED",
        "INSUFFICIENT_CONFIDENCE",
    }
)

STATE_READINESS_STATUSES = frozenset(
    {
        "READY",
        "PARTIAL_MISSING",
        "CONFLICTED",
        "INSUFFICIENT_CONFIDENCE",
    }
)

MISSINGNESS_AUDIT_CLASSES = frozenset(
    {
        "DESIGN_MISSING",
        "OBSERVATION_GAP",
        "STALE",
        "WITHHELD_MNAR_RISK",
        "UNCLASSIFIED",
    }
)

_MISSINGNESS_CLASS_BY_REASON = {
    "NOT_ASKED": "DESIGN_MISSING",
    "NOT_OBSERVED": "OBSERVATION_GAP",
    "OUTDATED": "STALE",
    "WITHHELD": "WITHHELD_MNAR_RISK",
    "UNKNOWN": "UNCLASSIFIED",
}


def _required_text(value: Any, field: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise ValueError(f"{field} is required")
    return text


@dataclass(frozen=True)
class StateRequirement:
    requirement_id: str
    domain: str
    key: str
    accepted_confidences: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.domain not in ACQUIRED_STATE_DOMAINS:
            raise ValueError(f"unsupported state requirement domain: {self.domain}")
        if not self.key.strip():
            raise ValueError("StateRequirement.key is required")
        if not self.accepted_confidences:
            raise ValueError("accepted_confidences cannot be empty")
        unknown = sorted(set(self.accepted_confidences) - set(CONFIDENCE_LEVELS))
        if unknown:
            raise ValueError(
                "unsupported accepted confidence values: " + ", ".join(unknown)
            )


@dataclass(frozen=True)
class MissingnessAuditItem:
    domain: str
    key: str
    reason: str
    audit_class: str
    last_observed_date: str | None

    def __post_init__(self) -> None:
        if self.audit_class not in MISSINGNESS_AUDIT_CLASSES:
            raise ValueError(f"unsupported missingness audit class: {self.audit_class}")


@dataclass(frozen=True)
class StateRequirementResult:
    requirement_id: str
    domain: str
    key: str
    status: str
    fact_ids: tuple[str, ...]
    observed_confidences: tuple[str, ...]
    missingness_reason: str | None
    conflict_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.status not in QUALITY_ITEM_STATUSES:
            raise ValueError(f"unsupported requirement status: {self.status}")


@dataclass(frozen=True)
class StateQualityReport:
    schema_version: str
    state_id: str
    readiness: str
    requirements: tuple[StateRequirementResult, ...]
    missingness_audit: tuple[MissingnessAuditItem, ...]
    unresolved_conflict_ids: tuple[str, ...]
    low_confidence_fact_ids: tuple[str, ...]
    mnar_risk_keys: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.schema_version != "0.1":
            raise ValueError("StateQualityReport schema_version must be 0.1")
        if self.readiness not in STATE_READINESS_STATUSES:
            raise ValueError(f"unsupported state readiness: {self.readiness}")

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "state_id": self.state_id,
            "readiness": self.readiness,
            "requirements": [asdict(item) for item in self.requirements],
            "missingness_audit": [
                asdict(item) for item in self.missingness_audit
            ],
            "unresolved_conflict_ids": list(self.unresolved_conflict_ids),
            "low_confidence_fact_ids": list(self.low_confidence_fact_ids),
            "mnar_risk_keys": list(self.mnar_risk_keys),
        }


def compile_state_requirements(
    document: Mapping[str, Any],
) -> tuple[StateRequirement, ...]:
    if str(document.get("schema_version", "")).strip() != "0.1":
        raise ValueError("state requirements schema_version must be 0.1")
    raw = document.get("requirements")
    if not isinstance(raw, Sequence) or isinstance(raw, (str, bytes)):
        raise ValueError("requirements must be an array")

    out: list[StateRequirement] = []
    seen: set[str] = set()
    for index, item in enumerate(raw):
        if not isinstance(item, Mapping):
            raise ValueError(f"requirements[{index}] must be an object")
        requirement_id = _required_text(
            item.get("requirement_id"),
            f"requirements[{index}].requirement_id",
        )
        if requirement_id in seen:
            raise ValueError(f"duplicate requirement_id: {requirement_id}")
        seen.add(requirement_id)

        accepted_raw = item.get(
            "accepted_confidences", ["HIGH", "MEDIUM", "LOW"]
        )
        if not isinstance(accepted_raw, Sequence) or isinstance(
            accepted_raw, (str, bytes)
        ):
            raise ValueError(
                f"requirements[{index}].accepted_confidences must be an array"
            )
        accepted = tuple(
            sorted(
                {
                    str(value).strip()
                    for value in accepted_raw
                    if str(value).strip()
                }
            )
        )
        out.append(
            StateRequirement(
                requirement_id=requirement_id,
                domain=_required_text(
                    item.get("domain"),
                    f"requirements[{index}].domain",
                ),
                key=_required_text(
                    item.get("key"),
                    f"requirements[{index}].key",
                ),
                accepted_confidences=accepted,
            )
        )
    return tuple(sorted(out, key=lambda item: item.requirement_id))


def _readiness(results: Sequence[StateRequirementResult]) -> str:
    statuses = {item.status for item in results}
    if "CONFLICTED" in statuses:
        return "CONFLICTED"
    if "MISSING" in statuses:
        return "PARTIAL_MISSING"
    if "INSUFFICIENT_CONFIDENCE" in statuses:
        return "INSUFFICIENT_CONFIDENCE"
    return "READY"


def audit_acquired_state_quality(
    state: AcquiredStateProfile,
    requirements: Sequence[StateRequirement],
) -> StateQualityReport:
    """Audit declared state requirements without imputing missing values."""

    assertions_by_key: dict[tuple[str, str], list[Any]] = {}
    for fact in state.assertions:
        assertions_by_key.setdefault((fact.domain, fact.key), []).append(fact)

    missing_by_key = {
        (item.domain, item.key): item for item in state.missingness
    }

    conflicts_by_key: dict[tuple[str, str], list[Any]] = {}
    for conflict in state.conflicts:
        conflicts_by_key.setdefault((conflict.domain, conflict.key), []).append(
            conflict
        )

    results: list[StateRequirementResult] = []
    for requirement in sorted(requirements, key=lambda item: item.requirement_id):
        key = (requirement.domain, requirement.key)
        facts = tuple(
            sorted(
                assertions_by_key.get(key, []),
                key=lambda item: item.fact_id,
            )
        )
        conflicts = tuple(
            sorted(
                conflicts_by_key.get(key, []),
                key=lambda item: item.conflict_id,
            )
        )
        missing = missing_by_key.get(key)

        if conflicts:
            status = "CONFLICTED"
        elif not facts:
            status = "MISSING"
        elif any(
            fact.confidence not in requirement.accepted_confidences
            for fact in facts
        ):
            status = "INSUFFICIENT_CONFIDENCE"
        else:
            status = "AVAILABLE"

        results.append(
            StateRequirementResult(
                requirement_id=requirement.requirement_id,
                domain=requirement.domain,
                key=requirement.key,
                status=status,
                fact_ids=tuple(fact.fact_id for fact in facts),
                observed_confidences=tuple(
                    sorted({fact.confidence for fact in facts})
                ),
                missingness_reason=missing.reason if missing else None,
                conflict_ids=tuple(
                    conflict.conflict_id for conflict in conflicts
                ),
            )
        )

    missingness_audit = tuple(
        sorted(
            (
                MissingnessAuditItem(
                    domain=item.domain,
                    key=item.key,
                    reason=item.reason,
                    audit_class=_MISSINGNESS_CLASS_BY_REASON[item.reason],
                    last_observed_date=(
                        item.last_observed_date.isoformat()
                        if item.last_observed_date
                        else None
                    ),
                )
                for item in state.missingness
            ),
            key=lambda item: (item.domain, item.key),
        )
    )

    unresolved_conflict_ids = tuple(
        sorted(item.conflict_id for item in state.conflicts)
    )
    low_confidence_fact_ids = tuple(
        sorted(
            item.fact_id
            for item in state.assertions
            if item.confidence in {"LOW", "INSUFFICIENT"}
        )
    )
    mnar_risk_keys = tuple(
        sorted(
            f"{item.domain}:{item.key}"
            for item in missingness_audit
            if item.audit_class == "WITHHELD_MNAR_RISK"
        )
    )

    return StateQualityReport(
        schema_version="0.1",
        state_id=state.state_id,
        readiness=_readiness(results),
        requirements=tuple(results),
        missingness_audit=missingness_audit,
        unresolved_conflict_ids=unresolved_conflict_ids,
        low_confidence_fact_ids=low_confidence_fact_ids,
        mnar_risk_keys=mnar_risk_keys,
    )

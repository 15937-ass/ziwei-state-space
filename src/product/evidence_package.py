"""Product-facing evidence contract.

The contract transports already-resolved chart facts and research evidence to
a language model or UI. It does not perform Zi Wei inference by itself.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


class ConfidenceBand(str, Enum):
    HIGH_CONFIDENCE = "HIGH_CONFIDENCE"
    MEDIUM_CONFIDENCE = "MEDIUM_CONFIDENCE"
    LOW_CONFIDENCE = "LOW_CONFIDENCE"
    CONFLICTED = "CONFLICTED"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"


@dataclass(frozen=True)
class EvidenceItem:
    rule_id: str
    claim: str
    source_id: str
    source_location: str
    epistemic: str
    review_status: str

    def validate(self) -> None:
        if not self.rule_id.strip():
            raise ValueError("EvidenceItem.rule_id is required")
        if not self.claim.strip():
            raise ValueError("EvidenceItem.claim is required")
        if not self.source_id.strip():
            raise ValueError("EvidenceItem.source_id is required")
        if not self.review_status.strip():
            raise ValueError("EvidenceItem.review_status is required")


@dataclass(frozen=True)
class ConflictItem:
    conflict_id: str
    description: str
    rule_ids: tuple[str, ...] = ()

    def validate(self) -> None:
        if not self.conflict_id.strip():
            raise ValueError("ConflictItem.conflict_id is required")
        if len(self.rule_ids) < 2:
            raise ValueError("ConflictItem requires at least two rule_ids")


@dataclass(frozen=True)
class ContrastiveItem:
    """Why an executable candidate did not activate.

    This is a deterministic gate report, not a free-form counterfactual
    prediction.
    """

    rule_id: str
    candidate_claim: str
    missing_all_of: tuple[str, ...] = ()
    unsatisfied_any_of: tuple[tuple[str, ...], ...] = ()
    blocked_by: tuple[str, ...] = ()
    missing_antecedents: tuple[str, ...] = ()

    def validate(self) -> None:
        if not self.rule_id.strip():
            raise ValueError("ContrastiveItem.rule_id is required")
        if not self.candidate_claim.strip():
            raise ValueError("ContrastiveItem.candidate_claim is required")


@dataclass
class EvidencePackage:
    question: str
    chart_facts: dict[str, Any] = field(default_factory=dict)
    active_rules: list[EvidenceItem] = field(default_factory=list)
    latent_states: dict[str, Any] = field(default_factory=dict)
    active_modes: list[dict[str, Any]] = field(default_factory=list)
    projections: list[dict[str, Any]] = field(default_factory=list)
    history_state: dict[str, Any] = field(default_factory=dict)
    conflicts: list[ConflictItem] = field(default_factory=list)
    contrastive: list[ContrastiveItem] = field(default_factory=list)
    alternative_interpretations: list[str] = field(default_factory=list)
    coverage: dict[str, Any] = field(default_factory=dict)
    confidence_band: ConfidenceBand = ConfidenceBand.INSUFFICIENT_EVIDENCE
    confidence_rationale: str = ""
    engine_version: str = ""
    knowledge_version: str = ""

    def validate(self) -> None:
        if not self.question.strip():
            raise ValueError("EvidencePackage.question is required")
        for item in self.active_rules:
            item.validate()
        for item in self.conflicts:
            item.validate()
        for item in self.contrastive:
            item.validate()

        if self.confidence_band is ConfidenceBand.HIGH_CONFIDENCE and not self.active_rules:
            raise ValueError("HIGH_CONFIDENCE requires at least one active evidence rule")
        if self.confidence_band is ConfidenceBand.CONFLICTED and not self.conflicts:
            raise ValueError("CONFLICTED requires at least one explicit conflict")

    def to_dict(self) -> dict[str, Any]:
        self.validate()
        payload = asdict(self)
        payload["confidence_band"] = self.confidence_band.value
        return payload

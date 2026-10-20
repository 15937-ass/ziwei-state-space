"""Fail-closed contract for social-platform Zi Wei quick reads.

This module does not infer Zi Wei claims. It accepts only already-resolved,
source-traceable Zhongzhou claims and prepares a narrow payload for an LLM
verbalizer. The verbalizer never receives raw chart facts or source books as a
license to invent additional claims.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Iterable


class QuickReadTopic(str, Enum):
    PERSONALITY = "personality"
    APPEARANCE = "appearance"
    BODY_TYPE = "body_type"
    HOBBIES = "hobbies"
    PEERS = "peers"
    TEACHERS_ELDERS = "teachers_elders"
    PARENTS = "parents"
    RELATIONSHIP_PATTERN = "relationship_pattern"
    CURRENT_RELATIONSHIP = "current_relationship"
    PARTNER_PREFERENCE = "partner_preference"
    STUDY_WORK = "study_work"
    SPECIFIC_YEAR = "specific_year"
    DECADE_TREND = "decade_trend"


class AssertionMode(str, Enum):
    DIRECT_TENDENCY = "DIRECT_TENDENCY"
    TENDENCY = "TENDENCY"
    CONDITIONAL = "CONDITIONAL"


class EvidenceNamespace(str, Enum):
    CANONICAL = "CANONICAL"
    TEMPORAL = "TEMPORAL"


TEMPORAL_TOPICS = {
    QuickReadTopic.CURRENT_RELATIONSHIP,
    QuickReadTopic.SPECIFIC_YEAR,
    QuickReadTopic.DECADE_TREND,
}


@dataclass(frozen=True)
class QuickReadEvidenceRef:
    namespace: EvidenceNamespace
    rule_id: str
    source_id: str
    source_location: str
    review_status: str
    school: str = "ZHONGZHOU"

    def validate(self) -> None:
        for value, name in (
            (self.rule_id, "rule_id"),
            (self.source_id, "source_id"),
            (self.source_location, "source_location"),
            (self.review_status, "review_status"),
        ):
            if not str(value).strip():
                raise ValueError(f"QuickReadEvidenceRef.{name} is required")
        if self.school != "ZHONGZHOU":
            raise ValueError("Social QuickRead v0.1 only accepts ZHONGZHOU evidence")


@dataclass(frozen=True)
class QuickReadClaim:
    claim_id: str
    topic: QuickReadTopic
    proposition: str
    assertion_mode: AssertionMode
    evidence_refs: tuple[QuickReadEvidenceRef, ...]
    target_period: str = ""

    def validate(self) -> None:
        if not self.claim_id.strip():
            raise ValueError("QuickReadClaim.claim_id is required")
        if not self.proposition.strip():
            raise ValueError("QuickReadClaim.proposition is required")
        if not self.evidence_refs:
            raise ValueError("QuickReadClaim requires at least one evidence ref")
        for item in self.evidence_refs:
            item.validate()

        namespaces = {item.namespace for item in self.evidence_refs}
        if self.topic in TEMPORAL_TOPICS:
            if EvidenceNamespace.TEMPORAL not in namespaces:
                raise ValueError(f"{self.topic.value} requires TEMPORAL evidence")
            if not self.target_period.strip():
                raise ValueError(f"{self.topic.value} requires target_period")

        if self.topic is QuickReadTopic.CURRENT_RELATIONSHIP:
            if self.assertion_mode is AssertionMode.DIRECT_TENDENCY:
                raise ValueError(
                    "current_relationship cannot be rendered as a direct fact from symbolic evidence"
                )


@dataclass(frozen=True)
class QuickReadPackage:
    claims: tuple[QuickReadClaim, ...]
    knowledge_version: str
    language: str = "zh-CN"
    target_chars_min: int = 120
    target_chars_max: int = 220

    def validate(self) -> None:
        if not self.knowledge_version.strip():
            raise ValueError("QuickReadPackage.knowledge_version is required")
        if not self.claims:
            raise ValueError("QuickReadPackage requires at least one claim")
        claim_ids = [item.claim_id for item in self.claims]
        if len(claim_ids) != len(set(claim_ids)):
            raise ValueError("QuickReadPackage.claim_id values must be unique")
        if self.target_chars_min < 80 or self.target_chars_max > 280:
            raise ValueError("quick-read length bounds are outside the supported social range")
        if self.target_chars_min >= self.target_chars_max:
            raise ValueError("target_chars_min must be less than target_chars_max")
        for item in self.claims:
            item.validate()

    def verbalizer_payload(self) -> dict[str, Any]:
        """Return only approved semantic claims plus style constraints.

        Source refs are validated upstream but deliberately omitted from the LLM
        payload. Raw chart facts, palace contents and source prose are also absent.
        This makes unsupported claim creation easier to detect and harder to prompt.
        """
        self.validate()
        return {
            "mode": "social_quickread_v0.1",
            "language": self.language,
            "length": {
                "min_chars": self.target_chars_min,
                "max_chars": self.target_chars_max,
            },
            "claims": [
                {
                    "claim_id": claim.claim_id,
                    "topic": claim.topic.value,
                    "proposition": claim.proposition,
                    "assertion_mode": claim.assertion_mode.value,
                    "target_period": claim.target_period or None,
                }
                for claim in self.claims
            ],
            "style_contract": {
                "single_paragraph": True,
                "no_headings": True,
                "no_bullets": True,
                "hide_astrology_jargon": True,
                "do_not_add_claims": True,
                "prefer_plain_spoken_chinese": True,
                "default_opening": "整体看",
                "hedges_only_when_needed": True,
            },
        }


FORBIDDEN_SURFACE_TOKENS = (
    "RULE_",
    "EvidencePackage",
    "source_id",
    "confidence_band",
    "根据紫微斗数",
    "综上所述",
    "命主",
    "此人",
)

HEDGE_TOKENS = ("可能", "大概率", "应该", "我会猜", "感觉")


def lint_rendered_text(
    text: str,
    *,
    min_chars: int = 120,
    max_chars: int = 220,
) -> tuple[str, ...]:
    """Return deterministic style warnings; this function does not rewrite text."""
    value = str(text or "").strip()
    warnings: list[str] = []
    if len(value) < min_chars:
        warnings.append("TEXT_TOO_SHORT")
    if len(value) > max_chars:
        warnings.append("TEXT_TOO_LONG")
    if "\n#" in value or value.startswith("#"):
        warnings.append("MARKDOWN_HEADING_FORBIDDEN")
    if any(
        line.lstrip().startswith(("- ", "* ", "1. ", "2. "))
        for line in value.splitlines()
    ):
        warnings.append("LIST_FORMAT_FORBIDDEN")
    for token in FORBIDDEN_SURFACE_TOKENS:
        if token in value:
            warnings.append(f"FORBIDDEN_TOKEN:{token}")
    hedge_count = sum(value.count(token) for token in HEDGE_TOKENS)
    if hedge_count > 5:
        warnings.append("OVER_HEDGED")
    return tuple(warnings)


def evidence_rule_ids(claims: Iterable[QuickReadClaim]) -> tuple[str, ...]:
    """Expose trace IDs for debug/audit without sending them to the verbalizer."""
    return tuple(
        sorted(
            {
                ref.rule_id
                for claim in claims
                for ref in claim.evidence_refs
            }
        )
    )

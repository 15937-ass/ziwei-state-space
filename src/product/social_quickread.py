"""Fail-closed contract for social-platform Zi Wei quick reads.

This module does not infer Zi Wei claims. It accepts only already-resolved,
source-traceable Zhongzhou claims and prepares a narrow payload for an LLM
verbalizer. A separate conversation-context capsule can keep the full validated
session available for follow-up questions without granting the LLM authority to
invent new Zi Wei claims from raw chart facts.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Iterable, Mapping


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


class QuickReadDomain(str, Enum):
    PERSONALITY = "personality"
    APPEARANCE = "appearance"
    SOCIAL = "social"
    FAMILY = "family"
    RELATIONSHIP = "relationship"
    STUDY_WORK = "study_work"
    WEALTH = "wealth"
    GENERAL = "general"


class QuickReadScopePreset(str, Enum):
    FULL = "full"
    RELATIONSHIP = "relationship"
    PERSONALITY = "personality"
    APPEARANCE = "appearance"
    SOCIAL = "social"
    FAMILY = "family"
    STUDY_WORK = "study_work"
    CUSTOM = "custom"


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


TOPIC_DEFAULT_DOMAINS: dict[QuickReadTopic, tuple[QuickReadDomain, ...]] = {
    QuickReadTopic.PERSONALITY: (QuickReadDomain.PERSONALITY,),
    QuickReadTopic.APPEARANCE: (QuickReadDomain.APPEARANCE,),
    QuickReadTopic.BODY_TYPE: (QuickReadDomain.APPEARANCE,),
    QuickReadTopic.HOBBIES: (QuickReadDomain.PERSONALITY,),
    QuickReadTopic.PEERS: (QuickReadDomain.SOCIAL,),
    QuickReadTopic.TEACHERS_ELDERS: (QuickReadDomain.SOCIAL,),
    QuickReadTopic.PARENTS: (QuickReadDomain.FAMILY,),
    QuickReadTopic.RELATIONSHIP_PATTERN: (QuickReadDomain.RELATIONSHIP,),
    QuickReadTopic.CURRENT_RELATIONSHIP: (QuickReadDomain.RELATIONSHIP,),
    QuickReadTopic.PARTNER_PREFERENCE: (QuickReadDomain.RELATIONSHIP,),
    QuickReadTopic.STUDY_WORK: (QuickReadDomain.STUDY_WORK,),
    QuickReadTopic.SPECIFIC_YEAR: (QuickReadDomain.GENERAL,),
    QuickReadTopic.DECADE_TREND: (QuickReadDomain.GENERAL,),
}


PRESET_DOMAINS: dict[QuickReadScopePreset, tuple[QuickReadDomain, ...]] = {
    QuickReadScopePreset.FULL: tuple(QuickReadDomain),
    QuickReadScopePreset.RELATIONSHIP: (QuickReadDomain.RELATIONSHIP,),
    QuickReadScopePreset.PERSONALITY: (QuickReadDomain.PERSONALITY,),
    QuickReadScopePreset.APPEARANCE: (QuickReadDomain.APPEARANCE,),
    QuickReadScopePreset.SOCIAL: (QuickReadDomain.SOCIAL,),
    QuickReadScopePreset.FAMILY: (QuickReadDomain.FAMILY,),
    QuickReadScopePreset.STUDY_WORK: (QuickReadDomain.STUDY_WORK,),
    QuickReadScopePreset.CUSTOM: (),
}


PILOT_SCOPE_ALIASES: dict[str, QuickReadScopePreset] = {
    "全盘": QuickReadScopePreset.FULL,
    "简批": QuickReadScopePreset.FULL,
    "整体": QuickReadScopePreset.FULL,
    "感情": QuickReadScopePreset.RELATIONSHIP,
    "恋爱": QuickReadScopePreset.RELATIONSHIP,
    "婚恋": QuickReadScopePreset.RELATIONSHIP,
    "性格": QuickReadScopePreset.PERSONALITY,
    "长相": QuickReadScopePreset.APPEARANCE,
    "外貌": QuickReadScopePreset.APPEARANCE,
    "人际": QuickReadScopePreset.SOCIAL,
    "朋友": QuickReadScopePreset.SOCIAL,
    "父母": QuickReadScopePreset.FAMILY,
    "家庭": QuickReadScopePreset.FAMILY,
    "事业": QuickReadScopePreset.STUDY_WORK,
    "工作": QuickReadScopePreset.STUDY_WORK,
    "学业": QuickReadScopePreset.STUDY_WORK,
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
    domains: tuple[QuickReadDomain, ...] = ()

    def resolved_domains(self) -> tuple[QuickReadDomain, ...]:
        return self.domains or TOPIC_DEFAULT_DOMAINS[self.topic]

    def validate(self) -> None:
        if not self.claim_id.strip():
            raise ValueError("QuickReadClaim.claim_id is required")
        if not self.proposition.strip():
            raise ValueError("QuickReadClaim.proposition is required")
        if not self.evidence_refs:
            raise ValueError("QuickReadClaim requires at least one evidence ref")
        for item in self.evidence_refs:
            item.validate()

        if len(set(self.resolved_domains())) != len(self.resolved_domains()):
            raise ValueError("QuickReadClaim.domains must be unique")

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
class QuickReadScope:
    preset: QuickReadScopePreset = QuickReadScopePreset.FULL
    include_domains: tuple[QuickReadDomain, ...] = ()
    include_topics: tuple[QuickReadTopic, ...] = ()
    period_labels: tuple[str, ...] = ()
    max_claims: int = 6

    def validate(self) -> None:
        if self.max_claims < 1 or self.max_claims > 12:
            raise ValueError("QuickReadScope.max_claims must be between 1 and 12")
        if len(set(self.include_domains)) != len(self.include_domains):
            raise ValueError("QuickReadScope.include_domains must be unique")
        if len(set(self.include_topics)) != len(self.include_topics):
            raise ValueError("QuickReadScope.include_topics must be unique")
        if len(set(self.period_labels)) != len(self.period_labels):
            raise ValueError("QuickReadScope.period_labels must be unique")
        if (
            self.preset is QuickReadScopePreset.CUSTOM
            and not self.include_domains
            and not self.include_topics
        ):
            raise ValueError("CUSTOM scope requires include_domains or include_topics")

    def active_domains(self) -> tuple[QuickReadDomain, ...]:
        preset_domains = PRESET_DOMAINS[self.preset]
        if self.preset is QuickReadScopePreset.CUSTOM:
            return self.include_domains
        if not self.include_domains:
            return preset_domains
        return tuple(dict.fromkeys((*preset_domains, *self.include_domains)))

    def allows(self, claim: QuickReadClaim) -> bool:
        self.validate()
        claim.validate()
        active_domains = set(self.active_domains())
        if active_domains and not active_domains.intersection(claim.resolved_domains()):
            return False
        if self.include_topics and claim.topic not in set(self.include_topics):
            return False
        if self.period_labels and claim.target_period:
            if claim.target_period not in set(self.period_labels):
                return False
        return True


@dataclass(frozen=True)
class QuickReadPackage:
    claims: tuple[QuickReadClaim, ...]
    knowledge_version: str
    scope: QuickReadScope = field(default_factory=QuickReadScope)
    language: str = "zh-CN"
    target_chars_min: int = 120
    target_chars_max: int = 220

    def selected_claims(self) -> tuple[QuickReadClaim, ...]:
        self.scope.validate()
        selected = tuple(claim for claim in self.claims if self.scope.allows(claim))
        return selected[: self.scope.max_claims]

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
        self.scope.validate()
        for item in self.claims:
            item.validate()
        if not self.selected_claims():
            raise ValueError("QuickReadPackage scope selects no supported claims")

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
            "scope": {
                "preset": self.scope.preset.value,
                "domains": [item.value for item in self.scope.active_domains()],
                "topics": [item.value for item in self.scope.include_topics],
                "period_labels": list(self.scope.period_labels),
            },
            "length": {
                "min_chars": self.target_chars_min,
                "max_chars": self.target_chars_max,
            },
            "claims": [
                {
                    "claim_id": claim.claim_id,
                    "topic": claim.topic.value,
                    "domains": [item.value for item in claim.resolved_domains()],
                    "proposition": claim.proposition,
                    "assertion_mode": claim.assertion_mode.value,
                    "target_period": claim.target_period or None,
                }
                for claim in self.selected_claims()
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


@dataclass(frozen=True)
class QuickReadConversationContext:
    """Full validated handoff kept with the GPT conversation for follow-up work.

    Unlike verbalizer_payload(), this payload is intentionally rich: it keeps all
    validated candidate claims, evidence refs and structured chart/profile context.
    Raw source prose is still excluded. The context is not permission for free-form
    Zi Wei inference; new claims must still pass the canonical/temporal runtime.
    """

    subject_key: str
    knowledge_version: str
    all_claims: tuple[QuickReadClaim, ...]
    active_scope: QuickReadScope
    rendered_text: str
    chart_context: Mapping[str, Any] = field(default_factory=dict)
    natal_profile_ref: str = ""
    temporal_profile_refs: tuple[str, ...] = ()

    def validate(self) -> None:
        if not self.subject_key.strip():
            raise ValueError("QuickReadConversationContext.subject_key is required")
        if not self.knowledge_version.strip():
            raise ValueError("QuickReadConversationContext.knowledge_version is required")
        if not self.all_claims:
            raise ValueError("QuickReadConversationContext requires all_claims")
        self.active_scope.validate()
        for claim in self.all_claims:
            claim.validate()
        if not str(self.rendered_text or "").strip():
            raise ValueError("QuickReadConversationContext.rendered_text is required")

    def continuation_payload(self) -> dict[str, Any]:
        """Return the full reusable session capsule for the same GPT thread."""
        self.validate()
        selected_ids = {
            item.claim_id
            for item in QuickReadPackage(
                claims=self.all_claims,
                knowledge_version=self.knowledge_version,
                scope=self.active_scope,
            ).selected_claims()
        }
        return {
            "mode": "social_quickread_continuation_v0.1",
            "subject_key": self.subject_key,
            "knowledge_version": self.knowledge_version,
            "active_scope": {
                "preset": self.active_scope.preset.value,
                "domains": [item.value for item in self.active_scope.active_domains()],
                "topics": [item.value for item in self.active_scope.include_topics],
                "period_labels": list(self.active_scope.period_labels),
            },
            "rendered_text": self.rendered_text,
            "chart_context": dict(self.chart_context),
            "natal_profile_ref": self.natal_profile_ref or None,
            "temporal_profile_refs": list(self.temporal_profile_refs),
            "claims": [
                {
                    "claim_id": claim.claim_id,
                    "selected_in_last_render": claim.claim_id in selected_ids,
                    "topic": claim.topic.value,
                    "domains": [item.value for item in claim.resolved_domains()],
                    "proposition": claim.proposition,
                    "assertion_mode": claim.assertion_mode.value,
                    "target_period": claim.target_period or None,
                    "evidence_refs": [
                        {
                            "namespace": ref.namespace.value,
                            "rule_id": ref.rule_id,
                            "source_id": ref.source_id,
                            "source_location": ref.source_location,
                            "review_status": ref.review_status,
                            "school": ref.school,
                        }
                        for ref in claim.evidence_refs
                    ],
                }
                for claim in self.all_claims
            ],
            "continuation_policy": {
                "reuse_validated_claims_first": True,
                "new_claim_requires_runtime_evidence": True,
                "raw_chart_context_is_navigation_not_inference_authority": True,
                "source_prose_not_embedded": True,
            },
        }

    def package_for_scope(self, scope: QuickReadScope) -> QuickReadPackage:
        """Reuse the same validated session for a new user-selected focus window."""
        package = QuickReadPackage(
            claims=self.all_claims,
            knowledge_version=self.knowledge_version,
            scope=scope,
        )
        package.validate()
        return package


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


def resolve_pilot_scope(text: str) -> QuickReadScope:
    """Resolve a minimal Chinese pilot request such as '只看感情' or '事业简批'.

    The pilot intentionally stays simple: one recognized focus preset, otherwise
    FULL. Fine-grained custom topic/year filtering remains available through the
    explicit QuickReadScope API.
    """
    value = str(text or "").strip()
    for token, preset in PILOT_SCOPE_ALIASES.items():
        if token in value:
            return QuickReadScope(preset=preset)
    return QuickReadScope(preset=QuickReadScopePreset.FULL)


def build_pilot_package(
    *,
    claims: tuple[QuickReadClaim, ...],
    knowledge_version: str,
    request_text: str,
    target_chars_min: int = 120,
    target_chars_max: int = 220,
) -> QuickReadPackage:
    """Convenience entry point for the manual ChatGPT-assisted pilot."""
    package = QuickReadPackage(
        claims=claims,
        knowledge_version=knowledge_version,
        scope=resolve_pilot_scope(request_text),
        target_chars_min=target_chars_min,
        target_chars_max=target_chars_max,
    )
    package.validate()
    return package

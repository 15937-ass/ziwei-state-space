"""PL3-M context gate v0.1.

Builds an auditable N + E_t + S_t + A_t + C_t routing context while preserving
blind/personalized separation.  It does not route manifestations or compute
probabilities.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any, Mapping

from .acquired_state import AcquiredStateProfile
from .natal_prior import NatalStateProfile
from .state_quality import StateQualityReport
from .temporal_environment import TemporalEnvironmentProfile


CONTEXT_MODES = frozenset({"BLIND", "PERSONALIZED"})
PERSONALIZATION_READINESS = frozenset(
    {
        "NOT_REQUESTED",
        "READY",
        "QUALITY_NOT_PROVIDED",
        "ABSTAIN_MISSING",
        "ABSTAIN_CONFLICT",
        "ABSTAIN_CONFIDENCE",
    }
)


@dataclass(frozen=True)
class RoutingAction:
    action_id: str
    label: str
    status: str
    confidence: str
    action_date: str | None
    observation_refs: tuple[str, ...]


@dataclass(frozen=True)
class RoutingStateAssertion:
    fact_id: str
    domain: str
    key: str
    value: Any
    status: str
    confidence: str
    observation_refs: tuple[str, ...]


@dataclass(frozen=True)
class ManifestationRoutingContext:
    schema_version: str
    context_id: str
    mode: str
    natal_profile_id: str
    temporal_profile_id: str
    knowledge_version: str
    target_label: str
    person_key: str | None
    acquired_state_id: str | None
    state_as_of_date: str | None
    active_natal_rule_ids: tuple[str, ...]
    active_temporal_reaction_ids: tuple[str, ...]
    active_temporal_rule_ids: tuple[str, ...]
    state_assertions: tuple[RoutingStateAssertion, ...]
    actions: tuple[RoutingAction, ...]
    exposures: tuple[str, ...]
    external_factors: tuple[str, ...]
    counterparty_factors: tuple[str, ...]
    state_quality_readiness: str | None
    personalization_readiness: str
    abstention_reasons: tuple[str, ...]
    empirical_probability_used: bool = False

    def __post_init__(self) -> None:
        if self.schema_version != "0.1":
            raise ValueError("ManifestationRoutingContext schema_version must be 0.1")
        if self.mode not in CONTEXT_MODES:
            raise ValueError(f"unsupported context mode: {self.mode}")
        if self.personalization_readiness not in PERSONALIZATION_READINESS:
            raise ValueError(
                f"unsupported personalization_readiness: "
                f"{self.personalization_readiness}"
            )
        if self.empirical_probability_used:
            raise ValueError(
                "PL3-M context gate cannot use empirical manifestation probability"
            )

        has_personal = any(
            (
                self.person_key,
                self.acquired_state_id,
                self.state_as_of_date,
                self.state_assertions,
                self.actions,
                self.exposures,
                self.external_factors,
                self.counterparty_factors,
                self.state_quality_readiness,
            )
        )
        if self.mode == "BLIND" and has_personal:
            raise ValueError(
                "BLIND context cannot contain acquired personal state/action/context"
            )
        if self.mode == "BLIND" and self.personalization_readiness != "NOT_REQUESTED":
            raise ValueError(
                "BLIND context personalization_readiness must be NOT_REQUESTED"
            )
        if self.mode == "PERSONALIZED" and not self.acquired_state_id:
            raise ValueError("PERSONALIZED context requires acquired_state_id")

    def symbolic_rule_ids(self) -> tuple[str, ...]:
        return tuple(
            sorted(
                set(self.active_natal_rule_ids)
                | set(self.active_temporal_rule_ids)
            )
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "context_id": self.context_id,
            "mode": self.mode,
            "natal_profile_id": self.natal_profile_id,
            "temporal_profile_id": self.temporal_profile_id,
            "knowledge_version": self.knowledge_version,
            "target_label": self.target_label,
            "person_key": self.person_key,
            "acquired_state_id": self.acquired_state_id,
            "state_as_of_date": self.state_as_of_date,
            "active_natal_rule_ids": list(self.active_natal_rule_ids),
            "active_temporal_reaction_ids": list(
                self.active_temporal_reaction_ids
            ),
            "active_temporal_rule_ids": list(self.active_temporal_rule_ids),
            "state_assertions": [asdict(item) for item in self.state_assertions],
            "actions": [asdict(item) for item in self.actions],
            "exposures": list(self.exposures),
            "external_factors": list(self.external_factors),
            "counterparty_factors": list(self.counterparty_factors),
            "state_quality_readiness": self.state_quality_readiness,
            "personalization_readiness": self.personalization_readiness,
            "abstention_reasons": list(self.abstention_reasons),
            "empirical_probability_used": self.empirical_probability_used,
        }


def _natal_rule_ids(profile: NatalStateProfile) -> tuple[str, ...]:
    return tuple(
        sorted(
            {
                rule.rule_id
                for domain in profile.domains
                for rule in domain.active_rules
            }
        )
    )


def _personalization_readiness(
    quality: StateQualityReport | None,
) -> tuple[str, tuple[str, ...], str | None]:
    if quality is None:
        return (
            "QUALITY_NOT_PROVIDED",
            ("STATE_QUALITY_REPORT_NOT_PROVIDED",),
            None,
        )

    if quality.readiness == "READY":
        return ("READY", (), quality.readiness)
    if quality.readiness == "PARTIAL_MISSING":
        reasons = tuple(
            sorted(
                f"MISSING:{item.domain}:{item.key}"
                for item in quality.requirements
                if item.status == "MISSING"
            )
        )
        return (
            "ABSTAIN_MISSING",
            reasons or ("STATE_REQUIREMENT_MISSING",),
            quality.readiness,
        )
    if quality.readiness == "CONFLICTED":
        reasons = tuple(
            sorted(
                f"CONFLICT:{item.domain}:{item.key}"
                for item in quality.requirements
                if item.status == "CONFLICTED"
            )
        )
        return (
            "ABSTAIN_CONFLICT",
            reasons or ("UNRESOLVED_STATE_CONFLICT",),
            quality.readiness,
        )
    if quality.readiness == "INSUFFICIENT_CONFIDENCE":
        reasons = tuple(
            sorted(
                f"INSUFFICIENT_CONFIDENCE:{item.domain}:{item.key}"
                for item in quality.requirements
                if item.status == "INSUFFICIENT_CONFIDENCE"
            )
        )
        return (
            "ABSTAIN_CONFIDENCE",
            reasons or ("STATE_EVIDENCE_CONFIDENCE_INSUFFICIENT",),
            quality.readiness,
        )

    raise ValueError(f"unsupported StateQualityReport readiness: {quality.readiness}")


def _context_id(payload: Mapping[str, Any]) -> str:
    raw = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return "MCTX-" + hashlib.sha256(raw).hexdigest()[:24]


def build_manifestation_routing_context(
    natal_profile: NatalStateProfile,
    temporal_profile: TemporalEnvironmentProfile,
    *,
    mode: str,
    acquired_state: AcquiredStateProfile | None = None,
    state_quality: StateQualityReport | None = None,
) -> ManifestationRoutingContext:
    """Assemble one routing context without creating manifestation semantics."""

    normalized_mode = str(mode or "").strip()
    if normalized_mode not in CONTEXT_MODES:
        raise ValueError(f"unsupported context mode: {normalized_mode or '<empty>'}")

    if temporal_profile.natal_profile_id != natal_profile.profile_id:
        raise ValueError(
            "TemporalEnvironmentProfile does not belong to NatalStateProfile"
        )
    if temporal_profile.knowledge_version != natal_profile.knowledge_version:
        raise ValueError("natal/temporal knowledge_version mismatch")

    natal_rules = _natal_rule_ids(natal_profile)
    temporal_reactions = tuple(
        sorted(item.reaction_id for item in temporal_profile.reactions)
    )
    temporal_rules = tuple(
        sorted({item.rule_id for item in temporal_profile.reactions})
    )

    if normalized_mode == "BLIND":
        if acquired_state is not None or state_quality is not None:
            raise ValueError(
                "BLIND mode must not receive acquired_state or state_quality"
            )
        personal_readiness = "NOT_REQUESTED"
        abstention_reasons: tuple[str, ...] = ()
        quality_readiness = None
        person_key = None
        state_id = None
        state_as_of = None
        assertions: tuple[RoutingStateAssertion, ...] = ()
        actions: tuple[RoutingAction, ...] = ()
        exposures: tuple[str, ...] = ()
        external: tuple[str, ...] = ()
        counterparty: tuple[str, ...] = ()

    else:
        if acquired_state is None:
            raise ValueError("PERSONALIZED mode requires acquired_state")
        if state_quality is not None and state_quality.state_id != acquired_state.state_id:
            raise ValueError(
                "StateQualityReport does not belong to supplied AcquiredStateProfile"
            )

        (
            personal_readiness,
            abstention_reasons,
            quality_readiness,
        ) = _personalization_readiness(state_quality)

        person_key = acquired_state.person_key
        state_id = acquired_state.state_id
        state_as_of = acquired_state.as_of_date.isoformat()

        assertions = tuple(
            sorted(
                (
                    RoutingStateAssertion(
                        fact_id=item.fact_id,
                        domain=item.domain,
                        key=item.key,
                        value=item.value,
                        status=item.status,
                        confidence=item.confidence,
                        observation_refs=item.observation_refs,
                    )
                    for item in acquired_state.assertions
                ),
                key=lambda item: item.fact_id,
            )
        )
        actions = tuple(
            sorted(
                (
                    RoutingAction(
                        action_id=item.action_id,
                        label=item.label,
                        status=item.status,
                        confidence=item.confidence,
                        action_date=(
                            item.action_date.isoformat()
                            if item.action_date
                            else None
                        ),
                        observation_refs=item.observation_refs,
                    )
                    for item in acquired_state.actions
                ),
                key=lambda item: item.action_id,
            )
        )

        exposures = tuple(
            sorted(
                {
                    item.label
                    for item in acquired_state.context_items
                    if item.kind == "EXPOSURE" and item.status == "ACTIVE"
                }
            )
        )
        external = tuple(
            sorted(
                {
                    item.label
                    for item in acquired_state.context_items
                    if item.kind == "EXTERNAL" and item.status == "ACTIVE"
                }
            )
        )
        counterparty = tuple(
            sorted(
                {
                    item.label
                    for item in acquired_state.context_items
                    if item.kind == "COUNTERPARTY"
                    and item.status == "ACTIVE"
                }
            )
        )

    identity_payload = {
        "mode": normalized_mode,
        "natal_profile_id": natal_profile.profile_id,
        "temporal_profile_id": temporal_profile.profile_id,
        "knowledge_version": natal_profile.knowledge_version,
        "target_label": temporal_profile.target_label,
        "person_key": person_key,
        "acquired_state_id": state_id,
        "state_quality_readiness": quality_readiness,
        "personalization_readiness": personal_readiness,
        "active_natal_rule_ids": list(natal_rules),
        "active_temporal_reaction_ids": list(temporal_reactions),
        "active_temporal_rule_ids": list(temporal_rules),
        "abstention_reasons": list(abstention_reasons),
    }

    return ManifestationRoutingContext(
        schema_version="0.1",
        context_id=_context_id(identity_payload),
        mode=normalized_mode,
        natal_profile_id=natal_profile.profile_id,
        temporal_profile_id=temporal_profile.profile_id,
        knowledge_version=natal_profile.knowledge_version,
        target_label=temporal_profile.target_label,
        person_key=person_key,
        acquired_state_id=state_id,
        state_as_of_date=state_as_of,
        active_natal_rule_ids=natal_rules,
        active_temporal_reaction_ids=temporal_reactions,
        active_temporal_rule_ids=temporal_rules,
        state_assertions=assertions,
        actions=actions,
        exposures=exposures,
        external_factors=external,
        counterparty_factors=counterparty,
        state_quality_readiness=quality_readiness,
        personalization_readiness=personal_readiness,
        abstention_reasons=abstention_reasons,
    )

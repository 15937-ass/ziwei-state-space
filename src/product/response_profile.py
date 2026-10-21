"""PL3-R Career decade/year ResponseProfile compiler v0.1.

This compiler is deliberately sparse and fail-closed.  It combines:
- already evaluated NATAL Career conditions;
- an environment-only TemporalEnvironmentProfile;
- explicit source-backed DECADE/YEAR TemporalReactionEvidence.

It does not infer a temporal reaction from raw temporal facts, projection prose,
similar target names, or domain membership.  A temporal reaction may enter the
profile only when it explicitly names a matched natal rule in
`matched_natal_rule_ids`.

The output is a symbolic ResponseProfile tau.  It contains no probability,
numeric magnitude, learned weight, user feedback, acquired state, or
manifestation claim.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any, Mapping

from .natal_prior import NatalStateProfile
from .temporal_environment import (
    MAGNITUDE_STATUSES,
    REACTION_EFFECTS,
    TemporalEnvironmentProfile,
    TemporalReactionEvidence,
)


RESPONSE_PROFILE_SCHEMA_VERSION = "0.1"
RESPONSE_COMPILER_VERSION = "PL3R_DECADE_YEAR_RESPONSE_COMPILER_V0_1"
ALLOWED_RESPONSE_LAYERS = frozenset({"DECADE", "YEAR"})
CAREER_DOMAIN_ALIASES = frozenset({"career", "CAREER", "事业", "官禄"})


@dataclass(frozen=True)
class CareerResponseEntry:
    natal_rule_id: str
    condition_id: str
    temporal_reaction_id: str
    temporal_rule_id: str
    layer: str
    effect: str
    effect_target: str
    projection_domain: str
    projection_target: str
    magnitude_status: str
    natal_source_location: str
    natal_source_span_ids: tuple[str, ...]
    temporal_source_id: str
    temporal_source_location: str
    temporal_review_status: str
    matched_natal_facts: tuple[str, ...] = ()
    matched_temporal_facts: tuple[str, ...] = ()
    runtime_effect_allowed: bool = False

    def __post_init__(self) -> None:
        required = {
            "natal_rule_id": self.natal_rule_id,
            "condition_id": self.condition_id,
            "temporal_reaction_id": self.temporal_reaction_id,
            "temporal_rule_id": self.temporal_rule_id,
            "effect_target": self.effect_target,
            "projection_domain": self.projection_domain,
            "projection_target": self.projection_target,
            "natal_source_location": self.natal_source_location,
            "temporal_source_id": self.temporal_source_id,
            "temporal_source_location": self.temporal_source_location,
            "temporal_review_status": self.temporal_review_status,
        }
        missing = [name for name, value in required.items() if not str(value).strip()]
        if missing:
            raise ValueError("CareerResponseEntry missing: " + ", ".join(missing))
        if self.condition_id != f"PRODUCT_CONDITION:{self.natal_rule_id}":
            raise ValueError("response entry condition_id/natal_rule_id mismatch")
        if self.layer not in ALLOWED_RESPONSE_LAYERS:
            raise ValueError(f"response layer out of scope: {self.layer}")
        if self.effect not in REACTION_EFFECTS:
            raise ValueError(f"unsupported response effect: {self.effect}")
        if self.magnitude_status not in MAGNITUDE_STATUSES:
            raise ValueError(f"unsupported magnitude_status: {self.magnitude_status}")
        if not self.natal_source_span_ids:
            raise ValueError("natal source spans are required")
        if self.runtime_effect_allowed:
            raise ValueError("PL3-R v0.1 does not authorize runtime event effects")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CareerResponseProfile:
    schema_version: str
    profile_id: str
    compiler_version: str
    natal_profile_id: str
    temporal_profile_id: str
    knowledge_version: str
    target_label: str
    active_layers: tuple[str, ...]
    matched_natal_rule_ids: tuple[str, ...]
    entries: tuple[CareerResponseEntry, ...]
    unknowns: tuple[str, ...]
    status: str
    runtime_effect_allowed: bool = False
    probability_used: bool = False
    empirical_calibration_used: bool = False
    acquired_state_used: bool = False
    outcome_used: bool = False

    def __post_init__(self) -> None:
        if self.schema_version != RESPONSE_PROFILE_SCHEMA_VERSION:
            raise ValueError("CareerResponseProfile schema_version must be 0.1")
        for value, name in (
            (self.profile_id, "profile_id"),
            (self.compiler_version, "compiler_version"),
            (self.natal_profile_id, "natal_profile_id"),
            (self.temporal_profile_id, "temporal_profile_id"),
            (self.knowledge_version, "knowledge_version"),
            (self.target_label, "target_label"),
            (self.status, "status"),
        ):
            if not str(value).strip():
                raise ValueError(f"CareerResponseProfile.{name} is required")
        if tuple(sorted(self.active_layers)) != self.active_layers:
            raise ValueError("active_layers must be sorted")
        if not {"DECADE", "YEAR"}.issubset(set(self.active_layers)):
            raise ValueError("Career ResponseProfile v0.1 requires DECADE and YEAR")
        if self.status not in {"SOURCE_BACKED_SYMBOLIC_RESPONSE", "PARTIAL_UNKNOWN"}:
            raise ValueError(f"unsupported response profile status: {self.status}")
        forbidden = {
            "runtime_effect_allowed": self.runtime_effect_allowed,
            "probability_used": self.probability_used,
            "empirical_calibration_used": self.empirical_calibration_used,
            "acquired_state_used": self.acquired_state_used,
            "outcome_used": self.outcome_used,
        }
        active = [name for name, value in forbidden.items() if value]
        if active:
            raise ValueError(
                "PL3-R ResponseProfile must remain symbolic/source-only; "
                f"forbidden flags: {', '.join(active)}"
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "profile_id": self.profile_id,
            "compiler_version": self.compiler_version,
            "natal_profile_id": self.natal_profile_id,
            "temporal_profile_id": self.temporal_profile_id,
            "knowledge_version": self.knowledge_version,
            "target_label": self.target_label,
            "active_layers": list(self.active_layers),
            "matched_natal_rule_ids": list(self.matched_natal_rule_ids),
            "entries": [item.to_dict() for item in self.entries],
            "unknowns": list(self.unknowns),
            "status": self.status,
            "runtime_effect_allowed": self.runtime_effect_allowed,
            "probability_used": self.probability_used,
            "empirical_calibration_used": self.empirical_calibration_used,
            "acquired_state_used": self.acquired_state_used,
            "outcome_used": self.outcome_used,
        }


def _required_text(value: Any, field: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise ValueError(f"{field} is required")
    return text


def _evaluation_index(
    evaluation_report: Mapping[str, Any],
) -> dict[str, Mapping[str, Any]]:
    scope = evaluation_report.get("scope")
    if not isinstance(scope, Mapping):
        raise ValueError("Career condition evaluation scope is required")
    if str(scope.get("domain", "")).strip().lower() != "career":
        raise ValueError("Response compiler requires Career condition evaluation")
    if str(scope.get("time_layer", "")).strip() != "NATAL":
        raise ValueError("Response compiler requires NATAL condition evaluation")

    evaluations = evaluation_report.get("evaluations")
    if not isinstance(evaluations, list) or len(evaluations) != 12:
        raise ValueError("Response compiler requires exact 12 Career evaluations")

    out: dict[str, Mapping[str, Any]] = {}
    for row in evaluations:
        if not isinstance(row, Mapping):
            raise ValueError("Career condition evaluation row must be an object")
        rule_id = _required_text(row.get("source_rule_id"), "source_rule_id")
        if rule_id in out:
            raise ValueError(f"duplicate Career evaluation: {rule_id}")
        expected_condition = f"PRODUCT_CONDITION:{rule_id}"
        if str(row.get("condition_id", "")).strip() != expected_condition:
            raise ValueError(f"{rule_id}: condition_id mismatch")
        if bool(row.get("runtime_effect_allowed", False)):
            raise ValueError(f"{rule_id}: upstream runtime effect may not be true")
        if bool(row.get("matched", False)):
            binding = row.get("effect_binding")
            if not isinstance(binding, Mapping):
                raise ValueError(f"{rule_id}: matched condition requires effect binding")
            if not bool(row.get("response_effect_bound", False)):
                raise ValueError(f"{rule_id}: matched effect must be source-bound")
        out[rule_id] = row

    if len(out) != 12:
        raise ValueError("Career evaluation ID census drift")
    return out


def _is_career_domain(value: str) -> bool:
    return str(value or "").strip() in CAREER_DOMAIN_ALIASES


def _reaction_unknown(
    reaction: TemporalReactionEvidence,
    suffix: str,
) -> str:
    return f"{suffix}:{reaction.reaction_id}"


def _entry_from(
    evaluation: Mapping[str, Any],
    reaction: TemporalReactionEvidence,
) -> CareerResponseEntry:
    rule_id = str(evaluation["source_rule_id"]).strip()
    binding = evaluation.get("effect_binding")
    if not isinstance(binding, Mapping):
        raise ValueError(f"{rule_id}: response entry requires effect binding")

    spans = binding.get("source_span_ids")
    if not isinstance(spans, list) or not spans:
        raise ValueError(f"{rule_id}: natal source_span_ids are required")

    return CareerResponseEntry(
        natal_rule_id=rule_id,
        condition_id=str(evaluation["condition_id"]).strip(),
        temporal_reaction_id=reaction.reaction_id,
        temporal_rule_id=reaction.rule_id,
        layer=reaction.layer,
        effect=reaction.effect,
        effect_target=reaction.target,
        projection_domain=_required_text(
            binding.get("projection_domain"), f"{rule_id}.projection_domain"
        ),
        projection_target=_required_text(
            binding.get("projection_target"), f"{rule_id}.projection_target"
        ),
        magnitude_status=reaction.magnitude_status,
        natal_source_location=_required_text(
            binding.get("source_location"), f"{rule_id}.source_location"
        ),
        natal_source_span_ids=tuple(str(item).strip() for item in spans),
        temporal_source_id=reaction.source_id,
        temporal_source_location=reaction.source_location,
        temporal_review_status=reaction.review_status,
        matched_natal_facts=tuple(sorted(reaction.matched_natal_facts)),
        matched_temporal_facts=tuple(sorted(reaction.matched_temporal_facts)),
    )


def _profile_id(
    *,
    natal_profile_id: str,
    temporal_profile_id: str,
    knowledge_version: str,
    target_label: str,
    active_layers: tuple[str, ...],
    matched_natal_rule_ids: tuple[str, ...],
    entries: tuple[CareerResponseEntry, ...],
    unknowns: tuple[str, ...],
    status: str,
) -> str:
    payload = {
        "natal_profile_id": natal_profile_id,
        "temporal_profile_id": temporal_profile_id,
        "knowledge_version": knowledge_version,
        "target_label": target_label,
        "active_layers": list(active_layers),
        "matched_natal_rule_ids": list(matched_natal_rule_ids),
        "entries": [item.to_dict() for item in entries],
        "unknowns": list(unknowns),
        "status": status,
    }
    raw = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return "TAU-" + hashlib.sha256(raw).hexdigest()[:24]


def build_career_response_profile(
    natal_profile: NatalStateProfile,
    evaluation_report: Mapping[str, Any],
    temporal_profile: TemporalEnvironmentProfile,
) -> CareerResponseProfile:
    """Compile a sparse source-backed Career ResponseProfile tau.

    Raw temporal facts are never interpreted here.  Only already-normalized
    TemporalReactionEvidence with an explicit matched_natal_rule_ids link may
    create a response entry.
    """

    if temporal_profile.natal_profile_id != natal_profile.profile_id:
        raise ValueError("Temporal/Natal profile lineage mismatch")
    if temporal_profile.knowledge_version != natal_profile.knowledge_version:
        raise ValueError("Temporal/Natal knowledge_version mismatch")

    active_layers = tuple(sorted(set(temporal_profile.active_layers)))
    if not {"DECADE", "YEAR"}.issubset(set(active_layers)):
        raise ValueError("Career ResponseProfile v0.1 requires DECADE and YEAR")

    evaluations = _evaluation_index(evaluation_report)
    matched_natal_ids = tuple(
        sorted(
            rule_id
            for rule_id, row in evaluations.items()
            if bool(row.get("matched", False))
        )
    )

    entries: list[CareerResponseEntry] = []
    unknowns: set[str] = set()

    for reaction in sorted(
        temporal_profile.reactions,
        key=lambda item: (
            item.layer,
            item.reaction_id,
            item.rule_id,
            item.target,
        ),
    ):
        if not _is_career_domain(reaction.domain):
            unknowns.add(_reaction_unknown(reaction, "REACTION_DOMAIN_OUT_OF_SCOPE"))
            continue
        if reaction.layer not in ALLOWED_RESPONSE_LAYERS:
            unknowns.add(_reaction_unknown(reaction, "REACTION_LAYER_OUT_OF_SCOPE"))
            continue
        links = tuple(sorted(set(reaction.matched_natal_rule_ids)))
        if not links:
            unknowns.add(
                _reaction_unknown(reaction, "REACTION_WITHOUT_EXPLICIT_NATAL_LINK")
            )
            continue

        matched_any = False
        for natal_rule_id in links:
            evaluation = evaluations.get(natal_rule_id)
            if evaluation is None:
                unknowns.add(
                    f"REACTION_UNKNOWN_NATAL_RULE:{reaction.reaction_id}:{natal_rule_id}"
                )
                continue
            if not bool(evaluation.get("matched", False)):
                unknowns.add(
                    f"REACTION_NATAL_CONDITION_NOT_MATCHED:"
                    f"{reaction.reaction_id}:{natal_rule_id}"
                )
                continue
            entries.append(_entry_from(evaluation, reaction))
            matched_any = True

        if not matched_any and not links:
            unknowns.add(_reaction_unknown(reaction, "REACTION_NOT_COMPILED"))

    entry_items = tuple(
        sorted(
            entries,
            key=lambda item: (
                item.layer,
                item.natal_rule_id,
                item.temporal_reaction_id,
                item.effect,
                item.effect_target,
            ),
        )
    )

    if not temporal_profile.reactions:
        unknowns.add("PRODUCTION_TEMPORAL_RESPONSE_NOT_AVAILABLE")
    if not entry_items:
        unknowns.add("NO_SOURCE_BACKED_DECADE_YEAR_RESPONSE")

    unknown_items = tuple(sorted(unknowns))
    status = (
        "SOURCE_BACKED_SYMBOLIC_RESPONSE"
        if entry_items
        else "PARTIAL_UNKNOWN"
    )

    profile_id = _profile_id(
        natal_profile_id=natal_profile.profile_id,
        temporal_profile_id=temporal_profile.profile_id,
        knowledge_version=natal_profile.knowledge_version,
        target_label=temporal_profile.target_label,
        active_layers=active_layers,
        matched_natal_rule_ids=matched_natal_ids,
        entries=entry_items,
        unknowns=unknown_items,
        status=status,
    )

    return CareerResponseProfile(
        schema_version=RESPONSE_PROFILE_SCHEMA_VERSION,
        profile_id=profile_id,
        compiler_version=RESPONSE_COMPILER_VERSION,
        natal_profile_id=natal_profile.profile_id,
        temporal_profile_id=temporal_profile.profile_id,
        knowledge_version=natal_profile.knowledge_version,
        target_label=temporal_profile.target_label,
        active_layers=active_layers,
        matched_natal_rule_ids=matched_natal_ids,
        entries=entry_items,
        unknowns=unknown_items,
        status=status,
    )

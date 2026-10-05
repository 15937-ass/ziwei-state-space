"""PL3-T source-gated natal x temporal reaction compiler.

The compiler consumes only an explicitly normalized reaction registry. It never
parses WP05 free-form condition prose into executable semantics.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from .condition_atoms import CompiledCondition, compile_condition_spec, fact_from_atom
from .natal_prior import NatalStateProfile
from .temporal_asset_adapter import TemporalAssetBundle
from .temporal_environment import (
    MAGNITUDE_STATUSES,
    REACTION_EFFECTS,
    TEMPORAL_LAYERS,
    TemporalReactionEvidence,
)


ALLOWED_REACTION_REVIEW = frozenset({"SOURCE_SPAN_VERIFIED", "HUMAN_VERIFIED"})
ALLOWED_REACTION_NORMALIZATION = frozenset(
    {"SOURCE_PRESERVING", "INFERRED", "IMPLEMENTATION"}
)


@dataclass(frozen=True)
class TemporalReactionRuleSpec:
    reaction_id: str
    rule_id: str
    layer: str
    domain: str
    target: str
    effect: str
    source_id: str
    source_location: str
    review_status: str
    normalization_epistemic: str
    magnitude_status: str
    required_natal_rule_ids: tuple[str, ...]
    natal_condition: CompiledCondition
    temporal_condition: CompiledCondition


@dataclass(frozen=True)
class ReactionMatchIssue:
    rule_id: str
    reason: str


@dataclass(frozen=True)
class TemporalReactionMatchReport:
    matched: tuple[TemporalReactionEvidence, ...]
    issues: tuple[ReactionMatchIssue, ...]

    def counts(self) -> dict[str, int]:
        counts: dict[str, int] = {"MATCHED": len(self.matched)}
        for issue in self.issues:
            counts[issue.reason] = counts.get(issue.reason, 0) + 1
        return counts


def _required_text(value: Any, field: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise ValueError(f"{field} is required")
    return text


def _truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def _positive_atom_count(spec: Mapping[str, Any]) -> int:
    count = 0
    all_of = spec.get("all_of", [])
    if isinstance(all_of, list):
        count += len(all_of)
    any_of = spec.get("any_of", [])
    if isinstance(any_of, list):
        count += sum(len(group) for group in any_of if isinstance(group, list))
    alternatives = spec.get("alternatives", [])
    if isinstance(alternatives, list):
        count += sum(len(group) for group in alternatives if isinstance(group, list))
    return count


def _iter_condition_atoms(spec: Mapping[str, Any]):
    for key in ("all_of", "none_of"):
        values = spec.get(key, [])
        if isinstance(values, list):
            for atom in values:
                yield atom

    for key in ("any_of", "alternatives"):
        groups = spec.get(key, [])
        if isinstance(groups, list):
            for group in groups:
                if isinstance(group, list):
                    for atom in group:
                        yield atom


def _validate_temporal_atom_layers(
    *,
    rule_id: str,
    layer: str,
    spec: Mapping[str, Any],
) -> None:
    for atom in _iter_condition_atoms(spec):
        if not isinstance(atom, Mapping):
            raise ValueError(f"{rule_id}: temporal condition atom must be an object")
        args = atom.get("args")
        if not isinstance(args, Mapping):
            raise ValueError(f"{rule_id}: temporal condition atom args must be an object")
        atom_layer = str(args.get("layer", "")).strip()
        if atom_layer != layer:
            raise ValueError(
                f"{rule_id}: every temporal condition atom must carry "
                f"layer={layer}; got {atom_layer or '<missing>'}"
            )


def _required_rule_ids(value: Any, rule_id: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise ValueError(f"{rule_id}: required_natal_rule_ids must be an array")
    ids = tuple(sorted({str(item).strip() for item in value if str(item).strip()}))
    return ids


def compile_temporal_reaction_registry(
    document: Mapping[str, Any],
) -> tuple[TemporalReactionRuleSpec, ...]:
    if str(document.get("schema_version", "")).strip() != "0.1":
        raise ValueError("temporal reaction registry schema_version must be 0.1")

    raw_rules = document.get("rules")
    if not isinstance(raw_rules, list):
        raise ValueError("temporal reaction registry rules must be an array")

    compiled: list[TemporalReactionRuleSpec] = []
    seen_reaction_ids: set[str] = set()
    seen_rule_ids: set[str] = set()

    for index, row in enumerate(raw_rules):
        if not isinstance(row, Mapping):
            raise ValueError(f"rules[{index}] must be an object")

        reaction_id = _required_text(row.get("reaction_id"), f"rules[{index}].reaction_id")
        rule_id = _required_text(row.get("rule_id"), f"rules[{index}].rule_id")
        if reaction_id in seen_reaction_ids:
            raise ValueError(f"duplicate reaction_id: {reaction_id}")
        if rule_id in seen_rule_ids:
            raise ValueError(f"duplicate temporal reaction rule_id: {rule_id}")
        seen_reaction_ids.add(reaction_id)
        seen_rule_ids.add(rule_id)

        layer = _required_text(row.get("layer"), f"{rule_id}.layer")
        if layer not in TEMPORAL_LAYERS:
            raise ValueError(f"{rule_id}: unsupported temporal layer: {layer}")

        effect = _required_text(row.get("effect"), f"{rule_id}.effect")
        if effect not in REACTION_EFFECTS:
            raise ValueError(f"{rule_id}: unsupported reaction effect: {effect}")

        magnitude_status = str(row.get("magnitude_status") or "UNIDENTIFIED").strip()
        if magnitude_status not in MAGNITUDE_STATUSES:
            raise ValueError(
                f"{rule_id}: unsupported magnitude_status: {magnitude_status}"
            )

        review_status = _required_text(row.get("review_status"), f"{rule_id}.review_status")
        if review_status not in ALLOWED_REACTION_REVIEW or not _truthy(
            row.get("source_span_verified")
        ):
            raise ValueError(
                f"{rule_id}: reaction requires verified source span and "
                "SOURCE_SPAN_VERIFIED/HUMAN_VERIFIED review"
            )

        normalization_epistemic = _required_text(
            row.get("normalization_epistemic"),
            f"{rule_id}.normalization_epistemic",
        )
        if (
            normalization_epistemic not in ALLOWED_REACTION_NORMALIZATION
            or not _truthy(row.get("normalization_verified"))
        ):
            raise ValueError(
                f"{rule_id}: reaction requires verified non-hypothetical normalization"
            )

        if _truthy(row.get("case_support_only")):
            raise ValueError(
                f"{rule_id}: CASE_SUPPORT_ONLY rows cannot enter canonical reaction runtime"
            )

        natal_raw = row.get("natal_condition", {})
        temporal_raw = row.get("temporal_condition", {})
        if not isinstance(natal_raw, Mapping):
            raise ValueError(f"{rule_id}: natal_condition must be an object")
        if not isinstance(temporal_raw, Mapping):
            raise ValueError(f"{rule_id}: temporal_condition must be an object")

        required_natal_rule_ids = _required_rule_ids(
            row.get("required_natal_rule_ids"), rule_id
        )

        if _positive_atom_count(natal_raw) == 0 and not required_natal_rule_ids:
            raise ValueError(
                f"{rule_id}: reaction requires explicit natal antecedent facts "
                "or required_natal_rule_ids"
            )
        if _positive_atom_count(temporal_raw) == 0:
            raise ValueError(
                f"{rule_id}: reaction requires explicit positive temporal condition"
            )

        _validate_temporal_atom_layers(
            rule_id=rule_id,
            layer=layer,
            spec=temporal_raw,
        )

        compiled.append(
            TemporalReactionRuleSpec(
                reaction_id=reaction_id,
                rule_id=rule_id,
                layer=layer,
                domain=_required_text(row.get("domain"), f"{rule_id}.domain"),
                target=_required_text(row.get("target"), f"{rule_id}.target"),
                effect=effect,
                source_id=_required_text(row.get("source_id"), f"{rule_id}.source_id"),
                source_location=_required_text(
                    row.get("source_location"), f"{rule_id}.source_location"
                ),
                review_status=review_status,
                normalization_epistemic=normalization_epistemic,
                magnitude_status=magnitude_status,
                required_natal_rule_ids=required_natal_rule_ids,
                natal_condition=compile_condition_spec(natal_raw),
                temporal_condition=compile_condition_spec(temporal_raw),
            )
        )

    return tuple(sorted(compiled, key=lambda item: item.rule_id))


def _active_natal_rule_ids(profile: NatalStateProfile) -> frozenset[str]:
    ids: set[str] = set()
    for domain in profile.domains:
        for rule in domain.active_rules:
            ids.add(rule.rule_id)
    return frozenset(ids)


def _natal_fact_set(profile: NatalStateProfile) -> frozenset[str]:
    return frozenset(
        {
            *profile.canonical_facts,
            *profile.named_structure_facts,
        }
    )


def match_temporal_reactions(
    natal_profile: NatalStateProfile,
    bundle: TemporalAssetBundle,
    rules: Sequence[TemporalReactionRuleSpec],
) -> TemporalReactionMatchReport:
    natal_facts = _natal_fact_set(natal_profile)
    temporal_facts = frozenset(bundle.condition_facts)
    natal_rule_ids = _active_natal_rule_ids(natal_profile)

    matched: list[TemporalReactionEvidence] = []
    issues: list[ReactionMatchIssue] = []

    for rule in sorted(rules, key=lambda item: item.rule_id):
        missing_rule_ids = sorted(
            set(rule.required_natal_rule_ids) - set(natal_rule_ids)
        )
        if missing_rule_ids:
            issues.append(
                ReactionMatchIssue(rule.rule_id, "NATAL_RULE_ANTECEDENT_MISMATCH")
            )
            continue

        if not rule.natal_condition.matches(natal_facts):
            issues.append(
                ReactionMatchIssue(rule.rule_id, "NATAL_FACT_ANTECEDENT_MISMATCH")
            )
            continue

        layer_fact = fact_from_atom("TIME_LAYER", layer=rule.layer)
        if layer_fact not in temporal_facts:
            issues.append(
                ReactionMatchIssue(rule.rule_id, "TEMPORAL_LAYER_MISSING")
            )
            continue

        if not rule.temporal_condition.matches(temporal_facts):
            issues.append(
                ReactionMatchIssue(rule.rule_id, "TEMPORAL_FACT_ANTECEDENT_MISMATCH")
            )
            continue

        matched.append(
            TemporalReactionEvidence(
                reaction_id=rule.reaction_id,
                rule_id=rule.rule_id,
                layer=rule.layer,
                domain=rule.domain,
                target=rule.target,
                effect=rule.effect,
                source_id=rule.source_id,
                source_location=rule.source_location,
                review_status=rule.review_status,
                magnitude_status=rule.magnitude_status,
                matched_natal_facts=rule.natal_condition.matched_facts(natal_facts),
                matched_temporal_facts=rule.temporal_condition.matched_facts(
                    temporal_facts
                ),
                matched_natal_rule_ids=tuple(rule.required_natal_rule_ids),
            )
        )

    return TemporalReactionMatchReport(
        matched=tuple(
            sorted(
                matched,
                key=lambda item: (item.layer, item.domain, item.target, item.rule_id),
            )
        ),
        issues=tuple(sorted(issues, key=lambda item: (item.rule_id, item.reason))),
    )

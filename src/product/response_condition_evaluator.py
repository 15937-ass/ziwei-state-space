"""PL3-R Career condition evaluator + semantic effect-binding pilot v0.1.

This module advances the bounded 12-row Career condition surface from a typed
Product condition plan to deterministic NATAL evaluation against the canonical
P09 (事业宫) palace structure.

Important boundary:
- condition truth may be evaluated;
- a source-reviewed Career projection descriptor may be attached when true;
- that descriptor remains SEMANTIC ONLY;
- no runtime response effect, ResponseProfile tau, probability, magnitude, or
  predictive-validity claim is created here.

The evaluator never parses free-form source prose.  It consumes only the typed
condition plans produced by Product #521 and source-reviewed projection fields
already present in the active K_response compatibility corpus.
"""

from __future__ import annotations

from dataclasses import dataclass
import copy
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from .palace_structure import PalaceOntology, ResolvedPalaceStructure, resolve_palace_structure
from .response_semantics_adapter import load_career_compatibility_records


ROOT = Path(__file__).resolve().parents[2]
CONDITION_REGISTRY_PATH = ROOT / "product" / "CAREER_CONDITION_COMPILER_PILOT_v0.1.json"
EFFECT_BINDING_REGISTRY_PATH = (
    ROOT / "product" / "CAREER_CONDITION_EFFECT_BINDING_PILOT_v0.1.json"
)

EVALUATOR_VERSION = "PL3R_CAREER_CONDITION_EVALUATOR_V0_1"
EFFECT_BINDING_VERSION = "PL3R_CAREER_EFFECT_BINDING_V0_1"
EFFECT_BINDING_ARTIFACT_ID = "CAREER_CONDITION_EFFECT_BINDING_PILOT_V0_1"
CAREER_PALACE_ID = "P09"

# Product-transport decompositions for the *two exact identifiers* present in
# the governed 12-row compiler input.  This is intentionally not a generic
# star-system parser or a new traditional-semantics registry.
_EXACT_STAR_SYSTEM_MEMBERS: Mapping[str, tuple[str, ...]] = {
    "天机巨门": ("天机", "巨门"),
    "天同巨门": ("天同", "巨门"),
}

# Same bounded rule: do not infer an arbitrary branch-token grammar.
_EXACT_BRANCH_SETS: Mapping[str, frozenset[str]] = {
    "子午": frozenset({"子", "午"}),
}

# Two relation-less LOCAL_OR plans retain source-local spatial semantics in the
# active K_response semantic basis.  They are deliberately enumerated here
# rather than generalized:
# - RC37-E06 says 巨门化禄 OR 禄存同度 -> same P09 palace.
# - RC37-E08 says 子午七杀会/见 the listed 禄 realizations -> the existing
#   FOUR_DIRECTIONS visibility scope (self + triads + opposite).
# No other relation-less LOCAL_OR receives a default.
_SOURCE_LOCAL_OR_SCOPE_BY_RULE: Mapping[str, tuple[str, str]] = {
    "CA07-681": (
        "SAME_PALACE",
        "CAREER_RESIDUAL_CLOSURE_37_v0.1:RC37-E06",
    ),
    "CA09-820": (
        "FOUR_DIRECTIONS_VISIBILITY",
        "CAREER_RESIDUAL_CLOSURE_37_v0.1:RC37-E08",
    ),
}

_STAR_FIELDS = ("major_stars", "minor_stars", "adjective_stars")
_ALL_MEMBER_REQUIREMENTS = frozenset(
    {"PAIR_REQUIRED", "BOTH_SOURCE_LITERAL", "BOTH_SOURCE_LOCAL"}
)
_ANY_MEMBER_REQUIREMENTS = frozenset({"ANY_SOURCE_LOCAL"})


@dataclass(frozen=True)
class CareerEffectBinding:
    source_rule_id: str
    condition_id: str
    time_layer: str
    projection_domain: str
    projection_target: str
    source_location: str
    source_span_ids: tuple[str, ...]
    compatibility_band: str
    effect_kind: str = "SOURCE_PROJECTION_DESCRIPTOR"
    binding_status: str = "BOUND_SOURCE_PROJECTION_SEMANTIC_ONLY"
    runtime_effect_allowed: bool = False

    def __post_init__(self) -> None:
        if not self.source_rule_id.strip():
            raise ValueError("effect binding source_rule_id is required")
        if self.condition_id != f"PRODUCT_CONDITION:{self.source_rule_id}":
            raise ValueError(f"{self.source_rule_id}: condition_id mismatch")
        if self.time_layer != "NATAL":
            raise ValueError(f"{self.source_rule_id}: v0.1 pilot accepts NATAL only")
        if not self.projection_domain.strip() or not self.projection_target.strip():
            raise ValueError(f"{self.source_rule_id}: projection descriptor is required")
        if not self.source_location.strip() or not self.source_span_ids:
            raise ValueError(f"{self.source_rule_id}: source provenance is required")
        if self.effect_kind != "SOURCE_PROJECTION_DESCRIPTOR":
            raise ValueError(f"{self.source_rule_id}: unsupported effect kind")
        if self.binding_status != "BOUND_SOURCE_PROJECTION_SEMANTIC_ONLY":
            raise ValueError(f"{self.source_rule_id}: unsupported binding status")
        if self.runtime_effect_allowed:
            raise ValueError(
                f"{self.source_rule_id}: semantic binding cannot authorize runtime"
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_rule_id": self.source_rule_id,
            "condition_id": self.condition_id,
            "time_layer": self.time_layer,
            "projection_domain": self.projection_domain,
            "projection_target": self.projection_target,
            "source_location": self.source_location,
            "source_span_ids": list(self.source_span_ids),
            "compatibility_band": self.compatibility_band,
            "effect_kind": self.effect_kind,
            "binding_status": self.binding_status,
            "runtime_effect_allowed": self.runtime_effect_allowed,
        }


@dataclass(frozen=True)
class CareerConditionEvaluation:
    source_rule_id: str
    condition_id: str
    compiler_status: str
    matched: bool
    matched_evidence: tuple[str, ...]
    effect_binding: CareerEffectBinding | None
    product_condition_compiled: bool = True
    condition_evaluated: bool = True
    response_effect_bound: bool = False
    runtime_effect_allowed: bool = False

    def __post_init__(self) -> None:
        if self.condition_id != f"PRODUCT_CONDITION:{self.source_rule_id}":
            raise ValueError(f"{self.source_rule_id}: evaluation condition_id mismatch")
        if not self.product_condition_compiled or not self.condition_evaluated:
            raise ValueError(f"{self.source_rule_id}: evaluation maturity flags drifted")
        if self.response_effect_bound != (self.matched and self.effect_binding is not None):
            raise ValueError(
                f"{self.source_rule_id}: response_effect_bound must mean matched + "
                "semantic descriptor attached"
            )
        if self.runtime_effect_allowed:
            raise ValueError(
                f"{self.source_rule_id}: evaluator may not authorize runtime effects"
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_rule_id": self.source_rule_id,
            "condition_id": self.condition_id,
            "compiler_status": self.compiler_status,
            "matched": self.matched,
            "matched_evidence": list(self.matched_evidence),
            "effect_binding": (
                self.effect_binding.to_dict() if self.effect_binding is not None else None
            ),
            "product_condition_compiled": self.product_condition_compiled,
            "condition_evaluated": self.condition_evaluated,
            "response_effect_bound": self.response_effect_bound,
            "runtime_effect_allowed": self.runtime_effect_allowed,
        }


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path.name}: JSON root must be an object")
    return payload


def load_career_condition_registry(
    path: Path = CONDITION_REGISTRY_PATH,
) -> dict[str, Any]:
    payload = _read_json(path)
    if payload.get("artifact_id") != "CAREER_CONDITION_COMPILER_PILOT_V0_1":
        raise ValueError("unexpected Career condition registry artifact")
    plans = payload.get("compiled_conditions")
    if not isinstance(plans, list) or len(plans) != 12:
        raise ValueError("Career condition evaluator requires exact 12 compiled plans")
    ids = [str(item.get("source_rule_id", "")).strip() for item in plans]
    if any(not item for item in ids) or len(set(ids)) != 12:
        raise ValueError("Career compiled plan source_rule_id set is invalid")
    return copy.deepcopy(payload)


def build_career_effect_binding_registry(
    *,
    condition_registry: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Bind exact compiled conditions to source-reviewed projection descriptors."""

    registry = (
        copy.deepcopy(condition_registry)
        if condition_registry is not None
        else load_career_condition_registry()
    )
    plans = registry.get("compiled_conditions")
    if not isinstance(plans, list) or len(plans) != 12:
        raise ValueError("effect binding requires exact 12 compiled conditions")

    compatibility = {
        str(row.get("source_rule_id", "")).strip(): row
        for row in load_career_compatibility_records()
    }

    bindings: list[CareerEffectBinding] = []
    for plan in sorted(plans, key=lambda item: str(item["source_rule_id"])):
        rule_id = str(plan["source_rule_id"]).strip()
        row = compatibility.get(rule_id)
        if row is None:
            raise ValueError(f"{rule_id}: active K_response compatibility row missing")

        span_ids = row.get("source_span_ids")
        if not isinstance(span_ids, list) or not span_ids:
            raise ValueError(f"{rule_id}: source_span_ids are required")

        bindings.append(
            CareerEffectBinding(
                source_rule_id=rule_id,
                condition_id=str(plan["condition_id"]),
                time_layer=str(row.get("time_layer", "")).strip(),
                projection_domain=str(row.get("projection_domain", "")).strip(),
                projection_target=str(row.get("projection_target", "")).strip(),
                source_location=str(row.get("source_location", "")).strip(),
                source_span_ids=tuple(str(item).strip() for item in span_ids),
                compatibility_band=str(row.get("compatibility_band", "")).strip(),
            )
        )

    if len(bindings) != 12:
        raise ValueError("effect binding census drift")

    return {
        "schema_version": "0.1",
        "artifact_id": EFFECT_BINDING_ARTIFACT_ID,
        "binding_version": EFFECT_BINDING_VERSION,
        "condition_registry": "product/CAREER_CONDITION_COMPILER_PILOT_v0.1.json",
        "knowledge_source": "ACTIVE_K_RESPONSE_COMPATIBILITY_251",
        "summary": {
            "compiled_conditions": 12,
            "semantic_effect_bindings": 12,
            "runtime_effects_authorized": 0,
            "response_profile_tau_generated": 0,
        },
        "bindings": [item.to_dict() for item in bindings],
        "maturity": {
            "condition_evaluator": "PILOT_IMPLEMENTED_V0_1",
            "effect_binding": "SOURCE_PROJECTION_SEMANTIC_ONLY",
            "runtime_response_execution": "NOT_IMPLEMENTED",
            "response_profile_tau": "NOT_IMPLEMENTED",
            "predictive_validity": "NOT_VALIDATED",
        },
    }


def _binding_index(
    payload: Mapping[str, Any] | None = None,
) -> dict[str, CareerEffectBinding]:
    source = (
        copy.deepcopy(payload)
        if payload is not None
        else build_career_effect_binding_registry()
    )
    raw = source.get("bindings")
    if not isinstance(raw, list) or len(raw) != 12:
        raise ValueError("effect binding registry must contain 12 rows")

    out: dict[str, CareerEffectBinding] = {}
    for row in raw:
        if not isinstance(row, Mapping):
            raise ValueError("effect binding row must be an object")
        binding = CareerEffectBinding(
            source_rule_id=str(row.get("source_rule_id", "")).strip(),
            condition_id=str(row.get("condition_id", "")).strip(),
            time_layer=str(row.get("time_layer", "")).strip(),
            projection_domain=str(row.get("projection_domain", "")).strip(),
            projection_target=str(row.get("projection_target", "")).strip(),
            source_location=str(row.get("source_location", "")).strip(),
            source_span_ids=tuple(str(x).strip() for x in row.get("source_span_ids", [])),
            compatibility_band=str(row.get("compatibility_band", "")).strip(),
            effect_kind=str(row.get("effect_kind", "")).strip(),
            binding_status=str(row.get("binding_status", "")).strip(),
            runtime_effect_allowed=bool(row.get("runtime_effect_allowed", False)),
        )
        if binding.source_rule_id in out:
            raise ValueError(f"duplicate effect binding: {binding.source_rule_id}")
        out[binding.source_rule_id] = binding
    return out


def _palace_star_rows(
    structure: ResolvedPalaceStructure,
    palace_id: str,
) -> tuple[Mapping[str, Any], ...]:
    palace = structure.palace(palace_id)
    rows: list[Mapping[str, Any]] = []
    for field in _STAR_FIELDS:
        raw = palace.raw.get(field, [])
        if not isinstance(raw, list):
            raise ValueError(f"{palace_id}.{field} must be an array")
        rows.extend(item for item in raw if isinstance(item, Mapping))
    return tuple(rows)


def _star_present(
    structure: ResolvedPalaceStructure,
    palace_id: str,
    star: str,
) -> bool:
    return any(
        str(row.get("name", "")).strip() == star
        for row in _palace_star_rows(structure, palace_id)
    )


def _transform_present(
    structure: ResolvedPalaceStructure,
    palace_id: str,
    star: str,
    transform: str,
) -> bool:
    mutagen = transform[1:] if transform.startswith("化") else transform
    return any(
        str(row.get("name", "")).strip() == star
        and str(row.get("mutagen") or "").strip() == mutagen
        for row in _palace_star_rows(structure, palace_id)
    )


def _term_match(
    structure: ResolvedPalaceStructure,
    palace_id: str,
    term: Mapping[str, Any],
) -> tuple[bool, tuple[str, ...]]:
    term_type = str(term.get("term_type", "")).strip()
    args = term.get("args")
    if not isinstance(args, list) or not args:
        raise ValueError("compiled term args must be a non-empty array")
    values = tuple(str(item).strip() for item in args)
    if any(not item for item in values):
        raise ValueError("compiled term args may not be blank")

    if term_type in {"STAR", "SYMBOL", "ATOM"}:
        if len(values) != 1:
            raise ValueError(f"{term_type} requires one argument")
        matched = _star_present(structure, palace_id, values[0])
        evidence = (f"{palace_id}:{term_type}:{values[0]}",) if matched else ()
        return matched, evidence

    if term_type == "TRANSFORM":
        if len(values) != 2:
            raise ValueError("TRANSFORM requires two arguments")
        matched = _transform_present(structure, palace_id, values[0], values[1])
        evidence = (
            (f"{palace_id}:TRANSFORM:{values[0]}:{values[1]}",)
            if matched
            else ()
        )
        return matched, evidence

    if term_type == "PALACE_BRANCH":
        if len(values) != 1:
            raise ValueError("PALACE_BRANCH requires one argument")
        allowed = _EXACT_BRANCH_SETS.get(values[0])
        if allowed is None:
            raise ValueError(
                f"unsupported bounded PALACE_BRANCH token: {values[0]}"
            )
        branch = structure.palace(palace_id).branch
        matched = branch in allowed
        evidence = (
            (f"{palace_id}:PALACE_BRANCH:{branch}:IN:{values[0]}",)
            if matched
            else ()
        )
        return matched, evidence

    if term_type == "STAR_SYSTEM":
        if len(values) != 1:
            raise ValueError("STAR_SYSTEM requires one argument")
        members = _EXACT_STAR_SYSTEM_MEMBERS.get(values[0])
        if members is None:
            raise ValueError(
                f"unsupported bounded STAR_SYSTEM identifier: {values[0]}"
            )
        matched = all(_star_present(structure, palace_id, star) for star in members)
        evidence = (
            tuple(f"{palace_id}:STAR_SYSTEM_MEMBER:{values[0]}:{star}" for star in members)
            if matched
            else ()
        )
        return matched, evidence

    raise ValueError(f"unsupported compiled term type for evaluator: {term_type}")


def _target_match(
    structure: ResolvedPalaceStructure,
    palace_ids: Sequence[str],
    target: Mapping[str, Any],
) -> tuple[bool, tuple[str, ...]]:
    requirement = str(target.get("member_requirement", "")).strip()
    members = target.get("members")
    if not isinstance(members, list) or not members:
        raise ValueError("compiled target members must be a non-empty array")

    member_results: list[tuple[bool, tuple[str, ...]]] = []
    for member in members:
        if not isinstance(member, Mapping):
            raise ValueError("compiled target member must be an object")
        matched = False
        evidence: tuple[str, ...] = ()
        for palace_id in palace_ids:
            local_match, local_evidence = _term_match(structure, palace_id, member)
            if local_match:
                matched = True
                evidence = local_evidence
                break
        member_results.append((matched, evidence))

    if requirement in _ALL_MEMBER_REQUIREMENTS:
        matched = all(item[0] for item in member_results)
        evidence = (
            tuple(
                evidence
                for item in member_results
                for evidence in item[1]
            )
            if matched
            else ()
        )
        return matched, evidence

    if requirement in _ANY_MEMBER_REQUIREMENTS:
        matched_items = [item for item in member_results if item[0]]
        if not matched_items:
            return False, ()
        evidence = tuple(
            evidence
            for item in matched_items
            for evidence in item[1]
        )
        return True, evidence

    raise ValueError(f"unsupported member requirement: {requirement}")


def _evaluate_direct_plan(
    structure: ResolvedPalaceStructure,
    plan: Mapping[str, Any],
) -> tuple[bool, tuple[str, ...]]:
    rule_id = str(plan.get("source_rule_id", "")).strip()
    if not rule_id:
        raise ValueError("direct condition plan requires source_rule_id")

    subjects = plan.get("subject_terms")
    if not isinstance(subjects, list) or not subjects:
        raise ValueError("direct condition plan requires subject_terms")

    evidence: list[str] = []
    for subject in subjects:
        if not isinstance(subject, Mapping):
            raise ValueError("subject term must be an object")
        matched, refs = _term_match(structure, CAREER_PALACE_ID, subject)
        if not matched:
            return False, ()
        evidence.extend(refs)

    target = plan.get("target")
    if not isinstance(target, Mapping):
        raise ValueError("direct condition plan requires target")

    relation = plan.get("relation")
    if relation is None:
        if str(target.get("node_type", "")).strip() != "LOCAL_OR":
            raise ValueError("relation-less v0.1 plan must be LOCAL_OR")
        source_local_scope = _SOURCE_LOCAL_OR_SCOPE_BY_RULE.get(rule_id)
        if source_local_scope is None:
            raise ValueError(
                f"{rule_id}: relation-less LOCAL_OR has no explicit "
                "source-backed evaluation scope"
            )
        scope_kind, scope_ref = source_local_scope
        if scope_kind == "SAME_PALACE":
            target_palaces = (CAREER_PALACE_ID,)
        elif scope_kind == "FOUR_DIRECTIONS_VISIBILITY":
            target_palaces = structure.sanfang_sizheng_of(CAREER_PALACE_ID)
        else:
            raise ValueError(
                f"{rule_id}: unsupported source-local evaluation scope {scope_kind}"
            )
        target_match, refs = _target_match(
            structure,
            target_palaces,
            target,
        )
        if target_match:
            evidence.append(
                f"SOURCE_LOCAL_SCOPE:{rule_id}:{scope_kind}:{scope_ref}"
            )
    else:
        if not isinstance(relation, Mapping):
            raise ValueError("relation must be an object or null")
        operator = str(relation.get("operator", "")).strip()
        geometry = str(relation.get("geometry", "")).strip()
        offsets = relation.get("palace_offsets")

        if operator == "EXACT_GEOMETRY":
            if geometry != "SAME_PALACE" or offsets != [0]:
                raise ValueError("EXACT_GEOMETRY evaluator scope drift")
            target_match, refs = _target_match(
                structure,
                (CAREER_PALACE_ID,),
                target,
            )
        elif operator == "FOUR_DIRECTIONS_VISIBILITY":
            if geometry != "UNSPECIFIED_WITHIN_SCOPE" or offsets != [0, 4, 6, 8]:
                raise ValueError("FOUR_DIRECTIONS_VISIBILITY evaluator scope drift")
            target_match, refs = _target_match(
                structure,
                structure.sanfang_sizheng_of(CAREER_PALACE_ID),
                target,
            )
        else:
            raise ValueError(f"unsupported relation operator: {operator}")

    if not target_match:
        return False, ()
    evidence.extend(refs)
    return True, tuple(sorted(set(evidence)))


def evaluate_career_conditions(
    snapshot: Mapping[str, Any],
    palace_ontology: PalaceOntology,
    *,
    condition_registry: Mapping[str, Any] | None = None,
    effect_binding_registry: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Evaluate the exact 12 Career NATAL conditions against one chart snapshot."""

    registry = (
        copy.deepcopy(condition_registry)
        if condition_registry is not None
        else load_career_condition_registry()
    )
    plans_raw = registry.get("compiled_conditions")
    if not isinstance(plans_raw, list) or len(plans_raw) != 12:
        raise ValueError("evaluator requires exact 12 compiled plans")

    plans = {
        str(item.get("source_rule_id", "")).strip(): item
        for item in plans_raw
        if isinstance(item, Mapping)
    }
    if len(plans) != 12 or any(not key for key in plans):
        raise ValueError("compiled plan index is invalid")

    bindings = _binding_index(effect_binding_registry)
    if set(bindings) != set(plans):
        raise ValueError("condition/effect binding ID sets differ")

    structure = resolve_palace_structure(snapshot, palace_ontology)
    cache: dict[str, CareerConditionEvaluation] = {}
    evaluating: set[str] = set()

    def evaluate(rule_id: str) -> CareerConditionEvaluation:
        if rule_id in cache:
            return cache[rule_id]
        if rule_id in evaluating:
            raise ValueError(f"dependency cycle detected at {rule_id}")
        plan = plans.get(rule_id)
        if plan is None:
            raise ValueError(f"condition plan missing: {rule_id}")
        evaluating.add(rule_id)

        compiler_status = str(plan.get("compiler_status", "")).strip()
        if compiler_status == "COMPILED_DIRECT_SEMANTIC_ONLY":
            matched, evidence = _evaluate_direct_plan(structure, plan)
        elif compiler_status == "COMPILED_DEPENDENCY_REFERENCE_SEMANTIC_ONLY":
            parent_condition_id = str(plan.get("parent_condition_id", "")).strip()
            prefix = "PRODUCT_CONDITION:"
            if not parent_condition_id.startswith(prefix):
                raise ValueError(f"{rule_id}: invalid parent condition reference")
            parent_rule_id = parent_condition_id[len(prefix):]
            parent = evaluate(parent_rule_id)
            matched = parent.matched
            evidence = (
                (f"PARENT_CONDITION:{parent_condition_id}:MATCHED",)
                if matched
                else ()
            )
        else:
            raise ValueError(f"{rule_id}: unsupported compiler_status")

        binding = bindings[rule_id] if matched else None
        result = CareerConditionEvaluation(
            source_rule_id=rule_id,
            condition_id=str(plan.get("condition_id", "")).strip(),
            compiler_status=compiler_status,
            matched=matched,
            matched_evidence=evidence,
            effect_binding=binding,
            response_effect_bound=matched,
        )
        cache[rule_id] = result
        evaluating.remove(rule_id)
        return result

    results = [evaluate(rule_id) for rule_id in sorted(plans)]
    matched = [item for item in results if item.matched]

    return {
        "schema_version": "0.1",
        "evaluator_version": EVALUATOR_VERSION,
        "scope": {
            "domain": "career",
            "palace_id": CAREER_PALACE_ID,
            "time_layer": "NATAL",
            "temporal_environment_consumed": False,
        },
        "summary": {
            "conditions_compiled": 12,
            "conditions_evaluated": 12,
            "conditions_matched": len(matched),
            "semantic_effects_bound": len(matched),
            "runtime_effects_authorized": 0,
            "response_profile_tau_generated": 0,
        },
        "evaluations": [item.to_dict() for item in results],
        "maturity": {
            "condition_evaluation": "DETERMINISTIC_NATAL_PILOT",
            "effect_binding": "SOURCE_PROJECTION_SEMANTIC_ONLY",
            "decade_year_response_compiler": "NOT_IMPLEMENTED",
            "response_profile_tau": "NOT_IMPLEMENTED",
            "predictive_validity": "NOT_VALIDATED",
        },
    }

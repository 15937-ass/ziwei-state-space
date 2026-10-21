"""PL3-R Career condition-IR compiler pilot v0.1.

This module performs a deliberately narrow structural compilation step:

Knowledge condition IR
    -> typed Product condition plan

It does NOT evaluate a chart/environment, bind a response effect, authorize
runtime execution, or produce ResponseProfile tau.  Product compilation here
means only that the source-reviewed IR has been translated into a deterministic
machine contract that a later evaluator may consume.
"""

from __future__ import annotations

from dataclasses import dataclass
import copy
import re
from typing import Any, Mapping, Sequence

from src.product.response_semantics_adapter import (
    CAREER_COMPILER_READINESS_CENSUS_PATH,
    CAREER_DEPENDENCY_IR_PATH,
    CAREER_DIRECT_CONDITION_IR_PATH,
    load_career_compiler_readiness_census,
    load_career_dependency_ir,
    load_career_direct_condition_ir,
    validate_career_compiler_readiness_cross_artifacts,
)


COMPILER_VERSION = "PL3R_CAREER_CONDITION_COMPILER_V0_1"
ARTIFACT_ID = "CAREER_CONDITION_COMPILER_PILOT_V0_1"

DIRECT_STATUS = "COMPILED_DIRECT_SEMANTIC_ONLY"
DEPENDENCY_STATUS = "COMPILED_DEPENDENCY_REFERENCE_SEMANTIC_ONLY"
REJECTION_STATUS = "NOT_COMPILER_INPUT"

_ALLOWED_SUBJECT_TYPES = frozenset(
    {"STAR", "STAR_SYSTEM", "TRANSFORM", "PALACE_BRANCH"}
)
_ALLOWED_TARGET_NODE_TYPES = frozenset(
    {
        "NAMED_COMPOSITE",
        "LOCAL_ANY_OF",
        "EXPLICIT_MEMBER_SET",
        "SOURCE_LOCAL_PAIR",
        "LOCAL_OR",
    }
)
_TERM_RE = re.compile(r"^(STAR|STAR_SYSTEM|TRANSFORM|PALACE_BRANCH|ATOM)\((.*)\)$")


@dataclass(frozen=True)
class CompiledTerm:
    term_type: str
    args: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.term_type.strip():
            raise ValueError("compiled term_type is required")
        if not self.args or any(not item.strip() for item in self.args):
            raise ValueError("compiled term args must be non-empty")

    def to_dict(self) -> dict[str, Any]:
        return {"term_type": self.term_type, "args": list(self.args)}


@dataclass(frozen=True)
class CompiledConditionPlan:
    condition_id: str
    source_rule_id: str
    compiler_version: str
    source_ir_kind: str
    source_ir_artifact: str
    subject_terms: tuple[CompiledTerm, ...]
    relation: Mapping[str, Any] | None
    target: Mapping[str, Any] | None
    source_expression_ref: str | None
    parent_condition_id: str | None
    inheritance_mode: str
    prohibited_inheritance: tuple[str, ...]
    compiler_status: str
    product_condition_compiled: bool
    condition_evaluated: bool
    response_effect_bound: bool
    runtime_effect_allowed: bool
    semantic_basis_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.compiler_version != COMPILER_VERSION:
            raise ValueError("compiled condition compiler_version mismatch")
        if self.compiler_status not in {DIRECT_STATUS, DEPENDENCY_STATUS}:
            raise ValueError("unsupported compiled condition status")
        if self.product_condition_compiled is not True:
            raise ValueError("compiled condition must mark Product compilation")
        if self.condition_evaluated:
            raise ValueError("v0.1 compiler must not evaluate conditions")
        if self.response_effect_bound:
            raise ValueError("v0.1 compiler must not bind response effects")
        if self.runtime_effect_allowed:
            raise ValueError("v0.1 compiler must not authorize runtime effects")
        if self.compiler_status == DIRECT_STATUS:
            if self.parent_condition_id is not None:
                raise ValueError("direct condition cannot have parent_condition_id")
            if not self.subject_terms:
                raise ValueError("direct condition requires subject terms")
            if self.target is None:
                raise ValueError("direct condition requires target")
        else:
            if not self.parent_condition_id:
                raise ValueError("dependency condition requires parent_condition_id")
            if self.subject_terms or self.relation is not None or self.target is not None:
                raise ValueError(
                    "dependency condition must reference parent plan without copying AST"
                )

    def to_dict(self) -> dict[str, Any]:
        return {
            "condition_id": self.condition_id,
            "source_rule_id": self.source_rule_id,
            "compiler_version": self.compiler_version,
            "source_ir_kind": self.source_ir_kind,
            "source_ir_artifact": self.source_ir_artifact,
            "subject_terms": [item.to_dict() for item in self.subject_terms],
            "relation": copy.deepcopy(self.relation),
            "target": copy.deepcopy(self.target),
            "source_expression_ref": self.source_expression_ref,
            "parent_condition_id": self.parent_condition_id,
            "inheritance_mode": self.inheritance_mode,
            "prohibited_inheritance": list(self.prohibited_inheritance),
            "compiler_status": self.compiler_status,
            "product_condition_compiled": self.product_condition_compiled,
            "condition_evaluated": self.condition_evaluated,
            "response_effect_bound": self.response_effect_bound,
            "runtime_effect_allowed": self.runtime_effect_allowed,
            "semantic_basis_refs": list(self.semantic_basis_refs),
        }


def _required_text(value: Any, path: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise ValueError(f"{path} is required")
    return text


def _parse_term(value: Any, path: str, *, raw_symbol_allowed: bool) -> CompiledTerm:
    text = _required_text(value, path)
    match = _TERM_RE.fullmatch(text)
    if match is None:
        if raw_symbol_allowed:
            return CompiledTerm("SYMBOL", (text,))
        raise ValueError(f"{path}: unsupported condition token {text}")

    term_type, body = match.groups()
    if term_type == "TRANSFORM":
        parts = tuple(item.strip() for item in body.split(","))
        if len(parts) != 2 or any(not item for item in parts):
            raise ValueError(f"{path}: TRANSFORM requires exactly two arguments")
        return CompiledTerm(term_type, parts)

    argument = body.strip()
    if not argument or "," in argument:
        raise ValueError(f"{path}: {term_type} requires exactly one argument")
    return CompiledTerm(term_type, (argument,))


def _compile_relation(value: Any, rule_id: str) -> dict[str, Any] | None:
    if value is None:
        return None
    if not isinstance(value, dict):
        raise ValueError(f"{rule_id}: relation must be an object or null")

    operator = _required_text(value.get("operator"), f"{rule_id}.relation.operator")
    geometry = _required_text(value.get("geometry"), f"{rule_id}.relation.geometry")
    offsets = value.get("palace_offsets")
    if not isinstance(offsets, list) or any(not isinstance(item, int) for item in offsets):
        raise ValueError(f"{rule_id}: palace_offsets must be integer array")

    if operator == "EXACT_GEOMETRY":
        if geometry != "SAME_PALACE" or offsets != [0]:
            raise ValueError(
                f"{rule_id}: EXACT_GEOMETRY v0.1 only supports SAME_PALACE offset 0"
            )
    elif operator == "FOUR_DIRECTIONS_VISIBILITY":
        if geometry != "UNSPECIFIED_WITHIN_SCOPE" or offsets != [0, 4, 6, 8]:
            raise ValueError(
                f"{rule_id}: FOUR_DIRECTIONS_VISIBILITY scope drift"
            )
    else:
        raise ValueError(f"{rule_id}: unsupported relation operator {operator}")

    return {
        "operator": operator,
        "geometry": geometry,
        "palace_offsets": list(offsets),
    }


def _compile_target(value: Any, rule_id: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{rule_id}: target must be an object")
    node_type = _required_text(value.get("node_type"), f"{rule_id}.target.node_type")
    requirement = _required_text(
        value.get("member_requirement"), f"{rule_id}.target.member_requirement"
    )
    members = value.get("members")
    if node_type not in _ALLOWED_TARGET_NODE_TYPES:
        raise ValueError(f"{rule_id}: unsupported target node_type {node_type}")
    if not isinstance(members, list) or not members:
        raise ValueError(f"{rule_id}: target members must be non-empty")

    expected: dict[str, tuple[str, int | None]] = {
        "NAMED_COMPOSITE": ("PAIR_REQUIRED", 2),
        "LOCAL_ANY_OF": ("ANY_SOURCE_LOCAL", None),
        "EXPLICIT_MEMBER_SET": ("BOTH_SOURCE_LITERAL", 2),
        "SOURCE_LOCAL_PAIR": ("BOTH_SOURCE_LOCAL", 2),
        "LOCAL_OR": ("ANY_SOURCE_LOCAL", None),
    }
    expected_requirement, expected_count = expected[node_type]
    if requirement != expected_requirement:
        raise ValueError(
            f"{rule_id}: {node_type} requirement drift: {requirement}"
        )
    if expected_count is not None and len(members) != expected_count:
        raise ValueError(
            f"{rule_id}: {node_type} requires exactly {expected_count} members"
        )

    raw_symbol_allowed = node_type != "LOCAL_OR"
    compiled_members = tuple(
        _parse_term(
            item,
            f"{rule_id}.target.members[{index}]",
            raw_symbol_allowed=raw_symbol_allowed,
        )
        for index, item in enumerate(members)
    )
    if node_type == "LOCAL_OR" and any(
        item.term_type not in {"TRANSFORM", "ATOM"}
        for item in compiled_members
    ):
        raise ValueError(
            f"{rule_id}: LOCAL_OR supports only explicit TRANSFORM/ATOM terms"
        )
    if node_type != "LOCAL_OR" and any(
        item.term_type != "SYMBOL" for item in compiled_members
    ):
        raise ValueError(
            f"{rule_id}: source-local member set must contain literal symbols"
        )

    return {
        "node_type": node_type,
        "member_requirement": requirement,
        "members": [item.to_dict() for item in compiled_members],
    }


def _compile_direct_record(record: Mapping[str, Any]) -> CompiledConditionPlan:
    rule_id = _required_text(record.get("source_rule_id"), "direct.source_rule_id")
    if record.get("inheritance_mode") != "NONE":
        raise ValueError(f"{rule_id}: direct IR inheritance_mode must be NONE")
    if record.get("source_local_only") is not True:
        raise ValueError(f"{rule_id}: direct IR must remain source-local")
    if record.get("global_default_created") is not False:
        raise ValueError(f"{rule_id}: compiler may not consume globalized IR")
    if record.get("product_condition_compiled") is not False:
        raise ValueError(f"{rule_id}: Knowledge IR must not pre-claim Product compile")
    if record.get("runtime_authorized") is not False:
        raise ValueError(f"{rule_id}: Knowledge IR must not authorize runtime")

    ir = record.get("condition_ir")
    if not isinstance(ir, dict):
        raise ValueError(f"{rule_id}: condition_ir must be an object")
    raw_subject = ir.get("subject_scope")
    if not isinstance(raw_subject, list) or not raw_subject:
        raise ValueError(f"{rule_id}: subject_scope must be non-empty")
    subject_terms = tuple(
        _parse_term(
            item,
            f"{rule_id}.subject_scope[{index}]",
            raw_symbol_allowed=False,
        )
        for index, item in enumerate(raw_subject)
    )
    unsupported = sorted(
        {item.term_type for item in subject_terms} - _ALLOWED_SUBJECT_TYPES
    )
    if unsupported:
        raise ValueError(f"{rule_id}: unsupported subject term(s) {unsupported}")

    relation = _compile_relation(ir.get("relation"), rule_id)
    target = _compile_target(ir.get("target"), rule_id)

    if target["node_type"] == "LOCAL_OR":
        if relation is not None:
            raise ValueError(f"{rule_id}: LOCAL_OR record must not invent relation")
    elif relation is None:
        raise ValueError(f"{rule_id}: non-LOCAL_OR record requires explicit relation")

    basis = record.get("semantic_basis")
    if not isinstance(basis, list) or not basis:
        raise ValueError(f"{rule_id}: semantic_basis must be non-empty")

    expression = _required_text(
        ir.get("canonical_expression"), f"{rule_id}.canonical_expression"
    )
    return CompiledConditionPlan(
        condition_id=f"PRODUCT_CONDITION:{rule_id}",
        source_rule_id=rule_id,
        compiler_version=COMPILER_VERSION,
        source_ir_kind="DIRECT_CONDITION_IR",
        source_ir_artifact=str(
            CAREER_DIRECT_CONDITION_IR_PATH.relative_to(
                CAREER_DIRECT_CONDITION_IR_PATH.parents[2]
            )
        ),
        subject_terms=subject_terms,
        relation=relation,
        target=target,
        source_expression_ref=expression,
        parent_condition_id=None,
        inheritance_mode="NONE",
        prohibited_inheritance=(),
        compiler_status=DIRECT_STATUS,
        product_condition_compiled=True,
        condition_evaluated=False,
        response_effect_bound=False,
        runtime_effect_allowed=False,
        semantic_basis_refs=tuple(str(item) for item in basis),
    )


def _compile_dependency_record(
    record: Mapping[str, Any],
    direct_plans: Mapping[str, CompiledConditionPlan],
) -> CompiledConditionPlan:
    child_id = _required_text(record.get("child_rule_id"), "dependency.child_rule_id")
    parent_id = _required_text(record.get("parent_rule_id"), f"{child_id}.parent_rule_id")
    if parent_id not in direct_plans:
        raise ValueError(f"{child_id}: dependency parent is not a compiled direct condition")
    if record.get("inheritance_mode") != "EXACT_PARENT_CONDITION_REFERENCE":
        raise ValueError(f"{child_id}: unsupported dependency inheritance mode")
    if record.get("local_delta") is not None:
        raise ValueError(f"{child_id}: v0.1 dependency local_delta must remain null")
    if record.get("inherited_component") != "PARENT_CONDITION_SCOPE_ONLY":
        raise ValueError(f"{child_id}: dependency inheritance scope drift")
    if record.get("condition_reference") != f"RULE_CONDITION({parent_id})":
        raise ValueError(f"{child_id}: dependency condition reference drift")
    if record.get("knowledge_ir_status") != "DEPENDENCY_IR_READY_SEMANTIC_ONLY":
        raise ValueError(f"{child_id}: dependency IR status is not compiler-ready")
    if record.get("product_condition_compiled") is not False:
        raise ValueError(f"{child_id}: Knowledge dependency IR pre-claims Product compile")
    if record.get("runtime_authorized") is not False:
        raise ValueError(f"{child_id}: Knowledge dependency IR authorizes runtime")

    prohibited = record.get("prohibited_inheritance")
    expected = {
        "PARENT_PROJECTION",
        "PARENT_OUTCOME",
        "PARENT_TARGET",
        "PARENT_VALENCE",
        "TEXT_ADJACENCY",
    }
    if not isinstance(prohibited, list) or set(prohibited) != expected:
        raise ValueError(f"{child_id}: prohibited inheritance contract drift")

    return CompiledConditionPlan(
        condition_id=f"PRODUCT_CONDITION:{child_id}",
        source_rule_id=child_id,
        compiler_version=COMPILER_VERSION,
        source_ir_kind="DEPENDENCY_CONDITION_IR",
        source_ir_artifact=str(
            CAREER_DEPENDENCY_IR_PATH.relative_to(
                CAREER_DEPENDENCY_IR_PATH.parents[2]
            )
        ),
        subject_terms=(),
        relation=None,
        target=None,
        source_expression_ref=str(record["condition_reference"]),
        parent_condition_id=f"PRODUCT_CONDITION:{parent_id}",
        inheritance_mode="EXACT_PARENT_CONDITION_REFERENCE",
        prohibited_inheritance=tuple(str(item) for item in prohibited),
        compiler_status=DEPENDENCY_STATUS,
        product_condition_compiled=True,
        condition_evaluated=False,
        response_effect_bound=False,
        runtime_effect_allowed=False,
        semantic_basis_refs=(
            f"KNOWLEDGE_DEPENDENCY_IR:{child_id}",
            f"PRODUCT_CONDITION:{parent_id}",
        ),
    )


def compile_career_condition_registry() -> dict[str, Any]:
    """Compile exactly the active 12-row Career condition-IR input surface."""

    validate_career_compiler_readiness_cross_artifacts()
    census = load_career_compiler_readiness_census()
    direct = load_career_direct_condition_ir()
    dependency = load_career_dependency_ir()

    direct_plans = {
        plan.source_rule_id: plan
        for plan in (
            _compile_direct_record(record)
            for record in sorted(
                direct["records"], key=lambda item: item["source_rule_id"]
            )
        )
    }
    dependency_plans = {
        plan.source_rule_id: plan
        for plan in (
            _compile_dependency_record(record, direct_plans)
            for record in sorted(
                dependency["records"], key=lambda item: item["child_rule_id"]
            )
        )
    }
    if set(direct_plans).intersection(dependency_plans):
        raise ValueError("direct and dependency compiled condition IDs overlap")

    all_plans = {**direct_plans, **dependency_plans}
    ready_ids = {
        item["source_rule_id"]
        for item in census["records"]
        if item.get("knowledge_condition_ir_ready") is True
    }
    if set(all_plans) != ready_ids:
        raise ValueError("compiled condition IDs do not equal Knowledge ready set")

    rejected_rows: list[dict[str, Any]] = []
    for row in sorted(census["records"], key=lambda item: item["source_rule_id"]):
        if row.get("knowledge_condition_ir_ready") is True:
            continue
        rule_id = str(row["source_rule_id"])
        band = str(row["compiler_readiness_band"])
        rejected_rows.append(
            {
                "source_rule_id": rule_id,
                "compiler_readiness_band": band,
                "compiler_status": REJECTION_STATUS,
                "blockers": [f"KNOWLEDGE_CONDITION_IR_NOT_READY:{band}"],
                "product_condition_compiled": False,
                "condition_evaluated": False,
                "response_effect_bound": False,
                "runtime_effect_allowed": False,
            }
        )

    plans = [
        all_plans[rule_id].to_dict()
        for rule_id in sorted(all_plans)
    ]
    return {
        "schema_version": "0.1",
        "artifact_id": ARTIFACT_ID,
        "compiler_version": COMPILER_VERSION,
        "knowledge_inputs": {
            "compiler_readiness_census": str(
                CAREER_COMPILER_READINESS_CENSUS_PATH.relative_to(
                    CAREER_COMPILER_READINESS_CENSUS_PATH.parents[2]
                )
            ),
            "direct_condition_ir": str(
                CAREER_DIRECT_CONDITION_IR_PATH.relative_to(
                    CAREER_DIRECT_CONDITION_IR_PATH.parents[2]
                )
            ),
            "dependency_condition_ir": str(
                CAREER_DEPENDENCY_IR_PATH.relative_to(
                    CAREER_DEPENDENCY_IR_PATH.parents[2]
                )
            ),
        },
        "summary": {
            "knowledge_condition_ir_ready": len(ready_ids),
            "compiled_conditions": len(plans),
            "compiled_direct": len(direct_plans),
            "compiled_dependency_reference": len(dependency_plans),
            "local_ready_not_compiler_input": len(rejected_rows),
            "condition_evaluated": 0,
            "response_effect_bound": 0,
            "runtime_effects_authorized": 0,
        },
        "compiled_conditions": plans,
        "rejected_local_ready_rows": rejected_rows,
        "maturity": {
            "condition_ir_compiler": "PILOT_IMPLEMENTED_V0_1",
            "condition_evaluator": "NOT_IMPLEMENTED",
            "response_effect_binding": "NOT_IMPLEMENTED",
            "response_profile_tau": "NOT_IMPLEMENTED",
            "predictive_validity": "NOT_VALIDATED",
        },
    }

"""Product #916 non-production structured-condition / temporal binding contract.

This module closes Product-owned PG-006 and PG-007 at the representation layer.
It does not parse arbitrary source prose, evaluate conditions, authorize
manifestation routing, or assign probability.

Structured semantics are supplied by a separately versioned, source-pinned
Product specification.  The compiler only verifies that the specification
matches the accepted Knowledge mapping exactly enough to preserve its reviewed
shape.  Unsupported or unresolved inputs fail closed.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping, Sequence


SCHEMA_VERSION = "0.1"
PROBABILITY_STATUS = "UNKNOWN"
SEMANTIC_MODE = "SOURCE_PINNED_PRESERVATION_ONLY"

CONDITION_GROUP_OPERATORS = frozenset({"ANY_OF"})
PALACE_DEPENDENCY_RELATIONS = frozenset({"OPPOSITE_PALACE"})
TEMPORAL_SCOPE_OPERATORS = frozenset({"ALL_REQUIRED"})
SUPPORTED_TIME_LAYER_BINDINGS = {
    "NATAL": ("NATAL",),
    "DECADE_YEAR": ("DECADE", "YEAR"),
}


def _required_text(value: Any, field: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise ValueError(f"{field} is required")
    return text


def _optional_text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _mapping(value: Any, field: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{field} must be an object")
    return value


def _sequence(value: Any, field: str) -> Sequence[Any]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise ValueError(f"{field} must be an array")
    return value


def _text_tuple(
    value: Any,
    field: str,
    *,
    allow_empty: bool = True,
) -> tuple[str, ...]:
    seq = _sequence(value, field)
    out = tuple(str(item).strip() for item in seq if str(item).strip())
    if not allow_empty and not out:
        raise ValueError(f"{field} cannot be empty")
    return out


def _validate_source_fragment(
    source_condition_text: str,
    fragment: str,
    field: str,
) -> str:
    text = _required_text(fragment, field)
    if text not in source_condition_text:
        raise ValueError(
            f"{field} is not an exact fragment of accepted source_condition_text"
        )
    return text


@dataclass(frozen=True)
class SourceConditionClause:
    clause_id: str
    source_fragment: str


@dataclass(frozen=True)
class AlternativeConditionGroup:
    group_id: str
    operator: str
    alternatives: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.operator not in CONDITION_GROUP_OPERATORS:
            raise ValueError(
                f"unsupported alternative condition operator: {self.operator}"
            )
        if len(self.alternatives) < 2:
            raise ValueError("ANY_OF group requires at least two alternatives")


@dataclass(frozen=True)
class CrossPalaceDependency:
    dependency_id: str
    relation: str
    source_fragment: str
    target_fragment: str

    def __post_init__(self) -> None:
        if self.relation not in PALACE_DEPENDENCY_RELATIONS:
            raise ValueError(
                f"unsupported palace dependency relation: {self.relation}"
            )
        if self.target_fragment not in self.source_fragment:
            raise ValueError(
                "cross-palace target_fragment must remain inside source_fragment"
            )


@dataclass(frozen=True)
class StructuredConditionContract:
    schema_version: str
    mapping_id: str
    source_condition_text: str
    required_clauses: tuple[SourceConditionClause, ...]
    alternative_groups: tuple[AlternativeConditionGroup, ...]
    cross_palace_dependencies: tuple[CrossPalaceDependency, ...]
    source_rule_ids: tuple[str, ...]
    forbidden_inferences: tuple[str, ...]
    semantic_mode: str = SEMANTIC_MODE
    evaluation_authorized: bool = False
    runtime_authorized: bool = False
    probability_status: str = PROBABILITY_STATUS

    def __post_init__(self) -> None:
        if self.schema_version != SCHEMA_VERSION:
            raise ValueError(
                "StructuredConditionContract schema_version must be 0.1"
            )
        if not (
            self.required_clauses
            or self.alternative_groups
            or self.cross_palace_dependencies
        ):
            raise ValueError("structured condition contract cannot be empty")
        if self.semantic_mode != SEMANTIC_MODE:
            raise ValueError("unsupported semantic mode")
        if self.evaluation_authorized or self.runtime_authorized:
            raise ValueError(
                "structured condition preservation cannot authorize evaluation/runtime"
            )
        if self.probability_status != PROBABILITY_STATUS:
            raise ValueError("structured condition probability_status must be UNKNOWN")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class TemporalLayerBinding:
    schema_version: str
    mapping_id: str
    declared_time_layer: str
    required_scopes: tuple[str, ...]
    scope_operator: str
    source_condition_text: str
    forbidden_inferences: tuple[str, ...]
    collapse_allowed: bool = False
    event_inference_allowed: bool = False
    evaluation_authorized: bool = False
    runtime_authorized: bool = False
    probability_status: str = PROBABILITY_STATUS

    def __post_init__(self) -> None:
        if self.schema_version != SCHEMA_VERSION:
            raise ValueError("TemporalLayerBinding schema_version must be 0.1")
        if self.scope_operator not in TEMPORAL_SCOPE_OPERATORS:
            raise ValueError(
                f"unsupported temporal scope operator: {self.scope_operator}"
            )
        expected = SUPPORTED_TIME_LAYER_BINDINGS.get(self.declared_time_layer)
        if expected is None:
            raise ValueError(
                f"unsupported declared_time_layer: {self.declared_time_layer}"
            )
        if self.required_scopes != expected:
            raise ValueError(
                f"{self.declared_time_layer} requires scopes {expected}"
            )
        if self.collapse_allowed:
            raise ValueError("accepted temporal scopes cannot be collapsed")
        if (
            self.event_inference_allowed
            or self.evaluation_authorized
            or self.runtime_authorized
        ):
            raise ValueError(
                "temporal binding cannot infer events or authorize evaluation/runtime"
            )
        if self.probability_status != PROBABILITY_STATUS:
            raise ValueError("temporal binding probability_status must be UNKNOWN")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _validate_mapping_boundary(mapping: Mapping[str, Any]) -> tuple[str, Mapping[str, Any]]:
    mapping_id = _required_text(mapping.get("mapping_id"), "mapping_id")
    if _required_text(mapping.get("probability_status"), "probability_status") != (
        PROBABILITY_STATUS
    ):
        raise ValueError(f"{mapping_id}: probability_status must remain UNKNOWN")
    if bool(mapping.get("executable", False)) or bool(
        mapping.get("product_consumable", False)
    ):
        raise ValueError(
            f"{mapping_id}: this non-production compiler accepts only fail-closed mappings"
        )
    conditions = _mapping(mapping.get("conditions"), f"{mapping_id}.conditions")
    unresolved = _text_tuple(
        conditions.get("unresolved_semantics", []),
        f"{mapping_id}.conditions.unresolved_semantics",
    )
    if unresolved:
        raise ValueError(
            f"{mapping_id}: unresolved source semantics must remain HOLD, not compile"
        )
    return mapping_id, conditions


def compile_structured_condition_contract(
    mapping: Mapping[str, Any],
    spec: Mapping[str, Any],
) -> StructuredConditionContract:
    """Compile one source-pinned preservation spec without parsing source prose."""

    mapping_id, conditions = _validate_mapping_boundary(mapping)
    spec_mapping_id = _required_text(spec.get("mapping_id"), "spec.mapping_id")
    if spec_mapping_id != mapping_id:
        raise ValueError("spec.mapping_id must match accepted mapping_id")

    source_text = _required_text(
        conditions.get("source_condition_text"),
        f"{mapping_id}.conditions.source_condition_text",
    )
    if _required_text(
        spec.get("source_condition_text"),
        "spec.source_condition_text",
    ) != source_text:
        raise ValueError("spec must pin exact accepted source_condition_text")

    required_clauses: list[SourceConditionClause] = []
    for index, item in enumerate(
        _sequence(spec.get("required_clauses", []), "spec.required_clauses")
    ):
        row = _mapping(item, f"spec.required_clauses[{index}]")
        required_clauses.append(
            SourceConditionClause(
                clause_id=_required_text(
                    row.get("clause_id"),
                    f"spec.required_clauses[{index}].clause_id",
                ),
                source_fragment=_validate_source_fragment(
                    source_text,
                    row.get("source_fragment"),
                    f"spec.required_clauses[{index}].source_fragment",
                ),
            )
        )

    groups: list[AlternativeConditionGroup] = []
    for index, item in enumerate(
        _sequence(spec.get("alternative_groups", []), "spec.alternative_groups")
    ):
        row = _mapping(item, f"spec.alternative_groups[{index}]")
        alternatives = tuple(
            _validate_source_fragment(
                source_text,
                alt,
                f"spec.alternative_groups[{index}].alternatives",
            )
            for alt in _text_tuple(
                row.get("alternatives", []),
                f"spec.alternative_groups[{index}].alternatives",
                allow_empty=False,
            )
        )
        groups.append(
            AlternativeConditionGroup(
                group_id=_required_text(
                    row.get("group_id"),
                    f"spec.alternative_groups[{index}].group_id",
                ),
                operator=_required_text(
                    row.get("operator"),
                    f"spec.alternative_groups[{index}].operator",
                ),
                alternatives=alternatives,
            )
        )

    dependencies: list[CrossPalaceDependency] = []
    for index, item in enumerate(
        _sequence(
            spec.get("cross_palace_dependencies", []),
            "spec.cross_palace_dependencies",
        )
    ):
        row = _mapping(item, f"spec.cross_palace_dependencies[{index}]")
        source_fragment = _validate_source_fragment(
            source_text,
            row.get("source_fragment"),
            f"spec.cross_palace_dependencies[{index}].source_fragment",
        )
        dependencies.append(
            CrossPalaceDependency(
                dependency_id=_required_text(
                    row.get("dependency_id"),
                    f"spec.cross_palace_dependencies[{index}].dependency_id",
                ),
                relation=_required_text(
                    row.get("relation"),
                    f"spec.cross_palace_dependencies[{index}].relation",
                ),
                source_fragment=source_fragment,
                target_fragment=_required_text(
                    row.get("target_fragment"),
                    f"spec.cross_palace_dependencies[{index}].target_fragment",
                ),
            )
        )

    return StructuredConditionContract(
        schema_version=SCHEMA_VERSION,
        mapping_id=mapping_id,
        source_condition_text=source_text,
        required_clauses=tuple(required_clauses),
        alternative_groups=tuple(groups),
        cross_palace_dependencies=tuple(dependencies),
        source_rule_ids=_text_tuple(
            mapping.get("source_rule_ids", []),
            f"{mapping_id}.source_rule_ids",
            allow_empty=False,
        ),
        forbidden_inferences=_text_tuple(
            mapping.get("forbidden_inferences", []),
            f"{mapping_id}.forbidden_inferences",
        ),
    )


def compile_temporal_layer_binding(
    mapping: Mapping[str, Any],
) -> TemporalLayerBinding:
    """Preserve accepted time-layer scope without collapsing it to a generic flag."""

    mapping_id, conditions = _validate_mapping_boundary(mapping)
    declared = _required_text(
        conditions.get("time_layer"),
        f"{mapping_id}.conditions.time_layer",
    )
    required_scopes = SUPPORTED_TIME_LAYER_BINDINGS.get(declared)
    if required_scopes is None:
        raise ValueError(
            f"{mapping_id}: unsupported time_layer for v0.1 binding: {declared}"
        )

    return TemporalLayerBinding(
        schema_version=SCHEMA_VERSION,
        mapping_id=mapping_id,
        declared_time_layer=declared,
        required_scopes=required_scopes,
        scope_operator="ALL_REQUIRED",
        source_condition_text=_required_text(
            conditions.get("source_condition_text"),
            f"{mapping_id}.conditions.source_condition_text",
        ),
        forbidden_inferences=_text_tuple(
            mapping.get("forbidden_inferences", []),
            f"{mapping_id}.forbidden_inferences",
        ),
    )

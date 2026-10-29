"""Product manifestation structured condition binding v0.2.

Bounded closure for Product gaps PG-008..PG-011 discovered by P3 audit #918.

This module is intentionally a non-production compatibility layer. It does not
parse arbitrary Chinese condition text. Every compiled structure must come from
an explicitly curated Product fixture pinned to an accepted canonical mapping,
and every retained source fragment/token must be verifiable against that exact
canonical source text.

v0.1 remains unchanged for KMM-000007..000009. v0.2 is scoped only to accepted
KMM-000010 and KMM-000012..000015.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping, Sequence

from .manifestation_adapter_contract_v0_2 import (
    MappingAdapterEnvelopeV02,
    compile_mapping_adapter_envelope,
)


SCHEMA_VERSION = "0.2"
ALLOWED_MAPPING_IDS = frozenset(
    {
        "KMM-000010",
        "KMM-000012",
        "KMM-000013",
        "KMM-000014",
        "KMM-000015",
    }
)
CONDITION_KINDS = frozenset(
    {
        "SOURCE_TEXT_ONLY",
        "LISTED_VARIANT_SET",
        "BRANCHED_CONDITIONAL",
        "PALACE_SCOPED_EXCEPTION",
        "QUALIFIED_CONDITION",
    }
)
TEMPORAL_SCOPE_MAP_V02 = {
    "NATAL": ("NATAL",),
    "DECADE": ("DECADE",),
    "DECADE_YEAR": ("DECADE", "YEAR"),
}
TEMPORAL_BINDING_MODE = "EXACT_DECLARED_SCOPES"

CONDITIONAL_OPERATOR_TOKENS = {
    "SIMULTANEOUS_IF": "若同时",
    "UNLESS": "除非",
    "EVEN_IF": "即使",
}
PALACE_SCOPE_TOKENS = {
    "LIFE_PALACE": "命宫",
}


def _required_text(value: Any, field: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise ValueError(f"{field} is required")
    return text


def _mapping(value: Any, field: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{field} must be an object")
    return value


def _sequence(value: Any, field: str) -> Sequence[Any]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise ValueError(f"{field} must be an array")
    return value


def _text_tuple(value: Any, field: str, *, allow_empty: bool = True) -> tuple[str, ...]:
    seq = _sequence(value, field)
    out = tuple(str(item).strip() for item in seq if str(item).strip())
    if not allow_empty and not out:
        raise ValueError(f"{field} cannot be empty")
    return out


def _verify_verbatim(source_text: str, fragment: str, field: str) -> None:
    if fragment not in source_text:
        raise ValueError(
            f"{field} must be retained verbatim from source_condition_text"
        )


@dataclass(frozen=True)
class TemporalLayerBindingV02:
    source_time_layer: str
    required_scopes: tuple[str, ...]
    binding_mode: str = TEMPORAL_BINDING_MODE
    event_outcome_inference_allowed: bool = False

    def __post_init__(self) -> None:
        expected = TEMPORAL_SCOPE_MAP_V02.get(self.source_time_layer)
        if expected is None:
            raise ValueError(
                f"unsupported canonical time_layer for v0.2: {self.source_time_layer}"
            )
        if self.required_scopes != expected:
            raise ValueError(
                f"{self.source_time_layer} must expand exactly to {expected}"
            )
        if self.binding_mode != TEMPORAL_BINDING_MODE:
            raise ValueError(
                f"temporal binding_mode must be {TEMPORAL_BINDING_MODE}"
            )
        if self.event_outcome_inference_allowed:
            raise ValueError("temporal binding cannot infer event/outcome")


@dataclass(frozen=True)
class SourceTextOnlyConditionV02:
    source_text: str

    def __post_init__(self) -> None:
        if not self.source_text.strip():
            raise ValueError("source_text is required")


@dataclass(frozen=True)
class ListedVariantSetV02:
    context_text: str
    variants: tuple[str, ...]
    combination_semantics: str
    source_operator_token: str | None = None

    def __post_init__(self) -> None:
        if not self.context_text.strip():
            raise ValueError("listed variant context_text is required")
        if len(self.variants) < 2:
            raise ValueError("listed variant set requires at least two variants")
        if self.combination_semantics != "SEPARATE_VARIANTS_NOT_ALL_REQUIRED":
            raise ValueError(
                "listed variant set must preserve SEPARATE_VARIANTS_NOT_ALL_REQUIRED"
            )
        if self.source_operator_token not in (None, ""):
            raise ValueError(
                "listed variant set must not fabricate a source operator token"
            )


@dataclass(frozen=True)
class ConditionalOperatorV02:
    operator: str
    source_token: str

    def __post_init__(self) -> None:
        expected = CONDITIONAL_OPERATOR_TOKENS.get(self.operator)
        if expected is None:
            raise ValueError(f"unsupported bounded conditional operator: {self.operator}")
        if self.source_token != expected:
            raise ValueError(
                f"{self.operator} must retain exact source token {expected}"
            )


@dataclass(frozen=True)
class ConditionBranchV02:
    branch_id: str
    source_text: str
    operator: ConditionalOperatorV02 | None = None
    simultaneous_requirements: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.branch_id.strip() or not self.source_text.strip():
            raise ValueError("branch_id and branch source_text are required")
        if self.operator is None and self.simultaneous_requirements:
            raise ValueError(
                "simultaneous requirements require an explicit bounded operator"
            )
        if self.operator is not None and self.operator.operator == "SIMULTANEOUS_IF":
            if len(self.simultaneous_requirements) < 2:
                raise ValueError(
                    "SIMULTANEOUS_IF branch requires at least two simultaneous requirements"
                )
        elif self.simultaneous_requirements:
            raise ValueError(
                "only SIMULTANEOUS_IF may carry simultaneous_requirements"
            )


@dataclass(frozen=True)
class BranchedConditionalV02:
    context_text: str
    branches: tuple[ConditionBranchV02, ...]

    def __post_init__(self) -> None:
        if not self.context_text.strip():
            raise ValueError("branched condition context_text is required")
        if len(self.branches) < 2:
            raise ValueError("branched condition requires at least two branches")
        ids = tuple(branch.branch_id for branch in self.branches)
        if len(set(ids)) != len(ids):
            raise ValueError("branch_id values must be unique")


@dataclass(frozen=True)
class PalaceScopedDependencyV02:
    palace_scope: str
    source_palace_token: str
    dependency_text: str

    def __post_init__(self) -> None:
        expected = PALACE_SCOPE_TOKENS.get(self.palace_scope)
        if expected is None:
            raise ValueError(f"unsupported bounded palace_scope: {self.palace_scope}")
        if self.source_palace_token != expected:
            raise ValueError(
                f"{self.palace_scope} must retain exact source palace token {expected}"
            )
        if expected not in self.dependency_text:
            raise ValueError(
                "palace-scoped dependency text must retain the named palace token"
            )


@dataclass(frozen=True)
class PalaceScopedExceptionV02:
    base_text: str
    operator: ConditionalOperatorV02
    dependency: PalaceScopedDependencyV02
    consequence_text: str

    def __post_init__(self) -> None:
        if self.operator.operator != "UNLESS":
            raise ValueError("palace-scoped exception must use UNLESS")
        if not self.base_text.strip() or not self.consequence_text.strip():
            raise ValueError("exception base/consequence text is required")


@dataclass(frozen=True)
class QualifiedConditionV02:
    context_text: str
    operator: ConditionalOperatorV02
    qualified_text: str

    def __post_init__(self) -> None:
        if self.operator.operator != "EVEN_IF":
            raise ValueError("qualified condition must use EVEN_IF")
        if not self.context_text.strip() or not self.qualified_text.strip():
            raise ValueError("qualified condition context/qualified text is required")


@dataclass(frozen=True)
class ManifestationConditionBindingV02:
    schema_version: str
    mapping_id: str
    fixture_id: str
    source_condition_text: str
    condition_kind: str
    condition: (
        SourceTextOnlyConditionV02
        | ListedVariantSetV02
        | BranchedConditionalV02
        | PalaceScopedExceptionV02
        | QualifiedConditionV02
    )
    temporal_binding: TemporalLayerBindingV02
    forbidden_inferences: tuple[str, ...]
    adapter_envelope: MappingAdapterEnvelopeV02
    runtime_authorized: bool = False
    probability_status: str = "UNKNOWN"

    def __post_init__(self) -> None:
        if self.schema_version != SCHEMA_VERSION:
            raise ValueError("ManifestationConditionBindingV02 schema_version must be 0.2")
        if self.mapping_id not in ALLOWED_MAPPING_IDS:
            raise ValueError(f"mapping_id outside bounded v0.2 scope: {self.mapping_id}")
        if self.condition_kind not in CONDITION_KINDS:
            raise ValueError(f"unsupported condition_kind: {self.condition_kind}")
        if self.runtime_authorized:
            raise ValueError("v0.2 condition binding cannot authorize runtime")
        if self.probability_status != "UNKNOWN":
            raise ValueError("v0.2 probability_status must remain UNKNOWN")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _compile_temporal_binding(
    raw: Mapping[str, Any],
    *,
    canonical_time_layer: str,
) -> TemporalLayerBindingV02:
    source_time_layer = _required_text(
        raw.get("source_time_layer"), "temporal_binding.source_time_layer"
    )
    if source_time_layer != canonical_time_layer:
        raise ValueError(
            "temporal fixture source_time_layer must equal canonical time_layer"
        )
    required_scopes = _text_tuple(
        raw.get("required_scopes", []),
        "temporal_binding.required_scopes",
        allow_empty=False,
    )
    return TemporalLayerBindingV02(
        source_time_layer=source_time_layer,
        required_scopes=required_scopes,
        binding_mode=_required_text(
            raw.get("binding_mode"), "temporal_binding.binding_mode"
        ),
        event_outcome_inference_allowed=bool(
            raw.get("event_outcome_inference_allowed", False)
        ),
    )


def _compile_source_text_only(
    raw: Mapping[str, Any],
    *,
    source_text: str,
) -> SourceTextOnlyConditionV02:
    retained = _required_text(raw.get("source_text"), "condition.source_text")
    if retained != source_text:
        raise ValueError("SOURCE_TEXT_ONLY must retain exact source_condition_text")
    return SourceTextOnlyConditionV02(source_text=retained)


def _compile_listed_variant_set(
    raw: Mapping[str, Any],
    *,
    source_text: str,
) -> ListedVariantSetV02:
    context_text = _required_text(raw.get("context_text"), "condition.context_text")
    variants = _text_tuple(
        raw.get("variants", []), "condition.variants", allow_empty=False
    )
    _verify_verbatim(source_text, context_text, "condition.context_text")
    for index, variant in enumerate(variants):
        _verify_verbatim(source_text, variant, f"condition.variants[{index}]")

    source_operator_token = raw.get("source_operator_token")
    if source_operator_token not in (None, ""):
        _verify_verbatim(
            source_text, str(source_operator_token), "condition.source_operator_token"
        )

    return ListedVariantSetV02(
        context_text=context_text,
        variants=variants,
        combination_semantics=_required_text(
            raw.get("combination_semantics"), "condition.combination_semantics"
        ),
        source_operator_token=source_operator_token,
    )


def _compile_operator(
    raw: Mapping[str, Any],
    *,
    source_text: str,
    field: str,
) -> ConditionalOperatorV02:
    operator = _required_text(raw.get("operator"), f"{field}.operator")
    source_token = _required_text(raw.get("source_token"), f"{field}.source_token")
    _verify_verbatim(source_text, source_token, f"{field}.source_token")
    return ConditionalOperatorV02(operator=operator, source_token=source_token)


def _compile_branch(
    raw: Mapping[str, Any],
    *,
    source_text: str,
    field: str,
) -> ConditionBranchV02:
    branch_source = _required_text(raw.get("source_text"), f"{field}.source_text")
    _verify_verbatim(source_text, branch_source, f"{field}.source_text")

    operator_raw = raw.get("operator")
    operator = None
    if operator_raw is not None:
        operator = _compile_operator(
            _mapping(operator_raw, f"{field}.operator"),
            source_text=source_text,
            field=f"{field}.operator",
        )

    simultaneous = _text_tuple(
        raw.get("simultaneous_requirements", []),
        f"{field}.simultaneous_requirements",
    )
    for index, requirement in enumerate(simultaneous):
        _verify_verbatim(
            source_text,
            requirement,
            f"{field}.simultaneous_requirements[{index}]",
        )

    return ConditionBranchV02(
        branch_id=_required_text(raw.get("branch_id"), f"{field}.branch_id"),
        source_text=branch_source,
        operator=operator,
        simultaneous_requirements=simultaneous,
    )


def _compile_branched_conditional(
    raw: Mapping[str, Any],
    *,
    source_text: str,
) -> BranchedConditionalV02:
    context_text = _required_text(raw.get("context_text"), "condition.context_text")
    _verify_verbatim(source_text, context_text, "condition.context_text")

    raw_branches = _sequence(raw.get("branches"), "condition.branches")
    branches = tuple(
        _compile_branch(
            _mapping(item, f"condition.branches[{index}]"),
            source_text=source_text,
            field=f"condition.branches[{index}]",
        )
        for index, item in enumerate(raw_branches)
    )
    return BranchedConditionalV02(context_text=context_text, branches=branches)


def _compile_palace_scoped_exception(
    raw: Mapping[str, Any],
    *,
    source_text: str,
) -> PalaceScopedExceptionV02:
    base_text = _required_text(raw.get("base_text"), "condition.base_text")
    consequence_text = _required_text(
        raw.get("consequence_text"), "condition.consequence_text"
    )
    _verify_verbatim(source_text, base_text, "condition.base_text")
    _verify_verbatim(source_text, consequence_text, "condition.consequence_text")

    operator = _compile_operator(
        _mapping(raw.get("operator"), "condition.operator"),
        source_text=source_text,
        field="condition.operator",
    )
    dep_raw = _mapping(raw.get("dependency"), "condition.dependency")
    dependency = PalaceScopedDependencyV02(
        palace_scope=_required_text(
            dep_raw.get("palace_scope"), "condition.dependency.palace_scope"
        ),
        source_palace_token=_required_text(
            dep_raw.get("source_palace_token"),
            "condition.dependency.source_palace_token",
        ),
        dependency_text=_required_text(
            dep_raw.get("dependency_text"), "condition.dependency.dependency_text"
        ),
    )
    _verify_verbatim(
        source_text, dependency.source_palace_token,
        "condition.dependency.source_palace_token"
    )
    _verify_verbatim(
        source_text, dependency.dependency_text,
        "condition.dependency.dependency_text"
    )
    return PalaceScopedExceptionV02(
        base_text=base_text,
        operator=operator,
        dependency=dependency,
        consequence_text=consequence_text,
    )


def _compile_qualified_condition(
    raw: Mapping[str, Any],
    *,
    source_text: str,
) -> QualifiedConditionV02:
    context_text = _required_text(raw.get("context_text"), "condition.context_text")
    qualified_text = _required_text(
        raw.get("qualified_text"), "condition.qualified_text"
    )
    _verify_verbatim(source_text, context_text, "condition.context_text")
    _verify_verbatim(source_text, qualified_text, "condition.qualified_text")
    operator = _compile_operator(
        _mapping(raw.get("operator"), "condition.operator"),
        source_text=source_text,
        field="condition.operator",
    )
    return QualifiedConditionV02(
        context_text=context_text,
        operator=operator,
        qualified_text=qualified_text,
    )


def compile_manifestation_condition_binding_v02(
    canonical_mapping: Mapping[str, Any],
    fixture: Mapping[str, Any],
) -> ManifestationConditionBindingV02:
    """Compile one explicitly curated v0.2 fixture against accepted Knowledge."""

    if str(fixture.get("schema_version", "")).strip() != SCHEMA_VERSION:
        raise ValueError("condition fixture schema_version must be 0.2")

    mapping_id = _required_text(canonical_mapping.get("mapping_id"), "mapping_id")
    if mapping_id not in ALLOWED_MAPPING_IDS:
        raise ValueError(f"canonical mapping outside bounded v0.2 scope: {mapping_id}")

    fixture_mapping_id = _required_text(
        fixture.get("mapping_id"), "fixture.mapping_id"
    )
    if fixture_mapping_id != mapping_id:
        raise ValueError("fixture mapping_id must match canonical mapping_id")

    envelope = compile_mapping_adapter_envelope(canonical_mapping)
    if envelope.conditions.unresolved_semantics:
        raise ValueError(
            f"{mapping_id}: unresolved semantics must remain HOLD, not compiled"
        )
    if envelope.probability_status != "UNKNOWN":
        raise ValueError(f"{mapping_id}: probability_status must remain UNKNOWN")

    source_text = envelope.conditions.source_condition_text
    fixture_source_text = _required_text(
        fixture.get("source_condition_text"), "fixture.source_condition_text"
    )
    if fixture_source_text != source_text:
        raise ValueError(
            "fixture source_condition_text must exactly match canonical mapping"
        )

    kind = _required_text(fixture.get("condition_kind"), "fixture.condition_kind")
    if kind not in CONDITION_KINDS:
        raise ValueError(f"unsupported condition_kind: {kind}")

    condition_raw = _mapping(fixture.get("condition"), "fixture.condition")
    if kind == "SOURCE_TEXT_ONLY":
        condition = _compile_source_text_only(condition_raw, source_text=source_text)
    elif kind == "LISTED_VARIANT_SET":
        condition = _compile_listed_variant_set(condition_raw, source_text=source_text)
    elif kind == "BRANCHED_CONDITIONAL":
        condition = _compile_branched_conditional(condition_raw, source_text=source_text)
    elif kind == "PALACE_SCOPED_EXCEPTION":
        condition = _compile_palace_scoped_exception(
            condition_raw, source_text=source_text
        )
    else:
        condition = _compile_qualified_condition(
            condition_raw, source_text=source_text
        )

    temporal_binding = _compile_temporal_binding(
        _mapping(fixture.get("temporal_binding"), "fixture.temporal_binding"),
        canonical_time_layer=envelope.conditions.time_layer,
    )

    return ManifestationConditionBindingV02(
        schema_version=SCHEMA_VERSION,
        mapping_id=mapping_id,
        fixture_id=_required_text(fixture.get("fixture_id"), "fixture.fixture_id"),
        source_condition_text=source_text,
        condition_kind=kind,
        condition=condition,
        temporal_binding=temporal_binding,
        forbidden_inferences=envelope.execution_boundary.forbidden_inferences,
        adapter_envelope=envelope,
        runtime_authorized=False,
        probability_status="UNKNOWN",
    )


def compile_fixture_registry_v02(
    canonical_mappings: Mapping[str, Mapping[str, Any]],
    fixture_registry: Mapping[str, Any],
) -> tuple[ManifestationConditionBindingV02, ...]:
    """Compile exactly the bounded v0.2 fixture set; no discovery path exists."""

    if str(fixture_registry.get("schema_version", "")).strip() != SCHEMA_VERSION:
        raise ValueError("fixture registry schema_version must be 0.2")

    raw = _sequence(fixture_registry.get("fixtures"), "fixtures")
    compiled: list[ManifestationConditionBindingV02] = []
    seen: set[str] = set()

    for index, item in enumerate(raw):
        fixture = _mapping(item, f"fixtures[{index}]")
        mapping_id = _required_text(
            fixture.get("mapping_id"), f"fixtures[{index}].mapping_id"
        )
        if mapping_id in seen:
            raise ValueError(f"duplicate fixture mapping_id: {mapping_id}")
        seen.add(mapping_id)

        canonical = canonical_mappings.get(mapping_id)
        if canonical is None:
            raise ValueError(
                f"fixture mapping_id has no supplied canonical mapping: {mapping_id}"
            )
        compiled.append(
            compile_manifestation_condition_binding_v02(canonical, fixture)
        )

    if seen != ALLOWED_MAPPING_IDS:
        missing = sorted(ALLOWED_MAPPING_IDS - seen)
        extra = sorted(seen - ALLOWED_MAPPING_IDS)
        raise ValueError(
            f"v0.2 registry must contain exact bounded mapping set; missing={missing}, extra={extra}"
        )

    return tuple(sorted(compiled, key=lambda item: item.mapping_id))

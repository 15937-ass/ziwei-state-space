"""Product manifestation structured-condition / temporal binding v0.1.

This module closes Product gaps PG-006 and PG-007 for a bounded accepted
checkpoint. It is deliberately non-production.

Important design rule: this module is NOT a free-text parser. A Product-owned
curated fixture must declare the structure to retain. The compiler only verifies
that the declared evidence is present verbatim in the accepted canonical
mapping and that temporal scope is an exact governed expansion of the canonical
time_layer.

No runtime authorization, probability, ranking, event inference, or Knowledge
semantic rewrite is performed here.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping, Sequence

from .manifestation_adapter_contract_v0_2 import (
    MappingAdapterEnvelopeV02,
    compile_mapping_adapter_envelope,
)


SCHEMA_VERSION = "0.1"
CONDITION_KINDS = frozenset(
    {"CROSS_PALACE_DEPENDENCY", "ALTERNATIVES", "SOURCE_TEXT_ONLY"}
)
TEMPORAL_SCOPE_MAP = {
    "NATAL": ("NATAL",),
    "DECADE_YEAR": ("DECADE", "YEAR"),
}
TEMPORAL_BINDING_MODE = "EXACT_DECLARED_SCOPES"


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


@dataclass(frozen=True)
class CrossPalaceDependencyV01:
    relation: str
    context_text: str
    dependency_text: str

    def __post_init__(self) -> None:
        if self.relation != "OPPOSITE_PALACE":
            raise ValueError("v0.1 supports only OPPOSITE_PALACE relation")
        if not self.context_text.strip() or not self.dependency_text.strip():
            raise ValueError("cross-palace context/dependency text is required")


@dataclass(frozen=True)
class AlternativeConditionV01:
    operator: str
    source_operator_token: str
    context_text: str
    alternatives: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.operator != "OR":
            raise ValueError("source-explicit alternatives must remain OR")
        if not self.source_operator_token.strip():
            raise ValueError("source_operator_token is required")
        if not self.context_text.strip():
            raise ValueError("alternative context_text is required")
        if len(self.alternatives) < 2:
            raise ValueError("OR alternatives require at least two branches")


@dataclass(frozen=True)
class SourceTextOnlyConditionV01:
    source_text: str

    def __post_init__(self) -> None:
        if not self.source_text.strip():
            raise ValueError("SourceTextOnlyConditionV01.source_text is required")


@dataclass(frozen=True)
class TemporalLayerBindingV01:
    source_time_layer: str
    required_scopes: tuple[str, ...]
    binding_mode: str = TEMPORAL_BINDING_MODE
    event_outcome_inference_allowed: bool = False

    def __post_init__(self) -> None:
        expected = TEMPORAL_SCOPE_MAP.get(self.source_time_layer)
        if expected is None:
            raise ValueError(
                f"unsupported canonical time_layer: {self.source_time_layer}"
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
            raise ValueError(
                "temporal layer binding cannot infer an event/outcome"
            )


@dataclass(frozen=True)
class ManifestationConditionBindingV01:
    schema_version: str
    mapping_id: str
    fixture_id: str
    source_condition_text: str
    condition_kind: str
    condition: (
        CrossPalaceDependencyV01
        | AlternativeConditionV01
        | SourceTextOnlyConditionV01
    )
    temporal_binding: TemporalLayerBindingV01
    forbidden_inferences: tuple[str, ...]
    adapter_envelope: MappingAdapterEnvelopeV02
    runtime_authorized: bool = False
    probability_status: str = "UNKNOWN"

    def __post_init__(self) -> None:
        if self.schema_version != SCHEMA_VERSION:
            raise ValueError(
                "ManifestationConditionBindingV01 schema_version must be 0.1"
            )
        if self.condition_kind not in CONDITION_KINDS:
            raise ValueError(
                f"unsupported condition_kind: {self.condition_kind}"
            )
        if self.runtime_authorized:
            raise ValueError("condition binding cannot authorize runtime")
        if self.probability_status != "UNKNOWN":
            raise ValueError("condition binding probability_status must be UNKNOWN")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _verify_verbatim(source_text: str, fragment: str, field: str) -> None:
    if fragment not in source_text:
        raise ValueError(
            f"{field} must be retained verbatim from source_condition_text"
        )


def _compile_cross_palace(
    raw: Mapping[str, Any],
    *,
    source_text: str,
) -> CrossPalaceDependencyV01:
    relation = _required_text(raw.get("relation"), "condition.relation")
    context_text = _required_text(
        raw.get("context_text"), "condition.context_text"
    )
    dependency_text = _required_text(
        raw.get("dependency_text"), "condition.dependency_text"
    )
    _verify_verbatim(source_text, context_text, "condition.context_text")
    _verify_verbatim(source_text, dependency_text, "condition.dependency_text")
    return CrossPalaceDependencyV01(
        relation=relation,
        context_text=context_text,
        dependency_text=dependency_text,
    )


def _compile_alternatives(
    raw: Mapping[str, Any],
    *,
    source_text: str,
) -> AlternativeConditionV01:
    operator = _required_text(raw.get("operator"), "condition.operator")
    source_operator_token = _required_text(
        raw.get("source_operator_token"), "condition.source_operator_token"
    )
    context_text = _required_text(
        raw.get("context_text"), "condition.context_text"
    )
    alternatives = _text_tuple(
        raw.get("alternatives", []),
        "condition.alternatives",
        allow_empty=False,
    )

    _verify_verbatim(
        source_text, source_operator_token, "condition.source_operator_token"
    )
    _verify_verbatim(source_text, context_text, "condition.context_text")
    for index, alternative in enumerate(alternatives):
        _verify_verbatim(
            source_text,
            alternative,
            f"condition.alternatives[{index}]",
        )

    return AlternativeConditionV01(
        operator=operator,
        source_operator_token=source_operator_token,
        context_text=context_text,
        alternatives=alternatives,
    )


def _compile_source_text_only(
    raw: Mapping[str, Any],
    *,
    source_text: str,
) -> SourceTextOnlyConditionV01:
    retained = _required_text(raw.get("source_text"), "condition.source_text")
    if retained != source_text:
        raise ValueError(
            "SOURCE_TEXT_ONLY condition must retain exact source_condition_text"
        )
    return SourceTextOnlyConditionV01(source_text=retained)


def _compile_temporal_binding(
    raw: Mapping[str, Any],
    *,
    canonical_time_layer: str,
) -> TemporalLayerBindingV01:
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
    return TemporalLayerBindingV01(
        source_time_layer=source_time_layer,
        required_scopes=required_scopes,
        binding_mode=_required_text(
            raw.get("binding_mode"), "temporal_binding.binding_mode"
        ),
        event_outcome_inference_allowed=bool(
            raw.get("event_outcome_inference_allowed", False)
        ),
    )


def compile_manifestation_condition_binding(
    canonical_mapping: Mapping[str, Any],
    fixture: Mapping[str, Any],
) -> ManifestationConditionBindingV01:
    """Compile one curated Product fixture against an accepted canonical mapping."""

    if str(fixture.get("schema_version", "")).strip() != SCHEMA_VERSION:
        raise ValueError("condition fixture schema_version must be 0.1")

    mapping_id = _required_text(
        canonical_mapping.get("mapping_id"), "mapping_id"
    )
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
        fixture.get("source_condition_text"),
        "fixture.source_condition_text",
    )
    if fixture_source_text != source_text:
        raise ValueError(
            "fixture source_condition_text must exactly match canonical mapping"
        )

    kind = _required_text(
        fixture.get("condition_kind"), "fixture.condition_kind"
    )
    if kind not in CONDITION_KINDS:
        raise ValueError(f"unsupported condition_kind: {kind}")

    condition_raw = _mapping(fixture.get("condition"), "fixture.condition")
    if kind == "CROSS_PALACE_DEPENDENCY":
        condition = _compile_cross_palace(
            condition_raw, source_text=source_text
        )
    elif kind == "ALTERNATIVES":
        condition = _compile_alternatives(
            condition_raw, source_text=source_text
        )
    else:
        condition = _compile_source_text_only(
            condition_raw, source_text=source_text
        )

    temporal_raw = _mapping(
        fixture.get("temporal_binding"), "fixture.temporal_binding"
    )
    temporal_binding = _compile_temporal_binding(
        temporal_raw,
        canonical_time_layer=envelope.conditions.time_layer,
    )

    return ManifestationConditionBindingV01(
        schema_version=SCHEMA_VERSION,
        mapping_id=mapping_id,
        fixture_id=_required_text(
            fixture.get("fixture_id"), "fixture.fixture_id"
        ),
        source_condition_text=source_text,
        condition_kind=kind,
        condition=condition,
        temporal_binding=temporal_binding,
        forbidden_inferences=envelope.execution_boundary.forbidden_inferences,
        adapter_envelope=envelope,
        runtime_authorized=False,
        probability_status="UNKNOWN",
    )


def compile_fixture_registry(
    canonical_mappings: Mapping[str, Mapping[str, Any]],
    fixture_registry: Mapping[str, Any],
) -> tuple[ManifestationConditionBindingV01, ...]:
    """Compile only explicitly enumerated fixtures; there is no discovery/parser path."""

    if str(fixture_registry.get("schema_version", "")).strip() != SCHEMA_VERSION:
        raise ValueError("fixture registry schema_version must be 0.1")

    raw = _sequence(fixture_registry.get("fixtures"), "fixtures")
    compiled: list[ManifestationConditionBindingV01] = []
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
            compile_manifestation_condition_binding(canonical, fixture)
        )

    return tuple(sorted(compiled, key=lambda item: item.mapping_id))

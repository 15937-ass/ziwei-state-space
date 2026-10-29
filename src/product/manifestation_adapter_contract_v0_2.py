"""Product manifestation adapter contract v0.2.

This is a versioned, non-production compatibility envelope.  It preserves
already-reviewed canonical manifestation semantics that Product v0.1 could not
retain losslessly (PG-001..PG-005) without authorizing runtime routing,
probability, ranking, or Product Knowledge promotion.

The envelope deliberately carries source text and review metadata as data.  It
does not infer chart facts, action completion, event outcomes, or hidden
condition semantics.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping, Sequence


SCHEMA_VERSION = "0.2"
ACTION_BINDING_NAMESPACE = "A_t.actions"
PROBABILITY_STATUS = "UNKNOWN"


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


def _text_tuple(value: Any, field: str, *, allow_empty: bool = True) -> tuple[str, ...]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise ValueError(f"{field} must be an array")
    out = tuple(str(item).strip() for item in value if str(item).strip())
    if not allow_empty and not out:
        raise ValueError(f"{field} cannot be empty")
    return out


def _mapping(value: Any, field: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{field} must be an object")
    return value


@dataclass(frozen=True)
class CanonicalReviewAxis:
    state: str
    value: str | None

    def __post_init__(self) -> None:
        if not self.state.strip():
            raise ValueError("CanonicalReviewAxis.state is required")
        if self.state == "KNOWN" and not self.value:
            raise ValueError("KNOWN CanonicalReviewAxis requires value")


@dataclass(frozen=True)
class SupersessionTrace:
    supersedes: tuple[str, ...]
    superseded_by: tuple[str, ...]
    reason: str | None


@dataclass(frozen=True)
class ReviewProvenance:
    review_status: str
    reviewer_type: str
    reviewer_id: str
    reviewed_at: str
    source_span_verified: bool
    normalization_verified: bool


@dataclass(frozen=True)
class ActionPrerequisiteBinding:
    source_text: str
    source_status: str
    target_namespace: str = ACTION_BINDING_NAMESPACE
    match_mode: str = "EXTERNAL_EXPLICIT_ONLY"
    chart_inference_allowed: bool = False

    def __post_init__(self) -> None:
        if not self.source_text.strip():
            raise ValueError("ActionPrerequisiteBinding.source_text is required")
        if not self.source_status.strip():
            raise ValueError("ActionPrerequisiteBinding.source_status is required")
        if self.target_namespace != ACTION_BINDING_NAMESPACE:
            raise ValueError("action prerequisite must bind to A_t.actions")
        if self.chart_inference_allowed:
            raise ValueError("action prerequisite cannot be inferred from chart")


@dataclass(frozen=True)
class NodeAdapterEnvelopeV02:
    schema_version: str
    manifestation_id: str
    parent_id: str | None
    domain: str
    abstraction_level: str
    source_supported_labels: tuple[str, ...]
    source_rule_ids: tuple[str, ...]
    source_refs: tuple[str, ...]
    output_kind: CanonicalReviewAxis
    event_specificity: CanonicalReviewAxis
    source_epistemic: str
    normalization_epistemic: str
    review_provenance: ReviewProvenance
    mapping_review_refs: tuple[str, ...]
    identity_rationale: str
    ambiguity_notes: tuple[str, ...]
    unresolved_notes: tuple[str, ...]
    canonical_identity_status: str
    supersession: SupersessionTrace
    probability_status: str = PROBABILITY_STATUS
    runtime_authorized: bool = False

    def __post_init__(self) -> None:
        if self.schema_version != SCHEMA_VERSION:
            raise ValueError("NodeAdapterEnvelopeV02 schema_version must be 0.2")
        if self.probability_status != PROBABILITY_STATUS:
            raise ValueError("adapter envelope requires probability_status=UNKNOWN")
        if self.runtime_authorized:
            raise ValueError("adapter envelope cannot authorize runtime")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class MappingConditionsV02:
    time_layer: str
    source_condition_text: str
    antecedent_rule_ids: tuple[str, ...]
    modality_terms: tuple[str, ...]
    action_prerequisites: tuple[ActionPrerequisiteBinding, ...]
    unresolved_semantics: tuple[str, ...]


@dataclass(frozen=True)
class ExecutionBoundaryV02:
    canonical_mapping_status: str
    canonical_mapping_approved: bool
    execution_readiness: str
    knowledge_executable: bool
    knowledge_product_consumable: bool
    execution_blockers: tuple[str, ...]
    forbidden_inferences: tuple[str, ...]
    negative_boundary_review_refs: tuple[str, ...]
    runtime_authorized: bool = False

    def __post_init__(self) -> None:
        if self.runtime_authorized:
            raise ValueError("v0.2 adapter boundary cannot authorize runtime")


@dataclass(frozen=True)
class MappingAdapterEnvelopeV02:
    schema_version: str
    mapping_id: str
    primary_source_rule_id: str
    source_rule_ids: tuple[str, ...]
    manifestation_id: str
    source_refs: tuple[str, ...]
    positive_review_refs: tuple[str, ...]
    source_epistemic: str
    normalization_epistemic: str
    output_kind: CanonicalReviewAxis
    event_specificity: CanonicalReviewAxis
    conditions: MappingConditionsV02
    execution_boundary: ExecutionBoundaryV02
    supersession: SupersessionTrace
    probability_status: str = PROBABILITY_STATUS

    def __post_init__(self) -> None:
        if self.schema_version != SCHEMA_VERSION:
            raise ValueError("MappingAdapterEnvelopeV02 schema_version must be 0.2")
        if self.probability_status != PROBABILITY_STATUS:
            raise ValueError("adapter envelope requires probability_status=UNKNOWN")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _compile_axis(payload: Mapping[str, Any], field: str) -> CanonicalReviewAxis:
    raw = _mapping(payload.get(field), field)
    state = _required_text(raw.get("state"), f"{field}.state")
    value = _optional_text(raw.get("value"))
    return CanonicalReviewAxis(state=state, value=value)


def _compile_supersession(payload: Mapping[str, Any]) -> SupersessionTrace:
    raw = _mapping(payload.get("supersession"), "supersession")
    return SupersessionTrace(
        supersedes=_text_tuple(raw.get("supersedes", []), "supersession.supersedes"),
        superseded_by=_text_tuple(
            raw.get("superseded_by", []), "supersession.superseded_by"
        ),
        reason=_optional_text(raw.get("reason")),
    )


def _compile_review_provenance(payload: Mapping[str, Any]) -> ReviewProvenance:
    raw = _mapping(payload.get("review_provenance"), "review_provenance")
    return ReviewProvenance(
        review_status=_required_text(
            raw.get("review_status"), "review_provenance.review_status"
        ),
        reviewer_type=_required_text(
            raw.get("reviewer_type"), "review_provenance.reviewer_type"
        ),
        reviewer_id=_required_text(
            raw.get("reviewer_id"), "review_provenance.reviewer_id"
        ),
        reviewed_at=_required_text(
            raw.get("reviewed_at"), "review_provenance.reviewed_at"
        ),
        source_span_verified=bool(raw.get("source_span_verified", False)),
        normalization_verified=bool(raw.get("normalization_verified", False)),
    )


def compile_node_adapter_envelope(
    payload: Mapping[str, Any],
) -> NodeAdapterEnvelopeV02:
    """Preserve a reviewed canonical node without promoting it to production."""

    probability_status = _required_text(
        payload.get("probability_status"), "probability_status"
    )
    if probability_status != PROBABILITY_STATUS:
        raise ValueError("canonical node probability_status must remain UNKNOWN")

    return NodeAdapterEnvelopeV02(
        schema_version=SCHEMA_VERSION,
        manifestation_id=_required_text(
            payload.get("manifestation_id"), "manifestation_id"
        ),
        parent_id=_optional_text(payload.get("parent_id")),
        domain=_required_text(payload.get("domain"), "domain"),
        abstraction_level=_required_text(
            payload.get("abstraction_level"), "abstraction_level"
        ),
        source_supported_labels=_text_tuple(
            payload.get("source_supported_labels", []),
            "source_supported_labels",
            allow_empty=False,
        ),
        source_rule_ids=_text_tuple(
            payload.get("source_rule_ids", []),
            "source_rule_ids",
            allow_empty=False,
        ),
        source_refs=_text_tuple(
            payload.get("source_refs", []), "source_refs", allow_empty=False
        ),
        output_kind=_compile_axis(payload, "output_kind"),
        event_specificity=_compile_axis(payload, "event_specificity"),
        source_epistemic=_required_text(
            payload.get("source_epistemic"), "source_epistemic"
        ),
        normalization_epistemic=_required_text(
            payload.get("normalization_epistemic"), "normalization_epistemic"
        ),
        review_provenance=_compile_review_provenance(payload),
        mapping_review_refs=_text_tuple(
            payload.get("mapping_review_refs", []), "mapping_review_refs"
        ),
        identity_rationale=_required_text(
            payload.get("identity_rationale"), "identity_rationale"
        ),
        ambiguity_notes=_text_tuple(
            payload.get("ambiguity_notes", []), "ambiguity_notes"
        ),
        unresolved_notes=_text_tuple(
            payload.get("unresolved_notes", []), "unresolved_notes"
        ),
        canonical_identity_status=_required_text(
            payload.get("canonical_identity_status"), "canonical_identity_status"
        ),
        supersession=_compile_supersession(payload),
        probability_status=probability_status,
    )


def _compile_action_prerequisites(
    conditions: Mapping[str, Any],
) -> tuple[ActionPrerequisiteBinding, ...]:
    raw = conditions.get("real_world_prerequisites", [])
    if not isinstance(raw, Sequence) or isinstance(raw, (str, bytes)):
        raise ValueError("conditions.real_world_prerequisites must be an array")

    bindings: list[ActionPrerequisiteBinding] = []
    for index, item in enumerate(raw):
        record = _mapping(
            item, f"conditions.real_world_prerequisites[{index}]"
        )
        bindings.append(
            ActionPrerequisiteBinding(
                source_text=_required_text(
                    record.get("text"),
                    f"conditions.real_world_prerequisites[{index}].text",
                ),
                source_status=_required_text(
                    record.get("status"),
                    f"conditions.real_world_prerequisites[{index}].status",
                ),
            )
        )
    return tuple(bindings)


def compile_mapping_adapter_envelope(
    payload: Mapping[str, Any],
) -> MappingAdapterEnvelopeV02:
    """Preserve canonical mapping metadata without interpreting it as executable."""

    probability_status = _required_text(
        payload.get("probability_status"), "probability_status"
    )
    if probability_status != PROBABILITY_STATUS:
        raise ValueError("canonical mapping probability_status must remain UNKNOWN")

    conditions = _mapping(payload.get("conditions"), "conditions")
    review_refs = _mapping(payload.get("review_refs"), "review_refs")

    boundary = ExecutionBoundaryV02(
        canonical_mapping_status=_required_text(
            payload.get("canonical_mapping_status"), "canonical_mapping_status"
        ),
        canonical_mapping_approved=bool(
            payload.get("canonical_mapping_approved", False)
        ),
        execution_readiness=_required_text(
            payload.get("execution_readiness"), "execution_readiness"
        ),
        knowledge_executable=bool(payload.get("executable", False)),
        knowledge_product_consumable=bool(
            payload.get("product_consumable", False)
        ),
        execution_blockers=_text_tuple(
            payload.get("execution_blockers", []), "execution_blockers"
        ),
        forbidden_inferences=_text_tuple(
            payload.get("forbidden_inferences", []), "forbidden_inferences"
        ),
        negative_boundary_review_refs=_text_tuple(
            review_refs.get("negative_boundaries", []),
            "review_refs.negative_boundaries",
        ),
    )

    return MappingAdapterEnvelopeV02(
        schema_version=SCHEMA_VERSION,
        mapping_id=_required_text(payload.get("mapping_id"), "mapping_id"),
        primary_source_rule_id=_required_text(
            payload.get("primary_source_rule_id"), "primary_source_rule_id"
        ),
        source_rule_ids=_text_tuple(
            payload.get("source_rule_ids", []),
            "source_rule_ids",
            allow_empty=False,
        ),
        manifestation_id=_required_text(
            payload.get("manifestation_id"), "manifestation_id"
        ),
        source_refs=_text_tuple(
            payload.get("source_refs", []), "source_refs", allow_empty=False
        ),
        positive_review_refs=_text_tuple(
            review_refs.get("positive", []), "review_refs.positive"
        ),
        source_epistemic=_required_text(
            payload.get("source_epistemic"), "source_epistemic"
        ),
        normalization_epistemic=_required_text(
            payload.get("normalization_epistemic"), "normalization_epistemic"
        ),
        output_kind=_compile_axis(payload, "output_kind"),
        event_specificity=_compile_axis(payload, "event_specificity"),
        conditions=MappingConditionsV02(
            time_layer=_required_text(
                conditions.get("time_layer"), "conditions.time_layer"
            ),
            source_condition_text=_required_text(
                conditions.get("source_condition_text"),
                "conditions.source_condition_text",
            ),
            antecedent_rule_ids=_text_tuple(
                conditions.get("antecedent_rule_ids", []),
                "conditions.antecedent_rule_ids",
            ),
            modality_terms=_text_tuple(
                conditions.get("modality_terms", []),
                "conditions.modality_terms",
            ),
            action_prerequisites=_compile_action_prerequisites(conditions),
            unresolved_semantics=_text_tuple(
                conditions.get("unresolved_semantics", []),
                "conditions.unresolved_semantics",
            ),
        ),
        execution_boundary=boundary,
        supersession=_compile_supersession(payload),
        probability_status=probability_status,
    )

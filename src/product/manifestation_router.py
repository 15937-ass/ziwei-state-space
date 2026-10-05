"""PL3-M source-supported manifestation possibility router v0.1.

The router consumes an already-reviewed KB-WP06C mapping registry and a
validated manifestation ontology.  It outputs source-supported possibilities
only.  It has no probability, ranking, or personalized preference logic.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping, Sequence

from .manifestation_ontology import (
    ManifestationOntologyRegistry,
    ManifestationSourceRef,
)


MAPPING_REGISTRY_STATUSES = frozenset(
    {
        "EMPTY_PENDING_KB_WP06C",
        "TEST_ONLY",
        "CANONICAL_READY",
    }
)

MAPPING_EVIDENCE_TIERS = frozenset(
    {
        "EXPLICIT",
        "TRANSPARENT_INFERENCE",
        "CASE_SUPPORT_ONLY",
        "HYPOTHESIS",
    }
)

ROUTABLE_EVIDENCE_TIERS = frozenset(
    {"EXPLICIT", "TRANSPARENT_INFERENCE"}
)

ROUTER_DISPOSITIONS = frozenset(
    {
        "ROUTED",
        "NO_ACTIVE_MAPPING",
        "ONTOLOGY_NOT_READY",
        "MAPPING_REGISTRY_NOT_READY",
    }
)

_CANONICAL_REVIEW_STATUSES = frozenset(
    {"SOURCE_SPAN_VERIFIED", "HUMAN_VERIFIED"}
)

_FORBIDDEN_MAPPING_FIELDS = frozenset(
    {
        "probability",
        "frequency",
        "weight",
        "score",
        "posterior",
        "likelihood",
        "hazard",
        "odds",
        "rank",
    }
)


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


def _text_tuple(
    value: Any,
    field: str,
    *,
    allow_empty: bool = True,
) -> tuple[str, ...]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise ValueError(f"{field} must be an array")
    out = tuple(sorted({str(item).strip() for item in value if str(item).strip()}))
    if not allow_empty and not out:
        raise ValueError(f"{field} cannot be empty")
    return out


@dataclass(frozen=True)
class ManifestationMapping:
    mapping_id: str
    required_activation_ids: tuple[str, ...]
    required_rule_ids: tuple[str, ...]
    manifestation_id: str
    evidence_tier: str
    probability_status: str
    source_refs: tuple[ManifestationSourceRef, ...]
    notes: str | None = None

    def __post_init__(self) -> None:
        if not self.mapping_id.strip():
            raise ValueError("ManifestationMapping.mapping_id is required")
        if not self.manifestation_id.strip():
            raise ValueError(
                f"{self.mapping_id}: manifestation_id is required"
            )
        if not self.required_activation_ids and not self.required_rule_ids:
            raise ValueError(
                f"{self.mapping_id}: mapping requires activation IDs and/or rule IDs"
            )
        if self.evidence_tier not in MAPPING_EVIDENCE_TIERS:
            raise ValueError(
                f"{self.mapping_id}: unsupported evidence_tier {self.evidence_tier}"
            )
        if self.probability_status != "UNKNOWN":
            raise ValueError(
                f"{self.mapping_id}: source mapping requires probability_status=UNKNOWN"
            )
        if not self.source_refs:
            raise ValueError(f"{self.mapping_id}: source_refs cannot be empty")


@dataclass(frozen=True)
class ManifestationMappingRegistry:
    schema_version: str
    registry_status: str
    knowledge_artifact_version: str | None
    mappings: tuple[ManifestationMapping, ...]
    blocked_reason: str | None = None

    def __post_init__(self) -> None:
        if self.schema_version != "0.1":
            raise ValueError(
                "ManifestationMappingRegistry schema_version must be 0.1"
            )
        if self.registry_status not in MAPPING_REGISTRY_STATUSES:
            raise ValueError(
                f"unsupported manifestation mapping status: {self.registry_status}"
            )
        if self.registry_status == "EMPTY_PENDING_KB_WP06C":
            if self.mappings:
                raise ValueError(
                    "EMPTY_PENDING_KB_WP06C registry must contain zero mappings"
                )
            if self.knowledge_artifact_version is not None:
                raise ValueError(
                    "pending mapping registry cannot claim knowledge_artifact_version"
                )
        elif self.registry_status == "CANONICAL_READY":
            if not self.mappings:
                raise ValueError("CANONICAL_READY mapping registry requires mappings")
            if not self.knowledge_artifact_version:
                raise ValueError(
                    "CANONICAL_READY mapping registry requires knowledge_artifact_version"
                )

    @property
    def canonical_ready(self) -> bool:
        return self.registry_status == "CANONICAL_READY"

    @property
    def is_empty(self) -> bool:
        return not self.mappings


@dataclass(frozen=True)
class SymbolicActivationContext:
    active_activation_ids: tuple[str, ...]
    active_rule_ids: tuple[str, ...]
    evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.active_activation_ids and not self.active_rule_ids:
            raise ValueError(
                "SymbolicActivationContext requires at least one active activation/rule"
            )


@dataclass(frozen=True)
class SourceSupportedPossibility:
    possibility_status: str
    mapping_id: str
    manifestation_id: str
    domain: str
    abstraction_level: str
    event_specificity: str
    source_supported_labels: tuple[str, ...]
    evidence_tier: str
    matched_activation_ids: tuple[str, ...]
    matched_rule_ids: tuple[str, ...]
    mapping_source_refs: tuple[ManifestationSourceRef, ...]
    ontology_source_refs: tuple[ManifestationSourceRef, ...]
    probability_status: str = "UNKNOWN"

    def __post_init__(self) -> None:
        if self.possibility_status != "SOURCE_SUPPORTED_POSSIBILITY":
            raise ValueError(
                "PL3-M v0.1 possibility status must be SOURCE_SUPPORTED_POSSIBILITY"
            )
        if self.evidence_tier not in ROUTABLE_EVIDENCE_TIERS:
            raise ValueError(
                "source-supported possibility requires routable evidence tier"
            )
        if self.probability_status != "UNKNOWN":
            raise ValueError(
                "source-supported possibility cannot carry empirical probability"
            )


@dataclass(frozen=True)
class HeldManifestationMapping:
    mapping_id: str
    manifestation_id: str
    evidence_tier: str
    reason: str


@dataclass(frozen=True)
class PossibilityRoutingResult:
    schema_version: str
    disposition: str
    possibilities: tuple[SourceSupportedPossibility, ...]
    held_mappings: tuple[HeldManifestationMapping, ...]
    ontology_status: str
    mapping_registry_status: str

    def __post_init__(self) -> None:
        if self.schema_version != "0.1":
            raise ValueError("PossibilityRoutingResult schema_version must be 0.1")
        if self.disposition not in ROUTER_DISPOSITIONS:
            raise ValueError(f"unsupported router disposition: {self.disposition}")

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "disposition": self.disposition,
            "possibilities": [asdict(item) for item in self.possibilities],
            "held_mappings": [asdict(item) for item in self.held_mappings],
            "ontology_status": self.ontology_status,
            "mapping_registry_status": self.mapping_registry_status,
        }


def _compile_source_refs(
    raw: Any,
    *,
    mapping_id: str,
    registry_status: str,
) -> tuple[ManifestationSourceRef, ...]:
    if not isinstance(raw, Sequence) or isinstance(raw, (str, bytes)):
        raise ValueError(f"{mapping_id}.source_refs must be an array")

    refs: list[ManifestationSourceRef] = []
    for index, item in enumerate(raw):
        if not isinstance(item, Mapping):
            raise ValueError(
                f"{mapping_id}.source_refs[{index}] must be an object"
            )
        ref = ManifestationSourceRef(
            source_id=_required_text(
                item.get("source_id"),
                f"{mapping_id}.source_refs[{index}].source_id",
            ),
            source_location=_required_text(
                item.get("source_location"),
                f"{mapping_id}.source_refs[{index}].source_location",
            ),
            review_status=_required_text(
                item.get("review_status"),
                f"{mapping_id}.source_refs[{index}].review_status",
            ),
            source_span_verified=bool(item.get("source_span_verified", False)),
        )
        if registry_status == "CANONICAL_READY":
            if (
                ref.review_status not in _CANONICAL_REVIEW_STATUSES
                or not ref.source_span_verified
            ):
                raise ValueError(
                    f"{mapping_id}: canonical mapping source refs require "
                    "SOURCE_SPAN_VERIFIED/HUMAN_VERIFIED and "
                    "source_span_verified=true"
                )
        elif registry_status == "TEST_ONLY":
            if ref.review_status != "TEST_ONLY":
                raise ValueError(
                    f"{mapping_id}: TEST_ONLY mappings require TEST_ONLY source refs"
                )
        refs.append(ref)

    if not refs:
        raise ValueError(f"{mapping_id}.source_refs cannot be empty")
    return tuple(
        sorted(
            refs,
            key=lambda item: (
                item.source_id,
                item.source_location,
                item.review_status,
            ),
        )
    )


def compile_manifestation_mapping_registry(
    payload: Mapping[str, Any],
) -> ManifestationMappingRegistry:
    if str(payload.get("schema_version", "")).strip() != "0.1":
        raise ValueError("manifestation mapping schema_version must be 0.1")

    registry_status = _required_text(
        payload.get("registry_status"), "registry_status"
    )
    if registry_status not in MAPPING_REGISTRY_STATUSES:
        raise ValueError(
            f"unsupported manifestation mapping status: {registry_status}"
        )

    raw = payload.get("mappings")
    if not isinstance(raw, Sequence) or isinstance(raw, (str, bytes)):
        raise ValueError("manifestation mappings must be an array")

    mappings: list[ManifestationMapping] = []
    seen: set[str] = set()

    for index, row in enumerate(raw):
        if not isinstance(row, Mapping):
            raise ValueError(f"mappings[{index}] must be an object")

        forbidden = sorted(_FORBIDDEN_MAPPING_FIELDS.intersection(row))
        if forbidden:
            raise ValueError(
                "source manifestation mapping cannot contain empirical/ranking "
                "fields: " + ", ".join(forbidden)
            )

        mapping_id = _required_text(
            row.get("mapping_id"), f"mappings[{index}].mapping_id"
        )
        if mapping_id in seen:
            raise ValueError(f"duplicate manifestation mapping_id: {mapping_id}")
        seen.add(mapping_id)

        mappings.append(
            ManifestationMapping(
                mapping_id=mapping_id,
                required_activation_ids=_text_tuple(
                    row.get("required_activation_ids", []),
                    f"{mapping_id}.required_activation_ids",
                ),
                required_rule_ids=_text_tuple(
                    row.get("required_rule_ids", []),
                    f"{mapping_id}.required_rule_ids",
                ),
                manifestation_id=_required_text(
                    row.get("manifestation_id"),
                    f"{mapping_id}.manifestation_id",
                ),
                evidence_tier=_required_text(
                    row.get("evidence_tier"),
                    f"{mapping_id}.evidence_tier",
                ),
                probability_status=_required_text(
                    row.get("probability_status"),
                    f"{mapping_id}.probability_status",
                ),
                source_refs=_compile_source_refs(
                    row.get("source_refs"),
                    mapping_id=mapping_id,
                    registry_status=registry_status,
                ),
                notes=_optional_text(row.get("notes")),
            )
        )

    return ManifestationMappingRegistry(
        schema_version="0.1",
        registry_status=registry_status,
        knowledge_artifact_version=_optional_text(
            payload.get("knowledge_artifact_version")
        ),
        blocked_reason=_optional_text(payload.get("blocked_reason")),
        mappings=tuple(sorted(mappings, key=lambda item: item.mapping_id)),
    )


def route_source_supported_possibilities(
    ontology: ManifestationOntologyRegistry,
    mappings: ManifestationMappingRegistry,
    context: SymbolicActivationContext,
) -> PossibilityRoutingResult:
    """Route only source-supported possibilities; never produce probabilities."""

    if ontology.registry_status == "EMPTY_PENDING_KB_WP06B":
        return PossibilityRoutingResult(
            schema_version="0.1",
            disposition="ONTOLOGY_NOT_READY",
            possibilities=(),
            held_mappings=(),
            ontology_status=ontology.registry_status,
            mapping_registry_status=mappings.registry_status,
        )

    if mappings.registry_status == "EMPTY_PENDING_KB_WP06C":
        return PossibilityRoutingResult(
            schema_version="0.1",
            disposition="MAPPING_REGISTRY_NOT_READY",
            possibilities=(),
            held_mappings=(),
            ontology_status=ontology.registry_status,
            mapping_registry_status=mappings.registry_status,
        )

    if ontology.registry_status != mappings.registry_status:
        raise ValueError(
            "ontology and mapping registry must use the same readiness mode "
            "(TEST_ONLY or CANONICAL_READY)"
        )

    nodes = ontology.by_id()
    active_activations = set(context.active_activation_ids)
    active_rules = set(context.active_rule_ids)

    possibilities: list[SourceSupportedPossibility] = []
    held: list[HeldManifestationMapping] = []

    for mapping in mappings.mappings:
        if not set(mapping.required_activation_ids).issubset(active_activations):
            continue
        if not set(mapping.required_rule_ids).issubset(active_rules):
            continue

        node = nodes.get(mapping.manifestation_id)
        if node is None:
            raise ValueError(
                f"{mapping.mapping_id}: manifestation_id not present in ontology: "
                f"{mapping.manifestation_id}"
            )

        if mapping.evidence_tier not in ROUTABLE_EVIDENCE_TIERS:
            held.append(
                HeldManifestationMapping(
                    mapping_id=mapping.mapping_id,
                    manifestation_id=mapping.manifestation_id,
                    evidence_tier=mapping.evidence_tier,
                    reason="NON_CANONICAL_ROUTING_TIER",
                )
            )
            continue

        possibilities.append(
            SourceSupportedPossibility(
                possibility_status="SOURCE_SUPPORTED_POSSIBILITY",
                mapping_id=mapping.mapping_id,
                manifestation_id=node.manifestation_id,
                domain=node.domain,
                abstraction_level=node.abstraction_level,
                event_specificity=node.event_specificity,
                source_supported_labels=node.source_supported_labels,
                evidence_tier=mapping.evidence_tier,
                matched_activation_ids=mapping.required_activation_ids,
                matched_rule_ids=mapping.required_rule_ids,
                mapping_source_refs=mapping.source_refs,
                ontology_source_refs=node.source_refs,
            )
        )

    disposition = "ROUTED" if possibilities else "NO_ACTIVE_MAPPING"
    return PossibilityRoutingResult(
        schema_version="0.1",
        disposition=disposition,
        possibilities=tuple(
            sorted(
                possibilities,
                key=lambda item: (
                    item.manifestation_id,
                    item.mapping_id,
                ),
            )
        ),
        held_mappings=tuple(
            sorted(held, key=lambda item: item.mapping_id)
        ),
        ontology_status=ontology.registry_status,
        mapping_registry_status=mappings.registry_status,
    )

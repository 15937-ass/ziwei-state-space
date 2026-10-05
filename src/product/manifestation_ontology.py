"""PL3-M manifestation ontology adapter v0.1.

This module validates a knowledge-side manifestation ontology artifact.  It
does not invent manifestation categories, probabilities, or chart-to-event
mappings.  Production remains fail-closed until KB-WP06B freezes a consumable
canonical artifact.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping, Sequence


REGISTRY_STATUSES = frozenset(
    {
        "EMPTY_PENDING_KB_WP06B",
        "TEST_ONLY",
        "CANONICAL_READY",
    }
)

PROBABILITY_STATUSES = frozenset({"UNKNOWN"})
EVENT_SPECIFICITIES = frozenset(
    {"ABSTRACT", "SCENE_LEVEL", "CONCRETE_EVENT"}
)

_CANONICAL_REVIEW_STATUSES = frozenset(
    {"SOURCE_SPAN_VERIFIED", "HUMAN_VERIFIED"}
)
_TEST_REVIEW_STATUSES = frozenset({"TEST_ONLY"})

_FORBIDDEN_NODE_FIELDS = frozenset(
    {
        "probability",
        "frequency",
        "weight",
        "score",
        "posterior",
        "likelihood",
        "hazard",
        "odds",
        "rank_probability",
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


def _text_tuple(value: Any, field: str, *, allow_empty: bool = False) -> tuple[str, ...]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise ValueError(f"{field} must be an array")
    out = tuple(sorted({str(item).strip() for item in value if str(item).strip()}))
    if not allow_empty and not out:
        raise ValueError(f"{field} cannot be empty")
    return out


@dataclass(frozen=True)
class ManifestationSourceRef:
    source_id: str
    source_location: str
    review_status: str
    source_span_verified: bool

    def __post_init__(self) -> None:
        if not self.source_id.strip():
            raise ValueError("ManifestationSourceRef.source_id is required")
        if not self.source_location.strip():
            raise ValueError("ManifestationSourceRef.source_location is required")


@dataclass(frozen=True)
class ManifestationNode:
    manifestation_id: str
    parent_id: str | None
    domain: str
    abstraction_level: str
    source_supported_labels: tuple[str, ...]
    source_rule_ids: tuple[str, ...]
    event_specificity: str
    ambiguity_notes: str | None
    probability_status: str
    source_refs: tuple[ManifestationSourceRef, ...]

    def __post_init__(self) -> None:
        if not self.manifestation_id.strip():
            raise ValueError("ManifestationNode.manifestation_id is required")
        if self.parent_id == self.manifestation_id:
            raise ValueError(
                f"{self.manifestation_id}: parent_id cannot reference itself"
            )
        if not self.domain.strip():
            raise ValueError(f"{self.manifestation_id}: domain is required")
        if not self.abstraction_level.strip():
            raise ValueError(
                f"{self.manifestation_id}: abstraction_level is required"
            )
        if not self.source_supported_labels:
            raise ValueError(
                f"{self.manifestation_id}: source_supported_labels cannot be empty"
            )
        if not self.source_rule_ids:
            raise ValueError(
                f"{self.manifestation_id}: source_rule_ids cannot be empty"
            )
        if self.event_specificity not in EVENT_SPECIFICITIES:
            raise ValueError(
                f"{self.manifestation_id}: unsupported event_specificity "
                f"{self.event_specificity}"
            )
        if self.probability_status not in PROBABILITY_STATUSES:
            raise ValueError(
                f"{self.manifestation_id}: canonical manifestation ontology "
                "requires probability_status=UNKNOWN"
            )
        if not self.source_refs:
            raise ValueError(
                f"{self.manifestation_id}: source_refs cannot be empty"
            )


@dataclass(frozen=True)
class ManifestationOntologyRegistry:
    schema_version: str
    registry_status: str
    knowledge_artifact_version: str | None
    nodes: tuple[ManifestationNode, ...]
    blocked_reason: str | None = None

    def __post_init__(self) -> None:
        if self.schema_version != "0.1":
            raise ValueError(
                "ManifestationOntologyRegistry schema_version must be 0.1"
            )
        if self.registry_status not in REGISTRY_STATUSES:
            raise ValueError(
                f"unsupported manifestation registry status: {self.registry_status}"
            )
        if self.registry_status == "EMPTY_PENDING_KB_WP06B":
            if self.nodes:
                raise ValueError(
                    "EMPTY_PENDING_KB_WP06B registry must contain zero nodes"
                )
            if self.knowledge_artifact_version is not None:
                raise ValueError(
                    "pending empty registry cannot claim knowledge_artifact_version"
                )
        elif self.registry_status == "CANONICAL_READY":
            if not self.nodes:
                raise ValueError("CANONICAL_READY registry requires nodes")
            if not self.knowledge_artifact_version:
                raise ValueError(
                    "CANONICAL_READY registry requires knowledge_artifact_version"
                )

    @property
    def canonical_ready(self) -> bool:
        return self.registry_status == "CANONICAL_READY"

    @property
    def is_empty(self) -> bool:
        return not self.nodes

    def by_id(self) -> dict[str, ManifestationNode]:
        return {item.manifestation_id: item for item in self.nodes}

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "registry_status": self.registry_status,
            "knowledge_artifact_version": self.knowledge_artifact_version,
            "blocked_reason": self.blocked_reason,
            "nodes": [asdict(item) for item in self.nodes],
        }


def _compile_source_refs(
    raw: Any,
    *,
    node_id: str,
    registry_status: str,
) -> tuple[ManifestationSourceRef, ...]:
    if not isinstance(raw, Sequence) or isinstance(raw, (str, bytes)):
        raise ValueError(f"{node_id}.source_refs must be an array")

    refs: list[ManifestationSourceRef] = []
    for index, item in enumerate(raw):
        if not isinstance(item, Mapping):
            raise ValueError(
                f"{node_id}.source_refs[{index}] must be an object"
            )
        ref = ManifestationSourceRef(
            source_id=_required_text(
                item.get("source_id"),
                f"{node_id}.source_refs[{index}].source_id",
            ),
            source_location=_required_text(
                item.get("source_location"),
                f"{node_id}.source_refs[{index}].source_location",
            ),
            review_status=_required_text(
                item.get("review_status"),
                f"{node_id}.source_refs[{index}].review_status",
            ),
            source_span_verified=bool(item.get("source_span_verified", False)),
        )

        if registry_status == "CANONICAL_READY":
            if (
                ref.review_status not in _CANONICAL_REVIEW_STATUSES
                or not ref.source_span_verified
            ):
                raise ValueError(
                    f"{node_id}: canonical source refs require "
                    "SOURCE_SPAN_VERIFIED/HUMAN_VERIFIED and "
                    "source_span_verified=true"
                )
        elif registry_status == "TEST_ONLY":
            if ref.review_status not in _TEST_REVIEW_STATUSES:
                raise ValueError(
                    f"{node_id}: TEST_ONLY registry requires TEST_ONLY source refs"
                )

        refs.append(ref)

    if not refs:
        raise ValueError(f"{node_id}.source_refs cannot be empty")
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


def _validate_topology(nodes: Sequence[ManifestationNode]) -> None:
    by_id = {item.manifestation_id: item for item in nodes}

    for node in nodes:
        if node.parent_id is not None and node.parent_id not in by_id:
            raise ValueError(
                f"{node.manifestation_id}: unknown parent_id {node.parent_id}"
            )

    visit: dict[str, int] = {}

    def dfs(node_id: str, trail: tuple[str, ...]) -> None:
        state = visit.get(node_id, 0)
        if state == 2:
            return
        if state == 1:
            raise ValueError(
                "manifestation ontology cycle detected: "
                + " -> ".join(trail + (node_id,))
            )
        visit[node_id] = 1
        parent = by_id[node_id].parent_id
        if parent is not None:
            dfs(parent, trail + (node_id,))
        visit[node_id] = 2

    for node_id in sorted(by_id):
        dfs(node_id, ())


def compile_manifestation_ontology_registry(
    payload: Mapping[str, Any],
) -> ManifestationOntologyRegistry:
    """Validate one manifestation ontology artifact without adding semantics."""

    if str(payload.get("schema_version", "")).strip() != "0.1":
        raise ValueError("manifestation ontology schema_version must be 0.1")

    registry_status = _required_text(
        payload.get("registry_status"), "registry_status"
    )
    if registry_status not in REGISTRY_STATUSES:
        raise ValueError(
            f"unsupported manifestation registry status: {registry_status}"
        )

    raw_nodes = payload.get("nodes")
    if not isinstance(raw_nodes, Sequence) or isinstance(
        raw_nodes, (str, bytes)
    ):
        raise ValueError("manifestation ontology nodes must be an array")

    nodes: list[ManifestationNode] = []
    seen: set[str] = set()

    for index, raw in enumerate(raw_nodes):
        if not isinstance(raw, Mapping):
            raise ValueError(f"nodes[{index}] must be an object")

        forbidden = sorted(_FORBIDDEN_NODE_FIELDS.intersection(raw))
        if forbidden:
            raise ValueError(
                "canonical manifestation node cannot contain empirical numeric "
                "fields: " + ", ".join(forbidden)
            )

        node_id = _required_text(
            raw.get("manifestation_id"),
            f"nodes[{index}].manifestation_id",
        )
        if node_id in seen:
            raise ValueError(f"duplicate manifestation_id: {node_id}")
        seen.add(node_id)

        node = ManifestationNode(
            manifestation_id=node_id,
            parent_id=_optional_text(raw.get("parent_id")),
            domain=_required_text(raw.get("domain"), f"{node_id}.domain"),
            abstraction_level=_required_text(
                raw.get("abstraction_level"),
                f"{node_id}.abstraction_level",
            ),
            source_supported_labels=_text_tuple(
                raw.get("source_supported_labels"),
                f"{node_id}.source_supported_labels",
            ),
            source_rule_ids=_text_tuple(
                raw.get("source_rule_ids"),
                f"{node_id}.source_rule_ids",
            ),
            event_specificity=_required_text(
                raw.get("event_specificity"),
                f"{node_id}.event_specificity",
            ),
            ambiguity_notes=_optional_text(raw.get("ambiguity_notes")),
            probability_status=_required_text(
                raw.get("probability_status"),
                f"{node_id}.probability_status",
            ),
            source_refs=_compile_source_refs(
                raw.get("source_refs"),
                node_id=node_id,
                registry_status=registry_status,
            ),
        )
        nodes.append(node)

    ordered = tuple(sorted(nodes, key=lambda item: item.manifestation_id))
    _validate_topology(ordered)

    return ManifestationOntologyRegistry(
        schema_version="0.1",
        registry_status=registry_status,
        knowledge_artifact_version=_optional_text(
            payload.get("knowledge_artifact_version")
        ),
        blocked_reason=_optional_text(payload.get("blocked_reason")),
        nodes=ordered,
    )

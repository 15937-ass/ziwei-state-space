"""PL3-M Manifestation Ontology adapter v0.1.

The adapter validates knowledge-side WP06B/WP06C shaped documents.  It does not
invent ontology nodes or mappings when the knowledge artifacts are absent.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence


ABSTRACTION_LEVELS = frozenset(
    {"LATENT_ACTIVATION", "MANIFESTATION_FAMILY", "CHANNEL", "EVENT_LABEL"}
)
MAPPING_EVIDENCE_TIERS = frozenset(
    {"EXPLICIT", "TRANSPARENT_INFERENCE", "CASE_SUPPORT_ONLY", "HYPOTHESIS"}
)
PROBABILITY_STATUSES = frozenset({"UNKNOWN", "SOURCE_CLAIM_ONLY", "CALIBRATED"})


def _text(value: Any, field: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise ValueError(f"{field} is required")
    return text


@dataclass(frozen=True)
class ManifestationNode:
    manifestation_id: str
    parent_id: str | None
    domain: str
    abstraction_level: str
    source_supported_labels: tuple[str, ...]
    source_rule_ids: tuple[str, ...]
    event_specificity: str
    ambiguity_notes: str
    probability_status: str

    def __post_init__(self) -> None:
        _text(self.manifestation_id, "manifestation_id")
        _text(self.domain, "domain")
        if self.abstraction_level not in ABSTRACTION_LEVELS:
            raise ValueError(f"unsupported abstraction_level: {self.abstraction_level}")
        if self.probability_status not in PROBABILITY_STATUSES:
            raise ValueError(f"unsupported probability_status: {self.probability_status}")
        if self.probability_status == "CALIBRATED":
            raise ValueError(
                "WP06B ontology adapter cannot accept calibrated probability truth"
            )


@dataclass(frozen=True)
class ManifestationMapping:
    mapping_id: str
    activation_id: str
    candidate_manifestation_ids: tuple[str, ...]
    evidence_tier: str
    source_rule_ids: tuple[str, ...]
    source_trace: tuple[str, ...]
    unresolved_alternatives: tuple[str, ...]

    def __post_init__(self) -> None:
        _text(self.mapping_id, "mapping_id")
        _text(self.activation_id, "activation_id")
        if self.evidence_tier not in MAPPING_EVIDENCE_TIERS:
            raise ValueError(f"unsupported evidence_tier: {self.evidence_tier}")
        if not self.candidate_manifestation_ids:
            raise ValueError("candidate_manifestation_ids cannot be empty")
        if not self.source_rule_ids and self.evidence_tier != "HYPOTHESIS":
            raise ValueError("source-backed mapping requires source_rule_ids")


@dataclass(frozen=True)
class ManifestationOntologyBundle:
    schema_version: str
    ontology_version: str
    nodes: tuple[ManifestationNode, ...]
    mappings: tuple[ManifestationMapping, ...]
    status: str

    def __post_init__(self) -> None:
        if self.schema_version != "0.1":
            raise ValueError("ManifestationOntologyBundle schema_version must be 0.1")
        _text(self.ontology_version, "ontology_version")
        if self.status not in {"READY", "EMPTY_KNOWLEDGE_DEPENDENCY"}:
            raise ValueError(f"unsupported ontology bundle status: {self.status}")

    def node_by_id(self) -> dict[str, ManifestationNode]:
        return {node.manifestation_id: node for node in self.nodes}


def compile_manifestation_ontology_bundle(
    ontology_document: Mapping[str, Any] | None,
    mapping_document: Mapping[str, Any] | None,
) -> ManifestationOntologyBundle:
    """Compile knowledge WP06B/WP06C documents, or fail closed when absent."""

    if ontology_document is None or mapping_document is None:
        return ManifestationOntologyBundle(
            schema_version="0.1",
            ontology_version="UNAVAILABLE",
            nodes=(),
            mappings=(),
            status="EMPTY_KNOWLEDGE_DEPENDENCY",
        )

    if str(ontology_document.get("schema_version", "")).strip() != "0.1":
        raise ValueError("WP06B ontology schema_version must be 0.1")
    if str(mapping_document.get("schema_version", "")).strip() != "0.1":
        raise ValueError("WP06C mapping schema_version must be 0.1")

    ontology_version = _text(
        ontology_document.get("ontology_version"), "ontology_version"
    )
    mapping_version = _text(
        mapping_document.get("ontology_version"), "mapping.ontology_version"
    )
    if ontology_version != mapping_version:
        raise ValueError("WP06B/WP06C ontology_version mismatch")

    raw_nodes = ontology_document.get("nodes")
    raw_mappings = mapping_document.get("mappings")
    if not isinstance(raw_nodes, Sequence) or isinstance(raw_nodes, (str, bytes)):
        raise ValueError("WP06B nodes must be an array")
    if not isinstance(raw_mappings, Sequence) or isinstance(raw_mappings, (str, bytes)):
        raise ValueError("WP06C mappings must be an array")

    nodes = []
    seen_nodes = set()
    for index, raw in enumerate(raw_nodes):
        if not isinstance(raw, Mapping):
            raise ValueError(f"nodes[{index}] must be an object")
        node_id = _text(raw.get("manifestation_id"), f"nodes[{index}].manifestation_id")
        if node_id in seen_nodes:
            raise ValueError(f"duplicate manifestation_id: {node_id}")
        seen_nodes.add(node_id)
        nodes.append(
            ManifestationNode(
                manifestation_id=node_id,
                parent_id=str(raw.get("parent_id")).strip() if raw.get("parent_id") else None,
                domain=_text(raw.get("domain"), f"nodes[{index}].domain"),
                abstraction_level=_text(
                    raw.get("abstraction_level"), f"nodes[{index}].abstraction_level"
                ),
                source_supported_labels=tuple(
                    sorted(str(x).strip() for x in raw.get("source_supported_labels", []) if str(x).strip())
                ),
                source_rule_ids=tuple(
                    sorted(str(x).strip() for x in raw.get("source_rule_ids", []) if str(x).strip())
                ),
                event_specificity=str(raw.get("event_specificity") or "").strip(),
                ambiguity_notes=str(raw.get("ambiguity_notes") or "").strip(),
                probability_status=_text(
                    raw.get("probability_status", "UNKNOWN"),
                    f"nodes[{index}].probability_status",
                ),
            )
        )

    node_ids = {node.manifestation_id for node in nodes}
    for node in nodes:
        if node.parent_id and node.parent_id not in node_ids:
            raise ValueError(f"unknown parent_id: {node.parent_id}")

    mappings = []
    seen_mappings = set()
    for index, raw in enumerate(raw_mappings):
        if not isinstance(raw, Mapping):
            raise ValueError(f"mappings[{index}] must be an object")
        mapping_id = _text(raw.get("mapping_id"), f"mappings[{index}].mapping_id")
        if mapping_id in seen_mappings:
            raise ValueError(f"duplicate mapping_id: {mapping_id}")
        seen_mappings.add(mapping_id)
        candidates = tuple(
            sorted(str(x).strip() for x in raw.get("candidate_manifestation_ids", []) if str(x).strip())
        )
        unknown = sorted(set(candidates) - node_ids)
        if unknown:
            raise ValueError("mapping references unknown manifestation ids: " + ", ".join(unknown))
        mappings.append(
            ManifestationMapping(
                mapping_id=mapping_id,
                activation_id=_text(raw.get("activation_id"), f"mappings[{index}].activation_id"),
                candidate_manifestation_ids=candidates,
                evidence_tier=_text(raw.get("evidence_tier"), f"mappings[{index}].evidence_tier"),
                source_rule_ids=tuple(sorted(str(x).strip() for x in raw.get("source_rule_ids", []) if str(x).strip())),
                source_trace=tuple(sorted(str(x).strip() for x in raw.get("source_trace", []) if str(x).strip())),
                unresolved_alternatives=tuple(sorted(str(x).strip() for x in raw.get("unresolved_alternatives", []) if str(x).strip())),
            )
        )

    return ManifestationOntologyBundle(
        schema_version="0.1",
        ontology_version=ontology_version,
        nodes=tuple(sorted(nodes, key=lambda x: x.manifestation_id)),
        mappings=tuple(sorted(mappings, key=lambda x: x.mapping_id)),
        status="READY",
    )


def require_manifestation_domain(
    bundle: ManifestationOntologyBundle,
    domain: str,
) -> tuple[ManifestationNode, ...]:
    """Return ontology nodes for a domain; fail closed if knowledge is unavailable."""

    if bundle.status != "READY":
        raise ValueError(
            "manifestation ontology unavailable: waiting for knowledge WP06B/WP06C"
        )
    rows = tuple(node for node in bundle.nodes if node.domain == domain)
    if not rows:
        raise ValueError(f"manifestation ontology has no ready domain: {domain}")
    return rows

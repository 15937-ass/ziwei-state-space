import json
from dataclasses import fields
from pathlib import Path

from src.product.manifestation_adapter_contract_v0_2 import (
    ACTION_BINDING_NAMESPACE,
    MappingAdapterEnvelopeV02,
    NodeAdapterEnvelopeV02,
    compile_mapping_adapter_envelope,
    compile_node_adapter_envelope,
)


ROOT = Path(__file__).resolve().parents[1]
NODE_1 = ROOT / "knowledge/core/wp06b/canonical_manifestations/KMN-000001.json"
NODE_3 = ROOT / "knowledge/core/wp06b/canonical_manifestations/KMN-000003.json"
MAP_1 = ROOT / "knowledge/core/wp06c/canonical_mappings/KMM-000001.json"
MAP_2 = ROOT / "knowledge/core/wp06c/canonical_mappings/KMM-000002.json"
MAP_3 = ROOT / "knowledge/core/wp06c/canonical_mappings/KMM-000003.json"
PROD_ONTOLOGY = ROOT / "product/PL3M_MANIFESTATION_ONTOLOGY_REGISTRY_v0.1.json"
PROD_MAPPING = ROOT / "product/PL3M_MANIFESTATION_MAPPING_REGISTRY_v0.1.json"


def _load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_node_v02_preserves_review_axes_provenance_and_separate_epistemics():
    raw = _load(NODE_3)
    envelope = compile_node_adapter_envelope(raw)

    assert envelope.schema_version == "0.2"
    assert envelope.output_kind.state == raw["output_kind"]["state"]
    assert envelope.output_kind.value == raw["output_kind"]["value"]
    assert envelope.event_specificity.state == raw["event_specificity"]["state"]
    assert envelope.event_specificity.value == raw["event_specificity"]["value"]
    assert envelope.source_epistemic == raw["source_epistemic"]
    assert envelope.normalization_epistemic == raw["normalization_epistemic"]
    assert envelope.review_provenance.review_status == raw["review_provenance"]["review_status"]
    assert envelope.review_provenance.reviewer_id == raw["review_provenance"]["reviewer_id"]
    assert envelope.canonical_identity_status == raw["canonical_identity_status"]
    assert envelope.supersession.supersedes == tuple(raw["supersession"]["supersedes"])
    assert envelope.probability_status == "UNKNOWN"
    assert envelope.runtime_authorized is False

    field_names = {item.name for item in fields(NodeAdapterEnvelopeV02)}
    assert "source_epistemic" in field_names
    assert "normalization_epistemic" in field_names
    assert "evidence_tier" not in field_names


def test_action_prerequisite_binds_only_to_external_action_namespace():
    raw = _load(MAP_2)
    envelope = compile_mapping_adapter_envelope(raw)

    assert raw["conditions"]["real_world_prerequisites"][0]["text"] == "勉强求变"
    assert len(envelope.conditions.action_prerequisites) == 1
    binding = envelope.conditions.action_prerequisites[0]
    assert binding.source_text == "勉强求变"
    assert binding.target_namespace == ACTION_BINDING_NAMESPACE
    assert binding.match_mode == "EXTERNAL_EXPLICIT_ONLY"
    assert binding.chart_inference_allowed is False

    boundary = envelope.execution_boundary
    assert boundary.knowledge_executable is False
    assert boundary.knowledge_product_consumable is False
    assert boundary.runtime_authorized is False


def test_unresolved_source_semantics_are_retained_not_interpreted():
    raw = _load(MAP_1)
    envelope = compile_mapping_adapter_envelope(raw)

    assert envelope.conditions.unresolved_semantics == tuple(
        raw["conditions"]["unresolved_semantics"]
    )
    assert envelope.conditions.unresolved_semantics
    assert envelope.execution_boundary.runtime_authorized is False
    assert envelope.probability_status == "UNKNOWN"


def test_negative_boundaries_and_forbidden_inferences_remain_first_class():
    raw = _load(MAP_3)
    envelope = compile_mapping_adapter_envelope(raw)

    assert envelope.execution_boundary.negative_boundary_review_refs == tuple(
        raw["review_refs"]["negative_boundaries"]
    )
    assert envelope.execution_boundary.forbidden_inferences == tuple(
        raw["forbidden_inferences"]
    )
    joined = " ".join(envelope.execution_boundary.forbidden_inferences)
    for marker in ("injury", "illness", "diagnosis", "treatment"):
        assert marker in joined

    field_names = {item.name for item in fields(MappingAdapterEnvelopeV02)}
    assert "source_epistemic" in field_names
    assert "normalization_epistemic" in field_names
    assert "evidence_tier" not in field_names


def test_v02_serialization_is_deterministic_and_does_not_promote_production():
    node_raw = _load(NODE_1)
    mapping_raw = _load(MAP_2)

    node_a = compile_node_adapter_envelope(node_raw).to_dict()
    node_b = compile_node_adapter_envelope(node_raw).to_dict()
    mapping_a = compile_mapping_adapter_envelope(mapping_raw).to_dict()
    mapping_b = compile_mapping_adapter_envelope(mapping_raw).to_dict()

    assert node_a == node_b
    assert mapping_a == mapping_b

    ontology = _load(PROD_ONTOLOGY)
    mappings = _load(PROD_MAPPING)
    assert ontology["registry_status"] == "EMPTY_PENDING_KB_WP06B"
    assert ontology["nodes"] == []
    assert mappings["registry_status"] == "EMPTY_PENDING_KB_WP06C"
    assert mappings["mappings"] == []

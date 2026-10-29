import json
from dataclasses import fields
from pathlib import Path

from src.product.manifestation_context import ManifestationRoutingContext
from src.product.manifestation_crosswalk import (
    CROSSWALK_DISPOSITIONS,
    classify_mapping_crosswalk,
    classify_node_crosswalk,
    missing_crosswalk_fields,
    runtime_consumption_allowed,
)
from src.product.manifestation_router import ManifestationMapping


ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / "product/PL3M_MANIFESTATION_CROSSWALK_PILOT_V0_1.json"
NODE_PATHS = [
    ROOT / "knowledge/core/wp06b/canonical_manifestations/KMN-000001.json",
    ROOT / "knowledge/core/wp06b/canonical_manifestations/KMN-000002.json",
    ROOT / "knowledge/core/wp06b/canonical_manifestations/KMN-000003.json",
]
MAPPING_PATHS = [
    ROOT / "knowledge/core/wp06c/canonical_mappings/KMM-000001.json",
    ROOT / "knowledge/core/wp06c/canonical_mappings/KMM-000002.json",
    ROOT / "knowledge/core/wp06c/canonical_mappings/KMM-000003.json",
]
PROD_ONTOLOGY = ROOT / "product/PL3M_MANIFESTATION_ONTOLOGY_REGISTRY_v0.1.json"
PROD_MAPPING = ROOT / "product/PL3M_MANIFESTATION_MAPPING_REGISTRY_v0.1.json"


def _load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def _pilot():
    return _load(PILOT)


def test_pilot_pins_exact_first_checkpoint_and_keeps_production_closed():
    pilot = _pilot()
    assert pilot["pinned_main_commit"] == (
        "df66959b126e44eb309507fc5400b82e3af58187"
    )
    assert len(pilot["frozen_knowledge_inputs"]) == 8
    assert pilot["adapter_feasibility"]["production_registry_population_allowed"] is False
    assert pilot["adapter_feasibility"]["active_kib_promotion_allowed"] is False
    assert pilot["adapter_feasibility"]["runtime_execution_allowed"] is False

    ontology = _load(PROD_ONTOLOGY)
    mapping = _load(PROD_MAPPING)
    assert ontology["registry_status"] == "EMPTY_PENDING_KB_WP06B"
    assert ontology["nodes"] == []
    assert mapping["registry_status"] == "EMPTY_PENDING_KB_WP06C"
    assert mapping["mappings"] == []


def test_every_observed_canonical_field_has_an_explicit_crosswalk_disposition():
    pilot = _pilot()
    node_paths = {
        row["field"] for row in pilot["field_crosswalk"]["canonical_node"]
    }
    mapping_paths = {
        row["field"] for row in pilot["field_crosswalk"]["canonical_mapping"]
    }

    assert missing_crosswalk_fields([_load(p) for p in NODE_PATHS], node_paths) == ()
    assert (
        missing_crosswalk_fields([_load(p) for p in MAPPING_PATHS], mapping_paths)
        == ()
    )

    for section in ("canonical_node", "canonical_mapping"):
        for row in pilot["field_crosswalk"][section]:
            assert row["disposition"] in CROSSWALK_DISPOSITIONS


def test_mandatory_entity_verdicts_are_deterministic():
    nodes = {item["manifestation_id"]: item for item in map(_load, NODE_PATHS)}
    mappings = {item["mapping_id"]: item for item in map(_load, MAPPING_PATHS)}

    assert classify_node_crosswalk(nodes["KMN-000001"]).crosswalk_disposition == "GAP_PRODUCT"
    assert classify_node_crosswalk(nodes["KMN-000002"]).crosswalk_disposition == "GAP_PRODUCT"
    assert classify_node_crosswalk(nodes["KMN-000003"]).crosswalk_disposition == "LOSSY"

    assert classify_mapping_crosswalk(mappings["KMM-000001"]).crosswalk_disposition == "HOLD"
    assert classify_mapping_crosswalk(mappings["KMM-000002"]).crosswalk_disposition == "GAP_PRODUCT"
    assert classify_mapping_crosswalk(mappings["KMM-000003"]).crosswalk_disposition == "LOSSY"

    assert all(not runtime_consumption_allowed(item) for item in mappings.values())


def test_kmm000001_fire_bell_ambiguity_stays_hold():
    mapping = _load(MAPPING_PATHS[0])
    unresolved = mapping["conditions"]["unresolved_semantics"]
    assert unresolved
    assert "BOTH_STARS" in unresolved[0]
    assert "EITHER_STAR" in unresolved[0]
    verdict = classify_mapping_crosswalk(mapping)
    assert verdict.crosswalk_disposition == "HOLD"
    assert verdict.runtime_consumption_allowed is False


def test_kmm000002_is_product_binding_gap_not_missing_reality_container():
    mapping = _load(MAPPING_PATHS[1])
    assert mapping["conditions"]["real_world_prerequisites"][0]["text"] == "勉强求变"

    context_fields = {item.name for item in fields(ManifestationRoutingContext)}
    mapping_fields = {item.name for item in fields(ManifestationMapping)}
    assert "actions" in context_fields
    assert "required_actions" not in mapping_fields
    assert "action_predicates" not in mapping_fields

    verdict = classify_mapping_crosswalk(mapping)
    assert verdict.crosswalk_disposition == "GAP_PRODUCT"
    assert "A_t/actions" in verdict.reason


def test_kmm000003_scene_crosswalk_preserves_negative_boundary_as_loss():
    mapping = _load(MAPPING_PATHS[2])
    assert mapping["output_kind"]["value"] == "SCENE_OR_CONTEXT"
    assert mapping["event_specificity"]["value"] == "SCENE_NOT_OBSERVED_EVENT"
    joined = " ".join(mapping["forbidden_inferences"])
    for marker in ("injury", "illness", "diagnosis", "treatment"):
        assert marker in joined

    verdict = classify_mapping_crosswalk(mapping)
    assert verdict.crosswalk_disposition == "LOSSY"
    assert verdict.runtime_consumption_allowed is False


def test_probability_and_predictive_claims_remain_outside_pilot():
    pilot = _pilot()
    assert pilot["adapter_feasibility"]["probability_claim_allowed"] is False
    assert pilot["adapter_feasibility"]["predictive_validity_claim_allowed"] is False
    for path in NODE_PATHS + MAPPING_PATHS:
        assert _load(path)["probability_status"] == "UNKNOWN"

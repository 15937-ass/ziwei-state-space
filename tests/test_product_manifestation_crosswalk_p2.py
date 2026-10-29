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
P1 = ROOT / "product/PL3M_MANIFESTATION_CROSSWALK_PILOT_V0_1.json"
P2 = ROOT / "product/PL3M_MANIFESTATION_CROSSWALK_EXPANDED_P2.json"
NODE_PATHS = [
    ROOT / f"knowledge/core/wp06b/canonical_manifestations/KMN-{i:06d}.json"
    for i in range(1, 10)
]
MAPPING_PATHS = [
    ROOT / f"knowledge/core/wp06c/canonical_mappings/KMM-{i:06d}.json"
    for i in range(1, 10)
]
PROD_ONTOLOGY = ROOT / "product/PL3M_MANIFESTATION_ONTOLOGY_REGISTRY_v0.1.json"
PROD_MAPPING = ROOT / "product/PL3M_MANIFESTATION_MAPPING_REGISTRY_v0.1.json"


def _load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_p2_pins_accepted_expanded_checkpoint_and_keeps_production_closed():
    p2 = _load(P2)
    assert p2["pinned_main_commit"] == "4e41074d351a720a639cb702d2ce100c44aa5ca1"
    assert p2["accepted_checkpoint"]["node_count"] == 9
    assert p2["accepted_checkpoint"]["mapping_count"] == 9
    assert len(p2["frozen_knowledge_inputs"]) == 20

    assert p2["adapter_feasibility"]["production_registry_population_allowed"] is False
    assert p2["adapter_feasibility"]["active_kib_promotion_allowed"] is False
    assert p2["adapter_feasibility"]["runtime_execution_allowed"] is False

    ontology = _load(PROD_ONTOLOGY)
    mapping = _load(PROD_MAPPING)
    assert ontology["registry_status"] == "EMPTY_PENDING_KB_WP06B"
    assert ontology["nodes"] == []
    assert mapping["registry_status"] == "EMPTY_PENDING_KB_WP06C"
    assert mapping["mappings"] == []


def test_p1_field_matrix_covers_every_expanded_checkpoint_field():
    p1 = _load(P1)
    node_paths = {row["field"] for row in p1["field_crosswalk"]["canonical_node"]}
    mapping_paths = {row["field"] for row in p1["field_crosswalk"]["canonical_mapping"]}

    assert missing_crosswalk_fields([_load(p) for p in NODE_PATHS], node_paths) == ()
    assert missing_crosswalk_fields([_load(p) for p in MAPPING_PATHS], mapping_paths) == ()

    p2 = _load(P2)
    assert p2["field_coverage"]["result"] == "PASS_NO_NEW_FIELD_PATHS"
    assert p2["field_coverage"]["node_missing_dispositions"] == []
    assert p2["field_coverage"]["mapping_missing_dispositions"] == []


def test_all_expanded_entity_verdicts_are_explicit_and_fail_closed():
    p2 = _load(P2)
    verdicts = {row["item_id"]: row for row in p2["entity_verdicts"]}
    assert len(verdicts) == 18
    for row in verdicts.values():
        assert row["disposition"] in CROSSWALK_DISPOSITIONS
        assert row["runtime_consumption_allowed"] is False

    nodes = {item["manifestation_id"]: item for item in map(_load, NODE_PATHS)}
    mappings = {item["mapping_id"]: item for item in map(_load, MAPPING_PATHS)}

    for item_id in nodes:
        assert classify_node_crosswalk(nodes[item_id]).crosswalk_disposition == verdicts[item_id]["disposition"]
    for item_id in mappings:
        assert classify_mapping_crosswalk(mappings[item_id]).crosswalk_disposition == verdicts[item_id]["disposition"]
        assert runtime_consumption_allowed(mappings[item_id]) is False


def test_unresolved_trigger_semantics_stay_hold():
    mappings = {item["mapping_id"]: item for item in map(_load, MAPPING_PATHS)}
    assert classify_mapping_crosswalk(mappings["KMM-000001"]).crosswalk_disposition == "HOLD"
    assert classify_mapping_crosswalk(mappings["KMM-000004"]).crosswalk_disposition == "HOLD"
    assert mappings["KMM-000004"]["conditions"]["unresolved_semantics"]
    assert mappings["KMM-000004"]["execution_readiness"] == "BLOCKED_SEMANTIC"


def test_expanded_checkpoint_exposes_structured_condition_gap_pg006():
    p2 = _load(P2)
    gaps = {row["gap_id"]: row for row in p2["new_gap_register"]}
    assert "PG-006" in gaps

    mapping_fields = {item.name for item in fields(ManifestationMapping)}
    for absent in ("condition_operator", "condition_groups", "cross_palace_dependencies"):
        assert absent not in mapping_fields

    kmm7 = _load(MAPPING_PATHS[6])
    kmm8 = _load(MAPPING_PATHS[7])
    assert "对宫" in kmm7["conditions"]["source_condition_text"]
    assert "opposite-palace" in " ".join(kmm7["forbidden_inferences"])
    assert "或" in kmm8["conditions"]["source_condition_text"]
    assert "AND" in " ".join(kmm8["forbidden_inferences"])


def test_expanded_checkpoint_exposes_temporal_layer_gap_pg007():
    p2 = _load(P2)
    gaps = {row["gap_id"]: row for row in p2["new_gap_register"]}
    assert "PG-007" in gaps

    kmm9 = _load(MAPPING_PATHS[8])
    assert kmm9["conditions"]["time_layer"] == "DECADE_YEAR"

    mapping_fields = {item.name for item in fields(ManifestationMapping)}
    context_fields = {item.name for item in fields(ManifestationRoutingContext)}
    assert "time_layer" not in mapping_fields
    assert "active_natal_rule_ids" in context_fields
    assert "active_temporal_rule_ids" in context_fields


def test_p1_gaps_remain_confirmed_and_no_probability_claim_is_added():
    p2 = _load(P2)
    stability = {row["gap_id"]: row["status"] for row in p2["p1_gap_stability"]}
    assert set(stability) == {"PG-001", "PG-002", "PG-003", "PG-004", "PG-005"}
    assert all(status.startswith("CONFIRMED") for status in stability.values())

    assert p2["adapter_feasibility"]["probability_claim_allowed"] is False
    assert p2["adapter_feasibility"]["predictive_validity_claim_allowed"] is False
    assert p2["adapter_feasibility"]["formal_crosswalk_freeze_ready"] is False
    for path in NODE_PATHS + MAPPING_PATHS:
        assert _load(path)["probability_status"] == "UNKNOWN"

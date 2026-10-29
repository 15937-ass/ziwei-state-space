"""Core #907 canonical mapping semantic-diversity batch 2."""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NODE_INDEX = ROOT / "knowledge/core/wp06b/CANONICAL_MANIFESTATION_NODE_INDEX_v0.1.json"
MAP_INDEX = ROOT / "knowledge/core/wp06c/CANONICAL_MANIFESTATION_MAPPING_INDEX_v0.1.json"
REVIEW = ROOT / "knowledge/core/wp06c/CANONICAL_MAPPING_DIVERSITY_BATCH_02_REVIEW_v0.1.json"
NODE_DIR = ROOT / "knowledge/core/wp06b/canonical_manifestations"
MAP_DIR = ROOT / "knowledge/core/wp06c/canonical_mappings"
P01 = ROOT / "knowledge/palaces/P01_life/wp05/LIFE_P06_SOURCE_GAP_SUPPLEMENT_PP17_20_v0.1.csv"
P02 = ROOT / "knowledge/palaces/P02_siblings/wp05/SIBLINGS_SB04_WUQU_SOURCE_AUDIT_v0.1.json"
PRODUCT_ONTOLOGY = ROOT / "product/PL3M_MANIFESTATION_ONTOLOGY_REGISTRY_v0.1.json"
PRODUCT_MAPPING = ROOT / "product/PL3M_MANIFESTATION_MAPPING_REGISTRY_v0.1.json"

EXPECTED = {
    "P01-SG-169": ("KMN-000010", "KMM-000010"),
    "P01-SG-175": ("KMN-000011", "KMM-000011"),
    "P01-SG-180": ("KMN-000012", "KMM-000012"),
    "P01-SG-190": ("KMN-000013", "KMM-000013"),
    "P02S-137": ("KMN-000014", "KMM-000014"),
    "P02S-169": ("KMN-000015", "KMM-000015"),
}


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return {r["projection_rule_id"]: r for r in csv.DictReader(f)}


def source_rows():
    rows = read_csv(P01)
    p02 = load(P02)
    for r in p02.get("records", p02.get("projection_rules", p02.get("items", []))):
        rows[r["projection_rule_id"]] = r
    return rows


def test_selected_sources_are_reusable_source_first_non_case():
    rows = source_rows()
    for rule in EXPECTED:
        r = rows[rule]
        case = r["case_support_only"]
        promoted = r["canonical_promotion"]
        assert (case is False) if isinstance(case, bool) else (case.lower() == "false")
        assert r["source_epistemic"] == "EXPLICIT"
        assert r["normalization_epistemic"] == "SOURCE_PRESERVING"
        assert (promoted is True) if isinstance(promoted, bool) else (promoted.lower() == "true")


def test_batch2_advances_canonical_checkpoint_to_fifteen():
    ni, mi = load(NODE_INDEX), load(MAP_INDEX)
    assert ni["coverage"]["production_node_count"] == 15
    assert ni["coverage"]["next_allocatable_id"] == "KMN-000016"
    assert mi["coverage"]["canonical_mapping_count"] == 15
    assert mi["coverage"]["next_allocatable_id"] == "KMM-000016"
    for rule, (nid, mid) in EXPECTED.items():
        n = load(NODE_DIR / f"{nid}.json")
        m = load(MAP_DIR / f"{mid}.json")
        assert n["source_rule_ids"] == [rule]
        assert m["primary_source_rule_id"] == rule
        assert m["manifestation_id"] == nid
        assert n["canonical_identity_status"] == "ACTIVE"
        assert m["canonical_mapping_approved"] is True
        assert m["executable"] is False
        assert m["product_consumable"] is False
        assert m["probability_status"] == "UNKNOWN"


def test_batch2_review_has_six_positive_and_six_negative_boundaries():
    d = load(REVIEW)
    assert set(d["semantic_diversity"]) == {
        "specific_decade_trigger",
        "explicit_unresolved_temporal_scope",
        "multi_variant_process_pattern",
        "conditional_scene_translation",
        "cross_palace_relationship_exception",
        "relational_durability_counterexample",
    }
    reviews = {r["review_record_id"]: r for r in d["mapping_review_records"]}
    assert len(reviews) == 12
    assert sum(r["mapping_disposition"]["value"] == "supported_candidate" for r in reviews.values()) == 6
    assert sum(r["mapping_disposition"]["value"] == "not_supported_for_target" for r in reviews.values()) == 6
    assert d["c1_milestone_assessment"]["after_batch_mapping_count"] == 15
    assert d["c1_milestone_assessment"]["threshold_reached"] is True
    assert d["c1_milestone_assessment"]["next_stage"] == "C3_SCHEMA_STABILITY_REVIEW"


def test_temporal_and_branch_boundaries_survive():
    decade = load(MAP_DIR / "KMM-000010.json")
    assert decade["conditions"]["time_layer"] == "DECADE"
    assert any("specific age" in x for x in decade["forbidden_inferences"])

    unresolved = load(MAP_DIR / "KMM-000011.json")
    assert unresolved["conditions"]["time_layer"] == "SOURCE_TEMPORAL_LAYER_UNSPECIFIED"
    assert unresolved["execution_readiness"] == "BLOCKED_SEMANTIC"
    assert unresolved["execution_blockers"] == ["UNRESOLVED_TEMPORAL_LAYER_FOR_PALACE_CONTEXT_PREFERENCE"]

    process = load(MAP_DIR / "KMM-000012.json")
    assert "羊陀夹" in process["conditions"]["source_condition_text"]
    assert any("occur together" in x for x in process["forbidden_inferences"])

    scene = load(MAP_DIR / "KMM-000013.json")
    assert "见奏书亦吉" in scene["conditions"]["source_condition_text"]
    assert "若同时" in scene["conditions"]["modality_terms"]
    assert any("merge" in x for x in scene["forbidden_inferences"])

    relation = load(MAP_DIR / "KMM-000014.json")
    assert "命宫见辅弼" in relation["conditions"]["source_condition_text"]
    assert "除非" in relation["conditions"]["modality_terms"]
    assert any("conflate" in x for x in relation["forbidden_inferences"])

    durability = load(MAP_DIR / "KMM-000015.json")
    assert "即使见吉曜" in durability["conditions"]["source_condition_text"]
    assert "即使" in durability["conditions"]["modality_terms"]
    assert any("numeric duration" in x for x in durability["forbidden_inferences"])


def test_product_and_probability_remain_fail_closed_at_c1_threshold():
    o, m = load(PRODUCT_ONTOLOGY), load(PRODUCT_MAPPING)
    assert o["nodes"] == []
    assert m["mappings"] == []
    assert load(NODE_INDEX)["invariants"]["universal_root_or_family_created"] is False
    assert load(MAP_INDEX)["invariants"]["executable_mappings"] == 0
    assert load(MAP_INDEX)["invariants"]["product_consumption_authorized"] is False
    assert load(MAP_INDEX)["invariants"]["probability_status"] == "UNKNOWN"

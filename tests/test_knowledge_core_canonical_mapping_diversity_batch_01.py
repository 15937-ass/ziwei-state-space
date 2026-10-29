"""Core #898 canonical mapping semantic-diversity batch 1."""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NODE_INDEX = ROOT / "knowledge/core/wp06b/CANONICAL_MANIFESTATION_NODE_INDEX_v0.1.json"
MAP_INDEX = ROOT / "knowledge/core/wp06c/CANONICAL_MANIFESTATION_MAPPING_INDEX_v0.1.json"
REVIEW = ROOT / "knowledge/core/wp06c/CANONICAL_MAPPING_DIVERSITY_BATCH_01_REVIEW_v0.1.json"
NODE_DIR = ROOT / "knowledge/core/wp06b/canonical_manifestations"
MAP_DIR = ROOT / "knowledge/core/wp06c/canonical_mappings"
P05 = ROOT / "knowledge/palaces/P05_wealth/w05/WEALTH_W05_SOURCE_GAP_SUPPLEMENT_v0.1.csv"
P01G = ROOT / "knowledge/palaces/P01_life/wp05/LIFE_P07_SOURCE_GAP_SUPPLEMENT_PP20_22_v0.1.csv"
P01R = ROOT / "knowledge/palaces/P01_life/wp05/LIFE_P08_SOURCE_READJUDICATION_701_800_v0.1.csv"
PRODUCT_ONTOLOGY = ROOT / "product/PL3M_MANIFESTATION_ONTOLOGY_REGISTRY_v0.1.json"
PRODUCT_MAPPING = ROOT / "product/PL3M_MANIFESTATION_MAPPING_REGISTRY_v0.1.json"

EXPECTED = {
    "P05-SG-002": ("KMN-000004", "KMM-000004"),
    "P05-SG-003": ("KMN-000005", "KMM-000005"),
    "P01-SG-213": ("KMN-000006", "KMM-000006"),
    "P01-745": ("KMN-000007", "KMM-000007"),
    "P01-727": ("KMN-000008", "KMM-000008"),
    "P01-750": ("KMN-000009", "KMM-000009"),
}


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return {r["projection_rule_id"]: r for r in csv.DictReader(f)}


def test_selected_sources_are_already_source_first_and_non_case():
    rows = {}
    rows.update(read_csv(P05))
    rows.update(read_csv(P01G))
    rows.update(read_csv(P01R))
    for rule in EXPECTED:
        r = rows[rule]
        assert r["case_support_only"].lower() == "false"
        assert r["source_epistemic"] == "EXPLICIT"
        assert r["canonical_promotion"].lower() == "true"


def test_batch1_historical_six_pairs_remain_accepted_after_later_expansion():
    ni, mi = load(NODE_INDEX), load(MAP_INDEX)
    assert ni["coverage"]["production_node_count"] >= 9
    assert mi["coverage"]["canonical_mapping_count"] >= 9
    assert int(ni["coverage"]["next_allocatable_id"].split("-")[1]) == ni["coverage"]["production_node_count"] + 1
    assert int(mi["coverage"]["next_allocatable_id"].split("-")[1]) == mi["coverage"]["canonical_mapping_count"] + 1
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


def test_semantic_diversity_and_review_boundaries_are_explicit():
    d = load(REVIEW)
    assert set(d["semantic_diversity"]) == {
        "state", "explicit_unresolved_semantics", "modifier_interaction",
        "cross_palace_dependency", "multiple_alternative_antecedents",
        "temporal_dynamic_condition",
    }
    reviews = {r["review_record_id"]: r for r in d["mapping_review_records"]}
    assert len(reviews) == 12
    assert sum(r["mapping_disposition"]["value"] == "supported_candidate" for r in reviews.values()) == 6
    assert sum(r["mapping_disposition"]["value"] == "not_supported_for_target" for r in reviews.values()) == 6
    for c in d["cohort"]:
        assert reviews[c["positive_target_review_id"]]["mapping_disposition"]["value"] == "supported_candidate"
        assert reviews[c["negative_target_review_id"]]["mapping_disposition"]["value"] == "not_supported_for_target"


def test_unresolved_trigger_and_other_boundaries_survive():
    risk = load(MAP_DIR / "KMM-000004.json")
    assert risk["execution_readiness"] == "BLOCKED_SEMANTIC"
    assert risk["execution_blockers"] == ["UNRESOLVED_SHA_YAO_KONG_JIE_TRIGGER_QUANTIFIER"]
    unresolved = " ".join(risk["conditions"]["unresolved_semantics"])
    assert "AND" in unresolved and "OR" in unresolved

    modifier = load(MAP_DIR / "KMM-000006.json")
    assert "往往" in modifier["conditions"]["modality_terms"]
    assert any("numeric weight" in x for x in modifier["forbidden_inferences"])

    cross = load(MAP_DIR / "KMM-000007.json")
    assert "对宫" in cross["conditions"]["source_condition_text"]
    assert any("opposite-palace" in x for x in cross["forbidden_inferences"])

    alternative = load(MAP_DIR / "KMM-000008.json")
    assert "或" in alternative["conditions"]["source_condition_text"]
    assert "唯若" in alternative["conditions"]["modality_terms"]
    assert any("AND requirement" in x for x in alternative["forbidden_inferences"])

    temporal = load(MAP_DIR / "KMM-000009.json")
    assert temporal["conditions"]["time_layer"] == "DECADE_YEAR"
    assert temporal["output_kind"]["value"] == "TEMPORAL_HINGE_STRUCTURE"
    assert any("specific event" in x for x in temporal["forbidden_inferences"])


def test_product_and_probability_remain_fail_closed():
    o, m = load(PRODUCT_ONTOLOGY), load(PRODUCT_MAPPING)
    assert o["nodes"] == []
    assert m["mappings"] == []
    assert load(NODE_INDEX)["invariants"]["universal_root_or_family_created"] is False
    assert load(MAP_INDEX)["invariants"]["executable_mappings"] == 0
    assert load(MAP_INDEX)["invariants"]["product_consumption_authorized"] is False
    assert load(MAP_INDEX)["invariants"]["probability_status"] == "UNKNOWN"

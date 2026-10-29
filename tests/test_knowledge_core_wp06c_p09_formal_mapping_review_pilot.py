"""Integrity tests for Core #864 P09 formal mapping-review pilot."""

import json
from pathlib import Path

from tools.knowledge_core_mapping_review_schema import validate_mapping_review_collection


ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / "knowledge/core/wp06c/P09_FORMAL_MAPPING_REVIEW_PILOT_v0.1.json"
ONTOLOGY = ROOT / "product/PL3M_MANIFESTATION_ONTOLOGY_REGISTRY_v0.1.json"
MAPPING = ROOT / "product/PL3M_MANIFESTATION_MAPPING_REGISTRY_v0.1.json"


def data():
    return json.loads(PILOT.read_text(encoding="utf-8"))


def test_pilot_is_formal_review_but_not_canonical_or_product_ready():
    d = data()
    assert d["status"] == "FORMAL_MAPPING_REVIEW_COMPLETED_NOT_CANONICAL"
    assert d["architecture"]["option"] == "OPTION_C"
    assert d["architecture"]["pi_decisions_ref"] == "PI-DECISION-CORE-841-2026-10-29"
    inv = d["invariants"]
    assert inv["candidate_review_only"] is True
    assert inv["canonical_ontology_ids_assigned"] is False
    assert inv["canonical_mappings_accepted"] is False
    assert inv["production_schema_changed"] is False
    assert inv["product_registry_modified"] is False
    assert inv["product_consumption_authorized"] is False
    assert inv["executable"] is False
    assert inv["probability_status"] == "UNKNOWN"
    assert inv["empirical_predictive_validity_claimed"] is False


def test_all_mapping_review_records_validate_and_are_unique():
    d = data()
    records = d["mapping_review_records"]
    assert len(records) == 6
    assert validate_mapping_review_collection(records) == []
    ids = [r["review_record_id"] for r in records]
    targets = [r["target_ref"] for r in records]
    assert len(ids) == len(set(ids))
    assert len(targets) == len(set(targets))


def test_three_positive_and_three_negative_target_reviews():
    d = data()
    values = [r["mapping_disposition"]["value"] for r in d["mapping_review_records"]]
    assert values.count("supported_candidate") == 3
    assert values.count("not_supported_for_target") == 3
    assert d["pilot_findings"]["positive_supported_candidate_reviews"] == 3
    assert d["pilot_findings"]["negative_not_supported_target_reviews"] == 3


def test_ca01035_is_process_not_single_event_and_keeps_modality_and_ambiguity():
    d = data()
    c = next(x for x in d["candidates"] if x["source_rule_id"] == "CA01-035")
    assert c["output_kind"] == {"state": "KNOWN", "value": "PROCESS_PATTERN"}
    assert c["event_specificity"] == {"state": "KNOWN", "value": "PROCESS_SEQUENCE_NOT_SINGLE_EVENT"}
    assert "往往" in c["conditions"]["preserve_modality"]
    assert any("BOTH_STARS" in x and "EITHER_STAR" in x for x in c["conditions"]["unresolved"])
    neg = next(r for r in d["mapping_review_records"] if r["review_record_id"] == c["negative_target_review_id"])
    assert neg["mapping_disposition"]["value"] == "not_supported_for_target"
    assert "single_observed_career_event" in neg["target_ref"]


def test_ca01045_keeps_real_world_action_and_antecedents():
    d = data()
    c = next(x for x in d["candidates"] if x["source_rule_id"] == "CA01-045")
    assert c["output_kind"]["value"] == "ACTION_CONDITIONED_OUTCOME"
    assert c["event_specificity"]["value"] == "CONDITIONAL_OUTCOME_NOT_OBSERVED"
    assert c["conditions"]["antecedent_rule_ids"] == ["CA01-042", "CA01-044"]
    assert c["conditions"]["real_world_prerequisite"] == "勉强求变"
    assert c["conditions"]["real_world_prerequisite_status"] == "EXPLICIT_IN_SOURCE_NOT_ESTABLISHED_BY_CHART_FACTS"
    pos = next(r for r in d["mapping_review_records"] if r["review_record_id"] == c["positive_target_review_id"])
    neg = next(r for r in d["mapping_review_records"] if r["review_record_id"] == c["negative_target_review_id"])
    assert pos["mapping_disposition"]["value"] == "supported_candidate"
    assert neg["mapping_disposition"]["value"] == "not_supported_for_target"
    assert "unconditional_chart_only" in neg["target_ref"]


def test_ca05469_scene_positive_and_personal_injury_negative():
    d = data()
    c = next(x for x in d["candidates"] if x["source_rule_id"] == "CA05-469")
    assert c["source_epistemic"] == "EXPLICIT"
    assert c["normalization_epistemic"] == "INFERRED"
    assert c["output_kind"]["value"] == "SCENE_OR_CONTEXT"
    assert c["event_specificity"]["value"] == "SCENE_NOT_OBSERVED_EVENT"
    pos = next(r for r in d["mapping_review_records"] if r["review_record_id"] == c["positive_target_review_id"])
    neg = next(r for r in d["mapping_review_records"] if r["review_record_id"] == c["negative_target_review_id"])
    assert pos["mapping_disposition"]["value"] == "supported_candidate"
    assert "industry_scene" in pos["target_ref"]
    assert neg["evidence_role"]["state"] == "NOT_APPLICABLE"
    assert neg["evidence_role"]["value"] is None
    assert neg["mapping_disposition"]["value"] == "not_supported_for_target"
    assert "personal_injury_or_illness_event" in neg["target_ref"]


def test_no_candidate_gets_canonical_id_execution_or_probability():
    d = data()
    for c in d["candidates"]:
        assert c["canonical_ontology_id"] is None
        assert c["canonical_mapping_approved"] is False
        assert c["executable"] is False
        assert c["product_consumable"] is False
        assert c["probability_status"] == "UNKNOWN"


def test_pilot_finds_no_new_schema_gap_but_next_promotion_requires_human_gate():
    d = data()
    f = d["pilot_findings"]
    assert f["schema_gap_found"] is False
    assert f["new_shared_semantic_primitive_required"] is False
    assert f["new_global_metadata_axis_required"] is False
    assert f["canonical_node_ids_required_to_promote_beyond_candidate_review"] is True
    assert f["production_mapping_registry_ready"] is False
    assert f["product_consumer_ready"] is False
    assert d["next_gate"]["status"] == "HUMAN_GATE_REQUIRED_BEFORE_CANONICAL_NODE_OR_MAPPING_PROMOTION"


def test_product_registries_remain_empty_fail_closed():
    ontology = json.loads(ONTOLOGY.read_text(encoding="utf-8"))
    mapping = json.loads(MAPPING.read_text(encoding="utf-8"))
    assert ontology["registry_status"] == "EMPTY_PENDING_KB_WP06B"
    assert ontology["nodes"] == []
    assert mapping["registry_status"] == "EMPTY_PENDING_KB_WP06C"
    assert mapping["mappings"] == []

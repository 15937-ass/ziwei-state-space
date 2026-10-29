"""Decision-packet integrity tests for Core #866."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "knowledge/core/wp06b/CANONICAL_MANIFESTATION_GOVERNANCE_PI_PACKET_v0.1.json"
ONTOLOGY_REGISTRY = ROOT / "product/PL3M_MANIFESTATION_ONTOLOGY_REGISTRY_v0.1.json"
MAPPING_REGISTRY = ROOT / "product/PL3M_MANIFESTATION_MAPPING_REGISTRY_v0.1.json"


def packet():
    return json.loads(PACKET.read_text(encoding="utf-8"))


def test_packet_is_proposal_only_and_requires_pi():
    d = packet()
    assert d["status"] == "PI_DECISIONS_RECORDED_CANONICALIZATION_POLICY_NOT_IMPLEMENTED"
    assert d["recommended_pi_response"] == "APPROVED_G1A_G2A_G3A"
    rec = d["pi_decision_record"]
    assert rec["record_status"] == "PI_DECISIONS_RECORDED"
    assert rec["accepted_options"] == {"G1": "A", "G2": "A", "G3": "A"}
    assert rec["authorizes"]["define_knowledge_owned_canonical_node_artifact_and_stable_id_policy"] is True
    assert rec["authorizes"]["ordinary_child_node_canonical_identity_under_frozen_gates"] is True
    assert not any(rec["does_not_authorize"].values())
    guards = d["non_decision_guardrails"]
    assert guards["canonical_mapping_promotion_authorized"] is False
    assert guards["canonical_node_ids_assigned_in_this_packet"] is False
    assert guards["universal_root_created"] is False
    assert guards["production_schema_changed"] is False
    assert guards["product_files_modified"] is False
    assert guards["product_consumption_authorized"] is False
    assert guards["probability_status"] == "UNKNOWN"
    assert guards["empirical_predictive_validity_claimed"] is False


def test_g1_recommendation_avoids_per_node_pi_but_keeps_universal_gate():
    d = packet()
    g1 = d["decisions"]["G1"]
    assert g1["recommendation"] == "A"
    assert g1["options"]["A"]["code"] == "POLICY_GATED_ORDINARY_CHILD_CANONICALIZATION"
    assert g1["options"]["A"]["exact_id_lexical_format_pi_decision_required"] is False
    assert any("universal manifestation family/root/shared primitive" in x for x in g1["options"]["A"]["gates"])
    after = d["after_recommended_approval"]
    assert after["per_node_pi_review_for_ordinary_children"] is False
    assert after["universal_family_human_gate_remains"] is True


def test_g2_recommendation_preserves_inference_epistemic_and_excludes_case_hypothesis():
    d = packet()
    g2 = d["decisions"]["G2"]
    assert g2["recommendation"] == "A"
    a = g2["options"]["A"]
    assert a["code"] == "ALLOW_TRACEABLE_INFERENCE_WITH_EPISTEMIC_PRESERVATION"
    assert "CASE_SUPPORT_ONLY_AS_SOLE_SUPPORT" in a["disallowed"]
    assert "HYPOTHESIS_AS_SOLE_SUPPORT" in a["disallowed"]
    assert "SILENT_INFERENCE" in a["disallowed"]
    assert "CA05-469" in a["implications"]
    assert "CA01-045" in a["implications"]


def test_g3_recommendation_keeps_knowledge_authoritative_and_product_fail_closed():
    d = packet()
    g3 = d["decisions"]["G3"]
    assert g3["recommendation"] == "A"
    assert g3["options"]["A"]["code"] == "KNOWLEDGE_SOURCE_NATIVE_AUTHORITY_PRODUCT_ADAPTER_LATER"
    assert g3["options"]["A"]["product_registry_change_now"] is False
    assert g3["options"]["B"]["recommendation_status"] == "REJECT"
    assert g3["options"]["C"]["recommendation_status"] == "REJECT"


def test_observed_compatibility_gap_is_explicit():
    d = packet()
    f = d["observed_facts"]
    assert f["knowledge_is_ontology_owner"] is True
    assert f["product_is_adapter_consumer"] is True
    assert f["product_node_has_output_kind"] is False
    assert f["product_event_specificity_values"] == ["ABSTRACT", "SCENE_LEVEL", "CONCRETE_EVENT"]
    assert set(f["knowledge_fine_event_specificity_examples"]) == {
        "PROCESS_SEQUENCE_NOT_SINGLE_EVENT",
        "CONDITIONAL_OUTCOME_NOT_OBSERVED",
        "SCENE_NOT_OBSERVED_EVENT",
    }
    assert f["ca01045_prerequisite_representable_by_current_product_router"] is False
    assert f["test_fixture_ids_are_not_production_convention"] is True


def test_ca01045_runtime_stays_held_regardless_of_recommendation():
    d = packet()
    assert d["non_decision_guardrails"]["ca01045_runtime"] == (
        "HELD_UNTIL_REAL_WORLD_ACTION_PREREQUISITE_HAS_ACCEPTED_INTERFACE"
    )


def test_product_registries_remain_empty_in_pi_packet():
    ontology = json.loads(ONTOLOGY_REGISTRY.read_text(encoding="utf-8"))
    mapping = json.loads(MAPPING_REGISTRY.read_text(encoding="utf-8"))
    assert ontology["registry_status"] == "EMPTY_PENDING_KB_WP06B"
    assert ontology["nodes"] == []
    assert mapping["registry_status"] == "EMPTY_PENDING_KB_WP06C"
    assert mapping["mappings"] == []

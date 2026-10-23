import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET_PATH = ROOT / "knowledge/core/wp06b/MANIFESTATION_ROOT_DECISION_PACKET_v0.1.json"
ONTOLOGY_REGISTRY = ROOT / "product/PL3M_MANIFESTATION_ONTOLOGY_REGISTRY_v0.1.json"
MAPPING_REGISTRY = ROOT / "product/PL3M_MANIFESTATION_MAPPING_REGISTRY_v0.1.json"


def packet():
    return json.loads(PACKET_PATH.read_text(encoding="utf-8"))


def source_row(item):
    path = ROOT / item["canonical_record_path"]
    if path.suffix == ".json":
        payload = json.loads(path.read_text(encoding="utf-8"))
        matches = [
            row for row in payload["records"]
            if row["projection_rule_id"] == item["source_rule_id"]
        ]
        assert len(matches) == 1, item["source_rule_id"]
        row = matches[0]
        return {
            "record_kind": "accepted_source_readjudication_json",
            "source_id": payload["source_basis"]["source_id"],
            "source_location": row["source_location"],
            "condition": row["canonical_condition"],
            "projection_domain": row["canonical_projection_domain"],
            "projection_target": row["canonical_projection_target"],
            "projection_mode": row["projection_mode"],
            "case_support_only": row["case_support_only"],
            "disposition": row["disposition"],
            "canonical_promotion": row["canonical_promotion"],
        }
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    matches = [row for row in rows if row["projection_rule_id"] == item["source_rule_id"]]
    assert len(matches) == 1, item["source_rule_id"]
    row = matches[0]
    return {"record_kind": "accepted_source_csv", **row}


def test_root_packet_uses_only_accepted_main_source_rows_and_exact_spans():
    d = packet()
    assert d["source_basis"]["source_id"] == "SRC-ZZ-003"
    assert d["source_basis"]["school"] == "中州派"
    assert d["source_basis"]["current_main_base_sha"] == "2143ac7030b531cd46836cf034baba6f801bdf8e"
    assert len(d["source_evidence"]) == 8
    assert len({x["source_rule_id"] for x in d["source_evidence"]}) == 8
    for item in d["source_evidence"]:
        row = source_row(item)
        assert row["source_id"] == item["source_id"] == "SRC-ZZ-003"
        assert row["source_location"] == item["source_location"]
        assert row["condition"] == item["source_condition_text"]
        assert row["projection_domain"] == item["projection_domain"]
        assert row["projection_target"] == item["projection_target"]
        assert row["projection_mode"] == item["projection_mode"]
        if row["record_kind"] == "accepted_source_csv":
            assert row["review_status"] == "SOURCE_SPAN_VERIFIED"
            assert row["source_span_verified"].lower() == "true"
            assert row["case_support_only"].lower() == str(item["case_support_only"]).lower()
        else:
            # P07 M01 pre-G12 CSV is historical acceleration input only; the
            # accepted source readjudication JSON is the canonical evidence.
            assert row["disposition"] == "DIRECT_SOURCE_RECHECK_CONFIRMED"
            assert row["canonical_promotion"] is True
            assert row["case_support_only"] is item["case_support_only"]
        page_match = re.search(r"printed_p(\d+)", row["source_location"])
        assert page_match, item["source_rule_id"]
        assert item["source_span_id"] == f"ZZ003-P{page_match.group(1)}"
        assert item["school"] == "中州派"
        assert item["probability_status"] == "UNKNOWN"
        assert item["ontology_node_id"] is None


def test_source_native_family_labels_are_candidates_not_frozen_ontology_vocabulary():
    d = packet()
    for item in d["source_evidence"]:
        assert item["candidate_family_review_id"]
        assert item["candidate_family_label"]
        assert item["abstraction_level_candidate"].endswith("_CANDIDATE") or item["abstraction_level_candidate"] in {
            "CONCRETE_EVENT_CANDIDATE_CASE_ONLY",
            "INFERENCE_CONSTRAINT_NOT_MANIFESTATION",
        }
        assert item["abstraction_vocabulary_frozen"] is False
        assert item["excluded_from_canonical_root_evidence"] in {True, False}
    ca01 = next(x for x in d["source_evidence"] if x["source_rule_id"] == "CA01-035")
    assert ca01["source_quote"] == "事业宫见火铃，主波折。故往往经艰苦而始能底定事业。"
    assert ca01["projection_mode"] == "FUNCTIONAL_PROJECTION"
    assert ca01["abstraction_level_candidate"] == "PROCESS_PATTERN_CANDIDATE"
    assert "火铃" in "；".join(ca01["ambiguity_notes"])
    assert "往往" in ca01["source_quote"]


def test_action_prerequisite_scene_boundary_and_case_only_exclusion_are_preserved():
    d = packet()
    ca01_045 = next(x for x in d["source_evidence"] if x["source_rule_id"] == "CA01-045")
    assert ca01_045["antecedent_rule_ids"] == ["CA01-042", "CA01-044"]
    assert ca01_045["real_world_action_prerequisite"] is True
    assert "勉强求变" in ca01_045["source_quote"]
    ca05_469 = next(x for x in d["source_evidence"] if x["source_rule_id"] == "CA05-469")
    assert ca05_469["projection_mode"] == "SCENE_TRANSLATION"
    assert ca05_469["event_specificity_candidate"] == "SCENE_NOT_OBSERVED_EVENT"
    assert "个人受伤" in "；".join(ca05_469["ambiguity_notes"])
    ca09_809 = next(x for x in d["source_evidence"] if x["source_rule_id"] == "CA09-809")
    assert ca09_809["case_support_only"] is True
    assert ca09_809["excluded_from_canonical_root_evidence"] is True
    ca01_005 = next(x for x in d["source_evidence"] if x["source_rule_id"] == "CA01-005")
    assert ca01_005["projection_mode"] == "CROSS_PALACE_CONSTRAINT"
    assert ca01_005["excluded_from_canonical_root_evidence"] is True


def test_root_choice_is_not_made_and_no_product_registry_is_populated():
    d = packet()
    assert d["status"] == "HUMAN_GATE_PACKET_NOT_CANONICAL"
    assert d["human_gate"]["gate_id"] == "HG-WP06B-MANIFESTATION-ROOT-01"
    assert d["human_gate"]["status"] == "PENDING_PI_DECISION"
    assert d["human_gate"]["decision_made"] is False
    assert len(d["root_options"]) == 3
    assert all(option["selected"] is False for option in d["root_options"])
    assert d["preliminary_review_recommendation"]["status"] == "RECOMMENDATION_FOR_PI_REVIEW_ONLY_NOT_SELECTED"
    assert d["canonicalization"]["accepted_root_id"] is None
    assert d["canonicalization"]["accepted_nodes"] == []
    assert d["canonicalization"]["ontology_node_ids_assigned"] is False
    assert d["canonicalization"]["production_ontology_registry_status"] == "EMPTY_PENDING_KB_WP06B"
    assert d["canonicalization"]["production_mapping_registry_status"] == "EMPTY_PENDING_KB_WP06C"
    assert d["canonicalization"]["product_consumption_authorized"] is False
    assert d["canonicalization"]["probability_status"] == "UNKNOWN"

    ontology = json.loads(ONTOLOGY_REGISTRY.read_text(encoding="utf-8"))
    mapping = json.loads(MAPPING_REGISTRY.read_text(encoding="utf-8"))
    assert ontology["registry_status"] == "EMPTY_PENDING_KB_WP06B"
    assert ontology["nodes"] == []
    assert mapping["registry_status"] == "EMPTY_PENDING_KB_WP06C"
    assert mapping["mappings"] == []


def test_projection_mode_is_not_reused_as_ontology_abstraction_level():
    d = packet()
    ca01 = next(x for x in d["source_evidence"] if x["source_rule_id"] == "CA01-035")
    assert ca01["projection_mode"] == "FUNCTIONAL_PROJECTION"
    assert ca01["abstraction_level_candidate"] == "PROCESS_PATTERN_CANDIDATE"
    assert ca01["projection_mode"] != ca01["abstraction_level_candidate"]
    assert all(x["ontology_node_id"] is None for x in d["source_evidence"])

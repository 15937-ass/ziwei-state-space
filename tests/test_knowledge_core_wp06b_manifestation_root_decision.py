import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET_PATH = ROOT / "knowledge/core/wp06b/MANIFESTATION_ROOT_DECISION_PACKET_v0.1.json"
ONTOLOGY_REGISTRY = ROOT / "product/PL3M_MANIFESTATION_ONTOLOGY_REGISTRY_v0.1.json"
MAPPING_REGISTRY = ROOT / "product/PL3M_MANIFESTATION_MAPPING_REGISTRY_v0.1.json"
P09_INDEX_PATH = ROOT / "knowledge/palaces/P09_career/wp06c/P09_WP06C_SOURCE_CANDIDATE_INDEX_v0.1.json"


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
    assert d["source_basis"]["source_review_base_sha"] == "2143ac7030b531cd46836cf034baba6f801bdf8e"
    assert d["source_basis"]["current_main_base_sha"] == "2267c5686ce353b5f7b8a4b56f0335bf3792ac63"
    assert d["capability_comparison"]["fixture_main_base_sha"] == "2267c5686ce353b5f7b8a4b56f0335bf3792ac63"
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
    w01_002 = next(x for x in d["source_evidence"] if x["source_rule_id"] == "W01-002")
    assert w01_002["projection_mode"] == "PALACE_SEMANTIC_BOUNDARY"
    assert w01_002["event_specificity_candidate"] == "NOT_A_MANIFESTATION"
    assert w01_002["excluded_from_canonical_root_evidence"] is True
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


def test_pi_decision_selects_option_c_direction_only_without_canonical_promotion():
    d = packet()
    assert d["status"] == "PI_DECISION_RECORDED_OPTION_C_NOT_CANONICAL"
    assert d["human_gate"]["gate_id"] == "HG-WP06B-MANIFESTATION-ROOT-01"
    assert d["human_gate"]["status"] == "PI_DECISION_RECORDED_OPTION_C_DIRECTION_ONLY"
    assert d["human_gate"]["decision_made"] is True
    assert d["human_gate"]["requires_pi_decision"] is False
    assert d["human_gate"]["follow_up_work"] == "W5_MINIMAL_METADATA_CONTRACT_REVIEW"
    assert d["pi_decision"]["selected_option_id"] == "OPTION-C"
    assert d["pi_decision"]["status"] == "DIRECTION_ACCEPTED_CONTRACT_NOT_FROZEN"
    assert d["pi_decision"]["follow_up_review_required"] is True
    assert len(d["root_options"]) == 3
    assert {o["option_id"]: o["selected"] for o in d["root_options"]} == {
        "OPTION-A": False, "OPTION-B": False, "OPTION-C": True
    }
    assert d["preliminary_review_recommendation"]["status"] == "SUPERSEDED_BY_EXPLICIT_PI_DECISION_OPTION_C"
    assert d["canonicalization"]["accepted_root_id"] is None
    assert d["canonicalization"]["accepted_nodes"] == []
    assert d["canonicalization"]["ontology_node_ids_assigned"] is False
    assert d["canonicalization"]["ontology_contract_frozen"] is False
    assert d["canonicalization"]["production_ontology_registry_status"] == "EMPTY_PENDING_KB_WP06B"
    assert d["canonicalization"]["production_mapping_registry_status"] == "EMPTY_PENDING_KB_WP06C"
    assert d["canonicalization"]["product_consumption_authorized"] is False
    assert d["canonicalization"]["probability_status"] == "UNKNOWN"
    assert d["capability_comparison"]["architecture_option_selected"] is True
    assert d["capability_comparison"]["selected_architecture_option"] == "OPTION-C"
    assert d["capability_comparison"]["canonical_root_selected"] is False

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

def test_packet_does_not_use_legacy_or_unrevalidated_palace_rows_as_canonical():
    d = packet()
    by_id = {item["source_rule_id"]: item for item in d["source_evidence"]}
    assert "W07-605" not in by_id
    assert "SP03-206" not in by_id
    assert "D06-508" not in by_id
    assert "D01-003" not in by_id
    assert by_id["M01-006"]["canonical_record_path"] == (
        "knowledge/palaces/P07_migration/wp05/"
        "MIGRATION_M01_SOURCE_READJUDICATION_100_v0.1.json"
    )
    assert all(
        item["canonical_record_path"] != "validation/wp05/M01_migration_projection_review_001_100.csv"
        for item in d["source_evidence"]
    )

def test_latest_main_p09_candidate_index_cross_check_does_not_promote_root_evidence():
    d = packet()
    cross_check = d["source_basis"]["latest_main_cross_check"]
    assert cross_check["main_base_sha"] == "2267c5686ce353b5f7b8a4b56f0335bf3792ac63"
    assert cross_check["artifact_commit_sha"] == "bee69d462a73abda1b51d3271d44f59627e3cbc6"
    assert d["source_basis"]["latest_main_governance_check"]["commit_sha"] == "3407150866a5ace99552daa674356b92610f080e"
    assert d["source_basis"]["latest_main_governance_check"]["merged_pr"] == 703
    assert d["source_basis"]["latest_main_governance_check"]["changed_paths"] == [
        "CHATGPT_START_HERE.md",
        "governance/GOVERNANCE_STATE.yaml",
        "governance/proposals/700-durable-ontology-plan-and-cross-chat-handoff.md"
    ]
    current_main_change = d["source_basis"]["latest_main_non_core_checkpoint"]
    assert current_main_change["main_sha"] == "971cffc166e318b1c47184c3d297422dac1e3c2b"
    latest_main = d["source_basis"]["latest_main_checkpoint"]
    assert latest_main["prior_main_sha"] == "971cffc166e318b1c47184c3d297422dac1e3c2b"
    assert latest_main["current_main_sha"] == "2267c5686ce353b5f7b8a4b56f0335bf3792ac63"
    assert latest_main["commits_ahead"] == 1
    assert latest_main["core_source_evidence_paths_changed"] is False
    assert latest_main["wp06b_paths_changed"] is False
    assert latest_main["source_record_blob_checks_unchanged"] is True
    assert latest_main["main_quality_gate_run_id"] == 39947533885
    assert current_main_change["prior_main_sha"] == "3407150866a5ace99552daa674356b92610f080e"
    assert current_main_change["merged_pr"] == 698
    assert current_main_change["changed_paths_since_prior_main"] == [
        "product/PL7_PROSPECTIVE_COHORT_MANAGER_ACCEPTANCE.md",
        "product/PRODUCT_STATE.yaml",
        "src/product/prospective_cohort_manager.py",
        "tests/test_product_prospective_cohort_manager.py",
        "tests/test_product_source_only_vertical_slice_blocker_handoff.py",
    ]
    assert current_main_change["source_evidence_paths_changed"] is False
    assert {item["path"]: item["blob_sha"] for item in current_main_change["verified_source_paths"]} == {
        "validation/wp05/CA01_career_projection_review_001_100.csv": "a18ce21a5d46da1c05f9ba0dace017d319ed377a",
        "validation/wp05/CA05_career_projection_review_401_500.csv": "08f812c0e928093977e17a303482e382d41375d0",
        "validation/wp05/W01_wealth_projection_review_001_100.csv": "f0db066d3f8abae58309104bcd75d863fe0cb557",
        "knowledge/palaces/P07_migration/wp05/MIGRATION_M01_SOURCE_READJUDICATION_100_v0.1.json": "8adc20a637ac99e5c7aa537850cbc4968fe10908",
    }
    assert cross_check["artifact_path"] == (
        "knowledge/palaces/P09_career/wp06c/P09_WP06C_SOURCE_CANDIDATE_INDEX_v0.1.json"
    )
    assert cross_check["artifact_status"] == "CANDIDATE_ONLY_NOT_CANONICAL"
    assert cross_check["source_rule_ids"] == ["CA01-035", "CA01-045", "CA05-469"]
    assert "does not prove a universal root" in cross_check["decision_impact"]

    index = json.loads(P09_INDEX_PATH.read_text(encoding="utf-8"))
    assert index["artifact_id"] == "KB-WP06C-P09-SOURCE-CANDIDATE-INDEX"
    assert index["status"] == "CANDIDATE_ONLY_NOT_CANONICAL"
    assert index["dependencies"]["wp06b_issue"] == 672
    assert index["dependencies"]["human_gate_id"] == d["human_gate"]["gate_id"]
    assert index["invariants"]["canonical_mapping"] is False
    assert index["invariants"]["ontology_node_ids_assigned"] is False
    assert index["invariants"]["executable"] is False
    assert index["invariants"]["product_consumable"] is False
    assert index["invariants"]["probability_status"] == "UNKNOWN"

    packet_by_rule = {item["source_rule_id"]: item for item in d["source_evidence"]}
    index_by_rule = {item["source_rule_id"]: item for item in index["candidates"]}
    assert set(index_by_rule) == {"CA01-035", "CA01-045", "CA05-469"}
    for rule_id, candidate in index_by_rule.items():
        item = packet_by_rule[rule_id]
        projection = candidate["normalized_projection"]
        assert candidate["source_span_ids"] == [item["source_span_id"]]
        assert projection["projection_domain"] == item["projection_domain"]
        assert projection["projection_target"] == item["projection_target"]
        assert projection["projection_mode"] == item["projection_mode"]
        assert candidate["ontology_node_id"] is None
        assert candidate["probability_status"] == "UNKNOWN"
        assert candidate["executable"] is False
        assert candidate["product_consumable"] is False


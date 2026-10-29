"""Integrity tests for Core #874 first canonical P09 manifestation nodes."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NODE_DIR = ROOT / "knowledge/core/wp06b/canonical_manifestations"
INDEX = ROOT / "knowledge/core/wp06b/CANONICAL_MANIFESTATION_NODE_INDEX_v0.1.json"
SCHEMA = ROOT / "knowledge/core/wp06b/CANONICAL_MANIFESTATION_NODE_SCHEMA_v0.1.json"
POLICY = ROOT / "knowledge/core/wp06b/CANONICAL_MANIFESTATION_ID_POLICY_v0.1.json"
PRODUCT_ONTOLOGY = ROOT / "product/PL3M_MANIFESTATION_ONTOLOGY_REGISTRY_v0.1.json"
PRODUCT_MAPPING = ROOT / "product/PL3M_MANIFESTATION_MAPPING_REGISTRY_v0.1.json"
PILOT = ROOT / "knowledge/core/wp06c/P09_FORMAL_MAPPING_REVIEW_PILOT_v0.1.json"
SOURCE_INDEX = ROOT / "knowledge/palaces/P09_career/wp06c/P09_WP06C_SOURCE_CANDIDATE_INDEX_v0.1.json"

EXPECTED = {
    "KMN-000001": "CA01-035",
    "KMN-000002": "CA01-045",
    "KMN-000003": "CA05-469",
}


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def nodes():
    return {p.stem: load(p) for p in sorted(NODE_DIR.glob("KMN-*.json"))}


def assert_node_matches_frozen_schema(node):
    schema = load(SCHEMA)
    policy = load(POLICY)
    required = set(schema["required"])
    assert required <= set(node)
    assert set(node) <= set(schema["properties"])
    assert re.fullmatch(policy["id_policy"]["regex"], node["manifestation_id"])
    assert node["parent_id"] is None or re.fullmatch(policy["id_policy"]["regex"], node["parent_id"])
    assert node["source_epistemic"] in schema["properties"]["source_epistemic"]["enum"]
    assert node["normalization_epistemic"] in schema["properties"]["normalization_epistemic"]["enum"]
    rp = node["review_provenance"]
    assert rp["review_status"] in schema["properties"]["review_provenance"]["properties"]["review_status"]["enum"]
    assert rp["source_span_verified"] is True
    assert rp["normalization_verified"] is True
    for axis in ("output_kind", "event_specificity"):
        assert node[axis]["state"] in schema["$defs"]["review_axis"]["properties"]["state"]["enum"]
        if node[axis]["state"] == "KNOWN":
            assert isinstance(node[axis]["value"], str) and node[axis]["value"]
        else:
            assert node[axis]["value"] is None
    assert node["source_supported_labels"]
    assert node["source_rule_ids"]
    assert node["source_refs"]
    assert node["mapping_review_refs"]
    assert node["identity_rationale"]
    assert node["probability_status"] == "UNKNOWN"
    assert node["canonical_identity_status"] == "ACTIVE"
    assert node["supersession"] == {"supersedes": [], "superseded_by": [], "reason": None}


def test_exactly_first_three_production_kmn_nodes_exist():
    d = nodes()
    assert set(d) == set(EXPECTED)
    for node_id, source_rule_id in EXPECTED.items():
        assert d[node_id]["manifestation_id"] == node_id
        assert source_rule_id in d[node_id]["source_rule_ids"]
        assert_node_matches_frozen_schema(d[node_id])


def test_index_is_partial_canonical_knowledge_and_next_id_is_000004():
    idx = load(INDEX)
    assert idx["status"] == "PARTIAL_CANONICAL_KNOWLEDGE"
    assert idx["coverage"]["production_node_count"] == 3
    assert idx["coverage"]["next_allocatable_id"] == "KMN-000004"
    assert [x["manifestation_id"] for x in idx["nodes"]] == list(EXPECTED)
    assert idx["forest_semantics"]["universal_root_present"] is False
    assert idx["forest_semantics"]["all_current_parent_ids_null"] is True
    assert all(load(ROOT / x["path"])["manifestation_id"] == x["manifestation_id"] for x in idx["nodes"])


def test_all_three_are_parentless_without_universal_root_claim():
    for node in nodes().values():
        assert node["parent_id"] is None
    policy = load(POLICY)
    assert policy["parent_policy"]["null_parent_does_not_mean_universal_root"] is True
    assert policy["parent_policy"]["universal_family_root_shared_primitive_requires_pi_human_gate"] is True


def test_ca01035_process_identity_preserves_modality_and_trigger_ambiguity():
    n = nodes()["KMN-000001"]
    assert n["output_kind"] == {"state": "KNOWN", "value": "PROCESS_PATTERN"}
    assert n["event_specificity"] == {"state": "KNOWN", "value": "PROCESS_SEQUENCE_NOT_SINGLE_EVENT"}
    text = " ".join(n["source_supported_labels"] + n["ambiguity_notes"] + n["unresolved_notes"])
    assert "往往" in text
    assert "BOTH_STARS" in text and "EITHER_STAR" in text
    assert n["normalization_epistemic"] == "SOURCE_PRESERVING"


def test_ca01045_identity_keeps_antecedents_and_real_world_action_blocker():
    n = nodes()["KMN-000002"]
    assert set(["CA01-042", "CA01-044", "CA01-045"]) <= set(n["source_rule_ids"])
    assert n["output_kind"]["value"] == "ACTION_CONDITIONED_OUTCOME"
    assert n["event_specificity"]["value"] == "CONDITIONAL_OUTCOME_NOT_OBSERVED"
    text = " ".join(n["source_supported_labels"] + n["ambiguity_notes"] + n["unresolved_notes"])
    assert "勉强求变" in text
    assert "non-executable" in n["unresolved_notes"][0]


def test_ca05469_is_inferred_career_scene_not_personal_injury_event():
    n = nodes()["KMN-000003"]
    assert n["domain"] == "career"
    assert n["normalization_epistemic"] == "INFERRED"
    assert n["output_kind"]["value"] == "SCENE_OR_CONTEXT"
    assert n["event_specificity"]["value"] == "SCENE_NOT_OBSERVED_EVENT"
    text = " ".join(n["source_supported_labels"] + n["ambiguity_notes"] + [n["identity_rationale"]])
    assert "行业" in text
    assert "injury" in text or "伤" in text
    assert "not evidence" in text or "不是" in text or "excludes" in text


def test_node_identity_remains_non_executable_and_non_product_after_separate_mapping_gate():
    idx = load(INDEX)
    # #874 established node identity only. #880 is a later, separately PI-authorized
    # canonical-mapping gate; mapping acceptance must not retroactively imply execution
    # or Product consumption.
    assert idx["invariants"]["canonical_mapping_promotions"] == 3
    assert idx["invariants"]["executable_mappings"] == 0
    assert idx["invariants"]["product_registry_modified"] is False
    assert idx["invariants"]["product_consumption_authorized"] is False
    assert idx["invariants"]["universal_root_or_family_created"] is False
    assert idx["invariants"]["probability_status"] == "UNKNOWN"
    expected_refs = {
        "KMN-000001": ["KMM-000001"],
        "KMN-000002": ["KMM-000002"],
        "KMN-000003": ["KMM-000003"],
    }
    for item in idx["nodes"]:
        assert item["canonical_mapping_approved"] is True
        assert item["canonical_mapping_refs"] == expected_refs[item["manifestation_id"]]
        assert item["executable"] is False
        assert item["product_consumable"] is False
        assert item["probability_status"] == "UNKNOWN"


def test_product_production_registries_remain_empty_fail_closed():
    ontology = load(PRODUCT_ONTOLOGY)
    mapping = load(PRODUCT_MAPPING)
    assert ontology["registry_status"] == "EMPTY_PENDING_KB_WP06B"
    assert ontology["nodes"] == []
    assert mapping["registry_status"] == "EMPTY_PENDING_KB_WP06C"
    assert mapping["mappings"] == []


def test_each_canonical_node_is_backed_by_accepted_positive_review_and_verified_source():
    d = nodes()
    pilot = load(PILOT)
    source_index = load(SOURCE_INDEX)
    pilot_candidates = {x["source_rule_id"]: x for x in pilot["candidates"]}
    source_candidates = {x["source_rule_id"]: x for x in source_index["candidates"]}
    reviews = {x["review_record_id"]: x for x in pilot["mapping_review_records"]}

    for node_id, source_rule_id in EXPECTED.items():
        node = d[node_id]
        pc = pilot_candidates[source_rule_id]
        sc = source_candidates[source_rule_id]
        positive = reviews[pc["positive_target_review_id"]]

        assert positive["mapping_disposition"] == {
            "state": "KNOWN",
            "value": "supported_candidate",
            "conflict_ref": None,
        }
        assert pc["positive_target_review_id"] in node["mapping_review_refs"]
        assert sc["source"]["review_status"] == "SOURCE_SPAN_VERIFIED"
        assert sc["source"]["source_span_verified"] is True
        assert sc["source"]["case_support_only"] is False
        assert node["source_epistemic"] == pc["source_epistemic"]
        assert node["normalization_epistemic"] == pc["normalization_epistemic"]


def test_ca05469_uses_later_accepted_inferred_normalization_boundary():
    node = nodes()["KMN-000003"]
    pilot = load(PILOT)
    candidate = next(x for x in pilot["candidates"] if x["source_rule_id"] == "CA05-469")
    assert candidate["normalization_epistemic"] == "INFERRED"
    assert node["normalization_epistemic"] == "INFERRED"
    assert "MR-P09-CA05469-INJURY-NEG-002" in node["mapping_review_refs"]

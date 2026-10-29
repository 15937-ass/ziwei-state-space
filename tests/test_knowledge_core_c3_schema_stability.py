"""Core #912 C3 schema-stability and review-provenance regression tests."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "knowledge/core/wp06c/CANONICAL_MAPPING_SCHEMA_STABILITY_REVIEW_C3_v0.1.json"
PROV = ROOT / "knowledge/core/wp06c/CANONICAL_MAPPING_REVIEW_PROVENANCE_INDEX_v0.1.json"
MAP_INDEX = ROOT / "knowledge/core/wp06c/CANONICAL_MANIFESTATION_MAPPING_INDEX_v0.1.json"
NODE_INDEX = ROOT / "knowledge/core/wp06b/CANONICAL_MANIFESTATION_NODE_INDEX_v0.1.json"
MAP_SCHEMA = ROOT / "knowledge/core/wp06c/CANONICAL_MANIFESTATION_MAPPING_SCHEMA_v0.1.json"
NODE_SCHEMA = ROOT / "knowledge/core/wp06b/CANONICAL_MANIFESTATION_NODE_SCHEMA_v0.1.json"
MAP_DIR = ROOT / "knowledge/core/wp06c/canonical_mappings"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_c3_verdict_is_stable_with_only_backward_compatible_refinement():
    d = load(REVIEW)
    assert d["verdict"] == "STABLE_WITH_BACKWARD_COMPATIBLE_REFINEMENT"
    r = d["backward_compatible_refinement"]
    assert r["schema_version_bump_required"] is False
    assert r["existing_kmn_or_kmm_rewrite_required"] is False
    assert r["semantic_change"] is False
    assert d["human_gate"]["required"] is False


def test_c3_audits_exactly_the_accepted_fifteen_mapping_checkpoint():
    d = load(REVIEW)
    mi, ni = load(MAP_INDEX), load(NODE_INDEX)
    assert mi["coverage"]["canonical_mapping_count"] == 15
    assert ni["coverage"]["production_node_count"] == 15
    assert mi["coverage"]["next_allocatable_id"] == "KMM-000016"
    assert ni["coverage"]["next_allocatable_id"] == "KMN-000016"
    matrix = d["stability_matrix"]
    assert len(matrix) == 15
    assert {x["mapping_id"] for x in matrix} == {f"KMM-{i:06d}" for i in range(1, 16)}
    assert all(x["canonical_preservation_verdict"] == "SUFFICIENT_NO_SCHEMA_CHANGE" for x in matrix)


def test_review_provenance_index_is_unique_non_semantic_and_resolves_all_mapping_refs():
    p = load(PROV)
    assert p["semantic_authority"] is False
    assert p["invariants"]["does_not_change_mapping_meaning"] is True
    assert p["invariants"]["does_not_change_review_disposition"] is True
    assert p["invariants"]["does_not_create_shared_semantic_primitive"] is True
    assert p["coverage"]["review_record_count"] == 30
    entries = p["entries"]
    by_id = {x["review_record_id"]: x for x in entries}
    assert len(by_id) == len(entries) == 30

    mi = load(MAP_INDEX)
    for item in mi["mappings"]:
        m = load(ROOT / item["path"])
        for ref in m["review_refs"]["positive"]:
            assert by_id[ref]["mapping_disposition"]["value"] == "supported_candidate"
        for ref in m["review_refs"]["negative_boundaries"]:
            assert by_id[ref]["mapping_disposition"]["value"] == "not_supported_for_target"


def test_open_axis_vocabulary_remains_open_and_not_refrozen_by_c3():
    d = load(REVIEW)
    ms, ns = load(MAP_SCHEMA), load(NODE_SCHEMA)
    assert d["accepted_architecture_constraints"]["output_kind_nonexhaustive_open"] is True
    assert "enum" not in ms["$defs"]["review_axis"]["properties"]["value"]
    node_value = ns["$defs"]["review_axis"]["properties"]["value"]["oneOf"][0]
    assert "enum" not in node_value
    assert d["corpus_observations"]["output_kind_distinct_count"] == 15
    assert d["corpus_observations"]["event_specificity_distinct_count"] == 14


def test_product_feedback_is_not_silently_reclassified_as_core_gap():
    d = load(REVIEW)
    rows = {x["gap_id"]: x for x in d["product_feedback_disposition"]}
    for gap in [f"PG-{i:03d}" for i in range(1, 8)]:
        assert rows[gap]["owner"] == "PRODUCT"
        assert rows[gap]["core_disposition"] == "NO_CORE_CHANGE"
    assert rows["HOLD-CORE-001"]["core_disposition"] == "PRESERVE_HOLD"
    assert rows["HOLD-CORE-002"]["core_disposition"] == "PRESERVE_HOLD"


def test_unresolved_and_external_prerequisite_cases_remain_fail_closed():
    d = load(REVIEW)
    ready = d["corpus_observations"]["execution_readiness_distribution"]
    assert ready == {
        "BLOCKED_SEMANTIC": 3,
        "BLOCKED_EXTERNAL_PREREQUISITE": 1,
        "KNOWLEDGE_READY_RUNTIME_NOT_AUTHORIZED": 11,
    }
    for mid in ("KMM-000001", "KMM-000004", "KMM-000011"):
        m = load(MAP_DIR / f"{mid}.json")
        assert m["execution_readiness"] == "BLOCKED_SEMANTIC"
        assert m["executable"] is False
    m2 = load(MAP_DIR / "KMM-000002.json")
    assert m2["execution_readiness"] == "BLOCKED_EXTERNAL_PREREQUISITE"
    assert m2["executable"] is False


def test_unexercised_contract_branches_are_declared_not_overclaimed():
    d = load(REVIEW)
    branches = set(d["unexercised_contract_branches"])
    assert "canonical KMM with output_kind UNKNOWN" in branches
    assert "canonical KMM with event_specificity NOT_APPLICABLE" in branches
    assert "canonical KMN with non-null parent_id" in branches
    assert "canonical KMN/KMM SUPERSEDED lifecycle" in branches


def test_c3_does_not_create_root_probability_or_product_authority():
    d = load(REVIEW)
    ni, mi = load(NODE_INDEX), load(MAP_INDEX)
    assert d["accepted_architecture_constraints"]["universal_root_created"] is False
    assert ni["invariants"]["universal_root_or_family_created"] is False
    assert mi["invariants"]["universal_root_or_family_created"] is False
    assert mi["invariants"]["executable_mappings"] == 0
    assert mi["invariants"]["product_consumption_authorized"] is False
    assert mi["invariants"]["probability_status"] == "UNKNOWN"

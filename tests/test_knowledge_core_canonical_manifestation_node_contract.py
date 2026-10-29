"""Integrity tests for Core #868 canonical manifestation node contract."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "knowledge/core/wp06b/CANONICAL_MANIFESTATION_NODE_SCHEMA_v0.1.json"
POLICY_PATH = ROOT / "knowledge/core/wp06b/CANONICAL_MANIFESTATION_ID_POLICY_v0.1.json"
PRODUCT_ONTOLOGY = ROOT / "product/PL3M_MANIFESTATION_ONTOLOGY_REGISTRY_v0.1.json"
PRODUCT_MAPPING = ROOT / "product/PL3M_MANIFESTATION_MAPPING_REGISTRY_v0.1.json"


def schema():
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def policy():
    return json.loads(POLICY_PATH.read_text(encoding="utf-8"))


def sample_node(node_id="KMN-999998", parent_id=None):
    return {
        "schema_version": "0.1",
        "manifestation_id": node_id,
        "parent_id": parent_id,
        "domain": "career",
        "abstraction_level": "test_only_source_native_level",
        "source_supported_labels": ["test-only label"],
        "source_rule_ids": ["TEST-RULE"],
        "source_refs": ["TEST-SOURCE#span"],
        "output_kind": {"state": "KNOWN", "value": "PROCESS_PATTERN"},
        "event_specificity": {"state": "KNOWN", "value": "PROCESS_SEQUENCE_NOT_SINGLE_EVENT"},
        "source_epistemic": "EXPLICIT",
        "normalization_epistemic": "SOURCE_PRESERVING",
        "review_provenance": {
            "review_status": "SOURCE_SPAN_VERIFIED",
            "reviewer_type": "MODEL",
            "reviewer_id": "test",
            "reviewed_at": "TEST_ONLY",
            "source_span_verified": True,
            "normalization_verified": True,
        },
        "mapping_review_refs": ["TEST-MR"],
        "identity_rationale": "Test-only stable identity rationale.",
        "ambiguity_notes": [],
        "unresolved_notes": [],
        "probability_status": "UNKNOWN",
        "canonical_identity_status": "ACTIVE",
        "supersession": {"supersedes": [], "superseded_by": [], "reason": None},
    }


def validate_collection(nodes):
    p = policy()
    pattern = re.compile(p["id_policy"]["regex"])
    ids = [n["manifestation_id"] for n in nodes]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate manifestation_id")
    id_set = set(ids)
    for node in nodes:
        node_id = node["manifestation_id"]
        if not pattern.fullmatch(node_id):
            raise ValueError("invalid manifestation_id")
        parent = node["parent_id"]
        if parent is not None and parent not in id_set:
            raise ValueError("parent_id does not resolve in artifact")
        if parent == node_id:
            raise ValueError("node cannot parent itself")
        if node["probability_status"] != "UNKNOWN":
            raise ValueError("canonical knowledge must not carry empirical probability")
        if node["source_epistemic"] not in p["canonicalization_gate"]["source_epistemic_allowed"]:
            raise ValueError("source epistemic not eligible")
        if node["normalization_epistemic"] not in p["canonicalization_gate"]["normalization_epistemic_allowed"]:
            raise ValueError("normalization epistemic not eligible")
        rp = node["review_provenance"]
        if rp["review_status"] not in p["canonicalization_gate"]["review_status_allowed"]:
            raise ValueError("review status not eligible")
        if not rp["source_span_verified"] or not rp["normalization_verified"]:
            raise ValueError("verification gate failed")
        for axis in ("output_kind", "event_specificity"):
            if node[axis]["state"] not in p["axis_policy"]["schema_allowed_canonical_axis_states"]:
                raise ValueError("axis state blocks canonicalization")
        supersession = node["supersession"]
        if node["canonical_identity_status"] == "ACTIVE":
            if supersession["superseded_by"] or supersession["reason"] is not None:
                raise ValueError("active node cannot be superseded")
        elif node["canonical_identity_status"] == "SUPERSEDED":
            if not supersession["superseded_by"] or not supersession["reason"]:
                raise ValueError("superseded node requires forward link and reason")

    parents = {n["manifestation_id"]: n["parent_id"] for n in nodes}
    for start in ids:
        seen = set()
        cur = start
        while cur is not None:
            if cur in seen:
                raise ValueError("parent cycle")
            seen.add(cur)
            cur = parents.get(cur)


def test_contract_is_frozen_without_assigning_production_ids():
    p = policy()
    assert p["status"] == "CANONICAL_CONTRACT_FROZEN_NO_PRODUCTION_NODES_ASSIGNED"
    assert p["production_nodes_created_in_this_work_unit"] is False
    assert p["canonical_mappings_promoted_in_this_work_unit"] is False
    assert p["assigned_production_ids"] == []
    assert p["universal_root_or_family_created"] is False


def test_id_namespace_is_opaque_and_not_fixture_convention():
    p = policy()["id_policy"]
    assert p["namespace"] == "KMN"
    assert p["regex"] == r"^KMN-[0-9]{6}$"
    assert p["opaque_semantics_free"] is True
    assert p["never_reuse"] is True
    assert p["immutable_after_assignment"] is True
    assert p["renumber_on_label_or_domain_wording_refinement"] is False
    assert all(p[key] is False for key in (
        "embeds_domain", "embeds_palace", "embeds_star", "embeds_rank", "embeds_probability"
    ))
    assert not re.fullmatch(p["regex"], "MFX-ROOT")
    assert not re.fullmatch(p["regex"], "M0-FX-CAREER-SCENE")


def test_parent_null_is_forest_semantics_not_universal_root():
    pp = policy()["parent_policy"]
    assert pp["option_c_source_native_forest"] is True
    assert pp["null_parent_allowed"] is True
    assert pp["null_parent_semantics"] == "NO_ACCEPTED_CANONICAL_PARENT_IN_CURRENT_ARTIFACT"
    assert pp["null_parent_does_not_mean_universal_root"] is True
    assert pp["universal_family_root_shared_primitive_requires_pi_human_gate"] is True


def test_schema_keeps_value_vocabulary_open_but_fails_closed_on_canonical_states():
    s = schema()
    axis = s["$defs"]["review_axis"]
    value = axis["properties"]["value"]["oneOf"][0]
    assert value["type"] == "string"
    assert "enum" not in value
    assert set(axis["properties"]["state"]["enum"]) == {"KNOWN", "UNKNOWN", "NOT_APPLICABLE"}
    assert s["properties"]["source_epistemic"]["enum"] == ["EXPLICIT", "INFERRED_FROM_SOURCE"]
    assert s["properties"]["normalization_epistemic"]["enum"] == ["SOURCE_PRESERVING", "INFERRED"]
    rp = s["properties"]["review_provenance"]["properties"]
    assert rp["review_status"]["enum"] == ["SOURCE_SPAN_VERIFIED", "HUMAN_VERIFIED"]
    assert rp["source_span_verified"]["const"] is True
    assert rp["normalization_verified"]["const"] is True
    assert "unresolved_notes" in s["required"]


def test_g1_g2_canonicalization_gates_are_encoded():
    gate = policy()["canonicalization_gate"]
    assert gate["ordinary_node_per_node_pi_required"] is False
    assert gate["source_epistemic_allowed"] == ["EXPLICIT", "INFERRED_FROM_SOURCE"]
    assert gate["normalization_epistemic_allowed"] == ["SOURCE_PRESERVING", "INFERRED"]
    assert gate["review_status_allowed"] == ["SOURCE_SPAN_VERIFIED", "HUMAN_VERIFIED"]
    assert gate["source_span_verified_required"] is True
    assert gate["normalization_verified_required"] is True
    assert gate["supported_mapping_review_required"] is True
    assert gate["case_support_only_as_sole_support_allowed"] is False
    assert gate["hypothesis_as_sole_support_allowed"] is False
    assert gate["probability_status_required"] == "UNKNOWN"


def test_collection_validation_rejects_duplicate_and_dangling_parent():
    one = sample_node()
    duplicate = sample_node()
    try:
        validate_collection([one, duplicate])
    except ValueError as exc:
        assert "duplicate" in str(exc)
    else:
        raise AssertionError("duplicate ID must fail")

    child = sample_node("KMN-999999", "KMN-999997")
    try:
        validate_collection([child])
    except ValueError as exc:
        assert "parent_id" in str(exc)
    else:
        raise AssertionError("dangling parent must fail")


def test_collection_validation_accepts_valid_forest_and_parent_link():
    root = sample_node("KMN-999997", None)
    child = sample_node("KMN-999998", "KMN-999997")
    validate_collection([root, child])


def test_unknown_can_be_preserved_but_missing_and_conflict_block():
    p = policy()["axis_policy"]
    assert p["unknown_allowed_only_when_identity_boundary_is_stable"] is True
    assert set(p["canonicalization_blocked_axis_states"]) == {"MISSING", "CONFLICT"}


def test_product_boundary_remains_fail_closed():
    b = policy()["product_boundary"]
    assert b["knowledge_is_ontology_owner"] is True
    assert b["product_is_adapter_consumer"] is True
    assert b["product_registry_change_authorized"] is False
    assert b["product_consumption_authorized"] is False
    assert b["canonical_node_does_not_imply_product_readiness"] is True


def test_parent_cycle_is_rejected():
    a = sample_node("KMN-999996", "KMN-999997")
    b = sample_node("KMN-999997", "KMN-999996")
    try:
        validate_collection([a, b])
    except ValueError as exc:
        assert "cycle" in str(exc)
    else:
        raise AssertionError("parent cycle must fail")


def test_supersession_requires_forward_link_and_reason():
    old = sample_node("KMN-999995")
    old["canonical_identity_status"] = "SUPERSEDED"
    old["supersession"] = {
        "supersedes": [],
        "superseded_by": ["KMN-999994"],
        "reason": "test-only identity split",
    }
    new = sample_node("KMN-999994")
    validate_collection([old, new])

    broken = sample_node("KMN-999993")
    broken["canonical_identity_status"] = "SUPERSEDED"
    broken["supersession"] = {"supersedes": [], "superseded_by": [], "reason": None}
    try:
        validate_collection([broken])
    except ValueError as exc:
        assert "forward link" in str(exc)
    else:
        raise AssertionError("superseded node without forward link/reason must fail")


def test_product_registries_remain_empty_and_fail_closed():
    ontology = json.loads(PRODUCT_ONTOLOGY.read_text(encoding="utf-8"))
    mapping = json.loads(PRODUCT_MAPPING.read_text(encoding="utf-8"))
    assert ontology["registry_status"] == "EMPTY_PENDING_KB_WP06B"
    assert ontology["nodes"] == []
    assert mapping["registry_status"] == "EMPTY_PENDING_KB_WP06C"
    assert mapping["mappings"] == []

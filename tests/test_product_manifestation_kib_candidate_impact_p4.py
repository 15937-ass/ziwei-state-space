import hashlib
import json
from pathlib import Path

from src.product.knowledge_bundle import (
    load_bundle,
    load_lock,
    verify_active_lock,
    verify_bundle,
)
from src.product.knowledge_impact import (
    DEPENDENCY_PROPAGATION,
    compare_bundles,
)


ROOT = Path(__file__).resolve().parents[1]
ACTIVE_BUNDLE_PATH = ROOT / "product/PRODUCT_KNOWLEDGE_BUNDLE_V0_3.json"
ACTIVE_LOCK_PATH = ROOT / "product/PRODUCT_KNOWLEDGE.lock.json"
CANDIDATE_BUNDLE_PATH = ROOT / "product/PRODUCT_KIB_CANDIDATE_P3_MANIFESTATION_IMPACT_V0_1.json"
REPORT_PATH = ROOT / "product/PL3M_MANIFESTATION_KMANIFEST_KIB_CANDIDATE_IMPACT_P4_V0_1.json"
FREEZE_PATH = ROOT / "product/PL3M_MANIFESTATION_P3_FORMAL_CROSSWALK_FREEZE_V0_1.json"
MAPPING_INDEX_PATH = ROOT / "knowledge/core/wp06c/CANONICAL_MANIFESTATION_MAPPING_INDEX_v0.1.json"
NODE_INDEX_PATH = ROOT / "knowledge/core/wp06b/CANONICAL_MANIFESTATION_NODE_INDEX_v0.1.json"
ONTOLOGY_REGISTRY_PATH = ROOT / "product/PL3M_MANIFESTATION_ONTOLOGY_REGISTRY_v0.1.json"
MAPPING_REGISTRY_PATH = ROOT / "product/PL3M_MANIFESTATION_MAPPING_REGISTRY_v0.1.json"


def _load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def _git_blob_sha(path):
    data = path.read_bytes()
    payload = f"blob {len(data)}\0".encode("ascii") + data
    return hashlib.sha1(payload).hexdigest()


def _component(bundle, component_id):
    return next(
        item for item in bundle["components"]
        if item["component_id"] == component_id
    )


def test_active_lock_and_noop_candidate_bundle_both_verify():
    active_lock = verify_active_lock(ROOT)
    active = load_bundle(ACTIVE_BUNDLE_PATH)
    candidate = load_bundle(CANDIDATE_BUNDLE_PATH)
    candidate_verification = verify_bundle(ROOT, candidate)

    assert active_lock["status"] == "PASS"
    assert active_lock["lock_id"] == "PRODUCT_KNOWLEDGE_LOCK_V0_3"
    assert active_lock["bundle_id"] == "KIB-PRODUCT-20261021-V0_3"
    assert active_lock["verified_artifact_count"] == 61

    assert candidate_verification["status"] == "PASS"
    assert candidate_verification["bundle_id"] == (
        "KIB-CANDIDATE-P3-MANIFESTATION-IMPACT-20261030-V0_1"
    )
    assert candidate_verification["verified_artifact_count"] == 61
    assert candidate["status"] == "CANDIDATE"
    assert candidate["candidate_from_bundle_id"] == active["bundle_id"]
    assert candidate["auto_refresh"] is False


def test_candidate_source_advance_alone_is_no_runtime_effect():
    active = load_bundle(ACTIVE_BUNDLE_PATH)
    candidate = load_bundle(CANDIDATE_BUNDLE_PATH)
    report = _load(REPORT_PATH)

    impact = compare_bundles(active, candidate)

    assert impact["source_commit_changed"] is True
    assert impact["overall_impact"] == "NO_RUNTIME_EFFECT"
    assert impact["direct_actions"] == ["NO_RUNTIME_EFFECT"]
    assert impact["downstream_invalidations"] == []
    assert impact["blockers"] == []
    assert all(
        item["primary_action"] == "NO_RUNTIME_EFFECT"
        and item["semantic_changed"] is False
        and item["artifact_set_changed"] is False
        for item in impact["component_impacts"]
    )

    summary = report["candidate_bundle_semantic_impact"]
    assert summary["overall_impact"] == impact["overall_impact"]
    assert summary["direct_actions"] == impact["direct_actions"]
    assert summary["downstream_invalidations"] == impact["downstream_invalidations"]
    assert summary["source_commit_changed"] is True


def test_k_manifest_remains_empty_in_active_and_candidate_kibs():
    active = load_bundle(ACTIVE_BUNDLE_PATH)
    candidate = load_bundle(CANDIDATE_BUNDLE_PATH)
    active_manifest = _component(active, "K_manifest")
    candidate_manifest = _component(candidate, "K_manifest")

    assert active_manifest["coverage_status"] == "EMPTY_NOT_READY"
    assert active_manifest["artifacts"] == []
    assert candidate_manifest["coverage_status"] == "EMPTY_NOT_READY"
    assert candidate_manifest["artifacts"] == []
    assert (
        candidate_manifest["component_semantic_digest"]
        == active_manifest["component_semantic_digest"]
    )


def test_all_15_mapping_and_node_authority_flags_block_materialization():
    mapping_index = _load(MAPPING_INDEX_PATH)
    node_index = _load(NODE_INDEX_PATH)
    report = _load(REPORT_PATH)

    assert len(mapping_index["mappings"]) == 15
    assert len(node_index["nodes"]) == 15
    assert all(row["executable"] is False for row in mapping_index["mappings"])
    assert all(
        row["product_consumable"] is False
        for row in mapping_index["mappings"]
    )
    assert all(row["probability_status"] == "UNKNOWN" for row in mapping_index["mappings"])

    assert all(row["executable"] is False for row in node_index["nodes"])
    assert all(row["product_consumable"] is False for row in node_index["nodes"])
    assert all(row["probability_status"] == "UNKNOWN" for row in node_index["nodes"])

    admission = report["k_manifest_admission"]
    assert admission["assessed_mapping_count"] == 15
    assert admission["knowledge_product_consumable_true_count"] == 0
    assert admission["materializable_k_manifest_entry_count"] == 0
    assert admission["materialized_k_manifest_entry_count"] == 0
    assert admission["status"] == "BLOCKED_NO_PRODUCT_CONSUMABLE_INPUTS"


def test_p4_classification_is_exactly_3_hold_4_preservation_8_structured():
    report = _load(REPORT_PATH)
    assessments = report["mapping_assessments"]

    assert len(assessments) == 15
    assert tuple(row["mapping_id"] for row in assessments) == tuple(
        f"KMM-{index:06d}" for index in range(1, 16)
    )
    assert all(
        row["candidate_k_manifest_entry_materialized"] is False
        for row in assessments
    )
    assert all(
        row["knowledge_authority"]["product_consumable"] is False
        and row["knowledge_authority"]["executable"] is False
        and row["knowledge_authority"]["probability_status"] == "UNKNOWN"
        for row in assessments
    )

    assert report["classification_counts"] == {
        "HOLD": 3,
        "PRESERVATION_ONLY": 4,
        "STRUCTURED_CANDIDATE": 8,
    }

    by_class = {}
    for row in assessments:
        by_class.setdefault(row["p4_classification"], set()).add(row["mapping_id"])

    assert by_class["HOLD"] == {
        "KMM-000001", "KMM-000004", "KMM-000011"
    }
    assert by_class["PRESERVATION_ONLY"] == {
        "KMM-000002", "KMM-000003", "KMM-000005", "KMM-000006"
    }
    assert by_class["STRUCTURED_CANDIDATE"] == {
        "KMM-000007", "KMM-000008", "KMM-000009", "KMM-000010",
        "KMM-000012", "KMM-000013", "KMM-000014", "KMM-000015"
    }


def test_p4_assessments_match_frozen_crosswalk_matrix_and_mapping_index():
    freeze = _load(FREEZE_PATH)
    mapping_index = _load(MAPPING_INDEX_PATH)
    report = _load(REPORT_PATH)
    freeze_by_id = {
        row["mapping_id"]: row
        for row in freeze["mapping_freeze_matrix"]
    }
    index_by_id = {
        row["mapping_id"]: row
        for row in mapping_index["mappings"]
    }

    for assessment in report["mapping_assessments"]:
        mapping_id = assessment["mapping_id"]
        frozen = freeze_by_id[mapping_id]
        canonical = index_by_id[mapping_id]

        assert assessment["manifestation_id"] == canonical["manifestation_id"]
        assert assessment["primary_source_rule_id"] == canonical["primary_source_rule_id"]
        assert assessment["execution_readiness"] == canonical["execution_readiness"]
        assert assessment["frozen_representation"] == frozen["representation"]
        assert assessment["frozen_contract"] == frozen["contract"]
        assert assessment["reason"] == frozen["reason"]


def test_p3_freeze_is_representation_only_not_consumption_authority():
    freeze = _load(FREEZE_PATH)
    report = _load(REPORT_PATH)

    assert freeze["status"] == "P3_FORMAL_CROSSWALK_FROZEN"
    assert freeze["verdict"]["formal_crosswalk_freeze_ready"] is True
    assert freeze["production_boundary"]["production_registry_population_allowed"] is False
    assert freeze["production_boundary"]["active_kib_promotion_allowed"] is False
    assert report["knowledge_authority_snapshot"]["product_may_override_flags"] is False
    assert report["k_manifest_admission"]["status"] == (
        "BLOCKED_NO_PRODUCT_CONSUMABLE_INPUTS"
    )


def test_hypothetical_k_manifest_semantic_change_uses_existing_impact_graph():
    report = _load(REPORT_PATH)
    policy = report["counterfactual_future_k_manifest_semantic_change"]

    assert policy["impact_class"] == "MANIFESTATION_REBUILD"
    assert policy["direct_downstream"] == {
        "artifact": "MANIFESTATION_M0",
        "action": "MANIFESTATION_REBUILD",
        "applicability": "DIRECT",
    }
    assert policy["conditional_downstream"] == [
        {
            "artifact": "EMPIRICAL_DATASET",
            "action": "DATASET_REMATERIALIZE",
            "applicability": "IF_PRESENT",
        },
        {
            "artifact": "CALIBRATED_MODEL",
            "action": "RETRAIN_OR_RECALIBRATE",
            "applicability": "IF_PRESENT",
        },
    ]
    assert DEPENDENCY_PROPAGATION["K_manifest"] == (
        ("MANIFESTATION_M0", "MANIFESTATION_REBUILD", "DIRECT"),
        ("EMPIRICAL_DATASET", "DATASET_REMATERIALIZE", "IF_PRESENT"),
        ("CALIBRATED_MODEL", "RETRAIN_OR_RECALIBRATE", "IF_PRESENT"),
    )


def test_active_lock_and_production_registries_remain_unchanged_and_empty():
    lock = _load(ACTIVE_LOCK_PATH)
    active = load_bundle(ACTIVE_BUNDLE_PATH)
    report = _load(REPORT_PATH)
    ontology = _load(ONTOLOGY_REGISTRY_PATH)
    mappings = _load(MAPPING_REGISTRY_PATH)

    assert lock["lock_id"] == "PRODUCT_KNOWLEDGE_LOCK_V0_3"
    assert lock["active_bundle_id"] == "KIB-PRODUCT-20261021-V0_3"
    assert lock["source_commit"] == "eaa33deeb77a4f982bc13121c06cad657975177b"
    assert lock["auto_refresh"] is False
    assert active["bundle_id"] == lock["active_bundle_id"]
    assert report["active_kib_snapshot"]["lock_id"] == lock["lock_id"]
    assert report["p4_verdict"]["active_lock_mutated"] is False

    assert ontology["registry_status"] == "EMPTY_PENDING_KB_WP06B"
    assert ontology["nodes"] == []
    assert mappings["registry_status"] == "EMPTY_PENDING_KB_WP06C"
    assert mappings["mappings"] == []


def test_all_p4_artifact_pins_match_exact_git_blob_ids():
    report = _load(REPORT_PATH)
    pins = [
        (ACTIVE_LOCK_PATH, report["active_kib_snapshot"]["lock_blob_sha"]),
        (ACTIVE_BUNDLE_PATH, report["active_kib_snapshot"]["active_bundle_blob_sha"]),
        (CANDIDATE_BUNDLE_PATH, report["candidate_kib_snapshot"]["git_blob_sha"]),
        (FREEZE_PATH, report["accepted_p3_freeze"]["git_blob_sha"]),
        (MAPPING_INDEX_PATH, report["knowledge_authority_snapshot"]["mapping_index_blob_sha"]),
        (NODE_INDEX_PATH, report["knowledge_authority_snapshot"]["node_index_blob_sha"]),
    ]
    for path, expected in pins:
        assert _git_blob_sha(path) == expected, path


def test_p4_verdict_keeps_all_production_authority_fail_closed():
    report = _load(REPORT_PATH)
    verdict = report["p4_verdict"]

    assert report["status"] == "CANDIDATE_IMPACT_ONLY_NO_PROMOTION"
    assert verdict["classification"] == "CANDIDATE_IMPACT_ONLY_NO_PROMOTION"
    assert verdict["candidate_k_manifest_materialization_allowed"] is False
    assert verdict["production_registry_population_allowed"] is False
    assert verdict["active_kib_promotion_allowed"] is False
    assert verdict["runtime_execution_allowed"] is False
    assert verdict["probability_claim_allowed"] is False
    assert verdict["predictive_validity_claim_allowed"] is False

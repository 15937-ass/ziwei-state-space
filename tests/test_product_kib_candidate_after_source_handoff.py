"""Contract tests for the accepted WP07B handoff's Product KIB assessment."""
import json
from pathlib import Path

from src.product.knowledge_bundle import compute_artifact_digest, verify_bundle
from src.product.knowledge_impact import compare_bundles, evaluate_promotion_gate

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_PATH = ROOT / "product" / "PRODUCT_KIB_CANDIDATE_AFTER_SOURCE_HANDOFF_V0_1.json"
ACTIVE_BUNDLE_PATH = ROOT / "product" / "PRODUCT_KNOWLEDGE_BUNDLE_V0_3.json"
LOCK_PATH = ROOT / "product" / "PRODUCT_KNOWLEDGE.lock.json"
SOURCE_PATH = ROOT / "knowledge" / "core" / "wp07b" / "TEMPORAL_REACTION_SOURCE_HANDOFF_v0.1.json"


def _package():
    return json.loads(PACKAGE_PATH.read_text(encoding="utf-8"))


def test_source_handoff_exact_bytes_commit_and_zero_eligibility_are_pinned():
    package = _package()
    source = package["source_handoff"]
    handoff = json.loads(SOURCE_PATH.read_text(encoding="utf-8"))
    assert source["path"] == "knowledge/core/wp07b/TEMPORAL_REACTION_SOURCE_HANDOFF_v0.1.json"
    assert source["git_blob_sha"] == compute_artifact_digest(SOURCE_PATH).removeprefix("git-sha1:")
    assert source["byte_count"] == len(SOURCE_PATH.read_bytes()) == 124065
    assert source["accepted_source_commit"] == package["accepted_source_commit"] == "2143ac7030b531cd46836cf034baba6f801bdf8e"
    assert source["analysis_snapshot_commit"] == handoff["snapshot"]["main_commit"] == "6088670a2a303b603d1af044288aa6a2e27a9db7"
    assert source["semantic_status"] == handoff["status"] == "SOURCE_REVIEW_COMPLETE_ZERO_ELIGIBLE_UNDER_CURRENT_CONTRACT"
    assert source["counts"]["total"] == {
        "candidates": 44,
        "eligible_current_contract": 0,
        "case_support_only": 17,
        "blocked_reusable": 27,
    }


def test_candidate_bundle_is_structurally_valid_and_verifies_exact_source_bytes():
    package = _package()
    active = json.loads(ACTIVE_BUNDLE_PATH.read_text(encoding="utf-8"))
    candidate = package["candidate_bundle"]
    verification = verify_bundle(ROOT, candidate)
    assert verification == package["candidate_verification"]
    assert verification["status"] == "PASS"
    assert candidate["status"] == "CANDIDATE"
    assert candidate["candidate_from_bundle_id"] == active["bundle_id"]
    assert candidate["source_commit"] == package["accepted_source_commit"]
    assert candidate["auto_refresh"] is False
    assert candidate["bundle_semantic_digest"] != active["bundle_semantic_digest"]


def test_only_the_accepted_wp07b_handoff_is_added_to_k_response():
    package = _package()
    active = json.loads(ACTIVE_BUNDLE_PATH.read_text(encoding="utf-8"))
    candidate = package["candidate_bundle"]
    active_components = {c["component_id"]: c for c in active["components"]}
    candidate_components = {c["component_id"]: c for c in candidate["components"]}
    added = set(candidate_components["K_response"]["artifacts"][i]["path"] for i in range(len(candidate_components["K_response"]["artifacts"]))) - set(a["path"] for a in active_components["K_response"]["artifacts"])
    assert added == {"knowledge/core/wp07b/TEMPORAL_REACTION_SOURCE_HANDOFF_v0.1.json"}
    assert len(active_components["K_response"]["artifacts"]) == 22
    assert len(candidate_components["K_response"]["artifacts"]) == 23
    assert candidate_components["K_response"]["coverage_status"] == "SOURCE_REVIEW_COMPLETE_ZERO_ELIGIBLE_UNDER_CURRENT_CONTRACT"
    assert candidate_components["K_response"]["component_semantic_digest"] != active_components["K_response"]["component_semantic_digest"]
    for component_id in ("K_signal", "K_method", "K_manifest"):
        assert candidate_components[component_id]["component_semantic_digest"] == active_components[component_id]["component_semantic_digest"]


def test_raw_impact_report_matches_existing_deterministic_comparator():
    package = _package()
    active = json.loads(ACTIVE_BUNDLE_PATH.read_text(encoding="utf-8"))
    actual = compare_bundles(active, package["candidate_bundle"])
    assert actual == package["impact_report"]
    assert actual["status"] == "READY_FOR_VALIDATION"
    assert actual["overall_impact"] == "READINESS_REBUILD"
    impacts = {x["component_id"]: x["primary_action"] for x in actual["component_impacts"]}
    assert impacts == {
        "K_manifest": "NO_RUNTIME_EFFECT",
        "K_method": "NO_RUNTIME_EFFECT",
        "K_response": "READINESS_REBUILD",
        "K_signal": "NO_RUNTIME_EFFECT",
    }
    invalidations = {x["artifact"]: x["applicability"] for x in actual["downstream_invalidations"]}
    assert invalidations["RESPONSE_READINESS"] == "DIRECT"
    assert invalidations["RESPONSE_PROFILE_TAU"] == "IF_PRESENT"
    assert invalidations["MANIFESTATION_M0"] == "IF_PRESENT"
    assert invalidations["EMPIRICAL_DATASET"] == "IF_PRESENT"
    assert invalidations["CALIBRATED_MODEL"] == "IF_PRESENT"


def test_promotion_gate_stays_blocked_despite_technical_readiness_pass():
    package = _package()
    impact_for_gate = dict(package["impact_report"])
    impact_for_gate["blockers"] = package["promotion_gate_input_blockers"]
    actual = evaluate_promotion_gate(
        impact_for_gate,
        candidate_verification=package["candidate_verification"],
        validation_results=package["promotion_gate"]["supplied_validation_results"],
    )
    assert actual == package["promotion_gate"]
    assert actual["status"] == "BLOCKED"
    assert actual["recommendation"] == "DO_NOT_PROMOTE"
    assert actual["active_lock_mutated"] is False
    assert set(actual["blockers"]) == {
        "NO_COMPILER_READY_TEMPORAL_REACTION_SPECIFICATION",
        "SOURCE_HANDOFF_ZERO_ELIGIBLE_UNDER_CURRENT_CONTRACT",
    }
    assert actual["supplied_validation_results"] == {"READINESS_REGRESSION": "PASS"}


def test_active_lock_v03_remains_pinned_and_no_runtime_authorization_is_granted():
    package = _package()
    active = json.loads(ACTIVE_BUNDLE_PATH.read_text(encoding="utf-8"))
    lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    assert lock["active_bundle_id"] == active["bundle_id"] == "KIB-PRODUCT-20261021-V0_3"
    assert lock["bundle_semantic_digest"] == active["bundle_semantic_digest"]
    assert lock["auto_refresh"] is False
    assert package["active_lock_mutated"] is False
    assert package["runtime_authorization"] == "NONE"
    assert package["production_temporal_reaction_registry_mutated"] is False
    assert package["manifestation_registries_mutated"] is False
    assert package["forecast_ledger_activated"] is False
    assert package["active_lock_snapshot"]["lock_blob_sha"] == compute_artifact_digest(LOCK_PATH).removeprefix("git-sha1:")
    assert package["active_lock_snapshot"]["active_bundle_blob_sha"] == compute_artifact_digest(ACTIVE_BUNDLE_PATH).removeprefix("git-sha1:")

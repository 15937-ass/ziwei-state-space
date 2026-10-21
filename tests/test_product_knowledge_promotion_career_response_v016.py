import json
from pathlib import Path

from src.product.knowledge_bundle import (
    compute_artifact_digest,
    load_bundle,
    load_lock,
    verify_active_lock,
    verify_bundle,
)
from src.product.knowledge_impact import compare_bundles, evaluate_promotion_gate
from src.product.response_semantics_adapter import (
    audit_response_semantics_adapter_readiness,
)


ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT / "product" / "PRODUCT_KNOWLEDGE_BUNDLE_V0_2.json"
CANDIDATE = (
    ROOT
    / "product"
    / "PRODUCT_KNOWLEDGE_CANDIDATE_CAREER_RESPONSE_V0_16.json"
)
NEW = ROOT / "product" / "PRODUCT_KNOWLEDGE_BUNDLE_V0_3.json"
PROMOTION = (
    ROOT
    / "product"
    / "PRODUCT_KNOWLEDGE_PROMOTION_CAREER_RESPONSE_V0_16.json"
)


def _component(bundle, component_id):
    return next(
        item
        for item in bundle["components"]
        if item["component_id"] == component_id
    )


def test_v016_promotion_evidence_matches_deterministic_impact():
    active = load_bundle(OLD)
    candidate = load_bundle(CANDIDATE)
    stored = json.loads(PROMOTION.read_text(encoding="utf-8"))

    verification = verify_bundle(ROOT, candidate)
    impact = compare_bundles(active, candidate)
    gate = evaluate_promotion_gate(
        impact,
        candidate_verification=verification,
        validation_results={"READINESS_REGRESSION": "PASS"},
    )

    assert verification == stored["candidate_verification"]
    assert impact == stored["impact"]
    assert gate == stored["promotion_gate"]
    assert impact["overall_impact"] == "READINESS_REBUILD"
    assert impact["direct_actions"] == [
        "NO_RUNTIME_EFFECT",
        "READINESS_REBUILD",
    ]


def test_v016_only_k_response_semantics_change():
    old = load_bundle(OLD)
    new = load_bundle(NEW)
    old_map = {item["component_id"]: item for item in old["components"]}
    new_map = {item["component_id"]: item for item in new["components"]}

    for component_id in ("K_signal", "K_manifest", "K_method"):
        assert (
            old_map[component_id]["component_semantic_digest"]
            == new_map[component_id]["component_semantic_digest"]
        )
    assert (
        old_map["K_response"]["component_semantic_digest"]
        != new_map["K_response"]["component_semantic_digest"]
    )


def test_v016_k_response_inventory_is_bounded_and_compiler_input_complete():
    old = load_bundle(OLD)
    new = load_bundle(NEW)
    old_paths = {
        item["path"]
        for item in _component(old, "K_response")["artifacts"]
    }
    new_paths = {
        item["path"]
        for item in _component(new, "K_response")["artifacts"]
    }

    assert len(old_paths) == 19
    assert len(new_paths) == 22
    assert old_paths - new_paths == {
        "knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251_v0.13.json",
    }
    assert new_paths - old_paths == {
        "knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251_v0.16.json",
        "knowledge/wp08/CAREER_COMPILER_READINESS_CENSUS_26_v0.1.json",
        "knowledge/wp08/CAREER_DEPENDENCY_IR_3_v0.1.json",
        "knowledge/wp08/CAREER_DIRECT_CONDITION_IR_9_v0.1.json",
    }


def test_v016_active_lock_points_to_v03_and_v02_remains_immutable():
    report = verify_active_lock(ROOT)
    lock = load_lock(ROOT / "product" / "PRODUCT_KNOWLEDGE.lock.json")

    assert report["status"] == "PASS"
    assert report["bundle_id"] == "KIB-PRODUCT-20261021-V0_3"
    assert report["verified_artifact_count"] == 61
    assert lock["previous_bundle_id"] == "KIB-PRODUCT-20261021-V0_2"
    assert lock["previous_bundle_path"] == (
        "product/PRODUCT_KNOWLEDGE_BUNDLE_V0_2.json"
    )

    # Historical v0.2 stays byte-identical to the accepted Product #504 bundle.
    assert compute_artifact_digest(OLD) == (
        "git-sha1:a7e4222d98b7bac8883b5094d17c8ba9e025708f"
    )
    assert verify_bundle(ROOT, load_bundle(OLD))["status"] == "PASS"


def test_v016_readiness_exposes_exactly_12_condition_ir_ready_rows():
    report = audit_response_semantics_adapter_readiness()
    career = report["career"]

    assert career["adapter_status_counts"] == {
        "BLOCKED_DEPENDENCY_COMPILER": 24,
        "BLOCKED_MULTIPLE": 44,
        "BLOCKED_SOURCE_UNDERDETERMINED": 157,
        "KNOWLEDGE_CONDITION_IR_READY_PENDING_PRODUCT_COMPILATION": 12,
        "LOCAL_STRUCTURE_NOT_CONDITION_IR_READY": 14,
    }
    assert career["compiler_readiness_band_counts"] == {
        "DEPENDENCY_EFFECTIVE_UNDERDETERMINED": 11,
        "DEPENDENCY_CONDITION_IR_READY": 3,
        "DIRECT_CONDITION_IR_READY": 9,
        "DIRECT_RELATION_OR_COMPOSITION_DEFERRED": 3,
    }
    assert career["knowledge_condition_ir_ready_total"] == 12
    assert career["dependency_condition_ir_records"] == 3
    assert career["direct_condition_ir_records"] == 9
    assert career["runtime_effects_authorized"] == 0
    assert career["condition_compiled_count"] == 0
    assert career["knowledge_execution_unlocked_count"] == 0


def test_v016_promotion_does_not_claim_response_compiler_or_prediction():
    stored = json.loads(PROMOTION.read_text(encoding="utf-8"))
    boundaries = stored["boundaries"]

    assert boundaries["k_signal_changed"] is False
    assert boundaries["k_manifest_changed"] is False
    assert boundaries["k_method_changed"] is False
    assert boundaries["response_compiler_implemented"] is False
    assert boundaries["response_profile_tau_implemented"] is False
    assert boundaries["predictive_validity_validated"] is False

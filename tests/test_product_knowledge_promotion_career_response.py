import json
from pathlib import Path

from src.product.knowledge_bundle import load_bundle, load_lock, verify_active_lock, verify_bundle
from src.product.knowledge_impact import compare_bundles, evaluate_promotion_gate
from src.product.response_semantics_adapter import audit_response_semantics_adapter_readiness

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT / "product" / "PRODUCT_KNOWLEDGE_BUNDLE_V0_1.json"
CANDIDATE = ROOT / "product" / "PRODUCT_KNOWLEDGE_CANDIDATE_CAREER_RESPONSE_V0_13.json"
NEW = ROOT / "product" / "PRODUCT_KNOWLEDGE_BUNDLE_V0_2.json"
PROMOTION = ROOT / "product" / "PRODUCT_KNOWLEDGE_PROMOTION_CAREER_RESPONSE_V0_13.json"
CORPUS = ROOT / "product" / "RESPONSE_CORPUS_READINESS_v0.1.json"


def _component(bundle, component_id):
    return next(x for x in bundle["components"] if x["component_id"] == component_id)


def test_promotion_evidence_matches_deterministic_impact():
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


def test_only_k_response_component_changes():
    old = load_bundle(OLD)
    new = load_bundle(NEW)
    old_map = {x["component_id"]: x for x in old["components"]}
    new_map = {x["component_id"]: x for x in new["components"]}
    for component_id in ("K_signal", "K_manifest", "K_method"):
        assert old_map[component_id]["component_semantic_digest"] == new_map[component_id]["component_semantic_digest"]
    assert old_map["K_response"]["component_semantic_digest"] != new_map["K_response"]["component_semantic_digest"]


def test_promoted_response_inventory_is_bounded():
    old = load_bundle(OLD)
    new = load_bundle(NEW)
    old_paths = {x["path"] for x in _component(old, "K_response")["artifacts"]}
    new_paths = {x["path"] for x in _component(new, "K_response")["artifacts"]}
    assert len(old_paths) == len(new_paths) == 19
    assert old_paths - new_paths == {
        "knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251_v0.3.json",
        "knowledge/wp08/CAREER_SEMANTIC_NORMALIZATION_36_v0.1.json",
    }
    assert new_paths - old_paths == {
        "knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251_v0.13.json",
        "knowledge/wp08/CAREER_SEMANTIC_NORMALIZATION_36_v0.2.json",
    }


def test_current_active_lock_verifies_and_preserves_v02_rollback():
    report = verify_active_lock(ROOT)
    lock = load_lock(ROOT / "product" / "PRODUCT_KNOWLEDGE.lock.json")
    assert report["status"] == "PASS"
    assert report["bundle_id"] == "KIB-PRODUCT-20261021-V0_3"
    assert report["verified_artifact_count"] == 61
    assert lock["previous_bundle_id"] == "KIB-PRODUCT-20261021-V0_2"


def test_readiness_improves_without_runtime_unlock():
    report = audit_response_semantics_adapter_readiness()
    career = report["career"]
    assert career["adapter_status_counts"] == {
        "BLOCKED_DEPENDENCY_COMPILER": 24,
        "BLOCKED_MULTIPLE": 44,
        "BLOCKED_SOURCE_UNDERDETERMINED": 157,
        "KNOWLEDGE_CONDITION_IR_READY_PENDING_PRODUCT_COMPILATION": 12,
        "LOCAL_STRUCTURE_NOT_CONDITION_IR_READY": 14,
    }
    assert career["knowledge_condition_ir_ready_total"] == 12
    assert career["runtime_effects_authorized"] == 0
    assert career["condition_compiled_count"] == 0
    assert career["knowledge_execution_unlocked_count"] == 0


def test_now6_stays_fail_closed():
    report = json.loads(CORPUS.read_text(encoding="utf-8"))
    assert report["summary"]["compiler_ready_kr_records"] == 0
    assert report["now6_gate"]["NOW6_RESPONSE_COMPILER_INPUT_READY"] is False

import copy
import json
from pathlib import Path

import pytest

from src.product.knowledge_bundle import (
    compute_artifact_digest,
    compute_bundle_semantic_digest,
    compute_component_semantic_digest,
    compute_semantic_digest,
    load_bundle,
    verify_bundle,
)
from src.product.knowledge_impact import (
    KnowledgeImpactError,
    build_candidate_bundle,
    compare_bundles,
    evaluate_promotion_gate,
    required_validations,
)


ROOT = Path(__file__).resolve().parents[1]
ACTIVE_PATH = ROOT / "product" / "PRODUCT_KNOWLEDGE_BUNDLE_V0_1.json"
CANDIDATE_PATH = ROOT / "product" / "PRODUCT_KNOWLEDGE_CANDIDATE_V0_1.json"
IMPACT_PATH = ROOT / "product" / "PRODUCT_KNOWLEDGE_IMPACT_V0_1.json"
LOCK_PATH = ROOT / "product" / "PRODUCT_KNOWLEDGE.lock.json"


def _artifact(component_id: str) -> dict:
    return {
        "path": f"fixtures/{component_id}.json",
        "artifact_type": "JSON",
        "artifact_digest": f"git-sha1:exact-{component_id}",
        "semantic_contract": "JSON_CANONICAL_FULL_V0_1",
        "semantic_digest": f"sha256:semantic-{component_id}",
    }


def _synthetic_bundle(source_commit: str = "A") -> dict:
    components = []
    for component_id in ("K_signal", "K_response", "K_manifest", "K_method"):
        artifacts = [_artifact(component_id)]
        components.append(
            {
                "component_id": component_id,
                "contract_version": "0.1",
                "coverage_status": "TEST_READY",
                "source_commit": source_commit,
                "artifacts": artifacts,
                "component_semantic_digest": compute_component_semantic_digest(
                    artifacts
                ),
            }
        )
    return {
        "schema_version": "0.1",
        "bundle_id": f"KIB-{source_commit}",
        "source_commit": source_commit,
        "components": components,
        "bundle_semantic_digest": compute_bundle_semantic_digest(components),
    }


def _component(bundle: dict, component_id: str) -> dict:
    return next(
        item
        for item in bundle["components"]
        if item["component_id"] == component_id
    )


def _semantic_mutation(bundle: dict, component_id: str) -> dict:
    candidate = copy.deepcopy(bundle)
    candidate["bundle_id"] = f"{bundle['bundle_id']}-MUTATED-{component_id}"
    component = _component(candidate, component_id)
    artifact = component["artifacts"][0]
    artifact["artifact_digest"] = (
        str(artifact["artifact_digest"]) + "-changed"
    )
    artifact["semantic_digest"] = (
        str(artifact["semantic_digest"]) + "-changed"
    )
    component["component_semantic_digest"] = compute_component_semantic_digest(
        component["artifacts"]
    )
    candidate["bundle_semantic_digest"] = compute_bundle_semantic_digest(
        candidate["components"]
    )
    return candidate


def _temp_active_bundle(tmp_path: Path) -> dict:
    components = []
    for component_id in ("K_signal", "K_response", "K_manifest", "K_method"):
        relative = f"inputs/{component_id}.json"
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(
                {"component": component_id, "value": 1},
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        artifact = {
            "path": relative,
            "artifact_type": "JSON",
            "artifact_digest": compute_artifact_digest(path),
            "semantic_contract": "JSON_CANONICAL_FULL_V0_1",
            "semantic_digest": compute_semantic_digest(
                path,
                "JSON_CANONICAL_FULL_V0_1",
            ),
        }
        components.append(
            {
                "component_id": component_id,
                "contract_version": "0.1",
                "coverage_status": "TEST_READY",
                "source_commit": "BASE",
                "artifacts": [artifact],
                "component_semantic_digest": compute_component_semantic_digest(
                    [artifact]
                ),
            }
        )
    return {
        "schema_version": "0.1",
        "bundle_id": "KIB-TEMP-ACTIVE",
        "source_commit": "BASE",
        "components": components,
        "bundle_semantic_digest": compute_bundle_semantic_digest(components),
    }


def test_bootstrap_candidate_matches_versioned_impact_report():
    active = load_bundle(ACTIVE_PATH)
    candidate = load_bundle(CANDIDATE_PATH)
    stored = json.loads(IMPACT_PATH.read_text(encoding="utf-8"))

    verification = verify_bundle(ROOT, candidate)
    impact = compare_bundles(active, candidate)
    gate = evaluate_promotion_gate(
        impact,
        candidate_verification=verification,
        validation_results={},
    )

    assert verification["status"] == "PASS"
    assert verification["verified_artifact_count"] == 58
    assert impact == stored["impact"]
    assert gate == stored["promotion_gate"]
    assert impact["overall_impact"] == "NO_RUNTIME_EFFECT"
    assert impact["source_commit_changed"] is True
    assert gate["recommendation"] == "SKIP_NO_RUNTIME_EFFECT"


def test_source_commit_advance_alone_does_not_force_rebuild():
    active = _synthetic_bundle("A")
    candidate = copy.deepcopy(active)
    candidate["bundle_id"] = "KIB-B"
    candidate["source_commit"] = "B"
    for component in candidate["components"]:
        component["source_commit"] = "B"

    impact = compare_bundles(active, candidate)

    assert impact["source_commit_changed"] is True
    assert impact["overall_impact"] == "NO_RUNTIME_EFFECT"
    assert impact["downstream_invalidations"] == []


def test_provenance_only_exact_change_requires_revalidation_not_recompile():
    active = _synthetic_bundle("A")
    candidate = copy.deepcopy(active)
    candidate["bundle_id"] = "KIB-PROVENANCE"
    component = _component(candidate, "K_response")
    component["artifacts"][0]["artifact_digest"] += "-metadata-only"

    impact = compare_bundles(active, candidate)
    response = next(
        item
        for item in impact["component_impacts"]
        if item["component_id"] == "K_response"
    )

    assert response["primary_action"] == "PROVENANCE_REVALIDATION"
    assert response["exact_changed"] is True
    assert response["semantic_changed"] is False
    assert response["artifact_deltas"][0]["change_type"] == "EXACT_ONLY"
    assert required_validations(impact) == ["LOCK_REVERIFY"]


def test_k_signal_semantic_change_propagates_only_downstream():
    active = _synthetic_bundle("A")
    candidate = _semantic_mutation(active, "K_signal")

    impact = compare_bundles(active, candidate)
    signal = next(
        item
        for item in impact["component_impacts"]
        if item["component_id"] == "K_signal"
    )
    nodes = {item["artifact"] for item in impact["downstream_invalidations"]}

    assert signal["primary_action"] == "SYMBOLIC_RECOMPILE"
    assert {
        "NATAL_ESSENCE",
        "RESPONSE_PROFILE_TAU",
        "MANIFESTATION_M0",
        "EMPIRICAL_DATASET",
        "CALIBRATED_MODEL",
    } <= nodes
    assert "METHOD_POLICY_PI" not in nodes


def test_k_response_change_rebuilds_readiness_and_response_downstream_only():
    active = _synthetic_bundle("A")
    candidate = _semantic_mutation(active, "K_response")

    impact = compare_bundles(active, candidate)
    response = next(
        item
        for item in impact["component_impacts"]
        if item["component_id"] == "K_response"
    )
    nodes = {item["artifact"] for item in impact["downstream_invalidations"]}

    assert response["primary_action"] == "READINESS_REBUILD"
    assert "RESPONSE_READINESS" in nodes
    assert "RESPONSE_PROFILE_TAU" in nodes
    assert "MANIFESTATION_M0" in nodes
    assert "NATAL_ESSENCE" not in nodes
    assert "METHOD_POLICY_PI" not in nodes


def test_multi_component_change_preserves_all_invalidation_triggers():
    active = _synthetic_bundle("A")
    candidate = _semantic_mutation(active, "K_signal")
    candidate = _semantic_mutation(candidate, "K_response")

    impact = compare_bundles(active, candidate)
    m0 = next(
        item
        for item in impact["downstream_invalidations"]
        if item["artifact"] == "MANIFESTATION_M0"
        and item["action"] == "MANIFESTATION_REBUILD"
    )

    assert m0["applicability"] == "IF_PRESENT"
    assert m0["trigger_components"] == ["K_response", "K_signal"]


def test_k_method_change_does_not_invalidate_natal_or_tau():
    active = _synthetic_bundle("A")
    candidate = _semantic_mutation(active, "K_method")

    impact = compare_bundles(active, candidate)
    method = next(
        item
        for item in impact["component_impacts"]
        if item["component_id"] == "K_method"
    )
    nodes = {item["artifact"] for item in impact["downstream_invalidations"]}

    assert method["primary_action"] == "METHOD_REPLAY"
    assert nodes == {"METHOD_POLICY_PI", "EXPERT_METHOD_REPLAY"}


def test_k_manifest_change_does_not_invalidate_upstream_n_or_tau():
    active = _synthetic_bundle("A")
    candidate = _semantic_mutation(active, "K_manifest")

    impact = compare_bundles(active, candidate)
    manifest = next(
        item
        for item in impact["component_impacts"]
        if item["component_id"] == "K_manifest"
    )
    nodes = {item["artifact"] for item in impact["downstream_invalidations"]}

    assert manifest["primary_action"] == "MANIFESTATION_REBUILD"
    assert nodes == {
        "MANIFESTATION_M0",
        "EMPIRICAL_DATASET",
        "CALIBRATED_MODEL",
    }


def test_component_contract_change_requires_migration_and_blocks_promotion():
    active = _synthetic_bundle("A")
    candidate = copy.deepcopy(active)
    candidate["bundle_id"] = "KIB-CONTRACT-CHANGE"
    _component(candidate, "K_response")["contract_version"] = "0.2"

    impact = compare_bundles(active, candidate)
    gate = evaluate_promotion_gate(
        impact,
        candidate_verification={"status": "PASS"},
        validation_results={},
    )

    assert impact["status"] == "BLOCKED"
    assert "MIGRATION_REQUIRED" in impact["direct_actions"]
    assert gate["status"] == "BLOCKED"
    assert "MIGRATION_REQUIRED" in gate["blockers"]


def test_missing_required_validation_blocks_promotion():
    active = _synthetic_bundle("A")
    candidate = _semantic_mutation(active, "K_method")
    impact = compare_bundles(active, candidate)

    gate = evaluate_promotion_gate(
        impact,
        candidate_verification={"status": "PASS"},
        validation_results={},
    )

    assert gate["status"] == "BLOCKED"
    assert gate["required_validations"] == ["METHOD_REPLAY_REGRESSION"]
    assert "VALIDATION_REQUIRED:METHOD_REPLAY_REGRESSION" in gate["blockers"]


def test_complete_required_validation_allows_explicit_promotion():
    active = _synthetic_bundle("A")
    candidate = _semantic_mutation(active, "K_method")
    impact = compare_bundles(active, candidate)

    gate = evaluate_promotion_gate(
        impact,
        candidate_verification={"status": "PASS"},
        validation_results={"METHOD_REPLAY_REGRESSION": "PASS"},
    )

    assert gate["status"] == "PROMOTABLE"
    assert gate["recommendation"] == "EXPLICIT_LOCK_PROMOTION_ALLOWED"
    assert gate["active_lock_mutated"] is False


def test_failed_candidate_verification_blocks_even_no_runtime_effect():
    active = _synthetic_bundle("A")
    candidate = copy.deepcopy(active)
    candidate["bundle_id"] = "KIB-B"

    impact = compare_bundles(active, candidate)
    gate = evaluate_promotion_gate(
        impact,
        candidate_verification={"status": "FAIL"},
        validation_results={},
    )

    assert gate["status"] == "BLOCKED"
    assert "CANDIDATE_BUNDLE_VERIFICATION_FAILED" in gate["blockers"]


def test_new_candidate_artifact_requires_explicit_semantic_contract(tmp_path):
    active = _temp_active_bundle(tmp_path)
    new_path = tmp_path / "inputs" / "new_response.json"
    new_path.write_text('{"new": true}', encoding="utf-8")

    with pytest.raises(KnowledgeImpactError):
        build_candidate_bundle(
            tmp_path,
            active,
            bundle_id="KIB-CANDIDATE",
            source_commit="NEXT",
            component_overrides={
                "K_response": {
                    "artifacts": [
                        {
                            "path": "inputs/new_response.json",
                            "artifact_type": "JSON",
                        }
                    ]
                }
            },
        )


def test_candidate_builder_supports_explicit_versioned_inventory_without_lock_mutation(
    tmp_path,
):
    active = _temp_active_bundle(tmp_path)
    new_path = tmp_path / "inputs" / "response_v2.json"
    new_path.write_text('{"new": 2}', encoding="utf-8")
    lock = tmp_path / "PRODUCT_KNOWLEDGE.lock.json"
    lock.write_text('{"sentinel": true}\n', encoding="utf-8")
    before = lock.read_bytes()

    candidate = build_candidate_bundle(
        tmp_path,
        active,
        bundle_id="KIB-CANDIDATE-V2",
        source_commit="NEXT",
        component_overrides={
            "K_response": {
                "coverage_status": "CANDIDATE_V2",
                "artifacts": [
                    {
                        "path": "inputs/response_v2.json",
                        "artifact_type": "JSON",
                        "semantic_contract": "JSON_CANONICAL_FULL_V0_1",
                    }
                ],
            }
        },
    )
    impact = compare_bundles(active, candidate)

    assert lock.read_bytes() == before
    response = _component(candidate, "K_response")
    assert response["artifacts"][0]["path"] == "inputs/response_v2.json"
    assert (
        next(
            item
            for item in impact["component_impacts"]
            if item["component_id"] == "K_response"
        )["primary_action"]
        == "READINESS_REBUILD"
    )


def test_promotion_gate_does_not_modify_repository_active_lock():
    active = load_bundle(ACTIVE_PATH)
    candidate = load_bundle(CANDIDATE_PATH)
    lock_before = LOCK_PATH.read_bytes()

    impact = compare_bundles(active, candidate)
    verification = verify_bundle(ROOT, candidate)
    evaluate_promotion_gate(
        impact,
        candidate_verification=verification,
        validation_results={},
    )

    assert LOCK_PATH.read_bytes() == lock_before

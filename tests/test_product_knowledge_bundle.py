import json
from pathlib import Path

import pytest

from src.product.knowledge_bundle import (
    KnowledgeLockError,
    KnowledgeLockMismatchError,
    compute_artifact_digest,
    compute_bundle_semantic_digest,
    compute_component_semantic_digest,
    compute_semantic_digest,
    load_bundle,
    load_lock,
    require_artifact_locked,
    validate_bundle_structure,
    verify_active_component_lock,
    verify_active_lock,
    verify_bundle,
)
from src.product.response_corpus_ingestion import build_response_corpus_readiness


ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "product" / "PRODUCT_KNOWLEDGE_BUNDLE_V0_1.json"
LOCK = ROOT / "product" / "PRODUCT_KNOWLEDGE.lock.json"


def _artifact(root, relative, contract="RAW_CONTENT_FULL_V0_1"):
    path = root / relative
    return {
        "path": relative,
        "artifact_type": "JSON",
        "artifact_digest": compute_artifact_digest(path),
        "semantic_contract": contract,
        "semantic_digest": compute_semantic_digest(path, contract),
    }


def _bundle_with_artifact(root, relative):
    response_artifact = _artifact(root, relative)
    components = [
        {
            "component_id": "K_signal",
            "contract_version": "0.1",
            "coverage_status": "EMPTY_TEST",
            "source_commit": "TEST",
            "artifacts": [],
            "component_semantic_digest": compute_component_semantic_digest([]),
        },
        {
            "component_id": "K_response",
            "contract_version": "0.1",
            "coverage_status": "TEST",
            "source_commit": "TEST",
            "artifacts": [response_artifact],
            "component_semantic_digest": compute_component_semantic_digest(
                [response_artifact]
            ),
        },
        {
            "component_id": "K_manifest",
            "contract_version": "0.1",
            "coverage_status": "EMPTY_TEST",
            "source_commit": "TEST",
            "artifacts": [],
            "component_semantic_digest": compute_component_semantic_digest([]),
        },
        {
            "component_id": "K_method",
            "contract_version": "0.1",
            "coverage_status": "EMPTY_TEST",
            "source_commit": "TEST",
            "artifacts": [],
            "component_semantic_digest": compute_component_semantic_digest([]),
        },
    ]
    bundle = {
        "schema_version": "0.1",
        "bundle_id": "KIB-TEST",
        "source_commit": "TEST",
        "components": components,
        "bundle_semantic_digest": compute_bundle_semantic_digest(components),
    }
    validate_bundle_structure(bundle)
    return bundle


def _write_active_lock(root, bundle):
    product_dir = root / "product"
    product_dir.mkdir(parents=True, exist_ok=True)
    bundle_path = product_dir / "PRODUCT_KNOWLEDGE_BUNDLE_V0_1.json"
    bundle_path.write_text(
        json.dumps(bundle, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    lock = {
        "schema_version": "0.1",
        "lock_id": "LOCK-TEST",
        "active_bundle_path": "product/PRODUCT_KNOWLEDGE_BUNDLE_V0_1.json",
        "active_bundle_id": bundle["bundle_id"],
        "bundle_artifact_digest": compute_artifact_digest(bundle_path),
        "bundle_semantic_digest": bundle["bundle_semantic_digest"],
        "source_commit": bundle["source_commit"],
        "auto_refresh": False,
    }
    (product_dir / "PRODUCT_KNOWLEDGE.lock.json").write_text(
        json.dumps(lock, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _two_component_bundle(root):
    signal_path = root / "knowledge" / "signal.json"
    response_path = root / "knowledge" / "response.json"
    signal_path.parent.mkdir(parents=True, exist_ok=True)
    signal_path.write_text('{"signal":"A"}\n', encoding="utf-8")
    response_path.write_text('{"response":"A"}\n', encoding="utf-8")

    signal_artifact = _artifact(root, "knowledge/signal.json")
    response_artifact = _artifact(root, "knowledge/response.json")
    components = [
        {
            "component_id": "K_signal",
            "contract_version": "0.1",
            "coverage_status": "TEST",
            "source_commit": "TEST",
            "artifacts": [signal_artifact],
            "component_semantic_digest": compute_component_semantic_digest(
                [signal_artifact]
            ),
        },
        {
            "component_id": "K_response",
            "contract_version": "0.1",
            "coverage_status": "TEST",
            "source_commit": "TEST",
            "artifacts": [response_artifact],
            "component_semantic_digest": compute_component_semantic_digest(
                [response_artifact]
            ),
        },
        {
            "component_id": "K_manifest",
            "contract_version": "0.1",
            "coverage_status": "EMPTY_TEST",
            "source_commit": "TEST",
            "artifacts": [],
            "component_semantic_digest": compute_component_semantic_digest([]),
        },
        {
            "component_id": "K_method",
            "contract_version": "0.1",
            "coverage_status": "EMPTY_TEST",
            "source_commit": "TEST",
            "artifacts": [],
            "component_semantic_digest": compute_component_semantic_digest([]),
        },
    ]
    bundle = {
        "schema_version": "0.1",
        "bundle_id": "KIB-TWO-COMPONENT-TEST",
        "source_commit": "TEST",
        "components": components,
        "bundle_semantic_digest": compute_bundle_semantic_digest(components),
    }
    _write_active_lock(root, bundle)
    return bundle


def test_repository_active_lock_verifies_exact_inputs():
    report = verify_active_lock(ROOT)

    assert report["status"] == "PASS"
    assert report["lock_id"] == "PRODUCT_KNOWLEDGE_LOCK_V0_1"
    assert report["verified_artifact_count"] == 58
    assert report["findings"] == []


def test_bundle_has_four_separated_knowledge_components():
    bundle = load_bundle(BUNDLE)
    by_id = {item["component_id"]: item for item in bundle["components"]}

    assert set(by_id) == {"K_signal", "K_response", "K_manifest", "K_method"}
    assert len(by_id["K_signal"]["artifacts"]) == 11
    assert len(by_id["K_response"]["artifacts"]) == 19
    assert len(by_id["K_method"]["artifacts"]) == 28
    assert by_id["K_manifest"]["coverage_status"] == "EMPTY_NOT_READY"
    assert by_id["K_manifest"]["artifacts"] == []

    assert by_id["K_signal"]["accepted_baseline_commit"] == (
        "720a617f6f2c9811b788af3e7b0865c1a3096e62"
    )
    assert by_id["K_response"]["accepted_baseline_commit"] == (
        "16bb9b30f491afa27368e88767e5662dbdc54983"
    )
    assert by_id["K_method"]["accepted_baseline_commit"] == (
        "9d3e4d61bc0729693a307c96345820fec798875d"
    )
    for component_id in ("K_signal", "K_response", "K_method"):
        assert by_id[component_id]["bootstrap_equivalence"] == (
            "ALL_LOCKED_ARTIFACT_BLOBS_IDENTICAL_TO_ACCEPTED_BASELINE"
        )


def test_active_lock_never_auto_refreshes():
    lock = load_lock(LOCK)
    bundle = load_bundle(BUNDLE)

    assert lock["auto_refresh"] is False
    assert bundle["auto_refresh"] is False
    assert lock["source_commit"] == bundle["source_commit"]
    assert lock["active_bundle_id"] == bundle["bundle_id"]


def test_locked_byte_mutation_fails_closed(tmp_path):
    path = tmp_path / "knowledge" / "fixture.json"
    path.parent.mkdir(parents=True)
    path.write_text('{"value":1}\n', encoding="utf-8")

    bundle = _bundle_with_artifact(tmp_path, "knowledge/fixture.json")
    assert verify_bundle(tmp_path, bundle)["status"] == "PASS"

    path.write_text('{"value":2}\n', encoding="utf-8")
    report = verify_bundle(tmp_path, bundle)

    assert report["status"] == "FAIL"
    assert {
        finding["code"] for finding in report["findings"]
    } >= {
        "ARTIFACT_DIGEST_MISMATCH",
        "SEMANTIC_DIGEST_MISMATCH",
    }


def test_unrelated_component_drift_does_not_invalidate_stable_component(tmp_path):
    _two_component_bundle(tmp_path)

    assert verify_active_component_lock(tmp_path, "K_signal")["status"] == "PASS"
    assert verify_active_component_lock(tmp_path, "K_response")["status"] == "PASS"

    (tmp_path / "knowledge" / "response.json").write_text(
        '{"response":"CHANGED"}\n',
        encoding="utf-8",
    )

    assert verify_active_lock(tmp_path)["status"] == "FAIL"
    assert verify_active_component_lock(tmp_path, "K_response")["status"] == "FAIL"
    assert verify_active_component_lock(tmp_path, "K_signal")["status"] == "PASS"


def test_semantic_mutation_changes_json_semantic_digest(tmp_path):
    path = tmp_path / "record.json"
    path.write_text(
        json.dumps(
            {
                "record_id": "R1",
                "activation": {"mode": "ANY"},
                "provenance": {"page": 1},
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    before = compute_semantic_digest(path, "JSON_CANONICAL_FULL_V0_1")

    path.write_text(
        json.dumps(
            {
                "record_id": "R1",
                "activation": {"mode": "ALL"},
                "provenance": {"page": 1},
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    after = compute_semantic_digest(path, "JSON_CANONICAL_FULL_V0_1")

    assert before != after


def test_provenance_only_change_can_leave_semantic_digest_stable(tmp_path):
    path = tmp_path / "response.json"
    first = {
        "record_id": "R1",
        "activation": {"mode": "ANY"},
        "execution_status": "LEXICAL_ONLY",
        "provenance": {"source": "A", "page": 1},
    }
    second = {
        **first,
        "provenance": {"source": "A", "page": 2},
    }

    path.write_text(json.dumps(first, ensure_ascii=False), encoding="utf-8")
    artifact_before = compute_artifact_digest(path)
    semantic_before = compute_semantic_digest(
        path,
        "JSON_RESPONSE_SEMANTICS_NO_PROVENANCE_V0_1",
    )

    path.write_text(json.dumps(second, ensure_ascii=False), encoding="utf-8")
    artifact_after = compute_artifact_digest(path)
    semantic_after = compute_semantic_digest(
        path,
        "JSON_RESPONSE_SEMANTICS_NO_PROVENANCE_V0_1",
    )

    assert artifact_before != artifact_after
    assert semantic_before == semantic_after


def test_json_formatting_and_key_order_do_not_change_canonical_semantics(tmp_path):
    path = tmp_path / "ordered.json"
    path.write_text('{"b":2,"a":{"y":2,"x":1}}', encoding="utf-8")
    first = compute_semantic_digest(path, "JSON_CANONICAL_FULL_V0_1")

    path.write_text(
        '{\n  "a": {"x": 1, "y": 2},\n  "b": 2\n}\n',
        encoding="utf-8",
    )
    second = compute_semantic_digest(path, "JSON_CANONICAL_FULL_V0_1")

    assert first == second


def test_unknown_semantic_contract_fails_closed(tmp_path):
    path = tmp_path / "x.json"
    path.write_text("{}", encoding="utf-8")

    with pytest.raises(KnowledgeLockError):
        compute_semantic_digest(path, "UNKNOWN_CONTRACT")


def test_unregistered_in_repository_artifact_is_rejected():
    with pytest.raises(KnowledgeLockMismatchError):
        require_artifact_locked(
            ROOT,
            ROOT / "product" / "PRODUCT_STATE.yaml",
            "K_response",
        )


def test_response_corpus_remains_fail_closed_under_active_lock():
    report = build_response_corpus_readiness()

    assert report["summary"]["source_temporal_candidate_rows"] == 1039
    assert report["summary"]["compiler_ready_kr_records"] == 0
    assert report["now6_gate"]["NOW6_RESPONSE_COMPILER_INPUT_READY"] is False

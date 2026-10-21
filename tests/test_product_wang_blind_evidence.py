import copy
import json
from pathlib import Path

import pytest

from src.product.wang_blind_evidence import (
    EVIDENCE_PATH,
    FORBIDDEN_BLIND_KEYS,
    load_wang_blind_evidence,
    validate_wang_blind_evidence,
    wang_blind_evidence_by_case,
)


ROOT = Path(__file__).resolve().parents[1]

EXPECTED = {
    "WANG-CASE-001": (["天相"], []),
    "WANG-CASE-002": ([], ["太阳", "天梁"]),
    "WANG-CASE-003": (["天同"], []),
    "WANG-CASE-004": (["天机", "太阴"], []),
    "WANG-CASE-005": (["太阳", "太阴"], []),
    "WANG-CASE-006": (["廉贞", "天府"], []),
    "WANG-CASE-007": (["天同", "天梁"], []),
    "WANG-CASE-008": (["天府"], []),
    "WANG-CASE-009": (["紫微", "破军"], []),
    "WANG-CASE-010": ([], ["天机", "巨门"]),
    "WANG-CASE-011": (["太阴"], []),
    "WANG-CASE-012": (["天梁"], []),
    "WANG-CASE-013": (["破军"], []),
    "WANG-CASE-014": (["太阴"], []),
    "WANG-CASE-015": ([], ["天同", "巨门"]),
    "WANG-CASE-016": ([], ["天机", "天梁"]),
    "WANG-CASE-017": ([], ["天同", "太阴"]),
    "WANG-CASE-018": (["破军"], []),
    "WANG-CASE-019": (["贪狼"], []),
    "WANG-CASE-020": (["贪狼"], []),
    "WANG-CASE-021": (["廉贞", "破军"], []),
    "WANG-CASE-022": (["破军"], []),
    "WANG-CASE-023": (["天府"], []),
    "WANG-CASE-024": ([], ["天梁"]),
}


def _load_raw():
    return json.loads(EVIDENCE_PATH.read_text(encoding="utf-8"))


def test_wang_blind_evidence_validates_and_covers_all_24_cases():
    payload = load_wang_blind_evidence()
    assert payload["scope"]["case_count"] == 24
    assert payload["scope"]["materialized_case_count"] == 24
    assert len(payload["cases"]) == 24
    assert list(wang_blind_evidence_by_case()) == list(EXPECTED)


def test_exact_source_reviewed_target_palace_major_star_systems():
    rows = wang_blind_evidence_by_case()
    for case_id, (direct, borrowed) in EXPECTED.items():
        row = rows[case_id]
        assert row["target_palace_main_stars"] == direct
        assert row["borrowed_from_opposite_main_stars"] == borrowed
        assert row["target_palace_empty_main_star"] is (not direct)
        assert row["full_chart_status"] == "NOT_MATERIALIZED"


def test_blind_evidence_contains_no_expert_answer_or_identity_leakage_keys():
    payload = _load_raw()
    serialized = json.dumps(payload, ensure_ascii=False)
    for forbidden in FORBIDDEN_BLIND_KEYS:
        assert f'"{forbidden}"' not in serialized

    for row in payload["cases"]:
        assert "WANG-PERSON-" not in json.dumps(row, ensure_ascii=False)
        assert row["blind_alias"].startswith("WANG-BLIND-")


def test_source_reference_alone_is_not_used_as_materialized_fact_identity():
    payload = load_wang_blind_evidence()
    for row in payload["cases"]:
        assert row["source_chart_span_ref"].startswith("WANG-ANXING-TUIDUAN:")
        assert all(
            ref.startswith(f'MATERIALIZED_FACT:{row["case_id"]}:TARGET_PALACE:')
            for ref in row["fact_refs"]
        )
        assert row["source_chart_span_ref"] not in row["fact_refs"]


def test_historical_lineage_survives_unrelated_k_response_promotion():
    payload = load_wang_blind_evidence()
    lock = json.loads(
        (ROOT / "product" / "PRODUCT_KNOWLEDGE.lock.json").read_text(
            encoding="utf-8"
        )
    )
    historical = json.loads(
        (ROOT / "product" / "PRODUCT_KNOWLEDGE_BUNDLE_V0_2.json").read_text(
            encoding="utf-8"
        )
    )
    active = json.loads(
        (ROOT / lock["active_bundle_path"]).read_text(encoding="utf-8")
    )

    assert payload["lineage"]["product_knowledge_lock_id"] == (
        "PRODUCT_KNOWLEDGE_LOCK_V0_2"
    )
    assert payload["lineage"]["active_product_knowledge_bundle_id"] == (
        historical["bundle_id"]
    )
    assert active["bundle_id"] == "KIB-PRODUCT-20261021-V0_3"
    historical_k_method = next(
        item for item in historical["components"]
        if item["component_id"] == "K_method"
    )
    active_k_method = next(
        item for item in active["components"]
        if item["component_id"] == "K_method"
    )
    assert (
        payload["lineage"]["k_method_component_semantic_digest"]
        == historical_k_method["component_semantic_digest"]
        == active_k_method["component_semantic_digest"]
    )
    assert lock["auto_refresh"] is False


def test_leakage_mutation_is_rejected():
    payload = _load_raw()
    mutated = copy.deepcopy(payload)
    mutated["cases"][0]["source_subject_label"] = "SHOULD_NOT_EXIST"
    with pytest.raises(ValueError, match="forbidden leakage keys"):
        validate_wang_blind_evidence(mutated)


def test_full_chart_overclaim_mutation_is_rejected():
    payload = _load_raw()
    mutated = copy.deepcopy(payload)
    mutated["scope"]["full_chart_materialized"] = True
    with pytest.raises(ValueError, match="full-chart materialization"):
        validate_wang_blind_evidence(mutated)


def test_direct_and_borrowed_system_cannot_be_mixed():
    payload = _load_raw()
    mutated = copy.deepcopy(payload)
    mutated["cases"][0]["borrowed_from_opposite_main_stars"] = ["天梁"]
    with pytest.raises(ValueError, match="cannot both be set"):
        validate_wang_blind_evidence(mutated)

from __future__ import annotations

import csv
import json
from pathlib import Path

from tools.knowledge_core_mapping_review_schema import validate_mapping_review_collection

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "knowledge/core/14star-property-normalization/14STAR_PROPERTY_NORMALIZATION_BASELINE_v0.1.json"
CANONICAL_RULES = ROOT / "knowledge/rules/stars/major_stars_canonical_v0.1.csv"


def load_baseline():
    return json.loads(BASELINE.read_text(encoding="utf-8"))


def test_solar_pilot_is_explicitly_noncanonical_and_source_bounded():
    data = load_baseline()
    assert data["status"] == "PROPOSAL_ONLY_NOT_CANONICAL"
    assert data["checkpoint_status"] == "IN_PROGRESS_STAGE_A_SOLAR_PILOT"
    assert data["progress"]["completed_pilot_cards"] == ["太阳"]
    assert data["progress"]["remaining_pilot_cards"] == ["太阴", "天相"]
    assert data["source_policy"]["source_id"] == "SRC-ZZ-002"
    assert data["source_policy"]["source_sha256"] == (
        "1cd57c205297f78004c0d59db7cb77b05ecad53313757e55d8f1c78600609e9a"
    )
    assert data["method_guardrails"]["candidate_canonicalization_authorized"] is False
    assert data["method_guardrails"]["product_consumption_authorized"] is False
    assert data["method_guardrails"]["normalization_epistemic"] == "UNRESOLVED"
    assert len(data["stars"]) == 1
    assert data["stars"][0]["name"] == "太阳"
    assert data["stars"][0]["status"] == "PILOT_CHECKPOINT_NOT_FINAL"


def test_solar_mapping_review_records_validate_against_accepted_v01_contract():
    data = load_baseline()
    records = data["mapping_review_records"]
    assert len(records) >= 5
    assert validate_mapping_review_collection(records) == []
    ids = [row["review_record_id"] for row in records]
    assert len(ids) == len(set(ids))
    assert {row["mapping_disposition"]["value"] for row in records} >= {
        "supported_candidate", "needs_review", "not_supported_for_target"
    }


def test_source_rows_remain_unresolved_and_are_not_mutated_by_the_pilot():
    data = load_baseline()
    with CANONICAL_RULES.open(encoding="utf-8", newline="") as stream:
        rows = {row["rule_id"]: row for row in csv.DictReader(stream)}
    for rule_id in ("ZZ-TY-002", "ZZ-TY-009", "ZZ-TY-010", "ZZ-TY-016", "ZZ-TY-017", "ZZ-TY-018"):
        assert rows[rule_id]["source_epistemic"] == "EXPLICIT"
        assert rows[rule_id]["normalization_epistemic"] == "UNRESOLVED"
        assert rows[rule_id]["source_span_verified"] == "false"
    assert data["method_guardrails"]["historical_source_review_is_not_a_canonical_rule_mutation"] is True


def test_solar_conditions_duplicate_span_and_projection_are_preserved():
    data = load_baseline()
    solar = data["stars"][0]
    claims = {row["claim_key"]: row for row in solar["source_claims"]}

    temple = claims["TY-CONDITION-009"]
    assert temple["source_rule_ids"] == ["ZZ-TY-009"]
    assert temple["conditions_to_preserve"] == [
        "太阳入庙", "同时会合过多带发射性质的星曜"
    ]

    duplicate = claims["TY-OVEREMISSION-010-X02"]
    assert set(duplicate["source_rule_ids"]) == {"ZZ-TY-010", "ZZ-TY-X02"}
    assert duplicate["independent_source_span_count"] == 1
    assert duplicate["canonical_condition_variants"] == [
        {"rule_id": "ZZ-TY-010", "condition": "发射过度"},
        {"rule_id": "ZZ-TY-X02", "condition": "过多发射星曜"},
    ]

    baseline = claims["TY-L1-BASELINE-EMISSION"]
    projection = claims["TY-L3-SOCIAL-PROMINENCE"]
    assert baseline["source_span_group"] == projection["source_span_group"]
    assert projection["claim_layer"] == "L3_PROJECTION_OR_OUTCOME"
    assert "ZZ-TY-003" not in baseline["source_rule_ids"]


def test_general_moderation_rule_is_not_promoted_to_solar_intrinsic_capacity():
    data = load_baseline()
    moderation = next(
        row for row in data["stars"][0]["source_claims"]
        if row["claim_key"] == "TY-METHOD-018-MODERATION"
    )
    assert moderation["claim_layer"] == "GENERAL_INTERPRETIVE_METHOD"
    record = next(
        row for row in data["mapping_review_records"]
        if row["review_record_id"] == "MR-TY-QI15-METHOD-RULE-005"
    )
    assert record["evidence_role"]["state"] == "UNKNOWN"
    assert record["mapping_disposition"]["value"] == "not_supported_for_target"
    assert record["mapping_disposition"]["state"] == "KNOWN"

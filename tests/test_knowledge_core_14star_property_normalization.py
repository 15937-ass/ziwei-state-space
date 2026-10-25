from __future__ import annotations

import csv
import json
from pathlib import Path

from tools.knowledge_core_mapping_review_schema import validate_mapping_review_collection

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "knowledge/core/14star-property-normalization/14STAR_PROPERTY_NORMALIZATION_BASELINE_v0.1.json"
CANONICAL_RULES = ROOT / "knowledge/rules/stars/major_stars_canonical_v0.1.csv"
TAIYIN_SOURCE_REVIEW = ROOT / "knowledge/core/14star-property-normalization/TAIYIN_SOURCE_SPAN_REVIEW_v0.1.csv"
TIANXIANG_SOURCE_REVIEW = ROOT / "knowledge/core/14star-property-normalization/TIANXIANG_SOURCE_SPAN_REVIEW_v0.1.csv"
TIANJI_SOURCE_REVIEW = ROOT / "knowledge/core/14star-property-normalization/TIANJI_SOURCE_SPAN_REVIEW_v0.1.csv"
WUQU_SOURCE_REVIEW = ROOT / "knowledge/core/14star-property-normalization/WUQU_SOURCE_SPAN_REVIEW_v0.1.csv"
ZIWEI_SOURCE_REVIEW = ROOT / "knowledge/core/14star-property-normalization/ZIWEI_SOURCE_SPAN_REVIEW_v0.1.csv"


def load_baseline():
    return json.loads(BASELINE.read_text(encoding="utf-8"))


def test_solar_taiyin_and_tianxiang_pilots_are_explicitly_noncanonical_and_source_bounded():
    data = load_baseline()
    assert data["status"] == "PROPOSAL_ONLY_NOT_CANONICAL"
    assert data["checkpoint_status"] == "STAGE_B_WUQU_CHECKPOINT_COMPLETED_NOT_FINAL"
    assert data["progress"]["completed_pilot_cards"] == ["太阳", "太阴", "天相"]
    assert data["progress"]["active_pilot_card"] is None
    assert data["progress"]["draft_pilot_cards"] == ["太阳", "太阴", "天相"]
    assert data["progress"]["remaining_pilot_cards"] == []
    assert data["source_policy"]["source_id"] == "SRC-ZZ-002"
    assert data["source_policy"]["source_sha256"] == (
        "1cd57c205297f78004c0d59db7cb77b05ecad53313757e55d8f1c78600609e9a"
    )
    assert data["method_guardrails"]["candidate_canonicalization_authorized"] is False
    assert data["method_guardrails"]["product_consumption_authorized"] is False
    assert data["method_guardrails"]["normalization_epistemic"] == "UNRESOLVED"
    assert len([star for star in data["stars"] if star["name"] in {"太阳", "太阴", "天相"}]) == 3
    assert len(data["stars"]) == 6
    assert data["stars"][5]["name"] == "武曲"
    assert data["stars"][0]["name"] == "太阳"
    assert data["stars"][0]["status"] == "PILOT_CHECKPOINT_COMPLETED_NOT_FINAL"
    assert data["stars"][1]["name"] == "太阴"
    assert data["stars"][1]["status"] == "PILOT_CHECKPOINT_COMPLETED_NOT_FINAL"
    assert data["stars"][2]["name"] == "天相"
    assert data["stars"][2]["status"] == "PILOT_CHECKPOINT_COMPLETED_NOT_FINAL"


def test_solar_mapping_review_records_validate_against_accepted_v01_contract():
    data = load_baseline()
    records = data["mapping_review_records"]
    assert len(records) >= 18
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
    for rule_id in ("ZZ-TY-002", "ZZ-TY-009", "ZZ-TY-010", "ZZ-TY-016", "ZZ-TY-017", "ZZ-TY-018", "ZZ-TYI-001", "ZZ-TYI-002", "ZZ-TYI-005", "ZZ-TYI-006", "ZZ-TYI-007", "ZZ-TYI-008", "ZZ-TYI-009", "ZZ-TYI-X09", "ZZ-TYI-Y01", "ZZ-TYI-Y02", "ZZ-TYI-Y04"):
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



def test_taiyin_baseline_and_condition_branches_are_preserved():
    data = load_baseline()
    taiyin = next(star for star in data["stars"] if star["name"] == "太阴")
    claims = {row["claim_key"]: row for row in taiyin["source_claims"]}

    baseline = claims["TYI-L1-BASELINE-CONVERGENCE"]
    assert baseline["source_rule_ids"] == ["ZZ-TYI-002"]
    assert baseline["candidate_target_ref"] == "QI-01"
    assert baseline["normalization_epistemic"] == "UNRESOLVED"

    optimal = claims["TYI-OPTIMAL-REGION"]
    assert optimal["conditions_to_preserve"] == ["太阴入庙", "太阴吉化", "收敛须适度"]

    overconvergence = claims["TYI-OVERCONVERGENCE-BRANCHES"]
    assert "或会合主潜藏/收敛的星曜" in overconvergence["conditions_to_preserve"]
    assert "替代分支，不静默改成所有条件同时成立" in overconvergence["conditions_to_preserve"]

    changqu = claims["TYI-CHANGQU-PAIRED-GATE"]
    assert set(changqu["source_rule_ids"]) == {"ZZ-TYI-003", "ZZ-TYI-X01", "ZZ-TYI-X02"}
    single = claims["TYI-CHANGQU-SINGLE-RESPONSE"]
    assert set(single["source_rule_ids"]) == {"ZZ-TYI-004", "ZZ-TYI-X03"}

    assert claims["TYI-L3-WEALTH-PROJECTION"]["claim_layer"] == "L3_PROJECTION_OR_OUTCOME"
    assert claims["TYI-CROSS-PALACE-FUDE-DEPENDENCY"]["claim_layer"] == "L2_RELATIONAL_OR_CROSS_PALACE_DEPENDENCY"
    assert claims["TYI-DAYBIRTH-TRADITIONAL-OUTCOMES"]["claim_layer"] == "L3_TRADITIONAL_DOWNSTREAM_OUTCOME_CLAIMS"


def test_taiyin_visual_source_review_does_not_mutate_canonical_source_flags():
    data = load_baseline()
    expected_ids = set(data["source_policy"]["taiyin_review_rule_ids"])
    with TAIYIN_SOURCE_REVIEW.open(encoding="utf-8", newline="") as stream:
        review_rows = {row["rule_id"]: row for row in csv.DictReader(stream)}
    assert len(expected_ids) == 25
    for rule_id in expected_ids:
        row = review_rows[rule_id]
        assert row["star"] == "太阴"
        assert row["source_span_status"] == "VERIFIED_VISUAL_SCAN"
        assert row["proposal_status"] == "PROPOSAL_ONLY_NOT_CANONICAL"
        assert row["normalization_epistemic_after"] == "UNRESOLVED"
        assert row["canonical_source_span_verified_after"] == "false"
        assert row["claim_role"] in {"INTRINSIC", "RELATIONAL", "CONDITIONAL", "UNRESOLVED_OTHER"}
        assert row["proposed_evidence_tier"] in {"DIRECT_STAR", "SAME_STAR_MODIFIER", "SYSTEM_CONTEXT"}

    with CANONICAL_RULES.open(encoding="utf-8", newline="") as stream:
        canonical = {row["rule_id"]: row for row in csv.DictReader(stream)}
    for rule_id in expected_ids:
        assert canonical[rule_id]["source_span_verified"] == "false"
        assert canonical[rule_id]["normalization_epistemic"] == "UNRESOLVED"


def test_tianxiang_source_review_is_bounded_and_canonical_rows_stay_unresolved():
    data = load_baseline()
    expected_ids = set(data["source_policy"]["tianxiang_review_rule_ids"])
    assert len(expected_ids) == 25
    assert data["source_policy"]["tianxiang_out_of_scope_rule_ids"] == ["ZZ-TX-009", "ZZ-TX-010"]

    with TIANXIANG_SOURCE_REVIEW.open(encoding="utf-8", newline="") as stream:
        review_rows = list(csv.DictReader(stream))
    assert len(review_rows) == 25
    assert {row["rule_id"] for row in review_rows} == expected_ids
    assert len({row["rule_id"] for row in review_rows}) == 25

    with CANONICAL_RULES.open(encoding="utf-8", newline="") as stream:
        canonical = {row["rule_id"]: row for row in csv.DictReader(stream)}
    for row in review_rows:
        rule_id = row["rule_id"]
        assert row["star"] == "天相"
        if rule_id in {"ZZ-TX-005", "ZZ-TX-006"}:
            assert row["source_pdf_page"] == "24"
            assert row["source_printed_page"] == "46"
        else:
            assert row["source_pdf_page"] == "13"
        assert row["source_span_status"] == "VERIFIED_VISUAL_SCAN"
        assert row["literal_source_span"].strip()
        assert row["proposal_status"] == "PROPOSAL_ONLY_NOT_CANONICAL"
        assert row["normalization_epistemic_before"] == "UNRESOLVED"
        assert row["normalization_epistemic_after"] == "UNRESOLVED"
        assert row["canonical_source_span_verified_before"] == "false"
        assert row["canonical_source_span_verified_after"] == "false"
        assert row["claim_role"] in {"INTRINSIC", "RELATIONAL", "CONDITIONAL", "UNRESOLVED_OTHER"}
        assert row["proposed_evidence_tier"] in {"DIRECT_STAR", "SAME_STAR_MODIFIER", "SYSTEM_CONTEXT"}
        assert canonical[rule_id]["source_span_verified"] == "false"
        assert canonical[rule_id]["normalization_epistemic"] == "UNRESOLVED"
    assert "ZZ-TX-009" not in expected_ids and "ZZ-TX-010" not in expected_ids
    review_by_id = {row["rule_id"]: row for row in review_rows}
    assert review_by_id["ZZ-TX-X09"]["source_printed_page"] == "25"
    assert review_by_id["ZZ-TX-X10"]["source_printed_page"] == "25"
    assert review_by_id["ZZ-TX-Y03"]["source_printed_page"] == "25"
    assert "是非尤的徵兆" in review_by_id["ZZ-TX-006"]["literal_source_span"]
    assert "是非怨尤" in review_by_id["ZZ-TX-006"]["modality_scope_ambiguity"]


def test_tianxiang_context_and_clamp_branches_are_not_promoted_to_intrinsic_qi02():
    data = load_baseline()
    tianxiang = next(star for star in data["stars"] if star["name"] == "天相")
    claims = {row["claim_key"]: row for row in tianxiang["source_claims"]}
    context = claims["TX-L2-ENVIRONMENT-DEPENDENCE"]
    assert set(context["source_rule_ids"]) == {"ZZ-TX-001", "ZZ-TX-X02"}
    assert context["candidate_target_ref"] == "STAR-TX.contextual_sensitivity"
    softness = claims["TX-CAIYIN-SOFTNESS-INFERENCE"]
    assert "未" in softness["claim_summary"]
    assert softness["row_adjudication_status"].startswith("VISUAL_SOURCE_REVIEWED")
    palace = claims["TX-PALACE-STABILITY-ALTERNATIVES"]
    assert "天府在丑宫或未宫入庙会合（二选一）" in palace["conditions_to_preserve"]
    firebell = claims["TX-FIREBELL-GATE"]
    assert set(firebell["source_rule_ids"]) == {"ZZ-TX-008", "ZZ-TX-Y06"}
    assert all(prop["canonicalization_authorized"] is False and prop["numeric_strength_assigned"] is False for prop in tianxiang["candidate_properties"])


def test_three_star_cross_comparison_is_complete_but_not_canonical_or_product_ready():
    data = load_baseline()
    comparison = data["cross_star_comparison"]
    assert comparison["status"] == "COMPLETED_RESEARCH_COMPARISON_METHOD_ACCEPTED_NOT_CANONICAL"
    assert comparison["scope"] == ["太阳", "太阴", "天相"]
    axes = {row["axis_id"]: row for row in comparison["comparison_axes"]}
    assert {
        "L0_STRUCTURE_METADATA",
        "L1_INTRINSIC_BASELINE_CANDIDATES",
        "CONDITIONS_AND_STATE_CHANGE",
        "L2_RELATIONSHIP_AND_CONTEXT",
        "L3_PROJECTION_OR_OUTCOME",
        "PROVENANCE_AND_EPISTEMIC_BOUNDARY",
    } <= set(axes)
    assert comparison["method_adequacy"]["accepted_v01_mapping_review_schema_sufficient_for_pilot_record_shape"] is True
    assert comparison["method_adequacy"]["shared_schema_extension_required_for_this_pilot"] is False
    assert comparison["method_adequacy"]["manual_semantic_review_required"] is True
    assert comparison["pi_method_decision_required_before_expansion"] is False
    assert comparison["pi_method_decision"]["context_check_passed"] is True
    assert comparison["pi_method_decision"]["canonical_mapping_approved"] is False
    assert comparison["pi_method_recommendation"] == "ACCEPT_METHOD_FOR_STAGE_B_WITHOUT_CANONICALIZATION"
    assert data["method_guardrails"]["candidate_canonicalization_authorized"] is False
    assert data["method_guardrails"]["product_consumption_authorized"] is False
    assert data["pilot_checkpoint_validation"]["run_id"] == 40169844516
    assert data["pilot_checkpoint_validation"]["conclusion"] == "success"


def test_context_audit_refs_existing_source_claims_without_growing_canonical_evidence():
    data = load_baseline()
    audit = data["context_method_audit"]
    claims = {claim["claim_key"]: claim for star in data["stars"] for claim in star["source_claims"]}
    assert audit["scope"]["source_sha256"] == data["source_policy"]["source_sha256"]
    assert audit["scope"]["visual_rechecked_scan_pages"] == [5, 10, 13, 24]
    ids = [row["audit_id"] for row in audit["records"]]
    assert len(ids) == len(set(ids))
    for row in audit["records"]:
        cited_rules = set()
        for key in row["source_claim_keys"]:
            cited_rules.update(claims[key]["source_rule_ids"])
        assert set(row["source_rule_ids"]) <= cited_rules
        assert row["source_locator"]["source_id"] == "SRC-ZZ-002"
        assert row["normalization_epistemic"] == "UNRESOLVED"
        assert row["canonical_accepted"] is row["executable"] is False
    assert len(data["mapping_review_records"]) == 84
    assert sum(not record["review_record_id"].startswith(("MR-TJ-", "MR-WQ-")) for record in data["mapping_review_records"]) == 50
    assert sum(record["review_record_id"].startswith("MR-TJ-") for record in data["mapping_review_records"]) == 17
    assert sum(record["review_record_id"].startswith("MR-WQ-") for record in data["mapping_review_records"]) == 17
    assert validate_mapping_review_collection(data["mapping_review_records"]) == []
    assert all("context_method_audit" not in record for record in data["mapping_review_records"])


def test_source_explicit_outer_or_does_not_resolve_the_inner_taiyin_group():
    data = load_baseline()
    audit = data["context_method_audit"]
    row = next(row for row in audit["records"] if row["audit_id"] == "CTX-TYI-01")
    expression = row["condition_expression_research_only"]
    assert expression["outer_connective"] == "SOURCE_EXPLICIT_OR"
    assert expression["branches"][0] == {
        "literal_group": "太阴落陷、化忌之时",
        "group_internal_connective": "UNRESOLVED",
    }
    taiyin = next(star for star in data["stars"] if star["name"] == "太阴")
    claim = next(c for c in taiyin["source_claims"] if c["claim_key"] == "TYI-OVERCONVERGENCE-BRANCHES")
    assert claim["conditions_to_preserve"][0] == "太阴落陷、化忌之时（组内连接关系未决）"
    assert "太阴落陷或化忌" not in claim["conditions_to_preserve"]
    gaps = {gap["id"]: gap for gap in audit["retained_source_ambiguities"]}
    assert gaps["CTX-GAP-TYI-INNER-CONNECTIVE"]["state"] == "UNRESOLVED"


def test_context_subjects_and_scoped_negation_cannot_be_flattened_into_star_traits():
    audit = load_baseline()["context_method_audit"]
    rows = {row["audit_id"]: row for row in audit["records"]}
    sun = rows["CTX-TY-01"]["condition_expression_research_only"]
    assert sun["outer_connective"] == "AND"
    assert sun["operands"] == ["太阳入庙", "过多带发射性质的星曜会合"]
    compensation = rows["CTX-TYI-02"]["condition_expression_research_only"]
    assert compensation["operands"][1] == {"subject": "太阳", "source_explicit_or": ["入庙", "化禄"]}
    relief = rows["CTX-TX-02"]["condition_expression_research_only"]
    assert relief["outer_connective"] == "AND"
    assert relief["negation_completeness_contract"] == "NOT_ESTABLISHED"
    assert relief["positive_group_internal_quantifier"] == "UNRESOLVED_FOR_RUNTIME"
    palace = rows["CTX-TX-03"]["condition_expression_research_only"]
    assert palace["alternative_subject"] == "天府"
    assert palace["source_explicit_or"] == ["丑", "未"]
    assert palace["brightness_subjects"] == ["天梁", "天府"]
    assert rows["CTX-TX-01"]["condition_expression_research_only"]["L2_assignment"] == "NOT_AUTOMATIC"


def test_branch_groups_and_element_labels_do_not_create_unproved_effect_rules():
    audit = load_baseline()["context_method_audit"]
    rows = {row["audit_id"]: row for row in audit["records"]}
    groups = rows["CTX-TYI-03"]["condition_expression_research_only"]
    assert groups["source_groups"][0] == {"branches": ["子", "午", "卯", "酉"], "system_literal": "同阴"}
    assert groups["generic_growth_stage_effect"] == "NOT_ESTABLISHED_IN_REVIEWED_CLAIMS"
    substrate = rows["CTX-L0-01"]["condition_expression_research_only"]
    assert substrate["five_element_effect_derivation"] == "NOT_ESTABLISHED"
    assert substrate["compound_labels"] == ["廉贞:木火", "巨门:土/金"]
    assert audit["runtime_contract_complete"] is False


def test_method_permission_and_progress_metadata_remain_consistent():
    data = load_baseline()
    audit = data["context_method_audit"]
    assert audit["authorization"]["stage_b_authorized_after_exit_conditions"] is True
    assert audit["authorization"]["canonicalization_authorized"] is False
    assert audit["authorization"]["product_consumption_authorized"] is False
    assert audit["research_disposition"] == "CONTINUE_STAGE_B_CANDIDATE_RESEARCH_NEXT_BOUNDED_TURN"
    assert audit["next_star"] == "紫微"  # Historical method-exit handoff; this star has now been researched.
    assert data["progress"]["completed_expansion_stars"] == ["紫微", "天机", "武曲"]
    assert data["progress"]["remaining_expansion_stars_in_existing_order"][0] == "天同"
    assert len(data["stars"]) == 6 and len(data["progress"]["remaining_expansion_stars_in_existing_order"]) == 8
    assert audit["exit_conditions"]["shared_schema_extension_required_for_current_research_records"] is False
    assert audit["exit_conditions"]["canonical_artifacts_changed"] is False


def test_ziwei_stage_b_candidate_card_preserves_role_context_conditions_and_time():
    data = load_baseline()
    ziwei = next(star for star in data["stars"] if star["name"] == "紫微")
    assert data["checkpoint_status"] == "STAGE_B_WUQU_CHECKPOINT_COMPLETED_NOT_FINAL"
    assert data["progress"]["stage"] == "B_WUQU_CHECKPOINT_COMPLETED_READY_FOR_TONG"
    assert ziwei["status"] == "STAGE_B_CHECKPOINT_COMPLETED_NOT_FINAL"
    assert len(ziwei["source_claims"]) >= 15
    assert len(ziwei["candidate_properties"]) == 5
    assert all(item["canonicalization_authorized"] is False for item in ziwei["candidate_properties"])
    assert all(item["numeric_strength_assigned"] is False for item in ziwei["candidate_properties"])
    assert not any(item["target_ref"].startswith("STAR-ZW.intrinsic_signature:QI-") for item in ziwei["candidate_properties"])
    claims = {row["claim_key"]: row for row in ziwei["source_claims"]}
    assert "帝座" in claims["ZW-L1-ROLE-METAPHOR"]["source_excerpt"]
    assert "同度" in claims["ZW-L2-CONTEXT-DEPENDENCE"]["source_excerpt"]
    gate = claims["ZW-INYE-STATE-GATE"]
    assert "入朝且无百官朝拱：尚可" in gate["conditions_to_preserve"]
    assert "落陷且无百官朝拱：在野孤君" in gate["conditions_to_preserve"]
    branches = claims["ZW-INYE-SHAJI-BRANCHES"]["conditions_to_preserve"]
    assert any("见空曜" in item for item in branches)
    assert any("不见空曜" in item for item in branches)
    assert claims["ZW-TEMPORAL-ROLE"]["claim_layer"] == "TEMPORAL_REACTION_OR_PROJECTION"
    assert claims["ZW-GENERAL-NONCANCELLATION"]["claim_layer"] == "GENERAL_INTERPRETIVE_METHOD"
    records = {row["review_record_id"]: row for row in data["mapping_review_records"]}
    assert records["MR-ZW-QR02-ROLE-002"]["mapping_disposition"]["value"] == "supported_candidate"
    assert records["MR-ZW-QI08-INTRINSIC-004"]["mapping_disposition"]["value"] == "not_supported_for_target"
    assert records["MR-ZW-QR01-INTRINSIC-006"]["mapping_disposition"]["value"] == "not_supported_for_target"
    assert records["MR-ZW-QR01-CONDITIONAL-007"]["mapping_disposition"]["value"] == "supported_candidate"
    assert records["MR-ZW-QI07-MODIFIER-008"]["mapping_disposition"]["value"] == "needs_review"
    assert validate_mapping_review_collection(data["mapping_review_records"]) == []


def test_ziwei_visual_review_covers_exact_canonical_rows_without_mutating_them():
    data = load_baseline()
    expected_ids = set(data["source_policy"]["ziwei_review_rule_ids"])
    assert len(expected_ids) == 43
    with CANONICAL_RULES.open(encoding="utf-8", newline="") as stream:
        canonical = {row["rule_id"]: row for row in csv.DictReader(stream) if row["rule_id"].startswith("ZZ-ZW")}
    with ZIWEI_SOURCE_REVIEW.open(encoding="utf-8", newline="") as stream:
        review_rows = list(csv.DictReader(stream))
    assert len(review_rows) == 43
    assert {row["rule_id"] for row in review_rows} == expected_ids == set(canonical)
    assert len({row["rule_id"] for row in review_rows}) == len(review_rows)
    for row in review_rows:
        assert row["source_id"] == "SRC-ZZ-002"
        assert row["source_pdf_page"] == "3"
        assert row["source_printed_page"] in {"5", "6", "5-6"}
        assert row["source_span_status"] == "VERIFIED_VISUAL_SCAN"
        assert row["proposal_status"] == "PROPOSAL_ONLY_NOT_CANONICAL"
        assert row["normalization_epistemic_after"] == "UNRESOLVED"
        assert row["canonical_source_span_verified_after"] == "false"
        assert row["claim_role"] in {"INTRINSIC", "RELATIONAL", "CONDITIONAL", "UNRESOLVED_OTHER"}
        assert row["proposed_evidence_tier"] in {"DIRECT_STAR", "SAME_STAR_MODIFIER", "SYSTEM_CONTEXT"}
        assert canonical[row["rule_id"]]["source_span_verified"] == "false"
        assert canonical[row["rule_id"]]["normalization_epistemic"] == "UNRESOLVED"
    assert data["source_policy"]["ziwei_source_locator"]["source_sha256"] == data["source_policy"]["source_sha256"]
    assert data["source_policy"]["ziwei_source_locator"]["canonical_source_span_verified_mutated"] is False



def test_tianji_stage_b_candidate_card_preserves_context_time_and_conditional_branches():
    data = load_baseline()
    tianji = next(star for star in data["stars"] if star["name"] == "天机")
    assert data["checkpoint_status"] == "STAGE_B_WUQU_CHECKPOINT_COMPLETED_NOT_FINAL"
    assert data["progress"]["stage"] == "B_WUQU_CHECKPOINT_COMPLETED_READY_FOR_TONG"
    assert tianji["status"] == "STAGE_B_CHECKPOINT_COMPLETED_NOT_FINAL"
    assert len(tianji["source_claims"]) >= 14
    assert len(tianji["candidate_properties"]) >= 8
    assert all(item["canonicalization_authorized"] is False for item in tianji["candidate_properties"])
    assert all(item["numeric_strength_assigned"] is False for item in tianji["candidate_properties"])
    claims = {row["claim_key"]: row for row in tianji["source_claims"]}
    assert "阴木" in claims["TJ-L0-SUBSTRATE"]["source_excerpt"]
    assert "谋士或军师" in claims["TJ-STRATEGIC-ROLE-METAPHOR"]["source_excerpt"]
    assert "文昌文曲" in claims["TJ-COGNITIVE-SUPPORT-GATE"]["source_excerpt"]
    assert any("昌曲" in condition for condition in claims["TJ-COGNITIVE-SUPPORT-GATE"]["conditions_to_preserve"])
    assert claims["TJ-TEMPORAL-NATAL-VS-LUCK"]["claim_layer"] == "TEMPORAL_REACTION_OR_SCOPE"
    assert "本命" in claims["TJ-TEMPORAL-NATAL-VS-LUCK"]["conditions_to_preserve"][0]
    assert "天阙" in claims["TJ-TIANQUE-RELATIONAL-GATE"]["source_excerpt"]
    assert "同度" in claims["TJ-SYSTEM-FAMILY-STRUCTURE"]["conditions_to_preserve"][0]
    records = {row["review_record_id"]: row for row in data["mapping_review_records"]}
    assert records["MR-TJ-QI07-BASELINE-002"]["mapping_disposition"]["value"] == "needs_review"
    assert records["MR-TJ-CONTEXT-DEPENDENCE-003"]["mapping_disposition"]["value"] == "supported_candidate"
    assert records["MR-TJ-TIME-SEPARATION-008"]["mapping_disposition"]["value"] == "not_supported_for_target"
    assert records["MR-TJ-QI08-HUAQUAN-010"]["mapping_disposition"]["value"] == "not_supported_for_target"
    assert validate_mapping_review_collection(data["mapping_review_records"]) == []


def test_tianji_visual_review_covers_exact_canonical_rows_without_mutating_them():
    data = load_baseline()
    expected_ids = set(data["source_policy"]["tianji_review_rule_ids"])
    assert len(expected_ids) == 39
    with CANONICAL_RULES.open(encoding="utf-8", newline="") as stream:
        canonical = {row["rule_id"]: row for row in csv.DictReader(stream) if row["rule_id"].startswith("ZZ-TJ")}
    with TIANJI_SOURCE_REVIEW.open(encoding="utf-8", newline="") as stream:
        review_rows = list(csv.DictReader(stream))
    assert len(review_rows) == 39
    assert {row["rule_id"] for row in review_rows} == expected_ids == set(canonical)
    assert len({row["rule_id"] for row in review_rows}) == len(review_rows)
    for row in review_rows:
        assert row["source_id"] == "SRC-ZZ-002"
        assert row["source_pdf_page"] == "4"
        assert row["source_printed_page"] in {"7", "8", "7-8"}
        assert row["source_span_status"] == "VERIFIED_VISUAL_SCAN"
        assert row["proposal_status"] == "PROPOSAL_ONLY_NOT_CANONICAL"
        assert row["normalization_epistemic_after"] == "UNRESOLVED"
        assert row["canonical_source_span_verified_after"] == "false"
        assert row["claim_role"] in {"INTRINSIC", "RELATIONAL", "CONDITIONAL", "UNRESOLVED_OTHER"}
        assert row["proposed_evidence_tier"] in {"DIRECT_STAR", "SAME_STAR_MODIFIER", "SYSTEM_CONTEXT"}
        assert canonical[row["rule_id"]]["source_span_verified"] == "false"
        assert canonical[row["rule_id"]]["normalization_epistemic"] == "UNRESOLVED"
    assert data["source_policy"]["tianji_source_locator"]["source_sha256"] == data["source_policy"]["source_sha256"]
    assert data["source_policy"]["tianji_source_locator"]["canonical_source_span_verified_mutated"] is False


def test_tianji_source_review_literals_are_transcribed_from_the_visual_source():
    with TIANJI_SOURCE_REVIEW.open(encoding="utf-8", newline="") as stream:
        rows = {row["rule_id"]: row for row in csv.DictReader(stream)}
    assert rows["ZZ-TJ-001"]["literal_source_span"] == "天机为南斗第一星，属阴木。"
    assert rows["ZZ-TJ-002"]["literal_source_span"].startswith("但却需要带聪明才艺性质的星曜会合。")
    assert rows["ZZ-TJ-018"]["literal_source_span"] == "流年或大运遇天机，与本命遇天机不同"
    assert rows["ZZ-TJ-025"]["literal_source_span"] == "空动令人的变动易流为空想；"
    assert rows["ZZ-TJ-X07"]["literal_source_span"].startswith("在十二星系中，天机永远与太阴、巨门、天梁同宫或相对")
    assert rows["ZZ-TJ-X08"]["literal_source_span"] == "一般情形下，最喜卯宫的天机巨门。"
    assert rows["ZZ-TJ-X09"]["literal_source_span"] == "于天机独坐的情形下，较不喜巳亥二宫。"
    assert rows["ZZ-TJ-Y05"]["literal_source_span"].startswith("在子午两宫，天机巨门相对；在卯酉两宫，[天机巨门]同度。")


def test_wuqu_stage_b_candidate_card_preserves_comparison_palace_gates_and_interactions():
    data = load_baseline()
    wuqu = next(star for star in data["stars"] if star["name"] == "武曲")
    assert data["checkpoint_status"] == "STAGE_B_WUQU_CHECKPOINT_COMPLETED_NOT_FINAL"
    assert data["progress"]["stage"] == "B_WUQU_CHECKPOINT_COMPLETED_READY_FOR_TONG"
    assert wuqu["status"] == "STAGE_B_CHECKPOINT_COMPLETED_NOT_FINAL"
    assert len(wuqu["source_claims"]) == 15
    assert len(wuqu["candidate_properties"]) >= 10
    assert all(item["canonicalization_authorized"] is False for item in wuqu["candidate_properties"])
    assert all(item["numeric_strength_assigned"] is False for item in wuqu["candidate_properties"])
    claims = {row["claim_key"]: row for row in wuqu["source_claims"]}
    assert "阴金" in claims["WQ-L0-SUBSTRATE"]["source_excerpt"]
    assert "太阴" in claims["WQ-FINANCIAL-QUALITY-ACTION"]["source_excerpt"]
    assert "非常之具体" in claims["WQ-FINANCIAL-QUALITY-ACTION"]["source_excerpt"]
    assert "宫垣" in claims["WQ-KINSHIP-PALACE-GATE"]["claim_summary"]
    assert "不一定代表事业失败" in claims["WQ-HUAJI-YANGTUO-INVESTMENT"]["source_excerpt"]
    assert "优柔寡断" in claims["WQ-CHANGQU-TRADEOFF"]["source_excerpt"]
    assert "躁决" in claims["WQ-WUPO-INTERACTION"]["source_excerpt"]
    records = {row["review_record_id"]: row for row in data["mapping_review_records"]}
    assert records["MR-WQ-QI05-ACTION-003"]["mapping_disposition"]["value"] == "supported_candidate"
    assert records["MR-WQ-QI02-RIGIDITY-005"]["mapping_disposition"]["value"] == "needs_review"
    assert records["MR-WQ-TIME-TRANSFORMATIONS-016"]["mapping_disposition"]["value"] == "not_supported_for_target"
    assert validate_mapping_review_collection(data["mapping_review_records"]) == []


def test_wuqu_visual_review_covers_exact_canonical_rows_without_mutating_them():
    data = load_baseline()
    expected_ids = set(data["source_policy"]["wuqu_review_rule_ids"])
    assert len(expected_ids) == 41
    with CANONICAL_RULES.open(encoding="utf-8", newline="") as stream:
        canonical = {row["rule_id"]: row for row in csv.DictReader(stream) if row["rule_id"].startswith("ZZ-WQ-")}
    with WUQU_SOURCE_REVIEW.open(encoding="utf-8", newline="") as stream:
        review_rows = list(csv.DictReader(stream))
    assert len(review_rows) == 41
    assert {row["rule_id"] for row in review_rows} == expected_ids == set(canonical)
    assert len({row["rule_id"] for row in review_rows}) == len(review_rows)
    for row in review_rows:
        assert row["source_id"] == "SRC-ZZ-002"
        assert row["source_pdf_page"] == "6"
        assert row["source_printed_page"] in {"11", "12"}
        assert row["source_span_status"] == "VERIFIED_VISUAL_SCAN"
        assert row["proposal_status"] == "PROPOSAL_ONLY_NOT_CANONICAL"
        assert row["normalization_epistemic_after"] == "UNRESOLVED"
        assert row["canonical_source_span_verified_after"] == "false"
        assert row["claim_role"] in {"INTRINSIC", "RELATIONAL", "CONDITIONAL", "UNRESOLVED_OTHER"}
        assert row["proposed_evidence_tier"] in {"DIRECT_STAR", "SAME_STAR_MODIFIER", "SYSTEM_CONTEXT"}
        assert canonical[row["rule_id"]]["source_span_verified"] == "false"
        assert canonical[row["rule_id"]]["normalization_epistemic"] == "UNRESOLVED"
    assert data["source_policy"]["wuqu_source_locator"]["source_sha256"] == data["source_policy"]["source_sha256"]
    assert data["source_policy"]["wuqu_source_locator"]["canonical_source_span_verified_mutated"] is False


def test_wuqu_source_review_literals_preserve_exact_text_and_context_boundaries():
    with WUQU_SOURCE_REVIEW.open(encoding="utf-8", newline="") as stream:
        rows = {row["rule_id"]: row for row in csv.DictReader(stream)}
    assert rows["ZZ-WQ-001"]["literal_source_span"] == "武曲为北斗第六星，属阴金。"
    assert rows["ZZ-WQ-005"]["literal_source_span"] == "因此二者比较，太阴就显得柔和，武曲则显得刚烈。"
    assert "武曲性刚，所以不宜再见火铃同度" not in rows["ZZ-WQ-005"]["literal_source_span"]
    assert rows["ZZ-WQ-009"]["literal_source_span"] == rows["ZZ-WQ-010"]["literal_source_span"]
    assert rows["ZZ-WQ-015"]["literal_source_span"] == rows["ZZ-WQ-017"]["literal_source_span"]
    assert "不一定代表事业失败" in rows["ZZ-WQ-X04"]["literal_source_span"]
    assert rows["ZZ-WQ-X11"]["source_printed_page"] == "12"
    assert "文昌、文曲" in rows["ZZ-WQ-X06"]["literal_source_span"]
    assert "躁决" in rows["ZZ-WQ-024"]["literal_source_span"]

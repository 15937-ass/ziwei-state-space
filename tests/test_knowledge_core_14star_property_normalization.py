from __future__ import annotations

import csv
import json
import re
from pathlib import Path

from tools.knowledge_core_mapping_review_schema import validate_mapping_review_collection

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "knowledge/core/14star-property-normalization/14STAR_PROPERTY_NORMALIZATION_BASELINE_v0.1.json"
CANONICAL_RULES = ROOT / "knowledge/rules/stars/major_stars_canonical_v0.1.csv"
TAIYIN_SOURCE_REVIEW = ROOT / "knowledge/core/14star-property-normalization/TAIYIN_SOURCE_SPAN_REVIEW_v0.1.csv"
SUN_SOURCE_REVIEW = ROOT / "knowledge/core/14star-property-normalization/SUN_SOURCE_SPAN_REVIEW_v0.1.csv"
TIANXIANG_SOURCE_REVIEW = ROOT / "knowledge/core/14star-property-normalization/TIANXIANG_SOURCE_SPAN_REVIEW_v0.1.csv"
TIANJI_SOURCE_REVIEW = ROOT / "knowledge/core/14star-property-normalization/TIANJI_SOURCE_SPAN_REVIEW_v0.1.csv"
WUQU_SOURCE_REVIEW = ROOT / "knowledge/core/14star-property-normalization/WUQU_SOURCE_SPAN_REVIEW_v0.1.csv"
TIANTONG_SOURCE_REVIEW = ROOT / "knowledge/core/14star-property-normalization/TIANTONG_SOURCE_SPAN_REVIEW_v0.1.csv"
ZIWEI_SOURCE_REVIEW = ROOT / "knowledge/core/14star-property-normalization/ZIWEI_SOURCE_SPAN_REVIEW_v0.1.csv"
LIANZHEN_SOURCE_REVIEW = ROOT / "knowledge/core/14star-property-normalization/LIANZHEN_SOURCE_SPAN_REVIEW_v0.1.csv"
TIANFU_SOURCE_REVIEW = ROOT / "knowledge/core/14star-property-normalization/TIANFU_SOURCE_SPAN_REVIEW_v0.1.csv"
TANLANG_SOURCE_REVIEW = ROOT / "knowledge/core/14star-property-normalization/TANLANG_SOURCE_SPAN_REVIEW_v0.1.csv"
JUMEN_SOURCE_REVIEW = ROOT / "knowledge/core/14star-property-normalization/JUMEN_SOURCE_SPAN_REVIEW_v0.1.csv"
QISHA_SOURCE_REVIEW = ROOT / "knowledge/core/14star-property-normalization/QISHA_SOURCE_SPAN_REVIEW_v0.1.csv"
POJUN_SOURCE_REVIEW = ROOT / "knowledge/core/14star-property-normalization/POJUN_SOURCE_SPAN_REVIEW_v0.1.csv"
TIANLIANG_SOURCE_REVIEW = ROOT / "knowledge/core/14star-property-normalization/TIANLIANG_SOURCE_SPAN_REVIEW_v0.1.csv"


def load_baseline():
    return json.loads(BASELINE.read_text(encoding="utf-8"))


def test_solar_taiyin_and_tianxiang_pilots_are_explicitly_noncanonical_and_source_bounded():
    data = load_baseline()
    assert data["status"] == "PROPOSAL_ONLY_NOT_CANONICAL"
    assert data["checkpoint_status"] == "STAGE_B_POJUN_CHECKPOINT_COMPLETED_NOT_FINAL"
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
    assert len(data["stars"]) == 14
    assert data["stars"][5]["name"] == "武曲"
    assert data["stars"][6]["name"] == "天同"
    assert data["stars"][7]["name"] == "廉贞"
    assert data["stars"][8]["name"] == "天府"
    assert data["stars"][9]["name"] == "贪狼"
    assert data["stars"][10]["name"] == "巨门"
    assert data["progress"]["stage"] == "B_POJUN_CHECKPOINT_COMPLETED_READY_FOR_FINAL_REVIEW"
    assert data["progress"]["remaining_expansion_stars_in_existing_order"] == []
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
    assert record["evidence_role"]["state"] == "NOT_APPLICABLE"
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
    assert len(expected_ids) == 26
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
    assert review_rows["ZZ-TYI-010"]["source_pdf_page"] == "21"
    assert review_rows["ZZ-TYI-010"]["source_printed_page"] == "41"
    assert "一页定位差异" in review_rows["ZZ-TYI-010"]["modality_scope_ambiguity"]
    for rule_id in expected_ids:
        assert canonical[rule_id]["source_span_verified"] == "false"
        assert canonical[rule_id]["normalization_epistemic"] == "UNRESOLVED"


def test_tianxiang_source_review_is_bounded_and_canonical_rows_stay_unresolved():
    data = load_baseline()
    expected_ids = set(data["source_policy"]["tianxiang_review_rule_ids"])
    assert len(expected_ids) == 27
    assert data["source_policy"]["tianxiang_out_of_scope_rule_ids"] == []

    with TIANXIANG_SOURCE_REVIEW.open(encoding="utf-8", newline="") as stream:
        review_rows = list(csv.DictReader(stream))
    assert len(review_rows) == 27
    assert {row["rule_id"] for row in review_rows} == expected_ids
    assert len({row["rule_id"] for row in review_rows}) == 27

    with CANONICAL_RULES.open(encoding="utf-8", newline="") as stream:
        canonical = {row["rule_id"]: row for row in csv.DictReader(stream)}
    for row in review_rows:
        rule_id = row["rule_id"]
        assert row["star"] == "天相"
        if rule_id in {"ZZ-TX-005", "ZZ-TX-006"}:
            assert row["source_pdf_page"] == "24"
            assert row["source_printed_page"] == "46"
        elif rule_id in {"ZZ-TX-009", "ZZ-TX-010"}:
            assert row["source_pdf_page"] == "24"
            assert row["source_printed_page"] == "47"
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
    assert "ZZ-TX-009" in expected_ids and "ZZ-TX-010" in expected_ids
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
        assert row["source_locator"]["source_id"] in {"SRC-ZZ-001", "SRC-ZZ-002"}
        assert row["normalization_epistemic"] == "UNRESOLVED"
        assert row["canonical_accepted"] is row["executable"] is False
    expected_prefix_counts = {
        "MR-TY-": 5,
        "MR-TYI-": 14,
        "MR-TX-": 19,
        "MR-ZW-": 12,
        "MR-TJ-": 17,
        "MR-WQ-": 18,
        "MR-TT-": 18,
        "MR-LZ-": 20,
        "MR-TF-": 18,
        "MR-TL-": 20,
        "MR-JM-": 20,
        "MR-TLIA-": 20,
        "MR-QS-": 20,
        "MR-PJ-": 20,
    }
    actual_prefix_counts = {
        prefix: sum(
            record["review_record_id"].startswith(prefix)
            for record in data["mapping_review_records"]
        )
        for prefix in expected_prefix_counts
    }
    assert actual_prefix_counts == expected_prefix_counts
    assert len(data["mapping_review_records"]) == sum(expected_prefix_counts.values())
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
    progress = data["progress"]
    assert progress["completed_expansion_stars"] == ["紫微", "天机", "武曲", "天同", "廉贞", "天府", "贪狼", "巨门", "天梁", "七杀", "破军"]
    assert progress["remaining_expansion_stars_in_existing_order"] == []
    # Current progress must reconcile with the cards and historical checkpoints.
    card_names = [star["name"] for star in data["stars"]]
    completed = progress["completed_pilot_cards"] + progress["completed_expansion_stars"]
    remaining = progress["remaining_expansion_stars_in_existing_order"]
    assert card_names == completed
    assert len(card_names) == len(set(card_names)) == 14
    assert len(remaining) == len(set(remaining)) == 0
    assert set(completed).isdisjoint(remaining)
    assert len(set(completed + remaining)) == 14
    history = progress["expansion_checkpoint_history"]
    assert [entry["star"] for entry in history] == progress["completed_expansion_stars"]
    assert history[-1]["next_star"] is None if not remaining else history[-1]["next_star"] == remaining[0]
    assert progress["active_expansion_star"] is None
    assert progress["draft_expansion_stars"] == progress["completed_expansion_stars"]
    assert audit["exit_conditions"]["shared_schema_extension_required_for_current_research_records"] is False
    assert audit["exit_conditions"]["canonical_artifacts_changed"] is False


def test_ziwei_stage_b_candidate_card_preserves_role_context_conditions_and_time():
    data = load_baseline()
    ziwei = next(star for star in data["stars"] if star["name"] == "紫微")
    assert "紫微" in data["progress"]["completed_expansion_stars"]
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
    assert "天机" in data["progress"]["completed_expansion_stars"]
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
    assert "武曲" in data["progress"]["completed_expansion_stars"]
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


def test_tiantong_source_review_covers_all_canonical_rows_and_preserves_quarantine():
    data = load_baseline()
    expected_ids = set(data["source_policy"]["tiantong_review_rule_ids"])
    assert len(expected_ids) == 25
    with TIANTONG_SOURCE_REVIEW.open(encoding="utf-8", newline="") as stream:
        review_rows = list(csv.DictReader(stream))
    assert len(review_rows) == 25
    assert {row["rule_id"] for row in review_rows} == expected_ids
    with CANONICAL_RULES.open(encoding="utf-8", newline="") as stream:
        canonical = {row["rule_id"]: row for row in csv.DictReader(stream)}
    for row in review_rows:
        assert row["star"] == "天同"
        assert row["proposal_status"] == "PROPOSAL_ONLY_NOT_CANONICAL"
        assert row["normalization_epistemic_before"] == row["normalization_epistemic_after"] == "UNRESOLVED"
        assert row["canonical_source_span_verified_before"] == row["canonical_source_span_verified_after"] == "false"
        assert canonical[row["rule_id"]]["source_span_verified"] == "false"
        if row["rule_id"] == "ZZ-TT-010":
            assert row["source_span_status"] == "SOURCE_MISMATCH_CONFIRMED"
            assert row["subject_alignment"] == "MISMATCHED"
            assert row["source_pdf_page"] == "115" and row["source_printed_page"] == "228"
        else:
            assert row["source_span_status"] == "VERIFIED_VISUAL_SCAN"
            assert row["subject_alignment"] == "MATCHED"
    with (ROOT / "knowledge/review/quarantine_v0.1.csv").open(encoding="utf-8", newline="") as stream:
        quarantine = {row["record_id"]: row for row in csv.DictReader(stream)}
    assert quarantine["ZZ-TT-010"]["effective_status"] == "QUARANTINED"
    assert quarantine["ZZ-TT-010"]["reason_code"] == "SOURCE_MISMATCH_CONFIRMED"


def test_tiantong_candidate_and_mapping_review_stay_noncanonical():
    data = load_baseline()
    tt = next(star for star in data["stars"] if star["name"] == "天同")
    claims = {row["claim_key"]: row for row in tt["source_claims"]}
    assert "比较性描述" in claims["TT-L1-HARMONY-COMPARISON"]["claim_summary"]
    assert claims["TT-L2-REVERSE-CONFIGURATION"]["source_locator"]["printed_page"] == 14
    assert claims["TT-L2-REVERSE-HUAJI"]["source_locator"]["printed_page"] == 178
    assert "紫杀行运" in claims["TT-L2-SAMEYIN-SCOPE"]["claim_summary"]
    assert "属于文昌化忌" in claims["TT-010-SOURCE-MISMATCH"]["claim_summary"]
    assert all(p["canonicalization_authorized"] is False and p["numeric_strength_assigned"] is False for p in tt["candidate_properties"])
    tt_records = [r for r in data["mapping_review_records"] if r["review_record_id"].startswith("MR-TT-")]
    assert len(tt_records) == 18
    assert validate_mapping_review_collection(data["mapping_review_records"]) == []
    mismatch = next(r for r in tt_records if r["review_record_id"] == "MR-TT-SOURCE-MISMATCH-009")
    assert mismatch["evidence_role"]["state"] == "NOT_APPLICABLE" and mismatch["evidence_role"]["value"] is None
    assert mismatch["mapping_disposition"]["value"] == "not_supported_for_target"


def test_lianzhen_candidate_checkpoint_keeps_source_disagreement_and_scope_unresolved():
    data = load_baseline()
    lz = next(star for star in data["stars"] if star["name"] == "廉贞")
    assert lz["status"] == "STAGE_B_CHECKPOINT_COMPLETED_NOT_FINAL"
    assert len(lz["source_claims"]) == 19
    assert len(lz["candidate_properties"]) == 20
    assert all(prop["normalization_epistemic"] == "UNRESOLVED" for prop in lz["candidate_properties"])
    assert all(prop["canonicalization_authorized"] is False for prop in lz["candidate_properties"])
    assert all(prop["numeric_strength_assigned"] is False for prop in lz["candidate_properties"])
    assert "廉贞" in data["progress"]["completed_expansion_stars"]
    lz_checkpoint = next(entry for entry in data["progress"]["expansion_checkpoint_history"] if entry["star"] == "廉贞")
    assert lz_checkpoint["next_star"] == "天府"

    claims = {claim["claim_key"]: claim for claim in lz["source_claims"]}
    assert claims["LZ-L0-SUBSTRATE-SOURCE-DISAGREEMENT"]["source_locator"]["source_id"] == "SRC-ZZ-001"
    assert claims["LZ-L0-SUBSTRATE-SOURCE-DISAGREEMENT"]["independent_source_span_count"] == 2
    assert claims["LZ-L1-DUALITY-TENSION"]["source_locator"]["pdf_scan_page"] == 8
    assert claims["LZ-HUALU-SCOPE"]["source_locator"]["pdf_scan_page"] == 90
    assert claims["LZ-LIANFU-CONTEXT"]["source_locator"]["pdf_scan_page"] == 20
    assert claims["LZ-LIANXIANG-CONTEXT"]["source_locator"]["pdf_scan_page"] == 42
    assert claims["LZ-LIANPO-CONTEXT"]["source_locator"]["pdf_scan_page"] == 75

    records = {record["review_record_id"]: record for record in data["mapping_review_records"]}
    assert sum(record_id.startswith("MR-LZ-") for record_id in records) == 20
    assert all(prop["mapping_review_record_id"] in records for prop in lz["candidate_properties"])
    assert validate_mapping_review_collection(data["mapping_review_records"]) == []

    with LIANZHEN_SOURCE_REVIEW.open(encoding="utf-8", newline="") as handle:
        review_rows = list(csv.DictReader(handle))
    with CANONICAL_RULES.open(encoding="utf-8", newline="") as handle:
        canonical_rows = list(csv.DictReader(handle))
    expected_ids = {row["rule_id"] for row in canonical_rows if row["rule_id"].startswith("ZZ-LZ-")}
    assert len(review_rows) == 27
    assert {row["rule_id"] for row in review_rows} == expected_ids
    assert len({row["rule_id"] for row in review_rows}) == len(review_rows)
    assert all(row["source_span_status"] == "VERIFIED_VISUAL_SCAN" for row in review_rows)
    assert all(row["proposal_status"] == "PROPOSAL_ONLY_NOT_CANONICAL" for row in review_rows)
    assert all(row["normalization_epistemic_after"] == "UNRESOLVED" for row in review_rows)
    assert all(row["canonical_source_span_verified_after"] == "false" for row in review_rows)
    by_id = {row["rule_id"]: row for row in review_rows}
    assert by_id["ZZ-LZ-001"]["source_id"] == "SRC-ZZ-001"
    assert by_id["ZZ-LZ-001"]["source_pdf_page"] == "44"
    assert "差异" in by_id["ZZ-LZ-001"]["modality_scope_ambiguity"]
    assert by_id["ZZ-LZ-003"]["source_pdf_page"] == "90"
    assert "化禄" in by_id["ZZ-LZ-003"]["condition_scope_assessment"]
    assert by_id["ZZ-LZ-008"]["source_pdf_page"] == "20"
    assert by_id["ZZ-LZ-009"]["source_pdf_page"] == "42"
    assert by_id["ZZ-LZ-010"]["source_pdf_page"] == "75"


def test_tianfu_candidate_checkpoint_is_source_bounded_and_noncanonical():
    data = load_baseline()
    tf = next(star for star in data["stars"] if star["name"] == "天府")
    assert tf["star_id"] == "STAR-TF"
    assert tf["status"] == "STAGE_B_CHECKPOINT_COMPLETED_NOT_FINAL"
    assert len(tf["source_claims"]) == 16
    assert len(tf["candidate_properties"]) == 18
    assert all(prop["canonicalization_authorized"] is False for prop in tf["candidate_properties"])
    assert all(prop["numeric_strength_assigned"] is False for prop in tf["candidate_properties"])
    assert all(prop["normalization_epistemic"] == "UNRESOLVED" for prop in tf["candidate_properties"])
    assert data["source_policy"]["tianfu_source_locator"]["pdf_scan_page"] == 9
    assert data["source_policy"]["tianfu_source_locator"]["printed_pages"] == [17, 18]
    assert data["source_policy"]["tianfu_source_locator"]["prior_visual_review_rows_reused"] == 5
    assert "天府" in data["progress"]["completed_expansion_stars"]
    tf_checkpoint = next(entry for entry in data["progress"]["expansion_checkpoint_history"] if entry["star"] == "天府")
    assert tf_checkpoint["next_star"] == "贪狼"
    assert tf_checkpoint["prior_visual_review_rows_reused"] == 5
    records = {record["review_record_id"]: record for record in data["mapping_review_records"]}
    tf_records = {key: record for key, record in records.items() if key.startswith("MR-TF-")}
    assert len(tf_records) == 18
    assert all(prop["mapping_review_record_id"] in records for prop in tf["candidate_properties"])
    assert validate_mapping_review_collection(data["mapping_review_records"]) == []
    with TIANFU_SOURCE_REVIEW.open(encoding="utf-8", newline="") as handle:
        review_rows = list(csv.DictReader(handle))
    with CANONICAL_RULES.open(encoding="utf-8", newline="") as handle:
        canonical_rows = list(csv.DictReader(handle))
    expected_ids = {row["rule_id"] for row in canonical_rows if row["rule_id"].startswith("ZZ-TF-")}
    assert len(review_rows) == 25
    assert {row["rule_id"] for row in review_rows} == expected_ids
    assert len({row["rule_id"] for row in review_rows}) == len(review_rows)
    assert all(row["source_span_status"] == "VERIFIED_VISUAL_SCAN" for row in review_rows)
    assert all(row["proposal_status"] == "PROPOSAL_ONLY_NOT_CANONICAL" for row in review_rows)
    assert all(row["normalization_epistemic_after"] == "UNRESOLVED" for row in review_rows)
    assert all(row["canonical_source_span_verified_after"] == "false" for row in review_rows)
    assert all(row["source_pdf_page"] == "9" for row in review_rows)
    by_id = {row["rule_id"]: row for row in review_rows}
    assert by_id["ZZ-TF-002"]["source_printed_page"] == "17"
    assert "不重复计为独立证据" in by_id["ZZ-TF-002"]["core_use_assessment"]
    assert by_id["ZZ-TF-007"]["source_printed_page"] == "17"
    assert "空库" in by_id["ZZ-TF-007"]["literal_source_span"]
    assert "露库" in by_id["ZZ-TF-008"]["literal_source_span"]
    assert by_id["ZZ-TF-008"]["source_printed_page"] == "17"
    assert by_id["ZZ-TF-009"]["source_printed_page"] == "17"
    assert "究竟成为孤立" in by_id["ZZ-TF-009"]["literal_source_span"]
    assert "canonical ZZ-TF-009" in by_id["ZZ-TF-009"]["modality_scope_ambiguity"]
    assert by_id["ZZ-TF-Y03"]["source_printed_page"] == "17"
    assert by_id["ZZ-TF-Y03"]["literal_source_span"] == by_id["ZZ-TF-009"]["literal_source_span"]
    assert by_id["ZZ-TF-Y04"]["source_printed_page"] == "17-18"
    assert by_id["ZZ-TF-010"]["source_printed_page"] == "18"
    assert "大限/流年" in by_id["ZZ-TF-010"]["condition_scope_assessment"]
    assert "财星" in by_id["ZZ-TF-002"]["modality_scope_ambiguity"]
    with CANONICAL_RULES.open(encoding="utf-8", newline="") as handle:
        rows = {row["rule_id"]: row for row in csv.DictReader(handle)}
    for rule_id in expected_ids:
        assert rows[rule_id]["source_epistemic"] == "EXPLICIT"
        assert rows[rule_id]["normalization_epistemic"] == "UNRESOLVED"
        assert rows[rule_id]["source_span_verified"] == "false"


def test_tanlang_candidate_checkpoint_preserves_source_scope_conditions_and_nonpromotion():
    data = load_baseline()
    tl = next(star for star in data["stars"] if star["name"] == "贪狼")
    assert tl["star_id"] == "STAR-TL"
    assert tl["status"] == "STAGE_B_CHECKPOINT_COMPLETED_NOT_FINAL"
    assert len(tl["source_claims"]) == 20
    assert len(tl["candidate_properties"]) == 20
    assert tl["held_canonical_rule_ids"] == ["ZZ-TL-010"]
    assert all(prop["canonicalization_authorized"] is False for prop in tl["candidate_properties"])
    assert all(prop["numeric_strength_assigned"] is False for prop in tl["candidate_properties"])
    assert all(prop["normalization_epistemic"] == "UNRESOLVED" for prop in tl["candidate_properties"])
    assert data["source_policy"]["tanlang_source_locator"]["pdf_scan_page"] == 11
    assert data["source_policy"]["tanlang_source_locator"]["printed_pages"] == [21, 22]
    assert data["source_policy"]["tanlang_source_locator"]["source_sha256"] == data["source_policy"]["source_sha256"]
    assert data["source_policy"]["tanlang_source_locator"]["prior_visual_review_rows_reused"] == 0
    assert data["source_policy"]["tanlang_additional_source_locators"][0]["pdf_scan_page"] == 51
    assert data["source_policy"]["tanlang_additional_source_locators"][1]["pdf_scan_page"] == 93
    assert "贪狼" in data["progress"]["completed_expansion_stars"]
    tl_checkpoint = next(entry for entry in data["progress"]["expansion_checkpoint_history"] if entry["star"] == "贪狼")
    assert tl_checkpoint["next_star"] == "巨门"
    assert tl_checkpoint["fully_verified_rows"] == 24
    assert tl_checkpoint["partially_verified_rows"] == 1
    assert tl_checkpoint["held_rows"] == 4
    records = {record["review_record_id"]: record for record in data["mapping_review_records"]}
    tl_records = {key: record for key, record in records.items() if key.startswith("MR-TL-")}
    assert len(tl_records) == 20
    assert all(prop["mapping_review_record_id"] in records for prop in tl["candidate_properties"])
    assert validate_mapping_review_collection(data["mapping_review_records"]) == []
    with TANLANG_SOURCE_REVIEW.open(encoding="utf-8", newline="") as handle:
        review_rows = list(csv.DictReader(handle))
    with CANONICAL_RULES.open(encoding="utf-8", newline="") as handle:
        canonical_rows = list(csv.DictReader(handle))
    expected_ids = {row["rule_id"] for row in canonical_rows if row["rule_id"].startswith("ZZ-TL-")}
    assert len(expected_ids) == 29
    assert len(review_rows) == 29
    assert {row["rule_id"] for row in review_rows} == expected_ids
    assert len({row["rule_id"] for row in review_rows}) == len(review_rows)
    by_id = {row["rule_id"]: row for row in review_rows}
    fully_verified = {f"ZZ-TL-{i:03d}" for i in range(1, 9)} | {f"ZZ-TL-X{i:02d}" for i in range(1, 15)} | {f"ZZ-TL-Y{i:02d}" for i in range(1, 6)}
    assert all(by_id[rule_id]["source_span_status"] == "VERIFIED_VISUAL_SCAN" for rule_id in fully_verified)
    assert by_id["ZZ-TL-009"]["source_span_status"] == "PARTIALLY_VERIFIED_VISUAL_SCAN"
    assert by_id["ZZ-TL-009"]["source_pdf_page"] == "93"
    assert by_id["ZZ-TL-009"]["source_printed_page"] == "184-185"
    held = {"ZZ-TL-010"}
    assert all(by_id[rule_id]["source_span_status"] in {"OUT_OF_SCOPE_SOURCE_NOT_VERIFIED", "NOT_VERIFIED_IN_REVIEWED_SPANS"} for rule_id in held)
    assert by_id["ZZ-TL-001"]["source_id"] == "SRC-ZZ-002"
    assert by_id["ZZ-TL-001"]["source_pdf_page"] == "11"
    assert by_id["ZZ-TL-003"]["source_pdf_page"] == "51"
    assert by_id["ZZ-TL-003"]["source_printed_page"] == "100"
    assert by_id["ZZ-TL-006"]["source_pdf_page"] == "41"
    assert by_id["ZZ-TL-006"]["source_id"] == "SRC-ZZ-001"
    assert by_id["ZZ-TL-007"]["source_pdf_page"] == "42"
    assert by_id["ZZ-TL-008"]["source_pdf_page"] == "42"
    assert by_id["ZZ-TL-010"]["source_pdf_page"] == ""
    assert all(row["normalization_epistemic_after"] == "UNRESOLVED" for row in review_rows)
    assert all(row["canonical_source_span_verified_after"] == "false" for row in review_rows)
    with CANONICAL_RULES.open(encoding="utf-8", newline="") as handle:
        canonical_by_id = {row["rule_id"]: row for row in csv.DictReader(handle)}
    for rule_id in expected_ids:
        assert canonical_by_id[rule_id]["source_epistemic"] == "EXPLICIT"
        assert canonical_by_id[rule_id]["normalization_epistemic"] == "UNRESOLVED"
        assert canonical_by_id[rule_id]["source_span_verified"] == "false"


def test_jumen_candidate_checkpoint_preserves_source_scope_and_nonpromotion():
    data = load_baseline()
    jm = next(star for star in data["stars"] if star["name"] == "巨门")
    assert jm["star_id"] == "STAR-JM"
    assert jm["status"] == "STAGE_B_CHECKPOINT_COMPLETED_NOT_FINAL"
    assert len(jm["source_claims"]) == 20
    assert len(jm["candidate_properties"]) == 20
    assert jm["held_canonical_rule_ids"] == []
    assert all(prop["canonicalization_authorized"] is False for prop in jm["candidate_properties"])
    assert all(prop["numeric_strength_assigned"] is False for prop in jm["candidate_properties"])
    assert all(prop["normalization_epistemic"] == "UNRESOLVED" for prop in jm["candidate_properties"])
    assert data["source_policy"]["jumen_source_locator"]["pdf_scan_page"] == 12
    assert data["source_policy"]["jumen_source_locator"]["printed_pages"] == [23, 24]
    assert data["source_policy"]["jumen_source_locator"]["source_sha256"] == data["source_policy"]["source_sha256"]
    assert data["source_policy"]["jumen_source_locator"]["prior_visual_review_rows_reused"] == 0
    assert data["source_policy"]["jumen_source_locator"]["verification"] == "VISUAL_SOURCE_REVIEWED; SHA256_MATCHES_SOURCES_INDEX"
    assert data["source_policy"]["jumen_source_locator"]["canonical_source_span_verified_mutated"] is False
    assert data["source_policy"]["jumen_review_path"] == "knowledge/core/14star-property-normalization/JUMEN_SOURCE_SPAN_REVIEW_v0.1.csv"
    assert len(data["source_policy"]["jumen_review_rule_ids"]) == 26
    assert data["source_policy"]["jumen_held_rule_ids"] == []
    assert data["source_policy"]["jumen_partial_rule_ids"] == ["ZZ-JM-003", "ZZ-JM-004", "ZZ-JM-006", "ZZ-JM-007"]
    assert data["progress"]["completed_expansion_stars"] == ["紫微", "天机", "武曲", "天同", "廉贞", "天府", "贪狼", "巨门", "天梁", "七杀", "破军"]
    assert data["progress"]["remaining_expansion_stars_in_existing_order"] == []
    jm_checkpoint = next(entry for entry in data["progress"]["expansion_checkpoint_history"] if entry["star"] == "巨门")
    assert jm_checkpoint["star"] == "巨门"
    assert jm_checkpoint["next_star"] == "天梁"
    assert jm_checkpoint["fully_verified_rows"] == 21
    assert jm_checkpoint["partially_verified_rows"] == 4
    assert jm_checkpoint["held_rows"] == 1

    records = {record["review_record_id"]: record for record in data["mapping_review_records"]}
    jm_records = {key: record for key, record in records.items() if key.startswith("MR-JM-")}
    assert len(jm_records) == 20
    assert all(prop["mapping_review_record_id"] in records for prop in jm["candidate_properties"])
    assert validate_mapping_review_collection(data["mapping_review_records"]) == []

    with JUMEN_SOURCE_REVIEW.open(encoding="utf-8", newline="") as handle:
        review_rows = list(csv.DictReader(handle))
    with CANONICAL_RULES.open(encoding="utf-8", newline="") as handle:
        canonical_rows = list(csv.DictReader(handle))
    expected_ids = {row["rule_id"] for row in canonical_rows if row["rule_id"].startswith("ZZ-JM-")}
    assert len(expected_ids) == 26
    assert len(review_rows) == 26
    assert {row["rule_id"] for row in review_rows} == expected_ids
    assert len({row["rule_id"] for row in review_rows}) == len(review_rows)
    assert all(row["proposal_status"] == "PROPOSAL_ONLY_NOT_CANONICAL" for row in review_rows)
    assert all(row["normalization_epistemic_after"] == "UNRESOLVED" for row in review_rows)
    assert all(row["canonical_source_span_verified_after"] == "false" for row in review_rows)
    by_id = {row["rule_id"]: row for row in review_rows}
    fully_verified = {"ZZ-JM-001", "ZZ-JM-002", "ZZ-JM-008", "ZZ-JM-009", "ZZ-JM-010"} | {f"ZZ-JM-X{i:02d}" for i in range(1, 12)} | {f"ZZ-JM-Y{i:02d}" for i in range(1, 6)}
    partial = {"ZZ-JM-003", "ZZ-JM-004", "ZZ-JM-006", "ZZ-JM-007"}
    held = set()
    assert all(by_id[rule_id]["source_span_status"] == "VERIFIED_VISUAL_SCAN" for rule_id in fully_verified)
    assert all(by_id[rule_id]["source_span_status"] == "PARTIALLY_VERIFIED_VISUAL_SCAN" for rule_id in partial)
    assert all(by_id[rule_id]["source_span_status"] == "OUT_OF_SCOPE_SOURCE_NOT_VERIFIED" for rule_id in held)
    assert by_id["ZZ-JM-005"]["source_id"] == "SRC-ZZ-001"
    assert by_id["ZZ-JM-005"]["source_span_status"] == "VERIFIED_VISUAL_SCAN"
    assert by_id["ZZ-JM-005"]["source_pdf_page"] == "42"
    assert by_id["ZZ-JM-005"]["source_printed_page"] == "83"
    assert by_id["ZZ-JM-003"]["source_pdf_page"] == "12"
    assert "多言" in by_id["ZZ-JM-004"]["modality_scope_ambiguity"]
    assert "调各" in by_id["ZZ-JM-Y03"]["modality_scope_ambiguity"]
    assert "双能" in by_id["ZZ-JM-Y03"]["modality_scope_ambiguity"]
    assert "遮蔽别人的光辉" in by_id["ZZ-JM-002"]["literal_source_span"]
    assert by_id["ZZ-JM-002"]["literal_source_span"] == "在斗数中，巨门为暗曜。所谓[暗曜]，并不是说巨门自己本身没有光辉，而是他善于遮蔽别人的光辉，故称为[暗]。"
    assert by_id["ZZ-JM-004"]["literal_source_span"] == "当有了才华之后。其言词虽多，亦不会专事对别人遮蔽；"
    assert by_id["ZZ-JM-008"]["literal_source_span"] == "当得到助力之后，亦应减少了一些疑忌之心，且可将疑忌化为有益的思虑。"
    assert "……" not in by_id["ZZ-JM-002"]["literal_source_span"]
    assert "……" not in by_id["ZZ-JM-X07"]["literal_source_span"]
    assert by_id["ZZ-JM-X07"]["literal_source_span"].endswith("因言词的机变更能取信于他人。")
    assert "调各" in by_id["ZZ-JM-Y03"]["literal_source_span"]
    assert "双能" in by_id["ZZ-JM-Y03"]["literal_source_span"]
    assert "在子午卯酉四垣，为[机巨]的结构" in by_id["ZZ-JM-Y05"]["literal_source_span"]
    assert "decade" in by_id["ZZ-JM-X10"]["canonical_time_scope"]
    with CANONICAL_RULES.open(encoding="utf-8", newline="") as handle:
        canonical_by_id = {row["rule_id"]: row for row in csv.DictReader(handle)}
    for rule_id in expected_ids:
        assert canonical_by_id[rule_id]["source_epistemic"] == "EXPLICIT"
        assert canonical_by_id[rule_id]["normalization_epistemic"] == "UNRESOLVED"
        assert canonical_by_id[rule_id]["source_span_verified"] == "false"


def test_tianliang_candidate_checkpoint_preserves_source_scope_and_nonpromotion():
    data = load_baseline()
    tianliang = next(star for star in data["stars"] if star["name"] == "天梁")
    assert tianliang["star_id"] == "STAR-TLIA"
    assert tianliang["status"] == "STAGE_B_CHECKPOINT_COMPLETED_NOT_FINAL"
    assert len(tianliang["source_claims"]) == 20
    assert len(tianliang["candidate_properties"]) == 20
    assert tianliang["held_canonical_rule_ids"] == []
    assert all(p["canonicalization_authorized"] is False for p in tianliang["candidate_properties"])
    assert all(p["numeric_strength_assigned"] is False for p in tianliang["candidate_properties"])
    assert all(p["normalization_epistemic"] == "UNRESOLVED" for p in tianliang["candidate_properties"])
    loc = data["source_policy"]["tianliang_source_locator"]
    assert loc["pdf_scan_page"] == 14 and loc["printed_pages"] == [27, 28]
    assert loc["source_sha256"] == data["source_policy"]["source_sha256"]
    assert loc["canonical_source_span_verified_mutated"] is False
    assert len(data["source_policy"]["tianliang_review_rule_ids"]) == 26
    assert data["source_policy"]["tianliang_held_rule_ids"] == []
    assert data["source_policy"]["tianliang_partial_rule_ids"] == []
    assert "天梁" in data["progress"]["completed_expansion_stars"]
    assert data["progress"]["remaining_expansion_stars_in_existing_order"] == []
    checkpoint = next(entry for entry in data["progress"]["expansion_checkpoint_history"] if entry["star"] == "天梁")
    assert checkpoint["star"] == "天梁" and checkpoint["next_star"] == "七杀"
    assert (checkpoint["fully_verified_rows"], checkpoint["partially_verified_rows"], checkpoint["held_rows"]) == (26, 0, 0)
    records = {r["review_record_id"]: r for r in data["mapping_review_records"]}
    tlia_records = {k:v for k,v in records.items() if k.startswith("MR-TLIA-")}
    assert len(tlia_records) == 20
    assert all(p["mapping_review_record_id"] in records for p in tianliang["candidate_properties"])
    assert validate_mapping_review_collection(data["mapping_review_records"]) == []
    with TIANLIANG_SOURCE_REVIEW.open(encoding="utf-8", newline="") as handle:
        review_rows = list(csv.DictReader(handle))
    with CANONICAL_RULES.open(encoding="utf-8", newline="") as handle:
        canonical_rows = list(csv.DictReader(handle))
    expected = {r["rule_id"] for r in canonical_rows if r["rule_id"].startswith("ZZ-TLIA-")}
    assert len(expected) == len(review_rows) == 26
    assert {r["rule_id"] for r in review_rows} == expected
    assert all(r["proposal_status"] == "PROPOSAL_ONLY_NOT_CANONICAL" for r in review_rows)
    assert all(r["normalization_epistemic_after"] == "UNRESOLVED" for r in review_rows)
    assert all(r["canonical_source_span_verified_after"] == "false" for r in review_rows)
    by_id = {r["rule_id"]:r for r in review_rows}
    assert sum(r["source_span_status"] == "VERIFIED_VISUAL_SCAN" for r in review_rows) == 26
    assert by_id["ZZ-TLIA-001"]["source_span_status"] == "VERIFIED_VISUAL_SCAN"
    assert "第三得" in by_id["ZZ-TLIA-001"]["literal_source_span"]
    assert "第三星" in by_id["ZZ-TLIA-001"]["modality_scope_ambiguity"]
    assert "PI裁定" in by_id["ZZ-TLIA-001"]["core_use_assessment"]
    assert by_id["ZZ-TLIA-010"]["source_span_status"] == "VERIFIED_VISUAL_SCAN"
    assert by_id["ZZ-TLIA-010"]["source_pdf_page"] == "80"
    assert by_id["ZZ-TLIA-010"]["source_printed_page"] == "159"


def test_qisha_candidate_checkpoint_preserves_source_scope_and_nonpromotion():
    data = load_baseline()
    qisha = next(star for star in data["stars"] if star["name"] == "七杀")
    assert qisha["star_id"] == "STAR-QS"
    assert qisha["status"] == "STAGE_B_CHECKPOINT_COMPLETED_NOT_FINAL"
    assert len(qisha["source_claims"]) == 20
    assert len(qisha["candidate_properties"]) == 20
    assert qisha["held_canonical_rule_ids"] == []
    assert all(p["canonicalization_authorized"] is False for p in qisha["candidate_properties"])
    assert all(p["numeric_strength_assigned"] is False for p in qisha["candidate_properties"])
    assert all(p["normalization_epistemic"] == "UNRESOLVED" for p in qisha["candidate_properties"])
    loc = data["source_policy"]["qisha_source_locator"]
    assert loc["pdf_scan_page"] == 15 and loc["printed_pages"] == [29, 30]
    assert loc["source_sha256"] == data["source_policy"]["source_sha256"]
    assert loc["canonical_source_span_verified_mutated"] is False
    assert len(data["source_policy"]["qisha_review_rule_ids"]) == 26
    assert data["source_policy"]["qisha_held_rule_ids"] == []
    assert data["source_policy"]["qisha_partial_rule_ids"] == []
    assert data["progress"]["completed_expansion_stars"] == ["紫微", "天机", "武曲", "天同", "廉贞", "天府", "贪狼", "巨门", "天梁", "七杀", "破军"]
    assert data["progress"]["remaining_expansion_stars_in_existing_order"] == []
    checkpoint = next(entry for entry in data["progress"]["expansion_checkpoint_history"] if entry["star"] == "七杀")
    assert checkpoint["star"] == "七杀" and checkpoint["next_star"] == "破军"
    assert (checkpoint["fully_verified_rows"], checkpoint["partially_verified_rows"], checkpoint["held_rows"]) == (26, 0, 0)
    records = {r["review_record_id"]: r for r in data["mapping_review_records"]}
    qs_records = {k:v for k,v in records.items() if k.startswith("MR-QS-")}
    assert len(qs_records) == 20
    assert all(p["mapping_review_record_id"] in records for p in qisha["candidate_properties"])
    assert len(data["mapping_review_records"]) == 241
    assert validate_mapping_review_collection(data["mapping_review_records"]) == []
    with QISHA_SOURCE_REVIEW.open(encoding="utf-8", newline="") as handle:
        review_rows = list(csv.DictReader(handle))
    with CANONICAL_RULES.open(encoding="utf-8", newline="") as handle:
        canonical_rows = list(csv.DictReader(handle))
    expected = {r["rule_id"] for r in canonical_rows if r["rule_id"].startswith("ZZ-QS-")}
    assert len(expected) == len(review_rows) == 26
    assert {r["rule_id"] for r in review_rows} == expected
    assert len({r["rule_id"] for r in review_rows}) == len(review_rows)
    assert all(r["proposal_status"] == "PROPOSAL_ONLY_NOT_CANONICAL" for r in review_rows)
    assert all(r["normalization_epistemic_after"] == "UNRESOLVED" for r in review_rows)
    assert all(r["canonical_source_span_verified_after"] == "false" for r in review_rows)
    by_id = {r["rule_id"]:r for r in review_rows}
    assert sum(r["source_span_status"] == "VERIFIED_VISUAL_SCAN" for r in review_rows) == 26
    assert by_id["ZZ-QS-005"]["source_span_status"] == "VERIFIED_VISUAL_SCAN"
    assert "廉洁" in by_id["ZZ-QS-005"]["literal_source_span"]
    assert "PI于2026-10-28裁定" in by_id["ZZ-QS-005"]["modality_scope_ambiguity"]
    assert "PI裁定" in by_id["ZZ-QS-005"]["core_use_assessment"]
    assert "廉贞" in by_id["ZZ-QS-005"]["modality_scope_ambiguity"]
    assert all(r["source_span_status"] != "OUT_OF_SCOPE_SOURCE_NOT_VERIFIED" for r in review_rows)
    with CANONICAL_RULES.open(encoding="utf-8", newline="") as handle:
        canonical_by_id = {r["rule_id"]:r for r in csv.DictReader(handle)}
    for rule_id in expected:
        assert canonical_by_id[rule_id]["source_epistemic"] == "EXPLICIT"
        assert canonical_by_id[rule_id]["normalization_epistemic"] == "UNRESOLVED"
        assert canonical_by_id[rule_id]["source_span_verified"] == "false"


def test_pojun_candidate_checkpoint_preserves_source_scope_and_nonpromotion():
    data = load_baseline()
    pojun = next(star for star in data["stars"] if star["name"] == "破军")
    assert pojun["star_id"] == "STAR-PJ"
    assert pojun["status"] == "STAGE_B_CHECKPOINT_COMPLETED_NOT_FINAL"
    assert len(pojun["source_claims"]) == 20
    assert len(pojun["candidate_properties"]) == 20
    assert pojun["held_canonical_rule_ids"] == []
    assert all(p["canonicalization_authorized"] is False for p in pojun["candidate_properties"])
    assert all(p["numeric_strength_assigned"] is False for p in pojun["candidate_properties"])
    assert all(p["normalization_epistemic"] == "UNRESOLVED" for p in pojun["candidate_properties"])
    assert data["progress"]["completed_expansion_stars"][-1] == "破军"
    assert data["progress"]["remaining_expansion_stars_in_existing_order"] == []
    checkpoint = data["progress"]["expansion_checkpoint_history"][-1]
    assert checkpoint["star"] == "破军" and checkpoint["next_star"] is None
    assert (checkpoint["fully_verified_rows"], checkpoint["partially_verified_rows"], checkpoint["held_rows"]) == (25, 0, 5)
    records = {r["review_record_id"]: r for r in data["mapping_review_records"]}
    pj_records = {k:v for k,v in records.items() if k.startswith("MR-PJ-")}
    assert len(pj_records) == 20
    assert all(p["mapping_review_record_id"] in records for p in pojun["candidate_properties"])
    assert len(data["mapping_review_records"]) == 241
    assert validate_mapping_review_collection(data["mapping_review_records"]) == []
    with POJUN_SOURCE_REVIEW.open(encoding="utf-8", newline="") as handle:
        review_rows = list(csv.DictReader(handle))
    with CANONICAL_RULES.open(encoding="utf-8", newline="") as handle:
        canonical_rows = list(csv.DictReader(handle))
    expected = {r["rule_id"] for r in canonical_rows if r["rule_id"].startswith("ZZ-PJ-")}
    assert len(expected) == len(review_rows) == 30
    assert {r["rule_id"] for r in review_rows} == expected
    assert all(r["proposal_status"] == "PROPOSAL_ONLY_NOT_CANONICAL" for r in review_rows)
    assert all(r["normalization_epistemic_after"] == "UNRESOLVED" for r in review_rows)
    assert all(r["canonical_source_span_verified_after"] == "false" for r in review_rows)
    by_id = {r["rule_id"]: r for r in review_rows}
    assert sum(r["source_span_status"] == "VERIFIED_VISUAL_SCAN" for r in review_rows) == 30
    assert all(by_id[f"ZZ-PJ-{n:03d}"]["source_span_status"] == "VERIFIED_VISUAL_SCAN" for n in range(6, 11))
    assert by_id["ZZ-PJ-006"]["source_pdf_page"] == "96"
    assert by_id["ZZ-PJ-007"]["source_pdf_page"] == "97"


def test_sun_source_review_covers_all_canonical_rows_without_promoting_them():
    with SUN_SOURCE_REVIEW.open(encoding="utf-8", newline="") as handle:
        review_rows = list(csv.DictReader(handle))
    with CANONICAL_RULES.open(encoding="utf-8", newline="") as handle:
        canonical_rows = list(csv.DictReader(handle))
    expected = {r["rule_id"] for r in canonical_rows if r["subject"] == "太阳"}
    assert len(expected) == len(review_rows) == 40
    assert {r["rule_id"] for r in review_rows} == expected
    assert all(r["source_id"] == "SRC-ZZ-002" for r in review_rows)
    assert all(r["source_pdf_page"] == "5" for r in review_rows)
    assert all(r["source_span_status"] == "VERIFIED_VISUAL_SCAN" for r in review_rows)
    assert all(r["proposal_status"] == "PROPOSAL_ONLY_NOT_CANONICAL" for r in review_rows)
    assert all(r["normalization_epistemic_after"] == "UNRESOLVED" for r in review_rows)
    assert all(r["canonical_source_span_verified_after"] == "false" for r in review_rows)
    canonical_by_id = {r["rule_id"]: r for r in canonical_rows}
    assert all(canonical_by_id[r["rule_id"]]["source_span_verified"] == "false" for r in review_rows)


def test_pre_pi_source_audit_followup_covers_all_canonical_rules_without_promotion():
    data = load_baseline()
    assert data["pre_pi_gates"]["pi_review_authorized"] is True
    assert data["pre_pi_gates"]["formal_mapping_approval"] is False
    followup = data["source_audit_followup"]
    assert followup["status"] == "PI_DECISION_CARDS_READY_PENDING_PI_DECISIONS"
    cards_path = ROOT / data["pre_pi_gates"]["decision_cards_path"]
    assert cards_path.exists()
    cards_text = cards_path.read_text(encoding="utf-8")
    assert cards_text.count("## 决策卡 ") == 3
    assert followup["guardrails"]["canonical_rules_mutated"] is False
    assert followup["guardrails"]["formal_mapping_approval"] is False
    assert followup["guardrails"]["product_consumption_authorized"] is False
    review_paths = [
        ROOT / data["source_policy"]["solar_review_path"],
        ROOT / data["source_policy"]["taiyin_review_path"],
        ROOT / data["source_policy"]["tianxiang_review_path"],
        ROOT / data["source_policy"]["tianji_review_path"],
        ROOT / data["source_policy"]["wuqu_review_path"],
        ROOT / data["source_policy"]["tiantong_review_path"],
        ROOT / data["source_policy"]["ziwei_review_path"],
        ROOT / data["source_policy"]["lianzheng_review_path"],
        ROOT / data["source_policy"]["tianfu_review_path"],
        ROOT / data["source_policy"]["tanlang_review_path"],
        ROOT / data["source_policy"]["jumen_review_path"],
        ROOT / data["source_policy"]["tianliang_review_path"],
        ROOT / data["source_policy"]["qisha_review_path"],
        ROOT / data["source_policy"]["pojun_review_path"],
    ]
    with CANONICAL_RULES.open(encoding="utf-8", newline="") as handle:
        canonical_rows = list(csv.DictReader(handle))
    canonical_ids = {row["rule_id"] for row in canonical_rows}
    all_rows = []
    for review_path in review_paths:
        with review_path.open(encoding="utf-8", newline="") as handle:
            all_rows.extend(csv.DictReader(handle))
    assert len(all_rows) == len(canonical_rows) == 430
    assert {row["rule_id"] for row in all_rows} == canonical_ids
    assert len({row["rule_id"] for row in all_rows}) == len(all_rows)
    counts = {}
    for row in all_rows:
        counts[row["source_span_status"]] = counts.get(row["source_span_status"], 0) + 1
    assert counts == {
        "VERIFIED_VISUAL_SCAN": 423,
        "PARTIALLY_VERIFIED_VISUAL_SCAN": 5,
        "NOT_VERIFIED_IN_REVIEWED_SPANS": 1,
        "SOURCE_MISMATCH_CONFIRMED": 1,
    }
    assert all(row["normalization_epistemic"] == "UNRESOLVED" for row in canonical_rows)
    assert all(row["source_span_verified"] == "false" for row in canonical_rows)
    held = {row["rule_id"] for row in all_rows if row["source_span_status"] in {"NOT_VERIFIED_IN_REVIEWED_SPANS", "SOURCE_MISMATCH_CONFIRMED"}}
    assert held == {"ZZ-TL-010", "ZZ-TT-010"}


def test_pre_pi_mapping_review_audit_counts_are_consistent():
    data = load_baseline()
    audit = data["pre_pi_gates"]["mapping_review_audit"]
    assert audit["mapping_review_records"] == audit["unique_review_ids"] == 241
    assert audit["candidate_properties"] == audit["properties_with_valid_review_links"] == 182
    assert audit["canonical_rules"] == 430
    assert audit["missing_canonical_rule_refs"] == 0
    assert audit["unique_target_refs"] == 81
    assert audit["source_ref_uses"] == 428
    assert audit["unique_source_refs"] == 360
    assert audit["duplicated_exact_source_ref_groups"] == 59
    assert audit["uses_in_duplicated_ref_groups"] == 127
    assert audit["candidate_canonicalization_authorized"] == 0
    assert audit["candidate_numeric_strength_assigned"] == 0
    assert audit["all_candidate_normalization_states"] == "UNRESOLVED"
    assert len(audit["unknown_evidence_role_review_record_ids"]) == 1
    assert audit["unknown_evidence_role_review_record_ids"] == ["MR-LZ-SYMBOLIC-ROLE-002"]
    reuse_path = ROOT / audit["source_ref_reuse_ledger_path"]
    assert reuse_path.exists()
    with reuse_path.open(encoding="utf-8") as handle:
        reuse_report = handle.read()
    assert f"{audit['duplicated_exact_source_ref_groups']}组" in reuse_report
    assert "shared_span:" in reuse_report


def test_wuqu_financial_role_candidate_is_reviewed_against_l3_not_qi05():
    data = load_baseline()
    wuqu = next(star for star in data["stars"] if star["name"] == "武曲")
    prop = next(p for p in wuqu["candidate_properties"] if p["candidate_key"] == "EXP-WQ-10")
    records = {r["review_record_id"]: r for r in data["mapping_review_records"]}
    review = records[prop["mapping_review_record_id"]]
    assert prop["target_ref"] == "knowledge/qi_ontology.yaml#/architecture/layers/L3"
    assert prop["mapping_review_record_id"] == "MR-WQ-L3-FINANCIAL-ROLE-016"
    assert review["target_ref"] == prop["target_ref"]
    assert prop["mapping_disposition"] == "candidate_only"
    assert set(prop["source_rule_ids"]) == {"ZZ-WQ-002", "ZZ-WQ-X01"}
    rejected_qi05 = records["MR-WQ-FINANCIAL-ROLE-002"]
    assert rejected_qi05["target_ref"] == "STAR-WQ.intrinsic_signature:QI-05"
    assert rejected_qi05["mapping_disposition"]["value"] == "not_supported_for_target"


def test_pre_pi_candidate_source_scope_mismatches_are_explicitly_audited():
    data = load_baseline()
    audit = data["pre_pi_gates"]["mapping_review_audit"]["candidate_source_scope_audit"]
    records = {row["review_record_id"]: row for row in data["mapping_review_records"]}
    mismatches = []
    for star in data["stars"]:
        for prop in star.get("candidate_properties", []):
            review = records[prop["mapping_review_record_id"]]
            directly_cited = {
                rule_id
                for source_ref in review.get("source_refs", [])
                for rule_id in re.findall(r"ZZ-[A-Z]+-(?:[0-9]{3}|X[0-9]{2}|Y[0-9]{2})", source_ref)
            }
            missing = set(prop.get("source_rule_ids", [])) - directly_cited
            if missing:
                mismatches.append((prop["candidate_key"], missing))
    assert len(mismatches) == audit["properties_with_source_scope_mismatch"] == 1
    assert sum(len(missing) for _, missing in mismatches) == audit["candidate_source_rule_ids_not_directly_cited"] == 1
    assert set(key for key, _ in mismatches) == set(audit["candidate_keys"])
    assert mismatches == [("EXP-WQ-06", {"ZZ-WQ-X06"})]
    report_path = ROOT / audit["path"]
    report = report_path.read_text(encoding="utf-8")
    assert "不应机械地把缺少的 ID 全部添加到审核记录" in report
    assert "不授予正式映射批准" in report

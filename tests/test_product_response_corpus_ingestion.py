import json
from pathlib import Path

from src.product.response_corpus_ingestion import (
    CAREER_TEMPORAL_ELIGIBILITY_PATH,
    CAREER_TEMPORAL_SUMMARY_PATH,
    MAJOR_STARS_PATH,
    RESPONSE_PILOT_PATH,
    SIXTY_SYSTEMS_OVERRIDES_PATH,
    SIXTY_SYSTEMS_PATH,
    SIXTY_SYSTEMS_REVIEW_PATH,
    build_response_corpus_readiness,
    inventory_career_temporal_eligibility,
    inventory_major_star_temporal_response,
    inventory_response_semantics_pilot,
    inventory_sixty_system_temporal_reaction,
    select_major_star_temporal_candidates,
    select_sixty_system_temporal_candidates,
    validate_current_fail_closed_state,
)


ROOT = Path(__file__).resolve().parents[1]
VERSIONED_REPORT = ROOT / "product" / "RESPONSE_CORPUS_READINESS_v0.1.json"


def test_major_star_exact_temporal_response_inventory():
    inventory = inventory_major_star_temporal_response()

    assert inventory.total_rows == 430
    assert inventory.selected_rows == 24
    assert inventory.readiness_class == (
        "SOURCE_TEMPORAL_CANDIDATE_AWAITING_KR_NORMALIZATION"
    )
    assert inventory.scope_counts == {
        "decade_or_year": 22,
        "natal_or_temporal": 2,
    }
    assert inventory.operator_counts == {
        "activate": 3,
        "condition": 3,
        "enhance": 10,
        "gate": 1,
        "project": 5,
        "transform": 2,
    }
    assert inventory.review_status_counts == {"MODEL_SELF_REVIEWED": 24}
    assert inventory.source_epistemic_counts == {"EXPLICIT": 24}
    assert inventory.source_span_verified_counts == {"false": 24}
    assert inventory.normalization_verified_counts == {"false": 24}
    assert all(v == 0 for v in inventory.missing_required_source_fields.values())
    assert "NO_CANONICAL_KR_RECORD_CONTRACT" in inventory.blockers


def test_sixty_system_exact_temporal_reaction_inventory_uses_review_sidecar():
    inventory = inventory_sixty_system_temporal_reaction()

    assert inventory.total_rows == 2193
    assert inventory.selected_rows == 1015
    assert inventory.readiness_class == (
        "SOURCE_TEMPORAL_CANDIDATE_AWAITING_KR_NORMALIZATION"
    )
    assert inventory.scope_counts == {
        "decade": 28,
        "decade_or_year": 840,
        "generic": 2,
        "temporal": 106,
        "year": 39,
    }
    assert inventory.review_status_counts == {"MODEL_SELF_REVIEWED": 1015}
    assert inventory.source_epistemic_counts == {"EXPLICIT": 1015}
    assert inventory.source_span_verified_counts == {"false": 1015}
    assert inventory.normalization_epistemic_counts == {
        "IMPLEMENTATION": 35,
        "UNRESOLVED": 980,
    }
    assert inventory.normalization_verified_counts == {"false": 1015}
    assert inventory.details["selected_rows_with_schema_override"] == 35
    assert all(v == 0 for v in inventory.missing_required_source_fields.values())
    assert "NORMALIZATION_EPISTEMIC_UNRESOLVED_PRESENT" in inventory.blockers


def test_exact_metadata_selectors_ignore_temporal_words_in_decoy_text():
    major_rows = [
        {
            "rule_id": "A",
            "rule_family": "projection_rule",
            "evidence_text": "mentions decade and year",
        },
        {
            "rule_id": "B",
            "rule_family": "temporal_response",
            "evidence_text": "no keyword needed",
        },
    ]
    system_rows = [
        {
            "rule_id": "C",
            "interaction_role": "mode_definition",
            "context": "大限/流年",
        },
        {
            "rule_id": "D",
            "interaction_role": "temporal_reaction",
            "context": "general",
        },
    ]

    assert [x["rule_id"] for x in select_major_star_temporal_candidates(major_rows)] == [
        "B"
    ]
    assert [
        x["rule_id"] for x in select_sixty_system_temporal_candidates(system_rows)
    ] == ["D"]


def test_career_temporal_audit_stays_knowledge_blocked():
    inventory = inventory_career_temporal_eligibility()

    assert inventory.total_rows == 9
    assert inventory.selected_rows == 9
    assert inventory.readiness_class == "KNOWLEDGE_EXPLICITLY_BLOCKED"
    assert inventory.scope_counts == {"DECADE": 7, "YEAR": 2}
    assert inventory.details["eligible_for_current_compiler"] == 0
    assert inventory.details["blocked"] == 8
    assert inventory.details["case_support_only_excluded"] == 1
    assert inventory.details["executable_pilot_emitted"] is False
    assert inventory.details["production_registry_should_remain_empty"] is True


def test_response_semantics_pilot_is_vocabulary_not_temporal_kr():
    inventory = inventory_response_semantics_pilot()

    assert inventory.total_rows == 8
    assert inventory.readiness_class == "SEMANTIC_VOCABULARY_ONLY"
    assert inventory.scope_counts == {"(unset)": 8}
    assert inventory.details["execution_status_counts"] == {
        "LEXICAL_ONLY": 4,
        "STRUCTURAL_ONLY": 4,
    }
    assert inventory.details["temporal_scope_bound_records"] == 0
    assert inventory.details["safe_symbolic_records"] == 0


def test_readiness_report_distinguishes_source_abundance_from_kr_readiness():
    report = build_response_corpus_readiness()
    summary = report["summary"]

    assert summary["source_temporal_candidate_rows"] == 1039
    assert summary["major_star_temporal_response_rows"] == 24
    assert summary["sixty_system_temporal_reaction_rows"] == 1015
    assert summary["career_temporal_audit_rows"] == 9
    assert summary["response_semantics_pilot_rows"] == 8
    assert summary["source_span_verified_temporal_candidate_rows"] == 0
    assert summary["normalization_verified_temporal_candidate_rows"] == 0
    assert summary["missing_required_source_field_occurrences"] == 0
    assert summary["knowledge_explicit_compiler_eligible_rows"] == 0
    assert summary["compiler_ready_kr_records"] == 0

    gate = report["now6_gate"]
    assert gate["NOW6_RESPONSE_COMPILER_INPUT_READY"] is False
    assert gate["response_compiler_implemented"] is False
    assert gate["response_profile_tau_implemented"] is False
    assert gate["predictive_validity"] == "NOT_VALIDATED"


def test_kr_gap_and_boundaries_remain_fail_closed():
    report = build_response_corpus_readiness()

    assert report["kr_contract_gap"]["knowledge_owned_normalization_required"] is True
    assert report["kr_contract_gap"]["product_may_infer_missing_semantics"] is False
    assert report["kr_contract_gap"]["product_may_split_decade_or_year"] is False
    assert report["kr_contract_gap"]["product_may_promote_case_support"] is False
    assert report["kr_contract_gap"]["product_may_numericize_valence"] is False

    assert report["boundaries"] == {
        "source_explicit_implies_compiler_ready": False,
        "reviewed_implies_executable": False,
        "normalized_source_row_implies_kr_record": False,
        "favorable_unfavorable_implies_numeric_gain": False,
        "temporal_scope_implies_layer_split": False,
        "case_support_implies_reusable_rule": False,
    }

    validate_current_fail_closed_state()


def test_versioned_readiness_report_matches_deterministic_audit():
    stored = json.loads(VERSIONED_REPORT.read_text(encoding="utf-8"))
    assert stored == build_response_corpus_readiness()


def test_all_declared_source_artifacts_exist():
    for path in (
        MAJOR_STARS_PATH,
        SIXTY_SYSTEMS_PATH,
        SIXTY_SYSTEMS_REVIEW_PATH,
        SIXTY_SYSTEMS_OVERRIDES_PATH,
        CAREER_TEMPORAL_ELIGIBILITY_PATH,
        CAREER_TEMPORAL_SUMMARY_PATH,
        RESPONSE_PILOT_PATH,
    ):
        assert path.exists()

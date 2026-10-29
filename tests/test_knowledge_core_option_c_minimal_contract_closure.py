"""Boundary and integrity tests for the proposal-only Option C contract review."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEW_PATH = (
    ROOT
    / "knowledge"
    / "core"
    / "wp06b"
    / "OPTION_C_MINIMAL_CONTRACT_CLOSURE_REVIEW_v0.1.json"
)


def load_review():
    return json.loads(REVIEW_PATH.read_text(encoding="utf-8"))


def test_review_is_explicitly_proposal_only_and_noncanonical():
    review = load_review()
    assert review["status"] == "PROPOSAL_ONLY_NOT_CANONICAL"
    assert review["architecture_decision"]["option"] == "OPTION_C"
    assert review["architecture_decision"]["reopen_architecture_choice"] is False
    assert review["architecture_decision"]["detailed_contract_frozen"] is False
    assert review["invariants"]["canonical_ontology_ids_assigned"] is False
    assert review["invariants"]["accepted_mappings_created"] is False
    assert review["invariants"]["production_schema_changed"] is False
    assert review["invariants"]["product_runtime_or_kib_changed"] is False
    assert review["invariants"]["probability_status"] == "UNKNOWN"
    assert review["invariants"]["empirical_predictive_validity_claimed"] is False


def test_candidate_vocabularies_remain_distinct_and_nonexhaustive():
    review = load_review()
    assert set(review["candidate_output_kind_values"]) == {
        "PROCESS_PATTERN",
        "ACTION_CONDITIONED_OUTCOME",
        "SCENE_OR_CONTEXT",
        "DIRECTIONAL_AXIS",
        "DOMAIN_SEMANTIC_BOUNDARY",
        "CROSS_PALACE_CONSTRAINT",
        "STRUCTURAL_CONSTRAINT",
        "TEMPORAL_CONDITION",
        "EVENT_CANDIDATE",
    }
    assert set(review["candidate_event_specificity_values"]) == {
        "PROCESS_SEQUENCE_NOT_SINGLE_EVENT",
        "CONDITIONAL_OUTCOME_NOT_OBSERVED",
        "SCENE_NOT_OBSERVED_EVENT",
        "EVENT_CLASS_CANDIDATE",
        "SPECIFIC_EVENT_CANDIDATE",
    }
    assert review["findings"][0]["status"] == "SUPPORTED_AS_CANDIDATE_SET_NOT_EXHAUSTIVE"


def test_required_boundary_cases_and_negative_inferences_are_preserved():
    review = load_review()
    cases = {case["id"]: case for case in review["boundary_cases"]}
    required = {
        "CA01-035",
        "CA01-045",
        "CA05-469",
        "M01-006",
        "W01-002",
        "CA01-005",
        "CA01-007",
        "CA09-809",
        "QI-02/QI-15",
        "QR-01/QR-04",
        "QI-04/QI-16:ZZ-PJ-X06",
        "QI-17-CAND/QI-18-CAND",
    }
    assert required <= set(cases)


def test_process_keeps_modality_and_does_not_become_an_event():
    review = load_review()
    case = next(c for c in review["boundary_cases"] if c["id"] == "CA01-035")
    assert case["output_kind"]["value"] == "PROCESS_PATTERN"
    assert case["event_specificity"]["value"] == "PROCESS_SEQUENCE_NOT_SINGLE_EVENT"
    assert any("往往" in item for item in case["preserve"])
    assert any("AND/OR" in item for item in case["preserve"])
    assert "inevitable outcome" in case["forbidden_inference"]
    assert "single observed event" in case["forbidden_inference"]


def test_action_conditioned_outcome_requires_real_world_action():
    review = load_review()
    case = next(c for c in review["boundary_cases"] if c["id"] == "CA01-045")
    assert case["output_kind"]["value"] == "ACTION_CONDITIONED_OUTCOME"
    assert case["event_specificity"]["value"] == "CONDITIONAL_OUTCOME_NOT_OBSERVED"
    assert any("CA01-042" in item and "CA01-044" in item for item in case["preserve"])
    assert any("勉强求变" in item for item in case["preserve"])
    assert any("action occurred" in item for item in case["forbidden_inference"])


def test_scene_and_direction_are_not_completed_personal_events():
    review = load_review()
    cases = {case["id"]: case for case in review["boundary_cases"]}
    assert cases["CA05-469"]["event_specificity"]["value"] == "SCENE_NOT_OBSERVED_EVENT"
    assert set(cases["CA05-469"]["forbidden_inference"]) >= {
        "personal injury",
        "illness",
        "accident event",
    }
    assert cases["M01-006"]["event_specificity"] == {
        "status": "NOT_APPLICABLE",
        "value": None,
    }
    assert "completed migration" in cases["M01-006"]["forbidden_inference"]


def test_constraints_and_domain_boundaries_are_not_event_nodes():
    review = load_review()
    cases = {case["id"]: case for case in review["boundary_cases"]}
    for case_id in ("W01-002", "CA01-005", "CA01-007"):
        assert cases[case_id]["event_specificity"]["status"] == "NOT_APPLICABLE"
    assert "independent manifestation node" in cases["W01-002"]["forbidden_inference"]
    assert "observed marriage event" in cases["CA01-007"]["forbidden_inference"]


def test_case_only_negative_control_cannot_be_generalized():
    review = load_review()
    case = next(c for c in review["boundary_cases"] if c["id"] == "CA09-809")
    assert case["output_kind"]["value"] == "EVENT_CANDIDATE"
    assert case["event_specificity"]["value"] == "SPECIFIC_EVENT_CANDIDATE"
    assert any("case_support_only=true" in item for item in case["preserve"])
    assert "canonical universal event family" in case["forbidden_inference"]
    assert "probability" in case["forbidden_inference"]


def test_qi_qr_roles_and_source_alternatives_stay_unresolved():
    review = load_review()
    cases = {case["id"]: case for case in review["boundary_cases"]}
    assert cases["QI-02/QI-15"]["output_kind"]["status"] == "UNKNOWN"
    assert "bearer/agent" in cases["QI-02/QI-15"]["preserve"]
    assert "realized support" in cases["QR-01/QR-04"]["preserve"]
    assert "source OR alternative" in cases["QI-04/QI-16:ZZ-PJ-X06"]["preserve"]
    assert "rewrite OR as AND" in cases["QI-04/QI-16:ZZ-PJ-X06"]["forbidden_inference"]


def test_candidate_dimensions_remain_candidate_only():
    review = load_review()
    case = next(c for c in review["boundary_cases"] if c["id"] == "QI-17-CAND/QI-18-CAND")
    assert "candidate identity" in case["preserve"]
    assert "assign formal IDs" in case["forbidden_inference"]
    assert "canonical mapping acceptance" in case["forbidden_inference"]


def test_missing_unknown_conflict_and_not_applicable_are_not_collapsed():
    review = load_review()
    states = review["status_semantics"]
    assert len({states["UNKNOWN"], states["MISSING"], states["CONFLICT"], states["NOT_APPLICABLE"]}) == 4
    assert "Not yet reviewed" in states["legacy_absent_mapping_review"]
    assert "not equivalent" in states["legacy_absent_mapping_review"]


def test_pi_decisions_are_recommendations_not_implicit_approval():
    review = load_review()
    card = review["pi_decision_card"]
    assert card["requires_explicit_pi_response"] is True
    assert card["canonical_approval"] is False
    assert card["consumer_readiness"] is False
    assert set(card["recommended_decisions"]) == {"D1", "D2", "D3", "D4", "D5"}

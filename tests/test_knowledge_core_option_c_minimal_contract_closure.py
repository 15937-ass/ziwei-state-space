import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW_PATH = ROOT / "knowledge/core/wp06b/OPTION_C_MINIMAL_CONTRACT_CLOSURE_REVIEW_v0.1.json"
MATRIX_PATH = ROOT / "knowledge/core/14star-property-matrix/14STAR_PROPERTY_MATRIX_QIQR_AUDIT_v0.1.json"
PROPOSAL_PATH = ROOT / "knowledge/core/wp06b/OPTION_C_METADATA_CONTRACT_PROPOSAL_v0.1.json"
MAPPING_SCHEMA_PATH = ROOT / "knowledge/core/wp06b/MAPPING_REVIEW_SCHEMA_v0.1.json"
REVIEW_SCHEMA_PATH = ROOT / "knowledge/REVIEW_SCHEMA_v0.3.md"


def _load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_closure_review_remains_proposal_only_and_does_not_canonicalize():
    review = _load(REVIEW_PATH)
    assert review["status"] == "PROPOSAL_ONLY_NOT_CANONICAL"
    assert review["architecture_direction"]["option"] == "OPTION-C"
    assert review["architecture_direction"]["canonical_root_selected"] is False
    assert review["architecture_direction"]["canonical_ids_assigned"] is False
    canonical = review["canonicalization"]
    assert canonical["canonical_mapping_accepted"] is False
    assert canonical["production_output_kind_values_frozen"] is False
    assert canonical["production_event_specificity_values_frozen"] is False
    assert canonical["product_consumption_authorized"] is False
    assert canonical["empirical_validity_claim"] is False


def test_taxonomy_recommendations_are_traceable_to_fourteen_star_audit():
    review = _load(REVIEW_PATH)
    matrix = _load(MATRIX_PATH)
    rec = matrix["pr710_taxonomy_recommendation"]
    assert rec["canonical_change_authorized"] is False
    assert rec["output_kind"]["action"] == "SPLIT"
    assert rec["event_specificity"]["action"] == "SPLIT_AND_RENAME"
    assert review["findings"]["output_kind"]["source_audit_action"] == rec["output_kind"]["action"]
    assert review["findings"]["event_specificity"]["source_audit_action"] == rec["event_specificity"]["action"]


def test_source_and_normalization_epistemic_axes_remain_separate():
    review = _load(REVIEW_PATH)
    proposal = _load(PROPOSAL_PATH)
    mapping_schema = _load(MAPPING_SCHEMA_PATH)
    boundaries = review["findings"]["epistemic_and_approval_boundaries"]
    assert boundaries["source_epistemic_values"] == ["EXPLICIT", "INFERRED_FROM_SOURCE", "UNRESOLVED_SOURCE"]
    assert boundaries["normalization_epistemic_values"] == ["SOURCE_PRESERVING", "INFERRED", "IMPLEMENTATION", "HYPOTHESIS", "UNRESOLVED"]
    assert boundaries["review_status_is_distinct"] is True
    assert boundaries["mapping_disposition_is_per_target_review_only"] is True
    assert boundaries["canonical_approval_is_separate"] is True
    assert boundaries["consumer_readiness_is_separate"] is True
    assert proposal["guardrails"]["product_consumption_authorized"] is False
    assert "mapping_disposition" in mapping_schema["properties"]


def test_all_required_source_boundary_cases_are_present_once():
    review = _load(REVIEW_PATH)
    cases = review["boundary_cases"]
    ids = [case["case_id"] for case in cases]
    required = ["CA01-035", "CA01-045", "CA05-469", "M01-006", "CA01-005", "CA01-007", "W01-002", "CA09-809"]
    assert len(ids) == len(set(ids))
    assert set(required).issubset(set(ids))
    by_id = {case["case_id"]: case for case in cases}
    assert by_id["CA01-035"]["semantic_form"] == "PROCESS_PATTERN"
    assert "往往" in by_id["CA01-035"]["prohibited_inference"]
    assert by_id["CA01-045"]["relation_constraint_role"] == "ACTION_PREREQUISITE"
    assert by_id["CA01-045"]["prerequisite_refs"] == ["CA01-042", "CA01-044"]
    assert by_id["CA05-469"]["semantic_form"] == "SCENE_OR_CONTEXT"
    assert by_id["M01-006"]["semantic_form"] == "DIRECTIONAL_AXIS"
    assert by_id["CA01-005"]["relation_constraint_role"] == "CROSS_PALACE_CONSTRAINT"
    assert by_id["CA01-007"]["relation_constraint_role"] == "CROSS_PALACE_CONSTRAINT"
    assert by_id["W01-002"]["relation_constraint_role"] == "DOMAIN_SEMANTIC_BOUNDARY"


def test_case_only_event_candidate_never_becomes_universal_or_observed():
    review = _load(REVIEW_PATH)
    case = next(item for item in review["boundary_cases"] if item["case_id"] == "CA09-809")
    assert case["evidence_status"].startswith("case_support_only")
    assert case["mapping_disposition"] == "candidate_only"
    assert case["occurrence_status"] == "NOT_ESTABLISHED_BY_SOURCE"
    assert case["event_granularity"] == {"state": "KNOWN", "value": "SPECIFIC_EVENT_CANDIDATE"}
    assert review["canonicalization"]["canonical_mapping_accepted"] is False


def test_non_event_claims_do_not_receive_event_granularity_values():
    review = _load(REVIEW_PATH)
    by_id = {case["case_id"]: case for case in review["boundary_cases"]}
    for case_id in ["CA01-035", "CA01-045", "CA05-469", "M01-006", "CA01-005", "CA01-007", "W01-002"]:
        assert by_id[case_id]["event_granularity"] == {"state": "NOT_APPLICABLE", "value": None}


def test_mapping_review_missing_legacy_envelope_is_not_mislabeled_missing():
    review = _load(REVIEW_PATH)
    mapping_schema = _load(MAPPING_SCHEMA_PATH)
    assert review["findings"]["epistemic_and_approval_boundaries"]["absent_legacy_mapping_review_envelope"] == "NOT_YET_REVIEWED_UNDER_THIS_CONTRACT_NOT_MISSING"
    assert mapping_schema["description"].find("does not approve a mapping") >= 0


def test_unresolved_qi_qr_boundaries_and_source_or_are_preserved():
    review = _load(REVIEW_PATH)
    ids = {item["id"] for item in review["qi_qr_counterexamples"]}
    assert {"QI01_QI14", "QI02_QI15", "QI08_QI06", "QI04_QI16", "QR01_QR04", "ZZ-PJ-X06"}.issubset(ids)
    zz = next(item for item in review["qi_qr_counterexamples"] if item["id"] == "ZZ-PJ-X06")
    assert "OR into AND" in zz["prohibited_inference"]
    assert review["status"] == "PROPOSAL_ONLY_NOT_CANONICAL"

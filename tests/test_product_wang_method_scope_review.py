import json
from pathlib import Path

from src.product.wang_method_scope_review import (
    build_wang_method_policy_readiness_v03,
    build_wang_method_scope_review,
)

ROOT = Path(__file__).resolve().parents[1]
REVIEW_PATH = ROOT / "product" / "WANG_METHOD_SCOPE_REVIEW_V0_1C.json"
READINESS_V02_PATH = ROOT / "product" / "WANG_METHOD_POLICY_READINESS_v0.2.json"
READINESS_V03_PATH = ROOT / "product" / "WANG_METHOD_POLICY_READINESS_v0.3.json"
POLICY_PATH = ROOT / "product" / "METHOD_POLICY_EXECUTION_RULES_v0.1.json"
PATTERNS_PATH = ROOT / "product" / "expert_cases" / "wang_tingzhi" / "METHOD_PATTERNS_v0.1.json"


def _read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_scope_review_is_deterministic_and_matches_committed_artifact():
    assert _read(REVIEW_PATH) == build_wang_method_scope_review()


def test_review_matrix_covers_all_24_cases_and_six_patterns_fail_closed():
    review = _read(REVIEW_PATH)
    assert review["summary"]["case_count"] == 24
    assert review["summary"]["method_pattern_count"] == 6
    assert review["summary"]["assessment_count"] == 144
    assert review["summary"]["exact_target_domain_matches"] == 0
    assert review["summary"]["explicit_case_to_pattern_source_links"] == 0
    assert review["summary"]["proposed_binding_count"] == 0
    assert review["summary"]["full_expert_replay_ready"] == 0
    assert review["summary"]["review_outcome_counts"] == {
        "DEFERRED_SYMBOLIC_INTERPRETATION": 48,
        "INSUFFICIENT_SOURCE_EVIDENCE": 64,
        "MISSING_CONTEXT_BINDING": 24,
        "SEMANTIC_ONLY_RELEVANCE": 8,
    }

    pattern_ids = [item["pattern_id"] for item in _read(PATTERNS_PATH)["method_patterns"]]
    assert len(review["case_reviews"]) == 24
    assert [row["case_id"] for row in review["case_reviews"]] == [
        f"WANG-CASE-{index:03d}" for index in range(1, 25)
    ]
    for row in review["case_reviews"]:
        assessments = row["method_pattern_assessments"]
        assert len(assessments) == 6
        assert [item["pattern_id"] for item in assessments] == pattern_ids
        for item in assessments:
            assert item["exact_target_domain_match"] is False
            assert item["explicit_case_to_pattern_source_link"] is False
            assert item["proposed_binding"] is None
            assert item["binding_status"] == "NOT_BOUND_FAIL_CLOSED"
            assert item["pattern_allowed_use"] == "SEMANTIC_ONLY"


def test_case_source_spans_are_preserved_but_conclusion_and_outcome_are_not_binding_basis():
    review = _read(REVIEW_PATH)
    assert review["review_contract"]["case_conclusion_or_outcome_content_used_for_binding"] is False
    assert review["review_contract"]["chart_structure_used_as_binding_basis"] is False
    for row in review["case_reviews"]:
        refs = row["source_span_refs"]
        assert set(refs) == {"chart", "reasoning", "conclusion", "outcome"}
        for assessment in row["method_pattern_assessments"]:
            assert assessment["case_source_basis_refs"] == [refs["reasoning"]]
            assert refs["conclusion"] not in assessment["case_source_basis_refs"]
            assert refs["outcome"] not in assessment["case_source_basis_refs"]
        assert row["case_allowed_use"] == "CASE_SUPPORT_ONLY"
        assert row["case_graph_allowed_use"] == ["CASE_SUPPORT_ONLY"]
        assert row["case_graph_canonical_rule_refs"] == []


def test_full_chart_materialization_split_and_zi_time_ambiguity_are_preserved():
    review = _read(REVIEW_PATH)
    assert review["summary"]["full_chart_materialized_case_count"] == 11
    assert review["summary"]["full_chart_unmaterialized_case_count"] == 13

    materialized = [
        row["case_id"] for row in review["case_reviews"]
        if row["chart_materialization"]["status"] == "MATERIALIZED"
    ]
    assert materialized == [
        "WANG-CASE-001",
        "WANG-CASE-003",
        "WANG-CASE-006",
        "WANG-CASE-009",
        "WANG-CASE-010",
        "WANG-CASE-012",
        "WANG-CASE-013",
        "WANG-CASE-015",
        "WANG-CASE-019",
        "WANG-CASE-021",
        "WANG-CASE-023",
    ]
    for row in review["case_reviews"]:
        chart = row["chart_materialization"]
        if chart["status"] == "MATERIALIZED":
            assert chart["materialization_claim"] == "SOURCE_INPUT_RECONSTRUCTED_TARGET_ANCHOR_VERIFIED"
            assert chart["target_anchor_verification"]["status"] == "UNIQUE_ANCHOR_MATCH_RECONFIRMED"
            assert chart["target_anchor_verification"]["matched"] is True
            assert chart["full_source_chart_equivalence_verified"] is False
        else:
            assert chart["chart_specific_analysis_status"] == "BLOCKED_UNMATERIALIZED"

    case_021 = next(row for row in review["case_reviews"] if row["case_id"] == "WANG-CASE-021")
    provenance = case_021["chart_materialization"]["source_candidate_provenance"]
    assert provenance["source_time_ambiguity_preserved"] is True
    assert provenance["time_index_candidates"] == [0, 12]
    assert provenance["anchor_match_count"] == 1


def test_readiness_v03_is_a_versioned_successor_without_runtime_promotion():
    readiness_v02 = _read(READINESS_V02_PATH)
    readiness_v03 = _read(READINESS_V03_PATH)
    policy = _read(POLICY_PATH)

    assert readiness_v02["artifact_id"] == "WANG_METHOD_POLICY_READINESS_V0_2"
    assert readiness_v02["summary"]["full_chart_blocked_fold_count"] == 24
    assert readiness_v03 == build_wang_method_policy_readiness_v03()
    assert readiness_v03["artifact_id"] == "WANG_METHOD_POLICY_READINESS_V0_3"
    assert readiness_v03["supersedes_artifact"] == "product/WANG_METHOD_POLICY_READINESS_v0.2.json"
    assert readiness_v03["summary"]["full_chart_materialized_fold_count"] == 11
    assert readiness_v03["summary"]["full_chart_blocked_fold_count"] == 13
    assert readiness_v03["summary"]["method_policy_runtime_target_chart_blocked_fold_count"] == 24
    assert readiness_v03["summary"]["case_target_scope_binding_count"] == 0
    assert readiness_v03["summary"]["full_expert_replay_ready"] == 0
    assert len(policy["dispositions"]) == 6

    for old_fold, new_fold in zip(readiness_v02["folds"], readiness_v03["folds"]):
        assert new_fold["held_out_case_id"] == old_fold["held_out_case_id"]
        assert new_fold["evidence_statuses"] == old_fold["evidence_statuses"]
        assert new_fold["blockers"] == old_fold["blockers"]
        assert new_fold["trace_final_status"] == old_fold["trace_final_status"]
        assert new_fold["full_expert_replay_ready"] is False
        assert new_fold["method_scope_review"]["explicit_binding_count"] == 0

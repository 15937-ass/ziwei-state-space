import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "product" / "WANG_METHOD_SCOPE_REVIEW_V0_1C.json"
READINESS_V02 = ROOT / "product" / "WANG_METHOD_POLICY_READINESS_v0.2.json"
READINESS_V03 = ROOT / "product" / "WANG_METHOD_POLICY_READINESS_v0.3.json"
INVENTORY = ROOT / "product" / "expert_cases" / "wang_tingzhi" / "CASE_SOURCE_INVENTORY_v0.1.json"
CASES = ROOT / "product" / "expert_cases" / "wang_tingzhi" / "cases"
METHODS = ROOT / "product" / "expert_cases" / "wang_tingzhi" / "METHOD_PATTERNS_v0.1.json"
RULES = ROOT / "product" / "METHOD_POLICY_EXECUTION_RULES_v0.1.json"
MATERIALIZATION = ROOT / "product" / "expert_cases" / "wang_tingzhi" / "FULL_CHART_MATERIALIZATION_V0_1B.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def case_path(case_id):
    number = int(case_id.rsplit("-", 1)[1])
    return CASES / f"wang_case_{number:03d}.json"

def test_scope_review_covers_each_case_once_and_each_pattern_once_per_case():
    review = load(REVIEW)
    inventory = load(INVENTORY)
    methods = load(METHODS)
    expected_cases = [case["case_id"] for case in inventory["cases"]]
    expected_patterns = [pattern["pattern_id"] for pattern in methods["method_patterns"]]

    assert len(review["matrix"]) == 24
    assert [case["case_id"] for case in review["matrix"]] == expected_cases
    assert review["summary"]["case_count"] == 24
    assert review["summary"]["method_pattern_count"] == 6
    assert review["summary"]["assessment_count"] == 144

    for row, source in zip(review["matrix"], inventory["cases"], strict=True):
        case_record = load(case_path(source["case_id"]))
        assert row["target"]["domain"] == source["domain"]
        assert row["target"]["palace"] == source["palace"]
        assert row["source"]["chart_span_ref"] == source["chart_span_ref"]
        assert row["source"]["reasoning_span_ref"] == source["reasoning_span_ref"]
        assert row["source"]["conclusion_span_ref"] == source["conclusion_span_ref"]
        assert row["source"]["outcome_span_ref"] == source["outcome_span_ref"]
        assert row["source"]["graph_status"] == source["graph_status"]
        assert row["source"]["source_id"] == case_record["source"]["source_id"]
        assert row["source"]["epistemic_status"] == case_record["epistemic_status"]
        assert row["source"]["allowed_use"] == case_record["allowed_use"] == "CASE_SUPPORT_ONLY"
        assert case_record["target"]["domains"] == [source["domain"]]
        assert case_record["target"]["target_time_label"] == row["target"]["target_time_label"]
        assert all(node["epistemic_status"] == "SOURCE_DEMONSTRATED" for node in case_record["expert_reasoning_graph"]["nodes"])
        assert all(node["allowed_use"] == "CASE_SUPPORT_ONLY" for node in case_record["expert_reasoning_graph"]["nodes"])
        assert all(source["palace"] in node["palace_targets"] for node in case_record["expert_reasoning_graph"]["nodes"])
        assert [item["pattern_id"] for item in row["pattern_assessments"]] == expected_patterns
        assert len(row["pattern_assessments"]) == 6

def test_source_level_candidates_are_cited_and_never_become_runtime_bindings():
    review = load(REVIEW)
    allowed_statuses = {
        "EXPLICIT_SCOPE_FIT",
        "SEMANTIC_ONLY_RELEVANCE",
        "MISSING_CONTEXT_BINDING",
        "DEFERRED_SYMBOLIC_INTERPRETATION",
        "INSUFFICIENT_SOURCE_EVIDENCE",
    }
    candidate_count = 0
    for case in review["matrix"]:
        reasoning_ref = case["source"]["reasoning_span_ref"]
        forbidden_refs = {
            case["source"]["conclusion_span_ref"],
            case["source"]["outcome_span_ref"],
        }
        for assessment in case["pattern_assessments"]:
            assert assessment["assessment_status"] in allowed_statuses
            assert assessment["proposed_executable_target_binding"] is False
            assert assessment["runtime_binding_authorized"] is False
            assert assessment["case_target_scope_check"]["exact_match_to_existing_pattern_target_domain"] is False
            assert assessment["case_target_scope_check"]["result"] == "NO_EXACT_TARGET_DOMAIN_MATCH"
            if assessment["source_method_association_candidate"]:
                candidate_count += 1
                assert reasoning_ref in assessment["source_evidence_refs"]
                assert assessment["method_definition_span_refs"]
                assert not (set(assessment["source_evidence_refs"]) & forbidden_refs)
            if assessment["source_text_method_use_observed"]:
                assert reasoning_ref in assessment["source_evidence_refs"]
                assert not (set(assessment["source_evidence_refs"]) & forbidden_refs)
    assert review["summary"]["exact_target_domain_scope_fits"] == 0
    assert review["summary"]["proposed_executable_target_bindings"] == 0
    assert review["summary"]["runtime_bindings_authorized"] == 0
    assert candidate_count == review["summary"]["source_method_association_candidates"]

def test_method_patterns_and_execution_dispositions_are_unchanged():
    review = load(REVIEW)
    methods = load(METHODS)
    rules = load(RULES)
    pattern_by_id = {p["pattern_id"]: p for p in methods["method_patterns"]}
    rule_by_id = {r["pattern_id"]: r for r in rules["dispositions"]}

    assert len(pattern_by_id) == 6
    assert all(p["allowed_use"] == "SEMANTIC_ONLY" for p in methods["method_patterns"])
    for case in review["matrix"]:
        for assessment in case["pattern_assessments"]:
            p = pattern_by_id[assessment["pattern_id"]]
            r = rule_by_id[assessment["pattern_id"]]
            assert assessment["source_allowed_use"] == p["allowed_use"]
            assert assessment["policy_disposition"] == r["disposition"]
            assert assessment["policy_target_domains"] == r["target_domains"]
            assert assessment["method_definition_span_refs"] == p["source_span_refs"]
    assert review["summary"]["method_patterns_promoted_from_semantic_only"] == 0

def test_materialized_11_and_blocked_13_are_distinguished_without_overclaiming():
    review = load(REVIEW)
    readiness = load(READINESS_V03)
    historical = load(READINESS_V02)
    materialization = load(MATERIALIZATION)
    materialized_ids = {case["case_id"] for case in materialization["cases"]}

    assert len(materialized_ids) == 11
    assert materialization["summary"]["not_materialized"] == 13
    historical_copy = load(READINESS_V02)
    assert historical_copy["issue"] == 512
    assert historical["summary"]["full_chart_blocked_fold_count"] == 24
    assert readiness["issue"] == 615
    assert readiness["summary"]["full_chart_materialized_fold_count"] == 11
    assert readiness["summary"]["full_chart_not_materialized_fold_count"] == 13
    assert readiness["summary"]["full_chart_blocked_fold_count"] == 13
    assert readiness["summary"]["target_chart_evidence_blocked_fold_count"] == 24
    assert readiness["summary"]["full_expert_replay_ready"] == 0

    for fold in readiness["folds"]:
        assert fold["full_source_chart_equivalence_verified"] is False
        assert fold["target_chart_evidence_status_unchanged"] == "BLOCKED"
        if fold["held_out_case_id"] in materialized_ids:
            assert fold["chart_materialization_status"] == "SOURCE_INPUT_RECONSTRUCTED_TARGET_ANCHOR_VERIFIED"
            assert fold["chart_specific_analysis_status"] == "AVAILABLE_WITH_ANCHOR_ONLY_CLAIM"
        else:
            assert fold["chart_materialization_status"] == "NOT_MATERIALIZED"
            assert fold["chart_specific_analysis_status"] == "BLOCKED"

    blocked_counts = Counter(fold["chart_materialization_blocked_reason"] for fold in readiness["folds"] if fold["chart_materialization_status"] == "NOT_MATERIALIZED")
    assert blocked_counts == {"MULTIPLE_ANCHOR_MATCH": 6, "NO_ANCHOR_MATCH": 5, "BLOCKED_SOURCE_INCOMPLETE": 2}
    case_021 = next(row for row in review["matrix"] if row["case_id"] == "WANG-CASE-021")
    assert case_021["chart_materialization"]["source_candidate_ambiguity_preserved"]["candidate_indices"] == [0, 12]
    assert case_021["chart_materialization"]["source_candidate_ambiguity_preserved"]["unique_anchor_match"].endswith("T00")
    assert review["summary"]["full_expert_replay_ready"] == 0

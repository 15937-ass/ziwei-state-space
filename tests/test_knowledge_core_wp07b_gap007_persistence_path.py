import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "knowledge/core/wp07b/GAP007_PERSISTENCE_PATH_SOURCE_AUDIT_v0.1.json"
GAP6_V1 = ROOT / "knowledge/core/wp07b/GAP006_GROUP_FAVORABILITY_SOURCE_AUDIT_v0.1.json"
GAP6_V2 = ROOT / "knowledge/core/wp07b/GAP006_GROUP_FAVORABILITY_SOURCE_AUDIT_v0.2.json"
HANDOFF_V1 = ROOT / "knowledge/core/wp07b/TEMPORAL_REACTION_SOURCE_HANDOFF_v0.1.json"
HANDOFF_V2 = ROOT / "knowledge/core/wp07b/TEMPORAL_REACTION_SOURCE_HANDOFF_v0.2.json"
CAREER_CSV = ROOT / "knowledge/wp07b/CAREER_TEMPORAL_REACTION_ELIGIBILITY_v0.1.csv"
PROPERTY_CSV = ROOT / "knowledge/palaces/P10_property/wp07b/PROPERTY_TEMPORAL_REACTION_ELIGIBILITY_v0.1.csv"
CAREER_REVIEW = ROOT / "knowledge/wp07a/CAREER_100_REVIEW_08_v0.1.json"
PROPERTY_REVIEW = ROOT / "knowledge/wp05/property/PROPERTY_TP03_SOURCE_READJUDICATION_100_v0.1.json"
CORE_STATE = ROOT / "knowledge/states/CORE_STATE.yaml"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def csv_rows(path):
    with path.open(encoding="utf-8", newline="") as f:
        return {row["candidate_id"]: row for row in csv.DictReader(f)}


def test_gap007_has_two_non_interchangeable_subtypes():
    audit = load(AUDIT)
    assert audit["verdict"] == "DESCRIPTIVE_PATH_SUBTYPES_CONFIRMED_NO_EXECUTION"
    rows = {row["id"]: row for row in audit["records"]}
    assert rows["CA09-851"]["temporal_subtype"] == "MULTI_YEAR_CONSECUTIVE_ANNUAL_WINDOW"
    assert rows["TP03-248"]["temporal_subtype"] == "SAME_YEAR_ANTECEDENT_BRANCH_WITH_EVENT_CONSEQUENCE"
    assert rows["CA09-851"]["executable"] is False
    assert rows["TP03-248"]["executable"] is False


def test_ca09_851_preserves_literal_duration_and_good_period_unknown():
    audit = load(AUDIT)
    ca = next(row for row in audit["records"] if row["id"] == "CA09-851")
    assert ca["source_condition"] == "破军连续有三四年良好流年"
    assert ca["source_time_scope_literal"] == "THREE_TO_FOUR_CONSECUTIVE_FAVORABLE_YEARS"
    assert "三四年保留为来源原词范围" in ca["interpretation_boundaries"][0]
    career = csv_rows(CAREER_CSV)["CA09-851"]
    assert career["eligibility_status"] == "BLOCKED_MULTIYEAR_SEQUENCE"
    assert "MULTIYEAR_SEQUENCE_NOT_SUPPORTED" in career["blocking_reasons"]
    assert "DURATION_IS_EVIDENCE_NOT_THRESHOLD" in career["blocking_reasons"]


def test_ca09_851_source_context_remains_uncompiled():
    ca = next(row for row in load(CAREER_REVIEW)["mappings"] if row["source_rule_id"] == "CA09-851")
    assert ca["source_condition_text"] == "破军连续有三四年良好流年"
    assert ca["condition"] is None
    assert ca["execution_readiness"] == "BLOCKED_TEMPORAL"
    assert ca["source_context"]["context_is_complete_antecedent"] is False


def test_tp03_248_parent_and_same_year_branch_remain_held():
    prop = load(PROPERTY_REVIEW)["records"]
    r248 = next(row for row in prop if row["projection_rule_id"] == "TP03-248")
    r247 = next(row for row in prop if row["projection_rule_id"] == "TP03-247")
    assert r248["canonical_condition"] == "前格见吉"
    assert r248["history_feedback"] == "PATH_DEPENDENT_GATE"
    assert r247["case_support_only"] is True
    assert r247["reusable_projection_rule"] is False
    eligibility = csv_rows(PROPERTY_CSV)["TP03-248"]
    assert eligibility["eligibility_status"] == "BLOCKED_PATH_AND_CASE_PARENT"
    assert "PARENT_CASE_SUPPORT_ONLY" in eligibility["blocking_reasons"]
    assert "GENERIC_BENEFIC_GROUP_UNDEFINED" in eligibility["blocking_reasons"]


def test_gap006_v2_adds_only_career_period_valence_overlap():
    v1 = load(GAP6_V1)
    v2 = load(GAP6_V2)
    assert v1["gap_disposition"]["impacted_rule_count"] == 12
    assert "CA09-851" not in v1["gap_disposition"]["impacted_rule_ids"]
    assert v2["gap_disposition"]["impacted_rule_count"] == 13
    assert "CA09-851" in v2["gap_disposition"]["impacted_rule_ids"]
    e13 = next(row for row in v2["evidence"] if row["id"] == "G006-E13")
    assert e13["semantic_class"] == "PERIOD_VALENCE_OR_SUPPORT"
    assert e13["independent_criterion_defined"] is False
    assert e13["executable"] is False
    assert v2["human_gate"]["status"] == "FUTURE_NOT_PENDING"


def test_handoff_v2_cross_gap_links_and_gate_scope_are_explicit():
    v1 = load(HANDOFF_V1)
    v2 = load(HANDOFF_V2)
    assert v1["snapshot"]["main_commit"] != v2["snapshot"]["main_commit"]
    gaps = {row["gap_id"]: row for row in v2["gap_register"]}
    assert "CA09-851" in gaps["WP07B-GAP-001-ANTECEDENT-CHAIN"]["impacted_rule_ids"]
    assert "CA09-851" in gaps["WP07B-GAP-006-GROUP-OR-FAVORABILITY"]["impacted_rule_ids"]
    assert gaps["WP07B-GAP-007-PERSISTENCE-AND-PATH"]["member_subtypes"]["CA09-851"] == "MULTI_YEAR_CONSECUTIVE_ANNUAL_WINDOW"
    assert gaps["WP07B-GAP-007-PERSISTENCE-AND-PATH"]["member_subtypes"]["TP03-248"] == "SAME_YEAR_ANTECEDENT_BRANCH_WITH_EVENT_CONSEQUENCE"
    assert gaps["WP07B-GAP-007-PERSISTENCE-AND-PATH"]["human_gate_applicability"]["applies_to"] == ["CA09-851"]


def test_no_runtime_or_shared_operator_was_created():
    audit = load(AUDIT)
    b = audit["boundaries"]
    assert b["conditions_compiled"] == 0
    assert b["execution_unlocked"] == 0
    assert b["runtime_changed"] is False
    assert b["schema_changed"] is False
    assert b["duration_threshold_added"] is False
    assert b["probability_added"] is False
    assert b["human_gate_required_now"] is False
    assert audit["current_contract_assessment"]["sequence_supported"] if "sequence_supported" in audit["current_contract_assessment"] else audit["current_contract_assessment"]["consecutive_year_sequence_supported"] is False


def test_core_state_points_to_active_c9_and_accepted_c8():
    state = CORE_STATE.read_text(encoding="utf-8")
    assert "active_issue: 945" in state
    assert "last_completed_issue: 941" in state
    assert "last_completed_pr: 942" in state
    assert "fa62cebd619646b9c53ca0dba88291a5c45c8141" in state

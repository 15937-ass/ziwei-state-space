import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
S2 = ROOT / "knowledge/activation/CONTEXTUAL_ACTIVATION_SEMANTICS_v0.2.json"
S3 = ROOT / "knowledge/activation/CONTEXTUAL_ACTIVATION_SEMANTICS_v0.3.json"
B1 = ROOT / "knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_01_v0.1.json"
B2 = ROOT / "knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_02_v0.1.json"
B3 = ROOT / "knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_03_v0.1.json"
SRC3 = ROOT / "knowledge/wp07c/CAREER_GROUP_LEXICON_REVIEW_03_v0.1.json"
CLOSURE = ROOT / "knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251_v0.1.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_final_51_and_cumulative_251_exact():
    b1,b2,b3,cl = load(B1),load(B2),load(B3),load(CLOSURE)
    assert len(b3["records"]) == 51
    assert b3["source_batch"]["first"] == "CA07-692"
    assert b3["source_batch"]["last"] == "CA09-887"
    assert b3["cumulative_coverage"] == {"reviewed":251,"total":251,"remaining":0}
    ids=[r["source_rule_id"] for r in b1["records"]+b2["records"]+b3["records"]]
    assert len(ids)==251 and len(set(ids))==251
    assert cl["coverage"]["complete"] is True
    assert cl["coverage"]["unique_source_rule_ids"] == 251

def test_final_batch_source_order_and_markers_preserved():
    b3,src=load(B3),load(SRC3)
    assert [r["source_rule_id"] for r in b3["records"]] == [r["source_rule_id"] for r in src["records"]]
    for row,source in zip(b3["records"],src["records"]):
        assert row["source_markers"] == source["explicit_surface_markers"]

def test_all_final_antecedents_have_explicit_refs():
    b3=load(B3)
    rows=[r for r in b3["records"] if r["antecedent_mode"]!="NONE"]
    assert len(rows)==7
    assert all(r["antecedent_mode"]=="EXPLICIT_RULE_REFERENCE" for r in rows)
    assert all(r["antecedent_rule_ids"] for r in rows)

def test_final_negations_require_closed_world_evidence():
    b3=load(B3)
    rows=[r for r in b3["records"] if "NEGATION" in r["clause_operators"]]
    assert len(rows)==7
    for row in rows:
        assert row["absence_evaluation"]=="SOURCE_NEGATION_REQUIRES_CLOSED_WORLD_EVIDENCE"
        assert "CLOSED_WORLD_ABSENCE_EVIDENCE" in row["unresolved_blockers"]

def test_explicit_member_set_is_not_generic_literal_blocked():
    b3=load(B3)
    by={r["source_rule_id"]:r for r in b3["records"]}
    row=by["CA07-699"]
    assert "EXPLICIT_MEMBER_SET_LOCAL" in row["member_realization_modes"]
    assert "MIXED_OR_SOURCE_LITERAL" not in row["member_realization_modes"]

def test_emphasis_is_non_numeric_and_local():
    s3,b3=load(S3),load(B3)
    rows=[r for r in b3["records"] if r["emphasis_modifiers"]]
    assert {r["source_rule_id"] for r in rows} == {"CA08-701","CA08-800","CA09-805"}
    for row in rows:
        for x in row["emphasis_modifiers"]:
            assert x["semantics"]=="SOURCE_FOCUS_NON_NUMERIC"
            assert x["numeric_gain"] is None
            assert x["ordering_claim"] is None
    assert s3["guardrails"]["emphasis_numeric_gain_inferred"] is False
    assert s3["guardrails"]["emphasis_universal_order_inferred"] is False

def test_degree_language_stays_non_numeric():
    s3,b3=load(S3),load(B3)
    rows=[r for r in b3["records"] if r["severity_modifiers"]]
    assert {r["source_rule_id"] for r in rows} == {"CA09-885","CA09-887"}
    for row in rows:
        assert "SEVERITY_THRESHOLD_UNSPECIFIED" in row["unresolved_blockers"]
        assert all(x["numeric_threshold"] is None for x in row["severity_modifiers"])
    assert s3["guardrails"]["joint_degree_numeric_threshold_inferred"] is False

def test_v03_bounded_extension_of_v02():
    s2,s3=load(S2),load(S3)
    for invariant in s2["invariants"]:
        assert invariant in s3["invariants"]
    for op in s2["clause_operators"]:
        assert op in s3["clause_operators"]
    assert s3["guardrails"]["global_any_default"] is False
    assert s3["guardrails"]["global_all_default"] is False
    assert s3["guardrails"]["global_n_of_default"] is False

def test_closure_preserves_unknown_instead_of_forcing_execution():
    cl=load(CLOSURE)
    assert cl["interpretation"]["semantic_review_complete"] is True
    assert cl["interpretation"]["execution_complete"] is False
    assert cl["interpretation"]["source_underdetermined_is_valid_completion_state"] is True
    assert cl["legitimate_unknown_policy"]["generic_group_cardinality"] == "NO_UNIVERSAL_RULE"
    assert cl["legitimate_unknown_policy"]["non_numeric_severity_threshold"] == "NO_UNIVERSAL_THRESHOLD"
    assert cl["summary"]["source_resolution_changes"] == 0
    assert cl["summary"]["conditions_compiled"] == 0
    assert cl["summary"]["execution_unlocked"] == 0

def test_emphasis_does_not_become_activation_blocker():
    b3=load(B3)
    rows=[r for r in b3["records"] if r["emphasis_modifiers"]]
    assert rows
    for row in rows:
        assert "SOURCE_EMPHASIS_NON_NUMERIC_ONLY" not in row["unresolved_blockers"]

def test_closure_separates_unresolved_from_explicit_antecedents():
    cl=load(CLOSURE)
    assert cl["summary"]["unresolved_antecedent_reference_rows"] == 16
    assert cl["summary"]["explicit_antecedent_dependency_rows"] == 49
    follow=cl["targeted_followups"]["antecedent_source_recheck"]
    assert follow["count"] == 16
    assert len(follow["source_rule_ids"]) == 16
    assert follow["policy"] == "RECHECK_SOURCE_CONTEXT_BEFORE_PI;NEVER_GUESS_BY_ADJACENCY"

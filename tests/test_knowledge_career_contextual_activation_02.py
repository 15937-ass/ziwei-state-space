import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA1 = ROOT / "knowledge/activation/CONTEXTUAL_ACTIVATION_SEMANTICS_v0.1.json"
SCHEMA2 = ROOT / "knowledge/activation/CONTEXTUAL_ACTIVATION_SEMANTICS_v0.2.json"
BATCH1 = ROOT / "knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_01_v0.1.json"
BATCH2 = ROOT / "knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_02_v0.1.json"
SOURCE2 = ROOT / "knowledge/wp07c/CAREER_GROUP_LEXICON_REVIEW_02_v0.1.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_second_batch_exact_100_and_cumulative_200():
    b1, b2 = load(BATCH1), load(BATCH2)
    assert len(b2["records"]) == 100
    assert b2["source_batch"]["first"] == "CA04-383"
    assert b2["source_batch"]["last"] == "CA07-691"
    assert b2["cumulative_coverage"] == {"reviewed": 200, "total": 251, "remaining": 51}
    assert len(b1["records"]) + len(b2["records"]) == 200

def test_second_batch_matches_source_ids_order_and_markers():
    b2, src = load(BATCH2), load(SOURCE2)
    assert [r["source_rule_id"] for r in b2["records"]] == [r["source_rule_id"] for r in src["records"]]
    assert len({r["source_rule_id"] for r in b2["records"]}) == 100
    for row, source in zip(b2["records"], src["records"]):
        assert row["source_markers"] == source["explicit_surface_markers"]

def test_all_second_batch_antecedents_have_explicit_refs():
    b2 = load(BATCH2)
    rows = [r for r in b2["records"] if r["antecedent_mode"] != "NONE"]
    assert len(rows) == 28
    assert all(r["antecedent_mode"] == "EXPLICIT_RULE_REFERENCE" for r in rows)
    assert all(r["antecedent_rule_ids"] for r in rows)

def test_negation_requires_closed_world_evidence():
    b2 = load(BATCH2)
    rows = [r for r in b2["records"] if "NEGATION" in r["clause_operators"]]
    assert len(rows) == 10
    for row in rows:
        assert row["absence_evaluation"] == "SOURCE_NEGATION_REQUIRES_CLOSED_WORLD_EVIDENCE"
        assert "CLOSED_WORLD_ABSENCE_EVIDENCE" in row["unresolved_blockers"]

def test_explicit_necessity_is_local_and_not_global_default():
    schema = load(SCHEMA2)
    b2 = load(BATCH2)
    rows = [r for r in b2["records"] if "EXPLICIT_NECESSITY" in r["clause_operators"]]
    assert {r["source_rule_id"] for r in rows} == {"CA06-502", "CA06-532"}
    assert all(r["necessity_scope"] == "SOURCE_LOCAL_CLAUSE_ONLY" for r in rows)
    assert schema["guardrails"]["universal_necessity_default"] is False

def test_severity_stays_non_numeric():
    schema = load(SCHEMA2)
    b2 = load(BATCH2)
    rows = [r for r in b2["records"] if r["severity_modifiers"]]
    assert {r["source_rule_id"] for r in rows} == {"CA04-390", "CA04-393", "CA05-442", "CA06-506"}
    for row in rows:
        assert "SEVERITY_THRESHOLD_UNSPECIFIED" in row["unresolved_blockers"]
        assert all(x["numeric_threshold"] is None for x in row["severity_modifiers"])
        assert all(x["semantics"] == "SOURCE_ORDINAL_NON_NUMERIC" for x in row["severity_modifiers"])
    assert schema["guardrails"]["severity_numeric_threshold_inferred"] is False

def test_v02_is_bounded_extension_of_v01():
    s1, s2 = load(SCHEMA1), load(SCHEMA2)
    for invariant in s1["invariants"]:
        assert invariant in s2["invariants"]
    for op in s1["clause_operators"]:
        assert op in s2["clause_operators"]
    assert "EXPLICIT_NECESSITY" in s2["clause_operators"]
    assert "SEVERITY_MODIFIER_NON_NUMERIC" in s2["member_realization_modes"]

def test_no_global_quantifier_defaults_or_execution_unlock():
    schema, b2 = load(SCHEMA2), load(BATCH2)
    guard = schema["guardrails"]
    assert guard["global_any_default"] is False
    assert guard["global_all_default"] is False
    assert guard["global_n_of_default"] is False
    assert guard["database_missing_means_absent"] is False
    assert b2["summary"]["source_resolution_changes"] == 0
    assert b2["summary"]["conditions_compiled"] == 0
    assert b2["summary"]["execution_unlocked"] == 0
    assert all(r["source_quantifier_resolution"] == "UNRESOLVED_NO_DEFAULT" for r in b2["records"])
    assert all(not r["condition_compiled"] and not r["execution_unlocked"] for r in b2["records"])

def test_explicit_member_sets_drop_generic_literal_blocker():
    b2 = load(BATCH2)
    by_id = {r["source_rule_id"]: r for r in b2["records"]}
    for rule_id in ["CA05-419", "CA06-582", "CA07-638"]:
        row = by_id[rule_id]
        assert "EXPLICIT_MEMBER_SET_LOCAL" in row["member_realization_modes"]
        assert "MIXED_OR_SOURCE_LITERAL" not in row["member_realization_modes"]
        assert "SEMANTIC_NORMALIZATION_OR_QUANTIFIER_UNSPECIFIED" not in row["unresolved_blockers"]
        assert row["activation_status"] == "PARTIAL_LOCAL_STRUCTURE"

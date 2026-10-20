import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "knowledge/activation/CONTEXTUAL_ACTIVATION_SEMANTICS_v0.1.json"
DATA = ROOT / "knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_01_v0.1.json"
SOURCE = ROOT / "knowledge/wp07c/CAREER_GROUP_LEXICON_REVIEW_01_v0.1.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_exact_first_100_coverage():
    data = load(DATA)
    assert len(data["records"]) == 100
    assert data["source_batch"]["count"] == 100
    assert data["source_batch"]["first"] == "CA01-057"
    assert data["source_batch"]["last"] == "CA04-382"
    assert len({r["source_rule_id"] for r in data["records"]}) == 100

def test_same_source_ids_and_order_as_review_batch():
    data = load(DATA)
    source = load(SOURCE)
    assert [r["source_rule_id"] for r in data["records"]] == [r["source_rule_id"] for r in source["records"]]

def test_source_markers_are_preserved_verbatim():
    data = load(DATA)
    source = load(SOURCE)
    src = {r["source_rule_id"]: r["explicit_surface_markers"] for r in source["records"]}
    for row in data["records"]:
        assert row["source_markers"] == src[row["source_rule_id"]]

def test_explicit_operator_normalization_is_local_only():
    data = load(DATA)
    by_id = {r["source_rule_id"]: r for r in data["records"]}
    assert set(by_id["CA01-059"]["clause_operators"]) >= {"EXPLICIT_OR", "EXPLICIT_AND", "NEGATION"}
    assert "SIMULTANEOUS" in by_id["CA02-117"]["clause_operators"]
    schema = load(SCHEMA)
    assert "EXPLICIT_OR_DOES_NOT_IMPLY_GROUP_INTERNAL_ANY" in schema["invariants"]
    assert "SIMULTANEOUS_DOES_NOT_IMPLY_GROUP_ALL_UNLESS_MEMBERS_ARE_EXPLICIT" in schema["invariants"]

def test_all_negated_rows_require_closed_world_evidence():
    data = load(DATA)
    rows = [r for r in data["records"] if "NEGATION" in r["clause_operators"]]
    assert rows
    for row in rows:
        assert row["absence_evaluation"] == "SOURCE_NEGATION_REQUIRES_CLOSED_WORLD_EVIDENCE"
        assert "CLOSED_WORLD_ABSENCE_EVIDENCE" in row["unresolved_blockers"]

def test_antecedents_are_never_guessed_by_adjacency():
    data = load(DATA)
    for row in data["records"]:
        if row["antecedent_mode"] == "EXPLICIT_RULE_REFERENCE":
            assert row["antecedent_rule_ids"]
        if row["antecedent_mode"] == "ANTECEDENT_SURFACE_UNRESOLVED":
            assert row["antecedent_rule_ids"] == []
            assert "ANTECEDENT_DEPENDENCY" in row["unresolved_blockers"]
    assert load(SCHEMA)["guardrails"]["antecedent_guessed_by_adjacency"] is False

def test_no_global_member_quantifier_defaults():
    schema = load(SCHEMA)
    guard = schema["guardrails"]
    assert guard["global_any_default"] is False
    assert guard["global_all_default"] is False
    assert guard["global_n_of_default"] is False
    data = load(DATA)
    assert all(r["source_quantifier_resolution"] == "UNRESOLVED_NO_DEFAULT" for r in data["records"])

def test_relation_bound_rows_can_still_have_unresolved_member_realization():
    data = load(DATA)
    by_id = {r["source_rule_id"]: r for r in data["records"]}
    row = by_id["CA02-116"]
    assert row["relation_binding_available"] is True
    assert "SYMBOLIC_GROUP_UNSPECIFIED" in row["member_realization_modes"]
    assert row["condition_compiled"] is False

def test_no_execution_unlock_or_semantic_rewrite():
    data = load(DATA)
    assert data["summary"]["source_resolution_changes"] == 0
    assert data["summary"]["conditions_compiled"] == 0
    assert data["summary"]["execution_unlocked"] == 0
    for row in data["records"]:
        assert row["source_resolution_changed"] is False
        assert row["condition_compiled"] is False
        assert row["execution_unlocked"] is False
    guard = data["guardrails"]
    assert guard["source_truth_rewritten"] is False
    assert guard["product_runtime_modified"] is False
    assert guard["numeric_weights_added"] is False
    assert guard["probabilities_added"] is False

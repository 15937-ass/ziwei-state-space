import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "knowledge/core/wp07b/GAP011_NEGATION_SOURCE_AUDIT_v0.1.json"
TP01 = ROOT / "knowledge/wp05/property/PROPERTY_TP01_SOURCE_READJUDICATION_100_v0.1.json"
TP03 = ROOT / "knowledge/wp05/property/PROPERTY_TP03_SOURCE_READJUDICATION_100_v0.1.json"
TP01_CSV = ROOT / "knowledge/palaces/P10_property/wp07b/PROPERTY_TEMPORAL_REACTION_ELIGIBILITY_v0.1.csv"
GROUP_AUDIT = ROOT / "knowledge/core/wp07b/GAP006_GROUP_FAVORABILITY_SOURCE_AUDIT_v0.1.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def record(rows, key, value):
    return next(row for row in rows if row[key] == value)


def test_three_source_negative_rows_are_exactly_scoped():
    audit = load(AUDIT)
    assert [row["id"] for row in audit["records"]] == [
        "TP01-050", "TP01-061", "TP03-234"
    ]
    assert audit["gap_disposition"]["impacted_rule_ids"] == [
        "TP01-050", "TP01-061", "TP03-234"
    ]
    assert all(row["executable"] is False for row in audit["records"])


def test_tp01_negative_rows_preserve_source_conditions_and_parent():
    tp01 = load(TP01)["records"]
    r050 = record(tp01, "projection_rule_id", "TP01-050")
    r061 = record(tp01, "projection_rule_id", "TP01-061")
    assert r050["canonical_condition"] == "前格不见吉曜"
    assert r061["canonical_condition"] == "流年天机化忌不见煞"
    assert r050["projection_rule_id"] == "TP01-050"
    audit = load(AUDIT)
    a050 = record(audit["records"], "id", "TP01-050")
    assert a050["antecedent"] == "TP01-049"
    assert a050["executable"] is False


def test_tp03_preserves_seen_and_not_seen_branches():
    tp03 = load(TP03)["records"]
    r234 = record(tp03, "projection_rule_id", "TP03-234")
    assert r234["canonical_condition"] == "流年太阴落陷化忌不见煞"
    audit = load(AUDIT)
    a234 = record(audit["records"], "id", "TP03-234")
    assert a234["semantic_disposition"] == (
        "SOURCE_LOCAL_NEGATIVE_ALTERNATIVE_BRANCH_PRESERVE_CONTRAST"
    )
    assert "BRIGHTNESS_NOT_TEMPORAL_CONDITION_FACT" in a234["other_blockers_preserved"]


def test_existing_gap_register_keeps_all_three_rows_fail_closed():
    with TP01_CSV.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    selected = {row["projection_rule_id"]: row for row in rows if row["projection_rule_id"] in {
        "TP01-050", "TP01-061", "TP03-234"
    }}
    assert set(selected) == {"TP01-050", "TP01-061", "TP03-234"}
    assert all(row["eligibility_status"] == "FAIL_CLOSED" for row in selected.values())


def test_c5_open_world_boundary_is_not_overridden():
    c5 = load(GROUP_AUDIT)
    audit = load(AUDIT)
    assert c5["verdict"] == "SHARED_DESCRIPTIVE_TAXONOMY_ONLY"
    assert c5["scope_findings"]["career_scope_only"] is True
    assert audit["source_semantics"]["group_membership"]["吉曜"].startswith("OPEN_WORLD")
    assert audit["source_semantics"]["universal_closed_world_negation_supported"] is False
    assert audit["source_semantics"]["absence_from_incomplete_fact_snapshot_equals_source_absence"] is False


def test_no_shared_operator_or_runtime_unlock():
    audit = load(AUDIT)
    b = audit["boundaries"]
    assert audit["verdict"] == "DESCRIPTIVE_NEGATION_CLASSIFICATION_NO_EXECUTION"
    assert audit["gap_disposition"]["runtime_semantics_added"] is False
    assert audit["source_semantics"]["shared_executable_operator_created"] is False
    assert b["shared_schema_changed"] is False
    assert b["conditions_compiled"] == 0
    assert b["execution_unlocked"] == 0
    assert b["human_gate_required_now"] is False
    assert b["product_files_changed"] is False
    assert b["runtime_changed"] is False

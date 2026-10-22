import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "validation/wp05/M02_migration_projection_review_101_200.csv"
READJ = ROOT / "knowledge/palaces/P07_migration/wp05/MIGRATION_M02_SOURCE_READJUDICATION_100_v0.1.json"
TIME = ROOT / "knowledge/palaces/P07_migration/wp05/MIGRATION_M02_SOURCE_TIME_SCOPE_v0.1.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def candidate_rows():
    with CANDIDATE.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def test_candidate_census_and_source_binding():
    rows = candidate_rows()
    assert len(rows) == 100
    assert len({r["projection_rule_id"] for r in rows}) == 100
    assert rows[0]["projection_rule_id"] == "M02-101"
    assert rows[-1]["projection_rule_id"] == "M02-200"
    assert all(r["source_id"] == "SRC-ZZ-003" for r in rows)
    assert all(r["palace_id"] == "P07" for r in rows)
    assert all(r["source_span_verified"] == "true" for r in rows)

def test_case_and_path_dependent_sets_are_reconfirmed():
    rows = candidate_rows()
    case_ids = {r["projection_rule_id"] for r in rows if r["case_support_only"] == "true"}
    assert case_ids == {
        "M02-116", "M02-136", "M02-137", "M02-151", "M02-159", "M02-165",
        "M02-187", "M02-188", "M02-191", "M02-193", "M02-194"
    }
    history = {r["projection_rule_id"] for r in rows if r["history_feedback"]}
    assert history == {"M02-172", "M02-184", "M02-192", "M02-195"}

def test_readjudication_promotes_all_100_with_bounded_repairs():
    d = load(READJ)
    s = d["summary"]
    assert s["reviewed"] == 100
    assert s["canonical_promoted"] == 100
    assert s["reusable_projection_rules"] == 89
    assert s["case_support_only"] == 11
    assert s["history_feedback"] == 4
    assert s["source_resolution_changed_rows"] == [
        "M02-127", "M02-146", "M02-181", "M02-185", "M02-192", "M02-200"
    ]
    assert s["source_text_uncertainty_preserved"] == ["M02-181", "M02-185"]
    assert s["source_scan_resolved_rows"] == ["M02-150"]
    assert s["source_synthesis_rows"] == ["M02-174"]
    assert len(d["records"]) == 100
    assert len({r["projection_rule_id"] for r in d["records"]}) == 100

def test_source_repairs_preserve_conditional_structure():
    d = load(READJ)
    m = {r["projection_rule_id"]: r for r in d["records"]}
    assert "太阳天梁" in m["M02-127"]["canonical_condition"]
    assert m["M02-146"]["canonical_projection_target"] == "external_loss_and_setback"
    assert "连接字面存疑" in m["M02-181"]["canonical_condition"]
    assert m["M02-185"]["canonical_projection_target"] == "external_adversity_or_trouble"
    assert "或天同与天梁对拱" in m["M02-192"]["canonical_condition"]
    assert "malefics_intensify_loss_and_trouble" in m["M02-200"]["canonical_projection_target"]
    assert all(r["canonical_promotion"] is True for r in d["records"])

def test_temporal_scope_does_not_create_a_new_layer_or_runtime_permission():
    d = load(TIME)
    assert d["chapter_scope"]["source_layers"] == ["NATAL", "DECADE", "YEAR", "MONTH"]
    overlay = d["event_relative_overlay"]
    assert overlay["overlay_id"] == "MIGRATION_FIRST_THREE_YEARS"
    assert overlay["human_gate"] == "HG-P07-TEMPORAL-01-A"
    assert overlay["active_year_index"] == [1, 2, 3]
    assert overlay["seventh_calendar_layer"] is False
    assert overlay["generic_event_timer"] is False
    assert overlay["change_in_M02"] is False
    assert d["default_star_system_records"]["runtime_eligibility_granted"] is False

def test_no_new_quantitative_or_shared_semantics():
    d = load(READJ)["summary"]
    for key in [
        "new_primitive_qi", "new_memory_type", "new_independent_time_scale",
        "new_shared_group_semantics", "numeric_weight", "probability", "decay"
    ]:
        assert d[key] == 0

def test_wuqu_adverse_passage_overlap_is_not_double_counted():
    d = load(READJ)
    m = {r["projection_rule_id"]: r for r in d["records"]}
    group = "WUQU_SA_PO_ADVERSE_OUTCOME"
    assert {m[x]["source_overlap_group"] for x in ["M02-146", "M02-171", "M02-172"]} == {group}
    assert m["M02-171"]["disposition"] == "SOURCE_OVERLAP_NOT_INDEPENDENT_SIGNAL"
    assert m["M02-171"]["source_overlap_role"] == "OVERLAPPING_RESTATEMENT_NOT_INDEPENDENT_SIGNAL"
    assert m["M02-172"]["source_overlap_role"] == "ORDERED_PROLONGED_STAY_TAIL_PATH_DEPENDENT"
    assert d["summary"]["source_overlap_groups"][0]["record_ids"] == ["M02-146", "M02-171", "M02-172"]

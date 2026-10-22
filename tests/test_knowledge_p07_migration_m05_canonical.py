import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "validation/wp05/M05_migration_projection_review_401_500.csv"
READJ = ROOT / "knowledge/palaces/P07_migration/wp05/MIGRATION_M05_SOURCE_READJUDICATION_100_v0.1.json"
TIME = ROOT / "knowledge/palaces/P07_migration/wp05/MIGRATION_M05_SOURCE_TIME_SCOPE_v0.1.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def candidate_rows():
    with CANDIDATE.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def records_by_id():
    return {r["projection_rule_id"]: r for r in load(READJ)["records"]}


def test_candidate_census_and_source_page_corrections():
    rows = candidate_rows()
    ids = [r["projection_rule_id"] for r in rows]
    assert len(rows) == 100 and len(set(ids)) == 100
    assert ids == [f"M05-{i}" for i in range(401, 501)]
    d = load(READJ)
    assert len(d["records"]) == 100
    assert all(r["source_id"] == "SRC-ZZ-003" for r in rows)
    assert all(r["canonical_promotion"] for r in d["records"])
    changed = {r["projection_rule_id"] for r in d["records"] if r["source_span_changed"]}
    expected = ({f"M05-{i}" for i in range(401, 424)}
                | {f"M05-{i}" for i in range(456, 463)}
                | {f"M05-{i}" for i in range(490, 501)})
    assert changed == expected
    assert len(changed) == d["summary"]["source_span_changed_count"] == 41
    r = records_by_id()
    assert r["M05-401"]["source_location"] == "SRC-ZZ-003 printed p117"
    assert r["M05-405"]["source_location"] == "SRC-ZZ-003 printed p117"
    assert r["M05-410"]["source_location"] == "SRC-ZZ-003 printed p117"
    assert r["M05-419"]["source_location"] == "SRC-ZZ-003 printed pp117–118"
    assert r["M05-424"]["source_location"] == "SRC-ZZ-003 printed p118"
    assert r["M05-456"]["source_location"] == "SRC-ZZ-003 printed p118"
    assert r["M05-461"]["source_location"] == "SRC-ZZ-003 printed p118"
    assert r["M05-462"]["source_location"] == "SRC-ZZ-003 printed pp118–119"
    assert r["M05-463"]["source_location"] == "SRC-ZZ-003 printed p119"
    assert r["M05-490"]["source_location"] == "SRC-ZZ-003 printed p119"


def test_all_antecedents_are_explicit_and_counts_reconcile():
    d = load(READJ)
    assert all(not any(x in r["canonical_condition"] for x in ["前格", "前述", "同上格局"])
               for r in d["records"])
    s = d["summary"]
    assert s["reviewed"] == 100 and s["canonical_promoted"] == 100
    assert s["source_condition_normalization_count"] == len(s["source_condition_normalized_rows"])
    assert s["source_resolution_change_count"] == len(s["source_resolution_changed_rows"])
    assert s["source_span_changed_count"] == len(s["source_span_changed_rows"]) == 41
    assert s["source_time_layer_changed_rows"] == []
    assert s["reusable_projection_rules"] == 90
    assert s["case_support_only"] == 10
    assert set(s["case_support_only_ids"]) == {
        "M05-407", "M05-423", "M05-431", "M05-445", "M05-453",
        "M05-454", "M05-455", "M05-466", "M05-476", "M05-489"
    }
    assert s["history_feedback"] == 0
    assert s["path_dependent_gate_reclassified_rows"] == ["M05-455", "M05-487"]
    assert s["canonical_path_dependent_gate_ids"] == []
    assert s["cumulative_reviewed_after_batch"] == 500
    assert s["cumulative_reusable_projection_rules_after_batch"] == 443
    assert s["cumulative_case_support_only_after_batch"] == 57
    assert s["cumulative_history_feedback_after_batch"] == 10


def test_m04_source_gaps_close_without_duplicate_evidence():
    d = load(READJ)
    resolution = {x["prior_gap_id"]: x for x in d["gap_resolution_map"]}
    assert resolution["P07-M04-GAP-001"]["mapped_to"] == ["M05-408", "M05-409"]
    assert resolution["P07-M04-GAP-002"]["mapped_to"] == ["M05-401", "M05-402", "M05-403", "M05-404"]
    assert resolution["P07-M04-GAP-003"]["mapped_to"] == ["M05-405", "M05-406", "M05-407"]
    assert all(x["status"] == "SOURCE_COVERED_IN_M05" for x in resolution.values())
    assert len(d["source_coverage_gaps"]) == d["summary"]["new_source_coverage_gap_count"] == 4
    assert {g["gap_id"] for g in d["carried_forward_source_gaps"]} == {
        "P07-M03-GAP-001", "P07-M03-GAP-012"
    }


def test_source_specific_repairs_and_overlap_groups():
    d = load(READJ)
    r = records_by_id()
    condition_423 = r["M05-423"]["canonical_condition"]
    assert "煞曜" in condition_423 and "刑耗诸星同会" in condition_423
    assert "怨罔" not in r["M05-423"]["canonical_condition"]
    assert "或" in r["M05-431"]["canonical_condition"]
    assert "魁钺与辅弼同会" in r["M05-447"]["canonical_condition"]
    assert r["M05-447"]["canonical_condition"] == r["M05-448"]["canonical_condition"]
    assert r["M05-455"]["case_support_only"] is True
    assert r["M05-455"]["history_feedback"] is None
    assert r["M05-455"]["path_dependent_gate_reclassified"] is True
    assert r["M05-487"]["history_feedback"] is None
    assert r["M05-487"]["path_dependent_gate_reclassified"] is True
    groups = {g["group_id"]: set(g["record_ids"]) for g in d["summary"]["source_overlap_groups"]}
    assert len(groups) == 23
    assert {"M05-401", "M05-402", "M05-403", "M05-404"} <= groups["JUMEN_MAOYOU_RELOCATION"]
    assert {"M05-447", "M05-448", "M05-449"} <= groups["TIANLIANG_AUSPICIOUS_SUPPORT"]
    assert {"M05-490", "M05-491", "M05-492", "M05-493"} <= groups["QISHA_MOVEMENT_TRIGGER"]


def test_time_scope_is_bounded_and_overlay_unchanged():
    d = load(TIME)
    assert d["chapter_scope"]["source_layers"] == ["NATAL", "DECADE", "YEAR", "MONTH"]
    assert len(d["records"]) == 100
    assert all(set(r["source_time_layers"]) <= {"NATAL", "DECADE", "YEAR", "MONTH"} for r in d["records"])
    by_id = {r["projection_rule_id"]: r for r in d["records"]}
    year_ids = {f"M05-{i}" for i in [405, 406, 407, 409, 444, 445, 488, 489]}
    assert {k for k, v in by_id.items() if v["source_time_layers"] == ["YEAR"]} == year_ids
    assert by_id["M05-409"]["scope_status"] == "YEAR_FLOWING_LU_TRIGGER_PRESERVED_WITHOUT_GENERIC_TIMER"
    overlay = d["event_relative_overlay"]
    assert overlay["overlay_id"] == "MIGRATION_FIRST_THREE_YEARS"
    assert overlay["human_gate"] == "HG-P07-TEMPORAL-01-A"
    assert overlay["active_year_index"] == [1, 2, 3]
    assert not overlay["seventh_calendar_layer"]
    assert not overlay["generic_event_timer"]
    assert not overlay["change_in_M05"]
    assert d["path_dependent_gate_audit"]["canonical_flags"] == []


def test_no_new_semantics_and_source_gap_inventory():
    d = load(READJ)
    s = d["summary"]
    for key in ["new_primitive_qi", "new_memory_type", "new_independent_time_scale",
                "new_shared_group_semantics", "numeric_weight", "probability", "decay",
                "product_runtime_change"]:
        assert s[key] == 0
    assert d["source_basis"]["printed_pages"] == "117–120"
    assert d["source_basis"]["pdf_scan_pages"] == [59, 60]
    assert {g["gap_id"] for g in d["source_coverage_gaps"]} == {
        "P07-M05-GAP-001", "P07-M05-GAP-002", "P07-M05-GAP-003", "P07-M05-GAP-004"
    }

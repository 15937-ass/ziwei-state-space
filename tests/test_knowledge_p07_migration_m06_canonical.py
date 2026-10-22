import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "validation/wp05/M06_migration_projection_final_tail_501_590.csv"
READJ = ROOT / "knowledge/palaces/P07_migration/wp05/MIGRATION_M06_SOURCE_READJUDICATION_090_v0.1.json"
TIME = ROOT / "knowledge/palaces/P07_migration/wp05/MIGRATION_M06_SOURCE_TIME_SCOPE_v0.1.json"
STATE = ROOT / "knowledge/states/P07_MIGRATION_STATE.yaml"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def candidate_rows():
    with CANDIDATE.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def records_by_id():
    return {r["projection_rule_id"]: r for r in load(READJ)["records"]}


def test_candidate_census_and_printed_page_corrections():
    rows = candidate_rows()
    ids = [r["projection_rule_id"] for r in rows]
    assert len(rows) == 90 and len(set(ids)) == 90
    assert ids == [f"M06-{i}" for i in range(501, 591)]
    d = load(READJ)
    assert len(d["records"]) == 90
    assert len({r["projection_rule_id"] for r in d["records"]}) == 90
    r = records_by_id()
    assert r["M06-501"]["source_location"] == "SRC-ZZ-003 printed p119"
    assert r["M06-518"]["source_location"] == "SRC-ZZ-003 printed p119"
    assert r["M06-519"]["source_location"] == "SRC-ZZ-003 printed p120"
    assert r["M06-578"]["source_location"] == "SRC-ZZ-003 printed p120"
    assert r["M06-579"]["source_location"] == "SRC-ZZ-003 printed p121"
    assert r["M06-589"]["source_location"] == "SRC-ZZ-003 printed p121"
    assert r["M06-590"]["source_location"] == "SRC-ZZ-003 printed p122"
    changed = {x["projection_rule_id"] for x in d["records"] if x["source_span_changed"]}
    expected = ({f"M06-{i}" for i in range(501, 519)}
                | {f"M06-{i}" for i in range(567, 579)}
                | {f"M06-{i}" for i in range(587, 590)})
    assert changed == expected
    assert len(changed) == d["summary"]["source_span_changed_count"] == 33


def test_all_antecedents_are_explicit_and_boundary_is_not_a_rule():
    d = load(READJ)
    r = records_by_id()
    assert all(not any(x in xrow["canonical_condition"] for x in ["前格", "前述", "同上格局"])
               for xrow in d["records"])
    assert all(r[f"M06-{i}"]["source_condition_normalized"] for i in range(501, 590))
    assert r["M06-590"]["canonical_promotion"] is False
    assert r["M06-590"]["disposition"] == "SOURCE_BOUNDARY_MARKER_NOT_RULE"
    assert "交友宫" in r["M06-590"]["source_literal_claim"]
    assert d["summary"]["reviewed"] == 90
    assert d["summary"]["canonical_promoted"] == 89
    assert d["summary"]["source_condition_normalization_count"] == 89
    assert d["summary"]["source_condition_shorthand_expanded_count"] == 24
    assert d["summary"]["source_boundary_markers"] == 1


def test_case_only_counts_and_cumulative_reconciliation():
    d = load(READJ)
    s = d["summary"]
    assert s["reusable_projection_rules"] == 76
    assert s["case_support_only"] == 13
    assert set(s["case_support_only_ids"]) == {
        "M06-521", "M06-522", "M06-523", "M06-529", "M06-530", "M06-531",
        "M06-542", "M06-560", "M06-572", "M06-579", "M06-580", "M06-583", "M06-586"
    }
    assert all(records_by_id()[rid]["case_support_reason"] for rid in s["case_support_only_ids"])
    assert s["cumulative_reviewed_after_batch"] == 590
    assert s["cumulative_reusable_projection_rules_after_batch"] == 519
    assert s["cumulative_case_support_only_after_batch"] == 70
    assert s["cumulative_source_boundary_markers_after_batch"] == 1
    assert 519 + 70 + 1 == 590
    legacy = s["legacy_tail_summary_reconciliation"]
    assert legacy["archived_claimed_cumulative_reusable"] == 521
    assert legacy["archived_claimed_cumulative_case_support_only"] == 69
    assert legacy["reconciled_cumulative_reusable"] == 519
    assert legacy["reconciled_cumulative_case_support_only"] == 70


def test_year_scope_and_path_sequence_audit():
    d = load(READJ)
    t = load(TIME)
    assert len(t["records"]) == 90
    assert t["chapter_scope"]["source_layers"] == ["NATAL", "DECADE", "YEAR", "MONTH"]
    by_id = {x["projection_rule_id"]: x for x in t["records"]}
    year_ids = {f"M06-{i}" for i in [540, 541, 542]}
    assert {k for k, v in by_id.items() if v["source_time_layers"] == ["YEAR"]} == year_ids
    assert by_id["M06-590"]["source_time_layers"] == []
    assert t["event_relative_overlay"]["overlay_id"] == "MIGRATION_FIRST_THREE_YEARS"
    assert t["event_relative_overlay"]["human_gate"] == "HG-P07-TEMPORAL-01-A"
    assert t["event_relative_overlay"]["active_year_index"] == [1, 2, 3]
    assert not t["event_relative_overlay"]["seventh_calendar_layer"]
    assert not t["event_relative_overlay"]["generic_event_timer"]
    assert not t["event_relative_overlay"]["change_in_M06"]
    audit = t["path_dependent_gate_audit"]
    assert audit["historical_flags"] == ["M06-579"]
    assert audit["canonical_flags"] == []
    assert audit["history_feedback_rows"] == 0
    r = records_by_id()["M06-579"]
    assert r["archived_history_feedback"] == "PATH_DEPENDENT_GATE"
    assert r["history_feedback"] is None
    assert r["path_dependent_gate_reclassified"] is True
    assert r["source_sequence_not_history_gate"] is True
    assert r["case_support_only"] is True


def test_alternatives_cross_palace_constraints_and_source_gaps():
    r = records_by_id()
    assert "火铃" in r["M06-514"]["canonical_condition"]
    assert "空劫" in r["M06-515"]["canonical_condition"]
    assert "廉贞化忌、武曲化忌来会" in r["M06-542"]["canonical_condition"]
    assert "或" not in r["M06-542"]["canonical_condition"]
    assert "命宫天府" in r["M06-517"]["canonical_condition"]
    assert "禄存与破军对拱" in r["M06-547"]["canonical_condition"]
    d = load(READJ)
    assert d["source_coverage_gaps"] == []
    assert {g["gap_id"] for g in d["carried_forward_source_gaps"]} == {
        "P07-M05-GAP-001", "P07-M05-GAP-002", "P07-M05-GAP-003", "P07-M05-GAP-004",
        "P07-M03-GAP-001", "P07-M03-GAP-012"
    }
    assert d["summary"]["carried_forward_source_gap_count"] == 6


def test_no_new_semantics_and_state_points_to_issue():
    d = load(READJ)
    s = d["summary"]
    for key in ["new_primitive_qi", "new_memory_type", "new_independent_time_scale",
                "new_shared_group_semantics", "numeric_weight", "probability", "decay",
                "product_runtime_change"]:
        assert s[key] == 0
    state = STATE.read_text(encoding="utf-8")
    assert "active_issue: 645" in state
    assert "knowledge/p07-645-migration-m06-canonical" in state
    assert 'status: "SOURCE_REVIEW_IN_PROGRESS"' in state
    assert "HG-P07-TEMPORAL-01-A" in state
    assert "No Product runtime authorization is implied" in state

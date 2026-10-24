import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "knowledge" / "palaces" / "P01_life" / "wp05"
STATE = ROOT / "knowledge" / "states" / "P01_LIFE_STATE.yaml"


def read_csv(name):
    with (BASE / name).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def read_json(name):
    return json.loads((BASE / name).read_text(encoding="utf-8"))


def test_p01_pojun_source_first_record_census_and_case_only_boundary():
    rows = read_csv("LIFE_P08_SOURCE_READJUDICATION_701_800_v0.1.csv")
    assert len(rows) == 51
    assert [r["projection_rule_id"] for r in rows] == [f"P01-{i:03d}" for i in range(701, 752)]
    assert all(r["source_id"] == "SRC-ZZ-003" for r in rows)
    assert all(r["canonical_promotion"] == "true" for r in rows)
    assert all(r["source_resolution_changed"] == "true" for r in rows)
    assert sum(r["case_support_only"] == "true" for r in rows) == 13
    by = {r["projection_rule_id"]: r for r in rows}
    assert "printed p22 bottom" in by["P01-701"]["source_location"]
    assert "14 破军" in by["P01-701"]["source_location"]
    assert "主立刻发生改变" in by["P01-714"]["source_literal_claim"]
    assert by["P01-714"]["source_text_uncertainty"]
    for rule_id in ("P01-702", "P01-703", "P01-708", "P01-711", "P01-720", "P01-721", "P01-732", "P01-736", "P01-741", "P01-742", "P01-743", "P01-746", "P01-749"):
        assert by[rule_id]["case_support_only"] == "true"
    assert "迁移宫" in by["P01-725"]["cross_palace_dependency"]
    assert "夫妻宫" in by["P01-749"]["cross_palace_dependency"]
    assert "流年大限" in by["P01-744"]["source_literal_claim"]


def test_p01_pojun_time_scope_preserves_explicit_and_generic_words():
    data = read_json("LIFE_P08_SOURCE_TIME_SCOPE_701_800_v0.1.json")
    rows = {r["projection_rule_id"]: r for r in data["records"]}
    assert len(rows) == 51
    assert rows["P01-730"]["source_time_layers"] == []
    assert rows["P01-730"]["scope_status"] == "SOURCE_GENERIC_PERIOD_NOT_NARROWED"
    assert rows["P01-731"]["source_time_layers"] == ["YEAR"]
    assert rows["P01-731"]["scope_status"] == "SOURCE_EXPLICIT_YEAR_WITH_GENERIC_PERIOD_UNRESOLVED"
    assert rows["P01-733"]["source_time_layers"] == ["DECADE"]
    assert rows["P01-744"]["source_time_layers"] == ["DECADE", "YEAR"]
    assert rows["P01-750"]["source_time_layers"] == ["DECADE", "YEAR"]
    assert rows["P01-735"]["source_time_layers"] == []
    assert rows["P01-735"]["scope_status"] == "SOURCE_LIFE_STAGE_WORD_RETAINED_NO_NEW_TIME_LAYER"


def test_p01_pojun_gap_ledger_summary_state_and_boundary_correction_reconcile():
    summary = read_json("LIFE_P08_SOURCE_READJUDICATION_SUMMARY_v0.1.json")
    s = summary["summary"]
    assert (s["historical_candidates_reviewed"], s["canonical_promoted"], s["new_canonical_records"]) == (0, 51, 51)
    assert (s["reusable_projection_rules"], s["case_support_only"]) == (38, 13)
    assert (s["cumulative_canonical_records_after_merge"], s["cumulative_reusable_projection_rules_after_merge"], s["cumulative_case_support_only_after_merge"]) == (933, 783, 150)
    assert s["registered_gaps_closed"] == ["P01-SRC-GAP-028"]
    assert s["new_source_gap_supplement_records"] == 0
    assert s["cumulative_source_gap_supplement_records_after_merge"] == 47
    assert summary["human_gate_required"] is False
    assert summary["product_runtime_authorization"] is False
    assert summary["post_merge_boundary_correction"]["verified_correction"].startswith("Printed p22 bottom")

    ledger = read_json("LIFE_P03_SOURCE_GAP_LEDGER_v0.1.json")
    entries = {g["gap_id"]: g for g in ledger["entries"]}
    assert entries["P01-SRC-GAP-027"]["status"] == "CLOSED_BY_SOURCE_RECHECK_AND_CANONICAL_RULES"
    assert "immediately before the heading 14 破军" in entries["P01-SRC-GAP-027"]["source_location"]
    gap = entries["P01-SRC-GAP-028"]
    assert gap["status"] == "CLOSED_BY_SOURCE_RECHECK_AND_CANONICAL_RULES"
    assert len(gap["rule_ids"]) == 51
    assert gap["rule_ids"][0] == "P01-701" and gap["rule_ids"][-1] == "P01-751"
    assert "printed p22 bottom" in gap["source_location"] and "printed p24" in gap["source_location"]
    assert ledger["unresolved_gap_ids"] == []
    assert ledger["next_checkpoint_gaps"] == []
    assert "P01 source audit complete through printed p24" in ledger["next_source_anchor"]

    state = STATE.read_text(encoding="utf-8")
    assert "canonical_source_records_on_main: 933" in state
    assert "cumulative_reusable_projection_rules_after_merge: 783" in state
    assert "cumulative_case_support_only_after_merge: 150" in state
    assert "next_source_gap_id: null" in state
    assert "P01 source audit complete through printed p24" in state
    assert "No Product/runtime authorization is implied" in state


def test_p01_previous_handoff_carries_post_merge_boundary_correction():
    report = (BASE / "LIFE_P07_SOURCE_READJUDICATION_601_700_v0.1.md").read_text(encoding="utf-8")
    assert "Post-merge boundary correction (Issue #714)" in report
    assert "printed p22 bottom" in report
    assert "printed p25" in report
    assert "6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c" in report

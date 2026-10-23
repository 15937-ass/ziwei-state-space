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


def test_p07_candidate_census_and_source_first_dispositions():
    rows = read_csv("LIFE_P07_SOURCE_READJUDICATION_601_700_v0.1.csv")
    assert len(rows) == 100
    assert [r["projection_rule_id"] for r in rows] == [f"P01-{i:03d}" for i in range(601, 701)]
    assert all(r["source_id"] == "SRC-ZZ-003" for r in rows)
    assert sum(r["canonical_promotion"] == "true" for r in rows) == 88
    assert sum(r["canonical_promotion"] == "false" for r in rows) == 12
    assert {r["projection_rule_id"] for r in rows if r["canonical_promotion"] == "false"} == {f"P01-{i:03d}" for i in range(601, 613)}
    assert all(r["disposition"] == "DEDUPLICATED_TO_EXISTING_CANONICAL" for r in rows[:12])
    assert all(r["source_resolution_changed"] == "true" for r in rows)
    assert sum(r["case_support_only"] == "true" for r in rows if r["canonical_promotion"] == "true") == 3
    by = {r["projection_rule_id"]: r for r in rows}
    assert "P01-SG-203" in by["P01-601"]["notes"]
    assert "P01-SG-208" in by["P01-612"]["notes"]
    assert "printed p20" in by["P01-613"]["source_location"]
    assert "printed p22" in by["P01-700"]["source_location"]
    assert by["P01-636"]["case_support_only"] == "true"
    assert by["P01-658"]["case_support_only"] == "true"
    assert by["P01-669"]["case_support_only"] == "true"
    assert "雄宿乾无格" in by["P01-656"]["source_text_uncertainty"]
    assert "雄宿乾元格" in by["P01-660"]["source_literal_claim"]
    assert "雄宿乾无格" in by["P01-686"]["source_text_uncertainty"]
    assert "不静默归一" in by["P01-662"]["source_text_uncertainty"]


def test_p07_source_gap_supplements_and_case_only_boundary():
    rows = read_csv("LIFE_P07_SOURCE_GAP_SUPPLEMENT_PP20_22_v0.1.csv")
    assert len(rows) == 5
    assert [r["projection_rule_id"] for r in rows] == [f"P01-SG-{i:03d}" for i in range(210, 215)]
    assert {r["source_gap_id"] for r in rows} == {"P01-SRC-GAP-027"}
    assert all(r["canonical_promotion"] == "true" for r in rows)
    assert sum(r["case_support_only"] == "true" for r in rows) == 1
    by = {r["projection_rule_id"]: r for r in rows}
    assert "不能相制为用" in by["P01-SG-210"]["source_literal_claim"]
    assert "福德宫紫微化权" in by["P01-SG-211"]["canonical_condition"]
    assert by["P01-SG-211"]["cross_palace_dependency"] == "福德宫紫微化权"
    assert "贪狼同时影响福德宫" in by["P01-SG-213"]["canonical_normalization"]
    assert "易发易破" in by["P01-SG-214"]["source_literal_claim"]
    assert by["P01-SG-211"]["case_support_only"] == "true"


def test_p07_time_scope_preserves_source_native_words():
    data = read_json("LIFE_P07_SOURCE_TIME_SCOPE_601_700_v0.1.json")
    rows = {r["projection_rule_id"]: r for r in data["records"]}
    assert len(rows) == 100
    assert rows["P01-609"]["source_time_layers"] == ["DECADE", "YEAR"]
    assert rows["P01-609"]["scope_status"] == "DEDUPLICATED_SCOPE_METADATA_TO_P01-SG-208"
    assert rows["P01-616"]["source_time_layers"] == ["DECADE", "YEAR"]
    assert rows["P01-616"]["scope_status"] == "SOURCE_EXPLICIT_MULTI_LAYER_WITH_GENERIC_PERIOD_UNRESOLVED"
    assert rows["P01-654"]["source_time_layers"] == ["DECADE", "YEAR"]
    assert rows["P01-654"]["scope_status"] == "SOURCE_EXPLICIT_DECADE_OR_YEAR_ALTERNATIVE"
    assert rows["P01-659"]["source_time_layers"] == []
    assert rows["P01-659"]["scope_status"] == "SOURCE_GENERIC_PERIOD_NOT_NARROWED"
    assert rows["P01-665"]["source_time_layers"] == []
    assert rows["P01-665"]["scope_status"] == "SOURCE_GENERIC_PERIOD_NOT_NARROWED"
    assert rows["P01-666"]["source_time_layers"] == ["YEAR"]
    assert rows["P01-682"]["source_time_layers"] == ["YEAR"]
    assert rows["P01-682"]["scope_status"] == "SOURCE_EXPLICIT_YEAR_WITH_GENERIC_PERIOD_UNRESOLVED"
    assert rows["P01-698"]["source_time_layers"] == ["DECADE", "YEAR"]
    assert rows["P01-698"]["scope_status"] == "SOURCE_EXPLICIT_DECADE_AND_YEAR"
    assert rows["P01-688"]["source_time_layers"] == []
    assert rows["P01-688"]["scope_status"] == "SOURCE_TEMPORAL_LAYER_UNSPECIFIED"


def test_p07_gap_ledger_and_cumulative_counts():
    summary = read_json("LIFE_P07_SOURCE_READJUDICATION_SUMMARY_v0.1.json")
    s = summary["summary"]
    assert (s["historical_candidates_reviewed"], s["canonical_promoted"], s["deduplicated_scope_metadata_rows"]) == (100, 88, 12)
    assert (s["new_source_gap_supplement_records"], s["new_canonical_records"]) == (5, 93)
    assert (s["candidate_reusable_projection_rules"], s["candidate_case_support_only"]) == (85, 3)
    assert (s["gap_supplement_reusable_projection_rules"], s["gap_supplement_case_support_only"]) == (4, 1)
    assert (s["reusable_projection_rules"], s["case_support_only"]) == (89, 4)
    assert (s["cumulative_canonical_records_after_merge"], s["cumulative_reusable_projection_rules_after_merge"], s["cumulative_case_support_only_after_merge"]) == (882, 745, 137)
    assert s["registered_gaps_closed"] == ["P01-SRC-GAP-027"]
    assert s["new_primitive_qi"] == s["new_memory_type"] == s["new_independent_time_scale"] == 0
    assert s["numeric_weight"] == s["probability"] == s["decay"] == 0
    assert summary["human_gate_required"] is False
    assert summary["product_runtime_authorization"] is False

    ledger = read_json("LIFE_P03_SOURCE_GAP_LEDGER_v0.1.json")
    entries = {g["gap_id"]: g for g in ledger["entries"]}
    gap = entries["P01-SRC-GAP-027"]
    assert gap["status"] == "CLOSED_BY_SOURCE_RECHECK_AND_CANONICAL_RULES"
    assert len(gap["rule_ids"]) == 93
    assert "P01-613" in gap["rule_ids"] and "P01-SG-214" in gap["rule_ids"]
    next_gap = ledger["next_checkpoint_gaps"][0]
    assert next_gap["gap_id"] == "P01-SRC-GAP-028"
    assert "printed p23" in next_gap["source_location"]
    assert "破军" in next_gap["source_claim"]
    assert "P01-701" in ledger["next_source_anchor"]
    state = STATE.read_text(encoding="utf-8")
    assert "canonical_source_records_on_main: 882" in state
    assert "cumulative_reusable_projection_rules_after_merge: 745" in state
    assert "cumulative_case_support_only_after_merge: 137" in state
    assert "P01-701…P01-800" in state
    assert "No Product/runtime authorization is implied" in state


def test_p07_report_records_verified_scan_boundary_and_text_variants():
    report = (BASE / "LIFE_P07_SOURCE_READJUDICATION_601_700_v0.1.md").read_text(encoding="utf-8")
    assert "6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c" in report
    assert "printed p20 bottom through printed p22" in report
    assert "Printed p23 begins 破军 prose" in report
    assert "雄宿乾无格" in report and "雄宿乾元格" in report
    assert "No Product/runtime authorization is implied" in report

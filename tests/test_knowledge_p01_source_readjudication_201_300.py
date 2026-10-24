import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "knowledge" / "palaces" / "P01_life" / "wp05"


def _read_csv(path):
    with (BASE / path).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def test_p03_candidate_census_and_dedup():
    rows = _read_csv("LIFE_P03_SOURCE_READJUDICATION_201_300_v0.1.csv")
    assert len(rows) == 100
    assert [r["projection_rule_id"] for r in rows] == [f"P03-{i:03d}" for i in range(201, 301)]
    assert all(r["source_id"] == "SRC-ZZ-003" for r in rows)
    assert sum(r["canonical_promotion"] == "true" for r in rows) == 98
    assert {r["projection_rule_id"] for r in rows if r["canonical_promotion"] == "false"} == {"P03-215", "P03-229"}
    assert all(r["case_support_only"] in {"true", "false"} for r in rows)


def test_p03_source_first_repairs():
    rows = {r["projection_rule_id"]: r for r in _read_csv("LIFE_P03_SOURCE_READJUDICATION_201_300_v0.1.csv")}
    assert rows["P03-202"]["cross_palace_dependency"] == ""
    assert "不据此推导固定父母宫依赖" in rows["P03-202"]["notes"]
    assert rows["P03-225"]["cross_palace_dependency"] == "寅宫巨阳（借会）"
    assert rows["P03-227"]["canonical_condition"].count("或") == 1
    assert rows["P03-231"]["cross_palace_dependency"] == ""
    assert rows["P03-231"]["canonical_condition"] == "P03-230结构；女命行至天相运"
    assert "不推广至所有子午同阴女命" in rows["P03-231"]["canonical_normalization"]
    assert rows["P03-269"]["cross_palace_dependency"] == ""
    assert rows["P03-278"]["opposite_palace_dependency"] == "破军化禄（对宫）"
    assert "中局" in rows["P03-288"]["source_literal_claim"]
    assert "小康" not in rows["P03-288"]["source_literal_claim"]
    assert "刑耗煞曜" in rows["P03-294"]["canonical_condition"]
    assert "火铃同会" in rows["P03-295"]["canonical_condition"]
    assert rows["P03-296"]["case_support_only"] == "true"
    assert "不成格者与寅宫同断" in rows["P03-300"]["source_literal_claim"]
    assert rows["P03-222"]["history_dependency"].startswith("EXISTING_HISTORY_SCHEMA_")
    assert rows["P03-287"]["history_dependency"].startswith("EXISTING_HISTORY_SCHEMA_")


def test_p03_time_scope_keeps_source_words():
    data = json.loads((BASE / "LIFE_P03_SOURCE_TIME_SCOPE_v0.1.json").read_text(encoding="utf-8"))
    rows = {r["projection_rule_id"]: r for r in data["records"]}
    assert len(rows) == 100
    assert rows["P03-212"]["source_time_expression"] == "无论大限流年均如是"
    assert rows["P03-228"]["source_time_expression"] == "无论流年或大限"
    assert rows["P03-232"]["source_time_expression"] == "年运"
    assert rows["P03-231"]["source_time_expression"] == "天相运"
    assert rows["P03-274"]["source_time_expression"] == "行至天同宫垣"
    assert rows["P03-275"]["source_time_expression"] == "至武曲宫垣"
    assert rows["P03-280"]["source_time_expression"] == "枢纽"
    assert rows["P03-282"]["source_time_expression"] == "大运流年"
    assert rows["P03-297"]["source_time_expression"] == "流年大限"
    assert rows["P03-215"]["scope_status"] == "DEDUPLICATED_SCOPE_METADATA_TO_P03-212_214"
    assert rows["P03-229"]["scope_status"] == "DEDUPLICATED_SCOPE_METADATA_TO_P03-228"


def test_tian_tong_source_gap_closed_across_printed_pages_10_11():
    rows = _read_csv("LIFE_TIAN_TONG_SOURCE_GAP_SUPPLEMENT_LINES_358_385_v0.1.csv")
    assert len(rows) == 47
    assert [r["projection_rule_id"] for r in rows] == [f"P01-SG-{i:03d}" for i in range(78, 125)]
    assert set(r["source_gap_id"] for r in rows) == {"P01-SRC-GAP-022"}
    assert sum(r["case_support_only"] == "true" for r in rows) == 5
    by_id = {r["projection_rule_id"]: r for r in rows}
    assert by_id["P01-SG-087"]["opposite_palace_dependency"] == "天梁"
    assert by_id["P01-SG-087"]["cross_palace_dependency"] == ""
    assert by_id["P01-SG-086"]["opposite_palace_dependency"] == "天梁在巳"
    assert by_id["P01-SG-086"]["cross_palace_dependency"] == ""
    assert by_id["P01-SG-109"]["cross_palace_dependency"] == "夫妻宫巨门化忌"
    assert any("运限的枢纽" in r["source_literal_claim"] for r in rows)
    assert any("凡[同巨]与陀罗同度者，主烦恼" in r["source_literal_claim"] for r in rows)
    assert any("寅申宫[天同天梁]同度，成[机月同梁]格" in r["source_literal_claim"] for r in rows)
    assert any("卯酉宫天同独坐，与太阴相对" in r["source_literal_claim"] for r in rows)
    assert any("年运枢纽" in r["source_literal_claim"] for r in rows)
    assert any("年限枢纽" in r["source_literal_claim"] for r in rows)
    assert {r["projection_rule_id"] for r in rows if r["case_support_only"] == "true"} == {"P01-SG-086", "P01-SG-089", "P01-SG-109", "P01-SG-116", "P01-SG-120"}


def test_tian_tong_source_gap_time_scope_is_not_narrowed():
    data = json.loads((BASE / "LIFE_TIAN_TONG_SOURCE_GAP_TIME_SCOPE_LINES_358_385_v0.1.json").read_text(encoding="utf-8"))
    rows = {r["projection_rule_id"]: r for r in data["records"]}
    assert len(rows) == 47
    assert rows["P01-SG-094"]["source_time_expression"] == "运限"
    assert rows["P01-SG-094"]["source_time_layers"] == []
    assert rows["P01-SG-094"]["scope_status"] == "SOURCE_GENERIC_PERIOD_NOT_NARROWED"
    assert rows["P01-SG-095"]["source_time_expression"] == "年限"
    assert rows["P01-SG-095"]["source_time_layers"] == []
    assert rows["P01-SG-110"]["source_time_expression"] == "流年大运"
    assert rows["P01-SG-110"]["source_time_layers"] == ["DECADE", "YEAR"]
    assert rows["P01-SG-110"]["scope_status"] == "SOURCE_EXPLICIT_DECADE_AND_YEAR"
    assert rows["P01-SG-116"]["source_time_expression"] == "否则（对照分支）"
    assert rows["P01-SG-116"]["source_time_layers"] == []
    assert rows["P01-SG-121"]["source_time_expression"] == "年限"
    assert rows["P01-SG-121"]["source_time_layers"] == []

def test_gap_ledger_and_summary_cumulative_counts():
    ledger = json.loads((BASE / "LIFE_P03_SOURCE_GAP_LEDGER_v0.1.json").read_text(encoding="utf-8"))
    assert ledger["unresolved_gap_ids"] == []
    closed = {g["gap_id"]: g for g in ledger["entries"]}
    assert closed["P01-SRC-GAP-025"]["status"] == "CLOSED_BY_SOURCE_RECHECK_AND_CANONICAL_RULES"
    assert len(closed["P01-SRC-GAP-025"]["rule_ids"]) == 91
    entries_now = {g["gap_id"]: g for g in ledger["entries"]}
    assert entries_now["P01-SRC-GAP-028"]["status"] == "CLOSED_BY_SOURCE_RECHECK_AND_CANONICAL_RULES"
    assert len(entries_now["P01-SRC-GAP-028"]["rule_ids"]) == 51
    assert "printed p22 bottom" in entries_now["P01-SRC-GAP-028"]["source_location"]
    assert ledger["next_checkpoint_gaps"] == []
    assert "P01 source audit complete through printed p24" in ledger["next_source_anchor"]
    assert ledger["entries"][0]["gap_id"] == "P01-SRC-GAP-022"
    assert len(ledger["entries"][0]["rule_ids"]) == 47
    summary = json.loads((BASE / "LIFE_P03_SOURCE_READJUDICATION_SUMMARY_v0.1.json").read_text(encoding="utf-8"))
    next_summary_gaps = summary["source_coverage_gaps_next_checkpoint"]
    assert next_summary_gaps[0]["gap_id"] == "P01-SRC-GAP-023"
    assert "寅申廉贞" in next_summary_gaps[0]["source_claim"]
    s = summary["summary"]
    assert s["historical_candidates_reviewed"] == 100
    assert s["canonical_promoted"] == 98
    assert s["new_tian_tong_gap_records"] == 47
    assert s["new_canonical_records"] == 145
    assert s["reusable_projection_rules"] == 129
    assert s["case_support_only"] == 16
    assert s["gap_supplement_case_support_only"] == 5
    assert s["cumulative_canonical_records_after_merge"] == 422
    assert s["cumulative_reusable_projection_rules_after_merge"] == 342
    assert s["cumulative_case_support_only_after_merge"] == 80
    assert s["new_primitive_qi"] == 0
    assert s["new_memory_type"] == 0
    assert s["new_independent_time_scale"] == 0
    assert s["numeric_weight"] == 0
    assert s["probability"] == 0
    assert summary["shared_semantic_gaps"] == []
    assert summary["human_gate_required"] is False

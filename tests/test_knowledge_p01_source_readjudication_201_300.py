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
    assert rows["P03-212"]["source_time_expression"] == "大限流年"
    assert rows["P03-228"]["source_time_expression"] == "流年或大限"
    assert rows["P03-232"]["source_time_expression"] == "年运"
    assert rows["P03-231"]["source_time_expression"] == "天相运"
    assert rows["P03-274"]["source_time_expression"] == "行至宫垣"
    assert rows["P03-280"]["source_time_expression"] == "枢纽"
    assert rows["P03-282"]["source_time_expression"] == "大运流年"
    assert rows["P03-297"]["source_time_expression"] == "流年大限"
    assert rows["P03-215"]["scope_status"] == "DEDUPLICATED_SCOPE_METADATA_TO_P03-212_214"
    assert rows["P03-229"]["scope_status"] == "DEDUPLICATED_SCOPE_METADATA_TO_P03-228"


def test_tian_tong_source_gap_closed():
    rows = _read_csv("LIFE_TIAN_TONG_SOURCE_GAP_SUPPLEMENT_LINES_358_385_v0.1.csv")
    assert len(rows) == 16
    assert [r["projection_rule_id"] for r in rows] == [f"P01-SG-{i:03d}" for i in range(78, 94)]
    assert set(r["source_gap_id"] for r in rows) == {"P01-SRC-GAP-022"}
    assert sum(r["case_support_only"] == "true" for r in rows) == 2
    assert any("年运枢纽" in r["source_literal_claim"] for r in rows)
    assert any("年限枢纽" in r["source_literal_claim"] for r in rows)


def test_gap_ledger_and_summary_cumulative_counts():
    ledger = json.loads((BASE / "LIFE_P03_SOURCE_GAP_LEDGER_v0.1.json").read_text(encoding="utf-8"))
    assert ledger["unresolved_gap_ids"] == []
    assert ledger["entries"][0]["gap_id"] == "P01-SRC-GAP-022"
    assert len(ledger["entries"][0]["rule_ids"]) == 16
    summary = json.loads((BASE / "LIFE_P03_SOURCE_READJUDICATION_SUMMARY_v0.1.json").read_text(encoding="utf-8"))
    s = summary["summary"]
    assert s["historical_candidates_reviewed"] == 100
    assert s["canonical_promoted"] == 98
    assert s["new_tian_tong_gap_records"] == 16
    assert s["new_canonical_records"] == 114
    assert s["cumulative_canonical_records_after_merge"] == 391
    assert s["cumulative_reusable_projection_rules_after_merge"] == 314
    assert s["cumulative_case_support_only_after_merge"] == 77
    assert s["new_primitive_qi"] == 0
    assert s["new_memory_type"] == 0
    assert s["new_independent_time_scale"] == 0
    assert s["numeric_weight"] == 0
    assert s["probability"] == 0
    assert summary["shared_semantic_gaps"] == []
    assert summary["human_gate_required"] is False

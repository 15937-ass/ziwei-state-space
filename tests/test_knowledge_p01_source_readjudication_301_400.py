import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "knowledge" / "palaces" / "P01_life" / "wp05"
STATE = ROOT / "knowledge" / "states" / "P01_LIFE_STATE.yaml"


def _read_csv(path):
    with (BASE / path).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def test_p04_candidate_census_and_counts():
    rows = _read_csv("LIFE_P04_SOURCE_READJUDICATION_301_400_v0.1.csv")
    assert len(rows) == 100
    assert [r["projection_rule_id"] for r in rows] == [f"P04-{i:03d}" for i in range(301, 401)]
    assert all(r["source_id"] == "SRC-ZZ-003" for r in rows)
    assert all(r["canonical_promotion"] == "true" for r in rows)
    assert sum(r["case_support_only"] == "true" for r in rows) == 12
    summary = json.loads((BASE / "LIFE_P04_SOURCE_READJUDICATION_SUMMARY_v0.1.json").read_text(encoding="utf-8"))
    assert summary["summary"]["historical_candidate_rows_reviewed"] == 100
    assert summary["summary"]["canonical_promotions_from_candidate_batch"] == 100
    assert summary["summary"]["source_gap_supplement_records"] == 11
    assert summary["summary"]["canonical_records_added"] == 111
    assert summary["summary"]["cumulative_canonical_records_after_merge"] == 533
    assert summary["summary"]["cumulative_reusable_projection_rules_after_merge"] == 438
    assert summary["summary"]["cumulative_case_support_only_after_merge"] == 95


def test_p04_source_first_dependency_and_page_repairs():
    rows = {r["projection_rule_id"]: r for r in _read_csv("LIFE_P04_SOURCE_READJUDICATION_301_400_v0.1.csv")}
    for rid in ("P04-304", "P04-305", "P04-306"):
        assert rows[rid]["opposite_palace_dependency"] == "贪狼"
        assert rows[rid]["cross_palace_dependency"] == ""
    for rid in ("P04-349", "P04-350", "P04-354"):
        assert rows[rid]["opposite_palace_dependency"] == "七杀"
        assert rows[rid]["cross_palace_dependency"] == ""
    assert rows["P04-375"]["opposite_palace_dependency"] == "紫杀"
    assert rows["P04-375"]["cross_palace_dependency"] == ""
    for rid in ("P04-340", "P04-345", "P04-346", "P04-356", "P04-357"):
        assert rows[rid]["cross_palace_dependency"] == ""
    assert rows["P04-301"]["cross_palace_dependency"] == "迁移宫"
    assert rows["P04-321"]["cross_palace_dependency"] == "疾厄宫"
    assert rows["P04-338"]["cross_palace_dependency"] == "福德宫;事业宫;夫妻宫"
    assert rows["P04-372"]["cross_palace_dependency"] == "事业宫"
    assert rows["P04-380"]["cross_palace_dependency"] == "迁移宫"
    assert rows["P04-384"]["cross_palace_dependency"] == "财帛宫"
    assert "财帛宫而定" in rows["P04-384"]["source_literal_claim"]
    assert rows["P04-389"]["cross_palace_dependency"] == "福德宫"
    assert rows["P04-390"]["cross_palace_dependency"] == "福德宫"
    for rid in [f"P04-{i:03d}" for i in range(376, 391)] + ["P04-398", "P04-399", "P04-400"]:
        assert "印刷页14" in rows[rid]["source_location"]
    for rid in [f"P04-{i:03d}" for i in range(391, 398)]:
        assert "印刷页15" in rows[rid]["source_location"]
    assert "兵戎" in rows["P04-303"]["canonical_normalization"]


def test_p04_time_scope_and_source_gap_supplement():
    time_scope = json.loads((BASE / "LIFE_P04_SOURCE_TIME_SCOPE_301_400_v0.1.json").read_text(encoding="utf-8"))
    assert len(time_scope["records"]) == 100
    by_id = {r["projection_rule_id"]: r for r in time_scope["records"]}
    for rid in ("P04-307", "P04-308", "P04-309", "P04-310", "P04-311"):
        assert by_id[rid]["source_time_layers"] == ["YEAR"]
    for rid in ("P04-312", "P04-313", "P04-314", "P04-315"):
        assert by_id[rid]["source_time_layers"] == ["DECADE"]
    for rid in ("P04-327", "P04-328", "P04-329"):
        assert by_id[rid]["source_time_layers"] == []
        assert by_id[rid]["scope_status"] == "SOURCE_GENERIC_YEAR_PERIOD_NOT_NARROWED"
    for rid in ("P04-341", "P04-342", "P04-343", "P04-344", "P04-374"):
        assert by_id[rid]["source_time_layers"] == []
        assert by_id[rid]["scope_status"] == "SOURCE_GENERIC_PERIOD_NOT_NARROWED"

    supplement = _read_csv("LIFE_P04_SOURCE_GAP_SUPPLEMENT_v0.1.csv")
    assert len(supplement) == 11
    assert [r["projection_rule_id"] for r in supplement] == [f"P01-SG-{i:03d}" for i in range(125, 136)]
    assert all(r["source_gap_id"] == "P01-SRC-GAP-023" for r in supplement)
    assert sum(r["case_support_only"] == "true" for r in supplement) == 3
    assert supplement[5]["cross_palace_dependency"] == "夫妻宫"

    gap_time = json.loads((BASE / "LIFE_P04_SOURCE_GAP_TIME_SCOPE_v0.1.json").read_text(encoding="utf-8"))
    assert len(gap_time["records"]) == 11
    ledger = json.loads((BASE / "LIFE_P04_SOURCE_GAP_LEDGER_v0.1.json").read_text(encoding="utf-8"))
    entries = {e["gap_id"]: e for e in ledger["entries"]}
    assert entries["P01-SRC-GAP-022"]["status"] == "CLOSED_BY_NEW_CANONICAL_RULES"
    assert entries["P01-SRC-GAP-023"]["status"] == "CLOSED_BY_NEW_CANONICAL_RULES"
    assert len(entries["P01-SRC-GAP-023"]["rule_ids"]) == 46
    assert entries["P01-SRC-GAP-024"]["status"] == "OPEN_FOR_NEXT_SOURCE_CHECKPOINT"
    assert ledger["next_checkpoint_gaps"][0]["gap_id"] == "P01-SRC-GAP-024"
    state = STATE.read_text(encoding="utf-8")
    assert "active_issue: 603" in state
    assert "active_pr: 604" in state
    assert "canonical_source_records_ready_on_branch: 533" in state
    assert "source_coverage_gaps_recorded_in_current_batch: 1" in state

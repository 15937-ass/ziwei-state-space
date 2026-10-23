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


def test_p06_candidate_census_source_first_and_promotions():
    rows = read_csv("LIFE_P06_SOURCE_READJUDICATION_501_600_v0.1.csv")
    assert len(rows) == 100
    assert [r["projection_rule_id"] for r in rows] == [f"P01-{i:03d}" for i in range(501, 601)]
    assert all(r["source_id"] == "SRC-ZZ-003" for r in rows)
    assert all(r["canonical_promotion"] == "true" for r in rows)
    assert all(r["source_resolution_changed"] == "true" for r in rows)
    assert sum(r["case_support_only"] == "true" for r in rows) == 6
    by = {r["projection_rule_id"]: r for r in rows}
    assert "或不见吉化" in by["P01-515"]["canonical_condition"]
    assert by["P01-563"]["opposite_palace_dependency"] == ""
    assert by["P01-564"]["opposite_palace_dependency"] == ""
    assert by["P01-563"]["cross_palace_dependency"] == "天同化忌（邻宫）"
    assert by["P01-564"]["cross_palace_dependency"] == "天同化忌（邻宫）"
    assert by["P01-543"]["event_specificity"] == "ABSTRACT"
    assert "同度或对拱" in by["P01-585"]["canonical_condition"]
    assert "同度或对拱" in by["P01-586"]["canonical_condition"]
    assert "天梁天马陷" in by["P01-590"]["source_text_uncertainty"]
    assert by["P01-590"]["canonical_condition"].endswith("“天梁天马陷”")
    assert by["P01-600"]["archived_primary_time_layer"] == "DECADE"


def test_p06_gap_supplement_census_and_case_only():
    rows = read_csv("LIFE_P06_SOURCE_GAP_SUPPLEMENT_PP17_20_v0.1.csv")
    assert len(rows) == 42
    assert [r["projection_rule_id"] for r in rows] == [f"P01-SG-{i:03d}" for i in range(168, 210)]
    assert all(r["source_gap_id"] == "P01-SRC-GAP-026" for r in rows)
    assert all(r["canonical_promotion"] == "true" for r in rows)
    assert sum(r["case_support_only"] == "true" for r in rows) == 10
    by = {r["projection_rule_id"]: r for r in rows}
    assert "文昌化忌" in by["P01-SG-168"]["source_literal_claim"]
    assert by["P01-SG-177"]["archived_primary_time_layer"] == "DECADE_YEAR"
    assert by["P01-SG-198"]["archived_primary_time_layer"] == "SOURCE_SCOPE_UNRESOLVED"
    assert by["P01-SG-204"]["cross_palace_dependency"] == "夫妻宫巨门吉化（尤喜化禄）"
    assert "丧门、吊客、白虎" in by["P01-SG-209"]["source_literal_claim"]
    assert "见奏书亦吉" in by["P01-SG-190"]["source_literal_claim"]
    assert "若同时又见煞及昌曲化忌" in by["P01-SG-190"]["source_literal_claim"]


def test_p06_time_scope_preserves_generic_and_multilayer_words():
    data = read_json("LIFE_P06_SOURCE_TIME_SCOPE_501_600_v0.1.json")
    rows = {r["projection_rule_id"]: r for r in data["records"]}
    assert len(rows) == 100
    for k in ("P01-520", "P01-521", "P01-522", "P01-523", "P01-527"):
        assert rows[k]["source_time_layers"] == ["DECADE"]
    assert rows["P01-528"]["source_time_layers"] == ["DECADE", "YEAR"]
    for k in ("P01-525", "P01-526"):
        assert rows[k]["source_time_layers"] == []
        assert rows[k]["scope_status"] == "SOURCE_TEMPORAL_LAYER_UNSPECIFIED"
    for k in ("P01-529", "P01-595", "P01-596", "P01-597", "P01-598"):
        assert rows[k]["source_time_layers"] == []
        assert "GENERIC" in rows[k]["scope_status"]
    assert rows["P01-561"]["source_time_expression"] == "流年命宫或小限"
    assert rows["P01-561"]["source_time_layers"] == ["YEAR"]
    assert rows["P01-600"]["source_time_layers"] == ["DECADE"]


def test_p06_gap_supplement_time_scope_and_cumulative_state():
    data = read_json("LIFE_P06_SOURCE_GAP_TIME_SCOPE_PP17_20_v0.1.json")
    rows = {r["projection_rule_id"]: r for r in data["records"]}
    assert len(rows) == 42
    assert rows["P01-SG-173"]["source_time_layers"] == ["DECADE", "YEAR"]
    assert rows["P01-SG-177"]["source_time_layers"] == ["DECADE", "YEAR"]
    assert rows["P01-SG-187"]["source_time_layers"] == ["DECADE", "YEAR"]
    assert rows["P01-SG-198"]["source_time_layers"] == []
    assert rows["P01-SG-208"]["source_time_layers"] == ["DECADE", "YEAR"]
    assert rows["P01-SG-209"]["source_time_layers"] == ["YEAR"]
    assert rows["P01-SG-209"]["scope_status"] == "SOURCE_EXPLICIT_YEAR_OR_SMALL_LIMIT_UNMAPPED"
    summary = read_json("LIFE_P06_SOURCE_READJUDICATION_SUMMARY_v0.1.json")["summary"]
    assert (summary["historical_candidates_reviewed"], summary["canonical_promoted"], summary["new_source_gap_supplement_records"]) == (100, 100, 42)
    assert (summary["new_canonical_records"], summary["reusable_projection_rules"], summary["case_support_only"]) == (142, 126, 16)
    assert (summary["cumulative_canonical_records_after_merge"], summary["cumulative_reusable_projection_rules_after_merge"], summary["cumulative_case_support_only_after_merge"]) == (789, 656, 133)
    assert summary["new_primitive_qi"] == summary["new_memory_type"] == summary["new_independent_time_scale"] == 0
    assert summary["numeric_weight"] == summary["probability"] == summary["decay"] == 0
    assert 'canonical_source_records_on_main: 789' in STATE.read_text(encoding="utf-8")
    assert "No Product/runtime authorization is implied" in STATE.read_text(encoding="utf-8")

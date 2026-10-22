import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "validation/wp05/M03_migration_projection_review_201_300.csv"
READJ = ROOT / "knowledge/palaces/P07_migration/wp05/MIGRATION_M03_SOURCE_READJUDICATION_100_v0.1.json"
TIME = ROOT / "knowledge/palaces/P07_migration/wp05/MIGRATION_M03_SOURCE_TIME_SCOPE_v0.1.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def candidate_rows():
    with CANDIDATE.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def records_by_id():
    return {r["projection_rule_id"]: r for r in load(READJ)["records"]}

def test_candidate_census_and_source_binding():
    rows = candidate_rows()
    ids = [r["projection_rule_id"] for r in rows]
    assert len(rows) == 100
    assert len(set(ids)) == 100
    assert ids[0] == "M03-201"
    assert ids[-1] == "M03-300"
    assert all(r["source_id"] == "SRC-ZZ-003" for r in rows)
    assert all(r["palace_id"] == "P07" for r in rows)
    assert all(r["source_location"].startswith("迁移宫printed_p") for r in rows)

def test_rejudication_census_and_case_only_boundary():
    d = load(READJ)
    s = d["summary"]
    assert s["reviewed"] == 100
    assert s["canonical_promoted"] == 100
    assert s["reusable_projection_rules"] == 81
    assert s["case_support_only"] == 19
    assert s["history_feedback"] == 0
    assert s["source_resolution_change_count"] == 34
    assert len(s["source_resolution_changed_rows"]) == 34
    assert s["source_condition_normalization_count"] == 97
    assert len(s["source_condition_normalized_rows"]) == 97
    assert s["path_dependent_gate_ids"] == []
    expected_case = {
        "M03-225","M03-226","M03-229","M03-235","M03-237","M03-238","M03-239",
        "M03-240","M03-241","M03-256","M03-259","M03-261","M03-263","M03-265",
        "M03-266","M03-272","M03-273","M03-285","M03-287"
    }
    assert set(s["case_support_only_ids"]) == expected_case
    actual = {r["projection_rule_id"] for r in d["records"] if r["case_support_only"]}
    assert actual == expected_case
    assert all(d["records"][i].get("case_support_reason") for i in range(len(d["records"])) if d["records"][i]["case_support_only"])
    assert all("源文" in d["records"][i]["case_support_reason"] for i in range(len(d["records"])) if d["records"][i]["case_support_only"])
    assert all(r["canonical_promotion"] is True for r in d["records"])

def test_every_prege_antecedent_is_resolved():
    d = load(READJ)
    assert len(d["records"]) == 100
    assert all("前格" not in r["canonical_condition"] for r in d["records"])
    original = {r["projection_rule_id"]: r for r in candidate_rows()}
    canonical = records_by_id()
    inherited = [rid for rid, row in original.items() if "前格" in row["condition"]]
    assert inherited
    assert all(canonical[rid]["canonical_condition"] != original[rid]["condition"] for rid in inherited)

def test_m03_291_attribution_is_corrected():
    m = records_by_id()["M03-291"]
    assert "太阴天机组合" in m["canonical_condition"]
    assert "天机化忌" in m["canonical_condition"]
    assert m["canonical_projection_domain"] == "career"
    assert "career" in m["canonical_projection_target"]
    assert "太阴化忌于庙旺之宫" not in m["canonical_condition"]
    assert m["disposition"] == "SOURCE_ATTRIBUTION_CORRECTED"

def test_m03_292_and_m03_293_remain_separate_source_branches():
    m = records_by_id()
    assert "太阴化忌守迁移宫" in m["M03-292"]["canonical_condition"]
    assert "投资" in m["M03-292"]["canonical_condition"]
    assert "太阳太阴组合" in m["M03-293"]["canonical_condition"]
    assert "太阴化忌" in m["M03-293"]["canonical_condition"]
    assert "虚耗" in m["M03-293"]["canonical_condition"]
    assert "刑曜" in m["M03-293"]["canonical_condition"]
    assert "代人受过" in m["M03-293"]["canonical_projection_target"] or "bear_blame" in m["M03-293"]["canonical_projection_target"]
    assert m["M03-292"]["canonical_condition"] != m["M03-293"]["canonical_condition"]

def test_lexical_uncertainty_is_preserved():
    m = records_by_id()["M03-233"]
    assert "source_text_uncertainty" in m
    assert "贞归三" in m["source_text_uncertainty"]
    assert m["canonical_projection_target"] == "external_setbacks_and_unsmooth_progress"
    assert m["disposition"] == "SOURCE_TEXT_UNCERTAINTY_PRESERVED"

def test_overlap_groups_cover_required_source_clauses():
    d = load(READJ)
    groups = {g["group_id"]: set(g["record_ids"]) for g in d["summary"]["source_overlap_groups"]}
    required = [
        {"M03-208","M03-209","M03-210"},
        {"M03-211","M03-212","M03-213"},
        {"M03-215","M03-216","M03-217"},
        {"M03-237","M03-238","M03-239"},
        {"M03-240","M03-241"},
        {"M03-254","M03-255","M03-256"},
        {"M03-258","M03-259","M03-260","M03-261"},
        {"M03-264","M03-265","M03-266"},
        {"M03-269","M03-270","M03-271","M03-272"},
        {"M03-284","M03-285"},
        {"M03-286","M03-287"},
        {"M03-295","M03-296"}
    ]
    for wanted in required:
        assert any(wanted.issubset(members) for members in groups.values())

def test_source_coverage_gaps_are_explicit_and_not_promoted():
    d = load(READJ)
    gaps = d["source_coverage_gaps"]
    assert len(gaps) == d["summary"]["source_coverage_gap_count"] == 12
    claims = " ".join(g["source_literal_claim"] for g in gaps)
    for term in ["财荫夹","辅弼","魁钺","火铃","羊陀","随娘改嫁","太阴与天同","太阴天机","流年大运化忌冲起"]:
        assert term in claims
    assert all(g["status"].startswith("SOURCE_COVERAGE_GAP") for g in gaps)
    assert not any("projection_rule_id" in g for g in gaps)

def test_temporal_scope_preserves_four_layers_and_existing_overlay():
    d = load(TIME)
    assert d["chapter_scope"]["source_layers"] == ["NATAL","DECADE","YEAR","MONTH"]
    overlay = d["event_relative_overlay"]
    assert overlay["overlay_id"] == "MIGRATION_FIRST_THREE_YEARS"
    assert overlay["human_gate"] == "HG-P07-TEMPORAL-01-A"
    assert overlay["active_year_index"] == [1,2,3]
    assert overlay["seventh_calendar_layer"] is False
    assert overlay["generic_event_timer"] is False
    assert overlay["change_in_M03"] is False
    assert d["default_star_system_records"]["runtime_eligibility_granted"] is False
    special = {r["projection_rule_id"]: r for r in d["special_records"]}
    assert special["M03-238"]["source_time_layers"] == ["YEAR"]
    assert special["M03-239"]["source_time_layers"] == ["YEAR"]
    gap = d["uncovered_source_time_claims"][0]
    assert gap["source_time_layers"] == ["DECADE","YEAR"]
    assert gap["runtime_eligibility_granted"] is False

def test_no_new_semantics_or_quantitative_claims():
    d = load(READJ)
    s = d["summary"]
    for key in ["new_primitive_qi","new_memory_type","new_independent_time_scale",
                "new_shared_group_semantics","numeric_weight","probability","decay","product_runtime_change"]:
        assert s[key] == 0
    assert d["source_basis"]["source_id"] == "SRC-ZZ-003"
    assert d["source_basis"]["printed_pages"] == "113–116"
    assert d["source_basis"]["pdf_scan_pages"] == [57,58]

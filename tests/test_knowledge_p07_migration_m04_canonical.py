import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "validation/wp05/M04_migration_projection_review_301_400.csv"
READJ = ROOT / "knowledge/palaces/P07_migration/wp05/MIGRATION_M04_SOURCE_READJUDICATION_100_v0.1.json"
TIME = ROOT / "knowledge/palaces/P07_migration/wp05/MIGRATION_M04_SOURCE_TIME_SCOPE_v0.1.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def candidate_rows():
    with CANDIDATE.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def records_by_id():
    return {r["projection_rule_id"]: r for r in load(READJ)["records"]}

def test_candidate_census_and_source_span_correction():
    rows = candidate_rows()
    ids = [r["projection_rule_id"] for r in rows]
    assert len(rows) == 100 and len(set(ids)) == 100
    assert ids[0] == "M04-301" and ids[-1] == "M04-400"
    assert all(r["source_id"] == "SRC-ZZ-003" and r["palace_id"] == "P07" for r in rows)
    d = load(READJ)
    assert len(d["records"]) == 100
    assert all("前格" not in r["canonical_condition"] for r in d["records"])
    recs = records_by_id()
    span_changed = {r["projection_rule_id"] for r in d["records"] if r["source_span_changed"]}
    assert len(span_changed) == 29
    assert span_changed == ({f"M04-{n}" for n in range(301,327)} | {"M04-347","M04-348","M04-349"})
    assert recs["M04-301"]["source_location"] == "SRC-ZZ-003 printed p115"
    assert recs["M04-325"]["source_location"] == "SRC-ZZ-003 printed pp115–116"
    assert recs["M04-326"]["source_location"] == "SRC-ZZ-003 printed pp115–116"
    assert recs["M04-327"]["source_location"] == "SRC-ZZ-003 printed p116"
    assert recs["M04-369"]["source_location"] == "SRC-ZZ-003 printed p117"

def test_source_resolution_counts_and_case_only_reasons():
    d = load(READJ); s = d["summary"]
    assert s["reviewed"] == 100 and s["canonical_promoted"] == 100
    assert s["reusable_projection_rules"] == 91 and s["case_support_only"] == 9
    assert s["history_feedback"] == 0 and s["source_resolution_change_count"] == 40
    assert len(s["source_resolution_changed_rows"]) == 40
    expected = {"M04-309","M04-314","M04-325","M04-326","M04-344","M04-345","M04-354","M04-363","M04-368"}
    assert set(s["case_support_only_ids"]) == expected
    assert {r["projection_rule_id"] for r in d["records"] if r["case_support_only"]} == expected
    assert all(r.get("case_support_reason") and "源文" in r["case_support_reason"] for r in d["records"] if r["case_support_only"])
    assert s["source_time_layer_changed_rows"] == []
    recs = records_by_id()
    assert recs["M04-368"]["primary_time_layer"] == "YEAR"
    assert recs["M04-388"]["primary_time_layer"] == "DECADE"
    assert recs["M04-389"]["primary_time_layer"] == "YEAR"
    assert s["path_dependent_gate_reclassified_rows"] == ["M04-328","M04-349"]
    assert s["canonical_path_dependent_gate_ids"] == []

def test_solar_attribution_and_sequence_gate_repairs():
    r = records_by_id()
    assert "太阳会天同化禄" in r["M04-327"]["canonical_condition"]
    assert "太阴会天同化禄" not in r["M04-327"]["canonical_condition"]
    assert "太阳会天机化禄" in r["M04-328"]["canonical_condition"]
    assert "太阴会天机化禄" not in r["M04-328"]["canonical_condition"]
    assert r["M04-328"]["history_feedback"] is None and r["M04-328"]["path_dependent_gate_reclassified"]
    assert r["M04-349"]["history_feedback"] is None and r["M04-349"]["path_dependent_gate_reclassified"]
    assert r["M04-349"]["canonical_condition"].endswith("同时又见煞忌")

def test_taiyin_loss_branch_is_not_overbound():
    r = records_by_id(); m319 = r["M04-319"]["canonical_condition"]
    assert "太阴化忌守迁移宫" in m319
    assert "太阳太阴组合守迁移宫" not in m319
    assert "不强制继承M04-318" in m319
    assert "双陀罗或双擎羊同躔" in r["M04-325"]["canonical_condition"]
    assert "两重羊陀夹" in r["M04-326"]["canonical_condition"]

def test_time_layers_and_existing_overlay_are_preserved():
    d = load(TIME)
    assert d["chapter_scope"]["source_layers"] == ["NATAL","DECADE","YEAR","MONTH"]
    special = {r["projection_rule_id"]:r for r in d["special_records"]}
    assert special["M04-325"]["source_time_layers"] == ["YEAR"]
    assert special["M04-326"]["source_time_layers"] == ["DECADE"]
    assert special["M04-368"]["source_time_layers"] == ["YEAR"]
    assert special["M04-388"]["source_time_layers"] == ["DECADE"]
    assert special["M04-389"]["source_time_layers"] == ["YEAR"]
    overlay = d["event_relative_overlay"]
    assert overlay["overlay_id"] == "MIGRATION_FIRST_THREE_YEARS"
    assert overlay["human_gate"] == "HG-P07-TEMPORAL-01-A"
    assert overlay["active_year_index"] == [1,2,3]
    assert not overlay["seventh_calendar_layer"] and not overlay["generic_event_timer"] and not overlay["change_in_M04"]
    assert d["path_dependent_gate_audit"]["canonical_flags"] == []
    assert d["path_dependent_gate_audit"]["history_feedback_rows"] == 0

def test_overlap_groups_and_gap_resolution_are_explicit():
    d = load(READJ)
    groups = {g["group_id"]:set(g["record_ids"]) for g in d["summary"]["source_overlap_groups"]}
    required = [
      {"M04-312","M04-313","M04-314"},{"M04-315","M04-316","M04-317","M04-318","M04-319"},
      {"M04-320","M04-321","M04-322","M04-323","M04-324"},{"M04-325","M04-326"},
      {"M04-327","M04-328"},{"M04-338","M04-339","M04-340","M04-341","M04-342"},
      {"M04-343","M04-344","M04-345","M04-346"},{"M04-347","M04-348","M04-349"},
      {"M04-369","M04-370","M04-371","M04-372","M04-373","M04-374","M04-375"},
      {"M04-381","M04-382","M04-383"},{"M04-387","M04-388","M04-389","M04-390","M04-391","M04-392"},
      {"M04-393","M04-394","M04-395"},{"M04-396","M04-397","M04-398","M04-399","M04-400"}
    ]
    for wanted in required:
        assert any(wanted.issubset(members) for members in groups.values())
    assert len(d["source_coverage_gaps"]) == d["summary"]["source_coverage_gap_count"] == 3
    assert len(d["carried_forward_source_gaps"]) == 2
    resolution = {x["prior_gap_id"]:x for x in d["gap_resolution_map"]}
    assert resolution["P07-M03-GAP-002"]["mapped_to"] == ["M04-301"]
    assert resolution["P07-M03-GAP-005"]["mapped_to"] == ["M04-309"]
    assert resolution["P07-M03-GAP-010"]["mapped_to"] == ["M04-325","M04-326"]
    assert resolution["P07-M03-GAP-011"]["mapped_to"] == ["M04-327","M04-328"]
    assert resolution["P07-M03-GAP-001"]["status"] == "CARRIED_FORWARD_UNRESOLVED"
    assert resolution["P07-M03-GAP-012"]["status"] == "CARRIED_FORWARD_OUTSIDE_M04_SOURCE_SPAN"

def test_new_gaps_capture_unrepresented_jumen_branches():
    d = load(READJ); claims = " ".join(g["source_literal_claim"] for g in d["source_coverage_gaps"])
    for term in ["禄存同度","卯酉二宫立命","流年巨门守迁移"]:
        assert term in claims
    assert all(g["status"].startswith("SOURCE_COVERAGE_GAP") for g in d["source_coverage_gaps"])
    assert not any("projection_rule_id" in g for g in d["source_coverage_gaps"])

def test_no_new_semantics_or_quantitative_claims():
    d = load(READJ); s = d["summary"]
    for key in ["new_primitive_qi","new_memory_type","new_independent_time_scale","new_shared_group_semantics","numeric_weight","probability","decay","product_runtime_change"]:
        assert s[key] == 0
    assert d["source_basis"]["printed_pages"] == "115–117"
    assert d["source_basis"]["pdf_scan_pages"] == [58,59]

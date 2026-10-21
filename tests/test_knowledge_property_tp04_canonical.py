import csv
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CSV=ROOT/"validation/wp05/TP04_property_projection_review_301_358.csv"
READJ=ROOT/"knowledge/wp05/property/PROPERTY_TP04_SOURCE_READJUDICATION_58_v0.1.json"
TIME=ROOT/"knowledge/wp05/property/PROPERTY_TP04_SOURCE_TIME_SCOPE_v0.1.json"
CLOSURE=ROOT/"knowledge/wp05/property/PROPERTY_P10_CANONICAL_CLOSURE_v0.1.json"

def load(p): return json.loads(p.read_text(encoding="utf-8"))
def rows():
    with CSV.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def test_tp04_exact_58_unique_and_source():
    r=rows()
    assert len(r)==58
    assert len({x["projection_rule_id"] for x in r})==58
    assert r[0]["projection_rule_id"]=="TP04-301"
    assert r[-1]["projection_rule_id"]=="TP04-358"
    assert all(x["source_id"]=="SRC-ZZ-003" for x in r)
    assert all(x["palace_id"]=="P10" for x in r)
    assert all(x["source_span_verified"]=="true" for x in r)

def test_tp04_census():
    r=rows()
    assert sum(x["case_support_only"]=="true" for x in r)==8
    assert sum(bool(x["history_feedback"]) for x in r)==3
    assert {x["projection_rule_id"] for x in r if x["history_feedback"]}=={"TP04-323","TP04-341","TP04-350"}
    assert sum(x["time_layer"]=="YEAR" for x in r)==6

def test_tp04_source_repairs():
    m={x["projection_rule_id"]:x for x in rows()}
    assert "sale_or_out_of_region" in m["TP04-305"]["projection_target"]
    assert "流年天机化忌" in m["TP04-308"]["condition"]
    assert "藩陷" in m["TP04-315"]["condition"]
    assert "倾效" in m["TP04-327"]["condition"]
    assert "collapse" not in m["TP04-327"]["projection_target"]
    assert m["TP04-328"]["projection_target"]=="source_specific_household_sadness_or_tears_event_candidate"
    assert "blood" not in m["TP04-328"]["projection_target"]
    assert "承上指代范围保留" in m["TP04-329"]["condition"]
    assert "陀罗铃星度" in m["TP04-331"]["condition"]
    assert "降黩" in m["TP04-333"]["condition"]
    assert m["TP04-333"]["projection_target"]=="status_decline_pressure_strengthens"
    assert "主人独虚惊" in m["TP04-338"]["condition"]
    assert "旧业翻断" in m["TP04-341"]["condition"]
    assert "叛变卖产业" in m["TP04-345"]["condition"]
    assert "天晋" in m["TP04-347"]["condition"]
    assert "天铖" in m["TP04-349"]["condition"] and "天钺" not in m["TP04-349"]["condition"]
    assert "财阴夹" in m["TP04-352"]["condition"] and "财荫夹" not in m["TP04-352"]["condition"]
    assert "降黩" in m["TP04-357"]["condition"]
    assert m["TP04-357"]["projection_target"]=="status_decline_or_service_institution_closure_candidate"

def test_tp04_readjudication_census_and_uncertainty():
    d=load(READJ)
    assert d["summary"]["reviewed"]==58
    assert d["summary"]["canonical_promoted"]==58
    assert d["summary"]["reusable_projection_rules"]==50
    assert d["summary"]["case_support_only"]==8
    assert d["summary"]["history_feedback"]==3
    assert d["summary"]["legacy_year_rows"]==6
    assert d["summary"]["source_resolution_change_count"]==15
    assert d["summary"]["source_resolution_changed_rows"]==[
        "TP04-305","TP04-308","TP04-315","TP04-327","TP04-328",
        "TP04-329","TP04-331","TP04-333","TP04-338","TP04-341",
        "TP04-345","TP04-347","TP04-349","TP04-352","TP04-357"
    ]
    assert d["source_basis"]["archived_candidate_status"]=="NONCANONICAL_ACCELERATION_INPUT_ONLY"
    assert d["source_basis"]["chapter_boundary_after"]=="福德宫"

def test_tp04_time_scope_and_life_stage():
    d=load(TIME); m={x["projection_rule_id"]:x for x in d["records"]}
    assert len(d["records"])==58
    assert m["TP04-308"]["legacy_primary_time_layer"]=="YEAR"
    assert m["TP04-308"]["scope_status"]=="YEAR_CONTEXT_INHERITED_FROM_PRECEDING_SENTENCE"
    assert m["TP04-323"]["source_time_layers"]==["NATAL","DECADE"]
    assert m["TP04-323"]["source_time_labels"]==["至大运佳美时"]
    assert m["TP04-330"]["literal_life_stage_labels"]==["中晚年始能置产"]
    assert d["summary"]["new_runtime_time_primitives"]==0

def test_property_palace_canonical_closure():
    d=load(CLOSURE)
    assert d["status"]=="CANONICAL_SOURCE_REVIEW_CLOSED_358_OF_358"
    assert d["totals"]["reviewed"]==358
    assert d["totals"]["reusable_projection_rules"]==308
    assert d["totals"]["case_support_only"]==50
    assert d["totals"]["history_feedback"]==14
    assert d["totals"]["canonical_id_last"]=="TP04-358"
    assert d["source_basis"]["next_printed_heading"]=="福德宫"
    assert d["totals"]["cross_boundary_imports"]==0

def test_no_new_quantitative_or_time_primitive():
    d=load(READJ)["summary"]
    for k in ["new_primitive_qi","new_memory_type","new_independent_time_scale","numeric_weight","probability","decay"]:
        assert d[k]==0

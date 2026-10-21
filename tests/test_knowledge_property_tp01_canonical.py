import csv
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CSV=ROOT/"validation/wp05/TP01_property_projection_review_001_100.csv"
READJ=ROOT/"knowledge/wp05/property/PROPERTY_TP01_SOURCE_READJUDICATION_100_v0.1.json"
TIME=ROOT/"knowledge/wp05/property/PROPERTY_TP01_SOURCE_TIME_SCOPE_v0.1.json"

def load(p): return json.loads(p.read_text(encoding="utf-8"))

def rows():
    with CSV.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def test_tp01_exact_100_and_unique():
    r=rows()
    assert len(r)==100
    assert len({x["projection_rule_id"] for x in r})==100
    assert r[0]["projection_rule_id"]=="TP01-001"
    assert r[-1]["projection_rule_id"]=="TP01-100"
    assert all(x["source_id"]=="SRC-ZZ-003" for x in r)
    assert all(x["palace_id"]=="P10" for x in r)
    assert all(x["source_span_verified"]=="true" for x in r)

def test_case_and_history_counts_reconfirmed():
    r=rows()
    assert sum(x["case_support_only"]=="true" for x in r)==9
    assert sum(bool(x["history_feedback"]) for x in r)==4
    assert {x["projection_rule_id"] for x in r if x["history_feedback"]}=={"TP01-021","TP01-034","TP01-067","TP01-073"}

def test_known_source_repairs():
    m={x["projection_rule_id"]:x for x in rows()}
    assert "紫贪贪狼化忌仍适用" in m["TP01-036"]["condition"]
    assert "冲会大限流煞" in m["TP01-048"]["condition"]
    assert "父母宫或命宫或田宅宫见昌曲" in m["TP01-048"]["condition"]
    assert "火星同度" in m["TP01-084"]["condition"]
    assert "会铃星" in m["TP01-084"]["condition"]

def test_readjudication_100_and_uncertainty():
    d=load(READJ)
    assert d["summary"]["reviewed"]==100
    assert d["summary"]["canonical_promoted"]==100
    assert d["summary"]["reusable_projection_rules"]==91
    assert d["summary"]["case_support_only"]==9
    assert d["summary"]["history_feedback"]==4
    assert d["summary"]["source_resolution_changed_rows"]==["TP01-036","TP01-048","TP01-084"]
    assert d["summary"]["source_text_uncertainty_preserved"]==["TP01-017","TP01-037"]
    assert d["source_basis"]["archived_candidate_status"]=="NONCANONICAL_ACCELERATION_INPUT_ONLY"

def test_source_time_scope_not_silently_narrowed():
    d=load(TIME); m={x["projection_rule_id"]:x for x in d["records"]}
    assert m["TP01-044"]["source_time_layers"]==["DECADE","YEAR"]
    assert m["TP01-045"]["source_time_layers"]==["DECADE","YEAR"]
    assert m["TP01-048"]["scope_status"]=="YEAR_EVENT_WITH_DECADE_CONTEXT"
    assert m["TP01-082"]["scope_status"]=="NATAL_RULE_WITH_LITERAL_LIFE_STAGE_THRESHOLDS"
    assert "age>40 self-acquisition begins" in m["TP01-082"]["literal_thresholds"]

def test_no_new_quantitative_or_time_primitive():
    d=load(READJ)["summary"]
    for k in ["new_primitive_qi","new_memory_type","new_independent_time_scale","numeric_weight","probability","decay"]:
        assert d[k]==0

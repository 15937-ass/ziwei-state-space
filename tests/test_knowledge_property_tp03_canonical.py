import csv
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CSV=ROOT/"validation/wp05/TP03_property_projection_review_201_300.csv"
READJ=ROOT/"knowledge/wp05/property/PROPERTY_TP03_SOURCE_READJUDICATION_100_v0.1.json"
TIME=ROOT/"knowledge/wp05/property/PROPERTY_TP03_SOURCE_TIME_SCOPE_v0.1.json"
GAP=ROOT/"knowledge/wp05/property/PROPERTY_TP03_GAP_LINEAGE_v0.1.json"

def load(p): return json.loads(p.read_text(encoding="utf-8"))
def rows():
    with CSV.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def test_tp03_exact_100_unique_and_source():
    r=rows()
    assert len(r)==100
    assert len({x["projection_rule_id"] for x in r})==100
    assert r[0]["projection_rule_id"]=="TP03-201"
    assert r[-1]["projection_rule_id"]=="TP03-300"
    assert all(x["source_id"]=="SRC-ZZ-003" for x in r)
    assert all(x["palace_id"]=="P10" for x in r)
    assert all(x["source_span_verified"]=="true" for x in r)

def test_case_history_and_time_counts_reconfirmed():
    r=rows()
    assert sum(x["case_support_only"]=="true" for x in r)==18
    assert sum(bool(x["history_feedback"]) for x in r)==2
    assert {x["projection_rule_id"] for x in r if x["history_feedback"]}=={"TP03-238","TP03-248"}
    assert sum(x["time_layer"]=="YEAR" for x in r)==9
    assert sum(x["time_layer"]=="DECADE" for x in r)==1

def test_known_source_repairs_and_uncertainty():
    m={x["projection_rule_id"]:x for x in rows()}
    assert m["TP03-205"]["condition"]=="天府空劫夹"
    assert "所会天相" in m["TP03-206"]["condition"]
    assert "前述受夹情形" in m["TP03-208"]["condition"]
    assert "惊喜" in m["TP03-252"]["condition"]
    assert "巨天太阳同拱者" in m["TP03-266"]["condition"]
    assert "大运流年" in m["TP03-273"]["condition"]
    assert "天相与须见禄" in m["TP03-278"]["condition"]
    assert "魁铖" in m["TP03-287"]["condition"] and "魁钺" not in m["TP03-287"]["condition"]
    assert m["TP03-290"]["projection_target"]=="property_decline_or_loss_pressure_strengthens"
    assert m["TP03-292"]["projection_target"]=="property_acquisition_or_household_celebration_is_supported"

def test_readjudication_census():
    d=load(READJ)
    assert d["summary"]["reviewed"]==100
    assert d["summary"]["canonical_promoted"]==100
    assert d["summary"]["reusable_projection_rules"]==82
    assert d["summary"]["case_support_only"]==18
    assert d["summary"]["history_feedback"]==2
    assert d["summary"]["source_resolution_change_count"]==9
    assert d["summary"]["source_resolution_changed_rows"]==["TP03-206","TP03-208","TP03-252","TP03-266","TP03-273","TP03-278","TP03-287","TP03-290","TP03-292"]
    assert d["summary"]["source_text_uncertainty_preserved"]==["TP03-252","TP03-256","TP03-257","TP03-266","TP03-278","TP03-287","TP03-290","TP03-292"]
    assert d["source_basis"]["archived_candidate_status"]=="NONCANONICAL_ACCELERATION_INPUT_ONLY"

def test_time_scope_and_literal_life_stage():
    d=load(TIME); m={x["projection_rule_id"]:x for x in d["records"]}
    assert len(d["records"])==100
    assert m["TP03-273"]["legacy_primary_time_layer"]=="DECADE"
    assert m["TP03-273"]["source_time_layers"]==["DECADE","YEAR"]
    assert m["TP03-273"]["source_time_labels"]==["大运","流年"]
    assert m["TP03-261"]["literal_life_stage_labels"]==["中年后自置"]
    assert m["TP03-262"]["literal_life_stage_labels"]==["中年后自置（巨门化禄强化）"]
    assert d["summary"]["new_runtime_time_primitives"]==0

def test_tp02_gap_001_closed_only_by_direct_tp03_205_review():
    d=load(GAP)
    assert d["summary"]["prior_gaps_reviewed"]==1
    assert d["summary"]["prior_gaps_closed_by_direct_source_recheck"]==1
    x=d["records"][0]
    assert x["prior_gap_id"]=="TP02-GAP-001"
    assert x["source_surface"]=="空劫夹亦主破败"
    assert x["resolving_rule_id"]=="TP03-205"
    assert x["relation"]=="SEPARATE_BRANCH_NOT_RELOCATION_TRIGGER"
    assert d["summary"]["auto_promotions"]==0

def test_no_new_quantitative_or_time_primitive():
    d=load(READJ)["summary"]
    for k in ["new_primitive_qi","new_memory_type","new_independent_time_scale","numeric_weight","probability","decay"]:
        assert d[k]==0

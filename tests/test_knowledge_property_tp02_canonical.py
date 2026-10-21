import csv
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CSV=ROOT/"validation/wp05/TP02_property_projection_review_101_200.csv"
READJ=ROOT/"knowledge/wp05/property/PROPERTY_TP02_SOURCE_READJUDICATION_100_v0.1.json"
TIME=ROOT/"knowledge/wp05/property/PROPERTY_TP02_SOURCE_TIME_SCOPE_v0.1.json"
GAPS=ROOT/"knowledge/wp05/property/PROPERTY_TP02_SOURCE_GAPS_v0.1.json"

def load(p): return json.loads(p.read_text(encoding="utf-8"))
def rows():
    with CSV.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def test_tp02_exact_100_unique_and_source():
    r=rows()
    assert len(r)==100
    assert len({x["projection_rule_id"] for x in r})==100
    assert r[0]["projection_rule_id"]=="TP02-101"
    assert r[-1]["projection_rule_id"]=="TP02-200"
    assert all(x["source_id"]=="SRC-ZZ-003" for x in r)
    assert all(x["palace_id"]=="P10" for x in r)
    assert all(x["source_span_verified"]=="true" for x in r)

def test_case_history_and_time_counts_reconfirmed():
    r=rows()
    assert sum(x["case_support_only"]=="true" for x in r)==15
    assert sum(bool(x["history_feedback"]) for x in r)==5
    assert {x["projection_rule_id"] for x in r if x["history_feedback"]}=={"TP02-119","TP02-124","TP02-144","TP02-161","TP02-181"}
    assert sum(x["time_layer"]=="YEAR" for x in r)==10

def test_known_source_repairs():
    m={x["projection_rule_id"]:x for x in rows()}
    assert "太阳太阴会合" in m["TP02-103"]["condition"]
    assert "流煞同会或冲会" in m["TP02-103"]["condition"]
    assert "魁然" in m["TP02-107"]["condition"] and "魁钺" not in m["TP02-107"]["condition"]
    assert "为刑为夹" in m["TP02-116"]["condition"]
    assert "火星同躔" in m["TP02-135"]["condition"]
    assert "虚耗刑忌" in m["TP02-135"]["condition"]
    assert m["TP02-136"]["condition"].startswith("武曲化忌或贪狼化忌")
    assert "更见煞忌重重" in m["TP02-150"]["condition"]
    assert "原文“破”" in m["TP02-177"]["condition"]
    assert "火铃同度" in m["TP02-191"]["condition"] and "羊陀交会" in m["TP02-191"]["condition"] and "流煞冲破" in m["TP02-191"]["condition"]
    assert "空劫夹" not in m["TP02-200"]["condition"]

def test_readjudication_census_and_uncertainty():
    d=load(READJ)
    assert d["summary"]["reviewed"]==100
    assert d["summary"]["canonical_promoted"]==100
    assert d["summary"]["reusable_projection_rules"]==85
    assert d["summary"]["case_support_only"]==15
    assert d["summary"]["history_feedback"]==5
    assert d["summary"]["source_resolution_change_count"]==9
    assert d["summary"]["source_resolution_changed_rows"]==["TP02-103","TP02-107","TP02-116","TP02-135","TP02-136","TP02-150","TP02-177","TP02-191","TP02-200"]
    assert d["summary"]["source_text_uncertainty_preserved"]==["TP02-105","TP02-107","TP02-116","TP02-136","TP02-137","TP02-170","TP02-177","TP02-200"]
    assert d["source_basis"]["archived_candidate_status"]=="NONCANONICAL_ACCELERATION_INPUT_ONLY"

def test_time_scope_preserves_minor_limit_and_life_stage():
    d=load(TIME); m={x["projection_rule_id"]:x for x in d["records"]}
    assert len(d["records"])==100
    for rid in ["TP02-175","TP02-176"]:
        assert m[rid]["source_time_layers"]==["YEAR"]
        assert m[rid]["source_time_labels"]==["流年","小限"]
        assert m[rid]["unmapped_source_time_labels"]==["小限"]
    assert m["TP02-122"]["literal_life_stage_labels"]==["中年后产业增加"]
    assert m["TP02-148"]["literal_life_stage_labels"]==["中晚年以后置产业甚丰"]
    assert d["summary"]["new_runtime_time_primitives"]==0

def test_tp02_200_gap_is_separate_branch():
    d=load(GAPS)
    assert d["summary"]["source_explicit_unassigned_projection_gaps"]==1
    x=d["records"][0]
    assert x["gap_id"]=="TP02-GAP-001"
    assert x["source_surface"]=="空劫夹亦主破败"
    assert x["related_candidate_rule_id"]=="TP02-200"
    assert x["relation_to_candidate"]=="SEPARATE_BRANCH_NOT_RELOCATION_TRIGGER"
    assert x["archived_next_batch_candidate_id"]=="TP03-205"
    assert "NOT_YET_CANONICAL" in x["epistemic_status"]
    assert d["summary"]["canonical_rules_created_from_gaps"]==0

def test_no_new_quantitative_or_time_primitive():
    d=load(READJ)["summary"]
    for k in ["new_primitive_qi","new_memory_type","new_independent_time_scale","numeric_weight","probability","decay"]:
        assert d[k]==0

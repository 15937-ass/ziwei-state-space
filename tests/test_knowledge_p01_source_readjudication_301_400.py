import csv, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"knowledge"/"palaces"/"P01_life"/"wp05"
def _csv(n):
    with (BASE/n).open(encoding="utf-8",newline="") as f:return list(csv.DictReader(f))
def _json(n):return json.loads((BASE/n).read_text(encoding="utf-8"))
def test_p04_census():
    r=_csv("LIFE_P04_SOURCE_READJUDICATION_301_400_v0.1.csv")
    assert len(r)==100 and [x["projection_rule_id"] for x in r]==[f"P04-{i:03d}" for i in range(301,401)]
    assert all(x["canonical_promotion"]=="true" and x["source_id"]=="SRC-ZZ-003" for x in r)
    assert sum(x["case_support_only"]=="true" for x in r)==12
def test_pages_and_dependencies():
    r={x["projection_rule_id"]:x for x in _csv("LIFE_P04_SOURCE_READJUDICATION_301_400_v0.1.csv")}
    for k,p in (("P04-301","p12"),("P04-335","p12"),("P04-336","p13"),("P04-371","p13"),("P04-372","p14"),("P04-400","p14")):assert r[k]["source_location"].endswith(p)
    assert r["P04-304"]["opposite_palace_dependency"]=="贪狼" and r["P04-304"]["cross_palace_dependency"]==""
    assert r["P04-306"]["cross_palace_dependency"]==""
    for k in ("P04-340","P04-345","P04-346","P04-347","P04-348","P04-356","P04-357"):assert r[k]["cross_palace_dependency"]==""
    for k in ("P04-349","P04-350","P04-354"):assert r[k]["opposite_palace_dependency"]=="七杀" and r[k]["cross_palace_dependency"]==""
    assert r["P04-372"]["cross_palace_dependency"]=="命宫;事业宫"
    assert r["P04-375"]["opposite_palace_dependency"]=="紫微七杀（紫杀）"
    assert r["P04-321"]["cross_palace_dependency"]=="疾厄宫"
    assert r["P04-338"]["cross_palace_dependency"]=="福德宫;事业宫;夫妻宫"
def test_time_scope():
    r={x["projection_rule_id"]:x for x in _json("LIFE_P04_SOURCE_TIME_SCOPE_301_400_v0.1.json")["records"]}
    assert r["P04-307"]["source_time_layers"]==["YEAR"] and r["P04-312"]["source_time_layers"]==["DECADE"]
    for k in ("P04-326","P04-327","P04-328","P04-329","P04-341","P04-342","P04-343","P04-344","P04-374"):assert r[k]["source_time_layers"]==[] and "GENERIC" in r[k]["scope_status"]
def test_gap_supplement_and_ledger():
    r=_csv("LIFE_P04_SOURCE_GAP_SUPPLEMENT_PP12_14_v0.1.csv")
    assert len(r)==28 and [x["projection_rule_id"] for x in r]==[f"P01-SG-{i:03d}" for i in range(125,153)]
    assert sum(x["case_support_only"]=="true" for x in r)==7
    by={x["projection_rule_id"]:x for x in r}
    assert by["P01-SG-125"]["source_gap_id"]=="P01-SRC-GAP-023" and by["P01-SG-137"]["source_gap_id"]=="P01-SRC-GAP-024"
    assert "并非反背" in by["P01-SG-146"]["source_literal_claim"]
    ts={x["projection_rule_id"]:x for x in _json("LIFE_P04_SOURCE_GAP_TIME_SCOPE_PP12_14_v0.1.json")["records"]}
    assert ts["P01-SG-125"]["source_time_layers"]==["DECADE","YEAR"]
    assert ts["P01-SG-132"]["source_time_layers"]==[] and ts["P01-SG-132"]["scope_status"]=="SOURCE_GENERIC_YEAR_PERIOD_NOT_NARROWED"
    led=_json("LIFE_P03_SOURCE_GAP_LEDGER_v0.1.json");g={x["gap_id"]:x for x in led["entries"]}
    assert g["P01-SRC-GAP-023"]["status"]=="CLOSED_BY_SOURCE_RECHECK_AND_CANONICAL_RULES" and len(g["P01-SRC-GAP-023"]["rule_ids"])==47
    assert g["P01-SRC-GAP-024"]["status"]=="CLOSED_BY_SOURCE_RECHECK_AND_CANONICAL_RULES" and len(g["P01-SRC-GAP-024"]["rule_ids"])==81
    assert led["next_checkpoint_gaps"][0]["gap_id"]=="P01-SRC-GAP-025"
def test_counts():
    s=_json("LIFE_P04_SOURCE_READJUDICATION_SUMMARY_v0.1.json")["summary"]
    assert (s["historical_candidates_reviewed"],s["canonical_promoted"],s["new_source_gap_supplement_records"],s["new_canonical_records"])==(100,100,28,128)
    assert (s["reusable_projection_rules"],s["case_support_only"],s["cumulative_canonical_records_after_merge"])==(109,19,550)
    assert (s["cumulative_reusable_projection_rules_after_merge"],s["cumulative_case_support_only_after_merge"])==(451,99)
    assert s["new_primitive_qi"]==s["new_memory_type"]==s["new_independent_time_scale"]==s["numeric_weight"]==s["probability"]==s["decay"]==0
    assert _json("LIFE_P04_SOURCE_READJUDICATION_SUMMARY_v0.1.json")["human_gate_required"] is False

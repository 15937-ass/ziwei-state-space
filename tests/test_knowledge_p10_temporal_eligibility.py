import csv
import json
from pathlib import Path

from src.product.condition_atoms import compile_condition_spec, fact_from_atom

ROOT=Path(__file__).resolve().parents[1]
CSV=ROOT/"knowledge/palaces/P10_property/wp07b/PROPERTY_TEMPORAL_REACTION_ELIGIBILITY_v0.1.csv"
SUMMARY=ROOT/"knowledge/palaces/P10_property/wp07b/PROPERTY_TEMPORAL_REACTION_ELIGIBILITY_SUMMARY_v0.1.json"

def rows():
    with CSV.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def summary():
    return json.loads(SUMMARY.read_text(encoding="utf-8"))

def test_property_temporal_exact_census():
    r=rows(); s=summary()
    assert len(r)==35
    assert len({x["candidate_id"] for x in r})==35
    assert sum(x["declared_time_layer"]=="YEAR" for x in r)==32
    assert sum(x["declared_time_layer"]=="DECADE" for x in r)==3
    assert sum(x["case_support_only"]=="true" for x in r)==16
    assert sum(x["eligibility_status"].startswith("EXCLUDED_CASE_SUPPORT_ONLY") for x in r)==16
    assert not [x for x in r if x["eligibility_status"]=="ELIGIBLE"]
    assert s["census"]["eligible_for_current_compiler"]==0
    assert s["census"]["blocked_reusable"]==19

def test_case_support_rows_never_enter_runtime():
    for row in rows():
        if row["case_support_only"]=="true":
            assert row["eligibility_status"]=="EXCLUDED_CASE_SUPPORT_ONLY"
            assert "CASE_SUPPORT_ONLY" in row["blocking_reasons"]

def test_clean_tanlang_annual_conditions_are_temporally_representable_but_not_natal_authorized():
    by={x["candidate_id"]:x for x in rows()}
    for rule_id, mutagen in (("TP03-245","禄"),("TP03-246","忌")):
        row=by[rule_id]
        assert row["eligibility_status"]=="BLOCKED_COMPILER_NATAL_ANTECEDENT"
        spec={"all_of":[{"atom_type":"TRANSFORMATION_PRESENT","args":{
            "layer":"YEAR","palace_name":"田宅宫","star":"贪狼","mutagen":mutagen
        }}]}
        compiled=compile_condition_spec(spec)
        facts=frozenset({fact_from_atom(
            "TRANSFORMATION_PRESENT",
            layer="YEAR",palace_name="田宅宫",star="贪狼",mutagen=mutagen
        )})
        assert compiled.matches(facts)
        assert "REQUIRED_NATAL_ANTECEDENT_ABSENT_IN_SOURCE" in row["blocking_reasons"]

def test_tianliang_tianji_rows_fail_closed_on_exact_temporal_binding_shape():
    by={x["candidate_id"]:x for x in rows()}
    for rule_id, mutagen in (("TP04-307","忌"),("TP04-308","禄")):
        row=by[rule_id]
        assert row["eligibility_status"]=="BLOCKED_TEMPORAL_STAR_TRANSFORMATION_BINDING"
        source_minimal=compile_condition_spec({"all_of":[{
            "atom_type":"TRANSFORMATION_PRESENT",
            "args":{"layer":"YEAR","star":"天机","mutagen":mutagen}
        }]})
        runtime_palace_bound=frozenset({fact_from_atom(
            "TRANSFORMATION_PRESENT",
            layer="YEAR",palace_name="田宅宫",star="天机",mutagen=mutagen
        )})
        assert not source_minimal.matches(runtime_palace_bound)

        # The Product gap contract forbids silently joining these independent facts.
        separate=frozenset({
            fact_from_atom("STAR_PRESENT",layer="YEAR",star="天机"),
            fact_from_atom("TRANSFORMATION_PRESENT",layer="YEAR",mutagen=mutagen),
        })
        assert not source_minimal.matches(separate)

def test_multi_layer_and_minor_limit_are_preserved_not_flattened():
    by={x["candidate_id"]:x for x in rows()}
    assert "DECADE+YEAR" in by["TP01-044"]["source_time_scope"]
    assert "DECADE+YEAR" in by["TP01-045"]["source_time_scope"]
    assert "DECADE+YEAR" in by["TP03-273"]["source_time_scope"]
    assert "小限" in by["TP02-175"]["source_time_scope"]
    assert "YEAR_SMALL_LIMIT_COMPOUND_SCOPE" in by["TP02-175"]["blocking_reasons"]

def test_no_new_semantics_or_quantitative_claims():
    s=summary()
    assert s["new_shared_semantics_created"] is False
    assert s["new_runtime_atom_created"] is False
    assert s["new_time_scale_created"] is False
    assert s["numeric_weight"]==0
    assert s["probability"]==0
    assert s["duration_threshold"]==0

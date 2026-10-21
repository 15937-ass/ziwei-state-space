import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PROFILE=ROOT/"knowledge/pattern/BAIGUAN_SUPPORT_PROFILE_v0.1.json"
CRITERION=ROOT/"knowledge/pattern/BAIGUAN_ACTIVATION_CRITERION_v0.1.json"
CAREER=ROOT/"knowledge/wp08/CAREER_STRUCTURED_PATTERN_04_v0.1.json"
C3=ROOT/"knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251_v0.3.json"
C4=ROOT/"knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251_v0.4.json"

def load(p):
    return json.loads(p.read_text(encoding="utf-8"))

def test_baiguan_profile_matches_approved_source_backed_families():
    p=load(PROFILE)
    assert p["anchor_star"]=="紫微"
    assert p["component_families"]["ORTHODOX_SUPPORT"]["members"]==["天府","天相"]
    assert p["component_families"]["ASSISTANT_SUPPORT"]["members"]==["左辅","右弼","天魁","天钺"]
    assert p["component_families"]["AUXILIARY_SUPPORT"]["members"]==["文昌","文曲","禄存","天马"]
    assert p["component_families"]["MINOR_ATTENDANTS"]["members"]==["三台","八座","恩光","天贵","台辅","封诰","龙池","凤阁","天福","天寿"]
    assert p["explicit_exclusions"]==["化禄","化权","化科"]

def test_quality_guards_are_preserved():
    p=load(PROFILE)
    guards={g["component"]:g for g in p["quality_guards"]}
    assert "与地空同度" in guards["天府"]["invalidating_for_normal_treasury_support"]
    assert "与天空同度" in guards["天府"]["invalidating_for_normal_treasury_support"]
    assert "见截空正空" in guards["天府"]["degrading"]
    assert "刑忌夹印" in guards["天相"]["degrading_or_transforming"]
    assert "羊陀夹" in guards["天相"]["degrading_or_transforming"]

def test_source_tension_is_not_erased():
    p=load(PROFILE)
    assert p["source_tension"]["status"]=="PRESERVED"
    assert p["source_tension"]["does_not_imply"]=="天府天相 alone = universal full 百官朝拱 truth"

def test_activation_criterion_freezes_no_universal_threshold():
    c=load(CRITERION)
    assert c["conclusion"]=="NO_UNIVERSAL_THRESHOLD"
    assert c["runtime_contract"]["aggregate_threshold"] is None
    assert c["runtime_contract"]["member_count_rule"] is None
    assert c["runtime_contract"]["pair_count_rule"] is None
    assert c["runtime_contract"]["generic_full_pattern_predicate"]=="UNAVAILABLE"
    assert c["human_gate_alignment"]["new_human_gate_required"] is False

def test_exact_four_career_pattern_rows_dispositioned():
    c=load(CAREER)
    assert c["coverage"]["target_rows"]==4
    assert c["coverage"]["reviewed"]==4
    assert c["coverage"]["remaining"]==0
    assert set(c["coverage"]["source_rule_ids"])=={"CA01-057","CA01-079","CA02-152","CA05-471"}
    assert all("STRUCTURED_PATTERN_EXECUTION_DEFERRED" in r["blockers_before"] for r in c["records"])
    assert all("STRUCTURED_PATTERN_EXECUTION_DEFERRED" not in r["blockers_after"] for r in c["records"])
    assert all("BAIGUAN_ACTIVATION_NO_UNIVERSAL_THRESHOLD" in r["blockers_after"] for r in c["records"])

def test_closure_v04_refines_pattern_blocker_without_unlocking():
    c3,c4=load(C3),load(C4)
    assert len(c3["records"])==251
    assert len(c4["records"])==251
    assert {r["source_rule_id"] for r in c3["records"]}=={r["source_rule_id"] for r in c4["records"]}
    assert c3["summary"]["blocker_counts"]["STRUCTURED_PATTERN_EXECUTION_DEFERRED"]==4
    assert c4["summary"]["structured_pattern_execution_deferred_after"]==0
    assert c4["summary"]["baiguan_activation_no_universal_threshold"]==4
    assert c3["summary"]["rows_with_no_current_activation_blocker"]==17
    assert c4["summary"]["rows_with_no_current_activation_blocker"]==17

def test_specific_other_blockers_are_preserved():
    rows={r["source_rule_id"]:r for r in load(C4)["records"]}
    assert "CLOSED_WORLD_ABSENCE_EVIDENCE" in rows["CA01-057"]["blockers"]
    assert "OPEN_CATEGORY_MEMBER_OR_QUANTIFIER_UNSPECIFIED" in rows["CA05-471"]["blockers"]
    assert rows["CA02-152"]["antecedent_mode"]=="EXPLICIT_RULE_REFERENCE"
    assert rows["CA02-152"]["antecedent_rule_ids"]==["CA02-151"]

def test_no_execution_or_numericization():
    c=load(CAREER)
    assert c["summary"]["source_resolution_changes"]==0
    assert c["summary"]["conditions_compiled"]==0
    assert c["summary"]["execution_unlocked"]==0
    assert all(not r["condition_compiled"] and not r["execution_unlocked"] for r in c["records"])
    p=load(PROFILE)
    assert p["guardrails"]["component_count_threshold"] is None
    assert p["guardrails"]["pair_count_threshold"] is None
    assert p["guardrails"]["weighted_score"] is False

def test_activation_state_ontology_matches_human_gate_boundary():
    p=load(PROFILE)
    assert p["ontology_activation_states"]==[
        "EXPLICIT_TEMPLATE_MATCH","PARTIAL_SUPPORT","CONFLICTED","ABSENT","UNKNOWN"
    ]
    assert p["runtime_v0_1_emittable_states"]==[
        "PARTIAL_SUPPORT","CONFLICTED","ABSENT","UNKNOWN"
    ]
    assert p["full_pattern_truth"]["generic_runtime_emission_allowed"] is False

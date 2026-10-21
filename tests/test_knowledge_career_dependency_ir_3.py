import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
IR=ROOT/"knowledge/wp08/CAREER_DEPENDENCY_IR_3_v0.1.json"
C14=ROOT/"knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251_v0.14.json"
C15=ROOT/"knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251_v0.15.json"

def load(p): return json.loads(p.read_text(encoding="utf-8"))

def test_exact_three_ir_candidates():
    ir=load(IR)
    assert ir["summary"]["ir_records"]==3
    assert [r["child_rule_id"] for r in ir["records"]]==["CA05-420","CA07-639","CA07-682"]
    assert [r["parent_rule_id"] for r in ir["records"]]==["CA05-419","CA07-638","CA07-681"]

def test_ir_is_exact_parent_condition_reference_only():
    ir=load(IR)
    for r in ir["records"]:
        assert r["inheritance_mode"]=="EXACT_PARENT_CONDITION_REFERENCE"
        assert r["parent_composition"]=="SINGLE_PARENT"
        assert r["source_surface_class"]=="EXACT_FOREGOING_REFERENCE"
        assert r["local_delta"] is None
        assert r["parent_effective_blockers"]==[]
        assert r["parent_assessment_complete"] is True
        assert r["inherited_component"]=="PARENT_CONDITION_SCOPE_ONLY"
        assert "PARENT_PROJECTION" in r["prohibited_inheritance"]
        assert r["product_condition_compiled"] is False
        assert r["runtime_authorized"] is False

def test_negative_controls_stay_negative():
    ir=load(IR)
    m={r["source_rule_id"]:r for r in ir["negative_controls"]}
    assert set(m)=={"CA02-171","CA03-236","CA04-323"}
    assert m["CA02-171"]["reason"]=="TRANSITIVE_PARENT_UNCERTAINTY"
    assert "OPEN_VALENCE_CATEGORY_ACTIVATION_CONTEXTUAL_UNRESOLVED" in m["CA02-171"]["effective_parent_blockers"]
    assert m["CA03-236"]["reason"]=="PARENT_SOURCE_UNDERDETERMINED"
    assert m["CA04-323"]["reason"]=="LOCAL_BLOCKERS_AND_PARENT_SCOPE_NOT_ASSESSED"
    assert all(x["must_not_promote"] for x in m.values())

def test_closure_exact_deltas():
    a,b=load(C14),load(C15)
    assert len(a["records"])==len(b["records"])==251
    assert a["summary"]["blocker_counts"]["ANTECEDENT_DEPENDENCY"]==50
    assert b["summary"]["blocker_counts"]["ANTECEDENT_DEPENDENCY"]==47
    assert a["summary"]["readiness_class_counts"]["DEPENDENCY_COMPILER_GATED"]==27
    assert b["summary"]["readiness_class_counts"]["DEPENDENCY_COMPILER_GATED"]==24
    assert a["summary"]["readiness_class_counts"]["LOCAL_STRUCTURE_READY"]==23
    assert b["summary"]["readiness_class_counts"]["LOCAL_STRUCTURE_READY"]==26
    assert a["summary"]["rows_with_no_current_activation_blocker"]==23
    assert b["summary"]["rows_with_no_current_activation_blocker"]==26
    assert b["summary"]["rows_with_source_underdetermination"]==201
    assert b["summary"]["source_resolution_changes"]==45
    assert b["summary"]["source_condition_repairs"]==13
    assert b["summary"]["conditions_compiled"]==0
    assert b["summary"]["execution_unlocked"]==0

def test_only_three_rows_clear_dependency_blocker():
    a,b=load(C14),load(C15)
    am={r["source_rule_id"]:r for r in a["records"]}
    bm={r["source_rule_id"]:r for r in b["records"]}
    cleared=[]
    for rid in am:
        before=set(am[rid]["blockers"])
        after=set(bm[rid]["blockers"])
        if "ANTECEDENT_DEPENDENCY" in before and "ANTECEDENT_DEPENDENCY" not in after:
            cleared.append(rid)
    assert cleared==["CA05-420","CA07-639","CA07-682"]

def test_promoted_rows_are_semantic_only():
    b=load(C15); m={r["source_rule_id"]:r for r in b["records"]}
    for rid in ["CA05-420","CA07-639","CA07-682"]:
        assert m[rid]["blockers"]==[]
        assert m[rid]["activation_status"]=="PARTIAL_LOCAL_STRUCTURE"
        assert m[rid]["readiness_class"]=="LOCAL_STRUCTURE_READY"
        assert m[rid]["dependency_ir_product_condition_compiled"] is False
        assert m[rid]["dependency_ir_runtime_authorized"] is False

def test_guardrails():
    g=load(IR)["guardrails"]
    assert all(v is False for v in g.values())

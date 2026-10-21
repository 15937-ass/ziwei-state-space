import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CENSUS=ROOT/"knowledge/wp08/CAREER_COMPILER_READINESS_CENSUS_26_v0.1.json"
DIR=ROOT/"knowledge/wp08/CAREER_DIRECT_CONDITION_IR_9_v0.1.json"
C15=ROOT/"knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251_v0.15.json"
C16=ROOT/"knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251_v0.16.json"

def load(p): return json.loads(p.read_text(encoding="utf-8"))

def test_census_exact_partition():
    c=load(CENSUS)
    assert len(c["records"])==26
    assert len({r["source_rule_id"] for r in c["records"]})==26
    assert c["summary"]["band_counts"]=={
        "DEPENDENCY_EFFECTIVE_UNDERDETERMINED":11,
        "DIRECT_CONDITION_IR_READY":9,
        "DEPENDENCY_CONDITION_IR_READY":3,
        "DIRECT_RELATION_OR_COMPOSITION_DEFERRED":3,
    }
    assert c["summary"]["total_knowledge_condition_ir_ready"]==12
    assert c["summary"]["not_condition_ir_ready_despite_local_structure_ready"]==14

def test_dependency_ready_and_underdetermined_sets():
    c=load(CENSUS)
    ready={r["source_rule_id"] for r in c["records"] if r["compiler_readiness_band"]=="DEPENDENCY_CONDITION_IR_READY"}
    assert ready=={"CA05-420","CA07-639","CA07-682"}
    u={r["source_rule_id"] for r in c["records"] if r["compiler_readiness_band"]=="DEPENDENCY_EFFECTIVE_UNDERDETERMINED"}
    assert len(u)==11
    x={r["source_rule_id"]:r for r in c["records"]}["CA02-171"]
    assert "OPEN_VALENCE_CATEGORY_ACTIVATION_CONTEXTUAL_UNRESOLVED" in x["effective_parent_blockers"]
    assert x["knowledge_condition_ir_ready"] is False

def test_direct_ir_exact_nine():
    d=load(DIR)
    ids=[r["source_rule_id"] for r in d["records"]]
    assert ids==["CA02-181","CA03-228","CA05-411","CA05-417","CA05-419","CA05-433","CA07-638","CA07-681","CA09-820"]
    assert len(ids)==9
    assert all(r["source_local_only"] for r in d["records"])
    assert all(r["product_condition_compiled"] is False for r in d["records"])
    assert all(r["runtime_authorized"] is False for r in d["records"])

def test_direct_deferred_controls_exact():
    d=load(DIR)
    m={r["source_rule_id"]:r for r in d["deferred_controls"]}
    assert set(m)=={"CA05-484","CA06-582","CA07-699"}
    assert m["CA05-484"]["reason"]=="MEETING_GENERIC_GEOMETRY_UNSPECIFIED"
    assert m["CA06-582"]["reason"]=="COMPOUND_VISIBILITY_PLUS_GENERIC_MEETING_NOT_DETERMINISTIC"
    assert m["CA07-699"]["reason"]=="GENERIC_TONGHUI_GEOMETRY_UNSPECIFIED"

def test_source_local_semantics_are_preserved():
    d=load(DIR); m={r["source_rule_id"]:r for r in d["records"]}
    assert m["CA03-228"]["condition_ir"]["canonical_expression"]=="SAME_PALACE(LOCAL_ANY_OF[火星,铃星])"
    assert m["CA05-411"]["condition_ir"]["canonical_expression"]=="SAME_PALACE(天同化忌, LOCAL_ANY_OF[擎羊,陀罗,火星,铃星])"
    assert m["CA05-433"]["condition_ir"]["canonical_expression"]=="SAME_PALACE(PAIR_CO_PRESENT(天厨,火星))"
    assert m["CA07-681"]["condition_ir"]["canonical_expression"]=="LOCAL_OR[TRANSFORM(巨门,化禄), ATOM(禄存)]"
    assert "TRANSFORM(武曲,化禄)" in m["CA09-820"]["condition_ir"]["canonical_expression"]

def test_v016_is_metadata_only_for_canonical_blockers():
    a,b=load(C15),load(C16)
    assert len(a["records"])==len(b["records"])==251
    assert a["summary"]["blocker_counts"]==b["summary"]["blocker_counts"]
    assert a["summary"]["readiness_class_counts"]==b["summary"]["readiness_class_counts"]
    assert a["summary"]["rows_with_no_current_activation_blocker"]==b["summary"]["rows_with_no_current_activation_blocker"]==26
    assert a["summary"]["rows_with_source_underdetermination"]==b["summary"]["rows_with_source_underdetermination"]==201
    assert b["summary"]["knowledge_condition_ir_ready_total"]==12
    assert b["summary"]["local_structure_ready_but_not_condition_ir_ready"]==14
    assert b["summary"]["conditions_compiled"]==0
    assert b["summary"]["execution_unlocked"]==0

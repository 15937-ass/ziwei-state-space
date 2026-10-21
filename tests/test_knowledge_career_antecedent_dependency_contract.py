import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
GRAPH=ROOT/"knowledge/wp08/CAREER_ANTECEDENT_DEPENDENCY_GRAPH_65_v0.1.json"
CONTRACT=ROOT/"knowledge/wp08/CAREER_DEPENDENCY_CONTRACT_v0.1.json"
C13=ROOT/"knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251_v0.13.json"
C14=ROOT/"knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251_v0.14.json"

def load(p): return json.loads(p.read_text(encoding="utf-8"))

def test_graph_exact_counts():
    g=load(GRAPH)
    assert len(g["records"])==65
    assert g["summary"]["explicit_reference_nodes"]==65
    assert g["summary"]["explicit_edges"]==66
    assert g["summary"]["compiler_gated_reference_nodes"]==50
    assert g["summary"]["already_reference_resolved_nodes"]==15
    assert g["summary"]["single_parent_nodes"]==64
    assert g["summary"]["multi_parent_nodes"]==1

def test_surface_classes_exact():
    s=load(GRAPH)["summary"]["surface_class_counts"]
    assert s=={
      "EXACT_FOREGOING_REFERENCE":28,
      "FOREGOING_REFERENCE_WITH_SOURCE_LOCAL_CONTINUATION":36,
      "EXPLICIT_SOURCE_LOCAL_ADDITIVE_CONTINUATION":1,
    }

def test_graph_is_acyclic_and_depth_bounded():
    g=load(GRAPH)
    assert g["summary"]["cycles"]==0
    assert g["summary"]["max_explicit_reference_depth"]==2
    assert g["summary"]["internal_reference_edges"]==1
    assert g["special_cases"]["CA02_171"]["chain"]=="CA02-171 -> CA02-170 -> CA02-169"

def test_every_parent_resolves_and_no_implicit_edge():
    g=load(GRAPH)
    assert g["summary"]["unresolved_parent_ids"]==0
    assert all(r["antecedent_rule_ids"] for r in g["records"])
    c=load(CONTRACT)
    assert c["semantics"]["reference_identity"].startswith("Rule IDs are authoritative")
    assert c["semantics"]["graph_constraints"]["implicit_parent_inference_allowed"] is False

def test_ca05473_is_branch_union_not_and():
    g=load(GRAPH); m={r["source_rule_id"]:r for r in g["records"]}
    x=m["CA05-473"]
    assert x["antecedent_rule_ids"]==["CA05-471","CA05-472"]
    assert x["parent_composition"]=="SOURCE_BRANCH_UNION_SHARED_QUALIFIER"
    assert "ANY_PARENT_BRANCH" in x["source_composition_adjudication"]["normalized_dependency_expression"]
    assert x["source_composition_adjudication"]["prohibited_interpretation"]=="AND_PARENT_BRANCHES"

def test_ca09847_is_only_non_qiange_additive():
    g=load(GRAPH)
    rows=[r for r in g["records"] if r["surface_class"]=="EXPLICIT_SOURCE_LOCAL_ADDITIVE_CONTINUATION"]
    assert [r["source_rule_id"] for r in rows]==["CA09-847"]
    assert rows[0]["antecedent_rule_ids"]==["CA09-846"]

def test_dependency_gate_readiness_partition():
    g=load(GRAPH)["summary"]
    assert g["dependency_only_rows"]==27
    assert g["dependency_plus_local_blockers_rows"]==23
    assert g["dependency_only_parent_ready"]==3
    assert g["dependency_only_parent_underdetermined"]==24
    assert g["immediate_dependency_compiler_candidate_ids"]==["CA05-420","CA07-639","CA07-682"]

def test_already_resolved_reference_partition():
    g=load(GRAPH)["summary"]
    assert g["already_reference_resolved_rule_ready"]==11
    assert g["already_reference_resolved_other_blockers"]==4

def test_closure_metadata_only_except_ca05473_scope_resolution():
    a,b=load(C13),load(C14)
    assert len(a["records"])==len(b["records"])==251
    assert a["summary"]["blocker_counts"]==b["summary"]["blocker_counts"]
    assert a["summary"]["rows_with_no_current_activation_blocker"]==b["summary"]["rows_with_no_current_activation_blocker"]==23
    assert a["summary"]["rows_with_source_underdetermination"]==b["summary"]["rows_with_source_underdetermination"]==201
    assert b["summary"]["source_resolution_changes"]==45
    assert b["summary"]["dependency_scope_corrections"]==a["summary"]["dependency_scope_corrections"]+1
    assert b["summary"]["conditions_compiled"]==0 and b["summary"]["execution_unlocked"]==0

def test_contract_never_claims_product_compilation():
    c=load(CONTRACT)
    assert c["compiler_boundary"]["knowledge_representation_complete"] is True
    assert c["compiler_boundary"]["product_compiler_implemented"] is False
    assert c["compiler_boundary"]["conditions_compiled"]==0
    assert c["compiler_boundary"]["execution_unlocked"]==0

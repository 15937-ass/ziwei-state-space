import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
LINKS=ROOT/"knowledge/wp08/CAREER_ORDINAL_RULE_LINKS_v0.1.json"
IMPACT=ROOT/"knowledge/wp08/CAREER_ORDINAL_BLOCKER_IMPACT_v0.1.json"
ORD=ROOT/"knowledge/wp08/CAREER_ORDINAL_CONSTRAINTS_v0.1.json"
CLOSURE=ROOT/"knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251_v0.2.json"
def load(p): return json.loads(p.read_text(encoding="utf-8"))

def test_all_130_constraints_dispositioned():
    links,ordr=load(LINKS),load(ORD)
    assert len(links["records"])==130
    assert len({r["constraint_id"] for r in links["records"]})==130
    assert {r["constraint_id"] for r in links["records"]}=={r["constraint_id"] for r in ordr["constraints"]}

def test_linked_rule_ids_exist_in_888_universe_shape():
    links=load(LINKS)
    for row in links["records"]:
        for rid in row["linked_rule_ids"]:
            assert rid.startswith("CA")
            major=int(rid[2:4])
            serial=int(rid.split("-")[1])
            assert 1<=major<=9
            assert 1<=serial<=888

def test_no_adjacency_or_transitive_closure():
    links=load(LINKS)
    assert links["method"]["adjacency_used"] is False
    assert links["guardrails"]["transitive_closure_added"] is False

def test_ordinal_evidence_does_not_fake_activation_resolution():
    impact=load(IMPACT)
    assert impact["summary"]["blockers_resolved_by_ordinal_evidence"]==0
    assert impact["summary"]["execution_unlocked"]==0
    for row in impact["records"]:
        assert row["resolved_blockers"]==[]
        assert row["execution_unlocked"] is False

def test_degree_constraints_do_not_resolve_severity_threshold():
    links={r["constraint_id"]:r for r in load(LINKS)["records"]}
    impact={r["constraint_id"]:r for r in load(IMPACT)["records"]}
    ords={r["constraint_id"]:r for r in load(ORD)["constraints"]}
    for cid,c in ords.items():
        if c["relation_type"]=="DEGREE_LABEL_ONLY" and "SEVERITY_THRESHOLD_UNSPECIFIED" in impact[cid]["linked_activation_blockers"]:
            assert impact[cid]["blocker_impact"]=="QUALITATIVE_REFINEMENT_ONLY"
            assert impact[cid]["resolved_blockers"]==[]

def test_activation_ids_touched_are_real_closure_records():
    closure={r["source_rule_id"] for r in load(CLOSURE)["records"]}
    for row in load(IMPACT)["records"]:
        assert set(row["linked_activation_rule_ids"]).issubset(closure)

def test_no_numericization_or_product_change():
    links,impact=load(LINKS),load(IMPACT)
    assert links["guardrails"]["numeric_weights_added"] is False
    assert links["guardrails"]["probabilities_added"] is False
    assert links["guardrails"]["product_runtime_modified"] is False
    assert impact["guardrails"]["severity_numericized"] is False
    assert impact["guardrails"]["ordinal_as_probability"] is False

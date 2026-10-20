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

def test_final_link_disposition_counts_and_zero_ambiguity():
    links=load(LINKS)
    assert links["disposition_counts"] == {
        "DIRECT_ATOMIC_RULE": 114,
        "METHODOLOGY_OR_CONTEXT_ONLY": 1,
        "MULTI_RULE_SHARED_SOURCE_SENTENCE": 15,
    }
    assert not any(r["disposition"]=="AMBIGUOUS_RULE_LINK" for r in links["records"])
    assert links["coverage"]["linked_atomic_rule_ids"] == 130

def test_no_source_explicit_atomic_gaps_remain():
    links=load(LINKS)
    gaps={r["constraint_id"] for r in links["records"] if r["disposition"]=="SOURCE_EXPLICIT_BUT_ATOMIC_RULE_GAP"}
    assert gaps == set()

def test_oc070_source_context_link_uses_tianfu_luoxian_severity_row():
    links={r["constraint_id"]:r for r in load(LINKS)["records"]}
    row=links["OC-070"]
    assert row["linked_rule_ids"] == ["CA06-538"]
    assert row["link_epistemic"] == "SOURCE_CONTEXT_CRITIC_OVERRIDE"

def test_final_impact_counts_and_zero_resolution():
    impact=load(IMPACT)
    assert impact["summary"]["impact_counts"] == {
        "NO_BLOCKER_REDUCTION": 94,
        "QUALITATIVE_REFINEMENT_ONLY": 36,
    }
    assert impact["summary"]["unique_activation_rules_touched"] == 33
    assert impact["summary"]["blockers_resolved_by_ordinal_evidence"] == 0

def test_oc018_is_recovered_to_existing_atomic_rule():
    links={r["constraint_id"]:r for r in load(LINKS)["records"]}
    row=links["OC-018"]
    assert row["disposition"]=="DIRECT_ATOMIC_RULE"
    assert row["linked_rule_ids"]==["CA03-223"]
    assert row["link_epistemic"]=="SOURCE_CONTEXT_CRITIC_OVERRIDE"

def test_final_source_context_recoveries():
    links={r["constraint_id"]:r for r in load(LINKS)["records"]}
    assert links["OC-018"]["linked_rule_ids"]==["CA03-223"]
    assert links["OC-038"]["linked_rule_ids"]==["CA04-372"]
    assert links["OC-070"]["linked_rule_ids"]==["CA06-538"]
    assert links["OC-102"]["linked_rule_ids"]==["CA08-770"]
    for cid in ["OC-018","OC-038","OC-070","OC-102"]:
        assert links[cid]["link_epistemic"]=="SOURCE_CONTEXT_CRITIC_OVERRIDE"

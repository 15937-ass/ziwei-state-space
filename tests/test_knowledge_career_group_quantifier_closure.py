import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKLOG = ROOT / "knowledge/wp07c/CAREER_BLOCKER_ONTOLOGY_BACKLOG_v0.1.json"
P1 = ROOT / "knowledge/wp07c/CAREER_GROUP_LEXICON_REVIEW_01_v0.1.json"
P2 = ROOT / "knowledge/wp07c/CAREER_GROUP_LEXICON_REVIEW_02_v0.1.json"
P3 = ROOT / "knowledge/wp07c/CAREER_GROUP_LEXICON_REVIEW_03_v0.1.json"
CLOSURE = ROOT / "knowledge/wp07c/CAREER_GROUP_QUANTIFIER_CLOSURE_v0.1.json"
GROUP_CODES = {"GROUP","RELATION_AND_GROUP","ABSENCE_AND_GROUP","DIGNITY_AND_GROUP"}

def load(p): return json.loads(p.read_text())
def order(rule_id):
    ca, seq = rule_id.replace("CA","").split("-")
    return int(ca)*1000 + int(seq)
def expected():
    rows=[r for r in load(BACKLOG)["blocked_records"] if r["blocker_code"] in GROUP_CODES]
    return sorted(rows,key=lambda r:order(r["source_rule_id"]))

def test_final_51_exact():
    d=load(P3); exp=expected()[200:]
    assert len(d["records"]) == 51
    assert [r["source_rule_id"] for r in d["records"]] == [r["source_rule_id"] for r in exp]
    assert d["scope"]["first_source_rule_id"] == "CA07-692"
    assert d["scope"]["last_source_rule_id"] == "CA09-887"
    assert d["scope"]["next_batch_start_source_rule_id"] is None
    assert d["scope"]["cumulative_reviewed"] == 251
    assert d["findings"]["group_quantifier_remaining"] == 0
    assert d["findings"]["source_review_complete"] is True

def test_all_three_batches_cover_exact_251_without_overlap_or_gap():
    parts=[load(P1)["records"],load(P2)["records"],load(P3)["records"]]
    ids=[r["source_rule_id"] for p in parts for r in p]
    exp=[r["source_rule_id"] for r in expected()]
    assert len(ids)==251
    assert len(set(ids))==251
    assert ids==exp

def test_final_batch_preserves_sources_and_stays_locked():
    exp={r["source_rule_id"]:r for r in expected()[200:]}
    for r in load(P3)["records"]:
        s=exp[r["source_rule_id"]]
        assert r["source_condition_text"]==s["source_condition_text"]
        assert r["source_location"]==s["source_location"]
        assert r["review_artifact"]==s["review_artifact"]
        assert r["source_span_ids"]
        assert r["review_reason_zh"]
        assert r["default_quantifier"] is None
        assert r["canonical_group_membership_committed"] is False
        assert r["condition_compiled"] is False
        assert r["execution_unlocked"] is False

def test_final_batch_counts():
    d=load(P3)
    assert Counter(r["blocker_code"] for r in d["records"]) == Counter({
        "GROUP":27,"RELATION_AND_GROUP":16,"ABSENCE_AND_GROUP":7,"DIGNITY_AND_GROUP":1
    })
    assert d["batch_summary"]["records_starting_with_inherited_前格"] == 7
    assert d["batch_summary"]["explicit_or_record_count"] == 4

def test_career_kewen_direct_definition_reconciles_broader_prior_candidate():
    d=load(P3); ev={x["evidence_id"]:x for x in d["source_evidence_catalog"]}
    assert ev["GLEX3-E01"]["career_domain_membership_candidates"] == ["文昌","文曲","龙池","凤阁","天才","化科"]
    assert ev["GLEX3-E01"]["global_transfer"].startswith("NOT_ALLOWED")
    c=load(CLOSURE)
    rec=[x for x in c["reconciliation"] if x["topic"]=="科文诸曜"][0]
    assert "事业宫章节直接定义" in rec["new_status"]
    assert "全局定义仍不推断" in rec["resolution"]

def test_luma_jiaochi_is_named_composite_not_generic_default():
    d=load(P3); ev={x["evidence_id"]:x for x in d["source_evidence_catalog"]}["GLEX3-E03"]
    assert ev["members"] == ["禄存","天马"]
    assert ev["relation"] == "SAME_PALACE_OR_OPPOSITION"
    assert ev["cardinality"] == "BOTH_MEMBERS_REQUIRED_BY_NAMED_COMPOSITE"
    assert ev["generic_luma_shorthand_default"] == "UNRESOLVED"

def test_human_gate_recommends_only_conservative_source_preserving_option():
    c=load(CLOSURE)
    hg=c["human_gate"]
    assert hg["gate_id"]=="HG-KB-GROUP-QUANTIFIER-01"
    assert hg["status"]=="READY_FOR_PI"
    assert hg["recommended_option"]=="A_CONSERVATIVE_SOURCE_PRESERVING"
    opts={o["id"]:o for o in hg["options"]}
    assert opts["B_GLOBAL_ANY_DEFAULT"]["recommendation"]=="REJECT"
    assert opts["C_GLOBAL_ALL_DEFAULT"]["recommendation"]=="REJECT"
    assert c["guardrails"]["executable_semantics_changed"] is False

def test_closure_has_full_coverage_and_no_semantic_smuggling():
    c=load(CLOSURE)
    assert c["coverage"]["total_group_related_blockers"]==251
    assert c["coverage"]["reviewed"]==251
    assert c["coverage"]["remaining"]==0
    unresolved={x["class"] for x in c["remains_unresolved_after_251_review"]}
    assert {"GENERIC_PAIR_CARDINALITY","VALENCE_OR_OPEN_CATEGORY","SEVERITY_CARDINALITY","INHERITED_ANTECEDENT"} <= unresolved

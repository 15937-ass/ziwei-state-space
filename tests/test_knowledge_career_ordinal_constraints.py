import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCHEMA=ROOT/"knowledge/ordinal/ORDINAL_CONSTRAINT_SCHEMA_v0.1.json"
REG=ROOT/"knowledge/wp08/CAREER_ORDINAL_CONSTRAINTS_v0.1.json"
AUDIT=ROOT/"knowledge/wp08/CAREER_ORDINAL_CANDIDATE_AUDIT_v0.1.json"

def load(p):
    return json.loads(p.read_text(encoding="utf-8"))

def test_source_scan_and_candidate_counts():
    r,a=load(REG),load(AUDIT)
    assert r["coverage"]["source_spans_scanned"] == 24
    assert r["coverage"]["candidate_sentences"] == 131
    assert r["coverage"]["accepted_candidate_sentences"] == 120
    assert r["coverage"]["excluded_candidate_sentences"] == 11
    assert r["coverage"]["normalized_constraints"] == 133
    assert a["summary"]["candidate_sentences"] == 131

def test_all_constraints_have_exact_source_provenance():
    r=load(REG)
    for c in r["constraints"]:
        assert c["scope"]["source_id"] == "SRC-ZZ-003"
        assert 132 <= c["scope"]["printed_page"] <= 155
        assert c["scope"]["span_id"].startswith("ZZ003-P")
        assert c["source_sentence"]
        assert c["source_epistemic"] == "SOURCE_EXPLICIT"

def test_no_numericization_or_probability():
    r,s=load(REG),load(SCHEMA)
    for c in r["constraints"]:
        assert c["numeric_value"] is None
        assert c["probability"] is None
        assert c["transitive_closure_allowed"] is False
        assert c["product_execution_unlocked"] is False
        if c["relation_type"]=="DEGREE_LABEL_ONLY":
            assert c["numeric_threshold"] is None
        if c["relation_type"]=="SOURCE_LOCAL_EMPHASIS":
            assert c["numeric_gain"] is None
            assert c["universal_ordering"] is False
    assert s["guardrails"]["numeric_weights_added"] is False
    assert s["guardrails"]["probabilities_added"] is False
    assert s["guardrails"]["transitive_closure_materialized"] is False

def test_key_pairwise_relations_are_preserved():
    rows=load(REG)["constraints"]
    triples={(r["relation_type"],r.get("lhs_source_expression"),r.get("rhs_source_expression"),r.get("metric")) for r in rows}
    assert ("MORE_IMPORTANT_THAN","事业宫本宫星曜","事业宫对宫星曜","interpretive_importance") in triples
    assert ("RANKED_AHEAD_OF","武曲化禄","禄存","廉相会禄条件之财权配置") in triples
    assert ("RANKED_AHEAD_OF","戌宫天同","未宫天同","configuration_rank") in triples
    assert ("RANKED_AHEAD_OF","夜生人","日生人","该太阴格局之贵") in triples
    assert ("RANKED_AHEAD_OF","人和","技能训练","七杀后天培养优先级") in triples
    assert ("WEAKER_THAN","七杀开创力","破军开创力","creative_power") in triples
    assert ("WEAKER_THAN","七杀风险","破军风险","career_risk") in triples
    assert ("PREFERRED_OVER","破军","七杀","毅力") in triples

def test_name_profit_and_power_profit_orders_are_explicit():
    rows=load(REG)["constraints"]
    name_profit=[r for r in rows if r["relation_type"]=="STRONGER_THAN" and r.get("lhs_source_expression")=="名" and r.get("rhs_source_expression")=="利"]
    power_profit=[r for r in rows if r["relation_type"]=="STRONGER_THAN" and r.get("lhs_source_expression")=="权" and r.get("rhs_source_expression")=="利"]
    assert len(name_profit) >= 6
    assert len(power_profit) == 1

def test_severity_labels_stay_qualitative():
    rows=[r for r in load(REG)["constraints"] if r["relation_type"]=="DEGREE_LABEL_ONLY"]
    assert rows
    surfaces={x for r in rows for x in r.get("degree_surfaces",[])}
    assert "煞轻" in surfaces
    assert "煞重" in surfaces
    assert "重重" in surfaces
    assert "力量微薄" in surfaces
    assert all(r.get("numeric_threshold") is None for r in rows)

def test_unsafe_candidates_are_excluded():
    a=load(AUDIT)
    excluded={(r["printed_page"],r["sentence_index"]):r["reason"] for r in a["records"] if r["disposition"]=="EXCLUDED"}
    assert excluded[(132,30)]=="OCR_UNSAFE_COMPOUND_SENTENCE"
    assert excluded[(150,14)]=="LEXICAL_FALSE_POSITIVE_FIRST_SEAT"
    assert excluded[(143,25)]=="OCR_UNSAFE_DEGREE_WORDING"

def test_no_product_execution_unlock():
    r=load(REG)
    assert r["guardrails"]["product_runtime_modified"] is False
    assert r["guardrails"]["execution_unlocked"] is False

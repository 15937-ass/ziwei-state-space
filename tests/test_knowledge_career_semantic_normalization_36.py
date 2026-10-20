import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
NORM=ROOT/"knowledge/wp08/CAREER_SEMANTIC_NORMALIZATION_36_v0.1.json"
C2=ROOT/"knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251_v0.2.json"
C3=ROOT/"knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251_v0.3.json"
SEM=ROOT/"knowledge/normalization/SOURCE_LITERAL_NORMALIZATION_SEMANTICS_v0.1.json"

def load(p):
    return json.loads(p.read_text(encoding="utf-8"))

def test_exact_36_residuals_dispositioned():
    n=load(NORM)
    assert n["coverage"]=={"target_rows":36,"reviewed":36,"remaining":0}
    assert len(n["records"])==36
    assert len({r["source_rule_id"] for r in n["records"]})==36

def test_generic_semantic_blocker_removed_from_all_36():
    n=load(NORM)
    for r in n["records"]:
        assert "SEMANTIC_NORMALIZATION_OR_QUANTIFIER_UNSPECIFIED" in r["blockers_before"]
        assert "SEMANTIC_NORMALIZATION_OR_QUANTIFIER_UNSPECIFIED" not in r["blockers_after"]
        assert r["source_resolution_changed"] is False
        assert r["condition_compiled"] is False
        assert r["execution_unlocked"] is False

def test_closure_v03_preserves_251_and_clears_generic_blocker():
    c2,c3=load(C2),load(C3)
    assert len(c2["records"])==251
    assert len(c3["records"])==251
    assert {r["source_rule_id"] for r in c2["records"]}=={r["source_rule_id"] for r in c3["records"]}
    assert c3["summary"]["semantic_normalization_or_quantifier_unspecified_before"]==36
    assert c3["summary"]["semantic_normalization_or_quantifier_unspecified_after"]==0
    assert "SEMANTIC_NORMALIZATION_OR_QUANTIFIER_UNSPECIFIED" not in c3["summary"]["blocker_counts"]

def test_explicit_source_examples_are_normalized():
    n={r["source_rule_id"]:r for r in load(NORM)["records"]}
    assert n["CA05-423"]["disposition"]=="NORMALIZED_EXPLICIT_LOGICAL_EXPRESSION"
    assert "OR" in n["CA05-423"]["normalized_expression"]
    assert "铃星,陀罗,阴煞,华盖,天刑" in n["CA04-391"]["normalized_expression"]
    assert "天厨" in n["CA05-433"]["normalized_expression"] and "火星" in n["CA05-433"]["normalized_expression"]
    assert "武曲" in n["CA09-818"]["normalized_expression"] and "天府" in n["CA09-818"]["normalized_expression"]

def test_open_categories_remain_open():
    n={r["source_rule_id"]:r for r in load(NORM)["records"]}
    for rid in ["CA02-147","CA03-238","CA03-256","CA03-257","CA04-358","CA04-378"]:
        assert "OPEN_CATEGORY_MEMBER_OR_QUANTIFIER_UNSPECIFIED" in n[rid]["blockers_after"]

def test_precise_source_shorthand_blockers_are_not_silently_closed():
    n={r["source_rule_id"]:r for r in load(NORM)["records"]}
    for rid in ["CA02-107","CA06-502","CA08-723","CA09-864"]:
        assert "SOURCE_SHORTHAND_MEMBERSHIP_UNSPECIFIED" in n[rid]["blockers_after"]
    assert "CARDINALITY_THRESHOLD_UNSPECIFIED" in n["CA07-633"]["blockers_after"]
    assert "TRANSFORMATION_CARRIER_UNSPECIFIED" in n["CA09-860"]["blockers_after"]

def test_structured_pattern_blockers_are_out_of_scope_and_preserved():
    c2,c3=load(C2),load(C3)
    assert c2["summary"]["blocker_counts"]["STRUCTURED_PATTERN_EXECUTION_DEFERRED"]==4
    assert c3["summary"]["blocker_counts"]["STRUCTURED_PATTERN_EXECUTION_DEFERRED"]==4

def test_no_defaults_numericization_or_execution_unlock():
    sem=load(SEM)
    n=load(NORM)
    assert "GROUP_NORMALIZATION_DOES_NOT_INFER_ANY_ALL_N_OF" in sem["invariants"]
    g=n["guardrails"]
    assert g["global_any_default"] is False
    assert g["global_all_default"] is False
    assert g["global_n_of_default"] is False
    assert g["numeric_weights_added"] is False
    assert g["probabilities_added"] is False
    assert g["product_runtime_modified"] is False

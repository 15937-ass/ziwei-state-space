import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "knowledge/core/wp07b/GAP006_GROUP_FAVORABILITY_SOURCE_AUDIT_v0.1.json"

EXPECTED = {
    "CA06-580","CA06-600","CA09-867","TP01-045","TP01-049","TP02-165",
    "TP02-166","TP02-175","TP03-233","TP03-248","TP04-355","TP04-356"
}

def load():
    return json.loads(AUDIT.read_text(encoding="utf-8"))

def test_verdict_and_gap_disposition_are_descriptive_only():
    d = load()
    assert d["verdict"] == "SHARED_DESCRIPTIVE_TAXONOMY_ONLY"
    g = d["gap_disposition"]
    assert g["disposition"] == "DESCRIPTIVE_TAXONOMY_CLARIFIED_EXECUTABLE_HOLD"
    assert g["runtime_semantics_added"] is False
    assert set(g["impacted_rule_ids"]) == EXPECTED
    assert g["impacted_rule_count"] == 12

def test_all_twelve_rows_remain_non_executable():
    d = load()
    rows = d["evidence"]
    assert len(rows) == 12
    assert {r["rule_id"] for r in rows} == EXPECTED
    assert all(r["executable"] is False for r in rows)
    assert all(r["remaining_blockers"] for r in rows)

def test_period_valence_is_not_a_reusable_runtime_fact():
    d = load()
    rows = {r["rule_id"]: r for r in d["evidence"]}
    for rid in ("CA06-580","CA06-600","CA09-867","TP02-175"):
        assert rows[rid]["semantic_class"] == "PERIOD_VALENCE_OR_SUPPORT"
        assert rows[rid]["independent_criterion_defined"] is False
    forbidden = set(d["forbidden_inferences"])
    assert "良好/不佳/吉 defines a reusable period predicate without independent source criteria" in forbidden
    assert "predicted outcome may be reused to define favorable/unfavorable period" in forbidden

def test_group_membership_never_implies_activation_or_cross_palace_globalization():
    d = load()
    assert d["scope_findings"]["career_scope_only"] is True
    assert d["scope_findings"]["property_scoped_category_lexicon_found"] is False
    assert d["scope_findings"]["cross_palace_globalization_authorized"] is False
    forbidden = set(d["forbidden_inferences"])
    assert "Career-scoped category closure applies automatically to Property/P10" in forbidden
    assert "group membership implies ANY member activation" in forbidden
    assert "group membership implies ALL member activation" in forbidden

def test_source_compounds_and_severity_stay_unexpanded():
    d = load()
    rows = {r["rule_id"]: r for r in d["evidence"]}
    assert rows["TP01-045"]["semantic_class"] == "QUALITATIVE_SEVERITY"
    assert rows["TP01-045"]["threshold_status"] == "QUALITATIVE_ONLY_NO_NUMERIC_THRESHOLD"
    assert rows["TP01-049"]["semantic_class"] == "CATEGORY_REFERENCE_SCOPE_OR_ACTIVATION"
    assert rows["TP01-049"]["composition_status"] == "EXPLICIT_MULTI_COMPONENT_CONDITION_PRESERVE_CLAUSE_STRUCTURE"
    for rid in ("TP02-165","TP02-166"):
        assert rows[rid]["semantic_class"] == "SOURCE_COMPOUND_CATEGORY"
        assert rows[rid]["activation_status"] == "UNSPECIFIED"

def test_human_gate_remains_future_not_pending():
    d = load()
    hg = d["human_gate"]
    assert hg["gate_candidate_id"] == "HG-WP07B-FAVORABILITY-AND-GROUPS-01"
    assert hg["status"] == "FUTURE_NOT_PENDING"
    assert hg["required_now"] is False

def test_no_runtime_probability_or_adjacent_gap_expansion():
    d = load()
    g = d["guardrails"]
    assert g["product_modified"] is False
    assert g["runtime_modified"] is False
    assert g["canonical_kmn_kmm_modified"] is False
    assert g["probability_added"] is False
    assert g["numeric_score_added"] is False
    assert g["closed_world_negation_added"] is False
    assert g["persistence_clock_added"] is False

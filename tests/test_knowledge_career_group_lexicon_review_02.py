import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "knowledge/wp07c/CAREER_GROUP_LEXICON_REVIEW_02_v0.1.json"
PREV = ROOT / "knowledge/wp07c/CAREER_GROUP_LEXICON_REVIEW_01_v0.1.json"
BACKLOG = ROOT / "knowledge/wp07c/CAREER_BLOCKER_ONTOLOGY_BACKLOG_v0.1.json"

GROUP_CODES = {"GROUP", "RELATION_AND_GROUP", "ABSENCE_AND_GROUP", "DIGNITY_AND_GROUP"}


def load(path):
    return json.loads(path.read_text())


def order(rule_id):
    ca, seq = rule_id.replace("CA", "").split("-")
    return int(ca) * 1000 + int(seq)


def all_group_rows():
    rows = [r for r in load(BACKLOG)["blocked_records"] if r["blocker_code"] in GROUP_CODES]
    return sorted(rows, key=lambda r: order(r["source_rule_id"]))


def test_exact_second_100_group_blockers_are_reviewed():
    d = load(PATH)
    expected = all_group_rows()[100:200]
    assert len(d["records"]) == d["scope"]["review_batch_size"] == 100
    assert d["scope"]["group_related_blocker_total"] == 251
    assert [r["source_rule_id"] for r in d["records"]] == [r["source_rule_id"] for r in expected]
    assert d["scope"]["first_source_rule_id"] == "CA04-383"
    assert d["scope"]["last_source_rule_id"] == "CA07-691"
    assert d["scope"]["next_batch_start_source_rule_id"] == "CA07-692"


def test_batch_01_and_02_are_contiguous_disjoint_and_cumulative_200():
    d = load(PATH)
    p = load(PREV)
    ids1 = [r["source_rule_id"] for r in p["records"]]
    ids2 = [r["source_rule_id"] for r in d["records"]]
    assert set(ids1).isdisjoint(ids2)
    assert p["scope"]["last_source_rule_id"] == d["scope"]["previous_last_source_rule_id"] == "CA04-382"
    all_ids = [r["source_rule_id"] for r in all_group_rows()[:200]]
    assert ids1 + ids2 == all_ids
    assert d["scope"]["cumulative_reviewed"] == 200
    assert d["findings"]["group_quantifier_remaining"] == 51


def test_every_record_preserves_source_and_has_no_default_semantics():
    d = load(PATH)
    expected = {r["source_rule_id"]: r for r in all_group_rows()[100:200]}
    for row in d["records"]:
        src = expected[row["source_rule_id"]]
        assert row["source_condition_text"] == src["source_condition_text"]
        assert row["source_location"] == src["source_location"]
        assert row["review_artifact"] == src["review_artifact"]
        assert row["source_span_ids"]
        assert row["review_reason_zh"]
        assert row["quantifier_resolution"] == "UNRESOLVED_NO_DEFAULT"
        assert row["default_quantifier"] is None
        assert row["canonical_group_membership_committed"] is False
        assert row["condition_compiled"] is False
        assert row["execution_unlocked"] is False


def test_batch_structure_counts_match_records():
    d = load(PATH)
    counts = Counter(r["blocker_code"] for r in d["records"])
    assert counts == Counter({
        "GROUP": 51,
        "RELATION_AND_GROUP": 37,
        "ABSENCE_AND_GROUP": 9,
        "DIGNITY_AND_GROUP": 3,
    })
    assert d["batch_summary"]["blocker_code_counts"] == dict(counts)
    assert d["batch_summary"]["records_starting_with_inherited_前格"] == 28
    assert d["batch_summary"]["explicit_absence_blocker_count"] == 9
    assert d["batch_summary"]["explicit_relation_and_group_count"] == 37


def test_surface_tokens_and_markers_are_literal_only():
    d = load(PATH)
    for row in d["records"]:
        text = row["source_condition_text"]
        assert all(token in text for token in row["surface_group_tokens"])
        assert all(marker["surface"] in text for marker in row["explicit_surface_markers"])
        assert row["normalization_epistemic"] == "SOURCE_PRESERVING_LEXICAL_CLASSIFICATION"


def test_term_specific_pair_evidence_is_not_global_default():
    d = load(PATH)
    ev = {x["evidence_id"]: x for x in d["source_evidence_catalog"]}
    assert ev["GLEX2-E03"]["term"] == "三台八座"
    assert ev["GLEX2-E03"]["local_quantifier_finding"] == "EXPLICIT_BOTH_AS_PAIR"
    assert ev["GLEX2-E03"]["canonical_default_frozen"] is False
    assert ev["GLEX2-E04"]["local_quantifier_finding"] == "EXPLICIT_BOTH_AS_PAIR_FOR_LONGFENG"
    assert ev["GLEX2-E04"]["canonical_default_frozen"] is False
    assert d["findings"]["generic_pair_shorthand_still_has_no_global_default"] is True


def test_four_and_six_malefic_membership_are_candidates_not_executable_freezes():
    d = load(PATH)
    ev = {x["evidence_id"]: x for x in d["source_evidence_catalog"]}
    assert ev["GLEX2-E01"]["candidate_membership"] == ["擎羊", "陀罗", "火星", "铃星", "地空", "地劫"]
    assert ev["GLEX2-E02"]["candidate_membership"] == ["擎羊", "陀罗", "火星", "铃星"]
    assert "NOT_CANONICALLY_FROZEN" in ev["GLEX2-E01"]["membership_status"]
    assert "NOT_CANONICALLY_FROZEN" in ev["GLEX2-E02"]["membership_status"]
    assert d["guardrails"]["canonical_group_memberships_added"] == 0


def test_local_or_does_not_become_group_internal_or_default():
    d = load(PATH)
    ev = {x["evidence_id"]: x for x in d["source_evidence_catalog"]}["GLEX2-E05"]
    assert ev["source_rule_examples"]
    assert all("或" in x["condition"] for x in ev["source_rule_examples"])
    assert ev["local_quantifier_finding"] == "EXPLICIT_OR_WHERE_WRITTEN"
    assert ev["universal_group_or_supported"] is False
    assert d["findings"]["explicit_or_is_clause_local_not_group_internal_default"] is True


def test_guardrails_keep_batch_non_executable():
    g = load(PATH)["guardrails"]
    assert g["role"] == "AUDIT_ONLY_SOURCE_LEXICON_EVIDENCE"
    assert g["conditions_compiled"] == 0
    assert g["executable_rules_added"] == 0
    assert g["canonical_group_defaults_added"] == 0
    assert g["canonical_group_memberships_added"] == 0
    assert g["product_runtime_modified"] is False
    assert g["production_registry_modified"] is False
    assert g["cross_school_evidence_imported"] is False
    assert g["numeric_weights_or_probabilities_created"] is False
    assert g["source_rows_modified"] is False

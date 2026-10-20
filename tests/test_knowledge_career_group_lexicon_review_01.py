import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "knowledge/wp07c/CAREER_GROUP_LEXICON_REVIEW_01_v0.1.json"
BACKLOG = ROOT / "knowledge/wp07c/CAREER_BLOCKER_ONTOLOGY_BACKLOG_v0.1.json"

GROUP_CODES = {"GROUP", "RELATION_AND_GROUP", "ABSENCE_AND_GROUP", "DIGNITY_AND_GROUP"}


def load(path):
    return json.loads(path.read_text())


def order(rule_id):
    ca, seq = rule_id.replace("CA", "").split("-")
    return int(ca) * 1000 + int(seq)


def expected_batch():
    rows = [r for r in load(BACKLOG)["blocked_records"] if r["blocker_code"] in GROUP_CODES]
    return sorted(rows, key=lambda r: order(r["source_rule_id"]))[:100]


def test_exact_first_100_group_blockers_are_reviewed():
    d = load(PATH)
    expected = expected_batch()
    assert d["scope"]["group_related_blocker_total"] == 251
    assert len(d["records"]) == d["scope"]["review_batch_size"] == 100
    assert [r["source_rule_id"] for r in d["records"]] == [r["source_rule_id"] for r in expected]
    assert d["scope"]["first_source_rule_id"] == "CA01-057"
    assert d["scope"]["last_source_rule_id"] == "CA04-382"


def test_next_batch_pointer_is_derived_without_opening_semantics():
    d = load(PATH)
    rows = [r for r in load(BACKLOG)["blocked_records"] if r["blocker_code"] in GROUP_CODES]
    rows = sorted(rows, key=lambda r: order(r["source_rule_id"]))
    assert d["scope"]["next_batch_start_source_rule_id"] == rows[100]["source_rule_id"]
    assert d["findings"]["rules_unlocked"] == 0


def test_each_record_preserves_source_and_has_no_default_quantifier():
    d = load(PATH)
    expected = {r["source_rule_id"]: r for r in expected_batch()}
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


def test_surface_tokens_and_markers_are_literal_only():
    d = load(PATH)
    for row in d["records"]:
        text = row["source_condition_text"]
        assert all(token in text for token in row["surface_collective_tokens"])
        assert all(marker["surface"] in text for marker in row["explicit_surface_markers"])
        assert row["normalization_epistemic"] == "SOURCE_PRESERVING_LEXICAL_CLASSIFICATION"


def test_source_evidence_catalog_keeps_local_scope_and_transfer_limits():
    d = load(PATH)
    evidence = {e["evidence_id"]: e for e in d["source_evidence_catalog"]}
    assert set(evidence) == {"GLEX-E01", "GLEX-E02", "GLEX-E03", "GLEX-E04", "GLEX-E05"}
    assert evidence["GLEX-E01"]["evidence_category"] == "EXPLICIT_AUXILIARY_EIGHT_MEMBERSHIP"
    assert evidence["GLEX-E03"]["quantifier_transfer"] == "LOCAL_ONLY"
    assert evidence["GLEX-E04"]["quantifier_transfer"] == "LOCAL_ONLY"
    inherited = evidence["GLEX-E05"]["inherited_findings"]
    assert inherited["target_quantifier"] == "UNRESOLVED"
    assert inherited["universal_and_supported"] is False
    assert inherited["universal_or_supported"] is False


def test_batch_counts_and_guardrails_are_consistent():
    d = load(PATH)
    counts = Counter(r["blocker_code"] for r in d["records"])
    assert d["batch_summary"]["blocker_code_counts"] == dict(counts)
    assert counts == Counter({"GROUP": 93, "RELATION_AND_GROUP": 6, "DIGNITY_AND_GROUP": 1})
    g = d["guardrails"]
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

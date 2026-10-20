import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = json.loads((ROOT / "knowledge/wp07a/CAREER_100_REVIEW_07_v0.1.json").read_text())
RECORDS = DOC["mappings"]
BY_ID = {item["source_rule_id"]: item for item in RECORDS}


def test_counts_and_range():
    assert len(RECORDS) == 100
    assert RECORDS[0]["source_rule_id"] == "CA07-647"
    assert RECORDS[-1]["source_rule_id"] == "CA08-749"
    counts = DOC["progress_counts"]
    assert counts["first_time_complete_condition_mappings"] == 24
    assert counts["methodology_or_context_only"] == 11
    assert counts["blocked_outcome_mappings"] == 65
    assert counts["unique_structured_rule_records_before"] == 652
    assert counts["unique_structured_rule_records_after"] == 752


def test_noncomplete_rules_have_null_condition():
    for item in RECORDS:
        if item["review_disposition"] != "COMPLETE_CONDITION_MAPPING":
            assert item["condition"] is None
            assert item["blocker_code"]


def test_key_boundaries():
    assert BY_ID["CA07-674"]["review_disposition"] == "COMPLETE_CONDITION_MAPPING"
    assert BY_ID["CA07-670"]["review_disposition"] == "METHODOLOGY_OR_CONTEXT_ONLY"
    assert BY_ID["CA07-675"]["blocker_code"] == "CONTEXT_STATE"
    assert BY_ID["CA08-710"]["blocker_code"] == "RELATION"
    assert BY_ID["CA08-716"]["blocker_code"] == "RELATION"
    assert BY_ID["CA08-706"]["blocker_code"] == "CONTEXT_STATE"
    assert BY_ID["CA08-746"]["blocker_code"] == "ABSENCE"


def test_source_spans():
    assert [item["printed_page"] for item in DOC["source_spans"]] == [149, 150, 151]
    assert all(item["visual_reviewed"] for item in DOC["source_spans"])
    assert all(len(item["extracted_text_not_silently_corrected"]) > 500 for item in DOC["source_spans"])


def test_guardrails():
    g = DOC["guardrails"]
    assert g["source_rows_modified"] is False
    assert g["product_runtime_modified"] is False
    assert g["production_registry_modified"] is False
    assert g["new_atoms_or_semantic_defaults"] is False
    assert g["outcome_probability_or_empirical_validity_claimed"] is False

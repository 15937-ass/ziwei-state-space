import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "knowledge/palaces/P09_career/gaps/P09_RELATION_SCOPE_GAP_DISPOSITION_3_v0.1.json"
STATE = ROOT / "knowledge/states/P09_CAREER_STATE.yaml"

SOURCE_SHA256 = "6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c"
EXPECTED = {
    "CA05-484": ("ZZ003-P145", "事业宫 printed p145 / PDF physical p73"),
    "CA06-582": ("ZZ003-P147", "事业宫 printed p147 / PDF physical p74"),
    "CA07-699": ("ZZ003-P150", "事业宫 printed p150 / PDF physical p75"),
}


def test_p09_relation_scope_recheck_preserves_source_gaps_and_fail_closed_status():
    payload = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    assert payload["artifact_id"] == "KB-P09-RELATION-SCOPE-GAP-DISPOSITION-3"
    assert payload["status"] == "SOURCE_RECHECKED_RESIDUALS_RETAINED"
    assert payload["issue"] == 784
    assert payload["source"]["source_id"] == "SRC-ZZ-003"
    assert payload["source"]["attachment_sha256"] == SOURCE_SHA256
    assert payload["source"]["visual_review"]["verification_method"] == "DIRECT_PDF_VISUAL_REVIEW"
    assert payload["source"]["visual_review"]["verified_pdf_physical_pages"] == [73, 74, 75]
    assert payload["source"]["visual_review"]["verified_printed_pages"] == [145, 147, 150]

    records = payload["records"]
    assert {row["source_rule_id"] for row in records} == set(EXPECTED)
    assert len(records) == 3
    assert len({row["gap_id"] for row in records}) == 3
    for row in records:
        span, location = EXPECTED[row["source_rule_id"]]
        assert row["source_span_id"] == span
        assert row["source_location"] == location
        assert row["disposition"] == "RETAINED_UNRESOLVED"
        assert row["condition_ir_artifact"] is None
        assert row["condition_compiled"] is False
        assert row["execution_unlocked"] is False
        assert row["product_consumable"] is False
        assert row["relation_gap"]["canonical_geometry"] == "UNSPECIFIED" or row["relation_gap"].get("meeting_geometry") == "UNSPECIFIED"
        assert row["direct_scan_finding"]

    by_id = {row["source_rule_id"]: row for row in records}
    assert by_id["CA05-484"]["preserved_local_semantics"]["source_clause_or_preserved"] is True
    assert by_id["CA06-582"]["relation_gap"]["composition"] == "UNRESOLVED"
    assert by_id["CA06-582"]["preserved_local_semantics"]["source_clause_local_both"] is True
    assert by_id["CA07-699"]["preserved_local_semantics"]["source_clause_local_both"] is True

    assert payload["summary"]["rows_rechecked"] == 3
    assert payload["summary"]["rows_with_source_supported_new_geometry"] == 0
    assert payload["summary"]["rows_retained_unresolved"] == 3
    assert payload["summary"]["canonical_rule_changes"] == 0
    assert payload["summary"]["condition_ir_changes"] == 0
    assert payload["summary"]["product_or_runtime_authorization"] is False
    assert payload["guardrails"]["accepted_888_rule_corpus_reextracted"] is False
    assert payload["guardrails"]["remaining_11_dependency_effective_underdetermined_rows_reopened"] is False


def test_p09_state_points_to_the_bounded_active_gap_issue_without_unlocking_runtime():
    state = STATE.read_text(encoding="utf-8")
    assert 'status: "ACTIVE"' in state
    assert "active_issue: 784" in state
    assert 'active_branch: "knowledge/p09-784-relation-gap-source-recheck"' in state
    assert "active_pr: 784" in state
    assert "No accepted 888-rule corpus re-extraction" in state
    assert "P09 stage is not closed" in state

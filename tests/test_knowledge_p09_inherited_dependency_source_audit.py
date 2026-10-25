import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "knowledge/palaces/P09_career/gaps/P09_INHERITED_DEPENDENCY_SOURCE_AUDIT_11_v0.1.json"
STATE = ROOT / "knowledge/states/P09_CAREER_STATE.yaml"
SOURCE_SHA256 = "6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c"
EXPECTED = {
    "CA01-058": (["CA01-057"], "ZZ003-P133", 133),
    "CA01-060": (["CA01-059"], "ZZ003-P133", 133),
    "CA02-108": (["CA02-107"], "ZZ003-P134", 134),
    "CA02-134": (["CA02-133"], "ZZ003-P135", 135),
    "CA02-157": (["CA02-156"], "ZZ003-P136", 136),
    "CA02-167": (["CA02-166"], "ZZ003-P136", 136),
    "CA02-168": (["CA02-166"], "ZZ003-P136", 136),
    "CA02-170": (["CA02-169"], "ZZ003-P136", 136),
    "CA02-171": (["CA02-170", "CA02-169"], "ZZ003-P136", 136),
    "CA02-199": (["CA02-198"], "ZZ003-P136", 136),
    "CA03-235": (["CA03-234"], "ZZ003-P137", 137),
}


def test_p09_inherited_dependency_audit_covers_exactly_the_11_fail_closed_rows():
    payload = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    assert payload["artifact_id"] == "KB-P09-INHERITED-DEPENDENCY-SOURCE-AUDIT-11-v0.1"
    assert payload["status"] == "SOURCE_RECHECKED_INHERITED_BLOCKERS_RETAINED"
    assert payload["issue"] == 787
    assert payload["source"]["source_id"] == "SRC-ZZ-003"
    assert payload["source"]["attachment_sha256"] == SOURCE_SHA256
    assert payload["source"]["visual_review"]["verification_method"] == "DIRECT_PDF_VISUAL_REVIEW"
    assert payload["source"]["visual_review"]["verified_pdf_physical_pages"] == [67, 68, 69]
    assert payload["source"]["visual_review"]["verified_printed_pages"] == [133, 134, 135, 136, 137]

    records = payload["records"]
    assert len(records) == 11
    assert {row["source_rule_id"] for row in records} == set(EXPECTED)
    assert len({row["gap_id"] for row in records}) == 11
    for row in records:
        parents, span, page = EXPECTED[row["source_rule_id"]]
        assert row["parent_chain"] == parents
        assert row["source_span_id"] == span
        assert f"printed p{page}" in row["source_location"]
        assert row["disposition"] == "RETAINED_UNRESOLVED"
        assert row["inherited_blockers"]
        assert row["direct_scan_finding"]
        assert row["antecedent_edge_changed"] is False

    by_id = {row["source_rule_id"]: row for row in records}
    assert by_id["CA02-171"]["parent_chain"] == ["CA02-170", "CA02-169"]
    assert "SOURCE_LIST_QUANTIFIER_UNSPECIFIED" in by_id["CA01-060"]["inherited_blockers"]
    assert "PAIR_OR_CLOSED_GROUP_ACTIVATION_CONTEXTUAL_UNRESOLVED" in by_id["CA02-167"]["inherited_blockers"]
    assert "SOURCE_COMPOUND_COMPOSITION_UNSPECIFIED" in by_id["CA02-199"]["inherited_blockers"]

    summary = payload["summary"]
    assert summary["rows_rechecked"] == 11
    assert summary["rows_source_resolved_for_inherited_blocker"] == 0
    assert summary["rows_retained_fail_closed"] == 11
    assert summary["antecedent_edges_changed"] == 0
    assert summary["canonical_source_rows_changed"] == 0
    assert summary["condition_ir_changes"] == 0
    assert summary["conditions_compiled"] == 0
    assert summary["execution_unlocked"] == 0
    assert summary["product_or_runtime_authorization"] is False
    assert payload["guardrails"]["accepted_888_rule_corpus_reextracted"] is False
    assert payload["guardrails"]["no_shared_core_semantics_changed"] is True


def test_p09_state_records_completed_gap_audit_without_unlocking_execution():
    state = STATE.read_text(encoding="utf-8")
    assert 'status: "ACTIVE_NO_ACTIVE_WORK"' in state
    assert "active_issue: null" in state
    assert "active_branch: null" in state
    assert "active_pr: null" in state
    assert "Issue #787" in state
    assert "11 inherited dependency-effective-underdetermined rows" in state
    assert "conditions_compiled=0" in state
    assert "execution_unlocked=0" in state
    assert "P09 stage is not closed" in state

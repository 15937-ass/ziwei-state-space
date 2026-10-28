import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CENSUS = ROOT / "knowledge/palaces/P03_spouse/wp05/P03_SOURCE_COVERAGE_CENSUS_ISSUE818_v0.1.json"
TEMPORAL = ROOT / "knowledge/palaces/P03_spouse/wp05/P03_TEMPORAL_RESIDUAL_HANDOFF_ISSUE818_v0.1.json"
REPORT = ROOT / "validation/knowledge/palaces/P03_spouse/issue_818/SOURCE_CENSUS_AND_TEMPORAL_HANDOFF_REVIEW.md"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_census_covers_all_printed_pages_and_accepted_source_records():
    d = load(CENSUS)
    pages = d["page_coverage"]
    assert len(pages) == 19
    assert [p["printed_page"] for p in pages] == list(range(33, 52))
    assert [p["pdf_physical_page"] for p in pages] == [
        17, 17, 18, 18, 19, 19, 20, 20, 21, 21,
        22, 22, 23, 23, 24, 24, 25, 25, 26,
    ]
    assert all(p["visible_section_anchor"] for p in pages)
    assert all(p["first_visible_text_anchor"] for p in pages)
    assert all(p["last_visible_text_anchor"] for p in pages)
    refs = [r for p in pages for r in p["accepted_source_record_refs"]]
    assert len(set(refs)) == 664
    assert d["accepted_baseline"]["unique_source_record_ids"] == 664
    assert d["accepted_baseline"]["unique_candidate_ids"] == 836
    assert d["boundary"]["printed_p52_excluded"] is True
    assert "子女宫" in d["boundary"]["end_anchor"]


def test_all_source_gap_ids_have_explicit_dispositions():
    d = load(CENSUS)
    gaps = d["source_gap_reconciliation"]
    assert len(gaps) == 17
    assert len({g["gap_id"] for g in gaps}) == 17
    expected_open = {
        "P03-SP01-GAP-001",
        "P03-SP02-GAP-001",
        "P03-SP02-GAP-004",
        "P03-SP02-GAP-005",
    }
    open_ids = {
        g["gap_id"] for g in gaps
        if g["census_disposition"].startswith("OPEN")
        or g["census_disposition"].startswith("PARTIALLY")
    }
    assert open_ids == expected_open
    assert all(g["latest_accepted_ledger_status"] for g in gaps)
    by_id = {g["gap_id"]: g for g in gaps}
    assert by_id["P03-SP01-GAP-001"]["followup_issue"] == 819
    assert by_id["P03-SP02-GAP-004"]["followup_issue"] == 819
    assert by_id["P03-SP02-GAP-005"]["followup_issue"] == 819
    assert "机录像" in by_id["P03-SP02-GAP-001"]["scan_literal_if_relevant"]
    assert "即为生变之兆" in by_id["P03-SP01-GAP-001"]["scan_literal_if_relevant"]
    assert d["execution_boundary"]["conditions_compiled"] == 0
    assert d["execution_boundary"]["execution_unlocked"] == 0


def test_temporal_handoff_reconciles_63_groups_and_175_unique_candidate_refs():
    d = load(TEMPORAL)
    r = d["reconciliation"]
    groups = d["residual_groups"]
    assert len(groups) == r["actual_group_count"] == r["expected_group_count"] == 63
    assert r["actual_candidate_row_refs"] == r["expected_candidate_row_refs"] == 175
    assert r["unique_candidate_row_refs"] == 175
    assert r["duplicate_candidate_row_refs"] == []
    assert r["missing_candidate_disposition_refs"] == []
    assert r["all_candidate_refs_resolve"] is True
    refs = []
    for i, group in enumerate(groups, start=1):
        assert group["residual_id"] == f"P03-TEMP-{i:03d}"
        assert group["candidate_row_count"] == len(group["candidate_ids"])
        assert group["candidate_row_count"] == len(group["candidate_rows"])
        assert [row["historical_candidate_id"] for row in group["candidate_rows"]] == group["candidate_ids"]
        assert group["source_expression"]
        assert group["source_reason_as_recorded"]
        assert group["time_granularity_disposition"].startswith("UNRESOLVED_FAIL_CLOSED")
        refs.extend(group["candidate_ids"])
    assert len(refs) == len(set(refs)) == 175
    assert d["execution_boundary"]["history_feedback"] == 0
    assert d["execution_boundary"]["conditions_compiled"] == 0
    assert d["execution_boundary"]["execution_unlocked"] == 0
    assert d["handoff"]["p11_admission_blocked"] is True


def test_review_report_and_followup_handoff_are_present():
    assert REPORT.exists()
    report = REPORT.read_text(encoding="utf-8")
    assert "P03-SP01-GAP-001" in report
    assert "P03-SP02-GAP-001" in report
    assert "Issue #819" in report
    assert "63 组、175 条候选引用" in report

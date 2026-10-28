import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WP05 = ROOT / "knowledge/palaces/P03_spouse/wp05"
CENSUS = WP05 / "P03_SOURCE_COVERAGE_CENSUS_ISSUE818_v0.1.json"
HANDOFF = WP05 / "P03_TEMPORAL_RESIDUAL_HANDOFF_ISSUE818_v0.1.json"
STATE = ROOT / "knowledge/states/P03_SPOUSE_STATE.yaml"
LEDGER_NAMES = [
    *(f"SPOUSE_SP{i:02d}_SOURCE_READJUDICATION_100_v0.1.json" for i in range(1, 9)),
    "SPOUSE_SP09_SOURCE_READJUDICATION_36_v0.1.json",
]
SOURCE_SHA = "6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def accepted_ledgers():
    return [(name, load(WP05 / name)) for name in LEDGER_NAMES]


def test_census_covers_exact_p03_page_boundary_and_record_inventory():
    census = load(CENSUS)
    ledgers = accepted_ledgers()
    pages = census["page_coverage"]

    assert census["issue"] == 818
    assert census["source_basis"]["approved_pdf_sha256"] == SOURCE_SHA
    assert census["boundary"]["printed_p52_excluded"] is True
    assert [p["printed_page"] for p in pages] == list(range(33, 52))
    assert all(
        p["pdf_physical_page"] == ((p["printed_page"] - 33) // 2) + 17
        for p in pages
    )
    assert "夫妻宫" in pages[0]["visible_section_anchor"]
    assert "子女宫" in census["boundary"]["end_anchor"]

    page_record_refs = [
        record_id
        for page in pages
        for record_id in page["accepted_source_record_refs"]
    ]
    page_candidate_refs = [
        candidate_id
        for page in pages
        for candidate_id in page["candidate_ids_referenced_by_these_records"]
        if candidate_id is not None
    ]
    ledger_records = [
        record
        for _, ledger in ledgers
        for record in ledger["records"]
    ]
    ledger_record_ids = [r["projection_rule_id"] for r in ledger_records]
    ledger_candidate_ids = [
        c["historical_candidate_id"]
        for _, ledger in ledgers
        for c in ledger["candidate_batch"]["candidate_dispositions"]
    ]
    ledger_promoted_candidate_ids = {
        r["historical_candidate_id"] for r in ledger_records
        if r.get("historical_candidate_id")
    }

    assert sum(p["accepted_source_record_ref_count"] for p in pages) == len(page_record_refs) == 679
    assert len(set(page_record_refs)) == len(ledger_record_ids) == 664
    assert set(page_record_refs) == set(ledger_record_ids)
    assert len(ledger_record_ids) == len(set(ledger_record_ids))
    assert len(ledger_candidate_ids) == len(set(ledger_candidate_ids)) == 836
    assert set(page_candidate_refs) == ledger_promoted_candidate_ids
    assert len(set(page_candidate_refs)) == 648


def test_all_17_source_gaps_are_reconciled_without_forcing_ambiguous_closure():
    census = load(CENSUS)
    ledgers = accepted_ledgers()
    gaps = census["source_gap_reconciliation"]

    latest_status = {}
    for _, ledger in ledgers:
        for gap in ledger.get("source_coverage_gaps", []):
            latest_status[gap["gap_id"]] = gap["status"]

    assert len(gaps) == 17
    assert len({g["gap_id"] for g in gaps}) == 17
    assert {g["gap_id"] for g in gaps} == set(latest_status)
    assert all(g["latest_accepted_ledger_status"] == latest_status[g["gap_id"]] for g in gaps)

    residuals = {
        g["gap_id"]: g
        for g in gaps
        if g["census_disposition"].startswith("OPEN")
        or g["census_disposition"].startswith("PARTIALLY_RESOLVED")
    }
    assert set(residuals) == {
        "P03-SP01-GAP-001",
        "P03-SP02-GAP-001",
        "P03-SP02-GAP-004",
        "P03-SP02-GAP-005",
    }
    assert residuals["P03-SP01-GAP-001"]["scan_literal_if_relevant"] == "此等宫垣，见煞忌空劫即为生变之兆。"
    assert residuals["P03-SP02-GAP-004"]["followup_issue"] == 819
    assert residuals["P03-SP02-GAP-005"]["followup_issue"] == 819
    assert "机录像" in residuals["P03-SP02-GAP-001"]["scan_literal_if_relevant"]
    assert "YEAR" in residuals["P03-SP02-GAP-001"]["census_note"]
    assert census["accepted_baseline"]["source_coverage_gaps_open_or_partial"] == 4


def test_temporal_handoff_reconciles_all_63_groups_and_175_rows_once():
    handoff = load(HANDOFF)
    final_ledger = load(WP05 / LEDGER_NAMES[-1])
    groups = handoff["residual_groups"]
    source_groups = final_ledger["temporal_scope_residuals"]
    reconciliation = handoff["reconciliation"]

    assert len(groups) == len(source_groups) == 63
    assert [g["residual_id"] for g in groups] == [f"P03-TEMP-{i:03d}" for i in range(1, 64)]
    assert [g["candidate_ids"] for g in groups] == [g["candidate_ids"] for g in source_groups]
    assert [g["source_expression"] for g in groups] == [g["source_expression"] for g in source_groups]
    assert [g["latest_ledger_status"] for g in groups] == [g["status"] for g in source_groups]

    candidate_refs = [candidate_id for group in groups for candidate_id in group["candidate_ids"]]
    candidate_rows = [row for group in groups for row in group["candidate_rows"]]
    assert sum(group["candidate_row_count"] for group in groups) == len(candidate_refs) == 175
    assert len(set(candidate_refs)) == len(candidate_refs)
    assert {row["historical_candidate_id"] for row in candidate_rows} == set(candidate_refs)
    assert all(len(group["candidate_rows"]) == group["candidate_row_count"] for group in groups)
    assert reconciliation["expected_group_count"] == reconciliation["actual_group_count"] == 63
    assert reconciliation["expected_candidate_row_refs"] == reconciliation["actual_candidate_row_refs"] == 175
    assert reconciliation["unique_candidate_row_refs"] == 175
    assert reconciliation["duplicate_candidate_row_refs"] == []
    assert reconciliation["missing_candidate_disposition_refs"] == []
    assert reconciliation["all_candidate_refs_resolve"] is True


def test_cumulative_checkpoint_and_fail_closed_execution_boundary():
    census = load(CENSUS)
    handoff = load(HANDOFF)
    ledgers = accepted_ledgers()
    state = STATE.read_text(encoding="utf-8")

    totals = {
        "reviewed": sum(d["summary"]["reviewed"] for _, d in ledgers),
        "promoted": sum(d["summary"]["canonical_promoted"] for _, d in ledgers),
        "records": sum(d["summary"]["canonical_record_count"] for _, d in ledgers),
        "reusable": sum(d["summary"]["reusable_projection_rules"] for _, d in ledgers),
        "case_only": sum(d["summary"]["case_support_only"] for _, d in ledgers),
        "held": sum(d["summary"]["held"] for _, d in ledgers),
        "deduplicated": sum(d["summary"]["deduplicated"] for _, d in ledgers),
    }
    assert totals == {
        "reviewed": 836,
        "promoted": 648,
        "records": 664,
        "reusable": 462,
        "case_only": 202,
        "held": 183,
        "deduplicated": 5,
    }
    assert census["accepted_baseline"]["candidate_rows_reviewed"] == 836
    assert census["accepted_baseline"]["candidate_rows_promoted"] == 648
    assert census["accepted_baseline"]["source_records"] == 664
    assert census["accepted_baseline"]["reusable_records"] == 462
    assert census["accepted_baseline"]["case_support_only_records"] == 202
    assert census["accepted_baseline"]["held_candidates"] == 183
    assert census["accepted_baseline"]["deduplicated_candidates"] == 5

    for boundary in (census["execution_boundary"], handoff["execution_boundary"]):
        assert boundary["history_feedback"] == 0
        assert boundary["conditions_compiled"] == 0
        assert boundary["execution_unlocked"] == 0
    assert census["execution_boundary"]["no_product_runtime_changes"] is True
    assert census["execution_boundary"]["no_shared_core_semantics"] is True
    assert handoff["execution_boundary"]["no_product_runtime"] is True
    assert handoff["execution_boundary"]["no_shared_core_semantics"] is True
    assert handoff["handoff"]["p11_admission_blocked"] is True
    # The census/handoff PR is accepted with the P03 slot released.
    # The queued follow-up may acquire the slot only in its own activation PR.
    assert 'status: "ACTIVE_NO_ACTIVE_WORK"' in state
    assert "active_issue: null" in state
    assert "active_branch: null" in state
    assert "active_pr: null" in state
    assert "P03_SOURCE_COVERAGE_CENSUS_AND_TEMPORAL_HANDOFF_ACCEPTED" in state
    for gap_id in (
        "P03-SP01-GAP-001",
        "P03-SP02-GAP-001",
        "P03-SP02-GAP-004",
        "P03-SP02-GAP-005",
    ):
        assert gap_id in state
    assert "63 groups / 175 rows" in state
    assert "Issue #819" in state
    assert "conditions_compiled: 0" in state
    assert "execution_unlocked: 0" in state
    assert "history_feedback: 0" in state

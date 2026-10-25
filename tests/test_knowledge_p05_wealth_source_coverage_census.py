import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CENSUS = ROOT / "knowledge/palaces/P05_wealth/coverage/WEALTH_P05_SOURCE_COVERAGE_CENSUS_P69_P92_v0.1.json"
STATE = ROOT / "knowledge/states/P05_WEALTH_STATE.yaml"
SOURCE_HASH = "6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c"


def load():
    return json.loads(CENSUS.read_text(encoding="utf-8"))


def test_source_hash_and_printed_boundary_are_explicit():
    data = load()
    assert data["source_basis"]["source_id"] == "SRC-ZZ-003"
    assert data["source_basis"]["sha256"] == SOURCE_HASH
    assert data["source_basis"]["boundary_literals"]["start"] == "财帛宫"
    assert data["source_basis"]["boundary_literals"]["stop"] == "疾厄宫"
    assert data["source_basis"]["printed_span"].startswith("p69")
    assert "p92" in data["source_basis"]["printed_span"]
    pages = data["physical_page_map"]
    assert pages[0] == {"physical_pdf_page": 35, "printed_pages": "69–70"}
    assert pages[-1] == {"physical_pdf_page": 47, "printed_pages": "93–94"}


def test_accepted_batch_counts_reconcile_without_quota_filling():
    data = load()
    counts = data["record_census"]
    assert counts["source_first_review_records"] == 803
    assert counts["source_first_canonical_promotions"] == 790
    assert counts["source_first_unpromoted"] == 13
    assert counts["p81_supplement_records"] == 4
    assert counts["total_records_accounted"] == 807
    assert counts["total_canonical_reusable_records"] == 794
    assert counts["case_support_only_records"] == 0
    batches = data["accepted_batches"]
    assert len(batches) == 14
    assert sum(b["source_first_review_records"] for b in batches) == 803
    assert sum(b["unpromoted_records"] for b in batches) == 13
    assert sum(b["supplement_records"] for b in batches) == 4
    assert len({b["batch_id"] for b in batches}) == len(batches)


def test_all_22_explicit_residual_gap_ids_are_retained_separately():
    data = load()
    ledger = data["explicit_residual_gap_ledger"]
    expected = (
        {"W05-SG-002"}
        | {f"W06-SG-{i:03d}" for i in range(1, 6)}
        | {f"W08-SG-{i:03d}" for i in range(1, 6)}
        | {f"W09-SG-{i:03d}" for i in range(6, 17)}
    )
    assert ledger["explicit_gap_id_count"] == 22
    assert set(ledger["gap_ids"]) == expected
    assert ledger["status_counts"] == {"PARTIALLY_RESOLVED": 1, "OPEN": 21}
    assert all(g["disposition"].startswith("RETAINED_") for g in ledger["gaps"])


def test_eight_w01_w02_record_uncertainties_are_not_double_counted():
    data = load()
    rows = data["record_level_uncertainties"]
    assert rows["count"] == 8
    assert set(rows["rule_ids"]) == {
        "W01-047", "W01-056", "W01-069", "W01-074", "W01-076", "W01-077",
        "W02-138", "W02-139"
    }
    assert all(r["status"] == "PRESERVED_RECORD_LEVEL_UNCERTAINTY" for r in rows["entries"])


def test_unreviewed_lianzheng_tail_is_not_mistaken_for_complete_coverage():
    data = load()
    disposition = data["disposition"]
    assert disposition["source_span_coverage"] == "NOT_YET_COMPLETE"
    assert disposition["uncovered_source_spans"] == 1
    assert disposition["total_open_coverage_items"] == 23
    assert disposition["next_palace_ready"] is False
    gap = data["uncovered_source_spans"][0]
    assert gap["gap_id"] == "P05-COV-GAP-001"
    assert gap["status"] == "OPEN_UNREVIEWED_SOURCE_SPAN"
    assert "丑未宫" in gap["start_literal"]
    assert "7 天府" in gap["end_boundary"]
    assert "顺耳" in gap["observed_literal_at_page_break"]


def test_state_cache_tracks_census_and_does_not_advance_the_palace_queue():
    state = STATE.read_text(encoding="utf-8")
    assert 'status: "ACTIVE"' in state
    assert "active_issue: 775" in state
    assert 'active_branch: "knowledge/p05-775-source-coverage-census"' in state
    assert "merged_rule_count: 794" in state
    assert "reviewed_rule_count: 803" in state
    assert "source_coverage_gaps_remaining: 23" in state
    assert "P05-COV-GAP-001" in state
    assert "next scheduled palace is P09 事业宫" in state
    assert "No Product/runtime authorization is implied" in state

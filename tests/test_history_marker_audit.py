from src.audit_history_markers import scan


def test_explicit_future_is_high_priority_history_candidate():
    rows = [{
        "rule_id": "R-1",
        "source_location": "p1",
        "condition": "x",
        "target_literal": "当前反应影响后运",
        "target_normalized": "",
        "evidence_text": "",
        "notes": "",
    }]
    got = scan(rows)
    assert len(got) == 1
    assert got[0]["priority"] == "P0_HISTORY_REVIEW"
    assert "EXPLICIT_FUTURE" in got[0]["marker_classes"]


def test_sequence_only_is_review_candidate_not_history_update():
    rows = [{
        "rule_id": "R-2",
        "source_location": "p2",
        "condition": "x",
        "target_literal": "先挫后成",
        "target_normalized": "",
        "evidence_text": "",
        "notes": "",
    }]
    got = scan(rows)
    assert len(got) == 1
    assert got[0]["priority"] == "P1_SEQUENCE_REVIEW"
    assert got[0]["review_status"] == "HEURISTIC_CANDIDATE"


def test_non_temporal_rule_is_not_flagged():
    rows = [{
        "rule_id": "R-3",
        "source_location": "p3",
        "condition": "太阳入庙",
        "target_literal": "发展机会",
        "target_normalized": "",
        "evidence_text": "",
        "notes": "",
    }]
    assert scan(rows) == []


def test_history_marker_snapshot_counts_match_full_corpus():
    import csv
    from pathlib import Path

    with Path("validation/decontamination/A2_history_marker_candidates_v0.1.csv").open(
        "r", encoding="utf-8-sig", newline=""
    ) as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == 45
    assert sum(row["priority"] == "P0_HISTORY_REVIEW" for row in rows) == 27
    assert sum(row["priority"] == "P1_SEQUENCE_REVIEW" for row in rows) == 18
    assert sum(row["review_status"] == "HEURISTIC_CANDIDATE" for row in rows) == 0
    assert sum(row["review_status"].startswith("MIGRATED_A2_R1_") for row in rows) == 18
    assert sum(row["review_status"] == "QUARANTINED_NORMALIZATION_MISMATCH" for row in rows) == 2
    assert sum(row["review_status"].startswith("REVIEWED_") for row in rows) == 25


def test_a2_confirmed_holds_are_subset_of_history_candidates():
    import csv
    from pathlib import Path

    with Path("validation/decontamination/A2_history_marker_candidates_v0.1.csv").open(
        "r", encoding="utf-8-sig", newline=""
    ) as handle:
        candidates = {row["record_id"] for row in csv.DictReader(handle)}

    with Path("validation/decontamination/A2_architecture_hold_v0.1.csv").open(
        "r", encoding="utf-8-sig", newline=""
    ) as handle:
        held = {row["record_id"] for row in csv.DictReader(handle)}

    assert held == {"ZZ-SYS-31-033", "ZZ-SYS-38-034", "ZZ-SYS-41-023"}
    assert held <= candidates


def test_a2_history_source_review_ledger_tracks_all_candidates():
    import csv
    from pathlib import Path

    with Path("validation/decontamination/A2_R1_history_source_review_v0.1.csv").open(
        "r", encoding="utf-8-sig", newline=""
    ) as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == 45
    assert sum(row["source_span_verified"] == "true" for row in rows) == 45
    assert sum(row["source_review_result"] == "PENDING_SOURCE_REVIEW" for row in rows) == 0
    assert sum(row["source_review_result"] == "NORMALIZATION_MISMATCH_CONFIRMED" for row in rows) == 2

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

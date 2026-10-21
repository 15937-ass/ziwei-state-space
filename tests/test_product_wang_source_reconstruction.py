import copy
import json

import pytest

from src.product.wang_source_reconstruction import (
    SIGNATURES_PATH,
    load_wang_source_birth_signatures,
    validate_wang_source_birth_signatures,
    wang_source_candidate_census,
    wang_source_candidates,
)


def _raw():
    return json.loads(SIGNATURES_PATH.read_text(encoding="utf-8"))


def test_source_birth_signature_census_covers_exact_24_cases():
    payload = load_wang_source_birth_signatures()
    assert len(payload["cases"]) == 24
    assert [row["case_id"] for row in payload["cases"]] == [
        f"WANG-CASE-{index:03d}" for index in range(1, 25)
    ]


def test_source_input_maturity_census_is_explicit_and_fail_closed():
    assert wang_source_candidate_census() == {
        "cases_total": 24,
        "cases_source_usable": 22,
        "cases_source_blocked": 2,
        "cases_exact": 12,
        "cases_day_alternatives": 7,
        "cases_zi_time_ambiguous": 3,
        "bounded_candidate_inputs": 37,
    }


def test_explicit_source_day_alternatives_are_not_collapsed():
    payload = load_wang_source_birth_signatures()
    by_id = {row["case_id"]: row for row in payload["cases"]}
    expected = {
        "WANG-CASE-002": [10, 11],
        "WANG-CASE-008": [8, 9],
        "WANG-CASE-014": [4, 12],
        "WANG-CASE-018": [2, 12, 15, 21],
        "WANG-CASE-020": [4, 7, 13],
        "WANG-CASE-022": [10, 20, 23, 29],
        "WANG-CASE-024": [10, 11],
    }
    for case_id, days in expected.items():
        assert by_id[case_id]["lunar_day_candidates"] == days
        assert by_id[case_id]["source_status"] == (
            "SOURCE_EXPLICIT_DAY_ALTERNATIVES"
        )


def test_unqualified_zi_time_expands_to_early_and_late_zi_only():
    payload = load_wang_source_birth_signatures()
    by_id = {row["case_id"]: row for row in payload["cases"]}
    for case_id in ("WANG-CASE-007", "WANG-CASE-017", "WANG-CASE-021"):
        row = by_id[case_id]
        assert row["source_time_label"] == "子"
        assert row["time_index_candidates"] == [0, 12]
        candidates = wang_source_candidates(row)
        assert [item.time_index for item in candidates] == [0, 12]


def test_hard_source_gaps_are_not_backfilled():
    payload = load_wang_source_birth_signatures()
    by_id = {row["case_id"]: row for row in payload["cases"]}

    day_unknown = by_id["WANG-CASE-004"]
    assert day_unknown["source_day_notation"] == "X"
    assert day_unknown["lunar_day_candidates"] == []
    assert wang_source_candidates(day_unknown) == ()

    page_broken = by_id["WANG-CASE-016"]
    assert page_broken["lunar_month"] is None
    assert page_broken["lunar_day_candidates"] == []
    assert page_broken["time_index_candidates"] == []
    assert wang_source_candidates(page_broken) == ()


def test_candidate_expansion_is_source_bounded_cartesian_product():
    payload = load_wang_source_birth_signatures()
    by_id = {row["case_id"]: row for row in payload["cases"]}
    row = by_id["WANG-CASE-018"]
    candidates = wang_source_candidates(row)
    assert [(item.lunar_day, item.time_index) for item in candidates] == [
        (2, 4),
        (12, 4),
        (15, 4),
        (21, 4),
    ]
    assert all(item.lunar_month == 8 for item in candidates)
    assert all(item.gender == "male" for item in candidates)


def test_forbidden_identity_or_expert_answer_leakage_is_rejected():
    payload = _raw()
    mutated = copy.deepcopy(payload)
    mutated["cases"][0]["source_subject_label"] = "SHOULD_NOT_EXIST"
    with pytest.raises(ValueError, match="forbidden leakage"):
        validate_wang_source_birth_signatures(mutated)


def test_incomplete_page_break_row_cannot_be_reverse_backfilled():
    payload = _raw()
    mutated = copy.deepcopy(payload)
    row = mutated["cases"][15]
    row["lunar_month"] = 7
    row["lunar_day_candidates"] = [1]
    row["time_index_candidates"] = [6]
    with pytest.raises(ValueError, match="must not be backfilled"):
        validate_wang_source_birth_signatures(mutated)

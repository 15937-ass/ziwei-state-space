import copy
import json
from pathlib import Path

import pytest

from src.product.wang_source_reconstruction import (
    SIGNATURES_PATH,
    load_wang_reconstruction_readiness,
    load_wang_source_birth_signatures,
    validate_wang_source_birth_signatures,
    validate_wang_reconstruction_readiness,
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


def test_stored_reconstruction_readiness_matches_probe_result():
    report = load_wang_reconstruction_readiness()
    assert report["summary"] == {
        "cases_total": 24,
        "source_candidate_inputs": 37,
        "evaluated_candidate_inputs": 37,
        "unique_anchor_match": 11,
        "multiple_anchor_match": 6,
        "no_anchor_match": 5,
        "blocked_source_incomplete": 2,
        "engine_unsupported": 0,
        "full_chart_materialization_ready": 11,
    }
    rows = {row["case_id"]: row for row in report["cases"]}
    assert all(row["engine_errors"] == [] for row in rows.values())
    assert report["boundaries"]["target_palace_identity_checked"] is True
    assert report["boundaries"]["partial_engine_failure_blocks_promotion"] is True
    assert {
        case_id
        for case_id, row in rows.items()
        if row["status"] == "UNIQUE_ANCHOR_MATCH"
    } == {
        "WANG-CASE-001",
        "WANG-CASE-003",
        "WANG-CASE-006",
        "WANG-CASE-009",
        "WANG-CASE-010",
        "WANG-CASE-012",
        "WANG-CASE-013",
        "WANG-CASE-015",
        "WANG-CASE-019",
        "WANG-CASE-021",
        "WANG-CASE-023",
    }


def test_ambiguous_and_no_match_cases_remain_fail_closed():
    report = load_wang_reconstruction_readiness()
    rows = {row["case_id"]: row for row in report["cases"]}
    assert {
        case_id
        for case_id, row in rows.items()
        if row["status"] == "MULTIPLE_ANCHOR_MATCH"
    } == {
        "WANG-CASE-002",
        "WANG-CASE-008",
        "WANG-CASE-014",
        "WANG-CASE-018",
        "WANG-CASE-020",
        "WANG-CASE-022",
    }
    assert {
        case_id
        for case_id, row in rows.items()
        if row["status"] == "NO_ANCHOR_MATCH"
    } == {
        "WANG-CASE-005",
        "WANG-CASE-007",
        "WANG-CASE-011",
        "WANG-CASE-017",
        "WANG-CASE-024",
    }
    assert all(
        not row["full_chart_materialization_ready"]
        for row in rows.values()
        if row["status"] != "UNIQUE_ANCHOR_MATCH"
    )


def test_probe_uses_explicit_by_lunar_entrypoint_and_target_identity_gate():
    probe_path = (
        Path(__file__).resolve().parents[1]
        / "product"
        / "tools"
        / "wang_lunar_reconstruction_probe.mjs"
    )
    probe = probe_path.read_text(encoding="utf-8")
    assert "astro.byLunar(" in probe
    assert "astro.withOptions(" not in probe
    assert 'entrypoint: "astro.byLunar"' in probe
    assert 'algorithm: "zhongzhou"' in probe
    assert "targetPalaceIdentityMatch" in probe
    assert 'FRIENDS: ["奴仆", "仆役", "交友"]' in probe
    assert "engineErrors.length > 0 || evaluated.length !== inputs.length" in probe


def test_partial_engine_failure_cannot_be_promoted_as_unique():
    report = copy.deepcopy(load_wang_reconstruction_readiness())
    row = next(item for item in report["cases"] if item["case_id"] == "WANG-CASE-002")
    row["status"] = "UNIQUE_ANCHOR_MATCH"
    row["evaluated_candidate_count"] = 1
    row["anchor_match_count"] = 1
    row["matched_candidate_ids"] = ["WANG-CASE-002:D10:T09"]
    row["engine_errors"] = [
        {
            "candidate_id": "WANG-CASE-002:D11:T09",
            "error": "synthetic engine failure",
        }
    ]
    row["full_chart_materialization_ready"] = True
    with pytest.raises(ValueError, match="candidate engine errors must block the case status"):
        validate_wang_reconstruction_readiness(report)


def test_partial_engine_failure_is_preserved_and_remains_unsupported():
    report = copy.deepcopy(load_wang_reconstruction_readiness())
    row = next(item for item in report["cases"] if item["case_id"] == "WANG-CASE-002")
    row["status"] = "ENGINE_UNSUPPORTED"
    row["evaluated_candidate_count"] = 1
    row["anchor_match_count"] = 1
    row["matched_candidate_ids"] = ["WANG-CASE-002:D10:T09"]
    row["engine_errors"] = [
        {
            "candidate_id": "WANG-CASE-002:D11:T09",
            "error": "synthetic engine failure",
        }
    ]
    row["full_chart_materialization_ready"] = False
    report["summary"]["evaluated_candidate_inputs"] = 36
    report["summary"]["multiple_anchor_match"] = 5
    report["summary"]["engine_unsupported"] = 1
    validate_wang_reconstruction_readiness(report)
    assert row["status"] == "ENGINE_UNSUPPORTED"
    assert row["full_chart_materialization_ready"] is False

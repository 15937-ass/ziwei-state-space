import json
from pathlib import Path

from src.product.wang_source_reconstruction import (
    load_wang_reconstruction_readiness,
    load_wang_source_birth_signatures,
    wang_source_candidates,
)

ROOT = Path(__file__).resolve().parents[1]
MATERIALIZER = ROOT / "product" / "tools" / "materialize_wang_full_charts.mjs"

ELIGIBLE_CASES = [
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
]


def test_source_readiness_allows_exactly_the_approved_eleven_cases():
    readiness = load_wang_reconstruction_readiness()
    eligible = [
        row["case_id"]
        for row in readiness["cases"]
        if row["status"] == "UNIQUE_ANCHOR_MATCH"
        and row["full_chart_materialization_ready"] is True
    ]
    assert eligible == ELIGIBLE_CASES
    assert readiness["summary"]["unique_anchor_match"] == 11
    assert readiness["summary"]["multiple_anchor_match"] == 6
    assert readiness["summary"]["no_anchor_match"] == 5
    assert readiness["summary"]["blocked_source_incomplete"] == 2
    assert readiness["summary"]["engine_unsupported"] == 0


def test_each_eligible_source_candidate_set_is_completely_evaluated():
    source = load_wang_source_birth_signatures()
    readiness = load_wang_reconstruction_readiness()
    source_by_id = {row["case_id"]: row for row in source["cases"]}
    ready_by_id = {row["case_id"]: row for row in readiness["cases"]}

    for case_id in ELIGIBLE_CASES:
        candidates = wang_source_candidates(source_by_id[case_id])
        row = ready_by_id[case_id]
        assert row["source_candidate_count"] == len(candidates)
        assert row["evaluated_candidate_count"] == len(candidates)
        assert row["anchor_match_count"] == 1
        assert len(row["matched_candidate_ids"]) == 1
        assert row["engine_errors"] == []


def test_materializer_pins_the_existing_iztro_zhongzhou_contract():
    source = MATERIALIZER.read_text(encoding="utf-8")
    assert 'from "iztro"' in source
    assert 'version: "2.6.1"' in source
    assert 'entrypoint: "astro.byLunar"' in source
    assert 'algorithm: "zhongzhou"' in source
    assert 'dayDivide: "forward"' in source
    assert 'yearDivide: "normal"' in source
    assert 'horoscopeDivide: "normal"' in source
    assert "SELECT_ONLY_AFTER_COMPLETE_EVALUATION_AND_EXACTLY_ONE_SOURCE_ANCHOR_MATCH" in source
    assert "WANG_FULL_CHART_CASE_JSON:" in source


def test_materializer_preserves_the_zi_time_candidate_ambiguity():
    source = load_wang_source_birth_signatures()
    readiness = load_wang_reconstruction_readiness()
    source_row = next(row for row in source["cases"] if row["case_id"] == "WANG-CASE-021")
    ready_row = next(row for row in readiness["cases"] if row["case_id"] == "WANG-CASE-021")
    candidates = wang_source_candidates(source_row)
    candidate_ids = [
        f"{candidate.case_id}:D{candidate.lunar_day:02d}:T{candidate.time_index:02d}"
        for candidate in candidates
    ]
    assert candidate_ids == ["WANG-CASE-021:D01:T00", "WANG-CASE-021:D01:T12"]
    assert ready_row["matched_candidate_ids"] == ["WANG-CASE-021:D01:T00"]
    assert ready_row["source_candidate_count"] == 2
    assert ready_row["evaluated_candidate_count"] == 2
    assert ready_row["anchor_match_count"] == 1


def test_materializer_does_not_read_expert_case_bundles_or_biography():
    source = MATERIALIZER.read_text(encoding="utf-8")
    forbidden = (
        "expert_reasoning_graph",
        "expert_conclusion_refs",
        "outcome_refs",
        "person_group_id",
        "biography",
        "source_subject_label",
    )
    assert all(key not in source for key in forbidden)

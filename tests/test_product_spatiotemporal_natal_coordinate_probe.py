from __future__ import annotations

import json
from pathlib import Path

import pytest

from product.experiments.spatiotemporal_v02.probe import (
    PINNED_FILES,
    REPORT_PATH,
    _load_inputs,
    _occupancy_matrix,
    _permutation_matrix,
    _validate_case,
    make_report,
)

ROOT = Path(__file__).resolve().parents[1]


def test_checked_in_report_is_exactly_reproducible():
    report = make_report()
    checked_in = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    assert report == checked_in
    assert report["status"] == "TEST_ONLY_NOT_CANONICAL"
    assert report["checks"]["input_hashes_match"] is True
    assert report["checks"]["canonical_accepted"] is False
    assert report["checks"]["runtime_effect_allowed"] is False


def test_all_eleven_charts_have_complete_unique_branch_and_palace_maps():
    artifact, _, branch_order, expected_ids = _load_inputs()
    assert tuple(case["case_id"] for case in artifact["cases"]) == expected_ids
    assert len(expected_ids) == 11
    for case in artifact["cases"]:
        case_result, _, _, _ = _validate_case(case, branch_order)
        assert case_result["palace_records"] == 12
        assert case_result["unique_branches"] == 12
        assert case_result["unique_palace_names"] == 12
        assert case_result["target_anchor_reconfirmed"] is True
        assert case_result["full_source_chart_equivalence_verified"] is False


def test_branch_indexed_view_is_invariant_to_artifact_array_order():
    artifact, _, branch_order, _ = _load_inputs()
    for case in artifact["cases"]:
        palaces = case["chart"]["palaces"]
        columns, rows = _occupancy_matrix(palaces, branch_order)
        reversed_columns, reversed_rows = _occupancy_matrix(list(reversed(palaces)), branch_order)
        assert columns == reversed_columns
        assert rows == reversed_rows


def test_permutation_matrices_are_one_hot_for_all_twelve_offsets():
    for offset in range(12):
        matrix = _permutation_matrix(offset)
        assert len(matrix) == 12
        assert all(sum(row) == 1 for row in matrix)
        assert all(sum(matrix[row][column] for row in range(12)) == 1 for column in range(12))


def test_incomplete_or_duplicate_branch_maps_fail_closed():
    artifact, _, branch_order, _ = _load_inputs()
    palaces = artifact["cases"][0]["chart"]["palaces"]
    with pytest.raises(ValueError, match="exact twelve-branch domain"):
        _occupancy_matrix(palaces[:-1], branch_order)

    duplicated = [dict(palace) for palace in palaces]
    duplicated[-1] = dict(duplicated[0])
    with pytest.raises(ValueError, match="duplicate palace branch"):
        _occupancy_matrix(duplicated, branch_order)


def test_source_boundary_and_temporal_limit_are_preserved():
    report = make_report()
    assert report["fixture_summary"]["full_source_chart_equivalence_verified"] == 0
    assert report["fixture_summary"]["temporal_scopes_present"] is False
    assert report["checks"]["full_source_chart_equivalence_claimed"] is False
    assert report["checks"]["temporal_scopes_present"] is False
    assert "six-layer PL1 temporal snapshot mapping" in report["not_evaluated"]
    assert all(PINNED_FILES[key]["git_blob_sha"] for key in PINNED_FILES)

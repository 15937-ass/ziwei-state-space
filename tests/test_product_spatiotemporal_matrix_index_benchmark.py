import json
from pathlib import Path

from product.experiments.spatiotemporal_matrix_index_v0_1.benchmark import (
    FEATURE_WIDTHS,
    REPORT_PATH,
    apply_index,
    apply_matrix,
    compose_index,
    compose_matrix,
    index_from_permutation,
    inverse_index,
    inverse_matrix,
    load_inputs,
    make_correctness_summary,
    matrix_from_permutation,
    matrix_to_permutation,
    synthetic_payload,
)

ROOT = Path(__file__).resolve().parents[1]
EXP_ROOT = ROOT / "product/experiments/spatiotemporal_matrix_index_v0_1"
MANIFEST_PATH = EXP_ROOT / "fixture_manifest_v0.1.json"


def test_fixture_and_manifest_are_pinned_and_source_rows_match():
    fixture, manifest, permutations = load_inputs()
    assert len(fixture["records"]) == 2
    assert len(permutations) == 24
    assert len({tuple(item) for item in permutations}) == 11
    assert manifest["fixture_sha256"] == "05f1dd790faae77ce0caf34af259e0b85c597056f3e18ac207a8e581ee1d2524"
    assert manifest["source_experiment"]["head"] == "a2595cb5e88f854fccd19281e14a7950604ba783"
    assert len(manifest["source_row_sha256"]) == 2


def test_index_and_matrix_views_agree_for_all_pinned_scope_permutations():
    _, _, permutations = load_inputs()
    for permutation in permutations:
        index = index_from_permutation(permutation)
        matrix = matrix_from_permutation(permutation)
        assert matrix_to_permutation(matrix) == index
        for width in FEATURE_WIDTHS:
            payload = synthetic_payload(width)
            assert apply_index(payload, index) == apply_matrix(payload, matrix)


def test_inverse_and_composition_laws_hold_for_all_pinned_scope_pairs():
    _, _, permutations = load_inputs()
    payload = synthetic_payload(12)
    for permutation in permutations:
        index = index_from_permutation(permutation)
        matrix = matrix_from_permutation(permutation)
        inverse = inverse_index(index)
        matrix_inverse = inverse_matrix(matrix)
        assert matrix_to_permutation(matrix_inverse) == inverse
        assert apply_index(apply_index(payload, index), inverse) == payload
        assert apply_matrix(apply_matrix(payload, matrix), matrix_inverse) == payload
    for left in permutations:
        for right in permutations:
            index_composition = compose_index(left, right)
            matrix_composition = compose_matrix(
                matrix_from_permutation(left),
                matrix_from_permutation(right),
            )
            assert matrix_to_permutation(matrix_composition) == index_composition


def test_correctness_summary_reports_expected_bounded_coverage():
    summary = make_correctness_summary()
    assert summary["counts"] == {
        "natal_charts": 2,
        "target_snapshots": 4,
        "temporal_scope_instances": 24,
        "unique_permutations": 11,
        "index_matrix_application_checks": 72,
        "inverse_checks": 24,
        "inverse_roundtrip_checks": 24,
        "all_pair_composition_checks": 576,
    }
    assert all(summary["checks"].values())


def test_committed_benchmark_report_is_observational_and_bounded():
    report = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    assert report["status"] == "TEST_ONLY_ENGINEERING_BENCHMARK"
    assert report["decision"] == "KEEP_INDEX_BASELINE_FOR_CURRENT_PYTHON_LIST_IMPLEMENTATION"
    assert report["workload"]["temporal_scope_instances"] == 24
    assert report["workload"]["timing_thresholds_enforced_in_ci"] is False
    assert report["timing_environment"]["python_version"]
    assert report["timing_environment"]["platform"]
    assert report["measurements"]["serialize_index_bytes"]["json_bytes"] == 27
    assert report["measurements"]["serialize_matrix_bytes"]["json_bytes"] == 313
    assert "optimized NumPy/BLAS" in " ".join(report["limitations"])

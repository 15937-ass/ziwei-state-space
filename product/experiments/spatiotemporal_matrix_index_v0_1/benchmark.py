from __future__ import annotations

import argparse
import hashlib
import json
import platform
import statistics
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
FIXTURE_PATH = ROOT / "fixtures" / "full_snapshot_projection_v0.1.json"
MANIFEST_PATH = ROOT / "fixture_manifest_v0.1.json"
REPORT_PATH = ROOT / "BENCHMARK_REPORT_v0.1.json"
FEATURE_WIDTHS = (12, 64, 256)
IDENTITY = tuple(range(12))


def load_inputs() -> tuple[dict[str, Any], dict[str, Any], list[list[int]]]:
    raw = FIXTURE_PATH.read_bytes()
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    actual_sha = hashlib.sha256(raw).hexdigest()
    if actual_sha != manifest["fixture_sha256"]:
        raise ValueError("pinned v0.3 fixture SHA-256 mismatch")
    fixture = json.loads(raw.decode("utf-8"))
    source_rows = {case_id: digest for case_id, digest in fixture["source_rows"]}
    if source_rows != manifest["source_row_sha256"]:
        raise ValueError("fixture source-row hashes do not match manifest")
    permutations = [
        list(scope["p"])
        for record in fixture["records"]
        for target in record["temporal"]
        for scope in target["scopes"].values()
    ]
    if len(permutations) != 24:
        raise ValueError("fixture must contain exactly 24 temporal scope permutations")
    for permutation in permutations:
        if len(permutation) != 12 or set(permutation) != set(range(12)):
            raise ValueError("each temporal palace order must be a permutation of 0..11")
    return fixture, manifest, permutations


def index_from_permutation(permutation: list[int]) -> tuple[int, ...]:
    return tuple(permutation)


def matrix_from_permutation(permutation: list[int]) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(int(column == source) for column in range(12))
        for source in permutation
    )


def matrix_to_permutation(matrix: Any) -> tuple[int, ...]:
    if len(matrix) != 12 or any(len(row) != 12 for row in matrix):
        raise ValueError("permutation matrix must be 12x12")
    result = []
    for row in matrix:
        if sum(row) != 1 or any(value not in (0, 1) for value in row):
            raise ValueError("each matrix row must contain exactly one 1")
        result.append(row.index(1))
    if set(result) != set(range(12)):
        raise ValueError("matrix columns must also form a permutation")
    return tuple(result)


def apply_index(payload: list[list[int]], permutation: Any) -> list[list[int]]:
    return [payload[source] for source in permutation]


def apply_matrix(payload: list[list[int]], matrix: Any) -> list[list[int]]:
    if len(payload) != 12 or not payload or not payload[0]:
        raise ValueError("payload must have twelve non-empty rows")
    if any(len(row) != len(payload[0]) for row in payload):
        raise ValueError("payload rows must have equal width")
    return [
        [
            sum(matrix[out][source] * payload[source][column] for source in range(12))
            for column in range(len(payload[0]))
        ]
        for out in range(12)
    ]


def inverse_index(permutation: Any) -> tuple[int, ...]:
    inverse = [0] * 12
    for output_position, source_position in enumerate(permutation):
        inverse[source_position] = output_position
    return tuple(inverse)


def inverse_matrix(matrix: Any) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(matrix[row][column] for row in range(12)) for column in range(12))


def compose_index(left: Any, right: Any) -> tuple[int, ...]:
    # Matrix product M(left) @ M(right) selects right[left[i]] at output row i.
    return tuple(right[left[index]] for index in range(12))


def compose_matrix(left: Any, right: Any) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(sum(left[row][k] * right[k][column] for k in range(12)) for column in range(12))
        for row in range(12)
    )


def synthetic_payload(width: int) -> list[list[int]]:
    return [[(row * 17 + column * 13) % 5 for column in range(width)] for row in range(12)]


def _deep_size(value: Any, seen: set[int] | None = None) -> int:
    if seen is None:
        seen = set()
    identity = id(value)
    if identity in seen:
        return 0
    seen.add(identity)
    size = sys.getsizeof(value)
    if isinstance(value, dict):
        size += sum(_deep_size(key, seen) + _deep_size(item, seen) for key, item in value.items())
    elif isinstance(value, (list, tuple, set, frozenset)):
        size += sum(_deep_size(item, seen) for item in value)
    return size


def make_correctness_summary() -> dict[str, Any]:
    fixture, manifest, permutations = load_inputs()
    applications = 0
    inverse_checks = 0
    composition_checks = 0
    roundtrip_checks = 0
    for permutation in permutations:
        index = index_from_permutation(permutation)
        matrix = matrix_from_permutation(permutation)
        if matrix_to_permutation(matrix) != index:
            raise AssertionError("matrix/index permutation construction mismatch")
        for width in FEATURE_WIDTHS:
            payload = synthetic_payload(width)
            if apply_index(payload, index) != apply_matrix(payload, matrix):
                raise AssertionError(f"matrix/index application mismatch at width {width}")
            applications += 1
        inverse = inverse_index(index)
        matrix_inverse = inverse_matrix(matrix)
        if matrix_to_permutation(matrix_inverse) != inverse:
            raise AssertionError("matrix/index inverse mismatch")
        payload = synthetic_payload(12)
        if apply_index(apply_index(payload, index), inverse) != payload:
            raise AssertionError("index inverse roundtrip failed")
        if apply_matrix(apply_matrix(payload, matrix), matrix_inverse) != payload:
            raise AssertionError("matrix inverse roundtrip failed")
        inverse_checks += 1
        roundtrip_checks += 1
    for left in permutations:
        for right in permutations:
            index_composition = compose_index(left, right)
            matrix_composition = compose_matrix(
                matrix_from_permutation(left),
                matrix_from_permutation(right),
            )
            if matrix_to_permutation(matrix_composition) != index_composition:
                raise AssertionError("matrix/index composition mismatch")
            composition_checks += 1
    source_rows = {case_id: digest for case_id, digest in fixture["source_rows"]}
    return {
        "counts": {
            "natal_charts": len(fixture["records"]),
            "target_snapshots": sum(len(record["temporal"]) for record in fixture["records"]),
            "temporal_scope_instances": len(permutations),
            "unique_permutations": len({tuple(item) for item in permutations}),
            "index_matrix_application_checks": applications,
            "inverse_checks": inverse_checks,
            "inverse_roundtrip_checks": roundtrip_checks,
            "all_pair_composition_checks": composition_checks,
        },
        "checks": {
            "fixture_sha256_matches_manifest": hashlib.sha256(FIXTURE_PATH.read_bytes()).hexdigest() == manifest["fixture_sha256"],
            "source_row_hashes_match_manifest": source_rows == manifest["source_row_sha256"],
            "all_scope_orders_are_valid_permutations": all(len(item) == 12 and set(item) == set(range(12)) for item in permutations),
            "index_matrix_application_equivalent": applications == len(permutations) * len(FEATURE_WIDTHS),
            "inverse_and_roundtrip_laws_hold": inverse_checks == 24 and roundtrip_checks == 24,
            "all_pair_composition_laws_hold": composition_checks == len(permutations) ** 2,
        },
    }


def _measure(function: Any, samples: int = 5, loops: int = 100, warmups: int = 20) -> dict[str, Any]:
    for _ in range(warmups):
        function()
    values = []
    for _ in range(samples):
        start = time.perf_counter_ns()
        for _ in range(loops):
            function()
        values.append((time.perf_counter_ns() - start) / loops)
    return {
        "median_ns_per_op": round(statistics.median(values), 1),
        "min_ns_per_op": round(min(values), 1),
        "max_ns_per_op": round(max(values), 1),
        "samples": samples,
        "loops_per_sample": loops,
    }


def _ratio(numerator: float, denominator: float) -> float:
    return round(numerator / denominator, 2) if denominator else 0.0


def make_report() -> dict[str, Any]:
    fixture, manifest, permutations = load_inputs()
    correctness = make_correctness_summary()
    permutation = permutations[0]
    second = permutations[7]
    index = index_from_permutation(permutation)
    matrix = matrix_from_permutation(permutation)
    second_matrix = matrix_from_permutation(second)
    timings: dict[str, Any] = {
        "build_index_map": _measure(lambda: index_from_permutation(permutation)),
        "build_dense_permutation_matrix": _measure(lambda: matrix_from_permutation(permutation)),
        "inverse_index_map": _measure(lambda: inverse_index(permutation)),
        "inverse_dense_matrix": _measure(lambda: inverse_matrix(matrix)),
        "compose_index_maps": _measure(lambda: compose_index(permutation, second)),
        "compose_dense_matrices": _measure(lambda: compose_matrix(matrix, second_matrix)),
        "serialize_index_bytes": {"json_bytes": len(json.dumps(list(permutation), separators=(",", ":")).encode("utf-8"))},
        "serialize_matrix_bytes": {"json_bytes": len(json.dumps(matrix, separators=(",", ":")).encode("utf-8"))},
    }
    for width in FEATURE_WIDTHS:
        payload = synthetic_payload(width)
        timings[f"apply_index_width_{width}"] = _measure(lambda payload=payload: apply_index(payload, permutation))
        timings[f"apply_matrix_width_{width}"] = _measure(lambda payload=payload: apply_matrix(payload, matrix))
    six_permutations = permutations[:6]
    six_matrices = [matrix_from_permutation(item) for item in six_permutations]
    payload = synthetic_payload(64)
    timings["batch_six_layers_index_width_64"] = _measure(
        lambda: [apply_index(payload, item) for item in six_permutations],
        samples=7,
        loops=50,
        warmups=30,
    )
    timings["batch_six_layers_matrix_prebuilt_width_64"] = _measure(
        lambda: [apply_matrix(payload, item) for item in six_matrices],
        samples=7,
        loops=50,
        warmups=30,
    )
    timings["batch_six_layers_matrix_build_and_apply_width_64"] = _measure(
        lambda: [apply_matrix(payload, matrix_from_permutation(item)) for item in six_permutations],
        samples=7,
        loops=50,
        warmups=30,
    )
    timings["retained_memory_estimate_bytes"] = {
        "index_map": _deep_size(list(permutation)),
        "dense_matrix": _deep_size([list(row) for row in matrix]),
    }
    comparisons = {
        "build_matrix_over_index": _ratio(timings["build_dense_permutation_matrix"]["median_ns_per_op"], timings["build_index_map"]["median_ns_per_op"]),
        "inverse_matrix_over_index": _ratio(timings["inverse_dense_matrix"]["median_ns_per_op"], timings["inverse_index_map"]["median_ns_per_op"]),
        "compose_matrix_over_index": _ratio(timings["compose_dense_matrices"]["median_ns_per_op"], timings["compose_index_maps"]["median_ns_per_op"]),
        "apply_matrix_over_index_width_12": _ratio(timings["apply_matrix_width_12"]["median_ns_per_op"], timings["apply_index_width_12"]["median_ns_per_op"]),
        "apply_matrix_over_index_width_64": _ratio(timings["apply_matrix_width_64"]["median_ns_per_op"], timings["apply_index_width_64"]["median_ns_per_op"]),
        "apply_matrix_over_index_width_256": _ratio(timings["apply_matrix_width_256"]["median_ns_per_op"], timings["apply_index_width_256"]["median_ns_per_op"]),
        "batch_matrix_prebuilt_over_index": _ratio(timings["batch_six_layers_matrix_prebuilt_width_64"]["median_ns_per_op"], timings["batch_six_layers_index_width_64"]["median_ns_per_op"]),
        "batch_matrix_build_apply_over_index": _ratio(timings["batch_six_layers_matrix_build_and_apply_width_64"]["median_ns_per_op"], timings["batch_six_layers_index_width_64"]["median_ns_per_op"]),
        "serialized_size_ratio": _ratio(timings["serialize_matrix_bytes"]["json_bytes"], timings["serialize_index_bytes"]["json_bytes"]),
        "memory_ratio": _ratio(timings["retained_memory_estimate_bytes"]["dense_matrix"], timings["retained_memory_estimate_bytes"]["index_map"]),
    }
    return {
        "schema_version": "0.1",
        "status": "TEST_ONLY_ENGINEERING_BENCHMARK",
        "source": {
            "source_experiment_issue": 772,
            "source_experiment_pr": 774,
            "source_experiment_head": manifest["source_experiment"]["head"],
            "fixture_sha256": manifest["fixture_sha256"],
            "source_row_sha256": manifest["source_row_sha256"],
            "fixture_role": manifest["fixture_role"],
        },
        "workload": {
            "case_ids": manifest["selection"]["case_ids"],
            "target_ids": manifest["selection"]["target_ids"],
            "temporal_scope_instances": len(permutations),
            "unique_permutations": len({tuple(item) for item in permutations}),
            "synthetic_payload_widths": list(FEATURE_WIDTHS),
            "batch_layers": 6,
            "index_representation": "12-entry permutation map",
            "matrix_representation": "dense 12x12 one-hot Python tuple/list matrix with explicit pure-Python multiplication",
            "timing_thresholds_enforced_in_ci": False,
        },
        "correctness": correctness,
        "timing_environment": {
            "python_version": sys.version.split()[0],
            "platform": platform.platform(),
            "environment_role": "one observational measurement runtime; not the GitHub Actions CI runtime",
            "cpu_model": "not captured",
        },
        "timing_protocol": {
            "single_operation_samples": 5,
            "single_operation_loops_per_sample": 100,
            "single_operation_warmups": 20,
            "six_layer_batch_samples": 7,
            "six_layer_batch_loops_per_sample": 50,
            "six_layer_batch_warmups": 30,
            "statistic": "median nanoseconds per operation, with min/max across samples",
            "note": "Timing snapshots vary by runtime and host; compare environments before comparing values.",
        },
        "measurements": timings,
        "relative_cost_ratios": comparisons,
        "decision": "KEEP_INDEX_BASELINE_FOR_CURRENT_PYTHON_LIST_IMPLEMENTATION",
        "limitations": [
            "Performance payloads are deterministic synthetic numeric rows; they are not source-transcribed chart truth.",
            "The dense matrix uses explicit pure-Python list-of-lists multiplication; optimized NumPy/BLAS, sparse representations and compiled kernels were not evaluated.",
            "These microbenchmarks do not establish production workload performance or a universal claim against matrix representations.",
            "The fixture is a reduced engine-generated projection, not source-transcribed ground truth.",
            "The scope-level mutagen-to-transformation-glyph binding remains unresolved and is not inferred.",
            "No traditional semantic correctness, canonical rule eligibility, predictive validity, or production migration claim is made.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="TEST_ONLY index-vs-matrix cost/benefit benchmark")
    parser.add_argument("--write-report", action="store_true", help="write the timing snapshot to BENCHMARK_REPORT_v0.1.json")
    args = parser.parse_args()
    report = make_report()
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.write_report:
        REPORT_PATH.write_text(rendered, encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()

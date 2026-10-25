"""TEST_ONLY natal-coordinate probe; no production execution path."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[3]
REPORT_PATH = ROOT / "product/experiments/spatiotemporal_v02/COMPARISON_REPORT_v0.2.json"

PINNED_FILES = {
    "artifact": {
        "path": "product/expert_cases/wang_tingzhi/FULL_CHART_MATERIALIZATION_V0_1B.json",
        "git_blob_sha": "3778e5f3d66c1e5ab44461360b6d9f71b3f8be56",
        "sha256": "402e607e7b563f2fe12de7d0c4cc8c5bec11f26bcee7c6b4a6f9c2243b1dfff1",
    },
    "relation": {
        "path": "knowledge/relation/RELATION_SEMANTICS_v0.1.json",
        "git_blob_sha": "26e6984b386954e18604f83de038a623365c85b6",
        "sha256": "a4192ff3c5b3d8be41ead79db2b447cc134fe499859d626b025c94ba77576b1c",
    },
    "branch_source": {
        "path": "src/product/structure_primitives.py",
        "git_blob_sha": "e4d0645b42c44fb737ee234960114253af23bd41",
        "sha256": "eeb8ade67e500e6d795912c05ad6058cce9e375cab790aaeedc1a3c615fe060c",
    },
    "materializer": {
        "path": "src/product/wang_full_chart_materialization.py",
        "git_blob_sha": "58b6ebdaf5b1e364798cec0361817dbe981d743a",
        "sha256": "8e9543c8a0d46f9bd0568cfa2497e356b28fb8dc947fe4ebae04d6e8d9b586a0",
    },
}
PIN_ORDER = ("artifact", "relation", "branch_source", "materializer")
EXPECTED_BRANCH_ORDER = tuple("子丑寅卯辰巳午未申酉戌亥")
STAR_FIELDS = ("major_stars", "minor_stars", "adjective_stars")
EXPECTED_ARTIFACT_ID = "WANG_FULL_CHART_MATERIALIZATION_V0_1B"
EXPECTED_MATERIALIZATION_LEVEL = "SOURCE_INPUT_RECONSTRUCTED_TARGET_ANCHOR_VERIFIED"


def _git_blob_sha(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


def _read_pinned_text(key: str) -> str:
    pin = PINNED_FILES[key]
    raw = (ROOT / pin["path"]).read_bytes()
    actual_blob = _git_blob_sha(raw)
    actual_sha256 = hashlib.sha256(raw).hexdigest()
    if actual_blob != pin["git_blob_sha"]:
        raise ValueError(f"{key}: Git blob mismatch: {actual_blob}")
    if actual_sha256 != pin["sha256"]:
        raise ValueError(f"{key}: SHA-256 mismatch: {actual_sha256}")
    return raw.decode("utf-8")


def _parse_branch_order(source: str) -> tuple[str, ...]:
    match = re.search(r"BRANCH_ORDER\s*=\s*\(([^)]*)\)", source, re.S)
    if not match:
        raise ValueError("pinned branch source has no BRANCH_ORDER tuple")
    values = tuple(re.findall(r"""["']([^"']+)["']""", match.group(1)))
    if values != EXPECTED_BRANCH_ORDER:
        raise ValueError(f"unexpected BRANCH_ORDER: {values}")
    return values


def _parse_expected_case_ids(source: str) -> tuple[str, ...]:
    match = re.search(r"EXPECTED_CASE_IDS\s*=\s*\((.*?)\n\)", source, re.S)
    if not match:
        raise ValueError("pinned materializer has no EXPECTED_CASE_IDS tuple")
    values = tuple(re.findall(r"""["'](WANG-CASE-\d+)["']""", match.group(1)))
    if len(values) != 11 or len(set(values)) != 11:
        raise ValueError("pinned materializer case IDs are not the expected unique set of 11")
    return values


def _load_inputs() -> tuple[dict[str, Any], dict[str, Any], tuple[str, ...], tuple[str, ...]]:
    texts = {key: _read_pinned_text(key) for key in PIN_ORDER}
    artifact = json.loads(texts["artifact"])
    relation = json.loads(texts["relation"])
    branch_order = _parse_branch_order(texts["branch_source"])
    expected_case_ids = _parse_expected_case_ids(texts["materializer"])

    if artifact.get("artifact_id") != EXPECTED_ARTIFACT_ID:
        raise ValueError("unexpected source artifact ID")
    if artifact.get("schema_version") != "0.1B":
        raise ValueError("unexpected source artifact schema version")
    if artifact.get("materialization_level") != EXPECTED_MATERIALIZATION_LEVEL:
        raise ValueError("unexpected materialization claim")
    if relation.get("coordinate_model", {}).get("id") != "PALACE_RELATION_Z12_OFFSET":
        raise ValueError("unexpected relation coordinate model")
    if relation.get("coordinate_model", {}).get("delta_formula") != (
        "delta=(p_object-p_subject) mod 12"
    ):
        raise ValueError("unexpected relation delta formula")
    return artifact, relation, branch_order, expected_case_ids


def _star_token(field: str, star: Mapping[str, Any]) -> str:
    return field + ":" + json.dumps(
        dict(star), ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )


def _occupancy_matrix(
    palaces: list[Mapping[str, Any]], branch_order: tuple[str, ...]
) -> tuple[tuple[str, ...], tuple[tuple[int, ...], ...]]:
    by_branch: dict[str, Mapping[str, Any]] = {}
    for palace in palaces:
        branch = palace.get("branch")
        if branch not in branch_order:
            raise ValueError(f"unsupported or missing palace branch: {branch!r}")
        if branch in by_branch:
            raise ValueError(f"duplicate palace branch: {branch}")
        by_branch[branch] = palace
    if set(by_branch) != set(branch_order):
        raise ValueError("palace list does not cover the exact twelve-branch domain")

    tokens_by_branch: list[list[str]] = []
    for branch in branch_order:
        palace = by_branch[branch]
        tokens: list[str] = [
            "palace_identity:" + json.dumps(
                {"name": palace.get("name")}, ensure_ascii=False, sort_keys=True, separators=(",", ":")
            )
        ]
        for field in STAR_FIELDS:
            stars = palace.get(field)
            if not isinstance(stars, list):
                raise ValueError(f"{branch}.{field} must be an array")
            for star in stars:
                if not isinstance(star, Mapping):
                    raise ValueError(f"{branch}.{field} contains a non-object star")
                tokens.append(_star_token(field, star))
        tokens_by_branch.append(tokens)

    columns = tuple(sorted({token for row in tokens_by_branch for token in row}))
    rows = tuple(
        tuple(Counter(tokens).get(column, 0) for column in columns)
        for tokens in tokens_by_branch
    )
    return columns, rows


def _rotate_index(rows: tuple[tuple[int, ...], ...], offset: int) -> tuple[tuple[int, ...], ...]:
    offset %= 12
    return tuple(rows[(target - offset) % 12] for target in range(12))


def _permutation_matrix(offset: int) -> tuple[tuple[int, ...], ...]:
    offset %= 12
    return tuple(
        tuple(int(target == (source + offset) % 12) for source in range(12))
        for target in range(12)
    )


def _rotate_matrix(
    rows: tuple[tuple[int, ...], ...], offset: int
) -> tuple[tuple[int, ...], ...]:
    permutation = _permutation_matrix(offset)
    column_count = len(rows[0]) if rows else 0
    return tuple(
        tuple(
            sum(permutation[target][source] * rows[source][column] for source in range(12))
            for column in range(column_count)
        )
        for target in range(12)
    )


def _allowed_offsets(relation: Mapping[str, Any]) -> dict[str, list[int]]:
    constraints = relation["coordinate_model"]["constraints"]
    result: dict[str, list[int]] = {}
    for geometry, specification in constraints.items():
        if geometry == "FLANKING":
            result[geometry] = list(specification["required_delta_set"])
        elif "allowed_delta" in specification:
            result[geometry] = list(specification["allowed_delta"])
    expected = {
        "SAME_PALACE": [0],
        "OPPOSITION": [6],
        "TRINE_ASPECT": [4, 8],
        "FOUR_DIRECTIONS_VISIBILITY": [0, 4, 6, 8],
        "THREE_DIRECTIONS_SCOPE": [0, 4, 8],
        "FLANKING": [1, 11],
    }
    if result != expected:
        raise ValueError(f"coordinate contract changed: {result}")
    return result


def _validate_case(
    case: Mapping[str, Any], branch_order: tuple[str, ...]
) -> tuple[dict[str, Any], tuple[str, ...], tuple[tuple[int, ...], ...], dict[str, Mapping[str, Any]]]:
    case_id = case.get("case_id")
    chart = case.get("chart")
    if not isinstance(chart, Mapping):
        raise ValueError(f"{case_id}: chart object is missing")
    palaces = chart.get("palaces")
    if not isinstance(palaces, list) or len(palaces) != 12:
        raise ValueError(f"{case_id}: expected exactly twelve palace records")

    branches = [palace.get("branch") for palace in palaces]
    names = [palace.get("name") for palace in palaces]
    if len(set(branches)) != 12 or set(branches) != set(branch_order):
        raise ValueError(f"{case_id}: branch map is not a complete unique Z12 domain")
    if len(set(names)) != 12 or not all(isinstance(name, str) and name for name in names):
        raise ValueError(f"{case_id}: palace names are not twelve unique non-empty labels")
    by_branch = {palace["branch"]: palace for palace in palaces}

    anchor = case.get("target_anchor_verification", {})
    if (
        anchor.get("status") != "UNIQUE_ANCHOR_MATCH_RECONFIRMED"
        or anchor.get("matched") is not True
        or anchor.get("target_palace_identity_match") is not True
    ):
        raise ValueError(f"{case_id}: target anchor is not independently marked as reconfirmed")
    if case.get("full_source_chart_equivalence_verified") is not False:
        raise ValueError(f"{case_id}: source-equivalence limitation changed unexpectedly")
    target_label = str(case.get("target_palace", ""))
    expected_observed_label = target_label[:-1] if target_label.endswith("宫") else target_label
    observed_label = anchor.get("observed_target_palace")
    observed_branch = anchor.get("observed_target_branch")
    if observed_label != expected_observed_label:
        raise ValueError(f"{case_id}: target palace label does not match anchor metadata")
    target_matches = [
        palace for palace in palaces
        if palace.get("name") == observed_label and palace.get("branch") == observed_branch
    ]
    if len(target_matches) != 1:
        raise ValueError(f"{case_id}: target palace label/branch mapping is not unique")

    if any(key in case for key in ("temporal", "temporal_scopes")) or "temporal" in chart:
        raise ValueError(f"{case_id}: natal-only artifact unexpectedly contains temporal scopes")

    columns, rows = _occupancy_matrix(palaces, branch_order)
    star_objects = sum(len(palace[field]) for palace in palaces for field in STAR_FIELDS)
    if star_objects != 68 or len(columns) != 80:
        raise ValueError(f"{case_id}: pinned chart occupancy shape changed")
    return (
        {
            "case_id": case_id,
            "palace_records": len(palaces),
            "unique_branches": len(set(branches)),
            "unique_palace_names": len(set(names)),
            "target_anchor_reconfirmed": True,
            "full_source_chart_equivalence_verified": False,
            "star_objects": star_objects,
            "occupancy_columns": len(columns),
        },
        columns,
        rows,
        by_branch,
    )


def make_report() -> dict[str, Any]:
    artifact, relation, branch_order, expected_case_ids = _load_inputs()
    cases = artifact.get("cases")
    if not isinstance(cases, list) or tuple(case.get("case_id") for case in cases) != expected_case_ids:
        raise ValueError("artifact case IDs do not match the pinned materializer's exact eligible set")
    if artifact.get("summary", {}).get("full_chart_materialized") != 11:
        raise ValueError("artifact materialization count changed")

    boundaries = artifact.get("boundaries", {})
    for key in (
        "source_subject_identity_used",
        "expert_reasoning_used",
        "expert_conclusion_used",
        "outcome_used",
        "external_biography_used",
        "missing_source_input_backfilled",
        "non_unique_candidate_promoted",
        "canonical_rule_promoted",
        "empirical_probability_used",
        "full_source_chart_equivalence_verified",
        "method_scope_broadened",
    ):
        if boundaries.get(key) is not False:
            raise ValueError(f"artifact boundary changed: {key}")

    allowed_offsets = _allowed_offsets(relation)
    branch_to_index = {branch: index for index, branch in enumerate(branch_order)}
    case_results: list[dict[str, Any]] = []
    counts = {
        "charts": 0,
        "palace_records": 0,
        "star_objects": 0,
        "occupancy_cells": 0,
        "index_matrix_offset_checks": 0,
        "inverse_checks": 0,
        "composition_checks": 0,
        "input_array_order_invariance_checks": 0,
        "target_anchor_identity_checks": 0,
        "same_palace_geometry_checks": 0,
        "opposition_geometry_checks": 0,
        "trine_geometry_checks": 0,
        "four_directions_visibility_checks": 0,
        "three_directions_scope_checks": 0,
        "flanking_geometry_checks": 0,
    }

    for case in cases:
        case_result, columns, rows, by_branch = _validate_case(case, branch_order)
        case_id = case_result["case_id"]
        for offset in range(12):
            indexed = _rotate_index(rows, offset)
            matrix_view = _rotate_matrix(rows, offset)
            if indexed != matrix_view:
                raise ValueError(f"{case_id}: index/matrix mismatch at offset {offset}")
            if _rotate_index(indexed, -offset) != rows:
                raise ValueError(f"{case_id}: inverse mismatch at offset {offset}")
            counts["index_matrix_offset_checks"] += 1
            counts["inverse_checks"] += 1

        for first in range(12):
            for second in range(12):
                if _rotate_index(_rotate_index(rows, first), second) != _rotate_index(
                    rows, first + second
                ):
                    raise ValueError(f"{case_id}: composition mismatch at {first}, {second}")
                counts["composition_checks"] += 1

        reversed_columns, reversed_rows = _occupancy_matrix(
            list(reversed(case["chart"]["palaces"]),), branch_order
        )
        if columns != reversed_columns or rows != reversed_rows:
            raise ValueError(f"{case_id}: input array order changed branch-indexed view")
        counts["input_array_order_invariance_checks"] += 1
        counts["target_anchor_identity_checks"] += 1

        for subject in branch_order:
            subject_index = branch_to_index[subject]
            subject_palace = by_branch[subject]
            for geometry, offsets in allowed_offsets.items():
                target_branches = [branch_order[(subject_index + delta) % 12] for delta in offsets]
                if geometry == "FLANKING" and (
                    offsets != [1, 11] or len(set(target_branches)) != 2
                ):
                    raise ValueError("FLANKING must preserve both neighboring branches")
                for target_branch, delta in zip(target_branches, offsets):
                    target_palace = by_branch[target_branch]
                    actual_delta = (
                        branch_to_index[target_palace["branch"]]
                        - branch_to_index[subject_palace["branch"]]
                    ) % 12
                    if actual_delta != delta:
                        raise ValueError(
                            f"{case_id}: {geometry} delta mismatch {subject}->{target_branch}"
                        )
                    if geometry == "SAME_PALACE" and target_palace is not subject_palace:
                        raise ValueError(f"{case_id}: SAME_PALACE did not preserve palace identity")
                count_key = {
                    "SAME_PALACE": "same_palace_geometry_checks",
                    "OPPOSITION": "opposition_geometry_checks",
                    "TRINE_ASPECT": "trine_geometry_checks",
                    "FOUR_DIRECTIONS_VISIBILITY": "four_directions_visibility_checks",
                    "THREE_DIRECTIONS_SCOPE": "three_directions_scope_checks",
                    "FLANKING": "flanking_geometry_checks",
                }[geometry]
                counts[count_key] += 1

        counts["charts"] += 1
        counts["palace_records"] += case_result["palace_records"]
        counts["star_objects"] += case_result["star_objects"]
        counts["occupancy_cells"] += 12 * len(columns)
        case_result.update(
            {
                "index_matrix_offset_checks": 12,
                "inverse_checks": 12,
                "composition_checks": 144,
                "input_array_order_invariant": True,
            }
        )
        case_results.append(case_result)

    expected_counts = {
        "charts": 11,
        "palace_records": 132,
        "star_objects": 748,
        "occupancy_cells": 10560,
        "index_matrix_offset_checks": 132,
        "inverse_checks": 132,
        "composition_checks": 1584,
        "input_array_order_invariance_checks": 11,
        "target_anchor_identity_checks": 11,
        "same_palace_geometry_checks": 132,
        "opposition_geometry_checks": 132,
        "trine_geometry_checks": 132,
        "four_directions_visibility_checks": 132,
        "three_directions_scope_checks": 132,
        "flanking_geometry_checks": 132,
    }
    if counts != expected_counts:
        raise ValueError(f"unexpected audit counts: {counts}")

    return {
        "schema_version": "0.2",
        "status": "TEST_ONLY_NOT_CANONICAL",
        "experiment_id": "PRODUCT_SPATIOTEMPORAL_NATAL_COORDINATE_PROBE_V0_2",
        "input_pins": [dict(PINNED_FILES[key]) for key in PIN_ORDER],
        "fixture_summary": {
            "artifact_id": artifact["artifact_id"],
            "materialization_level": artifact["materialization_level"],
            "source_cases_total": artifact["summary"]["source_cases_total"],
            "full_chart_materialized": artifact["summary"]["full_chart_materialized"],
            "not_materialized": artifact["summary"]["not_materialized"],
            "charts_checked": counts["charts"],
            "palaces_per_chart": 12,
            "target_anchor_reconfirmed": 11,
            "full_source_chart_equivalence_verified": 0,
            "temporal_scopes_present": False,
        },
        "coordinate_contract": {
            "model_id": relation["coordinate_model"]["id"],
            "branch_order": list(branch_order),
            "delta_formula": relation["coordinate_model"]["delta_formula"],
            "allowed_offsets": allowed_offsets,
        },
        "checks": {
            "input_hashes_match": True,
            "case_ids_match": True,
            "all_cases_have_12_unique_branches": True,
            "all_cases_have_12_unique_palace_names": True,
            "target_anchor_identities_reconfirmed": True,
            "full_source_chart_equivalence_claimed": False,
            "temporal_scopes_present": False,
            "input_array_order_invariant": True,
            "all_offsets_index_matrix_equivalent": True,
            "all_offsets_invertible": True,
            "all_compositions_match_mod_12": True,
            "z12_geometry_offsets_match_contract": True,
            "canonical_accepted": False,
            "runtime_effect_allowed": False,
        },
        "counts": counts,
        "case_results": case_results,
        "decision": (
            "KEEP_INDEX_BASELINE; index and permutation-matrix views agree under the declared "
            "Z12 coordinate encoding on this pinned engine-materialized natal fixture set; "
            "no production migration benefit is demonstrated."
        ),
        "not_evaluated": [
            "full source-chart equivalence",
            "six-layer PL1 temporal snapshot mapping",
            "cross-layer traditional reaction semantics",
            "runtime performance advantage",
            "predictive validity or probability calibration",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="write TEST_ONLY comparison JSON")
    args = parser.parse_args()
    rendered = json.dumps(make_report(), ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()

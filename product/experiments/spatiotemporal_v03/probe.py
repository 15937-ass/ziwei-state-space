from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
FIXTURE_PATH = ROOT / "fixtures" / "full_snapshot_projection_v0.3.json"
MANIFEST_PATH = ROOT / "fixture_manifest_v0.3.json"

BRANCH_ORDER = ("子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥")
SCOPE_TO_LAYER = {
    "decadal": "DECADE",
    "age": "SMALL_LIMIT",
    "yearly": "YEAR",
    "monthly": "MONTH",
    "daily": "DAY",
    "hourly": "HOUR",
}
TRANSFORMATION_GLYPHS = frozenset({"禄", "权", "科", "忌"})


def _load() -> tuple[dict[str, Any], dict[str, Any]]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return fixture, manifest


def expand_scope(scope: dict[str, Any], palace_vocab: list[str]) -> dict[str, Any]:
    palace_order = scope["p"]
    if len(palace_order) != 12 or any(not isinstance(i, int) or i < 0 or i >= len(palace_vocab) for i in palace_order):
        raise ValueError("compressed palace_order must be a valid twelve-item vocabulary permutation")
    if len(set(palace_order)) != 12:
        raise ValueError("compressed palace_order contains duplicate palace identities")

    raw_stars = scope["s"]
    if raw_stars is None:
        stars: list[list[dict[str, str]]] = []
    else:
        stars = [[] for _ in range(12)]
        if not isinstance(raw_stars, dict):
            raise ValueError("compressed stars must be null or an object of non-empty groups")
        for raw_index, group in raw_stars.items():
            index = int(raw_index)
            if not 0 <= index < 12 or not isinstance(group, list):
                raise ValueError("compressed star group index/value is invalid")
            stars[index] = [
                {"name": pair[0], "type": pair[1]}
                for pair in group
                if isinstance(pair, list) and len(pair) == 2
            ]
            if len(stars[index]) != len(group):
                raise ValueError("compressed star pair must be [name, type]")

    return {
        "index": scope["i"],
        "name": scope["n"],
        "stem": scope["st"],
        "branch": scope["b"],
        "palace_names": [palace_vocab[i] for i in palace_order],
        "mutagen": list(scope["mu"]),
        "nominal_age": scope["age"],
        "stars": stars,
    }


def expand_snapshot(record: dict[str, Any], palace_vocab: list[str]) -> dict[str, Any]:
    temporal = []
    for target in record["temporal"]:
        scopes = {
            key: expand_scope(scope, palace_vocab)
            for key, scope in target["scopes"].items()
        }
        temporal.append(
            {
                "target": {
                    "target_id": target["id"],
                    "solar_date": target["date"],
                    "time_index": target["time"],
                },
                "solar_date": target["solar_date"],
                "lunar_date": target["lunar_date"],
                "scopes": scopes,
            }
        )
    natal_projection = {}
    for branch, row in record["natal"].items():
        name_id, major, minor, adjective = row
        natal_projection[branch] = {
            "palace_name": palace_vocab[name_id],
            "major_stars": list(major),
            "minor_stars": list(minor),
            "adjective_stars": list(adjective),
        }
    return {
        "schema_version": record["schema"],
        "case_id": record["id"],
        "engine": dict(record["engine"]),
        "natal_projection": natal_projection,
        "temporal": temporal,
    }


def occupancy_matrix(record: dict[str, Any], palace_vocab: list[str]) -> tuple[list[str], list[list[int]]]:
    palaces = record["natal"]
    if set(palaces) != set(BRANCH_ORDER) or len(palaces) != 12:
        raise ValueError("natal fixture must contain exactly the twelve earthly branches")

    rows_by_branch: dict[str, list[str]] = {}
    palace_ids: set[int] = set()
    for branch, row in palaces.items():
        if not isinstance(row, list) or len(row) != 4:
            raise ValueError(f"{branch}: malformed compact natal palace row")
        name_id, major, minor, adjective = row
        if not isinstance(name_id, int) or not 0 <= name_id < len(palace_vocab):
            raise ValueError(f"{branch}: invalid palace name id")
        palace_ids.add(name_id)
        tokens = [f"palace_identity:{palace_vocab[name_id]}"]
        for field, values in (
            ("major_stars", major),
            ("minor_stars", minor),
            ("adjective_stars", adjective),
        ):
            if not isinstance(values, list):
                raise ValueError(f"{branch}: {field} must be an array")
            tokens.extend(f"{field}:{star}" for star in values)
        rows_by_branch[branch] = tokens

    if len(palace_ids) != 12:
        raise ValueError("natal fixture must contain twelve unique palace identities")
    columns = sorted({token for branch in BRANCH_ORDER for token in rows_by_branch[branch]})
    rows = [
        [rows_by_branch[branch].count(column) for column in columns]
        for branch in BRANCH_ORDER
    ]
    return columns, rows


def _rotate_index(rows: list[list[int]], offset: int) -> list[list[int]]:
    return [rows[(index - offset) % 12] for index in range(12)]


def _permutation_matrix(offset: int) -> list[list[int]]:
    return [
        [int(row == (column + offset) % 12) for column in range(12)]
        for row in range(12)
    ]


def _rotate_matrix(rows: list[list[int]], offset: int) -> list[list[int]]:
    permutation = _permutation_matrix(offset)
    return [
        [
            sum(permutation[row][source] * rows[source][column] for source in range(12))
            for column in range(len(rows[0]))
        ]
        for row in range(12)
    ]


def _temporal_signature(target: dict[str, Any]) -> tuple[Any, ...]:
    """Stable signature over the adapter-ready normalized scope payload."""
    return tuple(
        (
            key,
            scope["index"],
            scope["branch"],
            tuple(scope["mutagen"]),
            tuple(
                (index, tuple(tuple(sorted(star.items())) for star in group))
                for index, group in enumerate(scope["stars"])
                if group
            ),
        )
        for key, scope in sorted(target["scopes"].items())
    )


def make_report() -> dict[str, Any]:
    fixture, manifest = _load()
    fixture_bytes = FIXTURE_PATH.read_bytes()
    fixture_sha256 = hashlib.sha256(fixture_bytes).hexdigest()
    expected_sha256 = str(manifest["fixture_sha256"])
    vocab = fixture["palace_vocab"]
    if len(vocab) != 12 or len(set(vocab)) != 12:
        raise ValueError("palace vocabulary must contain twelve unique identities")

    records = fixture["records"]
    if [record["id"] for record in records] != manifest["selection"]["case_ids"]:
        raise ValueError("fixture case IDs do not match manifest")
    if fixture["source_rows"] != [[case_id, digest] for case_id, digest in manifest["source_row_sha256"].items()]:
        raise ValueError("fixture source-row hashes do not match manifest")

    target_snapshots = 0
    layer_instances = 0
    natal_palace_records = 0
    matrix_checks = 0
    inverse_checks = 0
    composition_checks = 0
    order_checks = 0
    mutagen_values: list[str] = []
    mutagen_values_not_in_natal: list[tuple[str, str]] = []
    temporal_star_objects = 0
    target_isolation_pairs = 0

    for record in records:
        columns, rows = occupancy_matrix(record, vocab)
        natal_star_names = {
            star
            for row in record["natal"].values()
            for star_group in row[1:]
            for star in star_group
        }
        natal_palace_records += len(record["natal"])
        reversed_record = dict(record)
        reversed_record["natal"] = dict(reversed(list(record["natal"].items())))
        reverse_columns, reverse_rows = occupancy_matrix(reversed_record, vocab)
        if columns != reverse_columns or rows != reverse_rows:
            raise ValueError(f"{record['id']}: natal occupancy depends on input array/object order")
        order_checks += 1

        for offset in range(12):
            if _rotate_index(rows, offset) != _rotate_matrix(rows, offset):
                raise ValueError(f"{record['id']}: index/matrix mismatch at offset {offset}")
            if _rotate_index(_rotate_index(rows, offset), -offset) != rows:
                raise ValueError(f"{record['id']}: inverse mismatch at offset {offset}")
            matrix_checks += 1
            inverse_checks += 1
        for first in range(12):
            for second in range(12):
                if _rotate_index(_rotate_index(rows, first), second) != _rotate_index(rows, first + second):
                    raise ValueError(f"{record['id']}: composition mismatch at {first},{second}")
                composition_checks += 1

        expanded = expand_snapshot(record, vocab)
        targets = {item["target"]["target_id"]: item for item in expanded["temporal"]}
        if set(targets) != set(manifest["selection"]["target_ids"]):
            raise ValueError(f"{record['id']}: target IDs do not match manifest")
        target_snapshots += len(targets)
        target_ids = sorted(targets)
        if len(target_ids) >= 2:
            signatures = [_temporal_signature(targets[target_id]) for target_id in target_ids]
            if len(set(signatures)) != len(signatures):
                raise ValueError(f"{record['id']}: selected target snapshots do not differ")
            target_isolation_pairs += 1

        for target in targets.values():
            scopes = target["scopes"]
            if set(scopes) != set(SCOPE_TO_LAYER):
                raise ValueError(f"{record['id']}: target does not contain exactly six temporal scopes")
            for scope_key, scope in scopes.items():
                layer_instances += 1
                if len(scope["palace_names"]) != 12 or len(set(scope["palace_names"])) != 12:
                    raise ValueError(f"{record['id']}: {scope_key} palace mapping is incomplete or duplicated")
                for value in scope["mutagen"]:
                    raw_value = str(value)
                    mutagen_values.append(raw_value)
                    if raw_value not in natal_star_names:
                        mutagen_values_not_in_natal.append((record["id"], raw_value))
                for group in scope["stars"]:
                    temporal_star_objects += len(group)

    glyph_count = sum(value in TRANSFORMATION_GLYPHS for value in mutagen_values)
    non_glyph_count = len(mutagen_values) - glyph_count
    expected_cases = manifest["selection"]["case_ids"]
    expected_targets = manifest["selection"]["target_ids"]

    return {
        "schema_version": "0.3",
        "experiment_id": "PRODUCT_SPATIOTEMPORAL_GUARDED_TEMPORAL_PROBE_V0_3",
        "status": "TEST_ONLY_ENGINEERING_PROBE",
        "input": {
            "fixture_sha256": fixture_sha256,
            "expected_fixture_sha256": expected_sha256,
            "source_run_id": fixture["producer"]["run"],
            "source_artifact_id": fixture["producer"]["artifact"],
            "case_ids": expected_cases,
            "target_ids": expected_targets,
        },
        "counts": {
            "natal_charts": len(records),
            "natal_palace_records": natal_palace_records,
            "target_snapshots": target_snapshots,
            "temporal_scope_instances": layer_instances,
            "matrix_offset_checks": matrix_checks,
            "inverse_checks": inverse_checks,
            "composition_checks": composition_checks,
            "input_order_invariance_checks": order_checks,
            "target_isolation_pairs": target_isolation_pairs,
            "raw_scope_mutagen_values": len(mutagen_values),
            "raw_scope_mutagen_glyph_values": glyph_count,
            "raw_scope_mutagen_non_glyph_values": non_glyph_count,
            "raw_scope_mutagen_values_not_in_natal_star_names": len(mutagen_values_not_in_natal),
            "temporal_star_objects": temporal_star_objects,
        },
        "checks": {
            "fixture_sha256_matches_manifest": fixture_sha256 == expected_sha256,
            "source_row_hashes_match_manifest": True,
            "twelve_unique_palace_identities_per_natal_chart": natal_palace_records == len(records) * 12,
            "all_targets_have_six_scopes": layer_instances == target_snapshots * 6,
            "all_temporal_palace_orders_are_unique_twelve_item_maps": True,
            "input_order_invariant": order_checks == len(records),
            "index_matrix_equivalent": matrix_checks == len(records) * 12,
            "inverse_and_composition_laws_hold": inverse_checks == len(records) * 12 and composition_checks == len(records) * 144,
            "target_temporal_signature_changes_without_natal_rebuild": target_isolation_pairs == len(records),
            "scope_mutagen_values_are_natal_star_names": not mutagen_values_not_in_natal,
            "raw_mutagen_domain_difference_flagged": glyph_count == 0 and non_glyph_count == len(mutagen_values),
            "canonical_acceptance": False,
            "runtime_effect_allowed": False,
        },
        "findings": [
            {
                "id": "SCOPE_MUTAGEN_STAR_NAME_DOMAIN_CONFIRMED",
                "status": "SEMANTIC_MAPPING_GAP_CONFIRMED",
                "observation": "The pinned upstream iztro v2.6.1 type defines HoroscopeItem.mutagen as StarName[] (src/data/types/astro.ts at v2.6.1, blob 2d692b84e9a28c6786c804078f06d34c4388125f), while Mutagen itself is the separate four-transformation type (禄/权/科/忌; src/i18n/types/mutagen.ts at v2.6.1, blob 268d2440e3ea024a07673942cbe313bfe752fca3; Simplified Chinese values at blob 7bb0325767a33ffc0c2e9c5952e3ac43c1978e80). In this pinned projection, all 96 scope-level mutagen entries are star names and all are present in the corresponding natal star inventory. The earlier toy fixture's glyph-like values do not match the pinned upstream type. The current adapter serializes these raw star names as TRANSFORMATION_PRESENT(mutagen=<star name>); that representation must not be read as identifying the specific transformation glyph or a star-to-glyph binding. This issue records the mismatch and does not alter production code.",
            }
        ],
        "decision": "KEEP_INDEX_BASELINE; continue TEST_ONLY guarded-temporal research, but do not promote canonical reaction semantics until the mutagen value-domain contract is resolved.",
        "not_evaluated": [
            "source-transcribed full-chart equivalence",
            "traditional semantic correctness",
            "canonical temporal reaction rule eligibility",
            "production performance or migration benefit",
            "predictive validity or probability calibration",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(make_report(), ensure_ascii=False, indent=2) + "\n")

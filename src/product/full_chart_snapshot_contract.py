"""Structural contract for PL1 normalized full-chart snapshots, schema v0.2.

Validation is deliberately non-semantic: it checks the payload consumed by the
Career Product API and never repairs, normalizes, or guesses missing facts.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from typing import Any, Mapping

from .temporal_asset_adapter import REQUIRED_SCOPE_KEYS, SCOPE_TO_LAYER


FULL_CHART_SCHEMA_VERSION = "0.2"
REQUIRED_ENGINE_FIELDS = ("name", "version", "source_revision", "adapter_version")
REQUIRED_NATAL_PALACE_FIELDS = (
    "name",
    "stem",
    "branch",
    "is_body_palace",
    "major_stars",
    "minor_stars",
    "adjective_stars",
)
REQUIRED_NATAL_STAR_FIELDS = ("name", "type", "brightness", "mutagen", "scope")
REQUIRED_TEMPORAL_STAR_FIELDS = ("name", "type")
REQUIRED_YEARLY_DEC_STAR_FIELDS = ("suiqian12", "jiangqian12")
EARTHLY_BRANCHES = frozenset("子丑寅卯辰巳午未申酉戌亥")
ISO_DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


@dataclass(frozen=True)
class FullChartSnapshotValidation:
    """Deterministic structural validation result for one full-chart snapshot."""

    ok: bool
    errors: tuple[str, ...] = ()


def _non_empty_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _valid_iso_date(value: Any) -> bool:
    if not isinstance(value, str) or not ISO_DATE_PATTERN.fullmatch(value):
        return False
    try:
        return date.fromisoformat(value).isoformat() == value
    except ValueError:
        return False


def _validate_star_array(
    value: Any,
    *,
    path: str,
    required_fields: tuple[str, ...],
    errors: list[str],
) -> None:
    if not isinstance(value, list):
        errors.append(f"{path} must be an array")
        return
    for index, star in enumerate(value):
        star_path = f"{path}[{index}]"
        if not isinstance(star, Mapping):
            errors.append(f"{star_path} must be an object")
            continue
        for field in required_fields:
            if field not in star:
                errors.append(f"{star_path} missing field: {field}")
        if "name" in star and not _non_empty_text(star["name"]):
            errors.append(f"{star_path}.name must be a non-empty string")
        for field in required_fields:
            if field != "name" and field in star and star[field] is not None and not isinstance(
                star[field], str
            ):
                errors.append(
                    f"{star_path}.{field} must be a string or null"
                )


def _validate_natal(snapshot: Mapping[str, Any], errors: list[str]) -> None:
    natal = snapshot.get("natal")
    if not isinstance(natal, Mapping):
        errors.append("natal must be an object")
        return

    if "solar_date" in natal and not _valid_iso_date(natal["solar_date"]):
        errors.append("natal.solar_date must be a valid YYYY-MM-DD date")
    for field in (
        "lunar_date",
        "chinese_date",
        "time",
        "time_range",
        "soul_star",
        "body_star",
        "five_elements_class",
        "soul_palace_branch",
        "body_palace_branch",
    ):
        if field in natal and natal[field] is not None and not isinstance(
            natal[field], str
        ):
            errors.append(f"natal.{field} must be a string or null")

    palaces = natal.get("palaces")
    if not isinstance(palaces, Mapping):
        errors.append("natal.palaces must be an object keyed by earthly branch")
        return

    actual_branches = {str(key) for key in palaces}
    missing_branches = sorted(EARTHLY_BRANCHES - actual_branches)
    unsupported_branches = sorted(actual_branches - EARTHLY_BRANCHES)
    if missing_branches or unsupported_branches or len(palaces) != 12:
        details = []
        if missing_branches:
            details.append("missing=" + ",".join(missing_branches))
        if unsupported_branches:
            details.append("unsupported=" + ",".join(unsupported_branches))
        if len(palaces) != 12:
            details.append(f"count={len(palaces)}")
        errors.append(
            "natal.palaces must map exactly the 12 earthly branches"
            + (": " + "; ".join(details) if details else "")
        )

    seen_names: dict[str, str] = {}
    for branch_key in sorted(palaces, key=lambda item: str(item)):
        palace = palaces[branch_key]
        path = f"natal.palaces.{branch_key}"
        if not isinstance(palace, Mapping):
            errors.append(f"{path} must be an object")
            continue

        for field in REQUIRED_NATAL_PALACE_FIELDS:
            if field not in palace:
                errors.append(f"{path} missing field: {field}")

        for field in ("name", "stem", "branch"):
            if field in palace and not _non_empty_text(palace[field]):
                errors.append(f"{path}.{field} must be a non-empty string")

        if "branch" in palace and palace["branch"] != branch_key:
            errors.append(f"{path}.branch must equal its mapping key")
        if "is_body_palace" in palace and not isinstance(
            palace["is_body_palace"], bool
        ):
            errors.append(f"{path}.is_body_palace must be a boolean")

        name = palace.get("name")
        if _non_empty_text(name):
            if name in seen_names:
                errors.append(
                    f"{path}.name duplicates {seen_names[name]}: {name}"
                )
            else:
                seen_names[name] = path

        for field in ("major_stars", "minor_stars", "adjective_stars"):
            if field in palace:
                _validate_star_array(
                    palace[field],
                    path=f"{path}.{field}",
                    required_fields=REQUIRED_NATAL_STAR_FIELDS,
                    errors=errors,
                )

        decadal = palace.get("decadal")
        if decadal is not None:
            if not isinstance(decadal, Mapping):
                errors.append(f"{path}.decadal must be an object or null")
            else:
                for field in ("range", "stem", "branch"):
                    if field not in decadal:
                        errors.append(f"{path}.decadal missing field: {field}")
                for field in ("stem", "branch"):
                    if field in decadal and not _non_empty_text(decadal[field]):
                        errors.append(
                            f"{path}.decadal.{field} must be a non-empty string"
                        )
                if (
                    "branch" in decadal
                    and _non_empty_text(decadal["branch"])
                    and decadal["branch"] not in EARTHLY_BRANCHES
                ):
                    errors.append(
                        f"{path}.decadal.branch must be an earthly branch"
                    )


def _validate_scope(path: str, scope: Any, errors: list[str]) -> None:
    if not isinstance(scope, Mapping):
        errors.append(f"{path} must be an object")
        return

    missing = [field for field in REQUIRED_SCOPE_KEYS if field not in scope]
    for field in missing:
        errors.append(f"{path} missing field: {field}")
    extra_fields = sorted(str(field) for field in scope if field not in REQUIRED_SCOPE_KEYS)
    if extra_fields:
        errors.append(
            f"{path} contains unsupported field(s): " + ", ".join(extra_fields)
        )

    if "index" in scope and (
        isinstance(scope["index"], bool) or not isinstance(scope["index"], int)
    ):
        errors.append(f"{path}.index must be an integer")
    for field in ("name", "stem", "branch"):
        if field in scope and not _non_empty_text(scope[field]):
            errors.append(f"{path}.{field} must be a non-empty string")
    if "nominal_age" in scope and scope["nominal_age"] is not None and (
        isinstance(scope["nominal_age"], bool)
        or not isinstance(scope["nominal_age"], int)
    ):
        errors.append(f"{path}.nominal_age must be an integer or null")

    palace_names = scope.get("palace_names")
    if "palace_names" in scope:
        if not isinstance(palace_names, list):
            errors.append(f"{path}.palace_names must be an array")
        else:
            if not palace_names:
                errors.append(f"{path}.palace_names must contain at least one item")
            for index, name in enumerate(palace_names):
                if not _non_empty_text(name):
                    errors.append(
                        f"{path}.palace_names[{index}] must be a non-empty string"
                    )

    mutagen = scope.get("mutagen")
    if "mutagen" in scope:
        if not isinstance(mutagen, list):
            errors.append(f"{path}.mutagen must be an array")
        else:
            for index, value in enumerate(mutagen):
                if not _non_empty_text(value):
                    errors.append(
                        f"{path}.mutagen[{index}] must be a non-empty string"
                    )

    stars = scope.get("stars")
    if "stars" in scope:
        if not isinstance(stars, list):
            errors.append(f"{path}.stars must be an array of arrays")
        else:
            if isinstance(palace_names, list) and len(stars) != len(palace_names):
                errors.append(
                    f"{path}.stars group count must equal palace_names length"
                )
            for group_index, group in enumerate(stars):
                group_path = f"{path}.stars[{group_index}]"
                _validate_star_array(
                    group,
                    path=group_path,
                    required_fields=REQUIRED_TEMPORAL_STAR_FIELDS,
                    errors=errors,
                )


def _validate_temporal(
    snapshot: Mapping[str, Any],
    selected_target_id: Any,
    errors: list[str],
) -> None:
    temporal = snapshot.get("temporal")
    if not isinstance(temporal, list):
        errors.append("temporal must be an array")
        return
    if not temporal:
        errors.append("temporal must contain at least one target")
        return

    if not _non_empty_text(selected_target_id):
        errors.append("target_id must be a non-empty string")

    if _non_empty_text(selected_target_id) and selected_target_id != selected_target_id.strip():
        errors.append("target_id must not contain surrounding whitespace")

    seen_ids: set[str] = set()
    for index, item in enumerate(temporal):
        path = f"temporal[{index}]"
        if not isinstance(item, Mapping):
            errors.append(f"{path} must be an object")
            continue

        target = item.get("target")
        if not isinstance(target, Mapping):
            errors.append(f"{path}.target must be an object")
            target = {}

        target_id = target.get("target_id")
        if not _non_empty_text(target_id):
            errors.append(f"{path}.target.target_id must be a non-empty string")
        else:
            if target_id != target_id.strip():
                errors.append(f"{path}.target.target_id must not contain surrounding whitespace")
            if target_id in seen_ids:
                errors.append(f"duplicate temporal target_id: {target_id}")
            seen_ids.add(target_id)

        target_date = target.get("solar_date")
        if not _valid_iso_date(target_date):
            errors.append(f"{path}.target.solar_date must be a valid YYYY-MM-DD date")

        time_index = target.get("time_index")
        if isinstance(time_index, bool) or not isinstance(time_index, int):
            errors.append(f"{path}.target.time_index must be an integer")

        solar_date = item.get("solar_date")
        if not _valid_iso_date(solar_date):
            errors.append(f"{path}.solar_date must be a valid YYYY-MM-DD date")
        elif _valid_iso_date(target_date) and solar_date != target_date:
            errors.append(f"{path}.solar_date must equal {path}.target.solar_date")

        if not _non_empty_text(item.get("lunar_date")):
            errors.append(f"{path}.lunar_date must be a non-empty string")

        scopes = item.get("scopes")
        if not isinstance(scopes, Mapping):
            errors.append(f"{path}.scopes must be an object")
            continue

        missing_scopes = [key for key in SCOPE_TO_LAYER if key not in scopes]
        for scope_key in missing_scopes:
            errors.append(f"{path}.scopes missing required scope: {scope_key}")
        extra_scopes = sorted(str(key) for key in scopes if key not in SCOPE_TO_LAYER)
        if extra_scopes:
            errors.append(
                f"{path}.scopes contains unsupported scope(s): "
                + ", ".join(extra_scopes)
            )
        for scope_key in SCOPE_TO_LAYER:
            if scope_key in scopes:
                _validate_scope(f"{path}.scopes.{scope_key}", scopes[scope_key], errors)

        yearly_dec = item.get("yearly_dec_stars")
        if yearly_dec is not None:
            if not isinstance(yearly_dec, Mapping):
                errors.append(f"{path}.yearly_dec_stars must be an object or null")
            else:
                extra_fields = sorted(
                    str(field)
                    for field in yearly_dec
                    if field not in REQUIRED_YEARLY_DEC_STAR_FIELDS
                )
                if extra_fields:
                    errors.append(
                        f"{path}.yearly_dec_stars contains unsupported field(s): "
                        + ", ".join(extra_fields)
                    )
                for field in REQUIRED_YEARLY_DEC_STAR_FIELDS:
                    if field not in yearly_dec:
                        errors.append(
                            f"{path}.yearly_dec_stars missing field: {field}"
                        )
                    elif not isinstance(yearly_dec[field], list):
                        errors.append(
                            f"{path}.yearly_dec_stars.{field} must be an array"
                        )
                    else:
                        for tag_index, tag in enumerate(yearly_dec[field]):
                            if not _non_empty_text(tag):
                                errors.append(
                                    f"{path}.yearly_dec_stars.{field}[{tag_index}] "
                                    "must be a non-empty string"
                                )

    if _non_empty_text(selected_target_id) and selected_target_id not in seen_ids:
        errors.append(
            f"selected target_id not found in normalized temporal snapshot: "
            f"{selected_target_id}"
        )


def validate_normalized_full_chart_snapshot(
    snapshot: Any,
    *,
    target_id: Any,
) -> FullChartSnapshotValidation:
    """Validate the PL1 full-exporter v0.2 contract without mutating the payload."""

    errors: list[str] = []
    if not isinstance(snapshot, Mapping):
        return FullChartSnapshotValidation(
            False,
            ("normalized full-chart snapshot must be an object",),
        )

    if "case_id" in snapshot and snapshot["case_id"] is not None and not isinstance(
        snapshot["case_id"], str
    ):
        errors.append("case_id must be a string or null")

    schema_version = snapshot.get("schema_version")
    if schema_version != FULL_CHART_SCHEMA_VERSION:
        errors.append(
            "schema_version must be '0.2' for the PL1 full-chart exporter"
        )

    engine = snapshot.get("engine")
    if not isinstance(engine, Mapping):
        errors.append("engine must be an object")
    else:
        for field in REQUIRED_ENGINE_FIELDS:
            if not _non_empty_text(engine.get(field)):
                errors.append(f"engine.{field} is required for provenance")

    if not isinstance(snapshot.get("input"), Mapping):
        errors.append("input must be an object")

    _validate_natal(snapshot, errors)
    _validate_temporal(snapshot, target_id, errors)

    return FullChartSnapshotValidation(not errors, tuple(errors))

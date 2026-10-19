"""Structural validator for the normalized PL1 full-chart snapshot v0.2.

This validates transport shape and provenance fields only. It does not infer
missing stars, repair scopes, or add astrological semantics.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any


SUPPORTED_SCHEMA_VERSION = "0.2"
REQUIRED_ENGINE_FIELDS = ("name", "version", "adapter_version")
REQUIRED_NATAL_PALACE_FIELDS = (
    "name",
    "stem",
    "branch",
    "is_body_palace",
    "major_stars",
    "minor_stars",
    "adjective_stars",
)
REQUIRED_SCOPE_FIELDS = (
    "index",
    "name",
    "stem",
    "branch",
    "palace_names",
    "mutagen",
    "nominal_age",
    "stars",
)
REQUIRED_SCOPE_KEYS = ("decadal", "age", "yearly", "monthly", "daily", "hourly")


def _is_array(value: Any) -> bool:
    return isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray))


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _validate_star_array(
    value: Any,
    *,
    field: str,
    errors: list[str],
    require_groups: bool = False,
) -> None:
    if not _is_array(value):
        errors.append(f"{field} must be an array")
        return
    for index, item in enumerate(value):
        item_path = f"{field}[{index}]"
        if require_groups:
            if not _is_array(item):
                errors.append(f"{item_path} must be an array")
                continue
            for star_index, star in enumerate(item):
                star_path = f"{item_path}[{star_index}]"
                if not isinstance(star, Mapping):
                    errors.append(f"{star_path} must be an object")
                elif not _text(star.get("name")):
                    errors.append(f"{star_path}.name is required")
        elif not isinstance(item, Mapping):
            errors.append(f"{item_path} must be an object")
        elif not _text(item.get("name")):
            errors.append(f"{item_path}.name is required")


def validate_normalized_inference_snapshot(
    snapshot: Mapping[str, Any],
    *,
    target_id: str,
) -> None:
    """Raise ValueError when a full PL1 v0.2 snapshot violates the inference contract."""

    if not isinstance(snapshot, Mapping):
        raise ValueError("normalized inference snapshot root must be an object")

    errors: list[str] = []
    if str(snapshot.get("schema_version", "")).strip() != SUPPORTED_SCHEMA_VERSION:
        errors.append(
            f"schema_version must be {SUPPORTED_SCHEMA_VERSION!r} for full-chart inference"
        )

    engine = snapshot.get("engine")
    if not isinstance(engine, Mapping):
        errors.append("engine must be an object")
    else:
        for key in REQUIRED_ENGINE_FIELDS:
            if not _text(engine.get(key)):
                errors.append(f"engine.{key} is required")

    if not isinstance(snapshot.get("input"), Mapping):
        errors.append("input must be an object")

    natal = snapshot.get("natal")
    if not isinstance(natal, Mapping):
        errors.append("natal must be an object")
    else:
        palaces = natal.get("palaces")
        if not isinstance(palaces, Mapping):
            errors.append("natal.palaces must be an object")
        else:
            if len(palaces) != 12:
                errors.append(f"natal.palaces must contain 12 palaces, got {len(palaces)}")
            for palace_key in sorted(palaces, key=str):
                palace = palaces[palace_key]
                path = f"natal.palaces[{palace_key!r}]"
                if not isinstance(palace, Mapping):
                    errors.append(f"{path} must be an object")
                    continue
                for key in REQUIRED_NATAL_PALACE_FIELDS:
                    if key not in palace:
                        errors.append(f"{path}.{key} is required")
                for key in ("name", "stem", "branch"):
                    if key in palace and not _text(palace.get(key)):
                        errors.append(f"{path}.{key} must be non-empty text")
                for key in ("major_stars", "minor_stars", "adjective_stars"):
                    if key in palace:
                        _validate_star_array(
                            palace.get(key),
                            field=f"{path}.{key}",
                            errors=errors,
                        )

    temporal = snapshot.get("temporal")
    if not _is_array(temporal) or not temporal:
        errors.append("temporal must be a non-empty array")
        temporal = ()

    normalized_target_id = str(target_id or "").strip()
    if not normalized_target_id:
        errors.append("target_id is required")

    targets: list[tuple[str, Mapping[str, Any]]] = []
    seen_target_ids: set[str] = set()
    for index, item in enumerate(temporal):
        path = f"temporal[{index}]"
        if not isinstance(item, Mapping):
            errors.append(f"{path} must be an object")
            continue
        target = item.get("target")
        if not isinstance(target, Mapping):
            errors.append(f"{path}.target must be an object")
            continue
        item_target_id = str(target.get("target_id", "")).strip()
        if not item_target_id:
            errors.append(f"{path}.target.target_id is required")
            continue
        if item_target_id in seen_target_ids:
            errors.append(f"target_id is not unique in normalized temporal snapshot: {item_target_id}")
        seen_target_ids.add(item_target_id)
        targets.append((item_target_id, item))

        if not _text(target.get("solar_date")):
            errors.append(f"{path}.target.solar_date is required")
        raw_time_index = target.get("time_index")
        if raw_time_index is not None and (
            isinstance(raw_time_index, bool) or not isinstance(raw_time_index, int)
        ):
            errors.append(f"{path}.target.time_index must be an integer or null")
        if not _text(item.get("solar_date")):
            errors.append(f"{path}.solar_date is required")
        if not _text(item.get("lunar_date")):
            errors.append(f"{path}.lunar_date is required")

    matching = [item for item_target_id, item in targets if item_target_id == normalized_target_id]
    if normalized_target_id and not matching:
        errors.append(
            f"target_id not found in normalized temporal snapshot: {normalized_target_id}"
        )
    if len(matching) > 1:
        errors.append(
            f"target_id is not unique in normalized temporal snapshot: {normalized_target_id}"
        )

    if matching:
        scopes = matching[0].get("scopes")
        if not isinstance(scopes, Mapping):
            errors.append("selected temporal target scopes must be an object")
        else:
            for scope_key in REQUIRED_SCOPE_KEYS:
                scope = scopes.get(scope_key)
                scope_path = f"selected temporal target scopes.{scope_key}"
                if not isinstance(scope, Mapping):
                    errors.append(f"{scope_path} must be an object")
                    continue
                for key in REQUIRED_SCOPE_FIELDS:
                    if key not in scope:
                        errors.append(f"{scope_path}.{key} is required")
                for key in ("name", "stem", "branch"):
                    if key in scope and not _text(scope.get(key)):
                        errors.append(f"{scope_path}.{key} must be non-empty text")
                if "index" in scope and (
                    isinstance(scope.get("index"), bool)
                    or not isinstance(scope.get("index"), int)
                ):
                    errors.append(f"{scope_path}.index must be an integer")
                if "nominal_age" in scope and scope.get("nominal_age") is not None and (
                    isinstance(scope.get("nominal_age"), bool)
                    or not isinstance(scope.get("nominal_age"), int)
                ):
                    errors.append(f"{scope_path}.nominal_age must be an integer or null")
                if "palace_names" in scope:
                    palace_names = scope.get("palace_names")
                    if not _is_array(palace_names):
                        errors.append(f"{scope_path}.palace_names must be an array")
                    elif any(not _text(name) for name in palace_names):
                        errors.append(f"{scope_path}.palace_names entries must be non-empty text")
                if "mutagen" in scope:
                    mutagen = scope.get("mutagen")
                    if not _is_array(mutagen):
                        errors.append(f"{scope_path}.mutagen must be an array")
                    elif any(not _text(value) for value in mutagen):
                        errors.append(f"{scope_path}.mutagen entries must be non-empty text")
                if "stars" in scope:
                    stars = scope.get("stars")
                    if not _is_array(stars):
                        errors.append(f"{scope_path}.stars must be an array")
                    else:
                        if "palace_names" in scope and _is_array(scope.get("palace_names")):
                            if len(stars) != len(scope["palace_names"]):
                                errors.append(
                                    f"{scope_path}.stars must align with palace_names length"
                                )
                        _validate_star_array(
                            stars,
                            field=f"{scope_path}.stars",
                            errors=errors,
                            require_groups=True,
                        )

        yearly_dec = matching[0].get("yearly_dec_stars")
        if yearly_dec is not None:
            if not isinstance(yearly_dec, Mapping):
                errors.append("selected temporal target yearly_dec_stars must be an object or null")
            else:
                for key in ("suiqian12", "jiangqian12"):
                    values = yearly_dec.get(key)
                    if not _is_array(values):
                        errors.append(
                            f"selected temporal target yearly_dec_stars.{key} must be an array"
                        )

    if errors:
        raise ValueError("normalized inference snapshot invalid: " + "; ".join(errors))

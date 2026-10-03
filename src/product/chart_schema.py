"""Validation helpers for product normalized chart snapshots."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Protocol


REQUIRED_TOP_LEVEL = ("schema_version", "engine", "input", "chart")
REQUIRED_PALACE_FIELDS = (
    "stem",
    "branch",
    "is_body_palace",
    "major_stars",
    "minor_stars",
    "adjective_stars",
)


class ChartAdapter(Protocol):
    """Minimal adapter interface for deterministic external/internal engines."""

    name: str
    version: str

    def render(self, birth_input: Mapping[str, Any]) -> Mapping[str, Any]:
        ...


@dataclass(frozen=True)
class SnapshotValidation:
    ok: bool
    errors: tuple[str, ...] = ()


def validate_normalized_chart(snapshot: Mapping[str, Any]) -> SnapshotValidation:
    errors: list[str] = []

    for key in REQUIRED_TOP_LEVEL:
        if key not in snapshot:
            errors.append(f"missing top-level field: {key}")

    if errors:
        return SnapshotValidation(False, tuple(errors))

    engine = snapshot["engine"]
    if not isinstance(engine, Mapping):
        errors.append("engine must be a mapping")
    else:
        for key in ("name", "version", "adapter_version"):
            if not engine.get(key):
                errors.append(f"engine.{key} is required")

    chart = snapshot["chart"]
    if not isinstance(chart, Mapping):
        errors.append("chart must be a mapping")
        return SnapshotValidation(False, tuple(errors))

    palaces = chart.get("palaces")
    if not isinstance(palaces, Mapping):
        errors.append("chart.palaces must be a mapping")
        return SnapshotValidation(False, tuple(errors))

    if len(palaces) != 12:
        errors.append(f"chart.palaces must contain 12 palaces, got {len(palaces)}")

    for palace_name, palace in palaces.items():
        if not isinstance(palace, Mapping):
            errors.append(f"palace {palace_name} must be a mapping")
            continue
        for field in REQUIRED_PALACE_FIELDS:
            if field not in palace:
                errors.append(f"palace {palace_name} missing field: {field}")

        for stars_field in ("major_stars", "minor_stars", "adjective_stars"):
            stars = palace.get(stars_field)
            if stars is not None and not isinstance(stars, list):
                errors.append(f"palace {palace_name}.{stars_field} must be a list")

    return SnapshotValidation(len(errors) == 0, tuple(errors))

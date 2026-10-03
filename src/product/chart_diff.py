"""Deterministic comparison of normalized Zi Wei chart snapshots.

This module is an engineering aid for cross-engine regression. Agreement
between engines is not treated as ground truth; mismatches are surfaced for
source/configuration resolution.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any, Iterable, Mapping, Sequence


_SET_LIKE_KEYS = frozenset(
    {
        "major_stars",
        "minor_stars",
        "adjective_stars",
        "transformations",
        "labels",
        "modifiers",
    }
)


@dataclass(frozen=True)
class ChartDifference:
    path: str
    left: Any
    right: Any
    category: str
    severity: str


def _stable_item(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _canonical_set_like(values: Sequence[Any]) -> tuple[str, ...]:
    return tuple(sorted(_stable_item(v) for v in values))


def _ignored(path: str, ignore_paths: tuple[str, ...]) -> bool:
    return any(path == prefix or path.startswith(prefix + ".") for prefix in ignore_paths)


def _category(path: str) -> str:
    if path.startswith("meta"):
        return "metadata"
    if "transformations" in path:
        return "transformations"
    if "stars" in path or "brightness" in path:
        return "stars"
    if path.startswith("limits") or "temporal" in path:
        return "temporal"
    if path.startswith("palaces"):
        return "chart_structure"
    return "other"


def _severity(path: str) -> str:
    critical_tokens = (
        ".major_stars",
        ".transformations",
        ".stem",
        ".branch",
        ".palace_id",
    )
    if any(token in path for token in critical_tokens):
        return "CRITICAL"
    if ".brightness" in path or path.startswith("limits"):
        return "HIGH"
    return "NORMAL"


def compare_chart_snapshots(
    left: Mapping[str, Any],
    right: Mapping[str, Any],
    *,
    ignore_paths: Iterable[str] = (),
) -> list[ChartDifference]:
    """Compare two normalized chart snapshots.

    Mapping order is ignored. Selected list-valued chart fields (stars,
    transformations, modifiers and labels) are treated as sets so engine
    serialization order does not create false mismatches. Other sequences
    remain order-sensitive.

    ignore_paths accepts exact paths or mapping-path prefixes.
    """

    ignored = tuple(ignore_paths)
    diffs: list[ChartDifference] = []

    def walk(a: Any, b: Any, path: str, key: str | None = None) -> None:
        if _ignored(path, ignored):
            return

        if isinstance(a, Mapping) and isinstance(b, Mapping):
            keys = sorted(set(a) | set(b))
            for child_key in keys:
                child_path = f"{path}.{child_key}" if path else str(child_key)
                if child_key not in a:
                    diffs.append(
                        ChartDifference(
                            child_path,
                            None,
                            b[child_key],
                            _category(child_path),
                            _severity(child_path),
                        )
                    )
                    continue
                if child_key not in b:
                    diffs.append(
                        ChartDifference(
                            child_path,
                            a[child_key],
                            None,
                            _category(child_path),
                            _severity(child_path),
                        )
                    )
                    continue
                walk(a[child_key], b[child_key], child_path, str(child_key))
            return

        if (
            isinstance(a, Sequence)
            and not isinstance(a, (str, bytes, bytearray))
            and isinstance(b, Sequence)
            and not isinstance(b, (str, bytes, bytearray))
        ):
            if key in _SET_LIKE_KEYS:
                ca = _canonical_set_like(a)
                cb = _canonical_set_like(b)
                if ca != cb:
                    diffs.append(
                        ChartDifference(path, ca, cb, _category(path), _severity(path))
                    )
                return

            if len(a) != len(b):
                diffs.append(
                    ChartDifference(
                        path + ".length",
                        len(a),
                        len(b),
                        _category(path),
                        _severity(path),
                    )
                )
            for index, (av, bv) in enumerate(zip(a, b)):
                walk(av, bv, f"{path}[{index}]", None)
            return

        if a != b:
            diffs.append(
                ChartDifference(path, a, b, _category(path), _severity(path))
            )

    walk(left, right, "")
    return diffs


def summarize_differences(differences: Sequence[ChartDifference]) -> dict[str, Any]:
    """Return a small machine-readable summary for CI/reporting."""

    counts = {"CRITICAL": 0, "HIGH": 0, "NORMAL": 0}
    categories: dict[str, int] = {}
    for diff in differences:
        counts[diff.severity] = counts.get(diff.severity, 0) + 1
        categories[diff.category] = categories.get(diff.category, 0) + 1

    return {
        "exact_match": len(differences) == 0,
        "total_differences": len(differences),
        "severity_counts": counts,
        "category_counts": dict(sorted(categories.items())),
    }

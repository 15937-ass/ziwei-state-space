"""Source-preserving discrete dignity lookup.

The table preserves printed categories such as 庙/旺/平/闲/陷 verbatim.
No numeric score, distance, or automatic valence is derived from them.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping


@dataclass(frozen=True)
class DignityEvidence:
    branch: str
    star: str
    category: str
    record_id: str
    source_id: str
    printed_page: str
    table_name: str


@dataclass(frozen=True)
class DignityTable:
    values: Mapping[tuple[str, str], DignityEvidence]

    def lookup(self, branch: str, star: str) -> DignityEvidence | None:
        return self.values.get((str(branch).strip(), str(star).strip()))

    def category(self, branch: str, star: str) -> str | None:
        item = self.lookup(branch, star)
        return item.category if item is not None else None

    def is_ru_miao(self, branch: str, star: str) -> bool:
        return self.category(branch, star) == "庙"


def _split(value: str) -> tuple[str, ...]:
    return tuple(part.strip() for part in str(value or "").split(";") if part.strip())


def load_dignity_table(path: str | Path) -> DignityTable:
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    values: dict[tuple[str, str], DignityEvidence] = {}
    for row in rows:
        if str(row.get("review_status", "")).strip() != "SOURCE_SPAN_VERIFIED":
            continue
        if str(row.get("source_span_verified", "")).strip().lower() != "true":
            continue
        if str(row.get("normalization_verified", "")).strip().lower() != "true":
            continue

        dimensions = _split(row.get("dimension_order", ""))
        vector = _split(row.get("source_vector", ""))
        if not dimensions or len(dimensions) != len(vector):
            # Rows such as branch_star_set are not dignity vectors.
            continue

        branch = str(row.get("palace_branch", "")).strip()
        if not branch:
            continue

        for star, category in zip(dimensions, vector):
            if category == "-":
                continue
            key = (branch, star)
            item = DignityEvidence(
                branch=branch,
                star=star,
                category=category,
                record_id=str(row.get("record_id", "")).strip(),
                source_id=str(row.get("source_id", "")).strip(),
                printed_page=str(row.get("printed_page", "")).strip(),
                table_name=str(row.get("table_name", "")).strip(),
            )
            previous = values.get(key)
            if previous is not None and previous.category != item.category:
                raise ValueError(
                    f"conflicting dignity category for {branch}/{star}: "
                    f"{previous.category!r} vs {item.category!r}"
                )
            values[key] = item

    if not values:
        raise ValueError("no verified dignity lookup values loaded")
    return DignityTable(values=dict(sorted(values.items())))

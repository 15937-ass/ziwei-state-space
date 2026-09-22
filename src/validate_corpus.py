"""Corpus validation utilities for Paper 1."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable, List, Mapping

REQUIRED_FIELDS = (
    "rule_id",
    "school",
    "source_work",
    "source_location",
    "subject_type",
    "subject",
    "context",
    "condition",
    "target_type",
    "target_literal",
    "target_normalized",
    "operator",
    "state_change",
    "valence",
    "epistemic_type_source",
    "evidence_text",
    "extraction_confidence",
    "status",
)


def read_csv(path: str | Path) -> List[Dict[str, str]]:
    with Path(path).open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def validate_required_fields(rows: Iterable[Mapping[str, str]]) -> Dict[str, int]:
    rows = list(rows)
    return {
        field: sum(1 for row in rows if not str(row.get(field, "")).strip())
        for field in REQUIRED_FIELDS
    }


def summarize_rules(rows: Iterable[Mapping[str, str]]) -> dict:
    rows = list(rows)
    return {
        "rule_count": len(rows),
        "by_star": dict(Counter(row["subject"] for row in rows)),
        "target_types": dict(Counter(row["target_type"] for row in rows)),
        "operators": dict(Counter(row["operator"] for row in rows)),
        "state_changes": dict(Counter(row["state_change"] for row in rows)),
        "valence": dict(Counter(row["valence"] for row in rows)),
        "required_field_missing": validate_required_fields(rows),
    }


def write_summary(paths: List[str], output: str) -> None:
    rows = []
    for path in paths:
        rows.extend(read_csv(path))
    Path(output).write_text(
        json.dumps(summarize_rules(rows), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

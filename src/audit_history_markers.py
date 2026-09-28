"""Heuristic scan for source text that may imply history-sensitive dynamics.

This scanner is deliberately conservative: it produces review candidates only.
It never converts a rule into a HistoryUpdate and never changes the executable
model.  Source-span review remains mandatory before any architecture migration.
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


MARKERS = {
    "EXPLICIT_FUTURE": re.compile(
        r"影响后运|后运受|后运.*影响|日后|以后.*(?:影响|形成|加深)|后来"
    ),
    "REINFORCE_DISPOSITION": re.compile(
        r"根深蒂固|加深.{0,6}(?:本质|怯懦|顽嚣|空虚|短志|浮荡)|"
        r"强化.{0,6}(?:本质|怯懦|顽嚣|空虚|短志|浮荡)|"
        r"形成.{0,8}(?:结构|本质|倾向|意志)"
    ),
    "STAGE_SEQUENCE": re.compile(
        r"早年.{0,20}(?:后|晚|后来)|先.{0,12}后|前期.{0,15}(?:后|以后)|"
        r"能否利用.{0,20}(?:后运|日后)"
    ),
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def scan(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for row in rows:
        text = " ".join(
            row.get(field, "")
            for field in ("condition", "target_literal", "target_normalized", "evidence_text", "notes")
        )
        hits = [name for name, pattern in MARKERS.items() if pattern.search(text)]
        if not hits:
            continue
        priority = (
            "P0_HISTORY_REVIEW"
            if {"EXPLICIT_FUTURE", "REINFORCE_DISPOSITION"} & set(hits)
            else "P1_SEQUENCE_REVIEW"
        )
        out.append(
            {
                "record_id": row.get("rule_id", ""),
                "source_location": row.get("source_location", ""),
                "marker_classes": "|".join(hits),
                "priority": priority,
                "condition": row.get("condition", ""),
                "target_literal": row.get("target_literal", ""),
                "evidence_text": row.get("evidence_text", ""),
                "review_status": "HEURISTIC_CANDIDATE",
            }
        )
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "catalog",
        nargs="?",
        default="knowledge/rules/systems/sixty_systems_canonical_v0.1.csv",
    )
    parser.add_argument("--output")
    args = parser.parse_args()

    rows = scan(read_csv(Path(args.catalog)))
    fields = [
        "record_id",
        "source_location",
        "marker_classes",
        "priority",
        "condition",
        "target_literal",
        "evidence_text",
        "review_status",
    ]

    if args.output:
        with Path(args.output).open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
    else:
        writer = csv.DictWriter(__import__("sys").stdout, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Emit deterministic PL2-E natal wealth JSON + Chinese report."""

from __future__ import annotations

import json
from pathlib import Path

from src.product.wealth_pilot import (
    build_wealth_structure_report,
    load_pilot_registry,
    load_projection_rows,
)
from src.product.wealth_semantics import (
    load_wealth_semantic_registry,
    render_wealth_structure_report,
)

ROOT = Path(__file__).resolve().parents[1]
W01 = ROOT / "validation/wp05/W01_wealth_projection_review_001_100.csv"
PILOT = ROOT / "product/PL2C_WEALTH_PILOT_v0.1.json"
SEMANTIC = ROOT / "product/PL2E_WEALTH_SEMANTIC_REGISTRY_v0.1.json"


def star(name: str, mutagen: str | None = None) -> dict:
    return {
        "name": name,
        "brightness": None,
        "mutagen": mutagen,
        "type": None,
        "scope": None,
    }


def sample_snapshot() -> dict:
    palaces = {}
    for i in range(11):
        palaces[f"示例宫{i}"] = {
            "stem": "甲",
            "branch": "子",
            "is_body_palace": False,
            "major_stars": [],
            "minor_stars": [],
            "adjective_stars": [],
        }
    palaces["财帛"] = {
        "stem": "乙",
        "branch": "丑",
        "is_body_palace": False,
        "major_stars": [
            star("武曲", "禄"),
            star("紫微", "科"),
            star("擎羊"),
        ],
        "minor_stars": [],
        "adjective_stars": [],
    }
    return {
        "schema_version": "0.1",
        "engine": {
            "name": "pl2e-synthetic",
            "version": "0.1",
            "adapter_version": "0.1",
        },
        "input": {"solar_date": "2000-01-01"},
        "chart": {"palaces": palaces},
    }


def main() -> None:
    rows = load_projection_rows(W01)
    pilot = load_pilot_registry(PILOT)
    semantic = load_wealth_semantic_registry(SEMANTIC)
    report = build_wealth_structure_report(
        sample_snapshot(),
        rows,
        pilot,
        semantic,
        question="PL2-E 本命财帛结构示例",
    )
    print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    print()
    print(render_wealth_structure_report(report), end="")


if __name__ == "__main__":
    main()

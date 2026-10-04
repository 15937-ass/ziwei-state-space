#!/usr/bin/env python3
"""Emit a deterministic no-LLM PL2-D wealth EvidencePackage sample."""

from __future__ import annotations

import json
from pathlib import Path

from src.product.wealth_pilot import (
    build_wealth_evidence_package,
    load_pilot_registry,
    load_projection_rows,
)

ROOT = Path(__file__).resolve().parents[1]
W01 = ROOT / "validation/wp05/W01_wealth_projection_review_001_100.csv"
REGISTRY = ROOT / "product/PL2C_WEALTH_PILOT_v0.1.json"


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
            "name": "pl2d-synthetic",
            "version": "0.1",
            "adapter_version": "0.1",
        },
        "input": {"solar_date": "2000-01-01"},
        "chart": {"palaces": palaces},
    }


def main() -> None:
    rows = load_projection_rows(W01)
    registry = load_pilot_registry(REGISTRY)
    package = build_wealth_evidence_package(
        sample_snapshot(),
        rows,
        registry,
        question="PL2-D 财帛结构化示例",
    )
    print(json.dumps(package.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

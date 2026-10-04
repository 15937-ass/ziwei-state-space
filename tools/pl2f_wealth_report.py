#!/usr/bin/env python3
"""Emit the PL2-F 22-rule deterministic natal wealth report."""

from __future__ import annotations

import json
from pathlib import Path

from src.product.wealth_pilot import (
    build_wealth_structure_report,
    compose_wealth_registries,
    load_pilot_registry,
    load_projection_rows,
)
from src.product.wealth_semantics import (
    compose_wealth_semantic_registries,
    load_wealth_semantic_overlay,
    load_wealth_semantic_registry,
    render_wealth_structure_report,
)

ROOT = Path(__file__).resolve().parents[1]
W01 = ROOT / "validation/wp05/W01_wealth_projection_review_001_100.csv"
B01 = ROOT / "product/PL2C_WEALTH_PILOT_v0.1.json"
B02 = ROOT / "product/PL2F_WEALTH_NORMALIZATION_BATCH2_v0.1.json"
SEM_BASE = ROOT / "product/PL2E_WEALTH_SEMANTIC_REGISTRY_v0.1.json"
SEM_B02 = ROOT / "product/PL2F_WEALTH_SEMANTIC_BATCH2_v0.1.json"


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
            star("天府"),
            star("文昌", "科"),
            star("天魁"),
            star("火星"),
        ],
        "minor_stars": [],
        "adjective_stars": [],
    }
    return {
        "schema_version": "0.1",
        "engine": {
            "name": "pl2f-synthetic",
            "version": "0.1",
            "adapter_version": "0.1",
        },
        "input": {"solar_date": "2000-01-01"},
        "chart": {"palaces": palaces},
    }


def main() -> None:
    rows = load_projection_rows(W01)
    executable = compose_wealth_registries(
        load_pilot_registry(B01),
        load_pilot_registry(B02),
    )
    semantic = compose_wealth_semantic_registries(
        load_wealth_semantic_registry(SEM_BASE),
        load_wealth_semantic_overlay(SEM_B02),
    )
    report = build_wealth_structure_report(
        sample_snapshot(),
        rows,
        executable,
        semantic,
        question="PL2-F 本命财帛结构示例",
    )
    print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    print()
    print(render_wealth_structure_report(report), end="")


if __name__ == "__main__":
    main()

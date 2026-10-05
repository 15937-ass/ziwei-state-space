#!/usr/bin/env python3
"""Emit the PL2-J B04 38-rule deterministic natal wealth report."""

from __future__ import annotations

import json
from pathlib import Path

from src.product.palace_structure import load_palace_ontology
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
B03 = ROOT / "product/PL2H_WEALTH_CROSS_PALACE_BATCH_v0.1.json"
B04 = ROOT / "product/PL2J_WEALTH_READY_BATCH1_v0.1.json"
SEM_BASE = ROOT / "product/PL2E_WEALTH_SEMANTIC_REGISTRY_v0.1.json"
SEM_B02 = ROOT / "product/PL2F_WEALTH_SEMANTIC_BATCH2_v0.1.json"
SEM_B03 = ROOT / "product/PL2H_WEALTH_SEMANTIC_BATCH3_v0.1.json"
SEM_B04 = ROOT / "product/PL2J_WEALTH_SEMANTIC_BATCH4_v0.1.json"
ONTOLOGY = ROOT / "knowledge/wp05/palace_ontology_v0.1.csv"

BRANCH = {
    "命宫": "酉",
    "兄弟宫": "戌",
    "夫妻宫": "未",
    "子女宫": "申",
    "财帛宫": "巳",
    "疾厄宫": "午",
    "迁移宫": "卯",
    "交友宫": "辰",
    "事业宫": "丑",
    "田宅宫": "寅",
    "福德宫": "亥",
    "父母宫": "子",
}


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
    stars = {
        "财帛宫": [
            star("左辅"),
            star("火星"),
            star("天机"),
            star("破军"),
            star("地空"),
            star("禄存"),
        ]
    }
    for palace_name, branch in BRANCH.items():
        palaces[branch] = {
            "name": palace_name[:-1],
            "stem": "甲",
            "branch": branch,
            "is_body_palace": False,
            "major_stars": list(stars.get(palace_name, [])),
            "minor_stars": [],
            "adjective_stars": [],
        }
    return {
        "schema_version": "0.2",
        "engine": {
            "name": "pl2j-synthetic",
            "version": "0.1",
            "adapter_version": "0.2",
        },
        "input": {},
        "natal": {"palaces": palaces},
    }


def main() -> None:
    rows = load_projection_rows(W01)
    executable = compose_wealth_registries(
        load_pilot_registry(B01),
        load_pilot_registry(B02),
        load_pilot_registry(B03),
        load_pilot_registry(B04),
    )
    semantic = compose_wealth_semantic_registries(
        load_wealth_semantic_registry(SEM_BASE),
        load_wealth_semantic_overlay(SEM_B02),
        load_wealth_semantic_overlay(SEM_B03),
        load_wealth_semantic_overlay(SEM_B04),
    )
    ontology = load_palace_ontology(ONTOLOGY)
    report = build_wealth_structure_report(
        sample_snapshot(),
        rows,
        executable,
        semantic,
        question="PL2-J B04 本命财帛结构示例",
        palace_ontology=ontology,
    )
    print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    print()
    print(render_wealth_structure_report(report), end="")


if __name__ == "__main__":
    main()

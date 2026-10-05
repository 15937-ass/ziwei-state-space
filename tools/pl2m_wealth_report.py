#!/usr/bin/env python3
"""Emit PL2-M 54-rule deterministic wealth EvidencePackage with antecedent trace."""

from __future__ import annotations

import json
from pathlib import Path

from src.product.palace_structure import load_palace_ontology
from src.product.wealth_pilot import (
    build_wealth_evidence_package,
    compose_wealth_registries,
    load_pilot_registry,
    load_projection_rows,
)

ROOT = Path(__file__).resolve().parents[1]
W01 = ROOT / "validation/wp05/W01_wealth_projection_review_001_100.csv"
ONTOLOGY = ROOT / "knowledge/wp05/palace_ontology_v0.1.csv"
BATCHES = [
    ROOT / "product/PL2C_WEALTH_PILOT_v0.1.json",
    ROOT / "product/PL2F_WEALTH_NORMALIZATION_BATCH2_v0.1.json",
    ROOT / "product/PL2H_WEALTH_CROSS_PALACE_BATCH_v0.1.json",
    ROOT / "product/PL2J_WEALTH_READY_BATCH1_v0.1.json",
    ROOT / "product/PL2J2_WEALTH_READY_BATCH2_v0.1.json",
    ROOT / "product/PL2M_WEALTH_ANTECEDENT_EXECUTABLE_BATCH_v0.1.json",
]

BRANCH = {
    "命宫": "酉", "兄弟宫": "戌", "夫妻宫": "未", "子女宫": "申",
    "财帛宫": "巳", "疾厄宫": "午", "迁移宫": "卯", "交友宫": "辰",
    "事业宫": "丑", "田宅宫": "寅", "福德宫": "亥", "父母宫": "子",
}


def star(name: str, mutagen: str | None = None) -> dict:
    return {"name": name, "brightness": None, "mutagen": mutagen, "type": None, "scope": None}


def snapshot() -> dict:
    stars = {
        "财帛宫": [star("武曲", "忌"), star("七杀")],
        "福德宫": [star("天府", "科")],
    }
    palaces = {}
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
        "engine": {"name": "pl2m-synthetic", "version": "0.1", "adapter_version": "0.2"},
        "input": {},
        "natal": {"palaces": palaces},
    }


def main() -> None:
    rows = load_projection_rows(W01)
    registry = compose_wealth_registries(
        *(load_pilot_registry(path) for path in BATCHES)
    )
    package = build_wealth_evidence_package(
        snapshot(),
        rows,
        registry,
        question="PL2-M antecedent trace sample",
        palace_ontology=load_palace_ontology(ONTOLOGY),
    )
    print(json.dumps(package.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

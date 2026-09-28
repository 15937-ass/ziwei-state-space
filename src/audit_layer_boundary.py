"""Deterministic triage for L1/L2 state vs L3 projection boundary candidates.

This classifier is intentionally conservative.  It does not rewrite canonical
records and it never marks normalization as verified.  Its purpose is to split
the 800 known outcome_descriptor + directional-operator candidates into review
buckets reproducibly.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path
from typing import Mapping


DIRECTIONAL = {"enhance", "weaken", "transform", "inhibit", "activate"}

L3 = re.compile(
    r"职业|事业|财富|财务|收入|损失|破败|成功|失败|机会|收获|婚姻|感情结果|"
    r"疾病|健康|手术|目疾|地位|声誉|名誉|官非|灾|考试|学业|迁移|投资|工作|"
    r"发展|待遇|职位|传统标签|教材案例|事件|输出|结果|风险标签|现实领域|现实发展|"
    r"现实收益|现实损耗|际遇|获利|破财|升迁|官禄|婚恋|生育"
)

L2 = re.compile(
    r"关系|支持|孤立|孤离|竞争|协同|团队|助力|贵人|属下|社交|合作|权威|主导|"
    r"网络|争议|冲突|拖累"
)

L1 = re.compile(
    r"端增强|端下降|增强$|下降$|稳定性|变动|变化|现实化|空想|目标导向|欲望驱动|"
    r"物欲|情欲|认知|决策|行动|意志|毅力|刚柔|刚性|柔弱|调和|缓冲|遮蔽|明朗|"
    r"阴暗|开朗|沉稳|浮薄|浮荡|坚忍|躁进|短志|顽嚣|正直|徇私|敏感|尖刻|明断|"
    r"怯懦|谦和|孤克|克忌|积极|消极|理性|感性|原则|规范|适应|承载|稳定端|开创端|"
    r"上进端"
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def is_candidate(row: Mapping[str, str]) -> bool:
    return (
        row.get("target_type") == "outcome_descriptor"
        and row.get("operator") in DIRECTIONAL
    )


def classify(row: Mapping[str, str]) -> dict[str, str]:
    text = " ".join(
        [
            row.get("target_literal", ""),
            row.get("target_normalized", ""),
            row.get("evidence_text", ""),
        ]
    )
    l3 = bool(L3.search(text))
    l2 = bool(L2.search(text))
    l1 = bool(L1.search(text))

    if l3 and not l1 and not l2:
        return {
            "audit_class": "LIKELY_L3_PROJECTION",
            "proposed_target_type": "outcome_descriptor",
            "proposed_operator": "project",
            "confidence": "high",
        }
    if l2 and not l3:
        return {
            "audit_class": "LIKELY_L2_RELATIONAL",
            "proposed_target_type": "relational_state",
            "proposed_operator": row.get("operator", ""),
            "confidence": "medium",
        }
    if l1 and not l3 and not l2:
        return {
            "audit_class": "LIKELY_L1_STATE",
            "proposed_target_type": "qi_state",
            "proposed_operator": row.get("operator", ""),
            "confidence": "medium",
        }
    if l3 and (l1 or l2):
        return {
            "audit_class": "MIXED_STATE_AND_PROJECTION",
            "proposed_target_type": "REVIEW_REQUIRED",
            "proposed_operator": "REVIEW_REQUIRED",
            "confidence": "low",
        }
    if l2 and l1:
        return {
            "audit_class": "MIXED_L1_L2",
            "proposed_target_type": "REVIEW_REQUIRED",
            "proposed_operator": "REVIEW_REQUIRED",
            "confidence": "low",
        }
    return {
        "audit_class": "UNRESOLVED",
        "proposed_target_type": "REVIEW_REQUIRED",
        "proposed_operator": "REVIEW_REQUIRED",
        "confidence": "low",
    }


def audit(path: Path) -> dict:
    rows = read_csv(path)
    candidates = [row for row in rows if is_candidate(row)]
    classified = [{**row, **classify(row)} for row in candidates]
    return {
        "candidate_count": len(classified),
        "counts": dict(Counter(row["audit_class"] for row in classified)),
        "records": classified,
        "note": "Triage only; normalization remains unverified until source-span review.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "catalog",
        nargs="?",
        default="knowledge/rules/systems/sixty_systems_canonical_v0.1.csv",
    )
    parser.add_argument("--output")
    args = parser.parse_args()

    report = audit(Path(args.catalog))
    payload = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""PL2-P blocker handoff contract after the 59/100 W01 executable checkpoint."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

HANDOFF_CLASSES=frozenset({
    "KNOWLEDGE_REVIEW_HANDOFF",
    "UPSTREAM_DEPENDENCY_HOLD",
    "HUMAN_REVIEW_REQUIRED",
    "PL3_TEMPORAL_HANDOFF",
})

@dataclass(frozen=True)
class WealthBlockerHandoff:
    projection_rule_id: str
    handoff_class: str
    owner: str
    recommended_work_unit: str

def load_wealth_blocker_handoff(path: str|Path) -> tuple[WealthBlockerHandoff,...]:
    with Path(path).open("r",encoding="utf-8-sig",newline="") as handle:
        rows=list(csv.DictReader(handle))
    return tuple(WealthBlockerHandoff(
        projection_rule_id=row["projection_rule_id"].strip(),
        handoff_class=row["handoff_class"].strip(),
        owner=row["owner"].strip(),
        recommended_work_unit=row["recommended_work_unit"].strip(),
    ) for row in rows)

def validate_wealth_blocker_handoff(
    rows: Iterable[WealthBlockerHandoff],
    *,
    expected_pending_rule_ids: Iterable[str],
) -> dict[str,int]:
    data=tuple(rows)
    expected={str(x).strip() for x in expected_pending_rule_ids}
    ids=[r.projection_rule_id for r in data]
    if len(ids)!=len(set(ids)):
        raise ValueError("PL2-P contains duplicate rule ids")
    if set(ids)!=expected:
        raise ValueError(
            f"PL2-P coverage mismatch missing={sorted(expected-set(ids))} "
            f"extra={sorted(set(ids)-expected)}"
        )
    counts={name:0 for name in sorted(HANDOFF_CLASSES)}
    for row in data:
        if row.handoff_class not in HANDOFF_CLASSES:
            raise ValueError(f"{row.projection_rule_id}: invalid handoff class")
        if not row.owner or not row.recommended_work_unit:
            raise ValueError(f"{row.projection_rule_id}: incomplete handoff metadata")
        if row.handoff_class=="HUMAN_REVIEW_REQUIRED" and row.owner!="USER_HUMAN_GATE":
            raise ValueError(f"{row.projection_rule_id}: human review must be user-owned")
        counts[row.handoff_class]+=1
    return counts

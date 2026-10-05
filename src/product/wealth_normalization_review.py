"""PL2-O source-grounded normalization review ledger."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


DISPOSITIONS = frozenset({
    "EXECUTABLE_NORMALIZATION_READY",
    "SOURCE_CLARIFIED_RELATION_PENDING",
    "SOURCE_CLARIFIED_STRUCTURE_PENDING",
    "SOURCE_SPAN_RECHECK",
    "SOURCE_SPLIT_REQUIRED",
    "OPEN_SET_UNRESOLVED",
})


@dataclass(frozen=True)
class NormalizationReview:
    projection_rule_id: str
    review_disposition: str
    human_gate_required: str
    normalized_condition_proposal: str
    source_clarification: str
    remaining_blocker: str
    recommended_work_unit: str


def load_normalization_review(path: str | Path) -> tuple[NormalizationReview, ...]:
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        rows=list(csv.DictReader(handle))
    return tuple(
        NormalizationReview(
            projection_rule_id=row["projection_rule_id"].strip(),
            review_disposition=row["review_disposition"].strip(),
            human_gate_required=row["human_gate_required"].strip(),
            normalized_condition_proposal=row["normalized_condition_proposal"].strip(),
            source_clarification=row["source_clarification"].strip(),
            remaining_blocker=row["remaining_blocker"].strip(),
            recommended_work_unit=row["recommended_work_unit"].strip(),
        )
        for row in rows
    )


def validate_normalization_review(
    rows: Iterable[NormalizationReview],
    *,
    expected_rule_ids: Iterable[str],
) -> dict[str,int]:
    data=tuple(rows)
    expected=set(expected_rule_ids)
    ids=[r.projection_rule_id for r in data]
    if len(ids)!=len(set(ids)):
        raise ValueError("duplicate rule id in PL2-O review")
    if set(ids)!=expected:
        raise ValueError(f"PL2-O coverage mismatch missing={sorted(expected-set(ids))} extra={sorted(set(ids)-expected)}")
    counts={k:0 for k in sorted(DISPOSITIONS)}
    for row in data:
        if row.review_disposition not in DISPOSITIONS:
            raise ValueError(f"{row.projection_rule_id}: invalid disposition")
        if row.human_gate_required!="NO":
            raise ValueError(f"{row.projection_rule_id}: PL2-O must not silently approve a Human Gate")
        if not row.source_clarification or not row.remaining_blocker or not row.recommended_work_unit:
            raise ValueError(f"{row.projection_rule_id}: incomplete review metadata")
        counts[row.review_disposition]+=1
    return counts

"""Product-side readiness audit for the WP05 Career Palace corpus.

This module does not normalize or repair knowledge records. It only checks
whether reviewed career-projection batches are structurally ready to enter
product executable-normalization work.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

ALLOWED_TIME_LAYERS = frozenset({"NATAL", "DECADE", "YEAR", "MONTH", "DAY", "HOUR"})

SCHEMA_DRIFT_TIME_CONDITION_SWAP = "TIME_LAYER_CONDITION_COLUMN_ORDER_DRIFT"


@dataclass(frozen=True)
class CareerBatchAudit:
    path: str
    row_count: int
    source_verified_rows: int
    case_support_only_rows: int
    history_feedback_rows: int
    schema_drift_rows: int
    schema_drift_type: str | None


@dataclass(frozen=True)
class CareerReadinessSummary:
    batch_count: int
    total_rows: int
    source_verified_rows: int
    case_support_only_rows: int
    history_feedback_rows: int
    schema_drift_rows: int
    closure_complete: bool
    ready_for_executable_normalization: bool
    blockers: tuple[str, ...]
    batches: tuple[CareerBatchAudit, ...]

    def to_dict(self) -> dict:
        return {
            "batch_count": self.batch_count,
            "total_rows": self.total_rows,
            "source_verified_rows": self.source_verified_rows,
            "case_support_only_rows": self.case_support_only_rows,
            "history_feedback_rows": self.history_feedback_rows,
            "schema_drift_rows": self.schema_drift_rows,
            "closure_complete": self.closure_complete,
            "ready_for_executable_normalization": self.ready_for_executable_normalization,
            "blockers": list(self.blockers),
            "batches": [
                {
                    "path": item.path,
                    "row_count": item.row_count,
                    "source_verified_rows": item.source_verified_rows,
                    "case_support_only_rows": item.case_support_only_rows,
                    "history_feedback_rows": item.history_feedback_rows,
                    "schema_drift_rows": item.schema_drift_rows,
                    "schema_drift_type": item.schema_drift_type,
                }
                for item in self.batches
            ],
        }


def _truthy(value: str) -> bool:
    return str(value or "").strip().lower() == "true"


def audit_career_batch(path: str | Path) -> CareerBatchAudit:
    path = Path(path)
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    if not rows:
        raise ValueError(f"{path}: career batch must not be empty")

    required = {
        "projection_rule_id",
        "source_id",
        "source_location",
        "palace_id",
        "time_layer",
        "condition",
        "projection_domain",
        "projection_target",
        "projection_mode",
        "review_status",
        "source_span_verified",
        "case_support_only",
        "history_feedback",
    }
    missing = sorted(required - set(rows[0]))
    if missing:
        raise ValueError(f"{path}: missing required columns: {', '.join(missing)}")

    verified = 0
    case_only = 0
    history = 0
    drift = 0

    for row in rows:
        rule_id = str(row.get("projection_rule_id", "")).strip()
        if not rule_id:
            raise ValueError(f"{path}: row missing projection_rule_id")

        if _truthy(row.get("source_span_verified", "")):
            verified += 1
        if _truthy(row.get("case_support_only", "")):
            case_only += 1
        if str(row.get("history_feedback", "")).strip():
            history += 1

        time_layer = str(row.get("time_layer", "")).strip()
        condition = str(row.get("condition", "")).strip()
        if time_layer not in ALLOWED_TIME_LAYERS:
            if condition in ALLOWED_TIME_LAYERS:
                drift += 1

    return CareerBatchAudit(
        path=str(path),
        row_count=len(rows),
        source_verified_rows=verified,
        case_support_only_rows=case_only,
        history_feedback_rows=history,
        schema_drift_rows=drift,
        schema_drift_type=SCHEMA_DRIFT_TIME_CONDITION_SWAP if drift else None,
    )


def audit_career_projection_batches(
    paths: Iterable[str | Path],
    *,
    closure_complete: bool,
) -> CareerReadinessSummary:
    batches = tuple(audit_career_batch(path) for path in paths)
    if not batches:
        raise ValueError("at least one career batch is required")

    total = sum(item.row_count for item in batches)
    verified = sum(item.source_verified_rows for item in batches)
    case_only = sum(item.case_support_only_rows for item in batches)
    history = sum(item.history_feedback_rows for item in batches)
    drift = sum(item.schema_drift_rows for item in batches)

    blockers: list[str] = []
    if verified != total:
        blockers.append("UNVERIFIED_SOURCE_ROWS")
    if drift:
        blockers.append(SCHEMA_DRIFT_TIME_CONDITION_SWAP)
    if not closure_complete:
        blockers.append("CAREER_CORPUS_CLOSURE_PENDING")

    return CareerReadinessSummary(
        batch_count=len(batches),
        total_rows=total,
        source_verified_rows=verified,
        case_support_only_rows=case_only,
        history_feedback_rows=history,
        schema_drift_rows=drift,
        closure_complete=bool(closure_complete),
        ready_for_executable_normalization=not blockers,
        blockers=tuple(blockers),
        batches=batches,
    )

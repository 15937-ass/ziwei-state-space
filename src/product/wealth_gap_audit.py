"""PL2-I product-side executable gap audit helpers.

The audit classifies *engineering readiness* of already source-span-verified W01
rows. It does not reinterpret the source text and does not promote rules into
the executable set.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping


READINESS_CLASSES = (
    "LOCAL_ATOM_READY",
    "CROSS_PALACE_READY",
    "NEEDS_STRUCTURE_PRIMITIVE",
    "NEEDS_TEMPORAL_STATE",
    "NEEDS_PATH_HISTORY",
    "NEEDS_VALENCE_MODEL",
    "ANTECEDENT_DEPENDENT",
    "NORMALIZATION_AMBIGUOUS",
)
READY_CLASSES = frozenset({"LOCAL_ATOM_READY", "CROSS_PALACE_READY"})


@dataclass(frozen=True)
class WealthGapAuditRow:
    projection_rule_id: str
    source_id: str
    source_location: str
    time_layer: str
    condition: str
    projection_domain: str
    projection_target: str
    projection_mode: str
    readiness_class: str
    secondary_blockers: tuple[str, ...]
    recommended_work_unit: str
    audit_note: str


@dataclass(frozen=True)
class WealthGapAuditSummary:
    total_pending: int
    counts: Mapping[str, int]
    immediately_ready: int

    def to_dict(self) -> dict:
        return {
            "total_pending": self.total_pending,
            "counts": dict(self.counts),
            "immediately_ready": self.immediately_ready,
        }


def load_wealth_gap_audit(path: str | Path) -> tuple[WealthGapAuditRow, ...]:
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    out: list[WealthGapAuditRow] = []
    for row in rows:
        secondary = tuple(
            item.strip()
            for item in str(row.get("secondary_blockers", "")).split(";")
            if item.strip()
        )
        out.append(
            WealthGapAuditRow(
                projection_rule_id=str(row.get("projection_rule_id", "")).strip(),
                source_id=str(row.get("source_id", "")).strip(),
                source_location=str(row.get("source_location", "")).strip(),
                time_layer=str(row.get("time_layer", "")).strip(),
                condition=str(row.get("condition", "")).strip(),
                projection_domain=str(row.get("projection_domain", "")).strip(),
                projection_target=str(row.get("projection_target", "")).strip(),
                projection_mode=str(row.get("projection_mode", "")).strip(),
                readiness_class=str(row.get("readiness_class", "")).strip(),
                secondary_blockers=secondary,
                recommended_work_unit=str(row.get("recommended_work_unit", "")).strip(),
                audit_note=str(row.get("audit_note", "")).strip(),
            )
        )
    return tuple(out)


def validate_wealth_gap_audit(
    projection_rows: Iterable[Mapping[str, str]],
    executable_rule_ids: Iterable[str],
    audit_rows: Iterable[WealthGapAuditRow],
) -> WealthGapAuditSummary:
    canonical: dict[str, Mapping[str, str]] = {}
    for row in projection_rows:
        rule_id = str(row.get("projection_rule_id", "")).strip()
        if not rule_id:
            raise ValueError("canonical projection row missing projection_rule_id")
        if rule_id in canonical:
            raise ValueError(f"duplicate canonical projection_rule_id: {rule_id}")
        canonical[rule_id] = row

    executable = {str(rule_id).strip() for rule_id in executable_rule_ids}
    unknown_exec = sorted(executable - set(canonical))
    if unknown_exec:
        raise ValueError("executable rule ids absent from W01: " + ", ".join(unknown_exec))

    expected_pending = set(canonical) - executable
    audit_index: dict[str, WealthGapAuditRow] = {}
    for row in audit_rows:
        if not row.projection_rule_id:
            raise ValueError("audit row missing projection_rule_id")
        if row.projection_rule_id in audit_index:
            raise ValueError(f"duplicate audit rule_id: {row.projection_rule_id}")
        audit_index[row.projection_rule_id] = row

        if row.readiness_class not in READINESS_CLASSES:
            raise ValueError(
                f"{row.projection_rule_id}: invalid readiness_class "
                f"{row.readiness_class!r}"
            )
        if not row.recommended_work_unit:
            raise ValueError(f"{row.projection_rule_id}: recommended_work_unit required")
        if not row.audit_note:
            raise ValueError(f"{row.projection_rule_id}: audit_note required")

        for blocker in row.secondary_blockers:
            if blocker not in READINESS_CLASSES:
                raise ValueError(
                    f"{row.projection_rule_id}: invalid secondary blocker {blocker!r}"
                )
            if blocker == row.readiness_class:
                raise ValueError(
                    f"{row.projection_rule_id}: secondary blocker duplicates primary class"
                )

        if row.readiness_class in READY_CLASSES and row.secondary_blockers:
            raise ValueError(
                f"{row.projection_rule_id}: READY rows cannot retain secondary blockers"
            )

    actual = set(audit_index)
    if actual != expected_pending:
        missing = sorted(expected_pending - actual)
        extra = sorted(actual - expected_pending)
        raise ValueError(f"audit coverage mismatch missing={missing} extra={extra}")

    parity_fields = (
        "source_id",
        "source_location",
        "time_layer",
        "condition",
        "projection_domain",
        "projection_target",
        "projection_mode",
    )
    for rule_id, audit_row in audit_index.items():
        source = canonical[rule_id]
        for field in parity_fields:
            audit_value = getattr(audit_row, field)
            source_value = str(source.get(field, "")).strip()
            if audit_value != source_value:
                raise ValueError(
                    f"{rule_id}: audit source drift in {field}: "
                    f"{audit_value!r} != {source_value!r}"
                )

        if audit_row.time_layer != "NATAL" and (
            audit_row.readiness_class != "NEEDS_TEMPORAL_STATE"
        ):
            raise ValueError(
                f"{rule_id}: non-NATAL pending rule must be NEEDS_TEMPORAL_STATE"
            )

        history_feedback = str(source.get("history_feedback", "")).strip()
        if history_feedback and (
            audit_row.readiness_class != "NEEDS_PATH_HISTORY"
            and "NEEDS_PATH_HISTORY" not in audit_row.secondary_blockers
        ):
            raise ValueError(
                f"{rule_id}: history_feedback requires NEEDS_PATH_HISTORY"
            )

    counts = {name: 0 for name in READINESS_CLASSES}
    for row in audit_index.values():
        counts[row.readiness_class] += 1

    ready = sum(counts[name] for name in READY_CLASSES)
    return WealthGapAuditSummary(
        total_pending=len(audit_index),
        counts=counts,
        immediately_ready=ready,
    )

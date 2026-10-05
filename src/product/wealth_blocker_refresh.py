"""PL2-K blocker-only roadmap validation for the remaining W01 rules."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROUTE_CLASSES = frozenset(
    {
        "ANTECEDENT_ENGINEERING",
        "STRUCTURE_SOURCE_BACKED",
        "SOURCE_NORMALIZATION_REQUIRED",
        "HUMAN_GATE_REQUIRED",
        "DEFER_PL3_TEMPORAL",
    }
)


@dataclass(frozen=True)
class WealthBlockerRoute:
    projection_rule_id: str
    time_layer: str
    condition: str
    primary_blocker: str
    secondary_blockers: tuple[str, ...]
    route_class: str
    human_gate_status: str
    support_basis: str
    recommended_work_unit: str
    route_rationale: str


def load_wealth_blocker_refresh(path: str | Path) -> tuple[WealthBlockerRoute, ...]:
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    out: list[WealthBlockerRoute] = []
    for row in rows:
        out.append(
            WealthBlockerRoute(
                projection_rule_id=str(row.get("projection_rule_id", "")).strip(),
                time_layer=str(row.get("time_layer", "")).strip(),
                condition=str(row.get("condition", "")).strip(),
                primary_blocker=str(row.get("primary_blocker", "")).strip(),
                secondary_blockers=tuple(
                    item.strip()
                    for item in str(row.get("secondary_blockers", "")).split(";")
                    if item.strip()
                ),
                route_class=str(row.get("route_class", "")).strip(),
                human_gate_status=str(row.get("human_gate_status", "")).strip(),
                support_basis=str(row.get("support_basis", "")).strip(),
                recommended_work_unit=str(row.get("recommended_work_unit", "")).strip(),
                route_rationale=str(row.get("route_rationale", "")).strip(),
            )
        )
    return tuple(out)


def validate_wealth_blocker_refresh(
    rows: Iterable[WealthBlockerRoute],
    *,
    expected_pending_rule_ids: Iterable[str],
) -> dict[str, int]:
    data = tuple(rows)
    expected = {str(x).strip() for x in expected_pending_rule_ids}
    ids = [row.projection_rule_id for row in data]

    if len(ids) != len(set(ids)):
        raise ValueError("PL2-K blocker refresh contains duplicate rule ids")
    if set(ids) != expected:
        missing = sorted(expected - set(ids))
        extra = sorted(set(ids) - expected)
        raise ValueError(f"PL2-K blocker coverage mismatch missing={missing} extra={extra}")

    counts = {name: 0 for name in sorted(ROUTE_CLASSES)}
    for row in data:
        if row.route_class not in ROUTE_CLASSES:
            raise ValueError(
                f"{row.projection_rule_id}: invalid route_class {row.route_class!r}"
            )
        if not row.primary_blocker:
            raise ValueError(f"{row.projection_rule_id}: primary_blocker required")
        if row.primary_blocker in {"LOCAL_ATOM_READY", "CROSS_PALACE_READY"}:
            raise ValueError(
                f"{row.projection_rule_id}: READY rule leaked into blocker-only refresh"
            )
        if not row.support_basis or not row.recommended_work_unit or not row.route_rationale:
            raise ValueError(f"{row.projection_rule_id}: incomplete blocker route metadata")

        if row.route_class == "HUMAN_GATE_REQUIRED":
            if row.human_gate_status != "YES":
                raise ValueError(f"{row.projection_rule_id}: Human Gate route must be YES")
        elif row.human_gate_status == "YES":
            raise ValueError(
                f"{row.projection_rule_id}: only HUMAN_GATE_REQUIRED may set YES"
            )

        if row.route_class == "DEFER_PL3_TEMPORAL":
            if row.primary_blocker != "NEEDS_TEMPORAL_STATE":
                raise ValueError(
                    f"{row.projection_rule_id}: PL3 route requires temporal blocker"
                )

        counts[row.route_class] += 1

    return counts

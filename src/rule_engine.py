"""Minimal traceable rule engine for Paper 1.

The engine is deliberately symbolic. It retrieves and filters approved/structured
rules, preserves provenance, and refuses to turn semantic states into fixed life
events without an explicit projection rule.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Mapping, Optional, Sequence


@dataclass(frozen=True)
class Rule:
    rule_id: str
    school: str
    source_work: str
    source_location: str
    subject: str
    context: str
    condition: str
    target_type: str
    target_literal: str
    target_normalized: str
    operator: str
    state_change: str
    valence: str
    epistemic_type_source: str
    evidence_text: str
    status: str

    @classmethod
    def from_row(cls, row: Mapping[str, str]) -> "Rule":
        return cls(
            rule_id=row["rule_id"],
            school=row["school"],
            source_work=row["source_work"],
            source_location=row["source_location"],
            subject=row["subject"],
            context=row["context"],
            condition=row["condition"],
            target_type=row["target_type"],
            target_literal=row["target_literal"],
            target_normalized=row["target_normalized"],
            operator=row["operator"],
            state_change=row["state_change"],
            valence=row["valence"],
            epistemic_type_source=row["epistemic_type_source"],
            evidence_text=row["evidence_text"],
            status=row["status"],
        )


def load_rules(*paths: str | Path) -> List[Rule]:
    rules: List[Rule] = []
    for path in paths:
        with Path(path).open("r", encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                rules.append(Rule.from_row(row))
    return rules


def query_rules(
    rules: Iterable[Rule],
    *,
    subject: Optional[str] = None,
    condition_contains: Optional[str] = None,
    target_type: Optional[str] = None,
    operator: Optional[str] = None,
) -> List[Rule]:
    out: List[Rule] = []
    for rule in rules:
        if subject is not None and rule.subject != subject:
            continue
        if condition_contains is not None and condition_contains not in rule.condition:
            continue
        if target_type is not None and rule.target_type != target_type:
            continue
        if operator is not None and rule.operator != operator:
            continue
        out.append(rule)
    return out


def trace(rule: Rule) -> dict:
    """Return the minimum provenance chain required by Paper 1."""
    return {
        "rule_id": rule.rule_id,
        "source_work": rule.source_work,
        "source_location": rule.source_location,
        "epistemic_type_source": rule.epistemic_type_source,
        "evidence_text": rule.evidence_text,
        "normalized_target": rule.target_normalized,
    }


def semantic_state_changes(rules: Sequence[Rule]) -> List[dict]:
    """Return symbolic state changes only; no fixed event prediction."""
    changes: List[dict] = []
    for rule in rules:
        if rule.target_type != "qi_state":
            continue
        changes.append(
            {
                "rule_id": rule.rule_id,
                "target": rule.target_normalized,
                "operator": rule.operator,
                "state_change": rule.state_change,
                "valence": rule.valence,
            }
        )
    return changes


def reject_fixed_event_mapping(event_name: str, provenance_rule_ids: Sequence[str]) -> None:
    """Guardrail: a concrete event requires an explicit downstream projection model."""
    if event_name and not provenance_rule_ids:
        raise ValueError(
            "Concrete event mapping requires explicit projection provenance; "
            "star/system state alone is insufficient."
        )

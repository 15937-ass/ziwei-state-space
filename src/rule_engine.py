"""Traceable symbolic rule loader / query layer for Paper 1.

The engine remains deliberately non-predictive.  Gate A1 adds one critical
property: effective rules can be assembled from immutable canonical extraction
plus auditable review/migration sidecars, and quarantined source mismatches are
not executable by default.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Optional, Sequence


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
    source_epistemic: str = ""
    normalization_epistemic: str = ""
    review_status: str = ""
    source_span_verified: bool = False
    normalization_verified: bool = False

    @classmethod
    def from_row(cls, row: Mapping[str, str]) -> "Rule":
        def as_bool(value: str) -> bool:
            return str(value).strip().lower() == "true"

        return cls(
            rule_id=row["rule_id"],
            school=row.get("school", ""),
            source_work=row.get("source_work", ""),
            source_location=row.get("source_location", ""),
            subject=row.get("subject", ""),
            context=row.get("context", ""),
            condition=row.get("condition", ""),
            target_type=row.get("target_type", ""),
            target_literal=row.get("target_literal", ""),
            target_normalized=row.get("target_normalized", ""),
            operator=row.get("operator", ""),
            state_change=row.get("state_change", ""),
            valence=row.get("valence", ""),
            epistemic_type_source=row.get("epistemic_type_source", ""),
            evidence_text=row.get("evidence_text", ""),
            status=row.get("status", ""),
            source_epistemic=row.get("source_epistemic", ""),
            normalization_epistemic=row.get("normalization_epistemic", ""),
            review_status=row.get("review_status", ""),
            source_span_verified=as_bool(row.get("source_span_verified", "false")),
            normalization_verified=as_bool(row.get("normalization_verified", "false")),
        )


def _read_csv(path: str | Path) -> List[dict[str, str]]:
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def _load_quarantine(path: str | Path | None) -> set[str]:
    if not path:
        return set()
    rows = _read_csv(path)
    ids: set[str] = set()
    for row in rows:
        record_id = row.get("record_id") or row.get("rule_id") or ""
        if record_id and row.get("effective_status", "QUARANTINED") == "QUARANTINED":
            ids.add(record_id)
    return ids


def _load_field_overrides(
    path: str | Path | None,
    *,
    id_field: str = "rule_id",
) -> Dict[str, Dict[str, str]]:
    """Load long-form {rule_id, field, new_value} migration rows."""
    if not path:
        return {}
    out: Dict[str, Dict[str, str]] = {}
    for row in _read_csv(path):
        record_id = row.get(id_field, "")
        field = row.get("field", "")
        if record_id and field:
            out.setdefault(record_id, {})[field] = row.get("new_value", "")
    return out


def _load_row_metadata(
    path: str | Path | None,
    *,
    id_field: str = "rule_id",
) -> Dict[str, Dict[str, str]]:
    """Load wide review metadata sidecar keyed by rule id."""
    if not path:
        return {}
    out: Dict[str, Dict[str, str]] = {}
    for row in _read_csv(path):
        record_id = row.get(id_field) or row.get("record_id") or ""
        if record_id:
            out[record_id] = dict(row)
    return out


def load_rules(
    *paths: str | Path,
    quarantine_path: str | Path | None = None,
    schema_overrides_path: str | Path | None = None,
    provenance_overrides_path: str | Path | None = None,
    review_metadata_path: str | Path | None = None,
    source_review_overrides_path: str | Path | None = None,
) -> List[Rule]:
    """Load effective rules while preserving immutable canonical files.

    Sidecars are optional so historical callers continue to work.  When
    supplied, the effective row is assembled in this order:

        canonical
        -> review metadata
        -> source-review metadata
        -> schema overrides
        -> provenance overrides
        -> quarantine filter
    """
    quarantined = _load_quarantine(quarantine_path)
    schema_overrides = _load_field_overrides(schema_overrides_path)
    provenance_overrides = _load_field_overrides(provenance_overrides_path)
    review_meta = _load_row_metadata(review_metadata_path)
    source_review = _load_row_metadata(source_review_overrides_path, id_field="record_id")

    rules: List[Rule] = []
    for path in paths:
        for raw in _read_csv(path):
            row = dict(raw)
            rule_id = row.get("rule_id", "")
            if not rule_id or rule_id in quarantined:
                continue

            if rule_id in review_meta:
                row.update({k: v for k, v in review_meta[rule_id].items() if k != "rule_id"})
            if rule_id in source_review:
                row.update({k: v for k, v in source_review[rule_id].items() if k not in {"record_id", "review_note"}})
            if rule_id in schema_overrides:
                row.update(schema_overrides[rule_id])
            if rule_id in provenance_overrides:
                row.update(provenance_overrides[rule_id])

            rules.append(Rule.from_row(row))
    return rules


def query_rules(
    rules: Iterable[Rule],
    *,
    subject: Optional[str] = None,
    condition_contains: Optional[str] = None,
    target_type: Optional[str] = None,
    operator: Optional[str] = None,
    require_source_verified: bool = False,
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
        if require_source_verified and not rule.source_span_verified:
            continue
        out.append(rule)
    return out


def trace(rule: Rule) -> dict:
    """Return the provenance/review chain used by the effective rule."""
    return {
        "rule_id": rule.rule_id,
        "source_work": rule.source_work,
        "source_location": rule.source_location,
        "legacy_epistemic_type_source": rule.epistemic_type_source,
        "source_epistemic": rule.source_epistemic,
        "normalization_epistemic": rule.normalization_epistemic,
        "review_status": rule.review_status,
        "source_span_verified": rule.source_span_verified,
        "normalization_verified": rule.normalization_verified,
        "evidence_text": rule.evidence_text,
        "normalized_target": rule.target_normalized,
    }


def semantic_state_changes(rules: Sequence[Rule]) -> List[dict]:
    """Return symbolic L1 changes only; no fixed event prediction."""
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
    """Guardrail: a concrete event requires explicit downstream projection provenance."""
    if event_name and not provenance_rule_ids:
        raise ValueError(
            "Concrete event mapping requires explicit projection provenance; "
            "star/system state alone is insufficient."
        )

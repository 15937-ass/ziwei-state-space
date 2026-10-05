"""Typed antecedent/reference links for product RuleIR.

This module records explicit relationships already present in reviewed source
rows. It does not infer antecedents from prose and does not promote reference-
only comparisons into chart triggers.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping


LINK_TYPES = frozenset(
    {
        "INHERIT_ACTIVE",
        "COMPARE_REFERENCES",
        "INHERIT_ACTIVE_PLUS_LOCAL_CONDITION",
    }
)

LINK_STATUSES = frozenset(
    {
        "EXECUTABLE_NOW",
        "REFERENCE_ONLY",
        "UPSTREAM_BLOCKED",
        "UPSTREAM_AND_LOCAL_BLOCKED",
    }
)


@dataclass(frozen=True)
class AntecedentLink:
    rule_id: str
    link_type: str
    antecedent_rule_ids: tuple[str, ...]
    status: str
    local_condition_note: str = ""
    note: str = ""


def load_antecedent_links(path: str | Path) -> tuple[AntecedentLink, ...]:
    with Path(path).open("r", encoding="utf-8") as handle:
        document = json.load(handle)
    if document.get("schema_version") != "0.1":
        raise ValueError("antecedent link schema_version must be 0.1")
    raw_links = document.get("links")
    if not isinstance(raw_links, Mapping) or not raw_links:
        raise ValueError("antecedent link document requires links")

    out: list[AntecedentLink] = []
    for raw_rule_id, raw in raw_links.items():
        rule_id = str(raw_rule_id).strip()
        if not rule_id or not isinstance(raw, Mapping):
            raise ValueError("antecedent link rows require rule_id and mapping")
        antecedents = raw.get("antecedent_rule_ids")
        if not isinstance(antecedents, list) or not antecedents:
            raise ValueError(f"{rule_id}: antecedent_rule_ids must be non-empty list")
        normalized = tuple(str(x).strip() for x in antecedents if str(x).strip())
        if len(normalized) != len(antecedents):
            raise ValueError(f"{rule_id}: empty antecedent rule id")
        out.append(
            AntecedentLink(
                rule_id=rule_id,
                link_type=str(raw.get("link_type", "")).strip(),
                antecedent_rule_ids=normalized,
                status=str(raw.get("status", "")).strip(),
                local_condition_note=str(raw.get("local_condition_note", "")).strip(),
                note=str(raw.get("note", "")).strip(),
            )
        )
    return tuple(sorted(out, key=lambda item: item.rule_id))


def validate_antecedent_links(
    links: Iterable[AntecedentLink],
    *,
    known_rule_ids: Iterable[str],
    executable_rule_ids: Iterable[str],
) -> dict[str, int]:
    data = tuple(links)
    known = {str(x).strip() for x in known_rule_ids}
    executable = {str(x).strip() for x in executable_rule_ids}
    ids = [item.rule_id for item in data]

    if len(ids) != len(set(ids)):
        raise ValueError("duplicate antecedent link rule_id")

    counts = {status: 0 for status in sorted(LINK_STATUSES)}
    for item in data:
        if item.rule_id not in known:
            raise ValueError(f"{item.rule_id}: link target missing from canonical rules")
        if item.link_type not in LINK_TYPES:
            raise ValueError(f"{item.rule_id}: invalid link_type {item.link_type!r}")
        if item.status not in LINK_STATUSES:
            raise ValueError(f"{item.rule_id}: invalid status {item.status!r}")
        missing_known = sorted(set(item.antecedent_rule_ids) - known)
        if missing_known:
            raise ValueError(
                f"{item.rule_id}: unknown antecedent(s): {', '.join(missing_known)}"
            )

        if item.status == "EXECUTABLE_NOW":
            if item.link_type != "INHERIT_ACTIVE":
                raise ValueError(
                    f"{item.rule_id}: EXECUTABLE_NOW requires INHERIT_ACTIVE"
                )
            missing_exec = sorted(set(item.antecedent_rule_ids) - executable)
            if missing_exec:
                raise ValueError(
                    f"{item.rule_id}: executable antecedent missing: {', '.join(missing_exec)}"
                )
        elif item.status == "REFERENCE_ONLY":
            if item.link_type != "COMPARE_REFERENCES":
                raise ValueError(
                    f"{item.rule_id}: REFERENCE_ONLY requires COMPARE_REFERENCES"
                )
        elif item.status == "UPSTREAM_BLOCKED":
            if set(item.antecedent_rule_ids).issubset(executable):
                raise ValueError(
                    f"{item.rule_id}: UPSTREAM_BLOCKED has no blocked antecedent"
                )
        elif item.status == "UPSTREAM_AND_LOCAL_BLOCKED":
            if item.link_type != "INHERIT_ACTIVE_PLUS_LOCAL_CONDITION":
                raise ValueError(
                    f"{item.rule_id}: local-blocked status requires typed link mode"
                )
            if not item.local_condition_note:
                raise ValueError(
                    f"{item.rule_id}: local_condition_note required for local blocker"
                )
            if set(item.antecedent_rule_ids).issubset(executable):
                raise ValueError(
                    f"{item.rule_id}: upstream/local blocked row has no blocked antecedent"
                )

        counts[item.status] += 1

    return counts

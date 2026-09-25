"""Repository decontamination audit for Phase-II knowledge artifacts.

This tool performs deterministic structural checks only. It does NOT decide
whether a Zi Wei Dou Shu statement is true, nor whether a normalization is
semantically faithful to the source. Its job is to surface candidates for
source-span review before later knowledge-base stages continue.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence


RULE_TARGET_TYPES = {
    "qi_state",
    "relational_state",
    "structural_relation",
    "outcome_descriptor",
}

RULE_OPERATORS = {
    "define",
    "assert",
    "condition",
    "enhance",
    "weaken",
    "transform",
    "inhibit",
    "activate",
    "compare",
    "project",
    "gate",
    "couple",
}

MODIFIER_OPERATORS = {
    "enhance",
    "weaken",
    "transform",
    "inhibit",
    "activate",
    "conditional",
    "projection",
    "structural_relation",
    "pair_interaction",
    "gate",
}

RULE_CATALOGS = (
    Path("knowledge/rules/stars/major_stars_canonical_v0.1.csv"),
    Path("knowledge/rules/systems/sixty_systems_canonical_v0.1.csv"),
)

MODIFIER_CATALOGS = (
    Path("knowledge/operators/auxiliary_eight_v0.1.csv"),
    Path("knowledge/operators/six_malefics_v0.1.csv"),
    Path("knowledge/operators/transformation_rules_v0.1.csv"),
    Path("knowledge/operators/misc_stars_v0.1.csv"),
)

COMPOSITE_MARKERS = (
    re.compile(r"[、；;]"),
    re.compile(r"/"),
    re.compile(r"且|或|以及"),
)


@dataclass(frozen=True)
class Finding:
    severity: str
    category: str
    catalog: str
    record_id: str
    field: str
    value: str
    source_location: str
    message: str


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def _id(row: Mapping[str, str]) -> str:
    return row.get("rule_id") or row.get("operator_rule_id") or ""


def duplicate_id_findings(path: Path, rows: Sequence[Mapping[str, str]]) -> list[Finding]:
    ids = [_id(row) for row in rows if _id(row)]
    counts = Counter(ids)
    findings: list[Finding] = []
    for record_id, count in counts.items():
        if count > 1:
            findings.append(
                Finding(
                    "P0",
                    "duplicate_id",
                    str(path),
                    record_id,
                    "id",
                    str(count),
                    "",
                    f"ID appears {count} times.",
                )
            )
    return findings


def audit_rule_catalog(path: Path, rows: Sequence[Mapping[str, str]]) -> list[Finding]:
    findings = duplicate_id_findings(path, rows)
    for row in rows:
        record_id = _id(row)
        target_type = row.get("target_type", "")
        operator = row.get("operator", "")
        if target_type not in RULE_TARGET_TYPES:
            findings.append(
                Finding(
                    "P0",
                    "schema_enum",
                    str(path),
                    record_id,
                    "target_type",
                    target_type,
                    row.get("source_location", ""),
                    "target_type is outside KB_SCHEMA.md controlled vocabulary.",
                )
            )
        if operator not in RULE_OPERATORS:
            findings.append(
                Finding(
                    "P0",
                    "schema_enum",
                    str(path),
                    record_id,
                    "operator",
                    operator,
                    row.get("source_location", ""),
                    "operator is outside KB_SCHEMA.md controlled vocabulary.",
                )
            )
    return findings


def audit_modifier_catalog(path: Path, rows: Sequence[Mapping[str, str]]) -> list[Finding]:
    findings = duplicate_id_findings(path, rows)
    for row in rows:
        record_id = _id(row)
        operator = row.get("operator_type", "")
        if operator not in MODIFIER_OPERATORS:
            findings.append(
                Finding(
                    "P0",
                    "schema_enum",
                    str(path),
                    record_id,
                    "operator_type",
                    operator,
                    row.get("source_location", ""),
                    "operator_type is outside operator_schema.yaml controlled vocabulary.",
                )
            )
    return findings


def composite_condition_score(condition: str) -> int:
    """Heuristic only: high score means source-span atomicity should be reviewed."""
    return sum(bool(pattern.search(condition or "")) for pattern in COMPOSITE_MARKERS)


def atomicity_candidates(path: Path, rows: Sequence[Mapping[str, str]]) -> list[Finding]:
    findings: list[Finding] = []
    for row in rows:
        condition = row.get("condition", "")
        score = composite_condition_score(condition)
        if score >= 2:
            findings.append(
                Finding(
                    "P1",
                    "atomicity_candidate",
                    str(path),
                    _id(row),
                    "condition",
                    condition,
                    row.get("source_location", ""),
                    "Condition contains multiple composition markers; source-span review required.",
                )
            )
    return findings


def outcome_operator_candidates(path: Path, rows: Sequence[Mapping[str, str]]) -> list[Finding]:
    findings: list[Finding] = []
    directional = {"enhance", "weaken", "transform", "inhibit", "activate"}
    for row in rows:
        if row.get("target_type") == "outcome_descriptor" and row.get("operator") in directional:
            findings.append(
                Finding(
                    "P1",
                    "layer_boundary_candidate",
                    str(path),
                    _id(row),
                    "operator",
                    row.get("operator", ""),
                    row.get("source_location", ""),
                    "Outcome descriptor uses a directional state operator; check L1/L2 -> L3 projection boundary.",
                )
            )
    return findings


def status_summary(rows: Iterable[Mapping[str, str]]) -> dict[str, int]:
    return dict(Counter(row.get("status", "") for row in rows))


def epistemic_summary(rows: Iterable[Mapping[str, str]]) -> dict[str, int]:
    return dict(
        Counter(
            (row.get("epistemic_type_source") or row.get("epistemic_type") or "")
            for row in rows
        )
    )


def run_audit(root: Path) -> dict:
    findings: list[Finding] = []
    summaries: dict[str, dict] = {}

    for relative in RULE_CATALOGS:
        path = root / relative
        rows = read_csv(path)
        findings.extend(audit_rule_catalog(relative, rows))
        findings.extend(atomicity_candidates(relative, rows))
        findings.extend(outcome_operator_candidates(relative, rows))
        summaries[str(relative)] = {
            "records": len(rows),
            "status": status_summary(rows),
            "epistemic": epistemic_summary(rows),
        }

    for relative in MODIFIER_CATALOGS:
        path = root / relative
        rows = read_csv(path)
        findings.extend(audit_modifier_catalog(relative, rows))
        summaries[str(relative)] = {
            "records": len(rows),
            "status": status_summary(rows),
            "epistemic": epistemic_summary(rows),
        }

    return {
        "summaries": summaries,
        "finding_counts": dict(Counter(item.severity for item in findings)),
        "findings": [asdict(item) for item in findings],
        "notes": [
            "P0 findings are deterministic schema violations.",
            "P1 findings are review candidates, not proof of semantic error.",
            "Epistemic/source-fidelity review requires returning to the source span.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="repository root")
    parser.add_argument("--output", help="optional JSON output path")
    parser.add_argument(
        "--fail-on-p0",
        action="store_true",
        help="exit nonzero when deterministic P0 findings exist",
    )
    args = parser.parse_args()

    report = run_audit(Path(args.root))
    payload = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
    else:
        print(payload)

    if args.fail_on_p0 and report["finding_counts"].get("P0", 0):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

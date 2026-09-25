"""Deterministic repository audit for Phase-II knowledge artifacts.

P0 = schema/provenance-control failure decided mechanically.
P1 = source-span review candidate; never proof that the domain claim is wrong.

The sixty-system v0.1 canonical file is intentionally kept immutable during A0.
v0.3 review metadata and schema repairs are applied as auditable sidecars.
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
    "define", "assert", "condition", "enhance", "weaken", "transform",
    "inhibit", "activate", "compare", "project", "gate", "couple",
}
RULE_STATE_CHANGES = {"none", "increase", "decrease", "transform", "nonlinear"}
RULE_VALENCE = {"favorable", "unfavorable", "context_dependent", "not_applicable"}

MODIFIER_OPERATORS = {
    "enhance", "weaken", "transform", "inhibit", "activate", "conditional",
    "projection", "structural_relation", "pair_interaction", "gate",
}

SOURCE_EPISTEMIC = {"EXPLICIT", "INFERRED_FROM_SOURCE", "UNRESOLVED_SOURCE"}
NORMALIZATION_EPISTEMIC = {
    "SOURCE_PRESERVING", "INFERRED", "IMPLEMENTATION", "HYPOTHESIS", "UNRESOLVED",
}
REVIEW_STATUS = {
    "MODEL_EXTRACTED", "MODEL_SELF_REVIEWED", "SOURCE_SPAN_VERIFIED", "HUMAN_VERIFIED",
}
BOOLEAN_TEXT = {"true", "false"}

V03_FIELDS = (
    "source_epistemic",
    "normalization_epistemic",
    "review_status",
    "reviewer_type",
    "reviewer_id",
    "reviewed_at",
    "source_span_verified",
    "normalization_verified",
    "normalization_rationale",
)

STAR_CATALOG = Path("knowledge/rules/stars/major_stars_canonical_v0.1.csv")
SYSTEM_CATALOG = Path("knowledge/rules/systems/sixty_systems_canonical_v0.1.csv")
SYSTEM_REVIEW = Path("knowledge/review/sixty_systems_review_v0.3.csv")
SYSTEM_OVERRIDES = Path("knowledge/migrations/a0_sixty_systems_schema_overrides_v0.1.csv")

MODIFIER_CATALOGS = (
    Path("knowledge/operators/auxiliary_eight_v0.1.csv"),
    Path("knowledge/operators/six_malefics_v0.1.csv"),
    Path("knowledge/operators/transformation_rules_v0.1.csv"),
    Path("knowledge/operators/misc_stars_v0.1.csv"),
)
DERIVED_CATALOGS = (Path("knowledge/operators/system_operator_edges_v0.1.csv"),)

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
    return (
        row.get("rule_id")
        or row.get("operator_rule_id")
        or row.get("edge_id")
        or row.get("source_rule_id")
        or ""
    )


def _p0(path: Path, row: Mapping[str, str], field: str, value: str, message: str) -> Finding:
    return Finding(
        "P0", "schema_v0.3", str(path), _id(row), field, value,
        row.get("source_location", ""), message,
    )


def duplicate_id_findings(path: Path, rows: Sequence[Mapping[str, str]]) -> list[Finding]:
    counts = Counter(_id(row) for row in rows if _id(row))
    return [
        Finding("P0", "duplicate_id", str(path), record_id, "id", str(count), "",
                f"ID appears {count} times.")
        for record_id, count in counts.items()
        if count > 1
    ]


def audit_review_fields(path: Path, rows: Sequence[Mapping[str, str]]) -> list[Finding]:
    findings: list[Finding] = []
    for row in rows:
        for field in V03_FIELDS:
            if field not in row:
                findings.append(_p0(path, row, field, "", "Missing v0.3 column."))
        if any(field not in row for field in V03_FIELDS):
            continue

        if row.get("source_epistemic", "") not in SOURCE_EPISTEMIC:
            findings.append(_p0(path, row, "source_epistemic", row.get("source_epistemic", ""),
                                "Invalid source_epistemic value."))
        if row.get("normalization_epistemic", "") not in NORMALIZATION_EPISTEMIC:
            findings.append(_p0(path, row, "normalization_epistemic",
                                row.get("normalization_epistemic", ""),
                                "Invalid normalization_epistemic value."))
        if row.get("review_status", "") not in REVIEW_STATUS:
            findings.append(_p0(path, row, "review_status", row.get("review_status", ""),
                                "Invalid review_status value."))
        for field in ("source_span_verified", "normalization_verified"):
            if row.get(field, "") not in BOOLEAN_TEXT:
                findings.append(_p0(path, row, field, row.get(field, ""),
                                    f"{field} must be true/false text."))

        if row.get("review_status") in {"MODEL_SELF_REVIEWED", "SOURCE_SPAN_VERIFIED", "HUMAN_VERIFIED"}:
            if not row.get("reviewer_type", "").strip():
                findings.append(_p0(path, row, "reviewer_type", "", "Reviewer type is required."))
            if not row.get("reviewer_id", "").strip():
                findings.append(_p0(path, row, "reviewer_id", "", "Reviewer id is required."))

        if row.get("review_status") in {"SOURCE_SPAN_VERIFIED", "HUMAN_VERIFIED"}:
            if row.get("source_span_verified") != "true":
                findings.append(_p0(
                    path, row, "source_span_verified", row.get("source_span_verified", ""),
                    "Verified review status requires source_span_verified=true.",
                ))

        if row.get("review_status") == "HUMAN_VERIFIED" and row.get("reviewer_type") == "MODEL":
            findings.append(_p0(
                path, row, "reviewer_type", row.get("reviewer_type", ""),
                "HUMAN_VERIFIED cannot be assigned by a model reviewer.",
            ))

        if row.get("normalization_epistemic") in {"INFERRED", "IMPLEMENTATION", "HYPOTHESIS"}:
            if not row.get("normalization_rationale", "").strip():
                findings.append(_p0(
                    path, row, "normalization_rationale", "",
                    "Non-source-preserving normalization requires a rationale.",
                ))
    return findings


def audit_rule_catalog(path: Path, rows: Sequence[Mapping[str, str]]) -> list[Finding]:
    findings = duplicate_id_findings(path, rows)
    findings.extend(audit_review_fields(path, rows))
    for row in rows:
        if row.get("target_type", "") not in RULE_TARGET_TYPES:
            findings.append(_p0(path, row, "target_type", row.get("target_type", ""),
                                "target_type is outside KB_SCHEMA.md controlled vocabulary."))
        if row.get("operator", "") not in RULE_OPERATORS:
            findings.append(_p0(path, row, "operator", row.get("operator", ""),
                                "operator is outside KB_SCHEMA.md controlled vocabulary."))
        if row.get("state_change", "") not in RULE_STATE_CHANGES:
            findings.append(_p0(path, row, "state_change", row.get("state_change", ""),
                                "state_change is outside KB_SCHEMA.md controlled vocabulary."))
        if row.get("valence", "") not in RULE_VALENCE:
            findings.append(_p0(path, row, "valence", row.get("valence", ""),
                                "valence is outside KB_SCHEMA.md controlled vocabulary."))
    return findings


def audit_modifier_catalog(path: Path, rows: Sequence[Mapping[str, str]]) -> list[Finding]:
    findings = duplicate_id_findings(path, rows)
    findings.extend(audit_review_fields(path, rows))
    for row in rows:
        if row.get("operator_type", "") not in MODIFIER_OPERATORS:
            findings.append(_p0(path, row, "operator_type", row.get("operator_type", ""),
                                "operator_type is outside operator_schema.yaml vocabulary."))
    return findings


def audit_derived_catalog(path: Path, rows: Sequence[Mapping[str, str]]) -> list[Finding]:
    findings = audit_review_fields(path, rows)
    for row in rows:
        if row.get("target_type", "") not in RULE_TARGET_TYPES:
            findings.append(_p0(path, row, "target_type", row.get("target_type", ""),
                                "Derived target_type is outside controlled vocabulary."))
        if row.get("operator", "") not in RULE_OPERATORS:
            findings.append(_p0(path, row, "operator", row.get("operator", ""),
                                "Derived operator is outside controlled vocabulary."))
    return findings


def effective_sixty_system_rows(root: Path) -> tuple[list[dict[str, str]], list[Finding]]:
    raw = read_csv(root / SYSTEM_CATALOG)
    review = read_csv(root / SYSTEM_REVIEW)
    overrides = read_csv(root / SYSTEM_OVERRIDES)
    findings: list[Finding] = []

    raw_by_id = {row["rule_id"]: dict(row) for row in raw}
    review_by_id = {row["rule_id"]: row for row in review}

    missing_review = set(raw_by_id) - set(review_by_id)
    extra_review = set(review_by_id) - set(raw_by_id)
    for rule_id in sorted(missing_review):
        findings.append(Finding(
            "P0", "review_sidecar", str(SYSTEM_REVIEW), rule_id, "rule_id", rule_id, "",
            "Canonical rule has no v0.3 review metadata.",
        ))
    for rule_id in sorted(extra_review):
        findings.append(Finding(
            "P0", "review_sidecar", str(SYSTEM_REVIEW), rule_id, "rule_id", rule_id, "",
            "Review metadata references an unknown canonical rule.",
        ))

    for rule_id, row in raw_by_id.items():
        if rule_id in review_by_id:
            row.update(review_by_id[rule_id])

    for patch in overrides:
        rule_id = patch.get("rule_id", "")
        field = patch.get("field", "")
        if rule_id not in raw_by_id:
            findings.append(Finding(
                "P0", "override_sidecar", str(SYSTEM_OVERRIDES), rule_id, field,
                patch.get("new_value", ""), "", "Override references unknown canonical rule.",
            ))
            continue
        row = raw_by_id[rule_id]
        if field not in {"target_type", "operator", "state_change", "valence"}:
            findings.append(Finding(
                "P0", "override_sidecar", str(SYSTEM_OVERRIDES), rule_id, field,
                patch.get("new_value", ""), row.get("source_location", ""),
                "A0 override field is not a controlled rule-schema field.",
            ))
            continue
        if row.get(field, "") != patch.get("old_value", ""):
            findings.append(Finding(
                "P0", "override_sidecar", str(SYSTEM_OVERRIDES), rule_id, field,
                patch.get("old_value", ""), row.get("source_location", ""),
                "Override old_value does not match raw canonical.",
            ))
            continue
        row[field] = patch.get("new_value", "")

    return list(raw_by_id.values()), findings


def composite_condition_score(condition: str) -> int:
    return sum(bool(pattern.search(condition or "")) for pattern in COMPOSITE_MARKERS)


def atomicity_candidates(path: Path, rows: Sequence[Mapping[str, str]]) -> list[Finding]:
    return [
        Finding(
            "P1", "atomicity_candidate", str(path), _id(row), "condition",
            row.get("condition", ""), row.get("source_location", ""),
            "Condition contains multiple composition markers; source-span review required.",
        )
        for row in rows
        if composite_condition_score(row.get("condition", "")) >= 2
    ]


def outcome_operator_candidates(path: Path, rows: Sequence[Mapping[str, str]]) -> list[Finding]:
    directional = {"enhance", "weaken", "transform", "inhibit", "activate"}
    return [
        Finding(
            "P1", "layer_boundary_candidate", str(path), _id(row), "operator",
            row.get("operator", ""), row.get("source_location", ""),
            "Outcome descriptor uses directional state operator; check L1/L2 -> L3 boundary.",
        )
        for row in rows
        if row.get("target_type") == "outcome_descriptor"
        and row.get("operator") in directional
    ]


def status_summary(rows: Iterable[Mapping[str, str]]) -> dict[str, int]:
    return dict(Counter(row.get("review_status", "") for row in rows))


def epistemic_summary(rows: Iterable[Mapping[str, str]]) -> dict[str, dict[str, int]]:
    rows = list(rows)
    return {
        "source": dict(Counter(row.get("source_epistemic", "") for row in rows)),
        "normalization": dict(Counter(row.get("normalization_epistemic", "") for row in rows)),
    }


def summarize(path: Path, rows: list[dict[str, str]]) -> dict:
    return {
        "records": len(rows),
        "review_status": status_summary(rows),
        "epistemic": epistemic_summary(rows),
    }


def run_audit(root: Path) -> dict:
    findings: list[Finding] = []
    summaries: dict[str, dict] = {}

    stars = read_csv(root / STAR_CATALOG)
    findings.extend(audit_rule_catalog(STAR_CATALOG, stars))
    findings.extend(atomicity_candidates(STAR_CATALOG, stars))
    findings.extend(outcome_operator_candidates(STAR_CATALOG, stars))
    summaries[str(STAR_CATALOG)] = summarize(STAR_CATALOG, stars)

    systems, sidecar_findings = effective_sixty_system_rows(root)
    findings.extend(sidecar_findings)
    findings.extend(audit_rule_catalog(SYSTEM_CATALOG, systems))
    findings.extend(atomicity_candidates(SYSTEM_CATALOG, systems))
    findings.extend(outcome_operator_candidates(SYSTEM_CATALOG, systems))
    summaries[str(SYSTEM_CATALOG)] = summarize(SYSTEM_CATALOG, systems)

    for relative in MODIFIER_CATALOGS:
        rows = read_csv(root / relative)
        findings.extend(audit_modifier_catalog(relative, rows))
        summaries[str(relative)] = summarize(relative, rows)

    for relative in DERIVED_CATALOGS:
        rows = read_csv(root / relative)
        findings.extend(audit_derived_catalog(relative, rows))
        summaries[str(relative)] = summarize(relative, rows)

    return {
        "summaries": summaries,
        "finding_counts": dict(Counter(item.severity for item in findings)),
        "findings": [asdict(item) for item in findings],
        "notes": [
            "P0 findings are deterministic schema/review-provenance violations.",
            "P1 findings are review candidates, not proof of semantic error.",
            "Sixty-system v0.1 raw canonical is immutable at A0; sidecars define effective v0.3 view.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="repository root")
    parser.add_argument("--output", help="optional JSON output path")
    parser.add_argument("--fail-on-p0", action="store_true")
    args = parser.parse_args()

    report = run_audit(Path(args.root))
    payload = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
    else:
        print(payload)

    return 2 if args.fail_on_p0 and report["finding_counts"].get("P0", 0) else 0


if __name__ == "__main__":
    raise SystemExit(main())

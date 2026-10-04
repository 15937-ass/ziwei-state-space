#!/usr/bin/env python3
"""Aggregate P1 B02-C matrix reports across bounded CI jobs."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


EXPECTED_BATCHES = {"P1-B02-C1", "P1-B02-C2", "P1-B02-C3"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("reports_root")
    ap.add_argument("--report", required=True)
    ap.add_argument("--require-full-decadal-coverage", action="store_true")
    args = ap.parse_args()

    paths = sorted(Path(args.reports_root).glob("**/p1_b02c_transition_report.json"))
    errors: list[str] = []
    reports: list[dict] = []
    for path in paths:
        try:
            reports.append(json.loads(path.read_text(encoding="utf-8")))
        except Exception as exc:
            errors.append(f"{path}: {exc}")

    batches = {r.get("batch") for r in reports}
    if batches != EXPECTED_BATCHES:
        errors.append(f"expected batches {sorted(EXPECTED_BATCHES)}, got {sorted(x for x in batches if x)}")

    all_seen: set[str] = set()
    changed_union: set[str] = set()
    change_count: Counter[str] = Counter()
    for report in reports:
        if report.get("structural_errors"):
            errors.append(f"{report.get('batch')}: structural_errors={report['structural_errors'][:3]}")
        if report.get("semantic_errors"):
            errors.append(f"{report.get('batch')}: semantic_errors={report['semantic_errors'][:3]}")

        coverage = report.get("year_transition_coverage", {})
        seen = coverage.get("per_case_year_pairs_seen", {})
        all_seen.update(seen)
        changed = set(coverage.get("case_ids_with_decadal_change", []))
        changed_union.update(changed)
        for cid, count in coverage.get("per_case_year_decadal_change_count", {}).items():
            change_count[cid] += int(count)

    zero_cases = sorted(all_seen - changed_union)
    distribution = Counter(change_count.get(cid, 0) for cid in all_seen)

    if len(all_seen) != 100:
        errors.append(f"expected 100 case IDs across reports, got {len(all_seen)}")
    if args.require_full_decadal_coverage and zero_cases:
        errors.append(f"decadal transition coverage missing {len(zero_cases)} cases: {zero_cases[:20]}")

    result = {
        "reports_found": len(paths),
        "batches": sorted(x for x in batches if x),
        "case_count": len(all_seen),
        "cases_with_at_least_one_decadal_transition": len(changed_union),
        "cases_without_decadal_transition": zero_cases,
        "decadal_transition_count_distribution": {
            str(k): v for k, v in sorted(distribution.items())
        },
        "semantic_assertions_all_clean": not any(r.get("semantic_errors") for r in reports),
        "structural_errors_all_clean": not any(r.get("structural_errors") for r in reports),
        "errors": errors,
    }

    Path(args.report).write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("P1 B02-C AGGREGATE")
    print(json.dumps(result, ensure_ascii=False, indent=2))

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Compare P1 full normalized outputs from two engines."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from src.product.chart_diff import compare_chart_snapshots


def load_jsonl(path: Path):
    rows = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        rows[row["case_id"]] = row
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("left")
    ap.add_argument("right")
    ap.add_argument("--report", required=True)
    ap.add_argument("--fail-on-diff", action="store_true")
    ap.add_argument("--max-total-diffs", type=int, default=500)
    ap.add_argument("--max-detail-per-case", type=int, default=100)
    args = ap.parse_args()

    left = load_jsonl(Path(args.left))
    right = load_jsonl(Path(args.right))
    ids = sorted(set(left) | set(right))

    details = []
    path_counts = Counter()
    severity_counts = Counter()
    cases_with_diffs = 0
    total_diffs = 0
    truncated = False

    for case_id in ids:
        if case_id not in left or case_id not in right:
            details.append({
                "case_id": case_id,
                "missing_engine_record": {
                    "left": case_id not in left,
                    "right": case_id not in right,
                },
            })
            cases_with_diffs += 1
            total_diffs += 1
            continue

        # Engine identity, chart contract ID and implementation entrypoint are
        # provenance metadata, not normalized chart facts. Keep school/config
        # metadata in the comparison so both engines must declare the same
        # Zhongzhou settings; production admission separately accepts iztro-js
        # only and rejects the x-iztro audit output.
        ignored_metadata_paths = ("engine", "chart_contract_id", "input.entrypoint")
        diffs = compare_chart_snapshots(
            left[case_id],
            right[case_id],
            ignore_paths=ignored_metadata_paths,
        )
        if diffs:
            cases_with_diffs += 1
            total_diffs += len(diffs)
            for d in diffs:
                path_counts[d.path] += 1
                severity_counts[d.severity] += 1
            details.append({
                "case_id": case_id,
                "differences": [
                    {
                        "path": d.path,
                        "left": d.left,
                        "right": d.right,
                        "category": d.category,
                        "severity": d.severity,
                    }
                    for d in diffs[: args.max_detail_per_case]
                ],
                "difference_count": len(diffs),
            })

        if total_diffs >= args.max_total_diffs:
            truncated = True
            break

    report = {
        "schema_version": "0.2",
        "left_engine": next(iter(left.values()))["engine"] if left else None,
        "right_engine": next(iter(right.values()))["engine"] if right else None,
        "case_count": len(ids),
        "temporal_targets_per_case": len(next(iter(left.values())).get("temporal", [])) if left else 0,
        "natal_snapshots_compared": len(ids),
        "horoscope_snapshots_compared": len(ids) * (len(next(iter(left.values())).get("temporal", [])) if left else 0),
        "cases_with_differences": cases_with_diffs,
        "total_differences": total_diffs,
        "exact_case_agreement_rate": (len(ids) - cases_with_diffs) / len(ids) if ids else 0,
        "severity_counts": dict(severity_counts),
        "top_difference_paths": path_counts.most_common(50),
        "details": details,
        "truncated_at_difference_cap": truncated,
        "max_total_diffs": args.max_total_diffs,
        "max_detail_per_case": args.max_detail_per_case,
        "ignored_metadata_paths": [
            "engine",
            "chart_contract_id",
            "input.entrypoint",
        ],
    }
    Path(args.report).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("P1 DUAL-ENGINE FULL DIFF")
    print(f"cases={report['case_count']}")
    print(f"natal={report['natal_snapshots_compared']}")
    print(f"horoscope={report['horoscope_snapshots_compared']}")
    print(f"cases_with_differences={cases_with_diffs}")
    print(f"total_differences={total_diffs}")
    print(f"exact_case_agreement_rate={report['exact_case_agreement_rate']:.6f}")
    if path_counts:
        print("top_difference_paths:")
        for path, count in path_counts.most_common(20):
            print(f"  {count:4d} {path}")

    if truncated:
        print(f"FAIL-FAST: difference cap reached ({args.max_total_diffs}); report is intentionally truncated")
        return 2
    if args.fail_on_diff and total_diffs:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

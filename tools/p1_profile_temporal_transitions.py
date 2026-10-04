#!/usr/bin/env python3
"""Profile P1 B02-C temporal transition boundaries.

This profiler is deliberately observational on its first pass: it records which
temporal scopes change across YEAR/MONTH/DAY boundary pairs and tracks nominal-age
and decadal coverage. Hard semantic assertions can then be frozen from the
observed, cross-engine-verified signature rather than invented in advance.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path


SCOPES = ("decadal", "age", "yearly", "monthly", "daily", "hourly")


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"malformed JSONL line {line_no}: {exc}") from exc
    return rows


def normalized_scope(scope: dict) -> dict:
    return {
        "index": scope.get("index"),
        "stem": scope.get("stem"),
        "branch": scope.get("branch"),
        "palace_names": scope.get("palace_names"),
        "mutagen": scope.get("mutagen"),
        "stars": scope.get("stars"),
        "nominal_age": scope.get("nominal_age"),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("engine_output")
    ap.add_argument("manifest")
    ap.add_argument("--report", required=True)
    ap.add_argument("--max-errors", type=int, default=10)
    args = ap.parse_args()

    rows = load_jsonl(Path(args.engine_output))
    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    pairs = manifest.get("transition_pairs", [])
    errors: list[str] = []

    if not pairs:
        errors.append("manifest contains no transition_pairs")

    pair_stats: dict[str, dict] = {}
    for pair in pairs:
        pid = pair.get("pair_id")
        kind = pair.get("kind")
        if not pid or kind not in {"YEAR", "MONTH", "DAY"} or not pair.get("left") or not pair.get("right"):
            errors.append(f"malformed transition pair: {pair}")
            continue
        pair_stats[pid] = {
            "kind": kind,
            "scope_relations": {scope: Counter() for scope in SCOPES},
            "changed_scope_patterns": Counter(),
            "age_nominal_delta": Counter(),
            "changed_fields": {scope: Counter() for scope in SCOPES},
        }

    year_decadal_changed_cases: set[str] = set()
    year_age_changed_cases: set[str] = set()
    per_case_year_decadal_changes: Counter[str] = Counter()
    per_case_year_pairs_seen: Counter[str] = Counter()
    examples: list[dict] = []

    for row in rows:
        cid = row.get("case_id")
        temporal = row.get("temporal", [])
        by_id = {
            item.get("target", {}).get("target_id"): item
            for item in temporal
            if item.get("target", {}).get("target_id")
        }

        for pair in pairs:
            if len(errors) >= args.max_errors:
                break
            pid = pair.get("pair_id")
            if pid not in pair_stats:
                continue

            left_id = pair["left"]
            right_id = pair["right"]
            left = by_id.get(left_id)
            right = by_id.get(right_id)
            if left is None or right is None:
                errors.append(f"{cid}: missing transition target {left_id} or {right_id}")
                continue

            changed_scopes: list[str] = []
            for scope_name in SCOPES:
                a0 = left.get("scopes", {}).get(scope_name)
                b0 = right.get("scopes", {}).get(scope_name)
                if a0 is None or b0 is None:
                    errors.append(f"{cid}: missing scope={scope_name} pair={pid}")
                    if len(errors) >= args.max_errors:
                        break
                    continue

                a = normalized_scope(a0)
                b = normalized_scope(b0)
                relation = "equal" if a == b else "different"
                pair_stats[pid]["scope_relations"][scope_name][relation] += 1

                if relation == "different":
                    changed_scopes.append(scope_name)
                    fields = [key for key in a if a.get(key) != b.get(key)]
                    for field in fields:
                        pair_stats[pid]["changed_fields"][scope_name][field] += 1
                    if len(examples) < 30:
                        examples.append({
                            "case_id": cid,
                            "pair_id": pid,
                            "kind": pair_stats[pid]["kind"],
                            "scope": scope_name,
                            "changed_fields": fields,
                        })

                if scope_name == "age":
                    av = a.get("nominal_age")
                    bv = b.get("nominal_age")
                    if isinstance(av, int) and isinstance(bv, int):
                        pair_stats[pid]["age_nominal_delta"][str(bv - av)] += 1

            pair_stats[pid]["changed_scope_patterns"]["|".join(changed_scopes) or "NONE"] += 1

            if pair_stats[pid]["kind"] == "YEAR":
                per_case_year_pairs_seen[cid] += 1
                left_dec = normalized_scope(left["scopes"]["decadal"])
                right_dec = normalized_scope(right["scopes"]["decadal"])
                if left_dec != right_dec:
                    year_decadal_changed_cases.add(cid)
                    per_case_year_decadal_changes[cid] += 1
                left_age = normalized_scope(left["scopes"]["age"])
                right_age = normalized_scope(right["scopes"]["age"])
                if left_age != right_age:
                    year_age_changed_cases.add(cid)

        if len(errors) >= args.max_errors:
            break

    serializable_pairs = {}
    for pid, stats in pair_stats.items():
        serializable_pairs[pid] = {
            "kind": stats["kind"],
            "scope_relations": {
                scope: dict(sorted(counter.items()))
                for scope, counter in stats["scope_relations"].items()
            },
            "changed_scope_patterns": dict(sorted(stats["changed_scope_patterns"].items())),
            "age_nominal_delta": dict(sorted(stats["age_nominal_delta"].items())),
            "changed_fields": {
                scope: dict(sorted(counter.items()))
                for scope, counter in stats["changed_fields"].items()
            },
        }

    report = {
        "batch": manifest.get("batch"),
        "manifest_version": manifest.get("version"),
        "records": len(rows),
        "transition_pair_count": len(pairs),
        "pair_stats": serializable_pairs,
        "year_transition_coverage": {
            "cases_with_decadal_change_in_this_manifest": len(year_decadal_changed_cases),
            "cases_with_age_scope_change_in_this_manifest": len(year_age_changed_cases),
            "case_ids_with_decadal_change": sorted(year_decadal_changed_cases),
            "per_case_year_decadal_change_count": dict(sorted(per_case_year_decadal_changes.items())),
            "per_case_year_pairs_seen": dict(sorted(per_case_year_pairs_seen.items())),
        },
        "examples": examples,
        "structural_errors": errors,
    }

    Path(args.report).write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("P1 B02-C TEMPORAL TRANSITION PROFILE")
    print(f"batch={report['batch']}")
    print(f"records={len(rows)} pairs={len(pairs)} structural_errors={len(errors)}")
    for pid, stats in serializable_pairs.items():
        print(f"PAIR {pid} kind={stats['kind']}")
        for scope in SCOPES:
            print(" ", scope, json.dumps(stats["scope_relations"][scope], ensure_ascii=False))
        if stats["age_nominal_delta"]:
            print("  age_nominal_delta", json.dumps(stats["age_nominal_delta"], ensure_ascii=False))
        print("  changed_patterns", json.dumps(stats["changed_scope_patterns"], ensure_ascii=False))
    print(
        "year_decadal_coverage=",
        len(year_decadal_changed_cases),
        "/",
        len(rows),
    )

    for item in errors[: args.max_errors]:
        print(" ", item)

    if len(errors) >= args.max_errors:
        print(f"FAIL-FAST: structural errors reached cap {args.max_errors}")
        return 2
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Profile and validate P1 B02-C temporal transition boundaries.

B02-C first observed the transition signatures, then freezes the stable
YEAR/MONTH/DAY locality invariants. It also checks that the selected decadal
scope is consistent with the natal decadal ranges whenever the target nominal
age falls inside exactly one such range.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
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


def decadal_matches_for_age(row: dict, nominal_age: int) -> list[dict]:
    matches: list[dict] = []
    for palace_branch, palace in row.get("natal", {}).get("palaces", {}).items():
        dec = palace.get("decadal")
        if not dec:
            continue
        rng = dec.get("range")
        if not isinstance(rng, list) or len(rng) != 2:
            continue
        lo, hi = rng
        if isinstance(lo, int) and isinstance(hi, int) and lo <= nominal_age <= hi:
            matches.append({
                "palace_branch": palace_branch,
                "stem": dec.get("stem"),
                "branch": dec.get("branch"),
                "range": rng,
            })
    return matches


def only_relation(counter: Counter, relation: str, n: int) -> bool:
    return counter.get(relation, 0) == n and sum(counter.values()) == n


def validate_pair_semantics(pid: str, stats: dict, n: int) -> list[str]:
    kind = stats["kind"]
    rel = stats["scope_relations"]
    delta = stats["age_nominal_delta"]
    patterns = stats["changed_scope_patterns"]
    errors: list[str] = []

    def expect(scope: str, relation: str) -> None:
        if not only_relation(rel[scope], relation, n):
            errors.append(
                f"{pid}: expected {scope}={relation} for all {n}, got {dict(rel[scope])}"
            )

    if kind == "YEAR":
        for scope in ("age", "yearly", "monthly", "daily", "hourly"):
            expect(scope, "different")
        if delta.get("1", 0) != n or sum(delta.values()) != n:
            errors.append(f"{pid}: expected age nominal delta +1 for all {n}, got {dict(delta)}")
        allowed = {
            "age|yearly|monthly|daily|hourly",
            "decadal|age|yearly|monthly|daily|hourly",
        }
        if set(patterns) - allowed or sum(patterns.values()) != n:
            errors.append(f"{pid}: unexpected YEAR changed-scope patterns {dict(patterns)}")
    elif kind == "MONTH":
        for scope in ("decadal", "age", "yearly"):
            expect(scope, "equal")
        for scope in ("monthly", "daily", "hourly"):
            expect(scope, "different")
        if delta.get("0", 0) != n or sum(delta.values()) != n:
            errors.append(f"{pid}: expected age nominal delta 0 for all {n}, got {dict(delta)}")
        if patterns != Counter({"monthly|daily|hourly": n}):
            errors.append(f"{pid}: unexpected MONTH changed-scope patterns {dict(patterns)}")
    elif kind == "DAY":
        for scope in ("decadal", "age", "yearly", "monthly"):
            expect(scope, "equal")
        for scope in ("daily", "hourly"):
            expect(scope, "different")
        if delta.get("0", 0) != n or sum(delta.values()) != n:
            errors.append(f"{pid}: expected age nominal delta 0 for all {n}, got {dict(delta)}")
        if patterns != Counter({"daily|hourly": n}):
            errors.append(f"{pid}: unexpected DAY changed-scope patterns {dict(patterns)}")

    return errors


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("engine_output")
    ap.add_argument("manifest")
    ap.add_argument("--report", required=True)
    ap.add_argument("--max-errors", type=int, default=10)
    ap.add_argument("--assert-semantics", action="store_true")
    args = ap.parse_args()

    rows = load_jsonl(Path(args.engine_output))
    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    pairs = manifest.get("transition_pairs", [])
    structural_errors: list[str] = []
    semantic_errors: list[str] = []

    if not pairs:
        structural_errors.append("manifest contains no transition_pairs")

    pair_stats: dict[str, dict] = {}
    for pair in pairs:
        pid = pair.get("pair_id")
        kind = pair.get("kind")
        if not pid or kind not in {"YEAR", "MONTH", "DAY"} or not pair.get("left") or not pair.get("right"):
            structural_errors.append(f"malformed transition pair: {pair}")
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

    range_checkable_targets = 0
    range_unmatched_targets = 0
    range_ambiguous_targets = 0
    range_actual_mismatch = 0
    range_transition_checks = 0
    range_transition_mismatches = 0
    range_unmatched_by_case: Counter[str] = Counter()

    for row in rows:
        cid = row.get("case_id")
        temporal = row.get("temporal", [])
        by_id = {
            item.get("target", {}).get("target_id"): item
            for item in temporal
            if item.get("target", {}).get("target_id")
        }

        # Target-level invariant: when a nominal age maps to exactly one natal
        # decadal range, the active decadal stem/branch must match that range.
        target_range_keys: dict[str, tuple | None] = {}
        for tid, item in by_id.items():
            age_scope = item.get("scopes", {}).get("age", {})
            nominal_age = age_scope.get("nominal_age")
            if not isinstance(nominal_age, int):
                target_range_keys[tid] = None
                continue
            matches = decadal_matches_for_age(row, nominal_age)
            if len(matches) == 0:
                range_unmatched_targets += 1
                range_unmatched_by_case[cid] += 1
                target_range_keys[tid] = None
            elif len(matches) > 1:
                range_ambiguous_targets += 1
                target_range_keys[tid] = None
                if args.assert_semantics:
                    semantic_errors.append(
                        f"{cid}/{tid}: nominal_age={nominal_age} matches multiple natal decadal ranges"
                    )
            else:
                match = matches[0]
                key = (match["palace_branch"], match["stem"], match["branch"], tuple(match["range"]))
                target_range_keys[tid] = key
                range_checkable_targets += 1
                actual = item.get("scopes", {}).get("decadal", {})
                if actual.get("stem") != match["stem"] or actual.get("branch") != match["branch"]:
                    range_actual_mismatch += 1
                    if args.assert_semantics:
                        semantic_errors.append(
                            f"{cid}/{tid}: active decadal {actual.get('stem')}{actual.get('branch')} "
                            f"!= natal-range {match['stem']}{match['branch']} age={nominal_age} range={match['range']}"
                        )

        for pair in pairs:
            if len(structural_errors) >= args.max_errors:
                break
            pid = pair.get("pair_id")
            if pid not in pair_stats:
                continue

            left_id = pair["left"]
            right_id = pair["right"]
            left = by_id.get(left_id)
            right = by_id.get(right_id)
            if left is None or right is None:
                structural_errors.append(f"{cid}: missing transition target {left_id} or {right_id}")
                continue

            changed_scopes: list[str] = []
            for scope_name in SCOPES:
                a0 = left.get("scopes", {}).get(scope_name)
                b0 = right.get("scopes", {}).get(scope_name)
                if a0 is None or b0 is None:
                    structural_errors.append(f"{cid}: missing scope={scope_name} pair={pid}")
                    if len(structural_errors) >= args.max_errors:
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
                actual_changed = left_dec != right_dec
                if actual_changed:
                    year_decadal_changed_cases.add(cid)
                    per_case_year_decadal_changes[cid] += 1

                left_key = target_range_keys.get(left_id)
                right_key = target_range_keys.get(right_id)
                if left_key is not None and right_key is not None:
                    range_transition_checks += 1
                    expected_changed = left_key != right_key
                    if expected_changed != actual_changed:
                        range_transition_mismatches += 1
                        if args.assert_semantics:
                            semantic_errors.append(
                                f"{cid}/{pid}: decadal transition actual={actual_changed} "
                                f"expected_from_natal_ranges={expected_changed}"
                            )

                if normalized_scope(left["scopes"]["age"]) != normalized_scope(right["scopes"]["age"]):
                    year_age_changed_cases.add(cid)

        if len(structural_errors) >= args.max_errors:
            break

    if args.assert_semantics and not structural_errors:
        for pid, stats in pair_stats.items():
            semantic_errors.extend(validate_pair_semantics(pid, stats, len(rows)))

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
        "semantic_assertions_enabled": args.assert_semantics,
        "pair_stats": serializable_pairs,
        "year_transition_coverage": {
            "cases_with_decadal_change_in_this_manifest": len(year_decadal_changed_cases),
            "cases_with_age_scope_change_in_this_manifest": len(year_age_changed_cases),
            "case_ids_with_decadal_change": sorted(year_decadal_changed_cases),
            "per_case_year_decadal_change_count": dict(sorted(per_case_year_decadal_changes.items())),
            "per_case_year_pairs_seen": dict(sorted(per_case_year_pairs_seen.items())),
        },
        "decadal_range_consistency": {
            "checkable_targets": range_checkable_targets,
            "unmatched_targets": range_unmatched_targets,
            "ambiguous_targets": range_ambiguous_targets,
            "active_scope_mismatches": range_actual_mismatch,
            "transition_checks": range_transition_checks,
            "transition_mismatches": range_transition_mismatches,
            "unmatched_case_ids": sorted(range_unmatched_by_case),
            "unmatched_targets_by_case": dict(sorted(range_unmatched_by_case.items())),
        },
        "examples": examples,
        "structural_errors": structural_errors,
        "semantic_errors": semantic_errors,
    }

    Path(args.report).write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("P1 B02-C TEMPORAL TRANSITION PROFILE")
    print(f"batch={report['batch']}")
    print(
        f"records={len(rows)} pairs={len(pairs)} "
        f"structural_errors={len(structural_errors)} semantic_errors={len(semantic_errors)}"
    )
    for pid, stats in serializable_pairs.items():
        print(f"PAIR {pid} kind={stats['kind']}")
        for scope in SCOPES:
            print(" ", scope, json.dumps(stats["scope_relations"][scope], ensure_ascii=False))
        if stats["age_nominal_delta"]:
            print("  age_nominal_delta", json.dumps(stats["age_nominal_delta"], ensure_ascii=False))
        print("  changed_patterns", json.dumps(stats["changed_scope_patterns"], ensure_ascii=False))
    print("decadal_range_consistency=", json.dumps(report["decadal_range_consistency"], ensure_ascii=False))
    print("year_decadal_coverage=", len(year_decadal_changed_cases), "/", len(rows))

    all_errors = structural_errors + semantic_errors
    for item in all_errors[: args.max_errors]:
        print(" ", item)

    if len(all_errors) >= args.max_errors:
        print(f"FAIL-FAST: errors reached cap {args.max_errors}")
        return 2
    return 1 if all_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

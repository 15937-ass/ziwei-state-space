#!/usr/bin/env python3
"""Profile late-Zi boundary relations under the canonical Zhongzhou v1.1 policy.

The canonical production choice is day_divide=current: late Zi remains on the
supplied date. This tool records temporal relation signatures descriptively;
cross-school differences remain diagnostic and are not production alternatives.
It fails only on structural problems (missing targets/scopes or malformed probes).
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def load_jsonl(path: Path) -> list[dict]:
    rows = []
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
    ap.add_argument("--report")
    ap.add_argument("--max-errors", type=int, default=10)
    args = ap.parse_args()

    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    rows = load_jsonl(Path(args.engine_output))
    probes = manifest.get("relation_probes", [])
    errors: list[str] = []
    relation_counts: dict[str, Counter[str]] = {}
    examples: list[dict] = []

    if not probes:
        errors.append("manifest contains no relation_probes")

    for probe in probes:
        pid = probe.get("probe_id")
        if not pid or not probe.get("left") or not probe.get("right") or not probe.get("scopes"):
            errors.append(f"malformed relation probe: {probe}")
            continue
        relation_counts[pid] = Counter()

    for row in rows:
        cid = row.get("case_id")
        by_id = {item["target"]["target_id"]: item for item in row.get("temporal", [])}

        for probe in probes:
            if len(errors) >= args.max_errors:
                break

            pid = probe.get("probe_id")
            left_id = probe.get("left")
            right_id = probe.get("right")
            scopes = probe.get("scopes", [])
            if not pid or not left_id or not right_id or not scopes:
                continue

            left = by_id.get(left_id)
            right = by_id.get(right_id)
            if left is None or right is None:
                errors.append(f"{cid}: missing probe target {left_id} or {right_id}")
                continue

            for scope_name in scopes:
                left_scope = left.get("scopes", {}).get(scope_name)
                right_scope = right.get("scopes", {}).get(scope_name)
                if left_scope is None or right_scope is None:
                    errors.append(
                        f"{cid}: missing scope={scope_name} for probe={pid}"
                    )
                    if len(errors) >= args.max_errors:
                        break
                    continue

                a = normalized_scope(left_scope)
                b = normalized_scope(right_scope)
                relation = "equal" if a == b else "different"
                relation_counts[pid][f"{scope_name}:{relation}"] += 1

                if relation == "different" and len(examples) < 20:
                    changed_fields = [
                        key for key in a
                        if a.get(key) != b.get(key)
                    ]
                    examples.append({
                        "case_id": cid,
                        "probe_id": pid,
                        "scope": scope_name,
                        "relation": relation,
                        "changed_fields": changed_fields,
                    })

        if len(errors) >= args.max_errors:
            break

    report = {
        "batch": manifest.get("batch"),
        "manifest_version": manifest.get("version"),
        "classification": manifest.get("semantic_policy", {}).get("classification"),
        "records": len(rows),
        "strict_universal_equivalence": False,
        "school_sensitive_target_ids": manifest.get("school_sensitive_target_ids", []),
        "relation_counts": {
            pid: dict(sorted(counter.items()))
            for pid, counter in sorted(relation_counts.items())
        },
        "examples": examples,
        "structural_errors": errors,
        "downstream_inference": manifest.get("semantic_policy", {}).get("downstream_inference"),
    }

    print("P1 B02-B ZI/DAY SEMANTIC PROFILE")
    print(f"records={len(rows)}")
    print("policy=Zhongzhou canonical same-day; relation probes are descriptive, cross-school differences are diagnostic only")
    for pid, counter in sorted(relation_counts.items()):
        print(pid, json.dumps(dict(sorted(counter.items())), ensure_ascii=False))
    print(f"structural_errors={len(errors)}")
    for item in errors[: args.max_errors]:
        print(" ", item)

    if args.report:
        Path(args.report).write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    if len(errors) >= args.max_errors:
        print(f"FAIL-FAST: structural errors reached cap {args.max_errors}")
        return 2
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

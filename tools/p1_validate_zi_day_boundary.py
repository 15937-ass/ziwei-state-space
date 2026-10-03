#!/usr/bin/env python3
"""Validate late-Zi forward-day temporal semantics for P1 B02-B."""

from __future__ import annotations

import argparse
import json
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
    # Compare actual temporal calculation, not display-only naming.
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
    ap.add_argument("--max-errors", type=int, default=10)
    args = ap.parse_args()

    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    rows = load_jsonl(Path(args.engine_output))
    errors: list[str] = []

    for row in rows:
        cid = row.get("case_id")
        by_id = {item["target"]["target_id"]: item for item in row.get("temporal", [])}

        for rule in manifest.get("effective_equivalence", []):
            left = by_id.get(rule["left"])
            right = by_id.get(rule["right"])
            if left is None or right is None:
                errors.append(f"{cid}: missing equivalence target {rule['left']} or {rule['right']}")
                continue
            for scope_name in rule["scopes"]:
                a = normalized_scope(left["scopes"][scope_name])
                b = normalized_scope(right["scopes"][scope_name])
                if a != b:
                    errors.append(
                        f"{cid}: forward-day equivalence failed "
                        f"{rule['left']} != {rule['right']} at scope={scope_name}"
                    )
                    if len(errors) >= args.max_errors:
                        break
            if len(errors) >= args.max_errors:
                break

        if len(errors) >= args.max_errors:
            break

        for rule in manifest.get("change_expectations", []):
            left = by_id.get(rule["left"])
            right = by_id.get(rule["right"])
            if left is None or right is None:
                errors.append(f"{cid}: missing change target {rule['left']} or {rule['right']}")
                continue
            for scope_name in rule["scopes"]:
                a = normalized_scope(left["scopes"][scope_name])
                b = normalized_scope(right["scopes"][scope_name])
                if a == b:
                    errors.append(
                        f"{cid}: expected boundary transition absent "
                        f"{rule['left']} == {rule['right']} at scope={scope_name}"
                    )
                    if len(errors) >= args.max_errors:
                        break
            if len(errors) >= args.max_errors:
                break

        if len(errors) >= args.max_errors:
            break

    print("P1 B02-B ZI/DAY SEMANTIC CHECK")
    print(f"records={len(rows)}")
    print(f"errors={len(errors)}")
    for item in errors[: args.max_errors]:
        print(" ", item)

    if len(errors) >= args.max_errors:
        print(f"FAIL-FAST: semantic errors reached cap {args.max_errors}")
        return 2
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

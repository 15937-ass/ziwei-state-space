#!/usr/bin/env python3
"""Validate B02 target manifests and lunar markers in normalized engine output."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise SystemExit(f"malformed JSONL at line {line_no}: {exc}") from exc
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("engine_output")
    ap.add_argument("manifest")
    ap.add_argument("--max-errors", type=int, default=10)
    ap.add_argument("--max-targets", type=int, default=8)
    args = ap.parse_args()

    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    targets = manifest.get("targets", [])
    if not targets:
        print("ERROR: manifest has no targets")
        return 2
    if len(targets) > args.max_targets:
        print(f"ERROR: target count {len(targets)} exceeds hard cap {args.max_targets}")
        return 2

    expected = {t["target_id"]: t.get("expected_lunar_marker") for t in targets}
    rows = load_jsonl(Path(args.engine_output))
    errors = []

    for row in rows:
        by_id = {x["target"]["target_id"]: x for x in row.get("temporal", [])}
        for target_id, marker in expected.items():
            if target_id not in by_id:
                errors.append(f"{row.get('case_id')}: missing target {target_id}")
            elif marker and marker not in str(by_id[target_id].get("lunar_date", "")):
                errors.append(
                    f"{row.get('case_id')}:{target_id}: lunar_date={by_id[target_id].get('lunar_date')!r} "
                    f"does not contain expected marker {marker!r}"
                )
            if len(errors) >= args.max_errors:
                print(f"FAIL-FAST: boundary expectation errors reached cap {args.max_errors}")
                for item in errors:
                    print(" ", item)
                return 2

    print("P1 B02 BOUNDARY EXPECTATION CHECK")
    print(f"records={len(rows)}")
    print(f"targets={len(targets)}")
    print(f"errors={len(errors)}")
    for item in errors:
        print(" ", item)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

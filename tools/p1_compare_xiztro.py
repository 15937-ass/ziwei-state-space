#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from x_iztro import Astro
from x_iztro.config import ChartConfig

input_csv = Path(sys.argv[1] if len(sys.argv) > 1 else "validation/product_chart_regression/regression_inputs_v0.1.csv")
js_jsonl = Path(sys.argv[2] if len(sys.argv) > 2 else "/tmp/p1_iztro_js.jsonl")
mismatch_jsonl = Path(sys.argv[3] if len(sys.argv) > 3 else "/tmp/p1_mismatches.jsonl")

def load_inputs() -> dict[str, dict[str, str]]:
    with input_csv.open(encoding="utf-8", newline="") as f:
        return {r["case_id"]: r for r in csv.DictReader(f)}

def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def _canonical_scalar(value: Any, path: str) -> Any:
    # iztro JS serializes dates as YYYY-M-D while x-iztro preserves/normalizes
    # zero padding in some paths. Compare semantic date value, not display formatting.
    if path.endswith("solarDate") and isinstance(value, str):
        parts = value.split("-")
        if len(parts) == 3 and all(part.isdigit() for part in parts):
            return tuple(int(part) for part in parts)
    return value


NON_COMPUTATIONAL_PATHS = {"copyright"}

def compare_js_keys(js: Any, other: Any, path: str = "") -> list[dict[str, Any]]:
    if path in NON_COMPUTATIONAL_PATHS:
        return []
    out: list[dict[str, Any]] = []
    if isinstance(js, dict):
        if not isinstance(other, dict):
            return [{"path": path, "js": js, "x": other, "reason": "type"}]
        for key, value in js.items():
            p = f"{path}.{key}" if path else key
            if key not in other:
                out.append({"path": p, "js": value, "x": None, "reason": "missing_key"})
            else:
                out.extend(compare_js_keys(value, other[key], p))
        return out
    if isinstance(js, list):
        if not isinstance(other, list):
            return [{"path": path, "js": js, "x": other, "reason": "type"}]
        if len(js) != len(other):
            out.append({"path": path + ".length", "js": len(js), "x": len(other), "reason": "length"})
        for i, (a, b) in enumerate(zip(js, other)):
            out.extend(compare_js_keys(a, b, f"{path}[{i}]"))
        return out
    cjs = _canonical_scalar(js, path)
    cother = _canonical_scalar(other, path)
    if cjs != cother:
        out.append({"path": path, "js": js, "x": other, "reason": "value"})
    return out

inputs = load_inputs()
astro = Astro()
mismatch_count = 0
record_mismatch_count = 0
path_counts: Counter[str] = Counter()
kind_counts: Counter[str] = Counter()
scope_counts: Counter[str] = Counter()
natal_records = 0
horoscope_records = 0
checked_horoscope_layers = Counter()

with js_jsonl.open(encoding="utf-8") as src, mismatch_jsonl.open("w", encoding="utf-8") as mout:
    for line in src:
        rec = json.loads(line)
        row = inputs[rec["case_id"]]
        cfg = ChartConfig(
            algorithm=row["algorithm"],
            day_divide=row["day_divide"],
            year_divide=row["year_divide"],
            horoscope_divide=row["horoscope_divide"],
            age_divide="normal",
            astro_type="heaven",
        )
        chart = astro.by_solar(
            row["solar_date"],
            int(row["time_index"]),
            row["gender"],
            fix_leap=row["fix_leap"].lower() == "true",
            language="zh-CN",
            config=cfg,
        )
        if rec["kind"] == "natal":
            other = chart.to_dict()
            natal_records += 1
        else:
            other = chart.horoscope(rec["target_date"], int(rec["target_time_index"])).to_dict()
            horoscope_records += 1
            for scope in ("decadal", "age", "yearly", "monthly", "daily", "hourly"):
                if scope in rec["payload"]:
                    checked_horoscope_layers[scope] += 1

        diffs = compare_js_keys(rec["payload"], other)
        if diffs:
            record_mismatch_count += 1
            mismatch_count += len(diffs)
            kind_counts[rec["kind"]] += len(diffs)
            for d in diffs:
                path_counts[d["path"]] += 1
                if rec["kind"] == "horoscope":
                    scope = d["path"].split(".", 1)[0]
                    scope_counts[scope] += 1
            mout.write(json.dumps({
                "case_id": rec["case_id"],
                "kind": rec["kind"],
                "target_date": rec.get("target_date"),
                "target_time_index": rec.get("target_time_index"),
                "diffs": diffs[:100],
                "diff_count": len(diffs),
            }, ensure_ascii=False) + "\n")

summary = {
    "comparison": "iztro-js-2.6.1 vs x-iztro-python-0.6.1",
    "algorithm": "zhongzhou",
    "natal_records": natal_records,
    "horoscope_records": horoscope_records,
    "total_records": natal_records + horoscope_records,
    "horoscope_layers_checked": dict(checked_horoscope_layers),
    "records_with_mismatch": record_mismatch_count,
    "field_mismatch_count": mismatch_count,
    "mismatch_by_kind": dict(kind_counts),
    "mismatch_by_scope": dict(scope_counts),
    "top_mismatch_paths": path_counts.most_common(25),
    "js_output_sha256": digest(js_jsonl),
    "mismatch_file_sha256": digest(mismatch_jsonl),
}
print("P1_CROSSCHECK_SUMMARY=" + json.dumps(summary, ensure_ascii=False, sort_keys=True))

if mismatch_count:
    print("P1_CROSSCHECK_FAILED: mismatches found", file=sys.stderr)
    sys.exit(2)
print("P1_CROSSCHECK_PASS: zero mismatches across all JS keys")

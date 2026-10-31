#!/usr/bin/env python3
"""Validate natal late-/early-Zi date attribution under Zhongzhou contract v1.1.

For each same-date/same-gender seed group, time_index 0 (00:00-00:59),
6 (daytime control), and 12 (23:00-23:59) must retain the same supplied
solar/lunar date. The hour branch may change the chart; it must not silently
move the birth date across midnight.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
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


def validate(rows: list[dict]) -> list[str]:
    errors: list[str] = []
    groups: dict[tuple[str, str], dict[int, dict]] = defaultdict(dict)

    for row in rows:
        case_id = row.get("case_id")
        input_data = row.get("input") or {}
        solar_date = input_data.get("solar_date")
        gender = input_data.get("gender")
        time_index = input_data.get("time_index")

        if input_data.get("time_basis") != "true_solar_time":
            errors.append(f"{case_id}: input.time_basis must be true_solar_time")
        if input_data.get("location_correction_applied") is not False:
            errors.append(f"{case_id}: location_correction_applied must be false")
        if input_data.get("day_divide") != "current":
            errors.append(f"{case_id}: day_divide must be current")
        if not isinstance(solar_date, str) or not isinstance(gender, str):
            errors.append(f"{case_id}: missing solar_date or gender")
            continue
        if isinstance(time_index, bool) or not isinstance(time_index, int):
            errors.append(f"{case_id}: time_index must be an integer")
            continue
        groups[(solar_date, gender)][time_index] = row

    checked = 0
    for (solar_date, gender), by_time in sorted(groups.items()):
        required = (0, 6, 12)
        if not all(index in by_time for index in required):
            continue
        lunar_dates = {
            index: (by_time[index].get("natal") or {}).get("lunar_date")
            for index in required
        }
        if any(not isinstance(value, str) or not value for value in lunar_dates.values()):
            errors.append(f"{solar_date}/{gender}: missing natal lunar_date in Zi boundary group")
            continue
        if len(set(lunar_dates.values())) != 1:
            errors.append(
                f"{solar_date}/{gender}: same supplied date has inconsistent lunar dates "
                f"across early-Zi/daytime/late-Zi: {lunar_dates}"
            )
        checked += 1

    if checked == 0:
        errors.append("no complete same-date/same-gender groups for time_index 0, 6, 12")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("engine_output")
    parser.add_argument("--report")
    parser.add_argument("--max-errors", type=int, default=20)
    args = parser.parse_args()

    rows = load_jsonl(Path(args.engine_output))
    errors = validate(rows)
    report = {
        "contract": "ZHONGZHOU_IZTRO_JS_2_6_1_V1_1",
        "policy": "day_divide=current",
        "input_time_basis": "true_solar_time",
        "records": len(rows),
        "same_date_gender_groups_checked": sum(
            1
            for key in {
                ((row.get("input") or {}).get("solar_date"), (row.get("input") or {}).get("gender"))
                for row in rows
            }
            if all(
                any(
                    (item.get("input") or {}).get("solar_date") == key[0]
                    and (item.get("input") or {}).get("gender") == key[1]
                    and (item.get("input") or {}).get("time_index") == idx
                    for item in rows
                )
                for idx in (0, 6, 12)
            )
        ),
        "errors": errors[: args.max_errors],
        "error_count": len(errors),
    }
    print("P1 ZHONGZHOU NATAL ZI-DAY BOUNDARY")
    print(f"records={len(rows)}")
    print(f"same_date_gender_groups_checked={report['same_date_gender_groups_checked']}")
    print(f"errors={len(errors)}")
    for error in errors[: args.max_errors]:
        print(" ", error)
    if args.report:
        Path(args.report).write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    if len(errors) >= args.max_errors:
        print(f"FAIL-FAST: errors reached cap {args.max_errors}")
        return 2
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

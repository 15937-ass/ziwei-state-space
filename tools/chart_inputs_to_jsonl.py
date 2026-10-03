#!/usr/bin/env python3
"""Convert product chart-regression seed CSV to adapter JSONL input."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.product.regression_cases import load_regression_inputs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_csv")
    parser.add_argument("output_jsonl")
    args = parser.parse_args()

    rows = load_regression_inputs(args.input_csv)
    output = Path(args.output_jsonl)
    with output.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row.as_export_dict(), ensure_ascii=False) + "\n")
    print(f"wrote {len(rows)} inputs to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

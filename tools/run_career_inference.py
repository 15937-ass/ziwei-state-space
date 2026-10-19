#!/usr/bin/env python3
"""Run the canonical Career inference slice and emit a deterministic JSON report."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from src.product.career_inference_report import build_career_inference_report
from src.product.career_inference_service import run_career_inference
from src.product.temporal_environment import TEMPORAL_LAYERS


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LAYERS = ("DECADE", "YEAR")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run source-traceable Career NATAL inference with selected temporal "
            "context and emit a Chinese JSON report."
        )
    )
    parser.add_argument("--snapshot", required=True, help="normalized full-chart JSON snapshot")
    parser.add_argument("--target-id", required=True, help="temporal target ID in the snapshot")
    parser.add_argument("--question", required=True, help="question recorded in the inference report")
    parser.add_argument(
        "--temporal-layers",
        nargs="+",
        choices=sorted(TEMPORAL_LAYERS),
        default=list(DEFAULT_LAYERS),
        help="selected temporal layers (default: DECADE YEAR)",
    )
    parser.add_argument(
        "--repo-root",
        default=str(ROOT),
        help="repository root containing Product registries (default: repository root)",
    )
    parser.add_argument(
        "--output",
        help="optional output JSON path; omit to write the report to stdout",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    snapshot_path = Path(args.snapshot)
    output_path = Path(args.output) if args.output else None

    try:
        if output_path is not None and snapshot_path.resolve() == output_path.resolve():
            raise ValueError("output path must not overwrite the input snapshot")

        with snapshot_path.open("r", encoding="utf-8") as handle:
            snapshot = json.load(handle)
        if not isinstance(snapshot, dict):
            raise ValueError("snapshot JSON root must be an object")

        run = run_career_inference(
            args.repo_root,
            snapshot,
            target_id=args.target_id,
            question=args.question,
            selected_temporal_layers=args.temporal_layers,
        )
        report = build_career_inference_report(args.repo_root, run)
        serialized = json.dumps(
            report,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        ) + "\n"

        if output_path is None:
            sys.stdout.write(serialized)
        else:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(serialized, encoding="utf-8")
            print(f"Wrote Career inference report: {output_path}")
        return 0
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

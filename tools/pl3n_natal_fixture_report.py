#!/usr/bin/env python3
import json
from dataclasses import asdict
from pathlib import Path

from src.product.natal_fixture_benchmark import run_natal_fixture_benchmark


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "product/PL3N_NATAL_FIXTURES_v0.1.json"


def main():
    results = run_natal_fixture_benchmark(ROOT, FIXTURES)
    print(json.dumps(
        [asdict(item) for item in results],
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    ))


if __name__ == "__main__":
    main()

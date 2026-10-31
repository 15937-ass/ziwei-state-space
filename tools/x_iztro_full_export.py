#!/usr/bin/env python3
"""P1 full exporter for x-iztro 0.6.1 (Rust core / Python binding)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from x_iztro import Astro, ChartConfig, __version__


def normalize_solar_date(value):
    parts = str(value).split("-")
    if len(parts) != 3:
        return str(value)
    return f"{int(parts[0]):04d}-{int(parts[1]):02d}-{int(parts[2]):02d}"


def stable_stars(stars):
    rows = [
        {
            "name": s.get("name"),
            "type": s.get("type"),
            "brightness": s.get("brightness"),
            "mutagen": s.get("mutagen"),
            "scope": s.get("scope"),
        }
        for s in (stars or [])
    ]
    return sorted(rows, key=lambda x: json.dumps(x, ensure_ascii=False, sort_keys=True))


def stable_flow_stars(groups):
    return [
        sorted(
            [{"name": s.get("name"), "type": s.get("type")} for s in (group or [])],
            key=lambda x: json.dumps(x, ensure_ascii=False, sort_keys=True),
        )
        for group in (groups or [])
    ]


def normalize_natal(raw):
    palaces = {}
    for p in raw.get("palaces", []):
        palaces[p["earthlyBranch"]] = {
            "name": p["name"],
            "stem": p["heavenlyStem"],
            "branch": p["earthlyBranch"],
            "is_body_palace": bool(p.get("isBodyPalace")),
            "major_stars": stable_stars(p.get("majorStars")),
            "minor_stars": stable_stars(p.get("minorStars")),
            "adjective_stars": stable_stars(p.get("adjectiveStars")),
            "decadal": (
                {
                    "range": p["decadal"]["range"],
                    "stem": p["decadal"]["heavenlyStem"],
                    "branch": p["decadal"]["earthlyBranch"],
                }
                if p.get("decadal")
                else None
            ),
        }
    return {
        "solar_date": normalize_solar_date(raw["solarDate"]),
        "lunar_date": raw["lunarDate"],
        "chinese_date": raw["chineseDate"],
        "time": raw["time"],
        "time_range": raw["timeRange"],
        "soul_star": raw["soul"],
        "body_star": raw["body"],
        "five_elements_class": raw["fiveElementsClass"],
        "soul_palace_branch": raw["earthlyBranchOfSoulPalace"],
        "body_palace_branch": raw["earthlyBranchOfBodyPalace"],
        "palaces": palaces,
    }


def normalize_scope(scope):
    return {
        "index": scope["index"],
        "name": scope["name"],
        "stem": scope["heavenlyStem"],
        "branch": scope["earthlyBranch"],
        "palace_names": scope["palaceNames"],
        "mutagen": scope["mutagen"],
        "nominal_age": scope.get("nominalAge"),
        "stars": stable_flow_stars(scope.get("stars")),
    }


def normalize_horoscope(raw, target):
    yearly_dec = raw.get("yearly", {}).get("yearlyDecStar")
    return {
        "target": target,
        "solar_date": normalize_solar_date(raw["solarDate"]),
        "lunar_date": raw["lunarDate"],
        "scopes": {
            "decadal": normalize_scope(raw["decadal"]),
            "age": normalize_scope(raw["age"]),
            "yearly": normalize_scope(raw["yearly"]),
            "monthly": normalize_scope(raw["monthly"]),
            "daily": normalize_scope(raw["daily"]),
            "hourly": normalize_scope(raw["hourly"]),
        },
        "yearly_dec_stars": (
            {
                "suiqian12": yearly_dec["suiqian12"],
                "jiangqian12": yearly_dec["jiangqian12"],
            }
            if yearly_dec
            else None
        ),
    }


def render(case_input, targets):
    config = ChartConfig(
        algorithm=case_input.get("algorithm", "zhongzhou"),
        day_divide=case_input.get("day_divide", "forward"),
        year_divide=case_input.get("year_divide", "normal"),
        horoscope_divide=case_input.get("horoscope_divide", "normal"),
        astro_type="heaven",
    )
    engine = Astro()
    chart = engine.by_solar(
        case_input["solar_date"],
        int(case_input["time_index"]),
        case_input["gender"],
        fix_leap=bool(case_input.get("fix_leap", True)),
        language="zh-CN",
        config=config,
    )
    natal_raw = chart.to_dict()
    temporal = []
    for target in targets:
        h = engine.get_horoscope(chart, target["solar_date"], int(target["time_index"]))
        temporal.append(normalize_horoscope(h.to_dict(), target))
    return {
        "case_id": case_input["case_id"],
        "schema_version": "0.2",
        "engine": {
            "name": "x-iztro-rust",
            "version": __version__,
            "source_revision": "17e35b48dcbf63ded819d96f563a66d1f9e3494c",
            "adapter_version": "0.2",
        },
        "input": {
            **case_input,
            "school": "zhongzhou",
            "astro_type": "heaven",
            "language": "zh-CN",
            "input_calendar": "solar",
            "entrypoint": "x-iztro-rust.by_solar",
            "chart_config": {
                "algorithm": config.algorithm,
                "astro_type": "heaven",
                "fix_leap": bool(case_input.get("fix_leap", True)),
                "day_divide": case_input.get("day_divide", "forward"),
                "year_divide": case_input.get("year_divide", "normal"),
                "horoscope_divide": case_input.get("horoscope_divide", "normal"),
                "language": "zh-CN",
            },
        },
        "natal": normalize_natal(natal_raw),
        "temporal": temporal,
    }


def main():
    if len(sys.argv) != 4:
        raise SystemExit("Usage: python tools/x_iztro_full_export.py input.jsonl targets.json output.jsonl")
    input_path, targets_path, output_path = map(Path, sys.argv[1:])
    targets = json.loads(targets_path.read_text(encoding="utf-8"))["targets"]
    rows = []
    for line in input_path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(render(json.loads(line), targets))
    output_path.write_text(
        "\n".join(json.dumps(r, ensure_ascii=False, separators=(",", ":")) for r in rows) + "\n",
        encoding="utf-8",
    )
    print(f"P1 x-iztro-rust: wrote {len(rows)} natal records and {len(rows) * len(targets)} horoscope snapshots")


if __name__ == "__main__":
    main()

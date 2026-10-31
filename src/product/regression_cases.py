"""Load and validate deterministic chart-regression seed inputs."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date
from pathlib import Path


@dataclass(frozen=True)
class ChartRegressionInput:
    case_id: str
    solar_date: str
    time_index: int
    gender: str
    fix_leap: bool
    algorithm: str
    day_divide: str
    year_divide: str
    horoscope_divide: str
    notes: str = ""

    def validate(self) -> None:
        if not self.case_id:
            raise ValueError("case_id is required")
        date.fromisoformat(self.solar_date)
        if not 0 <= self.time_index <= 12:
            raise ValueError(f"time_index out of range: {self.time_index}")
        if self.gender not in {"male", "female"}:
            raise ValueError(f"unsupported gender: {self.gender}")
        if self.algorithm not in {"zhongzhou", "default"}:
            raise ValueError(f"unsupported algorithm: {self.algorithm}")
        if self.day_divide not in {"current", "forward"}:
            raise ValueError(f"unsupported day_divide: {self.day_divide}")
        if self.year_divide not in {"normal", "exact"}:
            raise ValueError(f"unsupported year_divide: {self.year_divide}")
        if self.horoscope_divide not in {"normal", "exact"}:
            raise ValueError(f"unsupported horoscope_divide: {self.horoscope_divide}")

    def as_export_dict(self) -> dict[str, object]:
        self.validate()
        return {
            "case_id": self.case_id,
            "solar_date": self.solar_date,
            "time_index": self.time_index,
            "gender": self.gender,
            "fix_leap": self.fix_leap,
            "algorithm": self.algorithm,
            "day_divide": self.day_divide,
            "year_divide": self.year_divide,
            "horoscope_divide": self.horoscope_divide,
            "time_basis": "true_solar_time",
            "location_correction_applied": False,
        }


def _bool(value: str) -> bool:
    value = value.strip().lower()
    if value in {"true", "1", "yes"}:
        return True
    if value in {"false", "0", "no"}:
        return False
    raise ValueError(f"invalid boolean: {value}")


def load_regression_inputs(path: str | Path) -> list[ChartRegressionInput]:
    rows: list[ChartRegressionInput] = []
    seen: set[str] = set()
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for raw in reader:
            item = ChartRegressionInput(
                case_id=raw["case_id"],
                solar_date=raw["solar_date"],
                time_index=int(raw["time_index"]),
                gender=raw["gender"],
                fix_leap=_bool(raw["fix_leap"]),
                algorithm=raw["algorithm"],
                day_divide=raw["day_divide"],
                year_divide=raw["year_divide"],
                horoscope_divide=raw["horoscope_divide"],
                notes=raw.get("notes", ""),
            )
            item.validate()
            if item.case_id in seen:
                raise ValueError(f"duplicate case_id: {item.case_id}")
            seen.add(item.case_id)
            rows.append(item)
    return rows

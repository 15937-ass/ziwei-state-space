import copy
import json
from pathlib import Path

import pytest

from src.product.longitudinal_observation_v02 import (
    EventTimeInterval,
    compile_longitudinal_observation_v02,
    migrate_longitudinal_observation_v01_to_v02,
)

ROOT = Path(__file__).resolve().parents[1]
V01 = ROOT / "product/PL7_LONGITUDINAL_OBSERVATION_FIXTURES_v0.1.json"


def _v01_event():
    return json.loads(V01.read_text(encoding="utf-8"))["fixtures"][0]


def _v02_event():
    return migrate_longitudinal_observation_v01_to_v02(_v01_event())


def test_v01_exact_date_migrates_losslessly_to_day_interval():
    migrated = _v02_event()
    event_time = migrated["outcome"]["event_time"]
    assert event_time["precision"] == "DAY"
    assert event_time["lower_bound_date"] == "2027-06-15"
    assert event_time["upper_bound_date"] == "2027-06-15"
    record = compile_longitudinal_observation_v02(migrated)
    assert record.event_time.precision == "DAY"


def test_month_precision_preserves_calendar_bounds_without_midpoint():
    payload = _v02_event()
    payload["outcome"]["event_time"] = {
        "precision": "MONTH",
        "lower_bound_date": "2027-06-01",
        "upper_bound_date": "2027-06-30",
    }
    record = compile_longitudinal_observation_v02(payload)
    assert record.event_time.lower_bound.isoformat() == "2027-06-01"
    assert record.event_time.upper_bound.isoformat() == "2027-06-30"


def test_year_precision_is_valid_for_annual_target_window():
    payload = _v02_event()
    payload["outcome"]["event_time"] = {
        "precision": "YEAR",
        "lower_bound_date": "2027-01-01",
        "upper_bound_date": "2027-12-31",
    }
    record = compile_longitudinal_observation_v02(payload)
    assert record.event_time.precision == "YEAR"


def test_partial_overlap_is_temporally_ambiguous_not_positive_truth():
    payload = _v02_event()
    payload["window"]["start_date"] = "2027-04-01"
    payload["window"]["end_date"] = "2027-06-30"
    payload["outcome"]["event_time"] = {
        "precision": "YEAR",
        "lower_bound_date": "2027-01-01",
        "upper_bound_date": "2027-12-31",
    }
    with pytest.raises(ValueError, match="TEMPORAL_ASSIGNMENT_AMBIGUOUS"):
        compile_longitudinal_observation_v02(payload)


def test_month_precision_rejects_fake_midmonth_bounds():
    payload = _v02_event()
    payload["outcome"]["event_time"] = {
        "precision": "MONTH",
        "lower_bound_date": "2027-06-15",
        "upper_bound_date": "2027-06-15",
    }
    with pytest.raises(ValueError, match="normalized calendar month"):
        compile_longitudinal_observation_v02(payload)


def test_non_event_status_cannot_carry_event_time():
    payload = _v02_event()
    payload["outcome"]["status"] = "UNKNOWN"
    with pytest.raises(ValueError, match="requires outcome.event_time=null"):
        compile_longitudinal_observation_v02(payload)

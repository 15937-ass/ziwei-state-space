import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "p1_validate_birth_zi_boundary.py"


def load_module():
    spec = importlib.util.spec_from_file_location("p1_validate_birth_zi_boundary", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _row(case_id, time_index, lunar_date, *, time_basis="true_solar_time", day_divide="current", corrected=False):
    return {
        "case_id": case_id,
        "input": {
            "solar_date": "2028-01-25",
            "gender": "male",
            "time_index": time_index,
            "time_basis": time_basis,
            "day_divide": day_divide,
            "location_correction_applied": corrected,
        },
        "natal": {
            "solar_date": "2028-01-25",
            "lunar_date": lunar_date,
        },
    }


def test_same_supplied_date_keeps_early_daytime_and_late_zi_on_one_lunar_date():
    mod = load_module()
    rows = [
        _row("EARLY", 0, "二〇二八年十二月廿九"),
        _row("DAY", 6, "二〇二八年十二月廿九"),
        _row("LATE", 12, "二〇二八年十二月廿九"),
    ]
    assert mod.validate(rows) == []


def test_late_zi_must_not_be_shifted_to_the_next_lunar_date():
    mod = load_module()
    rows = [
        _row("EARLY", 0, "二〇二八年十二月廿九"),
        _row("DAY", 6, "二〇二八年十二月廿九"),
        _row("LATE", 12, "二〇二九年正月初一"),
    ]
    errors = mod.validate(rows)
    assert any("inconsistent lunar dates" in error for error in errors)


def test_validator_rejects_non_true_solar_or_second_location_correction():
    mod = load_module()
    rows = [
        _row("EARLY", 0, "same", time_basis="civil_time"),
        _row("DAY", 6, "same"),
        _row("LATE", 12, "same", corrected=True),
    ]
    errors = mod.validate(rows)
    assert any("time_basis must be true_solar_time" in error for error in errors)
    assert any("location_correction_applied must be false" in error for error in errors)


def test_validator_rejects_forward_day_divide():
    mod = load_module()
    rows = [
        _row("EARLY", 0, "same"),
        _row("DAY", 6, "same"),
        _row("LATE", 12, "same", day_divide="forward"),
    ]
    errors = mod.validate(rows)
    assert any("day_divide must be current" in error for error in errors)


def test_validator_rejects_incomplete_same_date_time_index_group():
    mod = load_module()
    rows = [
        _row("EARLY", 0, "same"),
        _row("DAY", 6, "same"),
    ]
    errors = mod.validate(rows)
    assert any("missing required time_index values [12]" in error for error in errors)

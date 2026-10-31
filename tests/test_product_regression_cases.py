from pathlib import Path

from src.product.regression_cases import load_regression_inputs


ROOT = Path(__file__).resolve().parents[1]
SEEDS = ROOT / "validation" / "product_chart_regression" / "regression_inputs_v0.2.csv"


def test_seed_set_has_100_unique_valid_cases():
    rows = load_regression_inputs(SEEDS)
    assert len(rows) == 100
    assert len({r.case_id for r in rows}) == 100


def test_seed_set_covers_both_zi_hour_boundaries_and_both_genders():
    rows = load_regression_inputs(SEEDS)
    assert {0, 12}.issubset({r.time_index for r in rows})
    assert {"male", "female"} == {r.gender for r in rows}


def test_seed_set_is_first_pass_zhongzhou_configuration():
    rows = load_regression_inputs(SEEDS)
    assert {r.algorithm for r in rows} == {"zhongzhou"}
    assert {r.day_divide for r in rows} == {"current"}

def test_v1_1_seed_export_declares_true_solar_time_without_location_correction():
    rows = load_regression_inputs(SEEDS)
    exported = rows[0].as_export_dict()
    assert exported["time_basis"] == "true_solar_time"
    assert exported["location_correction_applied"] is False

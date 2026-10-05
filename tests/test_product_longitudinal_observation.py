import copy
import json
from pathlib import Path

import pytest

from src.product.longitudinal_observation import compile_longitudinal_observation

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "product/PL7_LONGITUDINAL_OBSERVATION_FIXTURES_v0.1.json"


def _records():
    payload = json.loads(FIXTURES.read_text(encoding="utf-8"))
    return payload["fixtures"]


def test_four_fixture_statuses_are_supported():
    records = [compile_longitudinal_observation(item) for item in _records()]
    assert [item.event_status for item in records] == [
        "EVENT_OCCURRED",
        "EVENT_NOT_OCCURRED",
        "CENSORED",
        "UNKNOWN",
    ]


def test_closed_negative_is_not_missing_data():
    record = compile_longitudinal_observation(_records()[1])
    assert record.is_closed_negative
    assert record.calibration_usable

    bad = copy.deepcopy(_records()[1])
    bad["window"]["observed_through"] = "2027-07-01"
    with pytest.raises(ValueError, match="full window"):
        compile_longitudinal_observation(bad)


def test_censored_requires_early_end_and_reason():
    record = compile_longitudinal_observation(_records()[2])
    assert record.is_survival_usable_censoring
    assert record.calibration_usable

    bad = copy.deepcopy(_records()[2])
    bad["outcome"]["censor_reason"] = None
    with pytest.raises(ValueError, match="censor_reason"):
        compile_longitudinal_observation(bad)


def test_unknown_is_never_treated_as_negative_or_calibration_truth():
    record = compile_longitudinal_observation(_records()[3])
    assert not record.is_closed_negative
    assert not record.calibration_usable


def test_prospective_blind_forecast_must_be_locked_before_window():
    record = compile_longitudinal_observation(_records()[0])
    assert record.blind_benchmark_eligible

    bad = copy.deepcopy(_records()[0])
    bad["model_linkage"]["forecast"]["locked_date"] = "2027-01-02"
    with pytest.raises(ValueError, match="locked on/before"):
        compile_longitudinal_observation(bad)


def test_forecast_none_rejects_hidden_forecast_metadata():
    bad = copy.deepcopy(_records()[1])
    bad["model_linkage"]["forecast"]["forecast_id"] = "LEAK"
    with pytest.raises(ValueError, match="must be null"):
        compile_longitudinal_observation(bad)


def test_event_date_must_be_inside_target_window():
    bad = copy.deepcopy(_records()[0])
    bad["outcome"]["event_date"] = "2028-01-01"
    with pytest.raises(ValueError, match="target window"):
        compile_longitudinal_observation(bad)


def test_actions_distinguish_intent_from_actual_status():
    record = compile_longitudinal_observation(_records()[0])
    assert record.actions[0]["status"] == "ACTUAL"

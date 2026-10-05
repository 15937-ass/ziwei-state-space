import copy
import json
from pathlib import Path

import pytest

from src.product.prospective_checkin import (
    classify_checkin_answer,
    compile_prospective_checkin_plan,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "product/PL7_PROSPECTIVE_CHECKIN_FIXTURES_v0.1.json"


def _plans():
    return json.loads(FIXTURES.read_text(encoding="utf-8"))["fixtures"]


def test_blind_plan_is_locked_and_prediction_hidden():
    plan = compile_prospective_checkin_plan(_plans()[0])
    assert plan.blind_benchmark_plan
    assert plan.prediction_exposure == "HIDDEN"
    assert len(plan.targets) == 2


def test_blind_benchmark_rejects_visible_prediction():
    bad = copy.deepcopy(_plans()[0])
    bad["prediction_exposure"] = "VISIBLE"
    with pytest.raises(ValueError, match="requires prediction_exposure=HIDDEN"):
        compile_prospective_checkin_plan(bad)


def test_target_must_be_locked_before_window_start():
    bad = copy.deepcopy(_plans()[0])
    bad["target_lock_date"] = "2027-01-02"
    with pytest.raises(ValueError, match="target_lock_date"):
        compile_prospective_checkin_plan(bad)


def test_exactly_one_window_close_is_required():
    bad = copy.deepcopy(_plans()[0])
    bad["schedule"] = [bad["schedule"][0]]
    with pytest.raises(ValueError, match="exactly one WINDOW_CLOSE"):
        compile_prospective_checkin_plan(bad)


def test_midwindow_no_is_not_a_negative_sample():
    assert classify_checkin_answer("MID_WINDOW", "NO") == "NO_EVENT_YET"


def test_window_close_no_can_become_negative_candidate():
    assert classify_checkin_answer("WINDOW_CLOSE", "NO") == "EVENT_NOT_OCCURRED_CANDIDATE"


def test_outcome_truth_is_forbidden_in_prospective_plan():
    bad = copy.deepcopy(_plans()[1])
    bad["outcome"] = {"event_status": "EVENT_OCCURRED"}
    with pytest.raises(ValueError, match="outcome leakage"):
        compile_prospective_checkin_plan(bad)


def test_forecast_must_lock_before_target_lock():
    bad = copy.deepcopy(_plans()[1])
    bad["forecast"]["locked_date"] = "2026-12-25"
    with pytest.raises(ValueError, match="on/before target_lock_date"):
        compile_prospective_checkin_plan(bad)

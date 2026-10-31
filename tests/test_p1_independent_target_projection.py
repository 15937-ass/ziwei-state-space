import importlib.util
from pathlib import Path


MODULE_PATH = Path("tools/p1_independent_compare.py")


def load_module():
    spec = importlib.util.spec_from_file_location("p1_independent_compare", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_target_core_drops_validation_only_metadata():
    mod = load_module()
    target = {
        "target_id": "A2_LEAP_MONTH_ENTER",
        "solar_date": "2028-06-23",
        "time_index": 6,
        "expected_lunar_marker": "闰五月初一",
        "note": "validator-only",
    }
    assert mod.target_core(target) == {
        "target_id": "A2_LEAP_MONTH_ENTER",
        "solar_date": "2028-06-23",
        "time_index": 6,
    }


def test_target_core_is_symmetric_for_go_and_js_shapes():
    mod = load_module()
    js = {
        "target_id": "A1_LUNAR_YEAR_START",
        "solar_date": "2028-01-26",
        "time_index": 6,
        "expected_lunar_marker": "正月初一",
    }
    go = {
        "target_id": "A1_LUNAR_YEAR_START",
        "solar_date": "2028-01-26",
        "time_index": 6,
    }
    assert mod.target_core(js) == mod.target_core(go)


def test_late_zi_birth_is_marked_as_cross_school_diagnostic():
    mod = load_module()
    assert mod.is_late_zi_birth({"input": {"time_index": 12}}) is True
    assert mod.is_late_zi_birth({"input": {"time_index": 0}}) is False
    assert mod.is_late_zi_birth({"input": {"time_index": 11}}) is False


def test_canonical_zhongzhou_late_zi_target_is_go_diagnostic_only():
    import json

    manifest_path = Path("validation/product_chart_regression/temporal_targets_v0.3.json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["school_sensitive_target_ids"] == ["T1_LEAP_LATE_ZI"]
    assert manifest["independent_core_policy"]["canonical_contract"] == "ZHONGZHOU_IZTRO_JS_2_6_1_V1_1"

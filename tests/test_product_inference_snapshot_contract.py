import copy
import json
from pathlib import Path

import pytest

from src.product.inference_snapshot_contract import (
    SUPPORTED_SCHEMA_VERSION,
    validate_normalized_inference_snapshot,
)

ROOT = Path(__file__).resolve().parents[1]
ASSET_PATH = ROOT / "product/PL3T_TEMPORAL_ASSET_FIXTURE_v0.1.json"

BRANCH = {
    "命宫": "酉",
    "兄弟宫": "戌",
    "夫妻宫": "未",
    "子女宫": "申",
    "财帛宫": "巳",
    "疾厄宫": "午",
    "迁移宫": "卯",
    "交友宫": "辰",
    "事业宫": "丑",
    "田宅宫": "寅",
    "福德宫": "亥",
    "父母宫": "子",
}


def _snapshot():
    snapshot = json.loads(ASSET_PATH.read_text(encoding="utf-8"))
    palaces = {}
    for palace_name, branch in BRANCH.items():
        palaces[branch] = {
            "name": palace_name[:-1],
            "stem": "甲",
            "branch": branch,
            "is_body_palace": False,
            "major_stars": [],
            "minor_stars": [],
            "adjective_stars": [],
        }
    snapshot["natal"] = {"palaces": palaces}
    return snapshot


def test_valid_full_export_snapshot_passes_contract():
    snapshot = _snapshot()
    validate_normalized_inference_snapshot(snapshot, target_id="T-DEMO")


def test_contract_rejects_unsupported_schema_version_and_missing_engine_provenance():
    snapshot = _snapshot()
    snapshot["schema_version"] = "0.1"
    with pytest.raises(ValueError, match=f"schema_version must be {SUPPORTED_SCHEMA_VERSION}"):
        validate_normalized_inference_snapshot(snapshot, target_id="T-DEMO")

    snapshot = _snapshot()
    snapshot["engine"].pop("adapter_version")
    with pytest.raises(ValueError, match="engine.adapter_version is required"):
        validate_normalized_inference_snapshot(snapshot, target_id="T-DEMO")


def test_contract_rejects_missing_scope_and_duplicate_temporal_target():
    snapshot = _snapshot()
    del snapshot["temporal"][0]["scopes"]["yearly"]
    with pytest.raises(ValueError, match="scopes.yearly must be an object"):
        validate_normalized_inference_snapshot(snapshot, target_id="T-DEMO")

    snapshot = _snapshot()
    snapshot["temporal"].append(copy.deepcopy(snapshot["temporal"][0]))
    with pytest.raises(ValueError, match="target_id is not unique"):
        validate_normalized_inference_snapshot(snapshot, target_id="T-DEMO")


def test_contract_rejects_malformed_scope_arrays_and_yearly_dec_stars():
    snapshot = _snapshot()
    snapshot["temporal"][0]["scopes"]["yearly"]["stars"] = "not-an-array"
    with pytest.raises(ValueError, match="scopes.yearly.stars must be an array"):
        validate_normalized_inference_snapshot(snapshot, target_id="T-DEMO")

    snapshot = _snapshot()
    snapshot["temporal"][0]["yearly_dec_stars"]["suiqian12"] = None
    with pytest.raises(ValueError, match="yearly_dec_stars.suiqian12 must be an array"):
        validate_normalized_inference_snapshot(snapshot, target_id="T-DEMO")


def test_contract_rejects_missing_selected_target_and_invalid_natal_palace_count():
    snapshot = _snapshot()
    with pytest.raises(ValueError, match="target_id not found"):
        validate_normalized_inference_snapshot(snapshot, target_id="T-MISSING")

    snapshot = _snapshot()
    snapshot["natal"]["palaces"].pop("酉")
    with pytest.raises(ValueError, match="natal.palaces must contain 12 palaces"):
        validate_normalized_inference_snapshot(snapshot, target_id="T-DEMO")

import copy
import json
from pathlib import Path

import pytest

import src.product.career_inference_service as career_service
from src.product.full_chart_snapshot_contract import (
    FULL_CHART_SCHEMA_VERSION,
    REQUIRED_ENGINE_FIELDS,
    validate_normalized_full_chart_snapshot,
)

from src.product.temporal_asset_adapter import SCOPE_TO_LAYER, adapt_target_from_full_snapshot

ROOT = Path(__file__).resolve().parents[1]
ASSET_PATH = ROOT / "product/PL3T_TEMPORAL_ASSET_FIXTURE_v0.2.json"

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


def _star(name, mutagen=None):
    return {
        "name": name,
        "type": None,
        "brightness": None,
        "mutagen": mutagen,
        "scope": None,
    }


def _valid_snapshot():
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
    palaces[BRANCH["事业宫"]]["major_stars"] = [_star("武曲", "科")]
    snapshot["natal"] = {"palaces": palaces}
    return snapshot


def _assert_invalid(snapshot, target_id, expected_message):
    result = validate_normalized_full_chart_snapshot(
        snapshot,
        target_id=target_id,
    )
    assert result.ok is False
    assert any(expected_message in error for error in result.errors)


def test_machine_readable_schema_matches_runtime_contract_constants():
    schema = json.loads(
        (ROOT / "product/PL3_FULL_CHART_SNAPSHOT_SCHEMA_v0.2.json").read_text(
            encoding="utf-8"
        )
    )

    assert schema["properties"]["schema_version"]["const"] == FULL_CHART_SCHEMA_VERSION
    assert set(schema["properties"]["engine"]["required"]) == set(REQUIRED_ENGINE_FIELDS)
    assert set(schema["properties"]["natal"]["properties"]["palaces"]["required"]) == set(BRANCH.values())
    assert set(schema["$defs"]["scope"]["required"]) == {
        "index",
        "name",
        "stem",
        "branch",
        "palace_names",
        "mutagen",
        "nominal_age",
        "stars",
    }
    assert set(schema["$defs"]["temporalTarget"]["properties"]["scopes"]["required"]) == {
        "decadal",
        "age",
        "yearly",
        "monthly",
        "daily",
        "hourly",
    }


def test_valid_full_chart_v02_snapshot_is_accepted_without_mutation():
    snapshot = _valid_snapshot()
    before = copy.deepcopy(snapshot)

    result = validate_normalized_full_chart_snapshot(
        snapshot,
        target_id="T-DEMO",
    )

    assert FULL_CHART_SCHEMA_VERSION == "0.2"
    assert result.ok is True
    assert result.errors == ()
    assert snapshot == before


def test_yearly_dec_stars_are_optional_but_validated_when_present():
    snapshot = _valid_snapshot()
    snapshot["temporal"][0]["yearly_dec_stars"] = None
    assert validate_normalized_full_chart_snapshot(snapshot, target_id="T-DEMO").ok

    snapshot["temporal"][0].pop("yearly_dec_stars")
    assert validate_normalized_full_chart_snapshot(snapshot, target_id="T-DEMO").ok

    snapshot = _valid_snapshot()
    snapshot["temporal"][0]["yearly_dec_stars"] = {"suiqian12": []}
    _assert_invalid(snapshot, "T-DEMO", "yearly_dec_stars missing field: jiangqian12")


def test_unsupported_schema_and_missing_engine_provenance_fail_closed():
    snapshot = _valid_snapshot()
    snapshot["schema_version"] = "0.1"
    _assert_invalid(snapshot, "T-DEMO", "schema_version must be '0.2'")

    snapshot = _valid_snapshot()
    del snapshot["engine"]["source_revision"]
    _assert_invalid(snapshot, "T-DEMO", "engine.source_revision is required for provenance")


def test_natal_palace_mapping_must_cover_exactly_the_twelve_branches():
    snapshot = _valid_snapshot()
    snapshot["natal"]["palaces"].pop("酉")
    _assert_invalid(snapshot, "T-DEMO", "natal.palaces must map exactly the 12 earthly branches")

    snapshot = _valid_snapshot()
    snapshot["natal"]["palaces"]["酉"]["branch"] = "戌"
    _assert_invalid(snapshot, "T-DEMO", "natal.palaces.酉.branch must equal its mapping key")


@pytest.mark.parametrize(
    "scope_key",
    ["decadal", "age", "yearly", "monthly", "daily", "hourly"],
)
def test_each_of_the_six_adapter_scopes_is_required(scope_key):
    snapshot = _valid_snapshot()
    del snapshot["temporal"][0]["scopes"][scope_key]
    _assert_invalid(
        snapshot,
        "T-DEMO",
        f"temporal[0].scopes missing required scope: {scope_key}",
    )


@pytest.mark.parametrize(
    "field,expected",
    [
        ("index", "index must be an integer"),
        ("palace_names", "palace_names must be an array"),
        ("mutagen", "mutagen must be an array"),
        ("stars", "stars must be an array of arrays"),
    ],
)
def test_adapter_required_scope_fields_are_type_checked(field, expected):
    snapshot = _valid_snapshot()
    snapshot["temporal"][0]["scopes"]["yearly"][field] = {"bad": "shape"}
    _assert_invalid(snapshot, "T-DEMO", f"temporal[0].scopes.yearly.{expected}")


def test_scope_star_groups_must_align_with_palace_names_and_use_star_objects():
    snapshot = _valid_snapshot()
    snapshot["temporal"][0]["scopes"]["yearly"]["stars"] = [[]]
    _assert_invalid(
        snapshot,
        "T-DEMO",
        "temporal[0].scopes.yearly.stars group count must equal palace_names length",
    )

    snapshot = _valid_snapshot()
    snapshot["temporal"][0]["scopes"]["yearly"]["stars"][0] = ["not-an-object"]
    _assert_invalid(
        snapshot,
        "T-DEMO",
        "temporal[0].scopes.yearly.stars[0][0] must be an object",
    )


def test_temporal_target_ids_must_be_unique_and_selected_target_must_exist():
    snapshot = _valid_snapshot()
    snapshot["temporal"].append(copy.deepcopy(snapshot["temporal"][0]))
    _assert_invalid(snapshot, "T-DEMO", "duplicate temporal target_id: T-DEMO")

    snapshot = _valid_snapshot()
    _assert_invalid(
        snapshot,
        "T-NOT-PRESENT",
        "selected target_id not found in normalized temporal snapshot",
    )


def test_target_date_metadata_must_be_valid_and_consistent():
    snapshot = _valid_snapshot()
    snapshot["temporal"][0]["target"]["solar_date"] = "2033-02-30"
    _assert_invalid(snapshot, "T-DEMO", "target.solar_date must be a valid YYYY-MM-DD date")

    snapshot = _valid_snapshot()
    snapshot["temporal"][0]["solar_date"] = "2033-08-04"
    _assert_invalid(snapshot, "T-DEMO", "solar_date must equal temporal[0].target.solar_date")

    snapshot = _valid_snapshot()
    snapshot["temporal"][0]["target"]["time_index"] = "6"
    _assert_invalid(snapshot, "T-DEMO", "target.time_index must be an integer")


def test_malformed_snapshot_fails_before_any_provider_is_loaded(monkeypatch):
    def unexpected_provider_load(*args, **kwargs):
        raise AssertionError("provider must not load before snapshot validation")

    monkeypatch.setattr(
        career_service,
        "load_default_career_natal_provider",
        unexpected_provider_load,
    )

    with pytest.raises(ValueError, match="schema_version must be '0.2'"):
        career_service.run_career_inference(
            ROOT,
            {"schema_version": "0.1"},
            target_id="T-DEMO",
            question="contract fail-closed test",
        )


def test_unknown_scope_is_not_silently_discarded():
    snapshot = _valid_snapshot()
    snapshot["temporal"][0]["scopes"]["future_scope"] = {}
    _assert_invalid(
        snapshot,
        "T-DEMO",
        "temporal[0].scopes contains unsupported scope(s): future_scope",
    )


@pytest.mark.parametrize("selected_id", ["T-DEMO", " T-DEMO "])
def test_padded_target_ids_cannot_bypass_adapter_target_uniqueness(selected_id):
    snapshot = _valid_snapshot()
    duplicate = copy.deepcopy(snapshot["temporal"][0])
    duplicate["target"]["target_id"] = " T-DEMO "
    snapshot["temporal"].append(duplicate)
    _assert_invalid(snapshot, selected_id, "must not contain surrounding whitespace")


def test_unselected_target_scope_errors_identify_the_actual_array_position():
    snapshot = _valid_snapshot()
    other = copy.deepcopy(snapshot["temporal"][0])
    other["target"]["target_id"] = "T-OTHER"
    other["scopes"]["yearly"]["index"] = False
    snapshot["temporal"].append(other)
    _assert_invalid(snapshot, "T-DEMO", "temporal[1].scopes.yearly.index must be an integer")


@pytest.mark.parametrize("scope_key", SCOPE_TO_LAYER)
def test_explicit_empty_flow_star_array_is_accepted_without_inventing_stars(scope_key):
    snapshot = _valid_snapshot()
    snapshot["temporal"][0]["scopes"][scope_key]["stars"] = []
    before = copy.deepcopy(snapshot)
    assert validate_normalized_full_chart_snapshot(snapshot, target_id="T-DEMO").ok
    bundle = adapt_target_from_full_snapshot(snapshot, target_id="T-DEMO")
    assert not any(
        fact.layer == SCOPE_TO_LAYER[scope_key] and fact.fact.startswith("stars[")
        for fact in bundle.temporal_facts
    )
    assert snapshot == before


@pytest.mark.parametrize("scope_key", SCOPE_TO_LAYER)
@pytest.mark.parametrize("bad_value", [None, {}, [[]]])
def test_empty_array_compatibility_still_rejects_malformed_flow_star_arrays(scope_key, bad_value):
    snapshot = _valid_snapshot()
    snapshot["temporal"][0]["scopes"][scope_key]["stars"] = bad_value
    assert not validate_normalized_full_chart_snapshot(snapshot, target_id="T-DEMO").ok


@pytest.mark.parametrize("scope_key", SCOPE_TO_LAYER)
def test_empty_array_compatibility_does_not_make_stars_optional(scope_key):
    snapshot = _valid_snapshot()
    del snapshot["temporal"][0]["scopes"][scope_key]["stars"]
    _assert_invalid(snapshot, "T-DEMO", f"scopes.{scope_key} missing field: stars")


def test_real_export_age_shape_reaches_service_without_changing_natal_or_temporal_claims():
    snapshot = _valid_snapshot()
    snapshot["temporal"][0]["scopes"]["age"] = {
        "index": 8, "name": "小限", "stem": "甲", "branch": "戌",
        "palace_names": ["官禄", "仆役", "迁移", "疾厄", "财帛", "子女",
                         "夫妻", "兄弟", "命宫", "父母", "福德", "田宅"],
        "mutagen": ["廉贞", "破军", "武曲", "太阳"],
        "nominal_age": 49, "stars": [],
    }
    before = copy.deepcopy(snapshot)
    run = career_service.run_career_inference(
        ROOT, snapshot, target_id="T-DEMO", question="真实小限输入兼容验收",
    )
    assert run.status == "PARTIAL_TEMPORAL_REGISTRY_EMPTY"
    active_ids = {rule.rule_id for rule in run.natal_profile.domains[0].active_rules}
    assert {"CA04-336", "CA04-338", "CA04-341", "CA04-347"} <= active_ids
    assert run.reaction_report.matched == ()
    assert snapshot == before

import copy
import json
from pathlib import Path

import pytest

from src.product.condition_atoms import fact_from_atom
from src.product.natal_prior import NatalStateProfile
from src.product.temporal_asset_adapter import (
    SCOPE_TO_LAYER,
    adapt_target_from_full_snapshot,
)
from src.product.temporal_reaction_compiler import (
    compile_temporal_reaction_registry,
    match_temporal_reactions,
)
from product.experiments.spatiotemporal_v03.probe import (
    expand_snapshot,
    make_report,
)

ROOT = Path(__file__).resolve().parents[1]
EXP_ROOT = ROOT / "product/experiments/spatiotemporal_v03"
FIXTURE_PATH = EXP_ROOT / "fixtures/full_snapshot_projection_v0.3.json"
REPORT_PATH = EXP_ROOT / "COMPARISON_REPORT_v0.3.json"

EXPECTED_SCOPES = {
    "decadal": "DECADE",
    "age": "SMALL_LIMIT",
    "yearly": "YEAR",
    "monthly": "MONTH",
    "daily": "DAY",
    "hourly": "HOUR",
}


def _fixture():
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _expanded_record(record):
    fixture = _fixture()
    return expand_snapshot(record, fixture["palace_vocab"])


def _profile():
    return NatalStateProfile(
        schema_version="0.1",
        profile_id="NATAL-TEST-ONLY-GUARD-ANCHOR",
        engine_version="test-only",
        knowledge_version="TEST_FIXTURE_ONLY",
        canonical_facts=(
            fact_from_atom("SUBJECT_PRESENT", subject="TEST_ONLY_NATAL_ANCHOR"),
        ),
        named_structure_facts=(),
        baiguan_profiles=(),
        pattern_assessments=(),
        contextual_valences=(),
        domains=(),
    )


def _registry():
    return {
        "schema_version": "0.1",
        "status": "TEST_FIXTURE_ONLY_NOT_CANONICAL",
        "rules": [
            {
                "reaction_id": "TR-V03-YEAR-PALACE-STAR",
                "rule_id": "TR-V03-YEAR-PALACE-STAR",
                "layer": "YEAR",
                "domain": "test_only",
                "target": "year_palace_bound_star_guard",
                "effect": "ACTIVATE",
                "source_id": "TEST-FIXTURE",
                "source_location": "product/experiments/spatiotemporal_v03",
                "review_status": "SOURCE_SPAN_VERIFIED",
                "source_span_verified": True,
                "normalization_epistemic": "SOURCE_PRESERVING",
                "normalization_verified": True,
                "case_support_only": False,
                "magnitude_status": "UNIDENTIFIED",
                "required_natal_rule_ids": [],
                "natal_condition": {
                    "all_of": [
                        {
                            "atom_type": "SUBJECT_PRESENT",
                            "args": {"subject": "TEST_ONLY_NATAL_ANCHOR"},
                        }
                    ]
                },
                "temporal_condition": {
                    "all_of": [
                        {
                            "atom_type": "TIME_LAYER",
                            "args": {"layer": "YEAR"},
                        },
                        {
                            "atom_type": "PALACE_HAS_STAR",
                            "args": {
                                "layer": "YEAR",
                                "palace_name": "福德",
                                "star": "流马",
                            },
                        },
                    ]
                },
            }
        ],
    }


def test_report_is_exactly_reproducible_from_pinned_fixture():
    report = make_report()
    checked_in = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    assert report == checked_in
    assert report["status"] == "TEST_ONLY_ENGINEERING_PROBE"
    assert report["checks"]["canonical_acceptance"] is False
    assert report["checks"]["runtime_effect_allowed"] is False


def test_full_projection_has_twelve_palaces_and_all_six_scopes():
    fixture = _fixture()
    assert len(fixture["records"]) == 2
    assert fixture["selection"]["target_snapshots"] == 4
    assert fixture["selection"]["layer_instances"] == 24
    for record in fixture["records"]:
        assert len(record["natal"]) == 12
        for target in _expanded_record(record)["temporal"]:
            assert set(target["scopes"]) == set(EXPECTED_SCOPES)
            for scope_key, layer in EXPECTED_SCOPES.items():
                scope = target["scopes"][scope_key]
                assert len(scope["palace_names"]) == 12
                assert len(set(scope["palace_names"])) == 12
                assert layer in SCOPE_TO_LAYER.values()
                if scope_key == "age":
                    assert scope["stars"] == []
                else:
                    assert len(scope["stars"]) == 12


def test_same_natal_projection_is_independent_of_selected_target():
    fixture = _fixture()
    for record in fixture["records"]:
        snapshot = _expanded_record(record)
        natal_before = copy.deepcopy(snapshot["natal_projection"])
        targets = {item["target"]["target_id"]: item for item in snapshot["temporal"]}
        first = adapt_target_from_full_snapshot(snapshot, target_id="T1_LEAP_LATE_ZI")
        second = adapt_target_from_full_snapshot(snapshot, target_id="T3_DAYTIME")
        assert first.target_id == "T1_LEAP_LATE_ZI"
        assert second.target_id == "T3_DAYTIME"
        assert first.condition_facts != second.condition_facts
        assert first.temporal_facts != second.temporal_facts
        assert snapshot["natal_projection"] == natal_before
        assert targets["T1_LEAP_LATE_ZI"]["target"]["target_id"] != targets["T3_DAYTIME"]["target"]["target_id"]


def test_test_only_palace_bound_year_guard_matches_only_when_palace_binding_matches():
    rules = compile_temporal_reaction_registry(_registry())
    profile = _profile()
    fixture = _fixture()
    for record in fixture["records"]:
        snapshot = _expanded_record(record)
        t1 = adapt_target_from_full_snapshot(snapshot, target_id="T1_LEAP_LATE_ZI")
        t3 = adapt_target_from_full_snapshot(snapshot, target_id="T3_DAYTIME")
        t1_report = match_temporal_reactions(profile, t1, rules)
        t3_report = match_temporal_reactions(profile, t3, rules)
        assert len(t1_report.matched) == 1
        assert t1_report.matched[0].matched_temporal_facts
        assert t3_report.matched == ()


def test_temporal_guard_rejects_cross_layer_atom():
    document = copy.deepcopy(_registry())
    document["rules"][0]["temporal_condition"]["all_of"][1]["args"]["layer"] = "MONTH"
    with pytest.raises(ValueError, match="every temporal condition atom must carry"):
        compile_temporal_reaction_registry(document)


def test_scope_mutagen_raw_serialization_is_not_a_glyph_or_star_binding():
    record = _fixture()["records"][0]
    bundle = adapt_target_from_full_snapshot(
        _expanded_record(record),
        target_id="T1_LEAP_LATE_ZI",
    )
    facts = set(bundle.condition_facts)
    assert fact_from_atom(
        "TRANSFORMATION_PRESENT", layer="YEAR", mutagen="紫微"
    ) in facts
    assert fact_from_atom(
        "TRANSFORMATION_PRESENT", layer="YEAR", mutagen="科"
    ) not in facts
    assert fact_from_atom(
        "TRANSFORMATION_PRESENT",
        layer="YEAR",
        palace_name="福德",
        star="紫微",
        mutagen="科",
    ) not in facts


def test_scope_mutagen_values_follow_pinned_star_name_domain():
    fixture = _fixture()
    for record in fixture["records"]:
        natal_star_names = {
            star
            for row in record["natal"].values()
            for group in row[1:]
            for star in group
        }
        scope_values = [
            value
            for target in record["temporal"]
            for scope in target["scopes"].values()
            for value in scope["mu"]
        ]
        assert scope_values
        assert all(value in natal_star_names for value in scope_values)
        assert all(value not in {"禄", "权", "科", "忌"} for value in scope_values)


def test_missing_temporal_scope_fails_closed():
    record = _fixture()["records"][0]
    snapshot = _expanded_record(record)
    snapshot["temporal"][0]["scopes"].pop("hourly")
    with pytest.raises(ValueError, match="temporal scopes missing object: hourly"):
        adapt_target_from_full_snapshot(snapshot, target_id="T1_LEAP_LATE_ZI")

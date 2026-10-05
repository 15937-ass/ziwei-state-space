import json
from pathlib import Path

import pytest

from src.product.event_relative_window import (
    APPROVED_HUMAN_GATE,
    DEFAULT_WINDOW_REGISTRY_PATH,
    build_temporal_environment_with_migration_window,
    load_approved_migration_window_spec,
    resolve_approved_migration_window,
)
from src.product.natal_prior import NatalStateProfile
from src.product.temporal_environment import TemporalFact
from src.wp05_event_relative_time import MigrationEventRelativeContext

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "product/PL3T_EVENT_RELATIVE_WINDOW_FIXTURE_v0.1.json"


def _natal():
    return NatalStateProfile(
        schema_version="0.1",
        profile_id="NATAL-EVENT-RELATIVE-TEST",
        engine_version="test",
        knowledge_version="KB-TEST",
        canonical_facts=(),
        named_structure_facts=(),
        baiguan_profiles=(),
        pattern_assessments=(),
        contextual_valences=(),
        domains=(),
    )


def _fact():
    return TemporalFact(
        layer="YEAR",
        fact="TIME_LAYER|layer=YEAR",
        provenance="fixture",
    )


def test_registry_is_exactly_the_human_gate_approved_single_window():
    spec = load_approved_migration_window_spec(DEFAULT_WINDOW_REGISTRY_PATH)
    assert spec.window_id == "MIGRATION_FIRST_THREE_YEARS"
    assert spec.event_type == "DISTANT_RELOCATION_SETTLEMENT"
    assert spec.counter_name == "years_since_distant_relocation"
    assert (spec.min_index, spec.max_index) == (1, 3)
    assert spec.human_gate == APPROVED_HUMAN_GATE
    assert spec.review_status == "HUMAN_VERIFIED"


def test_fixture_cases_preserve_source_bounded_activation():
    document = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert document["approved_window_id"] == "MIGRATION_FIRST_THREE_YEARS"
    for case in document["cases"]:
        resolved = resolve_approved_migration_window(
            MigrationEventRelativeContext(
                confirmed_distant_settlement=case["confirmed_distant_settlement"],
                years_since_distant_relocation=case["years_since_distant_relocation"],
                travel_only=case["travel_only"],
            )
        )
        assert resolved.active is case["expected_active"]
        assert resolved.context_evidence.status == case["expected_status"]


@pytest.mark.parametrize("year", [1, 2, 3])
def test_active_window_preserves_ordinary_rotation_and_primary_migration_priority(year):
    resolved = resolve_approved_migration_window(
        MigrationEventRelativeContext(
            confirmed_distant_settlement=True,
            years_since_distant_relocation=year,
        )
    )
    assert resolved.active
    assert resolved.source_resolution.migration_palace_priority == "PRIMARY"
    assert resolved.source_resolution.annual_life_palace_rotation == "PRESERVED"
    assert resolved.source_resolution.other_palace_rotation == "PRESERVED"
    assert "projection_priority:migration_palace:primary" in resolved.routing_facts
    assert "rotation:annual_life_palace:preserved" in resolved.routing_facts


def test_elapsed_year_without_confirmed_settlement_never_activates():
    resolved = resolve_approved_migration_window(
        MigrationEventRelativeContext(
            confirmed_distant_settlement=False,
            years_since_distant_relocation=2,
        )
    )
    assert not resolved.active
    assert resolved.context_evidence.status == "INACTIVE_EVENT_UNCONFIRMED"
    assert "gate:migration_first_three_years:active" not in resolved.routing_facts


def test_travel_only_does_not_become_settlement_window():
    resolved = resolve_approved_migration_window(
        MigrationEventRelativeContext(
            confirmed_distant_settlement=False,
            years_since_distant_relocation=None,
            travel_only=True,
        )
    )
    assert not resolved.active
    assert resolved.context_evidence.status == "INACTIVE_TRAVEL_ONLY"
    assert resolved.routing_facts == ()


def test_temporal_environment_receives_context_evidence_without_new_time_layer():
    profile = build_temporal_environment_with_migration_window(
        _natal(),
        target_label="2030",
        temporal_facts=(_fact(),),
        migration_context=MigrationEventRelativeContext(
            confirmed_distant_settlement=True,
            years_since_distant_relocation=2,
        ),
    )
    assert profile.active_layers == ("YEAR",)
    assert len(profile.event_relative_context) == 1
    assert profile.event_relative_context[0].context_id == "MIGRATION_FIRST_THREE_YEARS"
    assert profile.event_relative_context[0].status == "ACTIVE"


def test_same_inputs_produce_same_temporal_profile():
    kwargs = dict(
        natal_profile=_natal(),
        target_label="2030",
        temporal_facts=(_fact(),),
        migration_context=MigrationEventRelativeContext(
            confirmed_distant_settlement=True,
            years_since_distant_relocation=3,
        ),
    )
    first = build_temporal_environment_with_migration_window(**kwargs)
    second = build_temporal_environment_with_migration_window(**kwargs)
    assert first.profile_id == second.profile_id


def test_registry_drift_fails_closed(tmp_path):
    bad = tmp_path / "bad.csv"
    bad.write_text(
        "window_id,event_type,counter_name,min_index,max_index,trigger_requirement,"
        "active_projection_context,preserved_contexts,source_id,source_location,"
        "review_status,human_gate\n"
        "MIGRATION_FIRST_THREE_YEARS,DISTANT_RELOCATION_SETTLEMENT,"
        "years_since_distant_relocation,1,4,"
        "confirmed_distant_settlement_and_not_travel_only,"
        "migration_palace_primary,"
        "annual_life_palace_rotation_and_other_palace_rotation,"
        "SRC-ZZ-003,迁移宫 printed p109,HUMAN_VERIFIED,HG-P07-TEMPORAL-01-A\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="registry drift"):
        load_approved_migration_window_spec(bad)


def test_multiple_windows_are_rejected_in_v01(tmp_path):
    source = DEFAULT_WINDOW_REGISTRY_PATH.read_text(encoding="utf-8")
    header, row = source.strip().splitlines()
    bad = tmp_path / "two.csv"
    bad.write_text(header + "\n" + row + "\n" + row + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="exactly one"):
        load_approved_migration_window_spec(bad)

import pytest

from src.product.event_relative_window import (
    MIGRATION_WINDOW_ID,
    MigrationFirstThreeYearsInput,
    resolve_migration_first_three_years,
)
from src.product.natal_prior import NatalStateProfile
from src.product.temporal_environment import (
    TemporalFact,
    build_temporal_environment_profile,
)


def _trigger(years, *, travel=False):
    return MigrationFirstThreeYearsInput(
        confirmed_distant_settlement=True,
        years_since_distant_relocation=years,
        travel_only=travel,
        trigger_provenance="OBS-RELOCATION-001",
    )


@pytest.mark.parametrize("year", [1, 2, 3])
def test_first_three_years_activate_source_bounded_window(year):
    result = resolve_migration_first_three_years(_trigger(year))
    assert result.status == "ACTIVE"
    assert result.window_id == MIGRATION_WINDOW_ID
    assert f"event_relative:distant_relocation_year:{year}" in result.evidence.routing_facts
    assert "projection_priority:migration_palace:primary" in result.evidence.routing_facts
    assert "rotation:annual_life_palace:preserved" in result.evidence.routing_facts


def test_year_four_is_inactive_without_decay_extension():
    result = resolve_migration_first_three_years(_trigger(4))
    assert result.status == "INACTIVE"
    assert result.reason == "OUTSIDE_SOURCE_EXPLICIT_YEAR_1_TO_3_WINDOW"
    assert all("primary" not in fact for fact in result.evidence.routing_facts)


def test_travel_only_does_not_activate_settlement_window():
    result = resolve_migration_first_three_years(_trigger(2, travel=True))
    assert result.status == "INACTIVE"
    assert result.reason == "TRAVEL_ONLY_EXCLUDED"


def test_confirmed_event_without_elapsed_year_is_insufficient():
    result = resolve_migration_first_three_years(_trigger(None))
    assert result.status == "INSUFFICIENT"
    assert result.reason == "YEARS_SINCE_RELOCATION_REQUIRED"


def test_confirmed_event_requires_trigger_provenance():
    with pytest.raises(ValueError, match="trigger_provenance"):
        MigrationFirstThreeYearsInput(
            confirmed_distant_settlement=True,
            years_since_distant_relocation=1,
            travel_only=False,
        )


def test_negative_year_is_rejected():
    with pytest.raises(ValueError, match="cannot be negative"):
        _trigger(-1)


def test_active_overlay_marks_explicit_external_trigger_without_feedback_mutation():
    natal = NatalStateProfile(
        schema_version="0.1",
        profile_id="NATAL-EVENT-RELATIVE",
        engine_version="test",
        knowledge_version="KB-TEST",
        canonical_facts=(),
        named_structure_facts=(),
        baiguan_profiles=(),
        pattern_assessments=(),
        contextual_valences=(),
        domains=(),
    )
    resolution = resolve_migration_first_three_years(_trigger(2))
    profile = build_temporal_environment_profile(
        natal,
        target_label="2030",
        temporal_facts=(
            TemporalFact(
                layer="YEAR",
                fact='scope.branch="辰"',
                provenance="test",
            ),
        ),
        event_relative_context=(resolution.evidence,),
    )
    assert profile.external_event_trigger_used
    assert not profile.feedback_used
    assert not profile.acquired_state_used
    assert not profile.outcome_used
    assert not profile.empirical_calibration_used
    assert profile.to_dict()["external_event_trigger_used"] is True

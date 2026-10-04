import pytest

from src.wp05_event_relative_time import (
    MigrationEventRelativeContext,
    migration_runtime_facts,
    resolve_migration_event_window,
)


@pytest.mark.parametrize("year", [1, 2, 3])
def test_first_three_years_after_confirmed_distant_settlement_are_active(year):
    resolved = resolve_migration_event_window(
        MigrationEventRelativeContext(
            confirmed_distant_settlement=True,
            years_since_distant_relocation=year,
        )
    )
    assert resolved.active is True
    assert resolved.migration_palace_priority == "PRIMARY"
    assert resolved.annual_life_palace_rotation == "PRESERVED"
    assert resolved.other_palace_rotation == "PRESERVED"
    assert "gate:migration_first_three_years:active" in resolved.facts


@pytest.mark.parametrize("year", [0, 4, 8])
def test_window_does_not_extend_outside_source_supported_years(year):
    resolved = resolve_migration_event_window(
        MigrationEventRelativeContext(
            confirmed_distant_settlement=True,
            years_since_distant_relocation=year,
        )
    )
    assert resolved.active is False
    assert resolved.migration_palace_priority == "BASELINE"
    assert "gate:migration_first_three_years:active" not in resolved.facts


def test_travel_only_never_creates_relocation_window():
    resolved = resolve_migration_event_window(
        MigrationEventRelativeContext(
            confirmed_distant_settlement=False,
            years_since_distant_relocation=None,
            travel_only=True,
        )
    )
    assert resolved.active is False
    assert migration_runtime_facts(
        MigrationEventRelativeContext(False, None, True)
    ) == frozenset()


def test_unconfirmed_event_does_not_activate_from_elapsed_year_alone():
    resolved = resolve_migration_event_window(
        MigrationEventRelativeContext(
            confirmed_distant_settlement=False,
            years_since_distant_relocation=2,
        )
    )
    assert resolved.active is False
    assert "event:distant_relocation_settlement:confirmed" not in resolved.facts


def test_confirmed_settlement_requires_external_elapsed_year():
    with pytest.raises(ValueError):
        MigrationEventRelativeContext(
            confirmed_distant_settlement=True,
            years_since_distant_relocation=None,
        )


def test_rejects_inconsistent_travel_and_settlement_flags():
    with pytest.raises(ValueError):
        MigrationEventRelativeContext(
            confirmed_distant_settlement=True,
            years_since_distant_relocation=1,
            travel_only=True,
        )


@pytest.mark.parametrize("bad", [-1, 1.5, "2", True])
def test_invalid_relative_year_is_rejected(bad):
    exc = ValueError if bad == -1 else TypeError
    with pytest.raises(exc):
        MigrationEventRelativeContext(
            confirmed_distant_settlement=True,
            years_since_distant_relocation=bad,
        )

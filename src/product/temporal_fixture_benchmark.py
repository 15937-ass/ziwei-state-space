"""Deterministic PL3-T temporal fixture benchmark.

Fixtures validate composition of already-approved product contracts:
PL1 temporal assets -> optional approved event-relative overlay ->
TemporalEnvironmentProfile.

They do not measure empirical prediction accuracy.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from .event_relative_window import (
    MigrationFirstThreeYearsInput,
    resolve_migration_first_three_years,
)
from .natal_prior import NatalStateProfile
from .temporal_asset_adapter import (
    adapt_target_from_full_snapshot,
    build_temporal_environment_from_assets,
)


@dataclass(frozen=True)
class TemporalFixture:
    fixture_id: str
    target_id: str
    event_relative_input: Mapping[str, Any] | None
    expected_active_layers: tuple[str, ...]
    expected_event_relative_status: str | None
    expected_routing_facts_all: tuple[str, ...]
    expected_external_event_trigger_used: bool


@dataclass(frozen=True)
class TemporalFixtureResult:
    fixture_id: str
    profile_id: str
    active_layers: tuple[str, ...]
    event_relative_statuses: tuple[str, ...]
    routing_facts: tuple[str, ...]
    external_event_trigger_used: bool


def _natal_profile() -> NatalStateProfile:
    return NatalStateProfile(
        schema_version="0.1",
        profile_id="NATAL-PL3T-FIXTURE",
        engine_version="pl3t-fixture:0.1",
        knowledge_version="KB-TEST",
        canonical_facts=(),
        named_structure_facts=(),
        baiguan_profiles=(),
        pattern_assessments=(),
        contextual_valences=(),
        domains=(),
    )


def load_temporal_fixtures(path: str | Path) -> tuple[TemporalFixture, ...]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if payload.get("schema_version") != "0.1":
        raise ValueError("temporal fixture schema_version must be 0.1")

    rows = payload.get("fixtures")
    if not isinstance(rows, list) or not rows:
        raise ValueError("temporal fixture document requires fixtures")

    seen: set[str] = set()
    out: list[TemporalFixture] = []
    for index, row in enumerate(rows):
        if not isinstance(row, Mapping):
            raise ValueError(f"fixtures[{index}] must be an object")
        fixture_id = str(row.get("fixture_id", "")).strip()
        if not fixture_id or fixture_id in seen:
            raise ValueError("fixture_id must be unique and non-empty")
        seen.add(fixture_id)

        target_id = str(row.get("target_id", "")).strip()
        if not target_id:
            raise ValueError(f"{fixture_id}: target_id is required")

        event_relative_input = row.get("event_relative_input")
        if event_relative_input is not None and not isinstance(
            event_relative_input, Mapping
        ):
            raise ValueError(
                f"{fixture_id}: event_relative_input must be object or null"
            )

        out.append(
            TemporalFixture(
                fixture_id=fixture_id,
                target_id=target_id,
                event_relative_input=(
                    dict(event_relative_input)
                    if isinstance(event_relative_input, Mapping)
                    else None
                ),
                expected_active_layers=tuple(
                    sorted(str(x) for x in row.get("expected_active_layers", []))
                ),
                expected_event_relative_status=(
                    str(row["expected_event_relative_status"]).strip()
                    if row.get("expected_event_relative_status") is not None
                    else None
                ),
                expected_routing_facts_all=tuple(
                    sorted(str(x) for x in row.get("expected_routing_facts_all", []))
                ),
                expected_external_event_trigger_used=bool(
                    row.get("expected_external_event_trigger_used", False)
                ),
            )
        )
    return tuple(out)


def _event_overlay(fixture: TemporalFixture):
    if fixture.event_relative_input is None:
        return ()

    raw = fixture.event_relative_input
    value = MigrationFirstThreeYearsInput(
        confirmed_distant_settlement=bool(
            raw.get("confirmed_distant_settlement", False)
        ),
        years_since_distant_relocation=raw.get(
            "years_since_distant_relocation"
        ),
        travel_only=bool(raw.get("travel_only", False)),
        trigger_provenance=str(raw.get("trigger_provenance", "")).strip(),
    )
    resolution = resolve_migration_first_three_years(value)
    return (resolution.evidence,)


def run_temporal_fixture(
    asset_snapshot: Mapping[str, Any],
    fixture: TemporalFixture,
) -> TemporalFixtureResult:
    bundle = adapt_target_from_full_snapshot(
        asset_snapshot,
        target_id=fixture.target_id,
    )
    event_context = _event_overlay(fixture)
    profile = build_temporal_environment_from_assets(
        _natal_profile(),
        bundle,
        event_relative_context=event_context,
    )

    statuses = tuple(sorted(item.status for item in profile.event_relative_context))
    routing_facts = tuple(
        sorted(
            {
                fact
                for item in profile.event_relative_context
                for fact in item.routing_facts
            }
        )
    )
    return TemporalFixtureResult(
        fixture_id=fixture.fixture_id,
        profile_id=profile.profile_id,
        active_layers=profile.active_layers,
        event_relative_statuses=statuses,
        routing_facts=routing_facts,
        external_event_trigger_used=profile.external_event_trigger_used,
    )


def validate_temporal_fixture(
    fixture: TemporalFixture,
    result: TemporalFixtureResult,
) -> None:
    if result.active_layers != fixture.expected_active_layers:
        raise AssertionError(
            f"{fixture.fixture_id}: expected layers "
            f"{fixture.expected_active_layers}, got {result.active_layers}"
        )

    if fixture.expected_event_relative_status is None:
        if result.event_relative_statuses:
            raise AssertionError(
                f"{fixture.fixture_id}: expected no event-relative overlay"
            )
    elif fixture.expected_event_relative_status not in result.event_relative_statuses:
        raise AssertionError(
            f"{fixture.fixture_id}: expected event-relative status "
            f"{fixture.expected_event_relative_status}, "
            f"got {result.event_relative_statuses}"
        )

    missing = sorted(
        set(fixture.expected_routing_facts_all) - set(result.routing_facts)
    )
    if missing:
        raise AssertionError(
            f"{fixture.fixture_id}: missing expected routing facts {missing}"
        )

    if (
        result.external_event_trigger_used
        != fixture.expected_external_event_trigger_used
    ):
        raise AssertionError(
            f"{fixture.fixture_id}: external_event_trigger_used expected "
            f"{fixture.expected_external_event_trigger_used}, "
            f"got {result.external_event_trigger_used}"
        )


def run_temporal_fixture_benchmark(
    asset_fixture_path: str | Path,
    fixture_path: str | Path,
) -> tuple[TemporalFixtureResult, ...]:
    asset_snapshot = json.loads(
        Path(asset_fixture_path).read_text(encoding="utf-8")
    )
    results: list[TemporalFixtureResult] = []

    for fixture in load_temporal_fixtures(fixture_path):
        first = run_temporal_fixture(asset_snapshot, fixture)
        second = run_temporal_fixture(asset_snapshot, fixture)

        if first.profile_id != second.profile_id:
            raise AssertionError(
                f"{fixture.fixture_id}: repeated run changed profile_id"
            )

        validate_temporal_fixture(fixture, first)
        results.append(first)

    return tuple(results)

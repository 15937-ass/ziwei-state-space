from pathlib import Path

from src.product.temporal_fixture_benchmark import (
    load_temporal_fixtures,
    run_temporal_fixture_benchmark,
)


ROOT = Path(__file__).resolve().parents[1]
ASSET = ROOT / "product/PL3T_TEMPORAL_ASSET_FIXTURE_v0.2.json"
FIXTURES = ROOT / "product/PL3T_TEMPORAL_FIXTURES_v0.1.json"


def test_temporal_fixture_registry_loads_four_contract_cases():
    fixtures = load_temporal_fixtures(FIXTURES)
    assert len(fixtures) == 4
    assert {item.fixture_id for item in fixtures} == {
        "TF01_BASE_TEMPORAL_ENVIRONMENT",
        "TF02_MIGRATION_YEAR_2_ACTIVE",
        "TF03_MIGRATION_YEAR_4_INACTIVE",
        "TF04_MIGRATION_TRAVEL_ONLY_INACTIVE",
    }


def test_temporal_fixture_benchmark_passes_all_contract_cases():
    results = run_temporal_fixture_benchmark(ASSET, FIXTURES)
    assert len(results) == 4

    by_id = {item.fixture_id: item for item in results}
    assert not by_id["TF01_BASE_TEMPORAL_ENVIRONMENT"].external_event_trigger_used
    assert by_id["TF02_MIGRATION_YEAR_2_ACTIVE"].external_event_trigger_used
    assert not by_id["TF03_MIGRATION_YEAR_4_INACTIVE"].external_event_trigger_used
    assert (
        "projection_priority:migration_palace:primary"
        in by_id["TF02_MIGRATION_YEAR_2_ACTIVE"].routing_facts
    )


def test_temporal_benchmark_does_not_require_production_reaction_registry():
    results = run_temporal_fixture_benchmark(ASSET, FIXTURES)
    assert all(result.active_layers for result in results)

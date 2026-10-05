import json
from pathlib import Path

from src.product.natal_fixture_benchmark import (
    load_natal_fixtures,
    run_natal_fixture,
    run_natal_fixture_benchmark,
)


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "product/PL3N_NATAL_FIXTURES_v0.1.json"


def test_all_pl3n_contract_fixtures_pass():
    results = run_natal_fixture_benchmark(ROOT, FIXTURES)
    assert len(results) == 4
    assert {result.fixture_id for result in results} == {
        "NF01_W01_067_FIRE_KONG_JI",
        "NF02_LU_MA_JIAO_CHI",
        "NF03_BAIGUAN_PARTIAL_NOT_PREDICATE",
        "NF04_BAIGUAN_TIANFU_EMPTY_CONFLICT",
    }


def test_fixture_profile_ids_are_deterministic_even_if_not_frozen_yet():
    fixtures = load_natal_fixtures(FIXTURES)
    for fixture in fixtures:
        a = run_natal_fixture(ROOT, fixture)
        b = run_natal_fixture(ROOT, fixture)
        assert a.profile_id == b.profile_id
        assert a == b


def test_fixture_spec_is_contract_only_not_empirical_accuracy_data():
    payload = json.loads(FIXTURES.read_text(encoding="utf-8"))
    assert payload["policy"]["empirical_accuracy_claim"] is False
    assert payload["policy"]["golden_profile_id_frozen"] is False
    text = FIXTURES.read_text(encoding="utf-8").lower()
    assert "probability" not in text
    assert "user_feedback" not in text

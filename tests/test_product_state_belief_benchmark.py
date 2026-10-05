import json
from pathlib import Path

from src.product.state_belief_benchmark import run_state_belief_benchmark

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "product/PL3S_STATE_BELIEF_FIXTURES_v0.1.json"


def test_state_belief_fixture_benchmark_passes_all_contract_cases():
    document = json.loads(FIXTURES.read_text(encoding="utf-8"))
    report = run_state_belief_benchmark(document)
    assert report.total == 5
    assert report.passed == 5
    assert report.failed == 0
    assert report.all_passed


def test_state_belief_benchmark_is_deterministic():
    document = json.loads(FIXTURES.read_text(encoding="utf-8"))
    first = run_state_belief_benchmark(document)
    second = run_state_belief_benchmark(document)
    assert first == second

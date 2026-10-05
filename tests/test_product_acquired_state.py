import copy
import json
from pathlib import Path

import pytest

from src.product.acquired_state import compile_acquired_state

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "product/PL3S_ACQUIRED_STATE_FIXTURE_v0.1.json"


def _payload():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_acquired_state_compiles_with_deterministic_id():
    first = compile_acquired_state(_payload())
    second = compile_acquired_state(_payload())
    assert first.state_id == second.state_id
    assert first.state_id.startswith("ASTATE-")
    assert first.person_key == "PERSON-FX-001"
    assert first.assertions[0].domain == "CAREER"


def test_input_order_does_not_change_state_id():
    payload = _payload()
    first = compile_acquired_state(payload)

    shuffled = copy.deepcopy(payload)
    shuffled["assertions"] = list(reversed(shuffled["assertions"]))
    shuffled["context_items"] = list(reversed(shuffled["context_items"]))
    shuffled["source_observation_ids"] = list(
        reversed(shuffled["source_observation_ids"])
    )
    second = compile_acquired_state(shuffled)

    assert first.state_id == second.state_id


def test_unknown_value_must_use_missingness_not_null_assertion():
    payload = _payload()
    payload["assertions"][0]["value"] = None
    with pytest.raises(ValueError, match="use missingness"):
        compile_acquired_state(payload)


def test_item_provenance_must_be_in_profile_observation_refs():
    payload = _payload()
    payload["assertions"][0]["observation_refs"] = ["OBS-NOT-LINKED"]
    with pytest.raises(ValueError, match="included in source_observation_ids"):
        compile_acquired_state(payload)


def test_canonical_or_probability_fields_are_rejected():
    payload = _payload()
    payload["natal_profile_id"] = "NATAL-LEAK"
    with pytest.raises(ValueError, match="cannot contain canonical/empirical"):
        compile_acquired_state(payload)

    payload = _payload()
    payload["population_probability"] = 0.9
    with pytest.raises(ValueError, match="cannot contain canonical/empirical"):
        compile_acquired_state(payload)


def test_conflict_requires_existing_distinct_fact_ids():
    payload = _payload()
    payload["conflicts"] = [
        {
            "conflict_id": "CF-STATE-001",
            "domain": "CAREER",
            "key": "employment_status",
            "fact_ids": ["SF-CAREER-001", "MISSING-FACT"],
            "status": "UNRESOLVED",
        }
    ]
    with pytest.raises(ValueError, match="unknown fact_ids"):
        compile_acquired_state(payload)


def test_supplied_state_id_must_match_content():
    payload = _payload()
    payload["state_id"] = "ASTATE-WRONG"
    with pytest.raises(ValueError, match="does not match"):
        compile_acquired_state(payload)

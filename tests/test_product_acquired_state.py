import json
from dataclasses import replace
from pathlib import Path

import pytest

from src.product.acquired_state import (
    ACQUIRED_STATE_DOMAINS,
    AcquiredStateEntry,
    MissingStateDimension,
    ObservationProvenance,
    RealityContextRecord,
    StateContradiction,
    build_acquired_state_profile,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "product/PL3S_ACQUIRED_STATE_FIXTURE_v0.1.json"


def _provenance():
    return (
        ObservationProvenance(
            observation_ref="OBS-1",
            source_type="USER_CONFIRMED",
            observed_at="2030-01-15",
            confirmed=True,
            source_ref="CHECKIN-1",
        ),
        ObservationProvenance(
            observation_ref="OBS-2",
            source_type="ACTION_LOG",
            observed_at="2030-01-15",
            confirmed=True,
            source_ref="ACTION-1",
        ),
    )


def _entries():
    return (
        AcquiredStateEntry(
            domain="CAREER",
            state_key="employment_status",
            value="EMPLOYED",
            status="KNOWN",
            confidence="CONFIRMED",
            provenance_refs=("OBS-1",),
        ),
        AcquiredStateEntry(
            domain="RESOURCE",
            state_key="debt_state",
            value=None,
            status="UNKNOWN",
            confidence="UNKNOWN",
        ),
    )


def _context():
    return (
        RealityContextRecord(
            record_id="ACT-1",
            record_type="ACTION",
            domain="CAREER",
            key="job_application",
            value="SUBMITTED",
            status="CONFIRMED",
            provenance_refs=("OBS-2",),
        ),
    )


def test_schema_domains_are_reality_domains_not_palace_ids():
    assert ACQUIRED_STATE_DOMAINS == {
        "RELATIONSHIP",
        "CAREER",
        "RESOURCE",
        "RELOCATION",
        "COMMITMENT",
        "EXPOSURE",
    }


def test_same_normalized_state_is_deterministic_across_input_order():
    first = build_acquired_state_profile(
        person_key="PERSON-X",
        as_of="2030-01-15",
        entries=_entries(),
        reality_context=_context(),
        provenance=_provenance(),
    )
    second = build_acquired_state_profile(
        person_key="PERSON-X",
        as_of="2030-01-15",
        entries=tuple(reversed(_entries())),
        reality_context=tuple(reversed(_context())),
        provenance=tuple(reversed(_provenance())),
    )
    assert first.state_id == second.state_id
    assert first.state_id.startswith("STATE-")


def test_known_state_requires_provenance():
    with pytest.raises(ValueError, match="requires observation provenance"):
        AcquiredStateEntry(
            domain="CAREER",
            state_key="employment_status",
            value="EMPLOYED",
            status="KNOWN",
            confidence="CONFIRMED",
        )


def test_unknown_is_not_negative_or_known_value():
    with pytest.raises(ValueError, match="value=None"):
        AcquiredStateEntry(
            domain="RELATIONSHIP",
            state_key="relationship_status",
            value="SINGLE",
            status="UNKNOWN",
            confidence="UNKNOWN",
        )


def test_action_is_separate_from_state_entry():
    profile = build_acquired_state_profile(
        person_key="PERSON-X",
        as_of="2030-01-15",
        entries=_entries(),
        reality_context=_context(),
        provenance=_provenance(),
    )
    assert profile.entries[0].state_key == "employment_status"
    assert profile.reality_context[0].record_type == "ACTION"


def test_unknown_provenance_reference_fails_closed():
    entry = replace(_entries()[0], provenance_refs=("OBS-NOT-FOUND",))
    with pytest.raises(ValueError, match="unknown observation provenance"):
        build_acquired_state_profile(
            person_key="PERSON-X",
            as_of="2030-01-15",
            entries=(entry,),
            provenance=_provenance(),
        )


def test_duplicate_state_key_requires_contradiction_routing():
    one = _entries()[0]
    two = replace(one, value="UNEMPLOYED")
    with pytest.raises(ValueError, match="route disagreement through contradictions"):
        build_acquired_state_profile(
            person_key="PERSON-X",
            as_of="2030-01-15",
            entries=(one, two),
            provenance=_provenance(),
        )


def test_contradiction_requires_two_provenance_refs():
    with pytest.raises(ValueError, match="at least two"):
        StateContradiction(
            contradiction_id="C-1",
            domain="CAREER",
            state_key="employment_status",
            provenance_refs=("OBS-1",),
        )


def test_long_raw_narrative_is_rejected():
    with pytest.raises(ValueError, match="raw narrative"):
        AcquiredStateEntry(
            domain="CAREER",
            state_key="note",
            value="x" * 300,
            status="KNOWN",
            confidence="CONFIRMED",
            provenance_refs=("OBS-1",),
        )


def test_forbidden_cross_layer_flags_fail_closed():
    profile = build_acquired_state_profile(
        person_key="PERSON-X",
        as_of="2030-01-15",
        entries=_entries(),
        provenance=_provenance(),
    )
    with pytest.raises(ValueError, match="cannot mutate natal/temporal"):
        replace(profile, natal_truth_mutated=True)


def test_fixture_builds_without_inference():
    doc = json.loads(FIXTURE.read_text(encoding="utf-8"))
    provenance = tuple(ObservationProvenance(**item) for item in doc["provenance"])
    entries = tuple(
        AcquiredStateEntry(
            **{**item, "provenance_refs": tuple(item["provenance_refs"])}
        )
        for item in doc["entries"]
    )
    context = tuple(
        RealityContextRecord(
            **{**item, "provenance_refs": tuple(item["provenance_refs"])}
        )
        for item in doc["reality_context"]
    )
    missing = tuple(MissingStateDimension(**item) for item in doc["missingness"])
    contradictions = tuple(
        StateContradiction(
            **{**item, "provenance_refs": tuple(item["provenance_refs"])}
        )
        for item in doc["contradictions"]
    )
    profile = build_acquired_state_profile(
        person_key=doc["person_key"],
        as_of=doc["as_of"],
        entries=entries,
        reality_context=context,
        missingness=missing,
        contradictions=contradictions,
        provenance=provenance,
    )
    assert profile.person_key == "PERSON-DEMO-001"
    assert len(profile.entries) == 3
    assert profile.empirical_probability_used is False
    assert profile.outcome_prediction_used is False

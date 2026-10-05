import copy
import json
from pathlib import Path

import pytest

from src.product.acquired_state import compile_acquired_state
from src.product.state_quality import (
    audit_acquired_state_quality,
    select_ready_observed_slots,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "product/PL3S_ACQUIRED_STATE_FIXTURE_v0.1.json"


def _payload():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_fixture_distinguishes_observed_and_missing_without_imputation():
    state = compile_acquired_state(_payload())
    report = audit_acquired_state_quality(state)
    assert report.observed_count == 2
    assert report.missing_count == 1
    assert report.conflicted_count == 0
    assert report.has_blockers is True
    missing = next(row for row in report.slots if row.status == "MISSING")
    assert missing.domain == "RESOURCE"
    assert missing.key == "liquid_asset_level"
    assert missing.missingness_reason == "NOT_ASKED"
    assert missing.values == ()


def test_missing_is_never_promoted_to_false_or_zero():
    state = compile_acquired_state(_payload())
    report = audit_acquired_state_quality(state)
    row = next(row for row in report.slots if row.status == "MISSING")
    assert row.disposition == "HOLD_MISSING"
    assert row.fact_ids == ()
    assert row.values == ()


def test_unresolved_conflict_is_held_not_resolved():
    payload = _payload()
    payload["assertions"].append(
        {
            "fact_id": "SF-CAREER-002",
            "domain": "CAREER",
            "key": "employment_status",
            "value": "UNEMPLOYED",
            "status": "REPORTED",
            "confidence": "MEDIUM",
            "valid_from": "2027-06-20",
            "valid_through": None,
            "observation_refs": ["OBS-STATE-002"],
            "source_note": "second report",
        }
    )
    payload["conflicts"] = [
        {
            "conflict_id": "CF-CAREER-001",
            "domain": "CAREER",
            "key": "employment_status",
            "fact_ids": ["SF-CAREER-001", "SF-CAREER-002"],
            "status": "UNRESOLVED",
        }
    ]
    state = compile_acquired_state(payload)
    report = audit_acquired_state_quality(state)
    row = next(
        item
        for item in report.slots
        if item.domain == "CAREER" and item.key == "employment_status"
    )
    assert row.status == "CONFLICTED"
    assert row.disposition == "HOLD_CONFLICT"
    assert set(row.values) == {"EMPLOYED", "UNEMPLOYED"}
    assert report.conflicted_count == 1


def test_contradictory_values_without_conflict_fail_closed():
    payload = _payload()
    payload["assertions"].append(
        {
            "fact_id": "SF-CAREER-002",
            "domain": "CAREER",
            "key": "employment_status",
            "value": "UNEMPLOYED",
            "status": "REPORTED",
            "confidence": "MEDIUM",
            "valid_from": "2027-06-20",
            "valid_through": None,
            "observation_refs": ["OBS-STATE-002"],
            "source_note": None,
        }
    )
    state = compile_acquired_state(payload)
    with pytest.raises(ValueError, match="without StateConflict"):
        audit_acquired_state_quality(state)


def test_observed_and_missing_same_slot_fail_closed():
    payload = _payload()
    payload["missingness"].append(
        {
            "domain": "CAREER",
            "key": "employment_status",
            "reason": "UNKNOWN",
            "last_observed_date": None,
        }
    )
    state = compile_acquired_state(payload)
    with pytest.raises(ValueError, match="both observed and missing"):
        audit_acquired_state_quality(state)


def test_confidence_labels_are_preserved_not_converted_to_probability():
    state = compile_acquired_state(_payload())
    report = audit_acquired_state_quality(state)
    row = next(
        item
        for item in report.slots
        if item.domain == "CAREER" and item.key == "employment_status"
    )
    assert row.confidence_labels == ("HIGH",)
    assert report.probability_calibration_used is False
    assert report.imputation_used is False
    assert report.conflict_resolution_used is False


def test_ready_selector_excludes_missing_and_conflicted_slots():
    payload = _payload()
    state = compile_acquired_state(payload)
    report = audit_acquired_state_quality(state)
    ready = select_ready_observed_slots(report)
    assert all(item.status == "OBSERVED" for item in ready)
    assert {(item.domain, item.key) for item in ready} == {
        ("CAREER", "employment_status"),
        ("RELOCATION", "distant_settlement_status"),
    }


def test_audit_is_deterministic():
    state = compile_acquired_state(_payload())
    first = audit_acquired_state_quality(state)
    second = audit_acquired_state_quality(state)
    assert first.to_dict() == second.to_dict()

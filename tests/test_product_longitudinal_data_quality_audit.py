import copy
import json
from pathlib import Path

from src.product.longitudinal_data_quality_audit import (
    audit_longitudinal_data_quality,
)
from src.product.longitudinal_observation_v02 import (
    migrate_longitudinal_observation_v01_to_v02,
)

ROOT = Path(__file__).resolve().parents[1]
OBSERVATIONS = ROOT / "product/PL7_LONGITUDINAL_OBSERVATION_FIXTURES_v0.1.json"
PLANS = ROOT / "product/PL7_PROSPECTIVE_CHECKIN_FIXTURES_v0.1.json"


def _observations():
    return json.loads(OBSERVATIONS.read_text(encoding="utf-8"))["fixtures"]


def _plans():
    return json.loads(PLANS.read_text(encoding="utf-8"))["fixtures"]


def _response(plan_id, target_id, checkpoint_id, answer, response_date, **overrides):
    payload = {
        "schema_version": "0.1",
        "record_id": f"RESP-{plan_id}-{target_id}-{checkpoint_id}",
        "plan_id": plan_id,
        "target_id": target_id,
        "checkpoint_id": checkpoint_id,
        "answer": answer,
        "response_date": response_date,
        "user_confirmed": True,
        "event_time_report": None,
    }
    payload.update(overrides)
    return payload


def _complete_responses():
    return [
        _response(
            "CP-FX-BLIND-001",
            "T-CAR-CHANGE",
            "CLOSE",
            "YES",
            "2028-01-02",
            event_time_report={"precision": "DAY", "value": "2027-05-12"},
        ),
        _response(
            "CP-FX-BLIND-001",
            "T-REL-NEW",
            "CLOSE",
            "NO",
            "2028-01-02",
        ),
        _response(
            "CP-FX-PERS-001",
            "T-WEA-CHANGE",
            "CLOSE",
            "NO",
            "2027-07-02",
        ),
    ]


def _codes(report):
    return {finding["code"] for finding in report["findings"]}


def test_fixture_audit_is_deterministic_and_does_not_claim_real_cohort_quality():
    report = audit_longitudinal_data_quality(
        observations=_observations(),
        plans=_plans(),
        checkin_responses=_complete_responses(),
    )
    encoded = json.dumps(report, sort_keys=True, ensure_ascii=False)
    assert encoded == json.dumps(
        audit_longitudinal_data_quality(
            observations=_observations(),
            plans=_plans(),
            checkin_responses=_complete_responses(),
        ),
        sort_keys=True,
        ensure_ascii=False,
    )
    assert report["status"] == "PASS"
    assert report["input_scope"]["cohort_origin"] == "NOT_ASSERTED_BY_AUDIT"
    assert report["input_scope"]["external_data_accessed"] is False
    assert "VISIBLE_FORECAST_EXPOSURE_REVIEW" in _codes(report)


def test_empty_inputs_are_not_misreported_as_a_successful_audit():
    report = audit_longitudinal_data_quality()
    assert report["status"] == "NO_DATA"
    assert report["counts"]["valid_observations"] == 0


def test_v02_observation_is_validated_through_existing_compiler():
    payload = migrate_longitudinal_observation_v01_to_v02(_observations()[0])
    report = audit_longitudinal_data_quality(observations=[payload])
    assert report["counts"]["valid_observations"] == 1
    assert report["status"] == "PASS"


def test_exact_duplicate_observation_id_is_reported_without_deduplication():
    record = _observations()[0]
    report = audit_longitudinal_data_quality(observations=[record, copy.deepcopy(record)])
    assert "DUPLICATE_OBSERVATION_RECORD_ID" in _codes(report)
    assert report["counts"]["valid_observations"] == 2


def test_observation_id_collision_is_distinguished_from_exact_duplicate():
    first = _observations()[0]
    second = copy.deepcopy(first)
    second["outcome"]["status"] = "EVENT_NOT_OCCURRED"
    second["outcome"]["event_date"] = None
    report = audit_longitudinal_data_quality(observations=[first, second])
    assert "OBSERVATION_RECORD_ID_COLLISION" in _codes(report)


def test_conflicting_resolved_outcomes_on_overlapping_windows_are_flagged():
    occurred = _observations()[0]
    not_occurred = copy.deepcopy(occurred)
    not_occurred["record_id"] = "LO-CONFLICT-001"
    not_occurred["outcome"]["status"] = "EVENT_NOT_OCCURRED"
    not_occurred["outcome"]["event_date"] = None
    report = audit_longitudinal_data_quality(
        observations=[occurred, not_occurred]
    )
    assert "OVERLAPPING_WINDOW_OUTCOME_CONFLICT" in _codes(report)


def test_overlapping_windows_alone_are_not_classified_as_outcome_conflict():
    first = _observations()[0]
    second = copy.deepcopy(first)
    second["record_id"] = "LO-OVERLAP-001"
    report = audit_longitudinal_data_quality(observations=[first, second])
    assert "OVERLAPPING_WINDOW_OUTCOME_CONFLICT" not in _codes(report)


def test_overlapping_windows_do_not_conflict_when_event_is_after_negative_window():
    occurred = _observations()[0]
    occurred["outcome"]["event_date"] = "2027-12-15"
    negative = copy.deepcopy(occurred)
    negative["record_id"] = "LO-NEGATIVE-JUN-001"
    negative["outcome"]["status"] = "EVENT_NOT_OCCURRED"
    negative["outcome"]["event_date"] = None
    negative["window"]["end_date"] = "2027-06-30"
    negative["window"]["observed_through"] = "2027-06-30"

    report = audit_longitudinal_data_quality(observations=[occurred, negative])
    codes = _codes(report)
    assert "OVERLAPPING_WINDOW_OUTCOME_CONFLICT" not in codes
    assert "OVERLAPPING_WINDOW_EVENT_TIME_AMBIGUITY" not in codes


def test_event_after_observed_through_does_not_conflict_with_early_negative():
    occurred = _observations()[0]
    negative = copy.deepcopy(occurred)
    negative["record_id"] = "LO-NEGATIVE-EARLY-001"
    negative["outcome"]["status"] = "EVENT_NOT_OCCURRED"
    negative["outcome"]["event_date"] = None
    negative["window"]["observed_through"] = "2027-05-31"

    report = audit_longitudinal_data_quality(observations=[occurred, negative])
    codes = _codes(report)
    assert "OVERLAPPING_WINDOW_OUTCOME_CONFLICT" not in codes
    assert "OVERLAPPING_WINDOW_EVENT_TIME_AMBIGUITY" not in codes


def test_partial_v02_event_interval_overlap_is_reviewed_not_called_conflict():
    occurred = migrate_longitudinal_observation_v01_to_v02(_observations()[0])
    occurred["outcome"]["event_time"] = {
        "precision": "INTERVAL",
        "lower_bound_date": "2027-06-15",
        "upper_bound_date": "2027-07-15",
    }
    negative = copy.deepcopy(_observations()[0])
    negative["record_id"] = "LO-NEGATIVE-JUL-001"
    negative["outcome"]["status"] = "EVENT_NOT_OCCURRED"
    negative["outcome"]["event_date"] = None
    negative["window"]["start_date"] = "2027-07-01"
    negative["window"]["end_date"] = "2027-12-31"
    negative["window"]["observed_through"] = "2027-12-31"

    report = audit_longitudinal_data_quality(observations=[occurred, negative])
    codes = _codes(report)
    assert "OVERLAPPING_WINDOW_EVENT_TIME_AMBIGUITY" in codes
    assert "OVERLAPPING_WINDOW_OUTCOME_CONFLICT" not in codes


def test_target_ontology_version_drift_is_flagged_without_claiming_registry_validation():
    first = _observations()[0]
    second = copy.deepcopy(first)
    second["record_id"] = "LO-ONTOLOGY-001"
    second["target"]["ontology_version"] = "MANIFESTATION-0.2"
    report = audit_longitudinal_data_quality(observations=[first, second])
    assert "TARGET_ONTOLOGY_VERSION_DRIFT" in _codes(report)
    assert "TARGET_DEFINITION_DRIFT" not in _codes(report)


def test_missing_window_close_responses_are_not_negative_samples():
    report = audit_longitudinal_data_quality(plans=[_plans()[0]])
    assert report["counts"]["missing_window_close_responses"] == 2
    assert "FOLLOW_UP_MISSING" in _codes(report)
    assert "POTENTIAL_INFORMATIVE_MISSINGNESS_REVIEW" in _codes(report)
    assert "EVENT_NOT_OCCURRED" not in {
        finding["code"] for finding in report["findings"]
    }


def test_duplicate_plan_target_checkpoint_responses_are_not_auto_selected():
    plan = _plans()[1]
    first = _response(
        plan["plan_id"], "T-WEA-CHANGE", "CLOSE", "NO", "2027-07-02"
    )
    second = _response(
        plan["plan_id"], "T-WEA-CHANGE", "CLOSE", "YES", "2027-07-02",
        event_time_report={"precision": "DAY", "value": "2027-05-12"},
    )
    second["record_id"] = "RESP-DUPLICATE-2"
    report = audit_longitudinal_data_quality(
        plans=[plan], checkin_responses=[first, second]
    )
    assert "DUPLICATE_PLAN_TARGET_CHECKPOINT_RESPONSE" in _codes(report)
    assert report["counts"]["complete_window_close_responses"] == 0
    assert report["counts"]["unresolved_window_close_responses"] == 1


def test_unmatched_plan_target_and_checkpoint_references_are_reported():
    plan = _plans()[0]
    responses = [
        _response(
            "NO-SUCH-PLAN", "T-CAR-CHANGE", "CLOSE", "NO", "2027-07-02"
        ),
        _response(
            plan["plan_id"], "NO-SUCH-TARGET", "CLOSE", "NO", "2027-07-02"
        ),
        _response(
            plan["plan_id"], "T-CAR-CHANGE", "NO-SUCH-CHECKPOINT",
            "NO", "2027-07-02"
        ),
    ]
    report = audit_longitudinal_data_quality(
        plans=[plan], checkin_responses=responses
    )
    codes = _codes(report)
    assert "UNMATCHED_PLAN_REFERENCE" in codes
    assert "UNMATCHED_TARGET_REFERENCE" in codes
    assert "UNMATCHED_CHECKPOINT_REFERENCE" in codes
    assert "FOLLOW_UP_MISSING" in codes


def test_no_response_and_unsure_remain_distinct_and_raise_review_flags():
    plan = _plans()[0]
    responses = [
        _response(plan["plan_id"], "T-CAR-CHANGE", "CLOSE", "NO_RESPONSE", "2028-01-02"),
        _response(plan["plan_id"], "T-REL-NEW", "CLOSE", "UNSURE", "2028-01-02"),
    ]
    report = audit_longitudinal_data_quality(
        plans=[plan], checkin_responses=responses
    )
    codes = _codes(report)
    assert "FOLLOW_UP_NO_RESPONSE" in codes
    assert "FOLLOW_UP_UNRESOLVED" in codes
    assert "POTENTIAL_INFORMATIVE_MISSINGNESS_REVIEW" in codes
    assert report["counts"]["window_close_no_response"] == 1


def test_midwindow_no_is_only_no_event_yet():
    plan = _plans()[0]
    response = _response(
        plan["plan_id"], "T-CAR-CHANGE", "Q2", "NO", "2027-06-30"
    )
    report = audit_longitudinal_data_quality(
        plans=[plan], checkin_responses=[response]
    )
    assert "MIDWINDOW_NO_NOT_NEGATIVE" in _codes(report)
    assert report["counts"]["missing_window_close_responses"] == 2


def test_unconfirmed_closeout_is_not_counted_as_complete():
    plan = _plans()[1]
    response = _response(
        plan["plan_id"], "T-WEA-CHANGE", "CLOSE", "NO", "2027-07-02",
        user_confirmed=False,
    )
    report = audit_longitudinal_data_quality(
        plans=[plan], checkin_responses=[response]
    )
    assert "FOLLOW_UP_NEEDS_CONFIRMATION" in _codes(report)
    assert report["counts"]["complete_window_close_responses"] == 0


def test_yes_closeout_without_event_time_detail_is_not_complete():
    plan = _plans()[1]
    response = _response(
        plan["plan_id"], "T-WEA-CHANGE", "CLOSE", "YES", "2027-07-02"
    )
    report = audit_longitudinal_data_quality(
        plans=[plan], checkin_responses=[response]
    )
    assert "FOLLOW_UP_EVENT_TIME_DETAIL_MISSING" in _codes(report)
    assert report["counts"]["complete_window_close_responses"] == 0


def test_invalid_observation_is_reported_without_aborting_the_audit():
    report = audit_longitudinal_data_quality(
        observations=[{"schema_version": "9", "record_id": "LO-BAD"}],
        plans=_plans(),
        checkin_responses=_complete_responses(),
    )
    assert "INVALID_OBSERVATION" in _codes(report)
    assert report["counts"]["valid_plans"] == 2


def test_target_definition_drift_is_reported():
    first = _observations()[0]
    second = copy.deepcopy(first)
    second["record_id"] = "LO-DEFINITION-DRIFT"
    second["target"]["event_type"] = "different_event_type"
    report = audit_longitudinal_data_quality(observations=[first, second])
    assert "TARGET_DEFINITION_DRIFT" in _codes(report)


def test_invalid_collection_type_is_review_required_not_no_data():
    report = audit_longitudinal_data_quality(observations="not-an-array")
    assert report["status"] == "REVIEW_REQUIRED"
    assert "INVALID_INPUT_COLLECTION" in _codes(report)


def test_duplicate_plan_id_is_ambiguous_for_response_join():
    plan = _plans()[0]
    response = _response(
        plan["plan_id"], "T-CAR-CHANGE", "CLOSE", "NO", "2028-01-02"
    )
    report = audit_longitudinal_data_quality(
        plans=[plan, copy.deepcopy(plan)],
        checkin_responses=[response],
    )
    assert "DUPLICATE_PLAN_ID" in _codes(report)
    assert "AMBIGUOUS_PLAN_REFERENCE" in _codes(report)
    assert report["counts"]["complete_window_close_responses"] == 0


def test_response_record_id_collision_is_reported():
    plan = _plans()[1]
    first = _response(
        plan["plan_id"], "T-WEA-CHANGE", "CLOSE", "NO", "2027-07-02"
    )
    second = _response(
        plan["plan_id"], "T-WEA-CHANGE", "CLOSE", "YES", "2027-07-02",
        event_time_report={"precision": "DAY", "value": "2027-05-12"},
    )
    second["record_id"] = first["record_id"]
    report = audit_longitudinal_data_quality(
        plans=[plan], checkin_responses=[first, second]
    )
    assert "RESPONSE_RECORD_ID_COLLISION" in _codes(report)
    assert "DUPLICATE_PLAN_TARGET_CHECKPOINT_RESPONSE" in _codes(report)


def test_invalid_response_schema_version_is_reported():
    plan = _plans()[1]
    response = _response(
        plan["plan_id"], "T-WEA-CHANGE", "CLOSE", "NO", "2027-07-02"
    )
    response["schema_version"] = "9"
    report = audit_longitudinal_data_quality(
        plans=[plan], checkin_responses=[response]
    )
    assert "INVALID_RESPONSE_SCHEMA_VERSION" in _codes(report)
    assert report["counts"]["complete_window_close_responses"] == 0
    assert report["counts"]["unresolved_window_close_responses"] == 1


def test_missing_response_record_id_is_not_counted_complete():
    plan = _plans()[1]
    response = _response(
        plan["plan_id"], "T-WEA-CHANGE", "CLOSE", "NO", "2027-07-02"
    )
    response.pop("record_id")
    report = audit_longitudinal_data_quality(
        plans=[plan], checkin_responses=[response]
    )
    assert "MISSING_RESPONSE_IDENTIFIER_FIELDS" in _codes(report)
    assert report["counts"]["complete_window_close_responses"] == 0

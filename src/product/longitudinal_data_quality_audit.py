"""Deterministic cross-record quality audit for PL7 longitudinal data.

This module reports reviewable data-quality findings. It does not repair or
deduplicate input, infer outcomes, classify missingness as MNAR, or alter
canonical Zi Wei semantics.
"""

from __future__ import annotations

from collections import defaultdict
from datetime import date
import json
from typing import Any, Mapping, Sequence

from .longitudinal_observation import compile_longitudinal_observation
from .longitudinal_observation_v02 import compile_longitudinal_observation_v02
from .prospective_checkin import (
    CHECKIN_ANSWERS,
    compile_prospective_checkin_plan,
)


def _is_sequence(value: Any) -> bool:
    return isinstance(value, Sequence) and not isinstance(
        value, (str, bytes, bytearray)
    )


def _text(value: Any) -> str:
    return str(value or "").strip()


def _parse_date(value: Any) -> date | None:
    text = _text(value)
    if not text:
        return None
    try:
        return date.fromisoformat(text)
    except ValueError:
        return None


def _overlaps(left_start: date, left_end: date, right_start: date, right_end: date) -> bool:
    return max(left_start, right_start) <= min(left_end, right_end)


def _finding_sort_key(item: Mapping[str, Any]) -> tuple[Any, ...]:
    severity_order = {"ERROR": 0, "WARNING": 1, "INFO": 2}
    return (
        severity_order.get(str(item.get("severity")), 3),
        str(item.get("code", "")),
        str(item.get("entity_type", "")),
        tuple(item.get("entity_ids", [])),
        json.dumps(item.get("details", {}), sort_keys=True, ensure_ascii=False),
    )


def audit_longitudinal_data_quality(
    observations: Sequence[Mapping[str, Any]] = (),
    plans: Sequence[Mapping[str, Any]] = (),
    checkin_responses: Sequence[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    """Audit caller-supplied PL7 records and return a stable JSON-ready report.

    Observation payloads may use schema v0.1 or v0.2. Plans are validated by
    the existing prospective check-in compiler. Check-in responses are audited
    against their plan/target/checkpoint references; they are not promoted to
    LongitudinalObservationRecord by this function.
    """

    findings: list[dict[str, Any]] = []

    def emit(
        code: str,
        severity: str,
        entity_type: str,
        entity_ids: Sequence[str] = (),
        details: Mapping[str, Any] | None = None,
    ) -> None:
        ids = sorted({_text(value) for value in entity_ids if _text(value)})
        findings.append(
            {
                "code": code,
                "severity": severity,
                "entity_type": entity_type,
                "entity_ids": ids,
                "details": dict(details or {}),
            }
        )

    def rows(value: Any, collection: str) -> tuple[list[Mapping[str, Any]], int]:
        if value is None:
            return [], 0
        if not _is_sequence(value):
            emit(
                "INVALID_INPUT_COLLECTION",
                "ERROR",
                collection,
                details={"expected": "array"},
            )
            return [], 0
        parsed: list[Mapping[str, Any]] = []
        for index, item in enumerate(value):
            if not isinstance(item, Mapping):
                emit(
                    f"INVALID_{collection.upper()}_ROW",
                    "ERROR",
                    collection,
                    [f"row:{index}"],
                    {"expected": "object"},
                )
                continue
            parsed.append(dict(item))
        return parsed, len(value)

    observation_rows, observations_supplied = rows(observations, "observations")
    plan_rows, plans_supplied = rows(plans, "plans")
    response_rows, responses_supplied = rows(checkin_responses, "checkin_responses")

    def duplicate_ids(
        items: Sequence[Mapping[str, Any]],
        field: str,
        entity_type: str,
        exact_code: str,
        collision_code: str,
    ) -> dict[str, list[Mapping[str, Any]]]:
        grouped: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
        for item in items:
            identifier = _text(item.get(field))
            if identifier:
                grouped[identifier].append(item)
        for identifier, group in sorted(grouped.items()):
            if len(group) < 2:
                continue
            exact = all(dict(item) == dict(group[0]) for item in group[1:])
            emit(
                exact_code if exact else collision_code,
                "WARNING" if exact else "ERROR",
                entity_type,
                [identifier],
                {
                    "occurrences": len(group),
                    "payloads_identical": exact,
                    "action": "review_only_no_auto_deduplication",
                },
            )
        return grouped

    duplicate_ids(
        observation_rows,
        "record_id",
        "observation",
        "DUPLICATE_OBSERVATION_RECORD_ID",
        "OBSERVATION_RECORD_ID_COLLISION",
    )
    plan_id_groups = duplicate_ids(
        plan_rows,
        "plan_id",
        "plan",
        "DUPLICATE_PLAN_ID",
        "PLAN_ID_COLLISION",
    )
    duplicate_ids(
        response_rows,
        "record_id",
        "checkin_response",
        "DUPLICATE_RESPONSE_RECORD_ID",
        "RESPONSE_RECORD_ID_COLLISION",
    )

    valid_observations: list[dict[str, Any]] = []
    target_definitions: dict[str, set[tuple[str, str, str, str]]] = defaultdict(set)
    target_versions: dict[str, set[str]] = defaultdict(set)

    for index, payload in enumerate(observation_rows):
        record_id = _text(payload.get("record_id")) or f"row:{index}"
        version = _text(payload.get("schema_version"))
        event_time_start: date | None = None
        event_time_end: date | None = None
        try:
            if version == "0.1":
                compiled = compile_longitudinal_observation(payload)
                base = compiled
                if base.event_date is not None:
                    event_time_start = base.event_date
                    event_time_end = base.event_date
            elif version == "0.2":
                compiled_v02 = compile_longitudinal_observation_v02(payload)
                base = compiled_v02.base
                if compiled_v02.event_time is not None:
                    event_time_start = compiled_v02.event_time.lower_bound
                    event_time_end = compiled_v02.event_time.upper_bound
            else:
                raise ValueError(f"unsupported schema_version: {version or '(missing)'}")
        except (ValueError, TypeError, KeyError) as exc:
            emit(
                "INVALID_OBSERVATION",
                "ERROR",
                "observation",
                [record_id],
                {"schema_version": version or None, "reason": str(exc)},
            )
            continue

        definition = (
            base.domain,
            base.manifestation_family,
            base.event_type,
            base.ontology_version,
        )
        target_definitions[base.target_id].add(definition)
        target_versions[base.target_id].add(base.ontology_version)
        valid_observations.append(
            {
                "record_id": base.record_id,
                "person_key": base.person_key,
                "target_id": base.target_id,
                "definition": definition,
                "ontology_version": base.ontology_version,
                "window_start": base.window_start,
                "window_end": base.window_end,
                "observed_through": base.observed_through,
                "event_status": base.event_status,
                "observation_confidence": base.observation_confidence,
                "event_time_start": event_time_start,
                "event_time_end": event_time_end,
            }
        )

    valid_plans: list[Any] = []
    raw_plan_ids = {
        identifier for identifier, group in plan_id_groups.items() if len(group) > 1
    }
    for index, payload in enumerate(plan_rows):
        plan_id = _text(payload.get("plan_id")) or f"row:{index}"
        try:
            plan = compile_prospective_checkin_plan(payload)
        except (ValueError, TypeError, KeyError) as exc:
            emit(
                "INVALID_PLAN",
                "ERROR",
                "plan",
                [plan_id],
                {"reason": str(exc)},
            )
            continue
        valid_plans.append(plan)
        for target in plan.targets:
            definition = (
                target.domain,
                target.manifestation_family,
                target.event_type,
                target.ontology_version,
            )
            target_definitions[target.target_id].add(definition)
            target_versions[target.target_id].add(target.ontology_version)

    for target_id, versions in sorted(target_versions.items()):
        if len(versions) > 1:
            emit(
                "TARGET_ONTOLOGY_VERSION_DRIFT",
                "WARNING",
                "target",
                [target_id],
                {
                    "ontology_versions": sorted(versions),
                    "action": "review_version_migration_and_target_comparability",
                },
            )

    for target_id, definitions in sorted(target_definitions.items()):
        core_definitions = {definition[:3] for definition in definitions}
        if len(core_definitions) > 1:
            emit(
                "TARGET_DEFINITION_DRIFT",
                "ERROR",
                "target",
                [target_id],
                {
                    "definitions": [
                        {
                            "domain": definition[0],
                            "manifestation_family": definition[1],
                            "event_type": definition[2],
                            "ontology_version": definition[3],
                        }
                        for definition in sorted(definitions)
                    ],
                    "action": "manual_semantic_review_required",
                },
            )

    grouped_observations: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for record in valid_observations:
        grouped_observations[(record["person_key"], record["target_id"])].append(record)

    resolved = {"EVENT_OCCURRED", "EVENT_NOT_OCCURRED"}
    for (person_key, target_id), group in sorted(grouped_observations.items()):
        ordered = sorted(group, key=lambda row: (row["window_start"], row["window_end"], row["record_id"]))
        for left_index, left in enumerate(ordered):
            for right in ordered[left_index + 1 :]:
                if not _overlaps(
                    left["window_start"],
                    left["window_end"],
                    right["window_start"],
                    right["window_end"],
                ):
                    continue
                if {left["event_status"], right["event_status"]} != resolved:
                    continue

                occurred = left if left["event_status"] == "EVENT_OCCURRED" else right
                negative = left if left["event_status"] == "EVENT_NOT_OCCURRED" else right
                if (
                    occurred["observation_confidence"] == "INSUFFICIENT"
                    or negative["observation_confidence"] == "INSUFFICIENT"
                ):
                    continue

                event_start = occurred["event_time_start"]
                event_end = occurred["event_time_end"]
                if event_start is None or event_end is None:
                    continue

                # A negative record only covers the part of its target window
                # that was actually observed. Window overlap by itself is not
                # evidence of contradiction.
                negative_covered_end = min(
                    negative["observed_through"], negative["window_end"]
                )
                if negative_covered_end < negative["window_start"]:
                    continue
                if (
                    event_end < negative["window_start"]
                    or event_start > negative_covered_end
                ):
                    continue

                event_fully_observed = (
                    negative["window_start"] <= event_start
                    and event_end <= negative_covered_end
                )
                finding_code = (
                    "OVERLAPPING_WINDOW_OUTCOME_CONFLICT"
                    if event_fully_observed
                    else "OVERLAPPING_WINDOW_EVENT_TIME_AMBIGUITY"
                )
                emit(
                    finding_code,
                    "ERROR" if event_fully_observed else "WARNING",
                    "observation_pair",
                    [occurred["record_id"], negative["record_id"]],
                    {
                        "person_key": person_key,
                        "target_id": target_id,
                        "event_record_id": occurred["record_id"],
                        "negative_record_id": negative["record_id"],
                        "event_time_start": event_start.isoformat(),
                        "event_time_end": event_end.isoformat(),
                        "negative_observed_start": negative["window_start"].isoformat(),
                        "negative_observed_through": negative_covered_end.isoformat(),
                        "interpretation": (
                            "event time is fully within negative observation coverage"
                            if event_fully_observed
                            else "event-time interval only partially overlaps negative observation coverage"
                        ),
                    },
                )

    # Only uniquely identified, valid plans can anchor response references.
    plans_by_id: dict[str, Any] = {}
    for plan in valid_plans:
        if len(plan_id_groups.get(plan.plan_id, [])) == 1:
            plans_by_id[plan.plan_id] = plan

    expected_closeouts: dict[tuple[str, str, str], dict[str, Any]] = {}
    for plan_id, plan in sorted(plans_by_id.items()):
        closeouts = [checkpoint for checkpoint in plan.schedule if checkpoint.checkpoint_type == "WINDOW_CLOSE"]
        # The compiler requires exactly one WINDOW_CLOSE; retain a guard for audit resilience.
        if len(closeouts) != 1:
            emit(
                "PLAN_CLOSEOUT_CONTRACT_VIOLATION",
                "ERROR",
                "plan",
                [plan_id],
                {"window_close_count": len(closeouts)},
            )
            continue
        closeout = closeouts[0]
        for target in plan.targets:
            key = (plan_id, target.target_id, closeout.checkpoint_id)
            expected_closeouts[key] = {
                "person_key": plan.person_key,
                "window_end": plan.window_end.isoformat(),
                "collection_purpose": plan.collection_purpose,
                "prediction_exposure": plan.prediction_exposure,
            }
        if plan.prediction_exposure == "VISIBLE":
            emit(
                "VISIBLE_FORECAST_EXPOSURE_REVIEW",
                "INFO",
                "plan",
                [plan_id],
                {
                    "collection_purpose": plan.collection_purpose,
                    "action": "keep_separate_from_blind_benchmark",
                },
            )

    response_key_groups: dict[tuple[str, str, str], list[Mapping[str, Any]]] = defaultdict(list)
    for payload in response_rows:
        key = (
            _text(payload.get("plan_id")),
            _text(payload.get("target_id")),
            _text(payload.get("checkpoint_id")),
        )
        if all(key):
            response_key_groups[key].append(payload)

    duplicate_response_keys = {
        key for key, group in response_key_groups.items() if len(group) > 1
    }
    for key in sorted(duplicate_response_keys):
        emit(
            "DUPLICATE_PLAN_TARGET_CHECKPOINT_RESPONSE",
            "ERROR",
            "checkin_response_group",
            list(key),
            {
                "occurrences": len(response_key_groups[key]),
                "action": "do_not_select_a_winner_automatically",
            },
        )

    matched_response_keys: set[tuple[str, str, str]] = set()
    complete_closeout_keys: set[tuple[str, str, str]] = set()
    closeout_no_response_keys: set[tuple[str, str, str]] = set()
    unresolved_closeout_keys: set[tuple[str, str, str]] = set()

    for index, payload in enumerate(response_rows):
        response_id = _text(payload.get("record_id")) or f"row:{index}"
        response_schema_version = _text(payload.get("schema_version"))
        plan_id = _text(payload.get("plan_id"))
        target_id = _text(payload.get("target_id"))
        checkpoint_id = _text(payload.get("checkpoint_id"))
        key = (plan_id, target_id, checkpoint_id)
        missing_identifier_fields = [
            field
            for field, value in (
                ("record_id", payload.get("record_id")),
                ("plan_id", payload.get("plan_id")),
                ("target_id", payload.get("target_id")),
                ("checkpoint_id", payload.get("checkpoint_id")),
            )
            if not _text(value)
        ]
        if missing_identifier_fields:
            emit(
                "MISSING_RESPONSE_IDENTIFIER_FIELDS",
                "ERROR",
                "checkin_response",
                [response_id],
                {"fields": missing_identifier_fields},
            )
        if response_schema_version not in {"0.1", "0.2"}:
            emit(
                "INVALID_RESPONSE_SCHEMA_VERSION",
                "ERROR",
                "checkin_response",
                [response_id],
                {"schema_version": response_schema_version or None},
            )
        answer = _text(payload.get("answer"))
        response_date = _parse_date(payload.get("response_date"))
        refs_valid = True
        answer_valid = answer in CHECKIN_ANSWERS
        date_valid = response_date is not None

        if not answer_valid:
            emit(
                "INVALID_CHECKIN_ANSWER",
                "ERROR",
                "checkin_response",
                [response_id],
                {"answer": answer or None},
            )
        if not date_valid:
            emit(
                "INVALID_RESPONSE_DATE",
                "ERROR",
                "checkin_response",
                [response_id],
                {"response_date": payload.get("response_date")},
            )
        if not isinstance(payload.get("user_confirmed"), bool):
            emit(
                "INVALID_USER_CONFIRMATION_FLAG",
                "ERROR",
                "checkin_response",
                [response_id],
                {"user_confirmed": payload.get("user_confirmed")},
            )

        plan = plans_by_id.get(plan_id)
        if plan is None:
            refs_valid = False
            if plan_id in raw_plan_ids:
                emit(
                    "AMBIGUOUS_PLAN_REFERENCE",
                    "ERROR",
                    "checkin_response",
                    [response_id, plan_id],
                    {"action": "resolve_plan_id_collision_before_join"},
                )
            else:
                emit(
                    "UNMATCHED_PLAN_REFERENCE",
                    "ERROR",
                    "checkin_response",
                    [response_id, plan_id],
                    {},
                )
            checkpoint_type = None
        else:
            plan_targets = {target.target_id for target in plan.targets}
            if target_id not in plan_targets:
                refs_valid = False
                emit(
                    "UNMATCHED_TARGET_REFERENCE",
                    "ERROR",
                    "checkin_response",
                    [response_id, plan_id, target_id],
                    {},
                )
            checkpoints = {
                checkpoint.checkpoint_id: checkpoint.checkpoint_type
                for checkpoint in plan.schedule
            }
            checkpoint_type = checkpoints.get(checkpoint_id)
            if checkpoint_type is None:
                refs_valid = False
                emit(
                    "UNMATCHED_CHECKPOINT_REFERENCE",
                    "ERROR",
                    "checkin_response",
                    [response_id, plan_id, checkpoint_id],
                    {},
                )

        if refs_valid and all(key):
            matched_response_keys.add(key)

        if checkpoint_type == "MID_WINDOW" and answer == "NO" and refs_valid:
            emit(
                "MIDWINDOW_NO_NOT_NEGATIVE",
                "INFO",
                "checkin_response",
                [response_id],
                {
                    "action": "retain_as_no_event_yet; never promote_to_EVENT_NOT_OCCURRED",
                },
            )

        if checkpoint_type != "WINDOW_CLOSE" or not refs_valid:
            continue

        if answer == "NO_RESPONSE":
            closeout_no_response_keys.add(key)
            unresolved_closeout_keys.add(key)
            emit(
                "FOLLOW_UP_NO_RESPONSE",
                "WARNING",
                "checkin_response",
                [response_id, plan_id, target_id],
                {"action": "keep_outcome_unknown; do_not_create_negative_sample"},
            )
            emit(
                "POTENTIAL_INFORMATIVE_MISSINGNESS_REVIEW",
                "WARNING",
                "follow_up",
                [plan_id, target_id],
                {
                    "reason": "window_close_no_response",
                    "interpretation": "risk_flag_only_not_an_MNAR_classification",
                },
            )
            continue

        if answer == "UNSURE":
            unresolved_closeout_keys.add(key)
            emit(
                "FOLLOW_UP_UNRESOLVED",
                "WARNING",
                "checkin_response",
                [response_id, plan_id, target_id],
                {"action": "preserve_unknown_not_negative"},
            )
            continue

        if answer not in {"YES", "NO"}:
            unresolved_closeout_keys.add(key)
            continue

        if payload.get("user_confirmed") is not True:
            unresolved_closeout_keys.add(key)
            emit(
                "FOLLOW_UP_NEEDS_CONFIRMATION",
                "WARNING",
                "checkin_response",
                [response_id, plan_id, target_id],
                {"action": "do_not_promote_unconfirmed_candidate"},
            )
            continue

        if answer == "YES" and not (
            payload.get("event_time_report") or payload.get("event_date")
        ):
            unresolved_closeout_keys.add(key)
            emit(
                "FOLLOW_UP_EVENT_TIME_DETAIL_MISSING",
                "WARNING",
                "checkin_response",
                [response_id, plan_id, target_id],
                {"action": "request_event_time_detail_without_imputation"},
            )
            continue

        if (
            key not in duplicate_response_keys
            and answer_valid
            and date_valid
            and response_schema_version in {"0.1", "0.2"}
            and not missing_identifier_fields
        ):
            complete_closeout_keys.add(key)

    missing_closeout_keys = set(expected_closeouts) - matched_response_keys
    for plan_id, target_id, checkpoint_id in sorted(missing_closeout_keys):
        emit(
            "FOLLOW_UP_MISSING",
            "WARNING",
            "follow_up",
            [plan_id, target_id, checkpoint_id],
            {
                "window_end": expected_closeouts[(plan_id, target_id, checkpoint_id)]["window_end"],
                "action": "missing_follow_up_is_not_a_negative_outcome",
            },
        )
        emit(
            "POTENTIAL_INFORMATIVE_MISSINGNESS_REVIEW",
            "WARNING",
            "follow_up",
            [plan_id, target_id],
            {
                "reason": "no_window_close_response_supplied",
                "interpretation": "risk_flag_only_not_an_MNAR_classification",
            },
        )

    # Any matched closeout key that did not meet the complete-response contract
    # remains unresolved, including duplicate keys and malformed responses.
    unresolved_closeout_keys.update(
        key
        for key in expected_closeouts
        if key in matched_response_keys and key not in complete_closeout_keys
    )

    total_supplied = observations_supplied + plans_supplied + responses_supplied
    findings.sort(key=_finding_sort_key)
    severity_counts = {
        severity: sum(1 for item in findings if item["severity"] == severity)
        for severity in ("ERROR", "WARNING", "INFO")
    }
    if severity_counts["ERROR"] or severity_counts["WARNING"]:
        status = "REVIEW_REQUIRED"
    elif total_supplied == 0:
        status = "NO_DATA"
    else:
        status = "PASS"

    return {
        "schema_version": "0.1",
        "audit_id": "PL7_LONGITUDINAL_DATA_QUALITY_AUDIT_V0_1",
        "status": status,
        "input_scope": {
            "observations_supplied": observations_supplied,
            "plans_supplied": plans_supplied,
            "checkin_responses_supplied": responses_supplied,
            "external_data_accessed": False,
            "cohort_origin": "NOT_ASSERTED_BY_AUDIT",
        },
        "counts": {
            "valid_observations": len(valid_observations),
            "valid_plans": len(valid_plans),
            "expected_window_close_responses": len(expected_closeouts),
            "matched_window_close_responses": sum(
                1 for key in matched_response_keys if key in expected_closeouts
            ),
            "complete_window_close_responses": len(complete_closeout_keys),
            "missing_window_close_responses": len(missing_closeout_keys),
            "window_close_no_response": len(closeout_no_response_keys),
            "unresolved_window_close_responses": len(unresolved_closeout_keys),
            "potential_informative_missingness_flags": sum(
                1
                for item in findings
                if item["code"] == "POTENTIAL_INFORMATIVE_MISSINGNESS_REVIEW"
            ),
            "findings": len(findings),
            "errors": severity_counts["ERROR"],
            "warnings": severity_counts["WARNING"],
            "info": severity_counts["INFO"],
        },
        "missingness_interpretation": (
            "RISK_FLAGS_ONLY_NOT_AN_MNAR_CLASSIFICATION; nonresponse, UNKNOWN, "
            "and CENSORED are not EVENT_NOT_OCCURRED."
        ),
        "findings": findings,
    }

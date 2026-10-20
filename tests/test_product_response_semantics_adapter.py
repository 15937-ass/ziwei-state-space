import copy
import json
from collections import Counter
from pathlib import Path

import pytest

from src.product.response_semantics_adapter import (
    ACTIVATION_CLOSURE_PATH,
    CATEGORY_REVIEW_PATH,
    CAREER_ORDINAL_CONSTRAINTS_PATH,
    RESPONSE_PILOT_PATH,
    CareerResponseDecision,
    ResponseSemanticEnvelope,
    absence_evidence_ready,
    adapt_response_pilot_registry,
    adapt_response_semantics_record,
    audit_response_semantics_adapter_readiness,
    build_career_response_decisions,
    load_activation_closure,
    load_career_compatibility_records,
    load_career_ordinal_constraints,
    load_response_pilot_records,
    validate_real_adapter_zero_unlock,
)


ROOT = Path(__file__).resolve().parents[1]
SYNTHETIC = (
    ROOT / "product" / "RESPONSE_SEMANTICS_ADAPTER_SYNTHETIC_FIXTURE_v0.1.json"
)
READINESS = (
    ROOT / "product" / "RESPONSE_SEMANTICS_ADAPTER_READINESS_v0.1.json"
)


def _load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def _decision(rule_id):
    return next(
        item for item in build_career_response_decisions()
        if item.source_rule_id == rule_id
    )


def test_all_pilot_response_records_adapt_without_semantic_loss():
    raw_records = load_response_pilot_records()
    envelopes = adapt_response_pilot_registry()

    assert len(raw_records) == len(envelopes) == 8

    for raw, envelope in zip(raw_records, envelopes):
        assert isinstance(envelope, ResponseSemanticEnvelope)
        assert envelope.semantic_payload() == raw


def test_real_response_pilot_authorizes_zero_runtime_effects():
    envelopes = adapt_response_pilot_registry()

    assert Counter(
        item.knowledge_execution_status for item in envelopes
    ) == {
        "LEXICAL_ONLY": 4,
        "STRUCTURAL_ONLY": 4,
    }
    assert all(item.allowed_use == "SEMANTIC_ONLY" for item in envelopes)
    assert all(item.runtime_effect_allowed is False for item in envelopes)
    assert all(item.authorization_ref is None for item in envelopes)


def test_membership_never_invents_activation_quantifier():
    records = {item["record_id"]: item for item in load_response_pilot_records()}
    fire_bell = adapt_response_semantics_record(records["RS-GROUP-FIRE-BELL"])

    assert [item["id"] for item in fire_bell.members] == ["火星", "铃星"]
    assert fire_bell.activation["mode"] == "UNSPECIFIED"
    assert "ACTIVATION_UNSPECIFIED_NO_DEFAULT" in fire_bell.blockers
    assert fire_bell.runtime_effect_allowed is False


def test_named_composite_does_not_become_generic_shorthand():
    records = {item["record_id"]: item for item in load_response_pilot_records()}
    luma = records["RS-COMPOSITE-LUMA-JIAOCHI"]

    adapted = adapt_response_semantics_record(
        luma,
        application_term="禄马",
    )

    assert adapted.term == "禄马交驰"
    assert "NAMED_COMPOSITE_NOT_GENERIC_SHORTHAND" in adapted.blockers
    assert adapted.runtime_effect_allowed is False


def test_safe_symbolic_still_requires_separate_authorization():
    fixture = _load(SYNTHETIC)
    record = fixture["record"]

    adapted = adapt_response_semantics_record(
        record,
        requested_scope=fixture["requested_scope"],
        application_term=fixture["application_term"],
    )

    assert adapted.knowledge_execution_status == "SAFE_SYMBOLIC"
    assert adapted.allowed_use == "SEMANTIC_ONLY"
    assert adapted.runtime_effect_allowed is False
    assert adapted.authorization_ref is None
    assert adapted.blockers == ("EXPLICIT_EXECUTION_AUTHORIZATION_REQUIRED",)


def test_synthetic_explicit_authorization_can_pass_positive_path():
    fixture = _load(SYNTHETIC)

    adapted = adapt_response_semantics_record(
        fixture["record"],
        authorization_ref=fixture["authorization_ref"],
        requested_scope=fixture["requested_scope"],
        application_term=fixture["application_term"],
    )

    assert adapted.allowed_use == "EXECUTABLE"
    assert adapted.runtime_effect_allowed is True
    assert adapted.authorization_ref == fixture["authorization_ref"]
    assert adapted.blockers == ()


def test_authorization_cannot_override_non_safe_knowledge_status():
    record = copy.deepcopy(load_response_pilot_records()[0])

    adapted = adapt_response_semantics_record(
        record,
        authorization_ref="SYNTHETIC_AUTH:BAD",
    )

    assert adapted.runtime_effect_allowed is False
    assert adapted.allowed_use == "SEMANTIC_ONLY"
    assert "AUTHORIZATION_CANNOT_OVERRIDE_KNOWLEDGE_STATUS" in adapted.blockers


def test_authorization_cannot_invent_unspecified_activation():
    fixture = _load(SYNTHETIC)
    record = copy.deepcopy(fixture["record"])
    record["activation"]["mode"] = "UNSPECIFIED"

    adapted = adapt_response_semantics_record(
        record,
        authorization_ref=fixture["authorization_ref"],
        requested_scope=fixture["requested_scope"],
        application_term=fixture["application_term"],
    )

    assert adapted.runtime_effect_allowed is False
    assert "AUTHORIZATION_CANNOT_INVENT_ACTIVATION" in adapted.blockers


def test_local_scope_requires_explicit_binding_before_authorization():
    fixture = _load(SYNTHETIC)

    adapted = adapt_response_semantics_record(
        fixture["record"],
        authorization_ref=fixture["authorization_ref"],
        requested_scope=None,
        application_term=fixture["application_term"],
    )

    assert adapted.runtime_effect_allowed is False
    assert "LOCAL_SCOPE_BINDING_REQUIRED" in adapted.blockers


def test_local_scope_mismatch_fails_closed():
    fixture = _load(SYNTHETIC)
    bad_scope = dict(fixture["requested_scope"])
    bad_scope["domain"] = "OTHER_DOMAIN"

    adapted = adapt_response_semantics_record(
        fixture["record"],
        authorization_ref=fixture["authorization_ref"],
        requested_scope=bad_scope,
        application_term=fixture["application_term"],
    )

    assert adapted.runtime_effect_allowed is False
    assert "SCOPE_MISMATCH:domain" in adapted.blockers
    assert "AUTHORIZATION_CANNOT_OVERRIDE_SCOPE" in adapted.blockers


def test_named_composite_authorization_requires_exact_application_term():
    fixture = _load(SYNTHETIC)
    record = copy.deepcopy(fixture["record"])
    record["semantic_role"] = "NAMED_COMPOSITE"
    record["term"] = "SYNTHETIC_NAMED_COMPOSITE"

    missing_term = adapt_response_semantics_record(
        record,
        authorization_ref=fixture["authorization_ref"],
        requested_scope=fixture["requested_scope"],
    )
    wrong_term = adapt_response_semantics_record(
        record,
        authorization_ref=fixture["authorization_ref"],
        requested_scope=fixture["requested_scope"],
        application_term="SYNTHETIC_GENERIC",
    )

    assert missing_term.runtime_effect_allowed is False
    assert (
        "NAMED_COMPOSITE_APPLICATION_TERM_REQUIRED"
        in missing_term.blockers
    )
    assert wrong_term.runtime_effect_allowed is False
    assert "NAMED_COMPOSITE_NOT_GENERIC_SHORTHAND" in wrong_term.blockers


def test_career_response_and_activation_join_is_exact_251():
    compatibility = load_career_compatibility_records()
    activation = load_activation_closure()
    decisions = build_career_response_decisions()

    compat_ids = {item["source_rule_id"] for item in compatibility}
    activation_ids = {item["source_rule_id"] for item in activation["records"]}
    decision_ids = {item.source_rule_id for item in decisions}

    assert len(compatibility) == 251
    assert len(activation["records"]) == 251
    assert len(decisions) == 251
    assert compat_ids == activation_ids == decision_ids
    assert len(decision_ids) == 251


def test_career_adapter_preserves_knowledge_readiness_classes():
    decisions = build_career_response_decisions()

    assert Counter(item.knowledge_readiness_class for item in decisions) == {
        "MULTI_CLASS_BLOCKED": 59,
        "LOCAL_STRUCTURE_READY": 17,
        "SOURCE_UNDERDETERMINED": 127,
        "NORMALIZATION_DEFERRED": 21,
        "DEPENDENCY_COMPILER_GATED": 27,
    }
    assert Counter(item.adapter_status for item in decisions) == {
        "BLOCKED_MULTIPLE": 59,
        "SEMANTIC_ONLY_PENDING_COMPILATION": 17,
        "BLOCKED_SOURCE_UNDERDETERMINED": 127,
        "BLOCKED_NORMALIZATION": 21,
        "BLOCKED_DEPENDENCY_COMPILER": 27,
    }


def test_local_structure_ready_is_not_execution_unlock():
    local_ready = [
        item
        for item in build_career_response_decisions()
        if item.knowledge_readiness_class == "LOCAL_STRUCTURE_READY"
    ]

    assert len(local_ready) == 17
    assert all(
        item.adapter_status == "SEMANTIC_ONLY_PENDING_COMPILATION"
        for item in local_ready
    )
    assert all(item.condition_compiled is False for item in local_ready)
    assert all(item.knowledge_execution_unlocked is False for item in local_ready)
    assert all(item.runtime_effect_allowed is False for item in local_ready)


def test_real_career_adapter_authorizes_zero_runtime_effects():
    decisions = build_career_response_decisions()

    assert all(isinstance(item, CareerResponseDecision) for item in decisions)
    assert all(item.condition_compiled is False for item in decisions)
    assert all(item.knowledge_execution_unlocked is False for item in decisions)
    assert all(item.runtime_effect_allowed is False for item in decisions)

    validate_real_adapter_zero_unlock()


def test_antecedent_source_recheck_is_consumed_without_unresolved_refs():
    activation = load_activation_closure()
    decisions = build_career_response_decisions()

    assert activation["summary"]["unresolved_antecedent_reference_rows"] == 0
    assert activation["summary"]["explicit_antecedent_dependency_rows"] == 64
    assert sum(
        1 for item in decisions if item.antecedent_mode == "EXPLICIT_RULE_REFERENCE"
    ) == 64


def test_ca01_080_uses_corrected_base_antecedent():
    decision = _decision("CA01-080")

    assert decision.antecedent_mode == "EXPLICIT_RULE_REFERENCE"
    assert decision.antecedent_rule_ids == ("CA01-078",)
    assert decision.runtime_effect_allowed is False


def test_ca01_098_does_not_inherit_contradictory_antecedent():
    decision = _decision("CA01-098")

    assert decision.antecedent_mode == "NONE"
    assert decision.antecedent_rule_ids == ()
    assert decision.runtime_effect_allowed is False


def test_relation_binding_does_not_imply_member_realization_or_execution():
    decision = _decision("CA01-081")

    assert decision.relation_binding_dispositions == ("RB1_SINGLE_TARGET_BOUND",)
    assert "OPEN_WORLD" in decision.category_membership_statuses
    assert decision.runtime_effect_allowed is False
    assert decision.adapter_status != "SEMANTIC_ONLY_PENDING_COMPILATION"


def test_closed_world_absence_requires_explicit_evidence_token():
    decision = _decision("CA01-057")
    assert "CLOSED_WORLD_ABSENCE_EVIDENCE" in decision.blockers

    assert absence_evidence_ready(
        decision,
        closed_world_evidence_ref=None,
    ) is False
    assert absence_evidence_ready(
        decision,
        closed_world_evidence_ref="EVIDENCE:CLOSED_WORLD:EXPLICIT",
    ) is True

    # Evidence-readiness does not itself unlock Product execution.
    assert decision.runtime_effect_allowed is False


def test_open_category_review_remains_non_executable():
    decision = _decision("CA01-081")

    assert "OPEN_WORLD" in decision.category_membership_statuses
    assert decision.runtime_effect_allowed is False


def test_career_ordinal_registry_is_semantic_only_and_non_numeric():
    constraints = load_career_ordinal_constraints()

    assert len(constraints) == 130
    assert all(item["product_execution_unlocked"] is False for item in constraints)
    assert all(item["transitive_closure_allowed"] is False for item in constraints)

    for item in constraints:
        for key in ("numeric_gain", "numeric_value", "probability", "numeric_threshold"):
            if key in item:
                assert item[key] is None


def test_ordinal_relation_types_are_preserved_without_numeric_gain():
    payload = _load(CAREER_ORDINAL_CONSTRAINTS_PATH)
    constraints = load_career_ordinal_constraints()

    assert Counter(item["relation_type"] for item in constraints) == Counter(
        payload["relation_type_counts"]
    )
    assert any(
        item["relation_type"] == "MORE_IMPORTANT_THAN"
        for item in constraints
    )
    assert any(
        item["relation_type"] == "SOURCE_LOCAL_EMPHASIS"
        for item in constraints
    )


def test_readiness_audit_matches_versioned_artifact():
    generated = audit_response_semantics_adapter_readiness()
    stored = _load(READINESS)

    assert generated == stored


def test_readiness_summary_records_zero_unauthorized_unlocks():
    payload = audit_response_semantics_adapter_readiness()

    assert payload["response_pilot"]["total"] == 8
    assert payload["response_pilot"]["runtime_effects_authorized"] == 0

    ordinal = payload["career_ordinal_registry"]
    assert ordinal["total_constraints"] == 130
    assert ordinal["runtime_effects_authorized"] == 0
    assert ordinal["numericized_constraints"] == 0
    assert ordinal["transitive_closure_authorized"] == 0

    career = payload["career"]
    assert career["total_rows"] == 251
    assert career["response_gain_total"] == 89
    assert career["semantic_only_pending_compilation"] == 17
    assert career["runtime_effects_authorized"] == 0
    assert career["condition_compiled_count"] == 0
    assert career["knowledge_execution_unlocked_count"] == 0
    assert career["unresolved_antecedent_reference_rows"] == 0
    assert career["explicit_antecedent_dependency_rows"] == 64
    assert career["closed_world_evidence_gated_rows"] == 23
    assert career["rows_with_source_underdetermination"] == 184
    assert career["relation_bound_rows"] == 132
    assert career["category_reviewed_rows"] == 59
    assert career["unauthorized_unlock_count"] == 0


def test_adapter_output_contains_no_probability_or_numeric_gain_fields():
    payload = audit_response_semantics_adapter_readiness()
    synthetic = _load(SYNTHETIC)

    def walk(value):
        if isinstance(value, dict):
            for key, child in value.items():
                assert key not in {
                    "probability",
                    "posterior",
                    "learned_weight",
                    "numeric_gain",
                    "effect_weight",
                    "confidence_score",
                    "reward",
                }
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(payload)
    walk(synthetic)


def test_source_knowledge_files_are_read_only_inputs():
    # Product tests assert the adapter points to Knowledge assets, while the
    # repository lane validator enforces that this Product PR does not edit them.
    assert RESPONSE_PILOT_PATH.exists()
    assert ACTIVATION_CLOSURE_PATH.exists()
    assert CATEGORY_REVIEW_PATH.exists()
    assert CAREER_ORDINAL_CONSTRAINTS_PATH.exists()

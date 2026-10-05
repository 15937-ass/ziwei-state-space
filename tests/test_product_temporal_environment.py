from dataclasses import replace

import pytest

from src.product.natal_prior import NatalStateProfile
from src.product.temporal_environment import (
    EventRelativeContextEvidence,
    TemporalFact,
    TemporalReactionEvidence,
    build_temporal_environment_profile,
)


def _natal():
    return NatalStateProfile(
        schema_version="0.1",
        profile_id="NATAL-TEST",
        engine_version="engine:test",
        knowledge_version="KB-TEST",
        canonical_facts=(),
        named_structure_facts=(),
        baiguan_profiles=(),
        pattern_assessments=(),
        contextual_valences=(),
        domains=(),
    )


def _facts():
    return (
        TemporalFact(
            layer="YEAR",
            fact="yearly:life_palace:P03",
            provenance="P1-temporal-fixture",
        ),
        TemporalFact(
            layer="DECADE",
            fact="decade:active_range:33-42",
            provenance="P1-temporal-fixture",
        ),
    )


def _reaction():
    return TemporalReactionEvidence(
        reaction_id="TR-001",
        rule_id="RULE-T-001",
        layer="YEAR",
        domain="career",
        target="career_change_activation",
        effect="ACTIVATE",
        source_id="SRC-ZZ-003",
        source_location="事业宫",
        review_status="SOURCE_SPAN_VERIFIED",
    )


def test_temporal_profile_is_environment_only_and_deterministic():
    first = build_temporal_environment_profile(
        _natal(),
        target_label="2030",
        temporal_facts=_facts(),
        reactions=(_reaction(),),
    )
    second = build_temporal_environment_profile(
        _natal(),
        target_label="2030",
        temporal_facts=tuple(reversed(_facts())),
        reactions=(_reaction(),),
    )

    assert first.profile_id == second.profile_id
    assert first.active_layers == ("DECADE", "YEAR")
    assert not first.feedback_used
    assert not first.acquired_state_used
    assert not first.outcome_used
    assert not first.empirical_calibration_used


def test_temporal_knowledge_version_must_match_natal_profile():
    with pytest.raises(ValueError, match="must match"):
        build_temporal_environment_profile(
            _natal(),
            target_label="2030",
            temporal_facts=_facts(),
            knowledge_version="KB-OTHER",
        )


def test_temporal_reaction_has_no_numeric_magnitude():
    reaction = _reaction()
    assert reaction.magnitude_status == "UNIDENTIFIED"
    with pytest.raises(ValueError, match="magnitude_status"):
        replace(reaction, magnitude_status="0.8")


def test_event_relative_context_is_preserved_not_generalized():
    context = EventRelativeContextEvidence(
        context_id="MIGRATION_FIRST_THREE_YEARS",
        status="ACTIVE",
        source_id="SRC-ZZ-003",
        source_location="迁移宫 printed p109",
        review_status="HUMAN_VERIFIED",
    )
    profile = build_temporal_environment_profile(
        _natal(),
        target_label="2030",
        temporal_facts=_facts(),
        event_relative_context=(context,),
    )
    assert profile.event_relative_context[0].context_id == "MIGRATION_FIRST_THREE_YEARS"
    assert profile.event_relative_context[0].status == "ACTIVE"


def test_unsupported_temporal_layer_fails_closed():
    with pytest.raises(ValueError, match="unsupported temporal layer"):
        TemporalFact(
            layer="LIFETIME",
            fact="unsupported",
            provenance="test",
        )

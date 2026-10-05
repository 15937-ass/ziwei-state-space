import json
from pathlib import Path

import pytest

from src.product.acquired_state import compile_acquired_state
from src.product.manifestation_context import build_manifestation_routing_context
from src.product.natal_prior import NatalStateProfile
from src.product.state_quality import (
    audit_acquired_state_quality,
    compile_state_requirements,
)
from src.product.temporal_environment import (
    TemporalEnvironmentProfile,
    TemporalReactionEvidence,
)

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "product/PL3S_ACQUIRED_STATE_FIXTURE_v0.1.json"
REQ = ROOT / "product/PL3S_STATE_QUALITY_REQUIREMENTS_FIXTURE_v0.1.json"


def _natal():
    return NatalStateProfile(
        schema_version="0.1",
        profile_id="NATAL-CONTEXT-FX",
        engine_version="test",
        knowledge_version="KB-CONTEXT-FX",
        canonical_facts=(),
        named_structure_facts=(),
        baiguan_profiles=(),
        pattern_assessments=(),
        contextual_valences=(),
        domains=(),
    )


def _temporal():
    return TemporalEnvironmentProfile(
        schema_version="0.1",
        profile_id="TEMP-CONTEXT-FX",
        natal_profile_id="NATAL-CONTEXT-FX",
        knowledge_version="KB-CONTEXT-FX",
        target_label="2030",
        active_layers=("YEAR",),
        temporal_facts=(),
        reactions=(
            TemporalReactionEvidence(
                reaction_id="TR-CONTEXT-FX",
                rule_id="RULE-TEMP-FX",
                layer="YEAR",
                domain="test",
                target="test_target",
                effect="ACTIVATE",
                source_id="TEST",
                source_location="fixture",
                review_status="SOURCE_SPAN_VERIFIED",
            ),
        ),
        conflicts=(),
        event_relative_context=(),
    )


def _state():
    return compile_acquired_state(
        json.loads(STATE.read_text(encoding="utf-8"))
    )


def _quality(state):
    requirements = compile_state_requirements(
        json.loads(REQ.read_text(encoding="utf-8"))
    )
    return audit_acquired_state_quality(state, requirements)


def test_blind_context_rejects_personal_state_and_contains_only_n_e():
    context = build_manifestation_routing_context(
        _natal(), _temporal(), mode="BLIND"
    )
    assert context.mode == "BLIND"
    assert context.personalization_readiness == "NOT_REQUESTED"
    assert context.acquired_state_id is None
    assert context.actions == ()
    assert context.external_factors == ()
    assert context.active_temporal_rule_ids == ("RULE-TEMP-FX",)

    with pytest.raises(ValueError, match="BLIND mode must not receive"):
        build_manifestation_routing_context(
            _natal(),
            _temporal(),
            mode="BLIND",
            acquired_state=_state(),
        )


def test_personalized_context_keeps_s_a_c_separate():
    state = _state()
    context = build_manifestation_routing_context(
        _natal(),
        _temporal(),
        mode="PERSONALIZED",
        acquired_state=state,
        state_quality=_quality(state),
    )
    assert context.person_key == state.person_key
    assert context.state_assertions
    assert context.actions
    assert context.exposures
    assert context.counterparty_factors
    assert not context.empirical_probability_used


def test_partial_missing_state_marks_personalized_abstention():
    state = _state()
    quality = _quality(state)
    assert quality.readiness == "PARTIAL_MISSING"
    context = build_manifestation_routing_context(
        _natal(),
        _temporal(),
        mode="PERSONALIZED",
        acquired_state=state,
        state_quality=quality,
    )
    assert context.personalization_readiness == "ABSTAIN_MISSING"
    assert context.abstention_reasons


def test_missing_quality_report_does_not_pretend_personalization_ready():
    context = build_manifestation_routing_context(
        _natal(),
        _temporal(),
        mode="PERSONALIZED",
        acquired_state=_state(),
    )
    assert context.personalization_readiness == "QUALITY_NOT_PROVIDED"


def test_state_quality_must_match_acquired_state():
    state = _state()
    quality = _quality(state)
    from dataclasses import replace
    bad = replace(quality, state_id="ASTATE-OTHER")
    with pytest.raises(ValueError, match="does not belong"):
        build_manifestation_routing_context(
            _natal(),
            _temporal(),
            mode="PERSONALIZED",
            acquired_state=state,
            state_quality=bad,
        )


def test_natal_temporal_version_mismatch_fails_closed():
    from dataclasses import replace
    with pytest.raises(ValueError, match="knowledge_version mismatch"):
        build_manifestation_routing_context(
            _natal(),
            replace(_temporal(), knowledge_version="KB-OTHER"),
            mode="BLIND",
        )


def test_same_inputs_produce_same_context_id():
    first = build_manifestation_routing_context(
        _natal(), _temporal(), mode="BLIND"
    )
    second = build_manifestation_routing_context(
        _natal(), _temporal(), mode="BLIND"
    )
    assert first.context_id == second.context_id

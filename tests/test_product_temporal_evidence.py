from dataclasses import replace

import pytest

from src.product.evidence_package import (
    ConfidenceBand,
    EvidenceItem,
    EvidencePackage,
    TemporalEvidenceNamespace,
)
from src.product.natal_prior import NatalStateProfile
from src.product.temporal_environment import (
    EventRelativeContextEvidence,
    TemporalFact,
    TemporalReactionEvidence,
    build_temporal_environment_profile,
)
from src.product.temporal_evidence import (
    attach_temporal_profile_to_evidence_package,
    temporal_profile_to_evidence_namespace,
)


def _natal():
    return NatalStateProfile(
        schema_version="0.1",
        profile_id="NATAL-TEMP-EVIDENCE",
        engine_version="test",
        knowledge_version="KB-TEST",
        canonical_facts=(),
        named_structure_facts=(),
        baiguan_profiles=(),
        pattern_assessments=(),
        contextual_valences=(),
        domains=(),
    )


def _profile(active_event=True):
    context = ()
    if active_event:
        context = (
            EventRelativeContextEvidence(
                context_id="MIGRATION_FIRST_THREE_YEARS",
                status="ACTIVE",
                source_id="SRC-ZZ-003",
                source_location="迁移宫 printed p109",
                review_status="HUMAN_VERIFIED",
                trigger_provenance="OBS-RELOCATION-001",
                routing_facts=(
                    "gate:migration_first_three_years:active",
                    "projection_priority:migration_palace:primary",
                    "rotation:annual_life_palace:preserved",
                ),
            ),
        )

    return build_temporal_environment_profile(
        _natal(),
        target_label="T-DEMO",
        temporal_facts=(
            TemporalFact(
                layer="YEAR",
                fact='scope.branch="辰"',
                provenance="PL1:test",
            ),
            TemporalFact(
                layer="DECADE",
                fact='scope.branch="寅"',
                provenance="PL1:test",
            ),
        ),
        reactions=(
            TemporalReactionEvidence(
                reaction_id="TR-001",
                rule_id="TR-RULE-001",
                layer="YEAR",
                domain="career",
                target="career_mobility_activation",
                effect="ACTIVATE",
                source_id="SRC-ZZ-003",
                source_location="事业宫 test",
                review_status="SOURCE_SPAN_VERIFIED",
                matched_natal_facts=("PALACE_HAS_STAR|palace=P09|star=紫微",),
                matched_temporal_facts=("STAR_PRESENT|layer=YEAR|star=天马",),
            ),
        ),
        conflicts=("conflict:test",),
        event_relative_context=context,
    )


def _package():
    return EvidencePackage(
        question="test temporal evidence",
        chart_facts={"time_layer": "NATAL"},
        active_rules=[
            EvidenceItem(
                rule_id="W01-001",
                claim="canonical claim",
                source_id="SRC-ZZ-003",
                source_location="财帛宫",
                epistemic="SOURCE",
                review_status="SOURCE_SPAN_VERIFIED",
            )
        ],
        projections=[{"rule_id": "W01-001", "projection_target": "wealth_state"}],
        confidence_band=ConfidenceBand.MEDIUM_CONFIDENCE,
        confidence_rationale="test",
        knowledge_version="KB-TEST",
    )


def test_temporal_profile_maps_to_separate_namespace_with_source_trace():
    namespace = temporal_profile_to_evidence_namespace(_profile())
    assert namespace.profile_id.startswith("TEMP-")
    assert namespace.active_layers == ("DECADE", "YEAR")
    assert namespace.temporal_reactions[0]["rule_id"] == "TR-RULE-001"
    assert namespace.temporal_reactions[0]["source_id"] == "SRC-ZZ-003"
    assert namespace.event_relative_context[0]["context_id"] == (
        "MIGRATION_FIRST_THREE_YEARS"
    )
    assert namespace.external_event_trigger_used is True
    assert "layer:YEAR:active" in namespace.environment_states
    assert (
        "event_relative:MIGRATION_FIRST_THREE_YEARS:ACTIVE"
        in namespace.environment_states
    )


def test_attach_temporal_namespace_preserves_canonical_payload():
    original = _package()
    updated = attach_temporal_profile_to_evidence_package(original, _profile())

    assert original.temporal is None
    assert updated.temporal is not None
    assert updated.active_rules == original.active_rules
    assert updated.projections == original.projections
    assert updated.chart_facts == original.chart_facts
    assert updated.temporal.profile_id == _profile().profile_id


def test_temporal_namespace_serializes_under_temporal_key():
    payload = attach_temporal_profile_to_evidence_package(
        _package(), _profile()
    ).to_dict()
    assert "temporal" in payload
    assert payload["temporal"]["target_label"] == "T-DEMO"
    assert payload["temporal"]["external_event_trigger_used"] is True
    assert payload["confidence_band"] == "MEDIUM_CONFIDENCE"


def test_knowledge_version_mismatch_fails_closed():
    package = replace(_package(), knowledge_version="KB-OTHER")
    with pytest.raises(ValueError, match="knowledge_version"):
        attach_temporal_profile_to_evidence_package(package, _profile())


def test_empty_package_knowledge_version_inherits_temporal_version():
    package = replace(_package(), knowledge_version="")
    updated = attach_temporal_profile_to_evidence_package(package, _profile())
    assert updated.knowledge_version == "KB-TEST"


@pytest.mark.parametrize(
    "forbidden_key",
    [
        "probability",
        "posterior",
        "outcome",
        "acquired_state",
        "empirical_calibration",
    ],
)
def test_temporal_namespace_rejects_personal_empirical_or_outcome_payload(forbidden_key):
    namespace = TemporalEvidenceNamespace(
        profile_id="TEMP-X",
        natal_profile_id="NATAL-X",
        target_label="T-X",
        temporal_facts=({forbidden_key: "should-not-be-here"},),
    )
    with pytest.raises(ValueError, match="TEMPORAL namespace"):
        namespace.validate()


def test_inactive_event_context_does_not_mark_external_trigger_used():
    namespace = temporal_profile_to_evidence_namespace(_profile(active_event=False))
    assert namespace.external_event_trigger_used is False
    assert not any(
        item.startswith("event_relative:") for item in namespace.environment_states
    )

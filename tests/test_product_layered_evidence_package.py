import pytest

from src.product.layered_evidence_package import (
    LayeredEvidencePackage,
    StructuredInferenceConclusion,
    build_layered_evidence_package,
)
from src.product.natal_prior import NatalStateProfile
from src.product.temporal_environment import (
    EventRelativeContextEvidence,
    TemporalFact,
    build_temporal_environment_profile,
)


def _natal():
    return NatalStateProfile(
        schema_version="0.1",
        profile_id="NATAL-LAYERED-TEST",
        engine_version="test",
        knowledge_version="KB-TEST",
        canonical_facts=("natal:fact:1",),
        named_structure_facts=("structure:test",),
        baiguan_profiles=(),
        pattern_assessments=(),
        contextual_valences=(),
        domains=(),
    )


def _temporal(natal=None):
    natal = natal or _natal()
    return build_temporal_environment_profile(
        natal,
        target_label="2030",
        temporal_facts=(
            TemporalFact(
                layer="YEAR",
                fact='scope.branch="辰"',
                provenance="fixture",
            ),
        ),
        event_relative_context=(
            EventRelativeContextEvidence(
                context_id="MIGRATION_FIRST_THREE_YEARS",
                status="ACTIVE",
                source_id="SRC-ZZ-003",
                source_location="迁移宫 printed p109",
                review_status="HUMAN_VERIFIED",
                trigger_provenance="OBS-1",
                routing_facts=("projection_priority:migration_palace:primary",),
            ),
        ),
    )


def test_layered_package_separates_four_namespaces():
    natal = _natal()
    package = build_layered_evidence_package(
        question="2030年的迁移环境",
        natal_profile=natal,
        temporal_profile=_temporal(natal),
    )
    payload = package.to_dict()

    assert payload["canonical"]["natal_profile_id"] == natal.profile_id
    assert payload["temporal"]["target_label"] == "2030"
    assert payload["personal"] == {}
    assert payload["empirical"] == {}
    assert payload["temporal"]["external_event_trigger_used"] is True


def test_temporal_package_rejects_wrong_natal_profile():
    natal = _natal()
    other = NatalStateProfile(
        schema_version="0.1",
        profile_id="NATAL-OTHER",
        engine_version="test",
        knowledge_version="KB-TEST",
        canonical_facts=(),
        named_structure_facts=(),
        baiguan_profiles=(),
        pattern_assessments=(),
        contextual_valences=(),
        domains=(),
    )
    with pytest.raises(ValueError, match="does not belong"):
        build_layered_evidence_package(
            question="test",
            natal_profile=other,
            temporal_profile=_temporal(natal),
        )


def test_pl3t_layered_package_forbids_personal_namespace():
    natal = _natal()
    base = build_layered_evidence_package(
        question="test",
        natal_profile=natal,
        temporal_profile=_temporal(natal),
    )
    with pytest.raises(ValueError, match="PERSONAL"):
        LayeredEvidencePackage(
            schema_version="0.1",
            question="test",
            canonical=base.canonical,
            temporal=base.temporal,
            personal={"relationship_status": "single"},
        )


def test_pl3t_layered_package_forbids_empirical_namespace():
    natal = _natal()
    base = build_layered_evidence_package(
        question="test",
        natal_profile=natal,
        temporal_profile=_temporal(natal),
    )
    with pytest.raises(ValueError, match="EMPIRICAL"):
        LayeredEvidencePackage(
            schema_version="0.1",
            question="test",
            canonical=base.canonical,
            temporal=base.temporal,
            empirical={"probability": 0.8},
        )


def test_structured_conclusion_round_trips_inside_evidence_package():
    natal = _natal()
    conclusion = StructuredInferenceConclusion(
        schema_version="0.1",
        status="PARTIAL",
        question="2030年的迁移环境",
        target_id="T-2030",
        selected_domains=("wealth",),
        canonical_rule_ids=(),
        temporal_reaction_rule_ids=(),
        evidence_refs=(),
        conflicts=("SOURCE_CONFLICT",),
        unknowns=("PRODUCTION_TEMPORAL_REACTION_REGISTRY_EMPTY",),
        limitations=("NO_REAL_WORLD_EVENT_CLAIM",),
    )
    package = build_layered_evidence_package(
        question="2030年的迁移环境",
        natal_profile=natal,
        temporal_profile=_temporal(natal),
        conclusion=conclusion,
    )

    payload = package.to_dict()
    assert payload["conclusion"]["status"] == "PARTIAL"
    assert payload["conclusion"]["target_id"] == "T-2030"
    assert payload["conclusion"]["unknowns"] == [
        "PRODUCTION_TEMPORAL_REACTION_REGISTRY_EMPTY"
    ]
    assert payload["conclusion"]["conflicts"] == ["SOURCE_CONFLICT"]


def test_structured_conclusion_question_must_match_package_question():
    natal = _natal()
    conclusion = StructuredInferenceConclusion(
        schema_version="0.1",
        status="PARTIAL",
        question="different question",
        target_id="T-2030",
        selected_domains=("wealth",),
        canonical_rule_ids=(),
        temporal_reaction_rule_ids=(),
        evidence_refs=(),
        conflicts=(),
        unknowns=("UNKNOWN",),
        limitations=("NO_REAL_WORLD_EVENT_CLAIM",),
    )
    with pytest.raises(ValueError, match="question must match"):
        build_layered_evidence_package(
            question="2030年的迁移环境",
            natal_profile=natal,
            temporal_profile=_temporal(natal),
            conclusion=conclusion,
        )

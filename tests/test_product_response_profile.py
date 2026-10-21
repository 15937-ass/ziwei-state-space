from dataclasses import replace

import pytest

from src.product.natal_prior import NatalStateProfile
from src.product.response_profile import (
    RESPONSE_COMPILER_VERSION,
    build_career_response_profile,
)
from src.product.temporal_environment import (
    TemporalFact,
    TemporalReactionEvidence,
    build_temporal_environment_profile,
)


RULE_IDS = (
    "CA02-181",
    "CA03-228",
    "CA05-411",
    "CA05-417",
    "CA05-419",
    "CA05-420",
    "CA05-433",
    "CA07-638",
    "CA07-639",
    "CA07-681",
    "CA07-682",
    "CA09-820",
)


def _natal(profile_id="NATAL-RESPONSE-TEST", knowledge_version="KB-TEST"):
    return NatalStateProfile(
        schema_version="0.1",
        profile_id=profile_id,
        engine_version="engine:test",
        knowledge_version=knowledge_version,
        canonical_facts=(),
        named_structure_facts=(),
        baiguan_profiles=(),
        pattern_assessments=(),
        contextual_valences=(),
        domains=(),
    )


def _binding(rule_id):
    return {
        "source_rule_id": rule_id,
        "condition_id": f"PRODUCT_CONDITION:{rule_id}",
        "time_layer": "NATAL",
        "projection_domain": "CAREER",
        "projection_target": f"projection:{rule_id}",
        "source_location": "SRC-ZZ-003 事业宫 test span",
        "source_span_ids": [f"SPAN:{rule_id}"],
        "compatibility_band": "LOCAL_STRUCTURE_READY",
        "effect_kind": "SOURCE_PROJECTION_DESCRIPTOR",
        "binding_status": "BOUND_SOURCE_PROJECTION_SEMANTIC_ONLY",
        "runtime_effect_allowed": False,
    }


def _evaluation_report(matched=("CA02-181", "CA03-228")):
    matched = set(matched)
    rows = []
    for rule_id in RULE_IDS:
        is_match = rule_id in matched
        rows.append(
            {
                "source_rule_id": rule_id,
                "condition_id": f"PRODUCT_CONDITION:{rule_id}",
                "compiler_status": "COMPILED_DIRECT_SEMANTIC_ONLY",
                "matched": is_match,
                "matched_evidence": [f"P09:TEST:{rule_id}"] if is_match else [],
                "effect_binding": _binding(rule_id) if is_match else None,
                "product_condition_compiled": True,
                "condition_evaluated": True,
                "response_effect_bound": is_match,
                "runtime_effect_allowed": False,
            }
        )
    return {
        "schema_version": "0.1",
        "scope": {
            "domain": "career",
            "palace_id": "P09",
            "time_layer": "NATAL",
            "temporal_environment_consumed": False,
        },
        "summary": {
            "conditions_compiled": 12,
            "conditions_evaluated": 12,
            "conditions_matched": len(matched),
            "semantic_effects_bound": len(matched),
            "runtime_effects_authorized": 0,
            "response_profile_tau_generated": 0,
        },
        "evaluations": rows,
    }


def _facts():
    return (
        TemporalFact(
            layer="DECADE",
            fact='scope.branch="寅"',
            provenance="PL1:test:decade",
        ),
        TemporalFact(
            layer="YEAR",
            fact='scope.branch="午"',
            provenance="PL1:test:year",
        ),
    )


def _reaction(reaction_id, *, effect, layer="YEAR", linked=("CA02-181",), magnitude="UNIDENTIFIED"):
    return TemporalReactionEvidence(
        reaction_id=reaction_id,
        rule_id=f"TEMP-{reaction_id}",
        layer=layer,
        domain="career",
        target=f"career_target:{reaction_id}",
        effect=effect,
        source_id="SRC-ZZ-003",
        source_location=f"事业宫 temporal test {reaction_id}",
        review_status="SOURCE_SPAN_VERIFIED",
        magnitude_status=magnitude,
        matched_natal_facts=(f"NATAL:{reaction_id}",),
        matched_temporal_facts=(f"TEMPORAL:{reaction_id}",),
        matched_natal_rule_ids=tuple(linked),
    )


def _temporal(natal, reactions=()):
    return build_temporal_environment_profile(
        natal,
        target_label="2030",
        temporal_facts=_facts(),
        reactions=reactions,
    )


def test_compiler_produces_sparse_source_backed_symbolic_response():
    natal = _natal()
    reactions = (
        _reaction("R-ACT", effect="ACTIVATE", layer="DECADE"),
        _reaction("R-STR", effect="STRENGTHEN"),
        _reaction("R-WEAK", effect="WEAKEN"),
        _reaction("R-XFORM", effect="TRANSFORM", magnitude="SOURCE_ORDINAL_ONLY"),
    )
    profile = build_career_response_profile(
        natal,
        _evaluation_report(),
        _temporal(natal, reactions),
    )

    assert profile.compiler_version == RESPONSE_COMPILER_VERSION
    assert profile.status == "SOURCE_BACKED_SYMBOLIC_RESPONSE"
    assert len(profile.entries) == 4
    assert {item.effect for item in profile.entries} == {
        "ACTIVATE",
        "STRENGTHEN",
        "WEAKEN",
        "TRANSFORM",
    }
    assert {item.layer for item in profile.entries} == {"DECADE", "YEAR"}
    assert all(item.natal_rule_id == "CA02-181" for item in profile.entries)
    assert all(item.runtime_effect_allowed is False for item in profile.entries)
    assert any(
        item.magnitude_status == "SOURCE_ORDINAL_ONLY"
        for item in profile.entries
    )
    assert profile.runtime_effect_allowed is False
    assert profile.probability_used is False
    assert profile.empirical_calibration_used is False


def test_profile_id_is_deterministic_under_reaction_order():
    natal = _natal()
    reactions = (
        _reaction("R1", effect="ACTIVATE", layer="DECADE"),
        _reaction("R2", effect="PRESERVE", layer="YEAR"),
    )
    first = build_career_response_profile(
        natal,
        _evaluation_report(),
        _temporal(natal, reactions),
    )
    second = build_career_response_profile(
        natal,
        _evaluation_report(),
        _temporal(natal, tuple(reversed(reactions))),
    )
    assert first.profile_id == second.profile_id
    assert first.to_dict() == second.to_dict()


def test_only_matched_natal_condition_can_seed_response_entry():
    natal = _natal()
    reaction = _reaction(
        "R-UNMATCHED",
        effect="ACTIVATE",
        linked=("CA05-411",),
    )
    profile = build_career_response_profile(
        natal,
        _evaluation_report(matched=("CA02-181",)),
        _temporal(natal, (reaction,)),
    )
    assert profile.entries == ()
    assert (
        "REACTION_NATAL_CONDITION_NOT_MATCHED:R-UNMATCHED:CA05-411"
        in profile.unknowns
    )
    assert "NO_SOURCE_BACKED_DECADE_YEAR_RESPONSE" in profile.unknowns


def test_explicit_natal_link_is_required_and_not_inferred_from_domain_or_target():
    natal = _natal()
    reaction = _reaction(
        "R-NOLINK",
        effect="ACTIVATE",
        linked=(),
    )
    profile = build_career_response_profile(
        natal,
        _evaluation_report(),
        _temporal(natal, (reaction,)),
    )
    assert profile.entries == ()
    assert "REACTION_WITHOUT_EXPLICIT_NATAL_LINK:R-NOLINK" in profile.unknowns


def test_month_reaction_is_preserved_as_out_of_scope_unknown():
    natal = _natal()
    reaction = _reaction(
        "R-MONTH",
        effect="ACTIVATE",
        layer="MONTH",
    )
    temporal = build_temporal_environment_profile(
        natal,
        target_label="2030-05",
        temporal_facts=_facts()
        + (
            TemporalFact(
                layer="MONTH",
                fact='scope.branch="辰"',
                provenance="PL1:test:month",
            ),
        ),
        reactions=(reaction,),
    )
    profile = build_career_response_profile(
        natal,
        _evaluation_report(),
        temporal,
    )
    assert profile.entries == ()
    assert "REACTION_LAYER_OUT_OF_SCOPE:R-MONTH" in profile.unknowns


def test_empty_production_reaction_path_is_partial_unknown_not_negative_evidence():
    natal = _natal()
    profile = build_career_response_profile(
        natal,
        _evaluation_report(),
        _temporal(natal, ()),
    )
    assert profile.status == "PARTIAL_UNKNOWN"
    assert profile.entries == ()
    assert "PRODUCTION_TEMPORAL_RESPONSE_NOT_AVAILABLE" in profile.unknowns
    assert "NO_SOURCE_BACKED_DECADE_YEAR_RESPONSE" in profile.unknowns


def test_temporal_natal_lineage_mismatch_fails_closed():
    natal = _natal(profile_id="NATAL-A")
    other = _natal(profile_id="NATAL-B")
    temporal = _temporal(other)
    with pytest.raises(ValueError, match="lineage mismatch"):
        build_career_response_profile(
            natal,
            _evaluation_report(),
            temporal,
        )


def test_temporal_natal_knowledge_version_mismatch_fails_closed():
    natal = _natal(knowledge_version="KB-A")
    other = _natal(knowledge_version="KB-B")
    temporal = _temporal(other)
    mismatched_lineage = replace(temporal, natal_profile_id=natal.profile_id)
    with pytest.raises(ValueError, match="knowledge_version mismatch"):
        build_career_response_profile(
            natal,
            _evaluation_report(),
            mismatched_lineage,
        )

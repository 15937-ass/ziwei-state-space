import json
from pathlib import Path

import pytest

from src.product.natal_prior import NatalStateProfile
from src.product.response_profile import (
    RESPONSE_COMPILER_VERSION,
    UNKNOWN_NO_CANONICAL_TEMPORAL_RESPONSE_RULE,
    compile_decade_year_response_profile,
    load_active_temporal_kr_gate,
)
from src.product.temporal_environment import (
    TemporalFact,
    TemporalReactionEvidence,
    build_temporal_environment_profile,
)


ROOT = Path(__file__).resolve().parents[1]


def _natal(profile_id: str = "NATAL-TAU-A") -> NatalStateProfile:
    return NatalStateProfile(
        schema_version="0.1",
        profile_id=profile_id,
        engine_version="test:tau",
        knowledge_version="KB-TAU-TEST",
        canonical_facts=(),
        named_structure_facts=(),
        baiguan_profiles=(),
        pattern_assessments=(),
        contextual_valences=(),
        domains=(),
    )


def _temporal(
    natal: NatalStateProfile,
    *,
    year_fact: str = "scope.branch=\"子\"",
    include_month: bool = False,
    reactions=(),
):
    facts = [
        TemporalFact(
            layer="DECADE",
            fact="scope.name=\"33-42\"",
            provenance="PL1:fixture:decade",
        ),
        TemporalFact(
            layer="YEAR",
            fact=year_fact,
            provenance="PL1:fixture:year",
        ),
    ]
    if include_month:
        facts.append(
            TemporalFact(
                layer="MONTH",
                fact="scope.branch=\"寅\"",
                provenance="PL1:fixture:month",
            )
        )
    return build_temporal_environment_profile(
        natal,
        target_label="TAU-TARGET-2030",
        temporal_facts=tuple(facts),
        reactions=tuple(reactions),
        conflicts=("SOURCE_SCOPE_CONFLICT",),
    )


def _governed_rows():
    condition_registry = json.loads(
        (ROOT / "product/CAREER_CONDITION_COMPILER_PILOT_v0.1.json").read_text(
            encoding="utf-8"
        )
    )
    binding_registry = json.loads(
        (ROOT / "product/CAREER_CONDITION_EFFECT_BINDING_PILOT_v0.1.json").read_text(
            encoding="utf-8"
        )
    )
    bindings = {
        row["source_rule_id"]: row for row in binding_registry["bindings"]
    }
    return condition_registry["compiled_conditions"], bindings


def _evaluation(*, matched_rule_ids=()):
    plans, bindings = _governed_rows()
    selected = set(matched_rule_ids)
    rows = []
    for plan in plans:
        rule_id = plan["source_rule_id"]
        matched = rule_id in selected
        rows.append(
            {
                "source_rule_id": rule_id,
                "condition_id": plan["condition_id"],
                "compiler_status": plan["compiler_status"],
                "matched": matched,
                "matched_evidence": (
                    [f"P09:FIXTURE:{rule_id}"] if matched else []
                ),
                "effect_binding": bindings[rule_id] if matched else None,
                "product_condition_compiled": True,
                "condition_evaluated": True,
                "response_effect_bound": matched,
                "runtime_effect_allowed": False,
            }
        )
    return {
        "schema_version": "0.1",
        "evaluator_version": "PL3R_CAREER_CONDITION_EVALUATOR_V0_1",
        "scope": {
            "domain": "career",
            "palace_id": "P09",
            "time_layer": "NATAL",
            "temporal_environment_consumed": False,
        },
        "summary": {
            "conditions_compiled": 12,
            "conditions_evaluated": 12,
            "conditions_matched": len(selected),
            "semantic_effects_bound": len(selected),
            "runtime_effects_authorized": 0,
            "response_profile_tau_generated": 0,
        },
        "evaluations": rows,
    }


def _first_rule_id() -> str:
    plans, _ = _governed_rows()
    return plans[0]["source_rule_id"]


def test_active_temporal_kr_gate_is_locked_zero_eligible_baseline():
    gate = load_active_temporal_kr_gate(ROOT)
    assert gate.eligible_rule_count == 0
    assert gate.executable_pilot_emitted is False
    assert gate.production_registry_should_remain_empty is True
    assert (
        gate.decision
        == "NO_ELIGIBLE_SOURCE_EXPLICIT_TEMPORAL_RULE_UNDER_CURRENT_CONTRACT"
    )


def test_tau_is_deterministic_and_explicitly_unknown_under_current_kr():
    natal = _natal()
    temporal = _temporal(natal)
    evaluation = _evaluation(matched_rule_ids=(_first_rule_id(),))

    first = compile_decade_year_response_profile(
        natal, evaluation, temporal, repository_root=ROOT
    )
    second = compile_decade_year_response_profile(
        natal, evaluation, temporal, repository_root=ROOT
    )

    assert first.profile_id == second.profile_id
    assert first.compiler_version == RESPONSE_COMPILER_VERSION
    assert first.consumed_layers == ("DECADE", "YEAR")
    assert first.dynamic_effects == ()
    assert first.runtime_effects_authorized == 0
    assert first.response_status == UNKNOWN_NO_CANONICAL_TEMPORAL_RESPONSE_RULE
    assert len(first.natal_semantic_evidence) == 1
    assert first.natal_semantic_evidence[0].semantic_status == (
        "SOURCE_PROJECTION_SEMANTIC_ONLY"
    )
    assert first.conflicts == ("SOURCE_SCOPE_CONFLICT",)


def test_same_n_changed_environment_changes_tau_identity_not_natal_identity():
    natal = _natal()
    evaluation = _evaluation()
    first = compile_decade_year_response_profile(
        natal,
        evaluation,
        _temporal(natal, year_fact="scope.branch=\"子\""),
        repository_root=ROOT,
    )
    second = compile_decade_year_response_profile(
        natal,
        evaluation,
        _temporal(natal, year_fact="scope.branch=\"午\""),
        repository_root=ROOT,
    )

    assert first.natal_profile_id == second.natal_profile_id == natal.profile_id
    assert first.profile_id != second.profile_id


def test_equivalent_environment_facts_with_different_n_preserve_n_specific_semantics():
    first_natal = _natal("NATAL-TAU-A")
    second_natal = _natal("NATAL-TAU-B")
    first = compile_decade_year_response_profile(
        first_natal,
        _evaluation(matched_rule_ids=(_first_rule_id(),)),
        _temporal(first_natal),
        repository_root=ROOT,
    )
    second = compile_decade_year_response_profile(
        second_natal,
        _evaluation(),
        _temporal(second_natal),
        repository_root=ROOT,
    )

    assert len(first.natal_semantic_evidence) == 1
    assert len(second.natal_semantic_evidence) == 0
    assert first.profile_id != second.profile_id


@pytest.mark.parametrize("missing_layer", ["DECADE", "YEAR"])
def test_missing_required_temporal_layer_fails_closed(missing_layer):
    natal = _natal()
    keep = "YEAR" if missing_layer == "DECADE" else "DECADE"
    temporal = build_temporal_environment_profile(
        natal,
        target_label="TAU-TARGET-2030",
        temporal_facts=(
            TemporalFact(
                layer=keep,
                fact="scope.name=\"fixture\"",
                provenance="PL1:fixture",
            ),
        ),
    )
    with pytest.raises(ValueError, match="requires temporal layer"):
        compile_decade_year_response_profile(
            natal, _evaluation(), temporal, repository_root=ROOT
        )


def test_unauthorized_temporal_reaction_fails_closed_on_zero_eligible_kr():
    natal = _natal()
    reaction = TemporalReactionEvidence(
        reaction_id="UNAUTHORIZED-TR-001",
        rule_id="UNAUTHORIZED-RULE",
        layer="YEAR",
        domain="career",
        target="career_change",
        effect="ACTIVATE",
        source_id="TEST",
        source_location="TEST",
        review_status="TEST_ONLY",
    )
    temporal = _temporal(natal, reactions=(reaction,))
    with pytest.raises(ValueError, match="authorizes zero Career reaction rules"):
        compile_decade_year_response_profile(
            natal, _evaluation(), temporal, repository_root=ROOT
        )


def test_month_is_preserved_as_environment_but_not_promoted_into_v01_tau():
    natal = _natal()
    profile = compile_decade_year_response_profile(
        natal,
        _evaluation(),
        _temporal(natal, include_month=True),
        repository_root=ROOT,
    )

    assert profile.consumed_layers == ("DECADE", "YEAR")
    assert profile.ignored_environment_layers == ("MONTH",)
    assert all(
        item.layer in {"DECADE", "YEAR"}
        for item in profile.temporal_environment_evidence
    )


def test_natal_temporal_lineage_mismatch_fails_closed():
    natal = _natal("NATAL-TAU-A")
    other = _natal("NATAL-TAU-B")
    with pytest.raises(ValueError, match="does not belong"):
        compile_decade_year_response_profile(
            natal,
            _evaluation(),
            _temporal(other),
            repository_root=ROOT,
        )


def test_forged_natal_effect_binding_is_rejected():
    natal = _natal()
    evaluation = _evaluation(matched_rule_ids=(_first_rule_id(),))
    evaluation["evaluations"][0]["effect_binding"] = dict(
        evaluation["evaluations"][0]["effect_binding"]
    )
    evaluation["evaluations"][0]["effect_binding"]["projection_target"] = "invented"
    with pytest.raises(ValueError, match="differs from governed registry"):
        compile_decade_year_response_profile(
            natal, evaluation, _temporal(natal), repository_root=ROOT
        )


def test_tau_contract_contains_no_probability_weight_or_posterior_output():
    natal = _natal()
    profile = compile_decade_year_response_profile(
        natal, _evaluation(), _temporal(natal), repository_root=ROOT
    )
    payload = profile.to_dict()

    assert payload["probability_used"] is False
    assert payload["numeric_magnitude_used"] is False
    assert payload["empirical_calibration_used"] is False
    assert payload["outcome_used"] is False
    assert payload["dynamic_effects"] == []
    assert "posterior" not in payload
    assert "weight" not in payload
    assert payload["maturity"]["predictive_validity"] == "NOT_VALIDATED"

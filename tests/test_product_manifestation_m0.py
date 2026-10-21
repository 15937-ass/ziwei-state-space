import json
from pathlib import Path

from src.product.manifestation_m0 import build_career_manifestation_candidates_m0
from src.product.manifestation_ontology import compile_manifestation_ontology_registry
from src.product.manifestation_router import compile_manifestation_mapping_registry
from src.product.response_profile import (
    CareerManifestationCandidate if False else CareerResponseEntry,
)
from src.product.response_profile import CareerResponseProfile


ROOT = Path(__file__).resolve().parents[1]
ONTOLOGY_FIXTURE = ROOT / "product/PL3M0_CAREER_ONTOLOGY_FIXTURE_v0.1.json"
MAPPING_FIXTURE = ROOT / "product/PL3M0_CAREER_MAPPING_FIXTURE_v0.1.json"
PROD_ONTOLOGY = ROOT / "product/PL3M_MANIFESTATION_ONTOLOGY_REGISTRY_v0.1.json"
PROD_MAPPING = ROOT / "product/PL3M_MANIFESTATION_MAPPING_REGISTRY_v0.1.json"


def _ontology(path=ONTOLOGY_FIXTURE):
    return compile_manifestation_ontology_registry(
        json.loads(path.read_text(encoding="utf-8"))
    )


def _mappings(path=MAPPING_FIXTURE):
    return compile_manifestation_mapping_registry(
        json.loads(path.read_text(encoding="utf-8"))
    )


def _entry(
    *,
    natal_rule_id="NATAL-FX-001",
    temporal_rule_id="TEMP-FX-001",
    reaction_id="REACTION-FX-001",
):
    return CareerResponseEntry(
        natal_rule_id=natal_rule_id,
        condition_id=f"PRODUCT_CONDITION:{natal_rule_id}",
        temporal_reaction_id=reaction_id,
        temporal_rule_id=temporal_rule_id,
        layer="YEAR",
        effect="ACTIVATE",
        effect_target="fixture-target",
        projection_domain="CAREER_TEST",
        projection_target="fixture-projection",
        magnitude_status="UNIDENTIFIED",
        natal_source_location="fixture natal source",
        natal_source_span_ids=("SPAN-FX-NATAL",),
        temporal_source_id="TEST-M0-SOURCE",
        temporal_source_location="fixture temporal source",
        temporal_review_status="TEST_ONLY",
        matched_natal_facts=("NATAL-FX-FACT",),
        matched_temporal_facts=("TEMP-FX-FACT",),
    )


def _tau(entries=(_entry(),), unknowns=()):
    return CareerResponseProfile(
        schema_version="0.1",
        profile_id="TAU-FX-001" if entries else "TAU-FX-EMPTY",
        compiler_version="PL3R_DECADE_YEAR_RESPONSE_COMPILER_V0_1",
        natal_profile_id="NATAL-FX",
        temporal_profile_id="TEMP-FX",
        knowledge_version="KB-FX",
        target_label="2030",
        active_layers=("DECADE", "YEAR"),
        matched_natal_rule_ids=tuple(
            sorted({item.natal_rule_id for item in entries})
        ),
        entries=tuple(entries),
        unknowns=tuple(unknowns),
        status=(
            "SOURCE_BACKED_SYMBOLIC_RESPONSE"
            if entries
            else "PARTIAL_UNKNOWN"
        ),
    )


def test_tau_rule_ids_route_one_source_supported_m0_and_hold_hypothesis():
    result = build_career_manifestation_candidates_m0(
        _tau(),
        _ontology(),
        _mappings(),
    )
    assert result.disposition == "ROUTED"
    assert len(result.candidates) == 1
    candidate = result.candidates[0]
    assert candidate.manifestation_id == "M0-FX-CAREER-SCENE"
    assert candidate.possibility_status == "SOURCE_SUPPORTED_POSSIBILITY"
    assert candidate.probability_status == "UNKNOWN"
    assert candidate.matched_rule_ids == ("TEMP-FX-001",)
    assert len(candidate.response_support) == 1
    support = candidate.response_support[0]
    assert support.natal_rule_id == "NATAL-FX-001"
    assert support.temporal_rule_id == "TEMP-FX-001"
    assert support.temporal_reaction_id == "REACTION-FX-001"
    assert [item.mapping_id for item in result.held_mappings] == [
        "M0-MAP-FX-HYPOTHESIS"
    ]
    assert result.empirical_probability_used is False
    assert result.ranking_used is False


def test_raw_rule_not_present_in_tau_cannot_trigger_m0():
    payload = json.loads(MAPPING_FIXTURE.read_text(encoding="utf-8"))
    payload["mappings"] = [
        {
            **payload["mappings"][0],
            "mapping_id": "M0-MAP-UNSEEN-RULE",
            "required_rule_ids": ["NATAL-NOT-IN-TAU"],
        }
    ]
    result = build_career_manifestation_candidates_m0(
        _tau(),
        _ontology(),
        compile_manifestation_mapping_registry(payload),
    )
    assert result.disposition == "NO_ACTIVE_MAPPING"
    assert result.candidates == ()
    assert "NO_ACTIVE_SOURCE_SUPPORTED_MAPPING" in result.blockers


def test_empty_tau_is_upstream_unknown_not_negative_prediction():
    result = build_career_manifestation_candidates_m0(
        _tau(
            entries=(),
            unknowns=(
                "PRODUCTION_TEMPORAL_RESPONSE_NOT_AVAILABLE",
                "NO_SOURCE_BACKED_DECADE_YEAR_RESPONSE",
            ),
        ),
        _ontology(PROD_ONTOLOGY),
        _mappings(PROD_MAPPING),
    )
    assert result.disposition == "UPSTREAM_RESPONSE_NOT_READY"
    assert result.candidates == ()
    assert "UPSTREAM_RESPONSE_PROFILE_HAS_NO_DYNAMIC_ENTRIES" in result.blockers
    assert "ONTOLOGY_NOT_READY" in result.blockers
    assert "MAPPING_REGISTRY_NOT_READY" in result.blockers
    assert "PRODUCTION_TEMPORAL_RESPONSE_NOT_AVAILABLE" in result.upstream_unknowns
    assert result.probability_status == "UNKNOWN"


def test_nonempty_tau_still_fails_closed_on_pending_production_ontology():
    result = build_career_manifestation_candidates_m0(
        _tau(),
        _ontology(PROD_ONTOLOGY),
        _mappings(PROD_MAPPING),
    )
    assert result.disposition == "ONTOLOGY_NOT_READY"
    assert result.candidates == ()
    assert "ONTOLOGY_NOT_READY" in result.blockers
    assert "MAPPING_REGISTRY_NOT_READY" in result.blockers


def test_result_id_is_deterministic():
    first = build_career_manifestation_candidates_m0(
        _tau(),
        _ontology(),
        _mappings(),
    )
    second = build_career_manifestation_candidates_m0(
        _tau(),
        _ontology(),
        _mappings(),
    )
    assert first.result_id == second.result_id
    assert first.to_dict() == second.to_dict()

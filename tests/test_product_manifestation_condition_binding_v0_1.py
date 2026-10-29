import copy
import json
from pathlib import Path

import pytest

from src.product.manifestation_condition_binding_v0_1 import (
    AlternativeConditionV01,
    CrossPalaceDependencyV01,
    SourceTextOnlyConditionV01,
    compile_fixture_registry,
    compile_manifestation_condition_binding,
)
from src.product.manifestation_crosswalk import classify_mapping_crosswalk


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "product/PL3M_MANIFESTATION_CONDITION_BINDING_FIXTURES_V0_1.json"
MAPPING_DIR = ROOT / "knowledge/core/wp06c/canonical_mappings"
PROD_ONTOLOGY = ROOT / "product/PL3M_MANIFESTATION_ONTOLOGY_REGISTRY_v0.1.json"
PROD_MAPPING = ROOT / "product/PL3M_MANIFESTATION_MAPPING_REGISTRY_v0.1.json"


def _load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def _mapping(mapping_id):
    return _load(MAPPING_DIR / f"{mapping_id}.json")


def _fixture(mapping_id):
    registry = _load(FIXTURES)
    return next(
        row for row in registry["fixtures"] if row["mapping_id"] == mapping_id
    )


def test_curated_registry_compiles_exactly_three_bounded_mappings():
    registry = _load(FIXTURES)
    canonical = {
        mapping_id: _mapping(mapping_id)
        for mapping_id in ("KMM-000007", "KMM-000008", "KMM-000009")
    }
    compiled = compile_fixture_registry(canonical, registry)

    assert tuple(item.mapping_id for item in compiled) == (
        "KMM-000007",
        "KMM-000008",
        "KMM-000009",
    )
    assert all(item.runtime_authorized is False for item in compiled)
    assert all(item.probability_status == "UNKNOWN" for item in compiled)


def test_pg006_cross_palace_dependency_is_explicit_and_verbatim():
    canonical = _mapping("KMM-000007")
    binding = compile_manifestation_condition_binding(
        canonical, _fixture("KMM-000007")
    )

    assert binding.condition_kind == "CROSS_PALACE_DEPENDENCY"
    assert isinstance(binding.condition, CrossPalaceDependencyV01)
    assert binding.condition.relation == "OPPOSITE_PALACE"
    assert binding.condition.context_text == "辰戌宫破军"
    assert binding.condition.dependency_text == "对宫[紫微天相]"
    assert binding.condition.dependency_text in binding.source_condition_text
    assert binding.temporal_binding.source_time_layer == "NATAL"
    assert binding.temporal_binding.required_scopes == ("NATAL",)
    assert "Do not drop the opposite-palace" in " ".join(
        binding.forbidden_inferences
    )


def test_pg006_source_explicit_or_cannot_be_collapsed_to_and():
    canonical = _mapping("KMM-000008")
    fixture = _fixture("KMM-000008")
    binding = compile_manifestation_condition_binding(canonical, fixture)

    assert binding.condition_kind == "ALTERNATIVES"
    assert isinstance(binding.condition, AlternativeConditionV01)
    assert binding.condition.operator == "OR"
    assert binding.condition.source_operator_token == "或"
    assert binding.condition.alternatives == (
        "廉贞化忌",
        "天相为刑忌所夹",
    )
    assert "Do not collapse the source-explicit 或 into an AND" in " ".join(
        binding.forbidden_inferences
    )

    invalid = copy.deepcopy(fixture)
    invalid["condition"]["operator"] = "AND"
    with pytest.raises(ValueError, match="must remain OR"):
        compile_manifestation_condition_binding(canonical, invalid)


def test_pg007_decade_year_expands_to_two_required_scopes_only():
    canonical = _mapping("KMM-000009")
    fixture = _fixture("KMM-000009")
    binding = compile_manifestation_condition_binding(canonical, fixture)

    assert binding.condition_kind == "SOURCE_TEXT_ONLY"
    assert isinstance(binding.condition, SourceTextOnlyConditionV01)
    assert binding.temporal_binding.source_time_layer == "DECADE_YEAR"
    assert binding.temporal_binding.required_scopes == ("DECADE", "YEAR")
    assert binding.temporal_binding.event_outcome_inference_allowed is False
    assert "dual layer" in " ".join(binding.forbidden_inferences)

    collapsed = copy.deepcopy(fixture)
    collapsed["temporal_binding"]["required_scopes"] = ["DECADE"]
    with pytest.raises(ValueError, match="must expand exactly"):
        compile_manifestation_condition_binding(canonical, collapsed)


def test_fixture_must_match_canonical_text_and_does_not_discover_semantics():
    canonical = _mapping("KMM-000007")
    fixture = _fixture("KMM-000007")

    changed = copy.deepcopy(fixture)
    changed["source_condition_text"] = "rewritten condition"
    with pytest.raises(ValueError, match="exactly match canonical"):
        compile_manifestation_condition_binding(canonical, changed)

    changed = copy.deepcopy(fixture)
    changed["condition"]["dependency_text"] = "紫微天相"
    # The retained dependency must include the source-explicit palace relation,
    # not merely a nearby star label.
    with pytest.raises(ValueError, match="verbatim"):
        compile_manifestation_condition_binding(canonical, changed)


def test_unresolved_hold_mappings_are_not_compiled_by_condition_contract():
    for mapping_id in ("KMM-000001", "KMM-000004"):
        canonical = _mapping(mapping_id)
        assert (
            classify_mapping_crosswalk(canonical).crosswalk_disposition
            == "HOLD"
        )

        fake_fixture = {
            "schema_version": "0.1",
            "fixture_id": f"FORBIDDEN-{mapping_id}",
            "mapping_id": mapping_id,
            "source_condition_text": canonical["conditions"]["source_condition_text"],
            "condition_kind": "SOURCE_TEXT_ONLY",
            "condition": {
                "source_text": canonical["conditions"]["source_condition_text"]
            },
            "temporal_binding": {
                "source_time_layer": canonical["conditions"]["time_layer"],
                "required_scopes": ["NATAL"],
                "binding_mode": "EXACT_DECLARED_SCOPES",
                "event_outcome_inference_allowed": False,
            },
        }
        with pytest.raises(ValueError, match="must remain HOLD"):
            compile_manifestation_condition_binding(canonical, fake_fixture)


def test_production_registries_remain_empty_and_fail_closed():
    fixtures = _load(FIXTURES)
    assert fixtures["production_boundary"]["production_registry_population_allowed"] is False
    assert fixtures["production_boundary"]["active_kib_promotion_allowed"] is False
    assert fixtures["production_boundary"]["runtime_execution_allowed"] is False
    assert fixtures["production_boundary"]["probability_claim_allowed"] is False
    assert fixtures["production_boundary"]["predictive_validity_claim_allowed"] is False

    ontology = _load(PROD_ONTOLOGY)
    mappings = _load(PROD_MAPPING)
    assert ontology["registry_status"] == "EMPTY_PENDING_KB_WP06B"
    assert ontology["nodes"] == []
    assert mappings["registry_status"] == "EMPTY_PENDING_KB_WP06C"
    assert mappings["mappings"] == []

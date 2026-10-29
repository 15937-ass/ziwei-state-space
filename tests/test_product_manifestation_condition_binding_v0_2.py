import copy
import json
from pathlib import Path

import pytest

from src.product.manifestation_condition_binding_v0_1 import (
    TEMPORAL_SCOPE_MAP as TEMPORAL_SCOPE_MAP_V01,
    compile_fixture_registry as compile_fixture_registry_v01,
)
from src.product.manifestation_condition_binding_v0_2 import (
    ALLOWED_MAPPING_IDS,
    BranchedConditionalV02,
    ListedVariantSetV02,
    PalaceScopedExceptionV02,
    QualifiedConditionV02,
    SourceTextOnlyConditionV02,
    compile_fixture_registry_v02,
    compile_manifestation_condition_binding_v02,
)


ROOT = Path(__file__).resolve().parents[1]
FIXTURES_V01 = ROOT / "product/PL3M_MANIFESTATION_CONDITION_BINDING_FIXTURES_V0_1.json"
FIXTURES_V02 = ROOT / "product/PL3M_MANIFESTATION_CONDITION_BINDING_FIXTURES_V0_2.json"
MAPPING_DIR = ROOT / "knowledge/core/wp06c/canonical_mappings"
ONTOLOGY_REGISTRY = ROOT / "product/PL3M_MANIFESTATION_ONTOLOGY_REGISTRY_v0.1.json"
MAPPING_REGISTRY = ROOT / "product/PL3M_MANIFESTATION_MAPPING_REGISTRY_v0.1.json"


def _load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def _mapping(mapping_id):
    return _load(MAPPING_DIR / f"{mapping_id}.json")


def _fixture(mapping_id):
    registry = _load(FIXTURES_V02)
    return next(
        row for row in registry["fixtures"] if row["mapping_id"] == mapping_id
    )


def test_v02_registry_is_exactly_the_bounded_pg008_011_mapping_set():
    registry = _load(FIXTURES_V02)
    canonical = {
        mapping_id: _mapping(mapping_id)
        for mapping_id in sorted(ALLOWED_MAPPING_IDS)
    }
    compiled = compile_fixture_registry_v02(canonical, registry)

    assert tuple(item.mapping_id for item in compiled) == (
        "KMM-000010",
        "KMM-000012",
        "KMM-000013",
        "KMM-000014",
        "KMM-000015",
    )
    assert all(item.runtime_authorized is False for item in compiled)
    assert all(item.probability_status == "UNKNOWN" for item in compiled)


def test_pg008_decade_is_one_exact_scope_without_event_inference():
    canonical = _mapping("KMM-000010")
    fixture = _fixture("KMM-000010")
    binding = compile_manifestation_condition_binding_v02(canonical, fixture)

    assert isinstance(binding.condition, SourceTextOnlyConditionV02)
    assert binding.temporal_binding.source_time_layer == "DECADE"
    assert binding.temporal_binding.required_scopes == ("DECADE",)
    assert binding.temporal_binding.event_outcome_inference_allowed is False

    collapsed = copy.deepcopy(fixture)
    collapsed["temporal_binding"]["required_scopes"] = ["YEAR"]
    with pytest.raises(ValueError, match="must expand exactly"):
        compile_manifestation_condition_binding_v02(canonical, collapsed)


def test_pg009_listed_variants_are_non_conjunctive_without_fabricated_or():
    canonical = _mapping("KMM-000012")
    fixture = _fixture("KMM-000012")
    binding = compile_manifestation_condition_binding_v02(canonical, fixture)

    assert isinstance(binding.condition, ListedVariantSetV02)
    assert binding.condition.variants == ("羊陀夹", "火铃夹", "空劫夹")
    assert (
        binding.condition.combination_semantics
        == "SEPARATE_VARIANTS_NOT_ALL_REQUIRED"
    )
    assert binding.condition.source_operator_token is None
    assert "或" not in binding.source_condition_text
    assert (
        binding.condition.boundary_evidence_text
        in binding.forbidden_inferences
    )

    fabricated = copy.deepcopy(fixture)
    fabricated["condition"]["source_operator_token"] = "或"
    with pytest.raises(ValueError, match="verbatim"):
        compile_manifestation_condition_binding_v02(canonical, fabricated)

    invented_boundary = copy.deepcopy(fixture)
    invented_boundary["condition"]["boundary_evidence_text"] = "invented boundary"
    with pytest.raises(ValueError, match="canonical forbidden_inferences"):
        compile_manifestation_condition_binding_v02(
            canonical, invented_boundary
        )


def test_pg010_kmm13_preserves_three_branches_and_simultaneous_requirements():
    canonical = _mapping("KMM-000013")
    fixture = _fixture("KMM-000013")
    binding = compile_manifestation_condition_binding_v02(canonical, fixture)

    assert isinstance(binding.condition, BranchedConditionalV02)
    assert tuple(branch.branch_id for branch in binding.condition.branches) == (
        "TALENT_STARS",
        "ZOUSHU",
        "QINGKE",
    )
    qingke = binding.condition.branches[2]
    assert qingke.operator is not None
    assert qingke.operator.operator == "SIMULTANEOUS_IF"
    assert qingke.operator.source_token == "若同时"
    assert qingke.simultaneous_requirements == ("见煞", "昌曲化忌")
    assert (
        binding.condition.boundary_evidence_text
        in binding.forbidden_inferences
    )

    dropped_requirement = copy.deepcopy(fixture)
    dropped_requirement["condition"]["branches"][2][
        "simultaneous_requirements"
    ] = ["见煞"]
    with pytest.raises(ValueError, match="at least two simultaneous requirements"):
        compile_manifestation_condition_binding_v02(
            canonical, dropped_requirement
        )

    no_canonical_modality = copy.deepcopy(canonical)
    no_canonical_modality["conditions"]["modality_terms"] = []
    with pytest.raises(ValueError, match="canonical modality_terms"):
        compile_manifestation_condition_binding_v02(
            no_canonical_modality, fixture
        )


def test_pg010_pg011_kmm14_keeps_unless_and_named_life_palace_scope():
    canonical = _mapping("KMM-000014")
    fixture = _fixture("KMM-000014")
    binding = compile_manifestation_condition_binding_v02(canonical, fixture)

    assert isinstance(binding.condition, PalaceScopedExceptionV02)
    assert binding.condition.operator.operator == "UNLESS"
    assert binding.condition.operator.source_token == "除非"
    assert binding.condition.dependency.palace_scope == "LIFE_PALACE"
    assert binding.condition.dependency.source_palace_token == "命宫"
    assert binding.condition.dependency.dependency_text == "命宫见辅弼"

    coerced_opposite = copy.deepcopy(fixture)
    coerced_opposite["condition"]["dependency"]["palace_scope"] = (
        "OPPOSITE_PALACE"
    )
    with pytest.raises(ValueError, match="unsupported bounded palace_scope"):
        compile_manifestation_condition_binding_v02(
            canonical, coerced_opposite
        )

    dropped_palace = copy.deepcopy(fixture)
    dropped_palace["condition"]["dependency"]["dependency_text"] = "见辅弼"
    with pytest.raises(ValueError, match="named palace token|verbatim"):
        compile_manifestation_condition_binding_v02(
            canonical, dropped_palace
        )


def test_pg010_kmm15_keeps_even_if_as_source_explicit_qualifier():
    canonical = _mapping("KMM-000015")
    fixture = _fixture("KMM-000015")
    binding = compile_manifestation_condition_binding_v02(canonical, fixture)

    assert isinstance(binding.condition, QualifiedConditionV02)
    assert binding.condition.operator.operator == "EVEN_IF"
    assert binding.condition.operator.source_token == "即使"
    assert binding.condition.context_text == "巳亥[武破]守兄弟宫"
    assert binding.condition.qualified_text == "见吉曜"

    wrong_operator = copy.deepcopy(fixture)
    wrong_operator["condition"]["operator"]["operator"] = "UNLESS"
    with pytest.raises(ValueError, match="must retain exact source token"):
        compile_manifestation_condition_binding_v02(
            canonical, wrong_operator
        )


def test_v02_does_not_expand_scope_to_unresolved_or_unlisted_mappings():
    registry = _load(FIXTURES_V02)
    missing = copy.deepcopy(registry)
    missing["fixtures"] = [
        row for row in missing["fixtures"] if row["mapping_id"] != "KMM-000015"
    ]
    canonical = {
        mapping_id: _mapping(mapping_id)
        for mapping_id in sorted(ALLOWED_MAPPING_IDS)
    }
    with pytest.raises(ValueError, match="exact bounded mapping set"):
        compile_fixture_registry_v02(canonical, missing)

    out_of_scope = _mapping("KMM-000011")
    fake_fixture = copy.deepcopy(_fixture("KMM-000010"))
    fake_fixture["mapping_id"] = "KMM-000011"
    fake_fixture["source_condition_text"] = out_of_scope["conditions"][
        "source_condition_text"
    ]
    with pytest.raises(ValueError, match="outside bounded v0.2 scope"):
        compile_manifestation_condition_binding_v02(
            out_of_scope, fake_fixture
        )


def test_v01_contract_remains_unchanged_and_reproducible():
    assert "DECADE" not in TEMPORAL_SCOPE_MAP_V01

    registry = _load(FIXTURES_V01)
    canonical = {
        mapping_id: _mapping(mapping_id)
        for mapping_id in ("KMM-000007", "KMM-000008", "KMM-000009")
    }
    compiled = compile_fixture_registry_v01(canonical, registry)
    assert tuple(item.mapping_id for item in compiled) == (
        "KMM-000007",
        "KMM-000008",
        "KMM-000009",
    )


def test_production_registries_remain_empty_and_fail_closed():
    registry = _load(FIXTURES_V02)
    for key, value in registry["production_boundary"].items():
        assert value is False, key

    ontology = _load(ONTOLOGY_REGISTRY)
    mappings = _load(MAPPING_REGISTRY)
    assert ontology["registry_status"] == "EMPTY_PENDING_KB_WP06B"
    assert ontology["nodes"] == []
    assert mappings["registry_status"] == "EMPTY_PENDING_KB_WP06C"
    assert mappings["mappings"] == []

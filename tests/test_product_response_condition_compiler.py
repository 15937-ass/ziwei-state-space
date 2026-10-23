import copy
import json
from pathlib import Path

import pytest

from src.product.response_condition_compiler import (
    COMPILER_VERSION,
    DEPENDENCY_STATUS,
    DIRECT_STATUS,
    REJECTION_STATUS,
    _compile_direct_record,
    compile_career_condition_registry,
)
from src.product.response_semantics_adapter import (
    load_career_compiler_readiness_census,
    load_career_dependency_ir,
    load_career_direct_condition_ir,
)


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "product" / "CAREER_CONDITION_COMPILER_PILOT_v0.1.json"

READY_IDS = {
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
}

DEPENDENCY_PARENT = {
    "CA05-420": "CA05-419",
    "CA07-639": "CA07-638",
    "CA07-682": "CA07-681",
}


def _stored():
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def test_compiler_registry_matches_deterministic_generation():
    assert compile_career_condition_registry() == _stored()


def test_compiler_covers_exact_promoted_ready_set_only():
    payload = compile_career_condition_registry()
    compiled = payload["compiled_conditions"]
    ids = {item["source_rule_id"] for item in compiled}

    assert ids == READY_IDS
    assert payload["summary"] == {
        "knowledge_condition_ir_ready": 12,
        "compiled_conditions": 12,
        "compiled_direct": 9,
        "compiled_dependency_reference": 3,
        "local_ready_not_compiler_input": 14,
        "condition_evaluated": 0,
        "response_effect_bound": 0,
        "runtime_effects_authorized": 0,
    }


def test_direct_and_dependency_compilation_remain_separate():
    payload = compile_career_condition_registry()
    by_id = {
        item["source_rule_id"]: item
        for item in payload["compiled_conditions"]
    }

    for rule_id in READY_IDS - set(DEPENDENCY_PARENT):
        row = by_id[rule_id]
        assert row["compiler_status"] == DIRECT_STATUS
        assert row["source_ir_kind"] == "DIRECT_CONDITION_IR"
        assert row["parent_condition_id"] is None
        assert row["subject_terms"]
        assert row["target"] is not None

    for child, parent in DEPENDENCY_PARENT.items():
        row = by_id[child]
        assert row["compiler_status"] == DEPENDENCY_STATUS
        assert row["source_ir_kind"] == "DEPENDENCY_CONDITION_IR"
        assert row["parent_condition_id"] == f"PRODUCT_CONDITION:{parent}"
        assert row["subject_terms"] == []
        assert row["relation"] is None
        assert row["target"] is None
        assert row["source_expression_ref"] == f"RULE_CONDITION({parent})"


def test_dependency_compiler_never_copies_prohibited_parent_semantics():
    payload = compile_career_condition_registry()
    by_id = {
        item["source_rule_id"]: item
        for item in payload["compiled_conditions"]
    }
    expected = {
        "PARENT_PROJECTION",
        "PARENT_OUTCOME",
        "PARENT_TARGET",
        "PARENT_VALENCE",
        "TEXT_ADJACENCY",
    }

    for child in DEPENDENCY_PARENT:
        row = by_id[child]
        assert set(row["prohibited_inheritance"]) == expected
        serialized = json.dumps(row, ensure_ascii=False)
        assert '"projection"' not in serialized
        assert '"outcome"' not in serialized
        assert '"valence"' not in serialized


def test_compilation_uses_structured_ir_not_free_form_source_prose():
    source = load_career_direct_condition_ir()["records"][0]
    baseline = _compile_direct_record(source).to_dict()

    mutated = copy.deepcopy(source)
    mutated["source_condition_text"] = (
        "THIS PROSE MUST NOT PARTICIPATE IN PRODUCT COMPILATION"
    )
    mutated["source_location"] = {"book": "changed audit-only metadata"}
    assert _compile_direct_record(mutated).to_dict() == baseline


def test_supported_relation_geometry_is_preserved_without_inference():
    payload = compile_career_condition_registry()
    by_id = {
        item["source_rule_id"]: item
        for item in payload["compiled_conditions"]
    }

    same_palace = by_id["CA02-181"]["relation"]
    assert same_palace == {
        "operator": "EXACT_GEOMETRY",
        "geometry": "SAME_PALACE",
        "palace_offsets": [0],
    }

    four_directions = by_id["CA05-419"]["relation"]
    assert four_directions == {
        "operator": "FOUR_DIRECTIONS_VISIBILITY",
        "geometry": "UNSPECIFIED_WITHIN_SCOPE",
        "palace_offsets": [0, 4, 6, 8],
    }
    assert by_id["CA07-681"]["relation"] is None
    assert by_id["CA09-820"]["relation"] is None


def test_member_requirements_and_typed_terms_are_not_globalized():
    payload = compile_career_condition_registry()
    by_id = {
        item["source_rule_id"]: item
        for item in payload["compiled_conditions"]
    }

    assert by_id["CA02-181"]["target"]["member_requirement"] == "PAIR_REQUIRED"
    assert by_id["CA03-228"]["target"]["member_requirement"] == "ANY_SOURCE_LOCAL"
    assert by_id["CA07-638"]["target"]["member_requirement"] == "BOTH_SOURCE_LITERAL"
    assert by_id["CA05-433"]["target"]["member_requirement"] == "BOTH_SOURCE_LOCAL"

    local_or = by_id["CA09-820"]["target"]
    assert local_or["node_type"] == "LOCAL_OR"
    assert [item["term_type"] for item in local_or["members"]] == [
        "TRANSFORM",
        "TRANSFORM",
        "TRANSFORM",
        "ATOM",
    ]


def test_unsupported_relation_geometry_fails_closed():
    source = copy.deepcopy(load_career_direct_condition_ir()["records"][0])
    source["condition_ir"]["relation"]["geometry"] = "GENERIC_MEETING"

    with pytest.raises(ValueError, match="EXACT_GEOMETRY"):
        _compile_direct_record(source)


def test_fourteen_local_ready_non_ir_rows_are_explicit_rejections():
    payload = compile_career_condition_registry()
    rejected = payload["rejected_local_ready_rows"]
    census = load_career_compiler_readiness_census()

    expected = {
        item["source_rule_id"]
        for item in census["records"]
        if item["knowledge_condition_ir_ready"] is False
    }
    assert len(rejected) == 14
    assert {item["source_rule_id"] for item in rejected} == expected
    assert all(item["compiler_status"] == REJECTION_STATUS for item in rejected)
    assert all(item["product_condition_compiled"] is False for item in rejected)
    assert all(item["runtime_effect_allowed"] is False for item in rejected)


def test_product_compilation_does_not_rewrite_knowledge_ir_flags():
    direct = load_career_direct_condition_ir()
    dependency = load_career_dependency_ir()

    assert all(
        item["product_condition_compiled"] is False
        and item["runtime_authorized"] is False
        for item in direct["records"]
    )
    assert all(
        item["product_condition_compiled"] is False
        and item["runtime_authorized"] is False
        for item in dependency["records"]
    )


def test_compiled_conditions_are_not_evaluated_or_effect_bound_or_authorized():
    payload = compile_career_condition_registry()
    for item in payload["compiled_conditions"]:
        assert item["compiler_version"] == COMPILER_VERSION
        assert item["product_condition_compiled"] is True
        assert item["condition_evaluated"] is False
        assert item["response_effect_bound"] is False
        assert item["runtime_effect_allowed"] is False


def test_compiler_output_contains_no_probability_or_numeric_weight_fields():
    serialized = json.dumps(
        compile_career_condition_registry(),
        ensure_ascii=False,
    ).lower()
    for forbidden in (
        '"probability"',
        '"posterior"',
        '"learned_weight"',
        '"numeric_gain"',
        '"effect_weight"',
        '"confidence_score"',
        '"reward"',
    ):
        assert forbidden not in serialized

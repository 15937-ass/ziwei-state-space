import json
from pathlib import Path

from src.product.manifestation_adapter_contract_v0_2 import (
    compile_mapping_adapter_envelope,
    compile_node_adapter_envelope,
)
from src.product.manifestation_condition_binding_v0_1 import (
    TEMPORAL_SCOPE_MAP,
    compile_fixture_registry,
)


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "product/PL3M_MANIFESTATION_P3_READINESS_AUDIT_V0_1.json"
FIXTURES = ROOT / "product/PL3M_MANIFESTATION_CONDITION_BINDING_FIXTURES_V0_1.json"
NODE_DIR = ROOT / "knowledge/core/wp06b/canonical_manifestations"
MAPPING_DIR = ROOT / "knowledge/core/wp06c/canonical_mappings"
ONTOLOGY_REGISTRY = ROOT / "product/PL3M_MANIFESTATION_ONTOLOGY_REGISTRY_v0.1.json"
MAPPING_REGISTRY = ROOT / "product/PL3M_MANIFESTATION_MAPPING_REGISTRY_v0.1.json"


def _load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def _mapping(mapping_id):
    return _load(MAPPING_DIR / f"{mapping_id}.json")


def _audit_row(mapping_id):
    audit = _load(AUDIT)
    return next(row for row in audit["mapping_audit"] if row["mapping_id"] == mapping_id)


def test_all_15_canonical_nodes_are_losslessly_preservable_by_v02_envelope():
    for index in range(1, 16):
        node_id = f"KMN-{index:06d}"
        raw = _load(NODE_DIR / f"{node_id}.json")
        envelope = compile_node_adapter_envelope(raw)

        assert envelope.manifestation_id == node_id
        assert envelope.output_kind.value == raw["output_kind"]["value"]
        assert envelope.event_specificity.value == raw["event_specificity"]["value"]
        assert envelope.source_epistemic == raw["source_epistemic"]
        assert envelope.normalization_epistemic == raw["normalization_epistemic"]
        assert envelope.probability_status == "UNKNOWN"
        assert envelope.runtime_authorized is False


def test_all_15_mapping_metadata_envelopes_preserve_fail_closed_boundaries():
    for index in range(1, 16):
        mapping_id = f"KMM-{index:06d}"
        raw = _mapping(mapping_id)
        envelope = compile_mapping_adapter_envelope(raw)

        assert envelope.mapping_id == mapping_id
        assert envelope.source_epistemic == raw["source_epistemic"]
        assert envelope.normalization_epistemic == raw["normalization_epistemic"]
        assert envelope.conditions.time_layer == raw["conditions"]["time_layer"]
        assert envelope.conditions.source_condition_text == raw["conditions"]["source_condition_text"]
        assert envelope.execution_boundary.execution_readiness == raw["execution_readiness"]
        assert envelope.execution_boundary.forbidden_inferences == tuple(raw["forbidden_inferences"])
        assert envelope.execution_boundary.runtime_authorized is False
        assert envelope.probability_status == "UNKNOWN"


def test_existing_semantic_holds_remain_holds_not_product_gap_rewrites():
    for mapping_id in ("KMM-000001", "KMM-000004", "KMM-000011"):
        raw = _mapping(mapping_id)
        assert raw["conditions"]["unresolved_semantics"]
        assert _audit_row(mapping_id)["verdict"] == "HOLD"


def test_product_916_structured_examples_remain_lossless_and_non_executable():
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
    for item in compiled:
        assert _audit_row(item.mapping_id)["verdict"] == "LOSSLESS_STRUCTURED_NONEXECUTABLE"


def test_pg008_detects_accepted_decade_layer_outside_current_structured_binding():
    raw = _mapping("KMM-000010")
    assert raw["conditions"]["time_layer"] == "DECADE"
    assert "DECADE" not in TEMPORAL_SCOPE_MAP
    row = _audit_row("KMM-000010")
    assert row["verdict"] == "GAP_PRODUCT"
    assert row["gap_ids"] == ["PG-008"]


def test_pg009_preserves_listed_variants_without_inventing_an_or_token():
    raw = _mapping("KMM-000012")
    source = raw["conditions"]["source_condition_text"]
    assert "或" not in source
    assert "Do not require 羊陀夹、火铃夹、空劫夹 to occur together" in " ".join(
        raw["forbidden_inferences"]
    )
    row = _audit_row("KMM-000012")
    assert row["verdict"] == "GAP_PRODUCT"
    assert row["gap_ids"] == ["PG-009"]


def test_pg010_pg011_are_source_explicit_structural_pressures_not_invented_semantics():
    m13 = _mapping("KMM-000013")
    m14 = _mapping("KMM-000014")
    m15 = _mapping("KMM-000015")

    assert m13["conditions"]["modality_terms"] == ["若同时"]
    assert "同时" in m13["conditions"]["source_condition_text"]
    assert _audit_row("KMM-000013")["gap_ids"] == ["PG-010"]

    assert m14["conditions"]["modality_terms"] == ["除非"]
    assert "命宫见辅弼" in m14["conditions"]["source_condition_text"]
    assert _audit_row("KMM-000014")["gap_ids"] == ["PG-010", "PG-011"]

    assert m15["conditions"]["modality_terms"] == ["即使"]
    assert "即使" in m15["conditions"]["source_condition_text"]
    assert _audit_row("KMM-000015")["gap_ids"] == ["PG-010"]


def test_p3_verdict_is_not_ready_and_production_remains_fail_closed():
    audit = _load(AUDIT)

    assert audit["status"] == "P3_NOT_READY_NEW_PRODUCT_GAPS"
    assert audit["freeze_readiness"]["canonical_node_envelope"] == "READY_FOR_P3_FREEZE"
    assert audit["freeze_readiness"]["canonical_mapping_metadata_envelope"] == "READY_FOR_P3_FREEZE"
    assert audit["freeze_readiness"]["structured_condition_binding"] == "NOT_READY"
    assert audit["freeze_readiness"]["formal_crosswalk_freeze"] == "NOT_READY"
    assert [row["gap_id"] for row in audit["new_gap_register"]] == [
        "PG-008",
        "PG-009",
        "PG-010",
        "PG-011",
    ]

    for key, value in audit["production_boundary"].items():
        assert value is False, key

    ontology = _load(ONTOLOGY_REGISTRY)
    mappings = _load(MAPPING_REGISTRY)
    assert ontology["nodes"] == []
    assert mappings["mappings"] == []

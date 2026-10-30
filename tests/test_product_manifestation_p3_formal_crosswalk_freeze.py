import hashlib
import json
from pathlib import Path

from src.product.manifestation_adapter_contract_v0_2 import (
    compile_mapping_adapter_envelope,
    compile_node_adapter_envelope,
)
from src.product.manifestation_condition_binding_v0_1 import (
    compile_fixture_registry as compile_fixture_registry_v01,
)
from src.product.manifestation_condition_binding_v0_2 import (
    compile_fixture_registry_v02,
)


ROOT = Path(__file__).resolve().parents[1]
FREEZE = ROOT / "product/PL3M_MANIFESTATION_P3_FORMAL_CROSSWALK_FREEZE_V0_1.json"
NODE_INDEX = ROOT / "knowledge/core/wp06b/CANONICAL_MANIFESTATION_NODE_INDEX_v0.1.json"
MAPPING_INDEX = ROOT / "knowledge/core/wp06c/CANONICAL_MANIFESTATION_MAPPING_INDEX_v0.1.json"
NODE_DIR = ROOT / "knowledge/core/wp06b/canonical_manifestations"
MAPPING_DIR = ROOT / "knowledge/core/wp06c/canonical_mappings"
FIXTURES_V01 = ROOT / "product/PL3M_MANIFESTATION_CONDITION_BINDING_FIXTURES_V0_1.json"
FIXTURES_V02 = ROOT / "product/PL3M_MANIFESTATION_CONDITION_BINDING_FIXTURES_V0_2.json"
ONTOLOGY_REGISTRY = ROOT / "product/PL3M_MANIFESTATION_ONTOLOGY_REGISTRY_v0.1.json"
MAPPING_REGISTRY = ROOT / "product/PL3M_MANIFESTATION_MAPPING_REGISTRY_v0.1.json"


def _load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def _mapping(mapping_id):
    return _load(MAPPING_DIR / f"{mapping_id}.json")


def _git_blob_sha(path):
    data = path.read_bytes()
    payload = f"blob {len(data)}\0".encode("ascii") + data
    return hashlib.sha1(payload).hexdigest()


def test_freeze_pins_match_exact_current_file_blobs():
    freeze = _load(FREEZE)
    for pin in freeze["pins"]:
        path = ROOT / pin["path"]
        assert path.exists(), pin["path"]
        assert _git_blob_sha(path) == pin["git_blob_sha"], pin["path"]


def test_freeze_corpus_is_exactly_15_kmn_and_15_kmm():
    freeze = _load(FREEZE)
    node_index = _load(NODE_INDEX)
    mapping_index = _load(MAPPING_INDEX)

    assert freeze["corpus"]["accepted_kmn_count"] == 15
    assert freeze["corpus"]["accepted_kmm_count"] == 15
    assert freeze["corpus"]["next_kmn_id"] == "KMN-000016"
    assert freeze["corpus"]["next_kmm_id"] == "KMM-000016"
    assert freeze["corpus"]["auto_extend_to_future_mappings"] is False

    assert node_index["coverage"]["production_node_count"] == 15
    assert mapping_index["coverage"]["canonical_mapping_count"] == 15
    assert tuple(row["manifestation_id"] for row in node_index["nodes"]) == tuple(
        f"KMN-{index:06d}" for index in range(1, 16)
    )
    assert tuple(row["mapping_id"] for row in mapping_index["mappings"]) == tuple(
        f"KMM-{index:06d}" for index in range(1, 16)
    )


def test_all_15_node_and_mapping_envelopes_remain_lossless_and_fail_closed():
    for index in range(1, 16):
        node_id = f"KMN-{index:06d}"
        mapping_id = f"KMM-{index:06d}"

        node_raw = _load(NODE_DIR / f"{node_id}.json")
        mapping_raw = _mapping(mapping_id)

        node = compile_node_adapter_envelope(node_raw)
        mapping = compile_mapping_adapter_envelope(mapping_raw)

        assert node.manifestation_id == node_id
        assert node.output_kind.value == node_raw["output_kind"]["value"]
        assert node.event_specificity.value == node_raw["event_specificity"]["value"]
        assert node.source_epistemic == node_raw["source_epistemic"]
        assert node.normalization_epistemic == node_raw["normalization_epistemic"]
        assert node.runtime_authorized is False
        assert node.probability_status == "UNKNOWN"

        assert mapping.mapping_id == mapping_id
        assert mapping.conditions.time_layer == mapping_raw["conditions"]["time_layer"]
        assert (
            mapping.conditions.source_condition_text
            == mapping_raw["conditions"]["source_condition_text"]
        )
        assert mapping.source_epistemic == mapping_raw["source_epistemic"]
        assert mapping.normalization_epistemic == mapping_raw["normalization_epistemic"]
        assert (
            mapping.execution_boundary.forbidden_inferences
            == tuple(mapping_raw["forbidden_inferences"])
        )
        assert mapping.execution_boundary.runtime_authorized is False
        assert mapping.probability_status == "UNKNOWN"


def test_explicit_hold_set_is_exact_and_remains_unresolved():
    freeze = _load(FREEZE)
    matrix = {
        row["mapping_id"]: row
        for row in freeze["mapping_freeze_matrix"]
    }
    expected_holds = {"KMM-000001", "KMM-000004", "KMM-000011"}

    actual_holds = {
        mapping_id
        for mapping_id, row in matrix.items()
        if row["representation"] == "EXPLICIT_HOLD"
    }
    assert actual_holds == expected_holds

    for mapping_id in expected_holds:
        raw = _mapping(mapping_id)
        assert raw["conditions"]["unresolved_semantics"]
        assert raw["executable"] is False
        assert raw["product_consumable"] is False
        assert raw["probability_status"] == "UNKNOWN"


def test_v01_structured_contract_freezes_exactly_kmm_000007_to_000009():
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
    assert all(item.runtime_authorized is False for item in compiled)
    assert all(item.probability_status == "UNKNOWN" for item in compiled)


def test_v02_structured_contract_freezes_exactly_new_five_examples():
    registry = _load(FIXTURES_V02)
    ids = (
        "KMM-000010",
        "KMM-000012",
        "KMM-000013",
        "KMM-000014",
        "KMM-000015",
    )
    canonical = {mapping_id: _mapping(mapping_id) for mapping_id in ids}
    compiled = compile_fixture_registry_v02(canonical, registry)
    assert tuple(item.mapping_id for item in compiled) == ids
    assert all(item.runtime_authorized is False for item in compiled)
    assert all(item.probability_status == "UNKNOWN" for item in compiled)


def test_freeze_matrix_covers_every_mapping_exactly_once():
    freeze = _load(FREEZE)
    matrix = freeze["mapping_freeze_matrix"]

    assert len(matrix) == 15
    assert len({row["mapping_id"] for row in matrix}) == 15
    assert tuple(row["mapping_id"] for row in matrix) == tuple(
        f"KMM-{index:06d}" for index in range(1, 16)
    )

    allowed_representations = {
        "EXPLICIT_HOLD",
        "LOSSLESS_NONEXECUTABLE",
        "LOSSLESS_PRESERVATION_ONLY",
        "LOSSLESS_STRUCTURED_NONEXECUTABLE",
    }
    assert all(
        row["representation"] in allowed_representations
        for row in matrix
    )


def test_all_pg001_to_pg011_are_closed_for_frozen_corpus():
    freeze = _load(FREEZE)
    gaps = freeze["gap_closure"]

    assert tuple(row["gap_id"] for row in gaps) == tuple(
        f"PG-{index:03d}" for index in range(1, 12)
    )
    assert all(row["status"] == "CLOSED" for row in gaps)
    assert freeze["verdict"]["open_product_gap_count_for_accepted_15"] == 0
    assert freeze["verdict"]["explicit_core_hold_count"] == 3
    assert freeze["verdict"]["formal_crosswalk_freeze_ready"] is True


def test_future_mappings_are_not_auto_admitted_by_freeze():
    freeze = _load(FREEZE)
    contract = freeze["freeze_contract"]

    assert freeze["corpus"]["auto_extend_to_future_mappings"] is False
    assert (
        contract["future_mapping_policy"]
        == "REQUIRES_INCREMENTAL_CROSSWALK_AUDIT_BEFORE_ADMISSION"
    )
    assert contract["generic_free_text_parser_allowed"] is False
    assert contract["keyword_semantic_discovery_allowed"] is False
    assert contract["unsupported_structure_behavior"] == "FAIL_CLOSED"


def test_freeze_is_not_production_or_runtime_authorization():
    freeze = _load(FREEZE)
    for key, value in freeze["production_boundary"].items():
        assert value is False, key

    assert freeze["verdict"]["production_promotion_ready"] is False
    assert freeze["verdict"]["runtime_ready"] is False

    mapping_index = _load(MAPPING_INDEX)
    assert all(row["executable"] is False for row in mapping_index["mappings"])
    assert all(
        row["product_consumable"] is False
        for row in mapping_index["mappings"]
    )
    assert all(
        row["probability_status"] == "UNKNOWN"
        for row in mapping_index["mappings"]
    )

    ontology = _load(ONTOLOGY_REGISTRY)
    mappings = _load(MAPPING_REGISTRY)
    assert ontology["nodes"] == []
    assert mappings["mappings"] == []

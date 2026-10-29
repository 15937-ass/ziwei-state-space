import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "knowledge/core/wp06c/CANONICAL_MANIFESTATION_MAPPING_SCHEMA_v0.1.json"
POLICY = ROOT / "knowledge/core/wp06c/CANONICAL_MANIFESTATION_MAPPING_ID_POLICY_v0.1.json"
INDEX = ROOT / "knowledge/core/wp06c/CANONICAL_MANIFESTATION_MAPPING_INDEX_v0.1.json"
NODE_INDEX = ROOT / "knowledge/core/wp06b/CANONICAL_MANIFESTATION_NODE_INDEX_v0.1.json"
REVIEW_INDEX = ROOT / "knowledge/core/wp06c/CANONICAL_MAPPING_REVIEW_PROVENANCE_INDEX_v0.1.json"
PRODUCT_MAPPING = ROOT / "product/PL3M_MANIFESTATION_MAPPING_REGISTRY_v0.1.json"
PRODUCT_ONTOLOGY = ROOT / "product/PL3M_MANIFESTATION_ONTOLOGY_REGISTRY_v0.1.json"
MAPPING_DIR = ROOT / "knowledge/core/wp06c/canonical_mappings"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def mappings():
    idx = load(INDEX)
    return idx, [load(ROOT / item["path"]) for item in idx["mappings"]]


def test_canonical_mapping_contract_and_ids_are_bounded():
    schema = load(SCHEMA)
    policy = load(POLICY)
    idx, rows = mappings()

    assert schema["properties"]["mapping_id"]["pattern"] == "^KMM-[0-9]{6}$"
    assert policy["lexical_format"] == "KMM-NNNNNN"
    assert policy["semantics_free"] is True
    assert policy["allocation"]["immutable"] is True
    assert policy["allocation"]["reusable_after_supersession"] is False

    assert idx["coverage"]["canonical_mapping_count"] == len(rows)
    assert idx["coverage"]["next_allocatable_id"] == f"KMM-{len(rows) + 1:06d}"
    assert [r["mapping_id"] for r in rows][:3] == ["KMM-000001", "KMM-000002", "KMM-000003"]
    assert len({r["mapping_id"] for r in rows}) == len(rows)
    assert all(re.fullmatch(r"KMM-[0-9]{6}", r["mapping_id"]) for r in rows)

    allowed = set(schema["properties"])
    required = set(schema["required"])
    for row in rows:
        assert required <= set(row)
        assert set(row) <= allowed
        assert row["canonical_mapping_status"] == "ACTIVE"
        assert row["canonical_mapping_approved"] is True
        assert row["probability_status"] == "UNKNOWN"
        assert row["executable"] is False
        assert row["product_consumable"] is False
        assert row["supersession"] == {"supersedes": [], "superseded_by": [], "reason": None}


def test_targets_exist_and_node_index_points_back_to_exactly_one_mapping():
    idx, rows = mappings()
    nodes = load(NODE_INDEX)
    node_by_id = {n["manifestation_id"]: n for n in nodes["nodes"]}

    assert {r["manifestation_id"] for r in rows} >= {"KMN-000001", "KMN-000002", "KMN-000003"}
    assert set(node_by_id) >= {r["manifestation_id"] for r in rows}

    for row in rows:
        node = node_by_id[row["manifestation_id"]]
        assert node["canonical_mapping_approved"] is True
        assert node["canonical_mapping_refs"] == [row["mapping_id"]]
        assert node["executable"] is False
        assert node["product_consumable"] is False
        assert node["probability_status"] == "UNKNOWN"

    assert nodes["invariants"]["canonical_mapping_promotions"] == len(rows)
    assert nodes["invariants"]["executable_mappings"] == 0


def test_review_refs_preserve_positive_and_negative_target_boundaries():
    _, rows = mappings()
    provenance = load(REVIEW_INDEX)
    assert provenance["semantic_authority"] is False
    review = {r["review_record_id"]: r for r in provenance["entries"]}
    assert len(review) == provenance["coverage"]["review_record_count"]

    for row in rows:
        for ref in row["review_refs"]["positive"]:
            assert review[ref]["mapping_disposition"]["value"] == "supported_candidate"
        for ref in row["review_refs"]["negative_boundaries"]:
            assert review[ref]["mapping_disposition"]["value"] == "not_supported_for_target"

    by_id = {r["mapping_id"]: r for r in rows}
    assert by_id["KMM-000001"]["review_refs"] == {
        "positive": ["MR-P09-CA01035-PROCESS-001"],
        "negative_boundaries": ["MR-P09-CA01035-EVENT-NEG-002"],
    }
    assert by_id["KMM-000002"]["review_refs"] == {
        "positive": ["MR-P09-CA01045-CONDITIONAL-001"],
        "negative_boundaries": ["MR-P09-CA01045-UNCONDITIONAL-NEG-002"],
    }
    assert by_id["KMM-000003"]["review_refs"] == {
        "positive": ["MR-P09-CA05469-SCENE-001"],
        "negative_boundaries": ["MR-P09-CA05469-INJURY-NEG-002"],
    }


def test_ca01035_preserves_modality_and_fire_bell_ambiguity():
    row = load(MAPPING_DIR / "KMM-000001.json")
    assert row["primary_source_rule_id"] == "CA01-035"
    assert row["conditions"]["source_condition_text"] == "事业宫见火铃"
    assert row["conditions"]["modality_terms"] == ["往往"]
    assert row["execution_readiness"] == "BLOCKED_SEMANTIC"
    assert row["execution_blockers"] == ["UNRESOLVED_FIRE_BELL_TRIGGER_QUANTIFIER"]
    unresolved = " ".join(row["conditions"]["unresolved_semantics"])
    assert "BOTH_STARS" in unresolved
    assert "EITHER_STAR" in unresolved


def test_ca01045_preserves_inherited_context_and_real_world_action_gate():
    row = load(MAPPING_DIR / "KMM-000002.json")
    assert row["primary_source_rule_id"] == "CA01-045"
    assert row["source_rule_ids"] == ["CA01-042", "CA01-044", "CA01-045"]
    assert row["conditions"]["antecedent_rule_ids"] == ["CA01-042", "CA01-044"]
    assert row["conditions"]["real_world_prerequisites"] == [{
        "text": "勉强求变",
        "status": "SOURCE_EXPLICIT_NOT_ESTABLISHED_BY_CHART",
    }]
    assert row["execution_readiness"] == "BLOCKED_EXTERNAL_PREREQUISITE"
    assert "REAL_WORLD_ACTION_PREREQUISITE_INTERFACE_NOT_ACCEPTED" in row["execution_blockers"]


def test_ca05469_is_scene_only_and_rejects_person_level_medical_event():
    row = load(MAPPING_DIR / "KMM-000003.json")
    assert row["primary_source_rule_id"] == "CA05-469"
    assert row["manifestation_id"] == "KMN-000003"
    assert row["normalization_epistemic"] == "INFERRED"
    assert row["output_kind"]["value"] == "SCENE_OR_CONTEXT"
    assert row["event_specificity"]["value"] == "SCENE_NOT_OBSERVED_EVENT"
    assert row["execution_readiness"] == "KNOWLEDGE_READY_RUNTIME_NOT_AUTHORIZED"
    forbidden = " ".join(row["forbidden_inferences"]).lower()
    for token in ("injury", "illness", "accident", "medical"):
        assert token in forbidden


def test_product_registries_remain_empty_fail_closed():
    mapping = load(PRODUCT_MAPPING)
    ontology = load(PRODUCT_ONTOLOGY)
    assert mapping["registry_status"] == "EMPTY_PENDING_KB_WP06C"
    assert mapping["mappings"] == []
    assert ontology["registry_status"] == "EMPTY_PENDING_KB_WP06B"
    assert ontology["nodes"] == []


def test_no_probability_or_empirical_promotion_and_no_universal_root():
    idx, rows = mappings()
    assert idx["invariants"]["canonical_mapping_promotions"] == len(rows)
    assert idx["invariants"]["executable_mappings"] == 0
    assert idx["invariants"]["product_registry_modified"] is False
    assert idx["invariants"]["product_consumption_authorized"] is False
    assert idx["invariants"]["universal_root_or_family_created"] is False
    assert idx["invariants"]["probability_status"] == "UNKNOWN"
    assert idx["invariants"]["empirical_predictive_validity_claimed"] is False
    assert all(row["probability_status"] == "UNKNOWN" for row in rows)

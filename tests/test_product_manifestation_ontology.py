import json
from pathlib import Path

import pytest

from src.product.manifestation_ontology import (
    compile_manifestation_ontology_bundle,
    require_manifestation_domain,
)

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "product/PL3M_MANIFESTATION_ONTOLOGY_REGISTRY_v0.1.json"


def _ontology():
    return {
        "schema_version": "0.1",
        "ontology_version": "TEST-ONTOLOGY-0.1",
        "nodes": [
            {
                "manifestation_id": "M-ROOT",
                "parent_id": None,
                "domain": "career",
                "abstraction_level": "MANIFESTATION_FAMILY",
                "source_supported_labels": ["career change"],
                "source_rule_ids": ["CA-TEST-001"],
                "event_specificity": "FAMILY",
                "ambiguity_notes": "",
                "probability_status": "UNKNOWN",
            },
            {
                "manifestation_id": "M-JOB",
                "parent_id": "M-ROOT",
                "domain": "career",
                "abstraction_level": "EVENT_LABEL",
                "source_supported_labels": ["job change"],
                "source_rule_ids": ["CA-TEST-001"],
                "event_specificity": "EVENT",
                "ambiguity_notes": "test-only schema fixture",
                "probability_status": "UNKNOWN",
            },
        ],
    }


def _mappings():
    return {
        "schema_version": "0.1",
        "ontology_version": "TEST-ONTOLOGY-0.1",
        "mappings": [
            {
                "mapping_id": "MAP-1",
                "activation_id": "ACT-CAREER-CHANGE",
                "candidate_manifestation_ids": ["M-JOB"],
                "evidence_tier": "EXPLICIT",
                "source_rule_ids": ["CA-TEST-001"],
                "source_trace": ["SRC-TEST:p1"],
                "unresolved_alternatives": [],
            }
        ],
    }


def test_missing_knowledge_artifacts_fail_closed_to_empty_bundle():
    bundle = compile_manifestation_ontology_bundle(None, None)
    assert bundle.status == "EMPTY_KNOWLEDGE_DEPENDENCY"
    assert bundle.nodes == ()
    assert bundle.mappings == ()
    with pytest.raises(ValueError, match="waiting for knowledge"):
        require_manifestation_domain(bundle, "career")


def test_product_registry_explicitly_records_empty_dependency():
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    assert registry["status"] == "EMPTY_KNOWLEDGE_DEPENDENCY"
    assert registry["node_count"] == 0
    assert registry["mapping_count"] == 0


def test_future_wp06b_wp06c_shaped_documents_compile_deterministically():
    first = compile_manifestation_ontology_bundle(_ontology(), _mappings())
    second = compile_manifestation_ontology_bundle(_ontology(), _mappings())
    assert first == second
    assert first.status == "READY"
    assert [x.manifestation_id for x in first.nodes] == ["M-JOB", "M-ROOT"]
    assert first.mappings[0].candidate_manifestation_ids == ("M-JOB",)


def test_unknown_parent_fails_closed():
    ontology = _ontology()
    ontology["nodes"][1]["parent_id"] = "M-NOT-FOUND"
    with pytest.raises(ValueError, match="unknown parent_id"):
        compile_manifestation_ontology_bundle(ontology, _mappings())


def test_mapping_unknown_manifestation_fails_closed():
    mapping = _mappings()
    mapping["mappings"][0]["candidate_manifestation_ids"] = ["M-NOT-FOUND"]
    with pytest.raises(ValueError, match="unknown manifestation"):
        compile_manifestation_ontology_bundle(_ontology(), mapping)


def test_source_backed_mapping_requires_rule_trace():
    mapping = _mappings()
    mapping["mappings"][0]["source_rule_ids"] = []
    with pytest.raises(ValueError, match="requires source_rule_ids"):
        compile_manifestation_ontology_bundle(_ontology(), mapping)


def test_hypothesis_can_exist_without_source_rule_but_stays_tiered():
    mapping = _mappings()
    mapping["mappings"][0]["evidence_tier"] = "HYPOTHESIS"
    mapping["mappings"][0]["source_rule_ids"] = []
    bundle = compile_manifestation_ontology_bundle(_ontology(), mapping)
    assert bundle.mappings[0].evidence_tier == "HYPOTHESIS"


def test_product_adapter_rejects_calibrated_probability_truth_in_wp06b():
    ontology = _ontology()
    ontology["nodes"][0]["probability_status"] = "CALIBRATED"
    with pytest.raises(ValueError, match="cannot accept calibrated probability"):
        compile_manifestation_ontology_bundle(ontology, _mappings())


def test_domain_lookup_fails_when_domain_not_in_ontology():
    bundle = compile_manifestation_ontology_bundle(_ontology(), _mappings())
    with pytest.raises(ValueError, match="no ready domain"):
        require_manifestation_domain(bundle, "relationship")

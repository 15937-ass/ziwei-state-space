from __future__ import annotations

import copy
import json
from pathlib import Path

from tools.knowledge_core_mapping_review_schema import (
    load_mapping_review_schema,
    validate_mapping_review,
    validate_mapping_review_collection,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "knowledge/core/wp06b/fixtures/mapping_review_schema_v0.1_fixtures.json"
KB_SCHEMA = ROOT / "knowledge/KB_SCHEMA.md"
REVIEW_SCHEMA = ROOT / "knowledge/REVIEW_SCHEMA_v0.3.md"


def load_fixture():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_valid_fixture_records_pass_the_typed_contract():
    fixture = load_fixture()
    assert fixture["fixture_status"] == "TEST_ONLY_NON_CANONICAL"
    assert validate_mapping_review_collection(fixture["valid_records"]) == []


def test_invalid_fixture_records_are_rejected():
    fixture = load_fixture()
    for example in fixture["invalid_records"]:
        errors = validate_mapping_review(example["record"])
        assert errors, example["case"]


def test_all_value_states_remain_distinct():
    fixture = load_fixture()
    observed = {row["evidence_role"]["state"] for row in fixture["valid_records"]}
    assert observed == {"KNOWN", "UNKNOWN", "MISSING", "CONFLICT", "NOT_APPLICABLE"}
    schema = load_mapping_review_schema()
    assert schema["$defs"]["review_value_state"]["enum"] == [
        "KNOWN", "UNKNOWN", "MISSING", "CONFLICT", "NOT_APPLICABLE"
    ]


def test_record_ids_are_unique_within_a_collection():
    record = load_fixture()["valid_records"][0]
    errors = validate_mapping_review_collection([record, copy.deepcopy(record)])
    assert any("review_record_id duplicates" in error for error in errors)


def test_machine_schema_is_strict_and_has_exact_candidate_vocabularies():
    schema = load_mapping_review_schema()
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert schema["additionalProperties"] is False
    assert schema["properties"]["schema_version"]["const"] == "0.1"
    assert schema["properties"]["source_refs"]["uniqueItems"] is True
    assert schema["properties"]["target_ref"]["type"] == "string"
    assert schema["properties"]["evidence_role"]["$ref"] == "#/$defs/evidence_role_state"
    assert schema["properties"]["mapping_disposition"]["$ref"] == "#/$defs/mapping_disposition_state"
    assert schema["$defs"]["evidence_role_values"]["enum"] == [
        "direct_state", "state_change", "external_modifier", "interaction",
        "resource_existence", "resource_availability", "realized_support", "projection_outcome",
    ]
    assert schema["$defs"]["mapping_disposition_values"]["enum"] == [
        "candidate_only", "needs_review", "supported_candidate",
        "not_supported_for_target", "superseded",
    ]


def test_mapping_review_does_not_add_canonical_or_option_c_gates():
    schema = load_mapping_review_schema()
    forbidden = {
        "canonical_approval", "consumer_readiness", "output_kind",
        "event_specificity", "source_epistemic", "normalization_epistemic", "review_status",
    }
    assert forbidden.isdisjoint(schema["properties"])


def test_shared_schema_docs_preserve_existing_review_epistemic_contract():
    kb = KB_SCHEMA.read_text(encoding="utf-8")
    review = REVIEW_SCHEMA.read_text(encoding="utf-8")
    assert "Mapping-review envelope v0.1" in kb
    assert "not yet reviewed under this contract" in kb
    assert "provenance, **not an independent-evidence count**" in kb
    assert "canonical approval" in kb.lower()
    assert "Boundary to the mapping-review contract" in review
    for value in (
        "EXPLICIT", "INFERRED_FROM_SOURCE", "UNRESOLVED_SOURCE",
        "SOURCE_PRESERVING", "INFERRED", "IMPLEMENTATION", "HYPOTHESIS", "UNRESOLVED",
        "MODEL_EXTRACTED", "MODEL_SELF_REVIEWED", "SOURCE_SPAN_VERIFIED", "HUMAN_VERIFIED",
    ):
        assert value in review


def test_qi15_qr04_and_source_fidelity_boundaries_are_documented():
    kb = KB_SCHEMA.read_text(encoding="utf-8")
    for phrase in (
        "QI-15", "QR-04", "resource_existence", "resource_availability",
        "realized_support", "source OR into AND", "existing Conflict object",
        "No bulk migration", "Product/runtime",
    ):
        assert phrase.lower() in kb.lower()

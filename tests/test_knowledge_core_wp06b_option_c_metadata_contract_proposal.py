import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROPOSAL = ROOT / "knowledge/core/wp06b/OPTION_C_METADATA_CONTRACT_PROPOSAL_v0.1.json"
ONTOLOGY_REGISTRY = ROOT / "product/PL3M_MANIFESTATION_ONTOLOGY_REGISTRY_v0.1.json"
MAPPING_REGISTRY = ROOT / "product/PL3M_MANIFESTATION_MAPPING_REGISTRY_v0.1.json"
FIXTURE = ROOT / "knowledge/core/wp06b/ONTOLOGY_CAPABILITY_COMPARISON_FIXTURE_v0.1.json"


def data():
    return json.loads(PROPOSAL.read_text(encoding="utf-8"))


def test_proposal_is_candidate_only_and_does_not_freeze_canonical_schema():
    d = data()
    assert d["status"] == "PROPOSAL_ONLY_NOT_CANONICAL"
    assert d["decision_reference"]["selected_option_id"] == "OPTION-C"
    assert d["decision_reference"]["contract_frozen"] is False
    assert d["guardrails"]["direction_approved"] is True
    assert d["guardrails"]["proposal_only"] is True
    assert d["guardrails"]["canonical_root_selected"] is False
    assert d["guardrails"]["accepted_root_id"] is None
    assert d["guardrails"]["accepted_nodes"] == []
    assert d["guardrails"]["ontology_node_ids_assigned"] is False
    assert d["guardrails"]["production_ontology_registry_unchanged"] is True
    assert d["guardrails"]["production_mapping_registry_unchanged"] is True
    assert d["guardrails"]["product_consumption_authorized"] is False
    assert d["guardrails"]["runtime_eligible"] is False
    assert d["guardrails"]["probability_status"] == "UNKNOWN"
    assert d["guardrails"]["empirical_validity_claim"] is False


def test_source_epistemic_reuses_frozen_review_schema_v03_values():
    d = data()
    source_axis = d["axes"]["source_epistemic"]
    assert source_axis["allowed_values"] == [
        "EXPLICIT", "INFERRED_FROM_SOURCE", "UNRESOLVED_SOURCE"
    ]
    assert source_axis["new_values_authorized"] is False
    assert "SOURCE_SPAN_VERIFIED" in source_axis["rules"][4]
    assert "case_support_only" in source_axis["rules"][5]


def test_axes_are_distinct_from_projection_mode_abstraction_and_review():
    d = data()
    axes = d["axes"]
    assert axes["output_kind"]["status"] == "PROPOSAL_ONLY"
    assert axes["event_specificity"]["status"] == "PROPOSAL_ONLY"
    assert axes["source_epistemic"]["status"] == "REUSE_EXISTING_SCHEMA_NO_NEW_ENUM"
    assert "projection_mode" in axes["output_kind"]["forbidden_substitutions"]
    assert "abstraction_level" in axes["output_kind"]["forbidden_substitutions"]
    assert len(d["semantic_separations"]) >= 5
    assert d["axis_status_contract"]["status"] == "PROPOSAL_ONLY"
    assert d["axis_status_contract"]["candidate_status_values"] == [
        "RESOLVED", "UNKNOWN", "MISSING", "CONFLICT", "NOT_APPLICABLE"
    ]


def test_source_examples_preserve_process_action_scene_and_constraint_boundaries():
    d = data()
    rows = {x["source_rule_id"]: x for x in d["examples"]}
    assert rows["CA01-035"]["output_kind"]["value"] == "PROCESS_PATTERN"
    assert rows["CA01-035"]["event_specificity"]["value"] == "PROCESS_SEQUENCE_NOT_SINGLE_EVENT"
    assert "往往" in rows["CA01-035"]["source_anchor"]
    assert rows["CA01-045"]["output_kind"]["value"] == "ACTION_CONDITIONED_OUTCOME"
    assert rows["CA01-045"]["real_world_action_prerequisite"] is True
    assert rows["CA01-045"]["prerequisite_rule_ids"] == ["CA01-042", "CA01-044"]
    assert rows["CA05-469"]["output_kind"]["value"] == "SCENE_OR_CONTEXT"
    assert rows["CA05-469"]["event_specificity"]["value"] == "SCENE_NOT_OBSERVED_EVENT"
    assert rows["M01-006"]["event_specificity"]["status"] == "NOT_APPLICABLE"
    assert rows["W01-002"]["event_specificity"]["status"] == "NOT_APPLICABLE"
    assert rows["CA01-005"]["event_specificity"]["status"] == "NOT_APPLICABLE"


def test_missing_source_epistemic_is_not_auto_promoted_from_span_review():
    d = data()
    rows = {x["source_rule_id"]: x for x in d["examples"]}
    for rule_id in ("M01-006", "W01-002", "CA01-005", "CA09-809"):
        assert rows[rule_id]["source_epistemic"]["status"] == "MISSING"
        assert rows[rule_id]["source_epistemic"]["value"] is None
    assert rows["CA09-809"]["case_support_only"] is True
    assert rows["CA09-809"]["excluded_from_canonical_root_evidence"] is True


def test_synthetic_controls_are_not_source_evidence_and_fail_closed():
    d = data()
    controls = {x["control_type"]: x for x in d["synthetic_controls"]}
    assert set(controls) == {
        "MISSING_PREREQUISITE",
        "CONFLICTING_EVIDENCE",
        "UNKNOWN",
        "LIKELY_MISCLASSIFICATION",
        "CASE_ONLY_PROMOTION",
    }
    assert all(x["source_backed"] is False for x in controls.values())
    assert controls["LIKELY_MISCLASSIFICATION"]["proposed_invalid_mapping"] == "PERSONAL_INJURY_EVENT"
    assert controls["CASE_ONLY_PROMOTION"]["input_record_ref"] == "CA05-493"


def test_production_registries_remain_empty_and_original_fixture_is_not_promoted():
    d = data()
    ontology = json.loads(ONTOLOGY_REGISTRY.read_text(encoding="utf-8"))
    mapping = json.loads(MAPPING_REGISTRY.read_text(encoding="utf-8"))
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert ontology["registry_status"] == "EMPTY_PENDING_KB_WP06B"
    assert ontology["nodes"] == []
    assert mapping["registry_status"] == "EMPTY_PENDING_KB_WP06C"
    assert mapping["mappings"] == []
    assert fixture["status"] == "NON_PRODUCTION_DESIGN_FIXTURE_NOT_CANONICAL"
    assert fixture["guardrails"]["selected_architecture_option"] == "OPTION-C"
    assert fixture["guardrails"]["canonical_root_selected"] is False

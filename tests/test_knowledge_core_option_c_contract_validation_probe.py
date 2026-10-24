from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests/fixtures/knowledge_core/qi_qr_contract_probe/contract_probe_v0.1.json"
REVIEW_SCHEMA = ROOT / "knowledge/REVIEW_SCHEMA_v0.3.md"
KB_SCHEMA = ROOT / "knowledge/KB_SCHEMA.md"
CONTRACT = ROOT / "knowledge/core/wp06b/OPTION_C_METADATA_CONTRACT_PROPOSAL_v0.2.md"
REPORT = ROOT / "knowledge/core/wp06b/OPTION_C_CONTRACT_VALIDATION_PROBE_v0.1.md"


def load_fixture():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_probe_fixture_is_explicitly_synthetic_and_noncanonical():
    data = load_fixture()
    assert data["status"] == "PROBE_ONLY_NOT_CANONICAL"
    assert "not a real source quotation" in data["purpose"]
    assert all(row["probe_source_id"].startswith("PROBE-") for row in data["source_claims"])
    assert all(row["probe_mapping_id"].startswith("PROBE-") for row in data["target_mappings"])
    assert all(row["probe_target_label"].endswith("-PROBE") for row in data["target_mappings"])
    assert "formal ontology ID" in data["purpose"]


def test_existing_schema_fields_support_provenance_and_epistemic_separation():
    review = REVIEW_SCHEMA.read_text(encoding="utf-8")
    kb = KB_SCHEMA.read_text(encoding="utf-8")
    for field in (
        "source_epistemic",
        "normalization_epistemic",
        "review_status",
        "reviewer_type",
        "reviewer_id",
        "reviewed_at",
        "source_span_verified",
        "normalization_verified",
    ):
        assert field in review
    for field in ("target_type", "operator", "condition", "provenance", "normalization_rationale"):
        assert field in kb
    assert "EXPLICIT" in review and "INFERRED_FROM_SOURCE" in review and "UNRESOLVED_SOURCE" in review
    assert "SOURCE_PRESERVING" in review and "HYPOTHESIS" in review and "UNRESOLVED" in review


def test_typed_mapping_disposition_and_evidence_role_are_not_assumed_to_exist():
    review = REVIEW_SCHEMA.read_text(encoding="utf-8")
    kb = KB_SCHEMA.read_text(encoding="utf-8")
    for field in ("mapping_disposition", "evidence_role"):
        pattern = rf"(?<![A-Za-z0-9_]){re.escape(field)}(?![A-Za-z0-9_])"
        assert re.search(pattern, review) is None
        assert re.search(pattern, kb) is None
    report = REPORT.read_text(encoding="utf-8")
    assert "typed-schema gap" in report.lower()
    assert "proposal-only" in report.lower()


def test_each_target_mapping_has_its_own_rationale_and_role_annotation():
    data = load_fixture()
    mappings = data["target_mappings"]
    assert len(mappings) == 2
    assert len({row["probe_target_label"] for row in mappings}) == 2
    assert len({row["normalization_rationale"] for row in mappings}) == 2
    assert all(row["normalization_rationale"].strip() for row in mappings)
    assert all(row["probe_only_evidence_role"].strip() for row in mappings)
    assert {row["probe_source_id"] for row in mappings} == {"PROBE-SRC-001"}
    # Shared source provenance is not counted as independent evidence.
    assert "not independent source evidence" in mappings[1]["normalization_rationale"]


def test_option_c_axes_are_not_repurposed_for_mapping_semantics():
    contract = CONTRACT.read_text(encoding="utf-8")
    data = load_fixture()
    for field in ("output_kind", "event_specificity", "source_epistemic"):
        assert field in contract
    assert "不塞入 Option C 三轴" in contract
    assert "mapping disposition" in data["axis_guardrail"]
    for row in data["target_mappings"]:
        assert "output_kind" not in row
        assert "event_specificity" not in row
        assert "source_epistemic" not in row


def test_qi15_roles_and_qr04_resource_states_remain_distinct():
    data = load_fixture()
    assert set(data["qi15_role_probe"]["required_roles"]) == {"bearer_agent", "target", "condition"}
    assert set(data["qi15_role_probe"]["effect_kinds"]) == {"state_change", "external_modifier", "interaction"}
    assert {row["probe_only_resource_state"] for row in data["qr04_resource_state_probe"]} == {
        "existence", "availability", "realized_support"
    }
    descriptions = [row["description"] for row in data["qr04_resource_state_probe"]]
    assert len(set(descriptions)) == 3


def test_source_alternatives_and_uncertainty_states_are_not_collapsed():
    data = load_fixture()
    claim = data["source_claims"][0]
    assert " OR " in claim["literal_text"]
    assert claim["condition"] == ["alternative A OR alternative B"]
    assert " AND " not in claim["literal_text"]
    states = data["uncertainty_state_probe"]["distinct_states"]
    assert states == ["UNKNOWN", "MISSING", "CONFLICT", "NOT_APPLICABLE"]
    conflict = data["uncertainty_state_probe"]["conflict_object"]
    assert conflict["status"] == "unresolved"
    assert conflict["resolution"] is None
    assert conflict["human_required"] is True


def test_candidate_canonical_and_consumer_gates_are_separate():
    data = load_fixture()
    gates = data["candidate_gate_probe"]
    assert gates["candidate_labels"] == ["QI-17-CAND", "QI-18-CAND"]
    assert gates["probe_only_mapping_disposition"] == "candidate_only"
    assert gates["probe_only_canonical_approval"] == "not_requested"
    assert gates["probe_only_consumer_readiness"] == "not_authorized"
    assert "PROBE-" in data["purpose"]


def test_report_records_capability_matrix_and_no_shared_schema_change():
    report = REPORT.read_text(encoding="utf-8")
    for phrase in (
        "Supported by existing typed fields",
        "Non-canonical review-envelope only",
        "Typed-schema gap",
        "No shared schema file was changed",
        "separate PI/Human Gate",
    ):
        assert phrase in report

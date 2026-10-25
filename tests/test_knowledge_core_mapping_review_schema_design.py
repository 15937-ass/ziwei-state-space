from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "knowledge/core/wp06b/MAPPING_REVIEW_SCHEMA_EXTENSION_DESIGN_v0.1.md"
REVIEW_SCHEMA = ROOT / "knowledge/REVIEW_SCHEMA_v0.3.md"
KB_SCHEMA = ROOT / "knowledge/KB_SCHEMA.md"
EVIDENCE = ROOT / "validation/knowledge/core/wp06b/MAPPING_REVIEW_SCHEMA_EXTENSION_DESIGN_EVIDENCE.md"


def read_design():
    return DESIGN.read_text(encoding="utf-8")


def test_design_is_explicitly_proposal_only_and_not_implementation():
    text = read_design()
    assert "PROPOSAL_ONLY_NOT_IMPLEMENTATION" in text
    assert "does not authorize shared-schema implementation" in text
    assert "All field names, enum values, examples, and shapes below are proposal-only" in text


def test_design_compares_two_shapes_and_recommends_one():
    text = read_design()
    assert "Option A — separate per-target" in text
    assert "Option B — add fields directly" in text
    assert "Recommend **Option A" in text
    assert "Trade-offs" in text


def test_proposed_role_and_disposition_values_are_explicitly_candidate_only():
    text = read_design()
    for role in (
        "direct_state", "state_change", "external_modifier", "interaction",
        "resource_existence", "resource_availability", "realized_support", "projection_outcome",
    ):
        assert f"`{role}`" in text
    for disposition in (
        "candidate_only", "needs_review", "supported_candidate",
        "not_supported_for_target", "superseded",
    ):
        assert f"`{disposition}`" in text
    assert "These are candidate values for PI review, not approved controlled values" in text
    assert "These values describe research/review handling of a candidate, not canonical acceptance" in text


def test_unknown_missing_conflict_and_not_applicable_are_distinct():
    text = read_design()
    for state in ("KNOWN", "UNKNOWN", "MISSING", "CONFLICT", "NOT_APPLICABLE"):
        assert f"`{state}`" in text
    assert "not `MISSING`" in text
    assert "existing Conflict object" in text or "Conflict object" in text


def test_existing_epistemic_review_and_option_c_axes_are_not_repurposed():
    text = read_design()
    for field in ("source_epistemic", "normalization_epistemic", "review_status",
                  "output_kind", "event_specificity", "source_epistemic"):
        assert f"`{field}`" in text
    assert "must not repurpose Option C's" in text
    review = REVIEW_SCHEMA.read_text(encoding="utf-8")
    kb = KB_SCHEMA.read_text(encoding="utf-8")
    assert "EXPLICIT" in review and "UNRESOLVED_SOURCE" in review
    assert "SOURCE_PRESERVING" in review and "HYPOTHESIS" in review
    assert "target_type" in kb and "normalization_rationale" in kb


def test_compatibility_migration_validation_and_rollback_are_covered():
    text = read_design()
    for section in ("## Compatibility", "## Migration", "## Validation and failure behavior", "## Rollback"):
        assert section in text
    assert "No bulk migration is recommended" in text
    assert "fails closed" in text


def test_qi15_qr04_and_source_fidelity_boundaries_are_documented():
    text = read_design()
    for phrase in ("QI-15 role decomposition", "QR-04 resource distinctions",
                   "Source alternatives", "not counted as multiple independent pieces of evidence"):
        assert phrase in text
    assert "never convert source “or” to “and”" in text.lower()


def test_human_gate_decisions_and_write_boundary_are_explicit():
    text = read_design()
    assert "Human Gate decisions required before implementation" in text
    assert "no shared schema, controlled vocabulary, canonical mapping, ontology, or Product/runtime implementation is authorized" in text
    evidence = EVIDENCE.read_text(encoding="utf-8")
    assert "No shared schema file was changed" in evidence
    assert "Exact-head validation" in evidence

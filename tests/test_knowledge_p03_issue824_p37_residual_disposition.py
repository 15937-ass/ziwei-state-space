import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WP05 = ROOT / "knowledge/palaces/P03_spouse/wp05"
DISPOSITION = WP05 / "P03_P37_RESIDUAL_DISPOSITION_ISSUE824_v0.1.json"
PRIOR_FOLLOWUP = WP05 / "P03_SOURCE_ATOM_FOLLOWUP_ISSUE819_v0.1.json"
STATE = ROOT / "knowledge/states/P03_SPOUSE_STATE.yaml"
APPROVED_SOURCE_SHA = "6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_p37_literal_is_visually_verified_without_semantic_normalization():
    d = load(DISPOSITION)
    basis = d["source_basis"]
    residual = d["residual"]

    assert d["issue"] == 824
    assert d["lane"] == "KNOWLEDGE_ONLY"
    assert d["shard"] == "P03"
    assert basis["source_id"] == "SRC-ZZ-003"
    assert basis["approved_pdf_sha256"] == APPROVED_SOURCE_SHA
    assert basis["locally_recomputed_pdf_sha256"] == APPROVED_SOURCE_SHA
    assert basis["verification_method"] == "DIRECT_VISUAL_REVIEW_OF_APPROVED_SOURCE_PDF_RENDER"
    assert basis["printed_page"] == 37
    assert basis["pdf_physical_page"] == 19

    assert residual["gap_id"] == "P03-SP02-GAP-001"
    assert residual["source_span_id"] == "ZZ003-P37-ISSUE824-RESIDUAL-001"
    assert residual["exact_target_literal"] == "机录像"
    assert residual["literal_visual_status"] == "VERIFIED_VISUAL_SCAN"
    assert "第二字符" in residual["literal_visual_note"]
    assert "不是 禄" in residual["literal_visual_note"]
    assert "【机录像】" in residual["source_context_literal"]
    assert "申宫又劣于寅宫" in residual["source_context_literal"]

    assert residual["intended_meaning_status"] == "UNRESOLVED_FAIL_CLOSED"
    assert residual["intended_meaning"] == "UNRESOLVED"
    assert residual["normalized_star_system_name"] is None
    assert residual["gap_closed"] is False
    assert residual["disposition"] == (
        "PARTIALLY_RESOLVED_SOURCE_LITERAL_VERIFIED_INTERPRETATION_AND_TIME_SCOPE_HELD"
    )


def test_p37_time_layer_remains_fail_closed():
    residual = load(DISPOSITION)["residual"]
    assert residual["source_time_expression"] == "经行至"
    assert residual["time_scope_status"] == "UNRESOLVED_FAIL_CLOSED"
    assert residual["assigned_time_layer"] is None
    assert "YEAR" in residual["time_scope_note"]
    assert "DECADE" in residual["time_scope_note"]
    assert "大限" in residual["time_scope_note"]
    assert "流年" in residual["time_scope_note"]


def test_prior_accepted_followup_is_preserved_as_historical_snapshot():
    prior = load(PRIOR_FOLLOWUP)
    residuals = prior["remaining_residuals"]
    assert len(residuals) == 1
    assert residuals[0]["gap_id"] == "P03-SP02-GAP-001"
    assert residuals[0]["source_literal"] == "机录像"
    assert residuals[0]["status"] == "OPEN_SOURCE_LITERAL_AND_TIME_SCOPE_UNRESOLVED"
    assert prior["summary"]["accepted_sp01_sp09_ledgers_modified"] == 0
    assert prior["summary"]["historical_candidate_csvs_modified"] == 0


def test_no_canonical_or_runtime_promotion_and_p03_slot_releases_at_handoff():
    d = load(DISPOSITION)
    boundary = d["execution_boundary"]
    state = STATE.read_text(encoding="utf-8")

    # This state is the post-acceptance handoff snapshot; live Issue/PR governs while open.
    assert 'status: "ACTIVE_NO_ACTIVE_WORK"' in state
    assert "active_issue: null" in state
    assert "active_branch: null" in state
    assert "active_pr: null" in state
    assert "ISSUE824_P37_LITERAL_VERIFIED_MEANING_AND_TIME_SCOPE_HELD_ACCEPTED" in state
    assert "P11 is the next scheduled palace" in state
    assert boundary["history_feedback"] == 0
    assert boundary["conditions_compiled"] == 0
    assert boundary["execution_unlocked"] == 0
    assert boundary["product_runtime_authorized"] is False
    assert boundary["shared_core_semantics_changed"] is False
    assert boundary["other_palace_changed"] is False
    assert boundary["accepted_sp01_sp09_ledgers_modified"] == 0
    assert boundary["historical_candidate_csvs_modified"] == 0
    assert boundary["canonical_rule_rows_added"] == 0
    assert boundary["canonical_promotion_count"] == 0
    assert boundary["new_primitive_qi"] == 0
    assert boundary["new_memory_type"] == 0
    assert boundary["new_independent_time_scale"] == 0
    assert boundary["numeric_weight"] == 0
    assert boundary["probability"] == 0
    assert boundary["decay"] == 0

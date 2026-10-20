from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]


def test_product_v04_roadmap_freezes_core_objects_and_response_layer():
    text = (ROOT / "PRODUCT_ROADMAP.md").read_text(encoding="utf-8")
    assert "Product-First Program v0.4" in text
    for token in ["Kc", "Kr", "Inference policy", "ResponseProfile", "PL3-METHOD", "PL3-R", "PL3-M0"]:
        assert token in text
    assert "A/B/D success != C success" in text


def test_product_v04_has_explicit_now_future_execution_plan():
    text = (
        ROOT / "product" / "phases" / "PRODUCT_VNEXT_EXECUTION_PLAN_v0.1.md"
    ).read_text(encoding="utf-8")
    assert "## 4. NOW" in text
    assert "## 7. FUTURE" in text
    assert "PRODUCT_METHOD_CASE_CONTRACTS_V0_1" in text
    assert "10-fold leave-one-case-out expert replay" in text
    assert "Career NATAL 190 is sufficient for the first vertical slice" in text


def test_product_state_is_recovered_from_closed_416_418():
    text = (ROOT / "product" / "PRODUCT_STATE.yaml").read_text(encoding="utf-8")
    assert 'status: "ACTIVE_NO_ACTIVE_WORK"' in text
    assert "active_issue: null" in text
    assert "active_pr: null" in text
    assert "last_completed_product_issue: 416" in text
    assert "last_completed_product_pr: 418" in text
    assert 'next_work_unit: "PRODUCT_METHOD_CASE_CONTRACTS_V0_1"' in text
    assert "190 accepted NATAL Career rules are on main" in text


def test_product_v04_preserves_epistemic_boundaries():
    text = (ROOT / "product" / "PRODUCT_STATE.yaml").read_text(encoding="utf-8")
    for boundary in [
        "response_profile_separate_from_temporal_environment: true",
        "expert_policy_does_not_own_canonical_truth: true",
        "expert_cases_not_empirical_probability_ground_truth: true",
        "cross_school_method_transfer_does_not_mutate_zhongzhou_core: true",
        "method_fidelity_separate_from_predictive_validity: true",
        "llm_owns_rule_selection: false",
        "llm_owns_probability: false",
    ]:
        assert boundary in text


def test_product_v04_wang_and_cross_school_contracts_are_explicit():
    roadmap = (ROOT / "PRODUCT_ROADMAP.md").read_text(encoding="utf-8")
    assert "Leave-One-Case-Out Expert Replay" in roadmap
    for band in [
        "IDENTICAL",
        "SEMANTIC_EQUIVALENT",
        "PROCEDURAL_COMPATIBLE",
        "SCHOOL_SPECIFIC",
        "CONFLICTING",
        "UNKNOWN",
    ]:
        assert band in roadmap
    assert "不反写中州 core" in roadmap


def test_product_v04_proposal_is_recorded():
    proposal = (
        ROOT
        / "governance"
        / "proposals"
        / "425-product-expert-reasoning-response-architecture.md"
    ).read_text(encoding="utf-8")
    assert "Proposal #425" in proposal
    assert "IMPLEMENTED BY PR #427" in proposal
    assert "Forecast Ledger" in proposal
    assert "Product runtime" in proposal

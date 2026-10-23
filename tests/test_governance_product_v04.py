from pathlib import Path
import re
import json
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


def _assert_product_execution_cache(text: str) -> None:
    """Validate recovery-pointer consistency without freezing a daily task."""
    block = re.search(r"(?ms)^execution:\n(.*?)(?=^\S|\Z)", text)
    assert block is not None, "Product state must have a top-level execution block"
    fields = {}
    for name in ("status", "active_issue", "active_pr"):
        matches = re.findall(rf"^  {name}:\s*([^\n]+)$", block.group(1), re.M)
        assert len(matches) == 1, f"execution.{name} must occur exactly once"
        # These controlled state fields use JSON-compatible YAML scalars.
        fields[name] = json.loads(matches[0])

    status = fields["status"]
    issue = fields["active_issue"]
    pr = fields["active_pr"]
    assert status in ("ACTIVE_NO_ACTIVE_WORK", "ACTIVE"), "unsupported execution status"
    if status == "ACTIVE_NO_ACTIVE_WORK":
        assert issue is None and pr is None, "idle cache cannot retain active pointers"
    else:
        assert type(issue) is int and issue > 0, "active cache needs a positive Issue ID"
        assert pr is None or (type(pr) is int and pr > 0), "PR ID must be positive or null"


def test_product_state_preserves_v04_entry_checkpoint_and_can_advance():
    text = (ROOT / "product" / "PRODUCT_STATE.yaml").read_text(encoding="utf-8")
    _assert_product_execution_cache(text)

    # Proposal #425 entry checkpoint remains durable history, while the
    # last-completed and next-work pointers are allowed to advance normally.
    assert "v04_entry_checkpoint_issue: 416" in text
    assert "v04_entry_checkpoint_pr: 418" in text

    issue_match = re.search(r"last_completed_product_issue:\s*(\d+)", text)
    pr_match = re.search(r"last_completed_product_pr:\s*(\d+)", text)
    next_match = re.search(r'next_work_unit:\s*"([^"]+)"', text)
    assert issue_match and int(issue_match.group(1)) >= 416
    assert pr_match and int(pr_match.group(1)) >= 418
    assert next_match

    next_work_unit = next_match.group(1)
    assert next_work_unit != "PRODUCT_METHOD_CASE_CONTRACTS_V0_1"

    now_block = text.split("critical_path:\n  now:\n", 1)[1].split(
        "  future:\n", 1
    )[0]
    assert f'- "{next_work_unit}"' in now_block
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


def _execution_fixture(status, issue, pr):
    return (
        "execution:\n"
        f"  status: {json.dumps(status)}\n"
        f"  active_issue: {json.dumps(issue)}\n"
        f"  active_pr: {json.dumps(pr)}\n"
    )


def test_product_execution_cache_accepts_consistent_idle_and_active_states():
    for fields in [
        ("ACTIVE_NO_ACTIVE_WORK", None, None),
        ("ACTIVE", 696, None),  # An Issue can be active before a PR exists.
        ("ACTIVE", 696, 698),  # Regression: the real Product #698 snapshot.
    ]:
        _assert_product_execution_cache(_execution_fixture(*fields))


def test_product_execution_cache_rejects_inconsistent_or_invalid_pointers():
    for fields in [
        ("ACTIVE_NO_ACTIVE_WORK", 696, None),
        ("ACTIVE_NO_ACTIVE_WORK", None, 698),
        ("ACTIVE", None, None),
        ("ACTIVE", None, 698),
        ("ACTIVE", 0, 698),
        ("ACTIVE", -1, 698),
        ("ACTIVE", "696", 698),
        ("ACTIVE", True, 698),
        ("ACTIVE", 696, 0),
        ("ACTIVE", 696, -1),
        ("ACTIVE", 696, "698"),
        ("ACTIVE", 696, True),
        ("UNKNOWN", None, None),
    ]:
        try:
            _assert_product_execution_cache(_execution_fixture(*fields))
        except AssertionError:
            continue
        raise AssertionError(f"invalid execution pointers were accepted: {fields!r}")


def test_product_execution_cache_requires_unique_top_level_fields():
    valid = _execution_fixture("ACTIVE", 696, 698)
    for text in [
        valid.replace('  status: "ACTIVE"\n', ""),
        valid + "  active_issue: 697\n",
        valid.replace("  active_pr: 698\n", ""),
        "capability_snapshot:\n  execution:\n    status: \"ACTIVE\"\n",
        valid.replace("  active_issue: 696", "  active_issue: invalid"),
    ]:
        try:
            _assert_product_execution_cache(text)
        except (AssertionError, ValueError):
            continue
        raise AssertionError("malformed execution block was accepted")

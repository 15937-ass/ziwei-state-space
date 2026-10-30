from pathlib import Path
import re

import pytest

ROOT = Path(__file__).resolve().parents[1]


def test_core_product_continuation_plan_is_durable_and_discoverable():
    plan = (ROOT / "governance/CORE_PRODUCT_CONTINUATION_PLAN_v1.md").read_text(encoding="utf-8")
    active_plan = (ROOT / "governance/CORE_PRODUCT_CONTINUATION_PLAN_v2.md").read_text(encoding="utf-8")
    for marker in [
        "Product plan pointer: #900",
        "Core plan pointer: #901",
        "First Product bounded nominee: #897",
        "First Core bounded nominee: #898",
        "15–30",
        "6–10",
        "DIRECT",
        "LOSSY",
        "GAP_PRODUCT",
        "GAP_CORE",
        "HOLD",
        "Integration Lease",
    ]:
        assert marker in plan

    project = (ROOT / "PROJECT_STATE.yaml").read_text(encoding="utf-8")
    assert 'core_product_continuation_plan: "governance/CORE_PRODUCT_CONTINUATION_PLAN_v2.md"' in project
    assert "PI-APPROVED / ACTIVE CONTINUATION PLAN" in active_plan
    assert "NATAL DetailedRead" in active_plan
    assert "DECADE" in active_plan
    assert "YEAR" in active_plan
    assert "SUPERSEDED for active continuation by [v2]" in plan
    assert "product_plan_pointer_issue: 900" in project
    assert "core_plan_pointer_issue: 901" in project


def _product_execution_fields(state: str) -> dict[str, str]:
    """Read only the live execution mapping, not commented historical pointers."""
    lines = state.splitlines()
    assert lines.count("execution:") == 1
    fields: dict[str, str] = {}
    for line in lines[lines.index("execution:") + 1 :]:
        if line and not line.startswith((" ", "\t")):
            break
        match = re.fullmatch(r"  ([a-z][a-z0-9_]*): (.+)", line)
        if match:
            key, value = match.groups()
            assert key not in fields, f"duplicate execution field: {key}"
            fields[key] = value
    return fields


def _assert_product_v2_lifecycle(fields: dict[str, str]) -> None:
    assert fields.get("continuation_plan") == '"governance/CORE_PRODUCT_CONTINUATION_PLAN_v2.md"'
    assert fields.get("plan_pointer_issue") == "900"
    assert fields.get("next_work_unit") == '"PRODUCT_NATAL_DETAILED_READ_CLOSED_LOOP_V1"'
    assert fields.get("continuation_next_work_unit") == '"PRODUCT_NATAL_DETAILED_READ_CLOSED_LOOP_V1"'

    lifecycle = (
        fields.get("status"),
        fields.get("phase"),
        fields.get("next_work_status"),
    )
    if lifecycle == ('"ACTIVE_NO_ACTIVE_WORK"', '"NATAL_DETAILED_READ_NEXT"', '"READY_TO_ADMIT"'):
        assert fields.get("active_issue") == "null"
        assert fields.get("active_pr") == "null"
        assert fields.get("active_branch") in (None, "null")
        assert fields.get("next_issue") == "null"
    elif lifecycle == ('"ACTIVE"', '"NATAL_DETAILED_READ_BUILD"', '"ACTIVE_BUILD"'):
        assert fields.get("active_issue") == "951"
        assert fields.get("active_pr") == "951"
        assert fields.get("active_branch") == '"product/951-natal-detailed-read-closed-loop-v1"'
        assert fields.get("next_issue") == "951"
    else:
        raise AssertionError(f"incoherent Product v2 lifecycle: {lifecycle!r}")


def test_product_state_points_to_first_bounded_nominee():
    state = (ROOT / "product/PRODUCT_STATE.yaml").read_text(encoding="utf-8")
    _assert_product_v2_lifecycle(_product_execution_fields(state))

    # Neither legitimate lifecycle permits a KIB-first detour or silent
    # promotion of the active lock, runtime semantics or Product evidence.
    assert "PRODUCT_KNOWLEDGE_LOCK_V0_3 / KIB-PRODUCT-20261021-V0_3" in state
    assert "PRODUCTION_DYNAMIC_CONTENT_EMPTY" in state
    assert "PRODUCTION_ONTOLOGY_MAPPING_AND_UPSTREAM_DYNAMIC_CONTENT_EMPTY" in state
    assert "knowledge_main_is_implicit_active_product_dependency: false" in state
    assert "knowledge_update_requires_impact_before_product_promotion: true" in state
    assert "llm_owns_probability: false" in state


def test_product_v2_lifecycle_fixtures_accept_only_coherent_states():
    ready = {
        "status": '"ACTIVE_NO_ACTIVE_WORK"',
        "phase": '"NATAL_DETAILED_READ_NEXT"',
        "next_work_status": '"READY_TO_ADMIT"',
        "continuation_plan": '"governance/CORE_PRODUCT_CONTINUATION_PLAN_v2.md"',
        "plan_pointer_issue": "900",
        "next_work_unit": '"PRODUCT_NATAL_DETAILED_READ_CLOSED_LOOP_V1"',
        "continuation_next_work_unit": '"PRODUCT_NATAL_DETAILED_READ_CLOSED_LOOP_V1"',
        "active_issue": "null",
        "active_pr": "null",
        "next_issue": "null",
    }
    active = {
        **ready,
        "status": '"ACTIVE"',
        "phase": '"NATAL_DETAILED_READ_BUILD"',
        "next_work_status": '"ACTIVE_BUILD"',
        "active_issue": "951",
        "active_pr": "951",
        "active_branch": '"product/951-natal-detailed-read-closed-loop-v1"',
        "next_issue": "951",
    }
    _assert_product_v2_lifecycle(ready)
    _assert_product_v2_lifecycle(active)

    invalid = [
        {**ready, "next_work_status": '"ACTIVE_BUILD"'},
        {**ready, "active_issue": "951"},
        {**ready, "active_branch": '"product/951-natal-detailed-read-closed-loop-v1"'},
        {**active, "phase": '"NATAL_DETAILED_READ_NEXT"'},
        {**active, "active_pr": "null"},
        {**active, "active_branch": '"product/other-branch"'},
        {**active, "next_issue": "null"},
        {**active, "status": '"READY_TO_INTEGRATE"'},
        {**active, "next_work_unit": '"PRODUCT_KIB_UPDATE_AFTER_NEXT_ACCEPTED_COMPILER_READY_SOURCE_ARTIFACT"'},
        {**active, "continuation_plan": '"governance/CORE_PRODUCT_CONTINUATION_PLAN_v1.md"'},
    ]
    for fields in invalid:
        with pytest.raises(AssertionError):
            _assert_product_v2_lifecycle(fields)


def test_core_state_recovery_cache_preserves_live_bounded_unit_contract():
    # CORE_STATE is a recovery cache; live Issue/PR overrides stale snapshots.
    # C9 may be ACTIVE while its bounded work is integrating, or the cache may
    # remain IDLE until the owning Core branch merges and Governance repairs it.
    # Never pin this test to historical #898/#880 or to an unmerged v2 plan.
    import re

    state = (ROOT / "knowledge/states/CORE_STATE.yaml").read_text(encoding="utf-8")
    status = re.search(r'^  status: "([^"]+)"$', state, re.M)
    assert status and status.group(1) in {"IDLE", "ACTIVE"}
    assert "plan_pointer_issue: 901" in state
    assert re.search(r"^  last_completed_issue: [0-9]+$", state, re.M)
    assert re.search(r"^  last_completed_pr: [0-9]+$", state, re.M)

    if status.group(1) == "ACTIVE":
        assert re.search(r"^  active_issue: [1-9][0-9]*$", state, re.M)
        assert re.search(r"^  active_pr: [1-9][0-9]*$", state, re.M)
        assert re.search(r'^  active_branch: "[^"]+"$', state, re.M)
    else:
        assert "active_issue: null" in state
        assert "active_pr: null" in state
        assert re.search(r"^  next_issue: (?:null|[0-9]+)$", state, re.M)


def test_three_stream_entry_routes_simple_continue_commands():
    card = (ROOT / "governance/THREE_STREAM_START_HERE.md").read_text(encoding="utf-8")
    assert "Core plan pointer #901" in card
    assert "Product plan pointer #900" in card
    assert "C9 #945/#946 已接受" in card
    assert "PRODUCT_NATAL_DETAILED_READ_CLOSED_LOOP_V1" in card
    assert "DECADE" in card
    assert "YEAR" in card
    assert "无需让我重述顺序" in card

    bootstrap = (ROOT / "CHATGPT_START_HERE.md").read_text(encoding="utf-8")
    assert "CORE_PRODUCT_CONTINUATION_PLAN_v2.md" in bootstrap
    assert "Core plan pointer 为 #901" in bootstrap
    assert "Product plan pointer 为 #900" in bootstrap
    assert "不要求用户重述规划" in bootstrap

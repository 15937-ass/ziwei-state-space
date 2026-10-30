from pathlib import Path

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


def test_product_state_points_to_first_bounded_nominee():
    state = (ROOT / "product/PRODUCT_STATE.yaml").read_text(encoding="utf-8")
    assert 'continuation_plan: "governance/CORE_PRODUCT_CONTINUATION_PLAN_v2.md"' in state
    assert "plan_pointer_issue: 900" in state
    assert 'next_work_unit: "PRODUCT_NATAL_DETAILED_READ_CLOSED_LOOP_V1"' in state
    assert 'continuation_next_work_unit: "PRODUCT_NATAL_DETAILED_READ_CLOSED_LOOP_V1"' in state
    assert "NATAL_DETAILED_READ_NEXT" in state
    assert 'next_work_status: "READY_TO_ADMIT"' in state


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
    assert "当前 C9 #945" in card
    assert "PRODUCT_NATAL_DETAILED_READ_CLOSED_LOOP_V1" in card
    assert "DECADE" in card
    assert "YEAR" in card
    assert "无需让我重述顺序" in card

    bootstrap = (ROOT / "CHATGPT_START_HERE.md").read_text(encoding="utf-8")
    assert "CORE_PRODUCT_CONTINUATION_PLAN_v2.md" in bootstrap
    assert "Core plan pointer 为 #901" in bootstrap
    assert "Product plan pointer 为 #900" in bootstrap
    assert "不要求用户重述规划" in bootstrap

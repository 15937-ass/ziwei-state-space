from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_core_product_continuation_plan_is_durable_and_discoverable():
    plan = (ROOT / "governance/CORE_PRODUCT_CONTINUATION_PLAN_v1.md").read_text(encoding="utf-8")
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
    assert 'core_product_continuation_plan: "governance/CORE_PRODUCT_CONTINUATION_PLAN_v1.md"' in project
    assert "product_plan_pointer_issue: 900" in project
    assert "core_plan_pointer_issue: 901" in project


def test_product_state_points_to_first_bounded_nominee():
    state = (ROOT / "product/PRODUCT_STATE.yaml").read_text(encoding="utf-8")
    assert 'continuation_plan: "governance/CORE_PRODUCT_CONTINUATION_PLAN_v1.md"' in state
    assert "plan_pointer_issue: 900" in state
    assert "next_issue: 897" in state
    assert 'continuation_next_work_unit: "PRODUCT_MANIFESTATION_CROSSWALK_PILOT_V0_1"' in state
    assert 'next_work_status: "READY_TO_ADMIT"' in state


def test_core_state_is_repaired_and_points_to_first_bounded_nominee():
    state = (ROOT / "knowledge/states/CORE_STATE.yaml").read_text(encoding="utf-8")
    assert 'status: "IDLE"' in state
    assert "active_issue: null" in state
    assert "active_pr: null" in state
    assert "plan_pointer_issue: 901" in state
    assert "next_issue: 898" in state
    assert "next_work_unit: null" in state
    assert "last_completed_issue: 880" in state
    assert "last_completed_pr: 881" in state


def test_three_stream_entry_routes_simple_continue_commands():
    card = (ROOT / "governance/THREE_STREAM_START_HERE.md").read_text(encoding="utf-8")
    assert "Core plan pointer #901" in card
    assert "Product plan pointer #900" in card
    assert "当前首单 #898" in card
    assert "当前首单 #897" in card
    assert "无需让我重述顺序" in card

    bootstrap = (ROOT / "CHATGPT_START_HERE.md").read_text(encoding="utf-8")
    assert "CORE_PRODUCT_CONTINUATION_PLAN_v1.md" in bootstrap
    assert "Core plan pointer 为 #901" in bootstrap
    assert "Product plan pointer 为 #900" in bootstrap
    assert "不要求用户重述规划" in bootstrap

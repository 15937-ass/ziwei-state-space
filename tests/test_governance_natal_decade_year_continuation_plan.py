from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def test_v2_is_active_and_preserves_v1_as_history() -> None:
    v2 = _read("governance/CORE_PRODUCT_CONTINUATION_PLAN_v2.md")
    v1 = _read("governance/CORE_PRODUCT_CONTINUATION_PLAN_v1.md")

    assert "PI-APPROVED / ACTIVE CONTINUATION PLAN" in v2
    assert "NATAL DetailedRead" in v2
    assert "DECADE" in v2
    assert "YEAR" in v2
    assert "SUPERSEDED for active continuation by [v2]" in v1


def test_product_state_tracks_ready_or_active_natal_work_without_kib_promotion() -> None:
    import re

    state = _read("product/PRODUCT_STATE.yaml")
    assert 'continuation_plan: "governance/CORE_PRODUCT_CONTINUATION_PLAN_v2.md"' in state
    assert "Active KIB v0.3 / lock remain unchanged" in state
    assert "No KIB promotion" in state

    unit = re.search(r'^  next_work_unit: "([^"]+)"$', state, re.M)
    continuation = re.search(r'^  continuation_next_work_unit: "([^"]+)"$', state, re.M)
    status = re.search(r'^  status: "([^"]+)"$', state, re.M)
    phase = re.search(r'^  phase: "([^"]+)"$', state, re.M)
    work_status = re.search(r'^  next_work_status: "([^"]+)"$', state, re.M)
    active_issue = re.search(r"^  active_issue: (null|[0-9]+)$", state, re.M)
    active_pr = re.search(r"^  active_pr: (null|[0-9]+)$", state, re.M)
    active_branch = re.search(r'^  active_branch: "([^"]+)"$', state, re.M)
    next_issue = re.search(r"^  next_issue: (null|[0-9]+)$", state, re.M)

    assert all((unit, continuation, status, phase, work_status, active_issue, active_pr, next_issue))
    assert continuation.group(1) == unit.group(1)
    stages = {
        "PRODUCT_NATAL_DETAILED_READ_CLOSED_LOOP_V1": ("NATAL_DETAILED_READ_BUILD", "NATAL_DETAILED_READ_NEXT", "951", "product/951-natal-detailed-read-closed-loop-v1"),
        "PRODUCT_NATAL_ACTUAL_USE_VALIDATION_V1": ("NATAL_ACTUAL_USE_VALIDATION", "NATAL_ACTUAL_USE_NEXT", "966", "product/966-natal-actual-use-validation-v1"),
    }
    assert unit.group(1) in stages, "DECADE/YEAR and KIB detours are not admitted"
    active_phase, ready_phase, issue, branch = stages[unit.group(1)]
    if work_status.group(1) == "READY_TO_ADMIT":
        assert status.group(1) == "ACTIVE_NO_ACTIVE_WORK"
        assert phase.group(1) == ready_phase
        assert active_issue.group(1) == "null"
        assert active_pr.group(1) == "null"
        assert next_issue.group(1) == "null"
        assert active_branch is None
    else:
        assert work_status.group(1) == "ACTIVE_BUILD"
        assert status.group(1) == "ACTIVE"
        assert phase.group(1) == active_phase
        assert active_issue.group(1) == issue
        assert active_pr.group(1) == issue
        assert next_issue.group(1) == issue
        assert active_branch and active_branch.group(1) == branch


def test_startup_guides_use_v2_and_describe_natal_decade_year_order() -> None:
    three_stream = _read("governance/THREE_STREAM_START_HERE.md")
    bootstrap = _read("CHATGPT_START_HERE.md")

    for content in (three_stream, bootstrap):
        assert "CORE_PRODUCT_CONTINUATION_PLAN_v2.md" in content
        assert "PRODUCT_NATAL_DETAILED_READ_CLOSED_LOOP_V1" in content
        assert "DECADE" in content
        assert "YEAR" in content


def test_palace_parallelism_is_not_increased_by_this_route() -> None:
    plan = _read("governance/CORE_PRODUCT_CONTINUATION_PLAN_v2.md")
    three_stream = _read("governance/THREE_STREAM_START_HERE.md")

    assert "one-palace-at-a-time" in plan
    assert "not approved" in plan
    assert "一次一个宫位" in three_stream
    assert "不得启用 P06 #773 作为第二槽" in three_stream

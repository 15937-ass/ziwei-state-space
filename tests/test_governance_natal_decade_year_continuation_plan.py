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


def test_product_state_starts_with_natal_detailed_read_without_kib_promotion() -> None:
    state = _read("product/PRODUCT_STATE.yaml")

    assert 'next_work_unit: "PRODUCT_NATAL_DETAILED_READ_CLOSED_LOOP_V1"' in state
    assert 'next_work_status: "READY_TO_ADMIT"' in state
    assert 'continuation_plan: "governance/CORE_PRODUCT_CONTINUATION_PLAN_v2.md"' in state
    assert "Active KIB v0.3 / lock remain unchanged" in state
    assert "No KIB promotion" in state
    assert "The next Product unit is PRODUCT_KIB_UPDATE_AFTER_NEXT_ACCEPTED_COMPILER_READY_SOURCE_ARTIFACT" not in state


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

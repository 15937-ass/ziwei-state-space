from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_active_continuation_plan_is_v2_2_and_keeps_existing_route():
    plan = (ROOT / "governance/CORE_PRODUCT_CONTINUATION_PLAN_v2.md").read_text(encoding="utf-8")
    assert "# Core + Product Continuous Progression Plan v2.2" in plan
    assert "ACTIVE CONTINUATION PLAN v2.2" in plan
    for marker in ("NATAL DetailedRead", "DECADE", "YEAR", "accepted", "Product-consumable"):
        assert marker in plan
    assert "No automatic KIB refresh or promotion" in plan
    assert "No unapproved runtime, probability, causal, predictive-validity" in plan


def test_product_feedback_is_typed_prioritized_and_owned():
    plan = (ROOT / "governance/CORE_PRODUCT_CONTINUATION_PLAN_v2.md").read_text(encoding="utf-8")
    handoff = (ROOT / "governance/CROSS_LANE_HANDOFF_v1.md").read_text(encoding="utf-8")
    for marker in ("KNOWLEDGE_GAP", "CORE_GAP", "PRODUCT_GAP", "HOLD_UNKNOWN"):
        assert marker in plan
        assert marker in handoff
    for marker in ("P0", "P1", "P2", "KNOWLEDGE_CORE_GAP", "second global status ledger"):
        assert marker in plan
        assert marker in handoff


def test_three_stream_limits_and_current_core_product_route_are_preserved():
    plan = (ROOT / "governance/CORE_PRODUCT_CONTINUATION_PLAN_v2.md").read_text(encoding="utf-8")
    card = (ROOT / "governance/THREE_STREAM_START_HERE.md").read_text(encoding="utf-8")
    assert "Core WIP <= 1" in plan
    assert "Product WIP <= 1" in plan
    assert "#676" in plan
    assert "one active palace + one Core + one Product" in plan
    assert "C9 #945/#946 is accepted" in plan
    assert "v0.5 NATAL" in plan
    assert "actual-use validation" in plan
    assert "Product-availability note" in plan
    assert "Tracking Governance Issue: #949 (v2 baseline); v2.2 addendum: #963" in plan
    assert "不得增加宫位槽位" in card
    assert "C9 #945/#946 已接受" in card
    assert "实际命盘" in card
    assert "Product-availability note" in card


def test_natal_to_decade_and_decade_to_year_are_capability_gated():
    plan = (ROOT / "governance/CORE_PRODUCT_CONTINUATION_PLAN_v2.md").read_text(encoding="utf-8")
    assert "NATAL -> DECADE" in plan
    assert "DECADE -> YEAR" in plan
    assert "Complete coverage of every palace" in plan
    assert "not prospective predictive validity" in plan or "does not establish prospective predictive validity" in plan
    assert "If no eligible fixture exists" in plan


def test_bootstrap_and_entry_card_route_to_the_same_v2_2_contract():
    bootstrap = (ROOT / "CHATGPT_START_HERE.md").read_text(encoding="utf-8")
    card = (ROOT / "governance/THREE_STREAM_START_HERE.md").read_text(encoding="utf-8")
    assert "CORE_PRODUCT_CONTINUATION_PLAN_v2.md" in bootstrap
    assert "内容版本 v2.2" in bootstrap
    assert "CORE_GAP" in bootstrap
    assert "三线推进操作卡（v2.2）" in card
    assert "KNOWLEDGE_GAP" in card
    assert "PRODUCT_GAP" in card
    assert "HOLD_UNKNOWN" in card

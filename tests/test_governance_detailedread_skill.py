from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_bootstrap_routes_quickread_and_detailedread_separately():
    bootstrap = (ROOT / "CHATGPT_START_HERE.md").read_text(encoding="utf-8")
    assert ".agents/skills/social_quickread/SKILL.md" in bootstrap
    assert ".agents/skills/social_detailedread/SKILL.md" in bootstrap
    assert "紫微斗数简批" in bootstrap
    assert "详批" in bootstrap
    assert "完整看盘" in bootstrap
    assert "明确的详批意图优先于简批默认长度合同" in bootstrap


def test_quickread_explicitly_hands_full_reading_upgrade_to_detailedread():
    quick = (ROOT / ".agents/skills/social_quickread/SKILL.md").read_text(encoding="utf-8")
    assert "120–220" in quick
    assert ".agents/skills/social_detailedread/SKILL.md" in quick
    assert "Do not keep the QuickRead 120–220-character default" in quick


def test_detailedread_is_thin_read_only_wrapper_over_accepted_product_contract():
    detailed = (ROOT / ".agents/skills/social_detailedread/SKILL.md").read_text(encoding="utf-8")
    assert "not a separate inference engine" in detailed
    assert "product/DETAILED_READ_V0_1.md" in detailed
    assert "src/product/detailed_read.py" in detailed
    assert "full inspection with progressive retrieval" in detailed
    assert "life themes rather than mechanically reciting twelve palaces" in detailed
    assert "Read-only" in detailed
    assert "does not itself start repository implementation" in detailed


def test_detailedread_preserves_epistemic_and_private_chat_boundaries():
    detailed = (ROOT / ".agents/skills/social_detailedread/SKILL.md").read_text(encoding="utf-8")
    assert "Accepted `main` is the source of truth" in detailed
    assert "Full inspection does **not** mean every topic must receive a strong conclusion" in detailed
    assert "Specific DECADE/YEAR claims require matching accepted temporal evidence" in detailed
    assert "Health content is non-diagnostic" in detailed
    assert "case-only material" in detailed
    assert "Hide rule IDs, source paths, coverage/debug metadata" in detailed


def test_ordinary_detailedread_does_not_leak_internal_pi_closeout():
    bootstrap = (ROOT / "CHATGPT_START_HERE.md").read_text(encoding="utf-8")
    workflow = (ROOT / "AGENT_WORKFLOW.md").read_text(encoding="utf-8")
    assert "普通 QuickRead、DetailedRead 或其他命理解读" in bootstrap
    assert "ordinary end-user QuickRead, DetailedRead, or other fortune-reading turn" in workflow
    assert "只要同一轮实际进行了仓库工作，仍必须执行本门槛" in bootstrap
    assert "If repository work occurs anywhere in the same turn, the mandatory closeout applies" in workflow


def test_quickread_and_detailedread_require_canonical_zhongzhou_iztro_chart():
    quick = (ROOT / ".agents/skills/social_quickread/SKILL.md").read_text(encoding="utf-8")
    detailed = (ROOT / ".agents/skills/social_detailedread/SKILL.md").read_text(encoding="utf-8")
    contract = "product/CANONICAL_CHART_CONTRACT_v1.0.md"
    for skill in (quick, detailed):
        assert contract in skill
        assert "iztro-js@2.6.1" in skill
        assert "Never hand-calculate" in skill
        assert "unverified input" in skill

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DECISION = ROOT / "knowledge/core/qi-qr-overlap-audit/QI_QR_OVERLAP_PI_DECISION_PACKAGE_v0.1.md"
CONTRACT = ROOT / "knowledge/core/wp06b/OPTION_C_METADATA_CONTRACT_PROPOSAL_v0.2.md"
AUDIT = ROOT / "knowledge/core/qi-qr-overlap-audit/QI_QR_OVERLAP_PAIR_AUDIT_v0.1.md"
CORE_STATE = ROOT / "knowledge/states/CORE_STATE.yaml"


def test_decision_package_covers_exactly_eight_overlap_pairs():
    text = DECISION.read_text(encoding="utf-8")
    headings = re.findall(r"^### OVERLAP-(\d{2}) — ", text, flags=re.MULTILINE)
    assert headings == [f"{n:02d}" for n in range(1, 9)]


def test_all_proposal_artifacts_are_noncanonical():
    for path in (DECISION, CONTRACT):
        text = path.read_text(encoding="utf-8")
        assert "PROPOSAL_ONLY_NOT_CANONICAL" in text


def test_candidate_pair_is_not_promoted():
    text = DECISION.read_text(encoding="utf-8")
    assert "QI-17-CAND / QI-18-CAND" in text
    assert "不分配正式 ID" in text
    assert "不接受映射" in text


def test_pj_x06_source_condition_gap_remains_unresolved():
    text = DECISION.read_text(encoding="utf-8")
    contract = CONTRACT.read_text(encoding="utf-8")
    assert "ZZ-PJ-X06" in text
    assert "unresolved" in text.lower()
    assert "ZZ-PJ-X06" in contract
    assert "不改写 ZZ-PJ-X06" in text


def test_contract_keeps_option_c_axes_separate_from_qi_qr_mapping_review():
    text = CONTRACT.read_text(encoding="utf-8")
    for term in ("output_kind", "event_specificity", "source_epistemic"):
        assert term in text
    assert "不塞入 Option C 三轴" in text
    assert "UNKNOWN" in text
    assert "MISSING" in text
    assert "CONFLICT" in text
    assert "NOT_APPLICABLE" in text


def test_no_canonical_change_is_authorized_by_this_package():
    text = DECISION.read_text(encoding="utf-8")
    contract = CONTRACT.read_text(encoding="utf-8")
    assert "不修改 canonical ontology" in text
    assert "knowledge/qi_ontology.yaml" in contract
    assert "Product adapter" in contract


def test_core_recovery_cache_matches_active_issue_and_pr():
    text = CORE_STATE.read_text(encoding="utf-8")
    assert 'status: "ACTIVE"' in text
    assert "active_issue: 735" in text
    assert 'active_branch: "knowledge/core-735-qi-qr-pi-decision-package-r2"' in text
    assert "active_pr: 743" in text


def test_original_audit_remains_the_research_source():
    text = AUDIT.read_text(encoding="utf-8")
    assert "PROPOSAL_ONLY_NOT_CANONICAL" in text
    assert "OVERLAP-08" in text


def test_each_pair_records_baseline_source_boundary_and_reconsideration_gate():
    text = DECISION.read_text(encoding="utf-8")
    blocks = re.split(r"(?=^### OVERLAP-\\d{2} — )", text, flags=re.MULTILINE)
    blocks = [block for block in blocks if block.startswith("### OVERLAP-")]
    assert len(blocks) == 8
    for block in blocks:
        assert "当前登记名称/定义（仅记录现状）：" in block
        assert "来源/归一化边界：" in block
        assert "改变决策的条件：" in block

    expected_baselines = (
        "QI-01「发射—收敛」—“气机向外扩散、显发与向内潜藏、收束之间的动力学倾向。”",
        "QI-14「信息/状态遮蔽—显露」—“信息、意图、能力或状态被隐藏、遮蔽，或被显露、可辨识的程度。”",
        "QI-03「稳定—变动」—“系统保持既有结构与发生迁移、转换、重组之间的倾向。”",
        "QI-04「守成—开创/冲刺」—“维护既有结构、资源与秩序，或主动突破既有结构推动新局的倾向。”",
        "QI-02「刚—柔」—“作用方式偏强硬、切断、压制或偏调和、缓冲、顺应的程度。”",
        "QI-15「缓冲/调和能力」—“吸收冲突、降低极端、化解不利或使不同性质趋向平衡的能力。”",
        "QI-08「行动驱动」—“把内部意图转换为主动行动、执行、进取和实际推进的驱动力。”",
        "QI-06「决策激活度」—“从决策延迟到适度审慎，再到过度冲决的激活程度。”",
        "QI-16「目标导向性」—“行动、变化与资源投入具有明确目标、方向与建设性组织的程度。”",
        "QI-17-CAND「意志控制强度」—“在欲望、情绪、诱因或环境压力下维持自主约束与方向的能力。”",
        "QI-18-CAND「毅力/持续性」—“在时间、阻力、延迟或重复挫折下维持行动的持续程度。”",
        "QR-01「关系整合—孤离」—“关系网络中的嵌入、支持、协同程度与孤立、疏离、孤克程度。”",
        "QR-04「支持资源」—“来自辅佐、同伴、属下、组织或贵人网络的可用支持程度。”",
    )
    for baseline in expected_baselines:
        assert baseline in text

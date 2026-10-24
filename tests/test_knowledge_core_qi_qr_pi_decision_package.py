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
    assert "不修改 knowledge/qi_ontology.yaml" in contract
    assert "不修改 Product adapter" in contract


def test_core_recovery_cache_matches_active_issue_and_pr():
    text = CORE_STATE.read_text(encoding="utf-8")
    assert 'status: "ACTIVE"' in text
    assert "active_issue: 735" in text
    assert 'active_branch: "knowledge/core-735-qi-qr-pi-decision-package"' in text
    assert "active_pr: 736" in text


def test_original_audit_remains_the_research_source():
    text = AUDIT.read_text(encoding="utf-8")
    assert "PROPOSAL_ONLY_NOT_CANONICAL" in text
    assert "OVERLAP-08" in text

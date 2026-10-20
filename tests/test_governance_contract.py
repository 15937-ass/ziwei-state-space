from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def test_governance_artifacts_exist():
    required = [
        "GOVERNANCE.md",
        "governance/PROPOSAL_PROCESS.md",
        "governance/PROPOSAL_TEMPLATE.md",
        "governance/PATH_OWNERSHIP.json",
        "PROJECT_STATE.yaml",
        "product/PRODUCT_STATE.yaml",
        "knowledge/KNOWLEDGE_STATE.yaml",
        "governance/GOVERNANCE_STATE.yaml",
    ]
    assert all((ROOT / p).exists() for p in required)


def test_path_ownership_has_three_lanes():
    data = json.loads(
        (ROOT / "governance/PATH_OWNERSHIP.json").read_text(encoding="utf-8")
    )
    assert set(data["allowed_paths"]) == {
        "PRODUCT_ONLY",
        "KNOWLEDGE_ONLY",
        "GOVERNANCE_ONLY",
    }


def test_project_state_is_bootstrap_not_history():
    text = (ROOT / "PROJECT_STATE.yaml").read_text(encoding="utf-8")
    assert 'execution_truth: "GITHUB_ISSUES"' in text
    assert "\n  completed:" not in text


def test_conversation_mode_has_full_connector_exposed_repository_authority():
    protocol = (
        ROOT / "governance/PUBLIC_ACTIONS_EXECUTION_PROTOCOL_v0.2.md"
    ).read_text(encoding="utf-8")
    assert "first-class repository operator" in protocol
    assert "every GitHub repository operation actually exposed by the connected tools" in protocol
    assert "operational-capability grant, not a semantic-governance bypass" in protocol
    assert "technical ceiling" in protocol


def test_g7_is_historical_after_g8_g9():
    g7 = (
        ROOT / "governance/WORK_CODEX_EXECUTION_PROTOCOL_v0.1.md"
    ).read_text(encoding="utf-8")
    assert "HISTORICAL" in g7
    assert "G9 / Issue #374" in g7


def test_full_repository_capability_does_not_remove_normal_pr_discipline():
    workflow = (ROOT / "AGENT_WORKFLOW.md").read_text(encoding="utf-8")
    assert "first-class repository operator" in workflow
    assert "Issue -> branch -> PR -> validation -> merge" in workflow
    assert "direct-to-main is not routine" in workflow

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


def test_recovery_precedence_is_explicit_and_pointer_driven():
    project = (ROOT / "PROJECT_STATE.yaml").read_text(encoding="utf-8")
    recovery = (ROOT / "governance/RECOVERY_PRECEDENCE_v1.md").read_text(encoding="utf-8")
    assert 'current_execution_protocol: "governance/PUBLIC_ACTIONS_EXECUTION_PROTOCOL_v0.2.md"' in project
    assert 'recovery_precedence: "governance/RECOVERY_PRECEDENCE_v1.md"' in project
    assert "live GitHub Issue" in recovery
    assert "legacy `tasks/*.yaml`" in recovery
    assert "README “Current phase”" in recovery
    assert "historical `READY_FOR_PI`" in recovery
    assert "G7 protocol" in recovery


def test_g7_is_quarantined_and_g8_is_current():
    g7 = (ROOT / "governance/WORK_CODEX_EXECUTION_PROTOCOL_v0.1.md").read_text(encoding="utf-8")
    g8 = (ROOT / "governance/PUBLIC_ACTIONS_EXECUTION_PROTOCOL_v0.2.md").read_text(encoding="utf-8")
    assert "HISTORICAL / SUPERSEDED" in g7
    assert "DO NOT USE FOR CURRENT RECOVERY" in g7
    assert "Historical GitHub Actions policy — DO NOT APPLY" in g7
    assert "ACTIVE — G8 EXECUTION POLICY" in g8
    assert "automatic `pull_request` triggers are allowed" in g8 or "`pull_request` triggers targeting `main`" in g8


def test_conversation_mode_has_full_connector_exposed_repository_authority():
    protocol = (ROOT / "governance/PUBLIC_ACTIONS_EXECUTION_PROTOCOL_v0.2.md").read_text(encoding="utf-8")
    workflow = (ROOT / "AGENT_WORKFLOW.md").read_text(encoding="utf-8")
    assert "first-class repository operator" in protocol
    assert "every GitHub repository operation actually exposed" in protocol
    assert "first-class repository operator" in workflow
    assert "direct-to-main is not routine" in workflow


def test_governance_and_plans_do_not_masquerade_as_live_task_queue():
    gov = (ROOT / "GOVERNANCE.md").read_text(encoding="utf-8")
    decisions = (ROOT / "DECISION_LOG.md").read_text(encoding="utf-8")
    knowledge = (ROOT / "KNOWLEDGE_BASE_ROADMAP.md").read_text(encoding="utf-8")
    product = (ROOT / "PRODUCT_ROADMAP.md").read_text(encoding="utf-8")
    plan = (ROOT / "product/phases/PRODUCT_VNEXT_EXECUTION_PLAN_v0.1.md").read_text(encoding="utf-8")
    assert "Status: **ACTIVE**" in gov
    assert "not an execution queue" in decisions
    assert "not an execution queue" in knowledge
    assert "roadmap status is not execution truth" in product
    assert "RECOVERY WARNING" in plan


def test_g9_proposal_exists_and_preserves_normal_pr_discipline():
    proposal = (ROOT / "governance/proposals/374-chat-repository-authority.md").read_text(encoding="utf-8")
    assert "APPROVED / IMPLEMENTING" in proposal
    assert "Issue -> branch -> PR -> validation -> merge" in proposal
    assert "no Zhongzhou canonical semantic changes" in proposal

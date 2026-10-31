from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def test_governance_artifacts_exist():
    required = [
        "GOVERNANCE.md",
        "governance/PROPOSAL_PROCESS.md",
        "governance/PROPOSAL_TEMPLATE.md",
        "governance/PATH_OWNERSHIP.json",
        "governance/KNOWLEDGE_SHARD_EXECUTION_v1.md",
        "governance/KNOWLEDGE_SHARDS.json",
        "PROJECT_STATE.yaml",
        "CHATGPT_START_HERE.md",
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



def test_canonical_chatgpt_bootstrap_prevents_actions_policy_regression():
    bootstrap = (ROOT / "CHATGPT_START_HERE.md").read_text(encoding="utf-8")
    project = (ROOT / "PROJECT_STATE.yaml").read_text(encoding="utf-8")
    workflow = (ROOT / "AGENT_WORKFLOW.md").read_text(encoding="utf-8")
    recovery = (ROOT / "governance/RECOVERY_PRECEDENCE_v1.md").read_text(encoding="utf-8")
    assert "唯一推荐的 ChatGPT 新对话启动指令" in bootstrap
    assert "pull_request" in bootstrap
    assert "workflow_dispatch" in bootstrap
    assert "禁止自动" in bootstrap and "push" in bootstrap
    assert "禁用 GitHub Actions" in bootstrap
    assert "G7 期间的限制描述为当前禁令" in bootstrap
    assert "discard that instruction" in workflow
    assert "blanket Actions disablement" in recovery
    assert "session_bootstrap" in project
    assert "chat_is_project_state_authority: false" in project
    assert "chat_is_repository_operator: true" in project
    assert "chat_is_authoritative:" not in project


def test_pi_first_closeout_is_compact_not_a_global_gate():
    bootstrap = (ROOT / "CHATGPT_START_HERE.md").read_text(encoding="utf-8")
    workflow = (ROOT / "AGENT_WORKFLOW.md").read_text(encoding="utf-8")
    contract = (ROOT / "governance/PI_DECISION_AND_SUBSTANTIVE_PROGRESS_v1.md").read_text(encoding="utf-8")
    assert "PI_CLOSEOUT_FINAL_GATE_REQUIRED" not in bootstrap
    assert "PI_CLOSEOUT_FINAL_GATE_REQUIRED" not in workflow
    assert "不得发送仓库工作对话的最终答复" not in bootstrap
    assert "ordinary end-user QuickRead" in workflow
    assert "普通 QuickRead、DetailedRead 或其他命理解读" in bootstrap
    assert "不要求六区块固定汇报" in bootstrap
    assert "global three-stream census" in contract
    assert "optional" in contract


def test_g7_is_quarantined_and_g8_is_current():
    g7 = (ROOT / "governance/archive/WORK_CODEX_EXECUTION_PROTOCOL_v0.1_G7_HISTORICAL.md").read_text(encoding="utf-8")
    g8 = (ROOT / "governance/PUBLIC_ACTIONS_EXECUTION_PROTOCOL_v0.2.md").read_text(encoding="utf-8")
    assert not (ROOT / "governance/WORK_CODEX_EXECUTION_PROTOCOL_v0.1.md").exists()
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
    assert "IMPLEMENTED BY PR #496" in proposal
    assert "Issue -> branch -> PR -> validation -> merge" in proposal
    assert "no Zhongzhou canonical semantic changes" in proposal


def test_knowledge_shard_contract_is_active():
    registry = json.loads(
        (ROOT / "governance/KNOWLEDGE_SHARDS.json").read_text(encoding="utf-8")
    )
    coordinator = (ROOT / "knowledge/KNOWLEDGE_STATE.yaml").read_text(encoding="utf-8")
    assert registry["limits"]["core_wip"] == 1
    assert registry["limits"]["total_palace_wip"] == 4
    assert registry["limits"]["per_palace_wip"] == 1
    assert set(registry["palaces"]) == {f"P{i:02d}" for i in range(1, 13)}
    assert 'mode: "PALACE_SHARDED_V1"' in coordinator


def test_pi_decision_and_substantive_progress_contract_is_wired_into_workflow():
    contract = (ROOT / "governance/PI_DECISION_AND_SUBSTANTIVE_PROGRESS_v1.md").read_text(encoding="utf-8")
    workflow = (ROOT / "AGENT_WORKFLOW.md").read_text(encoding="utf-8")
    bootstrap = (ROOT / "CHATGPT_START_HERE.md").read_text(encoding="utf-8")
    assert "PI-reserved decisions" in contract
    assert "Autonomous execution within approved scope" in contract
    assert "PI_DECISION_AND_SUBSTANTIVE_PROGRESS_v1.md" in workflow
    assert "PI_DECISION_AND_SUBSTANTIVE_PROGRESS_v1.md" in bootstrap
    assert "当前对话中 PI 明确提出的最新指令" in bootstrap
    assert "one primary outcome class" in workflow
    assert "current explicit PI instruction" in workflow
    assert "The PI reserves research mission/priority/resource/WIP decisions" in workflow


def test_every_repository_work_turn_has_one_truthful_primary_outcome_class():
    contract = (ROOT / "governance/PI_DECISION_AND_SUBSTANTIVE_PROGRESS_v1.md").read_text(encoding="utf-8")
    for outcome in (
        "SUBSTANTIVE_DELTA",
        "BLOCKER_IDENTIFIED",
        "VALIDATION_ONLY",
        "STATUS_ONLY",
        "NO_SUBSTANTIVE_PROGRESS",
    ):
        assert outcome in contract
    assert "not mandatory for every turn" in contract
    assert "Validation is a quality gate, not research progress." in contract
    assert "NO_SUBSTANTIVE_PROGRESS" in contract


def test_anti_ceremony_rules_exclude_administrative_activity_as_progress():
    contract = (ROOT / "governance/PI_DECISION_AND_SUBSTANTIVE_PROGRESS_v1.md").read_text(encoding="utf-8")
    for marker in (
        "commit count",
        "lines changed",
        "Issue/PR state transitions",
        "repeated reads",
        "newly created scaffolding",
        "unchanged test reruns",
    ):
        assert marker in contract
    assert "No single numeric KPI replaces evidence-based acceptance." in contract


def test_line_specific_progress_criteria_preserve_epistemic_maturity():
    contract = (ROOT / "governance/PI_DECISION_AND_SUBSTANTIVE_PROGRESS_v1.md").read_text(encoding="utf-8")
    for lane in ("Knowledge", "Core", "Product", "Governance"):
        assert f"### {lane}" in contract
    for maturity in (
        "source fidelity",
        "formal/specification consistency",
        "implementation correctness",
        "internal validation",
        "empirical calibration",
        "causal identification",
        "predictive validity",
        "production readiness",
    ):
        assert maturity in contract


def test_closeout_contract_is_task_scoped_and_lightweight():
    contract = (ROOT / "governance/PI_DECISION_AND_SUBSTANTIVE_PROGRESS_v1.md").read_text(encoding="utf-8")
    workflow = (ROOT / "AGENT_WORKFLOW.md").read_text(encoding="utf-8")
    bootstrap = (ROOT / "CHATGPT_START_HERE.md").read_text(encoding="utf-8")
    assert "six-section report are optional" in contract
    assert "no mandatory six-section report" in workflow
    assert "global three-stream census is optional" in workflow
    assert "Result" in workflow
    assert "Changed artifacts" in workflow
    assert "Validation actually performed" in workflow
    assert "do not create a second status ledger" in contract
    assert "current explicit PI instruction" in bootstrap

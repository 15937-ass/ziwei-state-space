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

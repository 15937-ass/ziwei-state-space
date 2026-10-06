"""Repository Governance v1 deterministic validator."""
from __future__ import annotations

import argparse
import fnmatch
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "GOVERNANCE.md",
    "governance/PROPOSAL_PROCESS.md",
    "governance/PROPOSAL_TEMPLATE.md",
    "governance/PATH_OWNERSHIP.json",
    "governance/CAPABILITY_READINESS_SCHEMA.md",
    "PROJECT_STATE.yaml",
    "product/PRODUCT_STATE.yaml",
    "knowledge/KNOWLEDGE_STATE.yaml",
    "governance/GOVERNANCE_STATE.yaml",
    ".github/PULL_REQUEST_TEMPLATE.md",
]

PROPOSAL_HEADINGS = [
    "## Motivation",
    "## Goals",
    "## Non-Goals",
    "## Proposed Design",
    "## Risks and Failure Modes",
    "## Test Plan",
    "## Migration Plan",
    "## Rollback Plan",
    "## Graduation Criteria",
    "## Human Gate",
    "## Decision",
]


def fail(msg: str) -> None:
    print(f"GOVERNANCE_ERROR: {msg}", file=sys.stderr)
    raise SystemExit(1)


def load_contract() -> dict:
    return json.loads((ROOT / "governance/PATH_OWNERSHIP.json").read_text(encoding="utf-8"))


def path_matches(path: str, pattern: str) -> bool:
    if pattern.endswith("/**"):
        return path.startswith(pattern[:-3])
    return fnmatch.fnmatch(path, pattern)


def changed_paths(base_ref: str) -> list[str]:
    proc = subprocess.run(
        ["git", "diff", "--name-only", f"{base_ref}...HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def validate_required() -> None:
    missing = [p for p in REQUIRED if not (ROOT / p).exists()]
    if missing:
        fail("missing required governance artifacts: " + ", ".join(missing))

    project_state = (ROOT / "PROJECT_STATE.yaml").read_text(encoding="utf-8")
    if 'execution_truth: "GITHUB_ISSUES"' not in project_state:
        fail("PROJECT_STATE must declare GitHub Issues as execution truth")
    if "\n  completed:" in project_state or "\ncompleted:" in project_state:
        fail("PROJECT_STATE must not duplicate completed-history lists")

    for rel in [
        "product/PRODUCT_STATE.yaml",
        "knowledge/KNOWLEDGE_STATE.yaml",
        "governance/GOVERNANCE_STATE.yaml",
    ]:
        text = (ROOT / rel).read_text(encoding="utf-8")
        if 'authoritative_execution: "GITHUB_ISSUE"' not in text:
            fail(f"{rel} must declare GITHUB_ISSUE execution authority")


def validate_proposals() -> None:
    folder = ROOT / "governance/proposals"
    if not folder.exists():
        return
    for path in folder.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        missing = [h for h in PROPOSAL_HEADINGS if h not in text]
        if missing:
            fail(f"{path.relative_to(ROOT)} missing proposal sections: {missing}")


def lane_from_branch(branch: str, contract: dict) -> str | None:
    for prefix, lane in contract["branch_prefixes"].items():
        if branch.startswith(prefix):
            return lane
    return None


def validate_lane_paths(branch: str, base_ref: str) -> None:
    contract = load_contract()
    lane = lane_from_branch(branch, contract)
    if not lane:
        fail(
            f"branch '{branch}' does not use an approved lane prefix "
            "(product/, knowledge/, governance/)"
        )
    allowed = contract["allowed_paths"][lane]
    bad = [
        path
        for path in changed_paths(base_ref)
        if not any(path_matches(path, pat) for pat in allowed)
    ]
    if bad:
        fail(f"{lane} branch modifies paths outside ownership: {bad}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-ref")
    parser.add_argument("--head-branch", default=os.environ.get("GITHUB_HEAD_REF", ""))
    parser.add_argument("--allow-main", action="store_true")
    args = parser.parse_args()

    validate_required()
    validate_proposals()

    if args.allow_main:
        print("Governance static validation passed (main/push mode).")
        return

    if not args.base_ref or not args.head_branch:
        fail("PR mode requires --base-ref and --head-branch")

    validate_lane_paths(args.head_branch, args.base_ref)
    print(f"Governance validation passed for {args.head_branch}.")


if __name__ == "__main__":
    main()

"""Repository Governance v1 deterministic validator."""
from __future__ import annotations

import argparse
import fnmatch
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "GOVERNANCE.md",
    "governance/PROPOSAL_PROCESS.md",
    "governance/PROPOSAL_TEMPLATE.md",
    "governance/PATH_OWNERSHIP.json",
    "governance/CAPABILITY_READINESS_SCHEMA.md",
    "governance/KNOWLEDGE_SHARD_EXECUTION_v1.md",
    "governance/INTEGRATION_QUEUE_PROTOCOL_v1.md",
    "governance/CORE_PRODUCT_CONTINUATION_PLAN_v1.md",
    "governance/CORE_PRODUCT_CONTINUATION_PLAN_v2.md",
    "governance/KNOWLEDGE_SHARDS.json",
    "PROJECT_STATE.yaml",
    "product/PRODUCT_STATE.yaml",
    "knowledge/KNOWLEDGE_STATE.yaml",
    "knowledge/states/CORE_STATE.yaml",
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


def load_knowledge_shards() -> dict:
    return json.loads((ROOT / "governance/KNOWLEDGE_SHARDS.json").read_text(encoding="utf-8"))


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


def classify_knowledge_branch(branch: str, shard_contract: dict) -> tuple[str, str | None]:
    grandfather = shard_contract.get("grandfather_branches", {})
    if branch in grandfather:
        return "GRANDFATHER", grandfather[branch]

    core_pattern = shard_contract["branch_patterns"]["core"]
    if re.fullmatch(core_pattern, branch):
        return "CORE", None

    palace_pattern = shard_contract["branch_patterns"]["palace"]
    match = re.fullmatch(palace_pattern, branch)
    if match:
        shard = match.group(1).upper()
        if shard not in shard_contract["palaces"]:
            raise ValueError(f"unknown Knowledge palace shard {shard}")
        return "PALACE", shard

    raise ValueError(
        "Knowledge branch must use knowledge/core-<issue>-<slug> or "
        "knowledge/pXX-<issue>-<slug>; only declared grandfather branches are exempt"
    )


def knowledge_shard_bad_paths(
    branch: str,
    paths: list[str],
    lane_contract: dict,
    shard_contract: dict,
) -> list[str]:
    kind, shard = classify_knowledge_branch(branch, shard_contract)

    if kind == "GRANDFATHER":
        allowed = lane_contract["allowed_paths"]["KNOWLEDGE_ONLY"]
    elif kind == "CORE":
        allowed = shard_contract["core"]["allowed_paths"]
    else:
        allowed = shard_contract["palaces"][shard]["allowed_paths"]

    return [
        path
        for path in paths
        if not any(path_matches(path, pattern) for pattern in allowed)
    ]


def validate_knowledge_shard_registry() -> None:
    data = load_knowledge_shards()
    expected = {f"P{i:02d}" for i in range(1, 13)}
    actual = set(data.get("palaces", {}))
    if actual != expected:
        fail(f"Knowledge shard registry must contain P01..P12 exactly; got {sorted(actual)}")

    limits = data.get("limits", {})
    if limits.get("core_wip") != 1:
        fail("Knowledge Core WIP must remain 1")
    if limits.get("total_palace_wip") != 4:
        fail("Knowledge palace WIP cap must remain 4 unless a new Governance decision changes it")
    if limits.get("per_palace_wip") != 1:
        fail("Knowledge per-palace WIP must remain 1")
    if limits.get("canonical_merge") != "SERIAL_EXACT_HEAD":
        fail("Knowledge canonical merge policy must be SERIAL_EXACT_HEAD")

    state_paths = [data["core"]["state"]]
    for shard, record in data["palaces"].items():
        state = record.get("state")
        if not state:
            fail(f"{shard} is missing a state path")
        state_paths.append(state)

    if len(set(state_paths)) != 13:
        fail("Knowledge Core + 12 palace state paths must be unique")

    missing = [p for p in state_paths if not (ROOT / p).exists()]
    if missing:
        fail("missing Knowledge shard states: " + ", ".join(missing))


def validate_required() -> None:
    missing = [p for p in REQUIRED if not (ROOT / p).exists()]
    if missing:
        fail("missing required governance artifacts: " + ", ".join(missing))

    project_state = (ROOT / "PROJECT_STATE.yaml").read_text(encoding="utf-8")
    if 'execution_truth: "GITHUB_ISSUES"' not in project_state:
        fail("PROJECT_STATE must declare GitHub Issues as execution truth")
    if "\n  completed:" in project_state or "\ncompleted:" in project_state:
        fail("PROJECT_STATE must not duplicate completed-history lists")
    if 'integration_protocol: "governance/INTEGRATION_QUEUE_PROTOCOL_v1.md"' not in project_state:
        fail("PROJECT_STATE must point to the integration queue protocol")
    if "integration_ledger_issue: 888" not in project_state:
        fail("PROJECT_STATE must point to coordination Issue #888")
    if 'core_product_continuation_plan: "governance/CORE_PRODUCT_CONTINUATION_PLAN_v2.md"' not in project_state:
        fail("PROJECT_STATE must point to the active Core/Product continuation plan v2")
    if "product_plan_pointer_issue: 900" not in project_state:
        fail("PROJECT_STATE must point to Product plan pointer #900")
    if "core_plan_pointer_issue: 901" not in project_state:
        fail("PROJECT_STATE must point to Core plan pointer #901")

    historical = (ROOT / "governance/CORE_PRODUCT_CONTINUATION_PLAN_v1.md").read_text(encoding="utf-8")
    for marker in [
        "Issue #900",
        "Issue #901",
        "Issue #897",
        "Issue #898",
        "15–30",
        "DIRECT",
        "LOSSY",
        "GAP_PRODUCT",
        "GAP_CORE",
        "HOLD",
        "SUPERSEDED for active continuation by [v2]",
    ]:
        if marker not in historical:
            fail(f"Historical Core/Product v1 continuation plan missing marker: {marker}")

    active = (ROOT / "governance/CORE_PRODUCT_CONTINUATION_PLAN_v2.md").read_text(encoding="utf-8")
    for marker in [
        "PI-APPROVED / ACTIVE CONTINUATION PLAN",
        "Product plan pointer: #900",
        "Core plan pointer: #901",
        "NATAL DetailedRead",
        "PRODUCT_NATAL_DETAILED_READ_CLOSED_LOOP_V1",
        "DECADE",
        "YEAR",
        "one-palace-at-a-time",
        "Integration Lease",
        "HOLD",
    ]:
        if marker not in active:
            fail(f"Active Core/Product v2 continuation plan missing marker: {marker}")

    integration = (ROOT / "governance/INTEGRATION_QUEUE_PROTOCOL_v1.md").read_text(encoding="utf-8")
    for marker in [
        "ACTIVE_BUILD",
        "READY_TO_INTEGRATE",
        "INTEGRATING",
        "Integration Lease",
        "Issue #888",
        "exact-head",
    ]:
        if marker not in integration:
            fail(f"integration queue protocol missing required marker: {marker}")

    for rel in [
        "product/PRODUCT_STATE.yaml",
        "knowledge/KNOWLEDGE_STATE.yaml",
        "governance/GOVERNANCE_STATE.yaml",
    ]:
        text = (ROOT / rel).read_text(encoding="utf-8")
        if 'authoritative_execution: "GITHUB_ISSUE"' not in text:
            fail(f"{rel} must declare GITHUB_ISSUE execution authority")

    knowledge = (ROOT / "knowledge/KNOWLEDGE_STATE.yaml").read_text(encoding="utf-8")
    if 'mode: "PALACE_SHARDED_V1"' not in knowledge:
        fail("Knowledge coordinator must declare PALACE_SHARDED_V1")

    validate_knowledge_shard_registry()


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

    paths = changed_paths(base_ref)
    if lane == "KNOWLEDGE_ONLY":
        try:
            bad = knowledge_shard_bad_paths(
                branch, paths, contract, load_knowledge_shards()
            )
        except ValueError as exc:
            fail(str(exc))
    else:
        allowed = contract["allowed_paths"][lane]
        bad = [
            path
            for path in paths
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

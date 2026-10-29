# Public Actions Execution Protocol v0.2

Status: **ACTIVE — G8 EXECUTION POLICY, G9 REPOSITORY-AUTHORITY AMENDMENT**  
Tracking Issues: #372 (G8), #374 (G9)  
Supersedes for routine execution: `governance/archive/WORK_CODEX_EXECUTION_PROTOCOL_v0.1_G7_HISTORICAL.md`  
Recovery precedence: `governance/RECOVERY_PRECEDENCE_v1.md`  
Final integration: `governance/INTEGRATION_QUEUE_PROTOCOL_v1.md` / coordination Issue #888

## 1. Purpose

This protocol lets the project continue when ChatGPT Work/Codex quota is unavailable by using GitHub Actions as the deterministic repository execution runtime.

The repository is public. G8 authorizes only standard GitHub-hosted runners. Larger or otherwise billable runners are not authorized by this protocol.

This changes **where computation happens**, not source truth, Ziwei interpretation, lane ownership, Human Gates, or product maturity claims.

## 2. Authority split

- **Current ChatGPT conversation/session**: first-class repository operator. It may use **every GitHub repository operation actually exposed by the connected tools**, including file create/update/delete, branch operations, Issue operations, PR/review/comment operations, draft/ready transitions, merge/auto-merge, workflow/run operations, and other connector-exposed repository management actions. It also performs orchestration, source review, critic/red-team passes, and PI-facing synthesis.
- **GitHub Actions standard public runners**: deterministic Python/Node/Go tests, audits, regression commands, and generated validation artifacts.
- **ChatGPT Work / Codex**: optional additional shell/coding execution runtime when quota is available. It is not required merely to perform GitHub repository writes.
- **GitHub**: canonical repository, Issues, PRs, commits, validation run history, and Human-Gate audit trail.

GitHub Issues remain execution truth. Main remains accepted state.

### Conversation-mode repository authority

Repository write authority is not reserved to Work/Codex. The current ChatGPT conversation may directly perform all connector-exposed GitHub operations needed by an authorized work unit. This is an operational-capability grant, not a semantic-governance bypass: lane ownership, Issue-first execution, PR discipline, validation requirements, Human Gates, Zhongzhou source integrity, and Product maturity boundaries remain in force.

Normal work remains `Issue -> branch -> PR -> validation -> merge`. Direct-to-main is not made routine merely because a connected API could permit it.

The connected tool surface is the technical ceiling. If a GitHub operation is not exposed by the current connector/tools, this protocol does not claim that operation is technically available.

### Recovery policy

For session/task recovery, follow `PROJECT_STATE.yaml` and `governance/RECOVERY_PRECEDENCE_v1.md`. Do not use historical files that still contain `ACTIVE`, `CURRENT`, `NEXT`, or `READY_FOR_PI` as task selectors unless the active Issue explicitly references them.

## 3. Trigger policy

Allowed:
- `pull_request` triggers targeting `main`;
- `workflow_dispatch` manual fallback;
- path filters on expensive Product regression workflows.

Not allowed:
- automatic `push` triggers;
- larger/billable runners without a new explicit PI approval;
- using workflow success as authority for canonical Ziwei meaning.

The repository quality gate runs on every PR. Product P1 regression workflows may use Product-oriented path filters.

## 4. Standard repository gate

The canonical quality workflow is `.github/workflows/decontamination-ci.yml` and must execute at least:

```bash
python -m pip install --upgrade pytest
PYTHONPATH="$PWD" python -m pytest -q
if [ -f tools/iztro_export.mjs ]; then node --check tools/iztro_export.mjs; fi
PYTHONPATH="$PWD" python src/audit_repository.py --fail-on-p0
python tools/validate_governance.py \
  --base-ref "origin/<base>" \
  --head-branch "<head>"
```

For manual main validation, `--allow-main` may be used. PR lane validation must use the PR base/head contract.

### Build validation versus final integration validation

Validation has two timing classes; this changes timing, not acceptance quality.

- **ACTIVE_BUILD / READY_TO_INTEGRATE:** run the bounded unit tests, schema/source checks, write-set checks, and relevant regressions needed to develop and review the change. These runs are useful evidence but are not the final merge authorization, and the branch does not repeatedly chase unrelated `main` movement merely to keep a speculative full gate fresh.
- **INTEGRATING:** only after acquiring the Integration Lease in Issue #888, synchronize the branch once to current `main` and run the complete final gate required by the work unit, including the repository quality gate. The successful run must identify the exact integration head/base intended for immediate merge.

Only one PR may be INTEGRATING globally. Other lanes may continue ACTIVE_BUILD while that lease is held, but they must not merge `main`.

## 5. Product regression

Existing Product workflows remain executable specifications and routine PR validators when their path filters match:

- `.github/workflows/product-p1-dual-engine.yml`
- `.github/workflows/product-p1-b02-calendar.yml`
- `.github/workflows/product-p1-b02b-zi-day.yml`
- `.github/workflows/product-p1-b02c-temporal.yml`

They retain pinned independent engine/version contracts already encoded in the repository.

A Product PR does not gain empirical validity merely because deterministic engine regression passes.

## 6. Knowledge work

At minimum before merge, and specifically during INTEGRATING after the lease is held:
- changed-unit deterministic tests;
- full repository pytest via the repository quality gate unless an Issue explicitly approves a narrower scope;
- P0 audit;
- Knowledge lane governance validation;
- any source/canonical checks required by the Issue.

Knowledge mapping candidates remain non-production until a Product work unit separately selects and integrates them.

## 7. Governance work

At minimum during INTEGRATING after the lease is held:
- repository quality gate;
- governance lane validation;
- inspection that Product/Knowledge semantics did not change unintentionally.

A governance migration may bootstrap the first PR-triggered workflow. If the new trigger executes successfully on that migration PR, that run is valid G8 evidence.

## 8. Validation evidence

Every accepted PR must record, directly or by durable workflow reference:

```text
Execution runtime: GitHub Actions standard public runner / Work / Codex
Base commit: <sha>
Head commit: <sha>

Integration:
- lease ledger: Issue #888
- lease acquisition/release comment(s): <references>
- synchronized main/base: <sha>

Validation:
- repository quality gate: PASS/FAIL
- pytest: <passed>/<failed>/<skipped>
- P0 audit: PASS/FAIL
- governance: PASS/FAIL
- Product regressions: PASS/FAIL/NOT_REQUIRED
- workflow run(s) or generated report(s): <references>

Known limitations:
- <none or explicit limitation>
```

Do not report an unexecuted command as passing.

## 9. Failure policy

- One ordinary technical repair/retry is allowed autonomously.
- A genuine assertion failure must be fixed or escalated; do not weaken a gate merely to obtain green CI.
- Infrastructure failure is recorded separately from semantic/test failure.
- Repeated or conceptual failures escalate under the existing risk/Human-Gate rules.
- If `main` changes after final-gate synchronization and before merge, the final gate is stale. Do not reuse it; re-enter synchronization under the lease and rerun the required exact-head gate.

## 10. Cost and safety boundary

G8 relies on the repository remaining public and workflows using standard GitHub-hosted runners. If repository visibility changes to private, or a workflow is moved to a larger/billable runner, routine automatic Actions must be suspended until cost/permission is reviewed.

No workflow may receive write permissions unless a bounded Governance Issue explicitly requires them.

## 11. Human Gate

PI approved G8 in chat on 2026-10-20 with the instruction that Work quota was unavailable and permissions could be modified so execution could continue in the current mode.

PI later approved G9 / Issue #374: ordinary ChatGPT conversation mode is a first-class repository operator and may use all repository operations actually exposed by connected tools. The same approval also authorizes recovery decontamination so superseded/historical status words do not override current pointers.

These approvals are execution/governance-infrastructure only. They do **not** authorize changes to Zhongzhou source truth, school boundaries, temporal semantics, causal claims, empirical probabilities, or Product maturity.

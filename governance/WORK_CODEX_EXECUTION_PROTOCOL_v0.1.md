# Work + Codex Execution Protocol v0.1

Status: **HISTORICAL — SUPERSEDED FOR ROUTINE EXECUTION BY G8; REPOSITORY-OPERATOR AUTHORITY AMENDED BY ISSUE #374 (G9)**  
Tracking Issue: #340  
Effective after merge of G7.

## 1. Purpose

This protocol moves routine project execution away from GitHub Actions because the account-level Actions included usage is exhausted and the Actions budget blocks additional billed usage.

The migration changes **where computation happens**, not the research or source-of-truth model.

## 2. Authority split

- **ChatGPT Work**: orchestration, research planning, source review, multi-step coordination, critic/red-team passes, progress synthesis.
- **Codex / OpenAI coding runtime**: edit repository files, run shell commands, execute Python/Node/Go validation, debug failures, produce deterministic reports.
- **GitHub**: canonical repository, Issues, PRs, commits, durable audit trail, Human Gates.
- **GitHub Actions**: manual emergency fallback only; no automatic push or pull_request execution.

GitHub Issues remain the authoritative execution ledger. Main remains accepted state.

## 3. Normal work-unit lifecycle

1. Recover PROJECT_STATE and the active lane state.
2. Open/confirm one bounded Issue.
3. Work performs producer/research pass.
4. Work performs critic/red-team pass.
5. Codex applies repository changes in the Issue branch.
6. Codex runs the required validation scope.
7. Record exact commands and results in the PR/Issue.
8. Open/update the PR.
9. Human Gate only when governance requires it.
10. Merge accepted work to main.
11. Start the next bounded Issue only after the current unit is closed.

## 4. Mandatory validation scopes

### 4.1 Standard repository gate

Run from repository root:

```bash
python -m pip install --upgrade pytest
PYTHONPATH="$PWD" python -m pytest -q
if [ -f tools/iztro_export.mjs ]; then node --check tools/iztro_export.mjs; fi
PYTHONPATH="$PWD" python src/audit_repository.py --fail-on-p0
python tools/validate_governance.py --allow-main
```

For a PR/lane validation, governance validation must use the PR base and branch:

```bash
python tools/validate_governance.py \
  --base-ref "origin/main" \
  --head-branch "<lane>/<issue>-..."
```

Do not substitute `--allow-main` for lane validation when validating a feature branch.

### 4.2 Product P1 dual-engine regression

Install pinned engines:

```bash
npm install --no-save iztro@2.6.1
python -m pip install --upgrade "x-iztro==0.6.1"
```

Build input and run the existing adapters/comparators using the exact commands preserved in:
- `.github/workflows/product-p1-dual-engine.yml`
- `.github/workflows/product-p1-b02-calendar.yml`
- `.github/workflows/product-p1-b02b-zi-day.yml`
- `.github/workflows/product-p1-b02c-temporal.yml`

Those workflows are now executable specifications/manual fallbacks, not routine CI.

When the independent Go audit is required, use the pinned external engine commit already encoded in the workflow:
`947166fc45cd7c8c0849da1bd870f570972a7172`.

### 4.3 Knowledge work

At minimum:
- targeted deterministic knowledge tests for the changed work unit;
- full `python -m pytest -q` before merge unless the Issue explicitly defines a narrower, approved validation scope;
- governance lane validation;
- source/canonical consistency checks required by the Issue.

Source-derived claims must remain traceable to the approved Zhongzhou material. Validation does not upgrade unsupported interpretations into canonical rules.

### 4.4 Governance work

At minimum:
- `python tools/validate_governance.py --base-ref origin/main --head-branch <governance-branch>`;
- tests covering changed governance invariants when present;
- static inspection that no unintended Product/Knowledge semantics changed.

## 5. Validation evidence format

Every PR must contain a **Validation Evidence** block:

```text
Execution runtime: Codex / OpenAI cloud environment
Base commit: <sha>
Head commit: <sha>

Commands:
1. <exact command>
2. <exact command>

Results:
- pytest: <passed>/<failed>/<skipped>
- P0 audit: PASS/FAIL
- governance: PASS/FAIL
- product regression: PASS/FAIL/NOT_REQUIRED
- generated reports: <paths or NONE>

Known limitations:
- <none or explicit limitation>
```

A statement such as "tests should pass" is not evidence.

## 6. Failure policy

- A real test failure must be fixed or explicitly escalated; never suppress it by deleting assertions or weakening gates without an approved Issue.
- Infrastructure/runtime failure must be separated from test failure.
- If an OpenAI execution environment cannot run a required external dependency, record the blocker and do not claim validation.
- Do not spend GitHub Actions minutes merely to reproduce validation already completed in Codex.

## 7. GitHub Actions policy

All workflows under `.github/workflows/` are manual-only after G7.

Allowed use:
- explicit emergency/manual reproduction;
- audit comparison when the account later has available Actions capacity;
- one-off confirmation requested by the PI.

Not allowed:
- automatic push triggers;
- automatic pull_request triggers;
- using Actions status as the sole validation evidence.

## 8. Reversibility

To revert G7:
1. restore the prior trigger blocks from Git history;
2. update this protocol and AGENT_WORKFLOW;
3. record the change in a Governance Issue;
4. only re-enable automatic Actions after confirming adequate quota/budget and PI approval.

## 9. Human Gate

The PI approved the G7 migration in chat on 2026-10-19.

The migration changes execution infrastructure only. It does **not** authorize changes to Zhongzhou theory, canonical source truth, probability claims, temporal semantics, or Product maturity claims.


## 10. Later authority amendment (G9 / Issue #374)

On 2026-10-20, the PI explicitly changed the repository-operator rule: ordinary ChatGPT conversation mode is authorized as a first-class repository operator and may use every GitHub operation actually exposed by the connected tools.

This supersedes the old G7 assumption that repository edits must be handed to Codex merely because the current session is not Work/Codex. The effective authority split is maintained in `governance/PUBLIC_ACTIONS_EXECUTION_PROTOCOL_v0.2.md`.

This amendment changes operational capability only. Issue-first execution, lane ownership, PR discipline, validation gates, Human Gates, Zhongzhou source integrity, and product maturity boundaries remain in force.

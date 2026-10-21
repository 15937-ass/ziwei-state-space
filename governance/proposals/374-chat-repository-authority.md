# Proposal #374 — Conversation Repository Authority and Recovery Decontamination

Status: **APPROVED / IMPLEMENTING**  
Tracking Issue: #374  
Risk: R3 / Human Gate  
Lane: GOVERNANCE_ONLY

## Motivation

The PI approved ordinary ChatGPT conversation mode as a first-class repository operator. The repository also contains preserved historical artifacts whose old status words can mislead a new conversation into selecting the wrong task or execution policy.

This proposal therefore combines two tightly related governance fixes:

1. **G9 repository authority** — conversation mode may use all connector-exposed repository operations.
2. **Recovery decontamination** — historical `ACTIVE/CURRENT/NEXT/READY_FOR_PI` markers must not override live authority pointers.

The need is concrete: G7 remained labeled as an active execution contract and its manual-only Actions rule caused a later conversation to ignore the already-active G8 public-Actions policy.

## Goals

- make the current ChatGPT conversation a first-class repository operator;
- keep GitHub Issues/PRs as live execution/implementation truth;
- add one explicit recovery-precedence contract;
- make `PROJECT_STATE.yaml` point directly to the current execution protocol and recovery contract;
- quarantine G7 as historical/superseded;
- prevent README/task/validation/proposal/roadmap historical status words from selecting work;
- preserve historical evidence rather than rewriting old validation results;
- keep standard public GitHub-hosted PR Actions as approved deterministic validation;
- retain lane ownership, Human Gates, source integrity, and PR validation.

## Non-Goals

- no Zhongzhou canonical semantic changes;
- no Product runtime changes;
- no Knowledge rule changes;
- no deletion of historical evidence;
- no permission to bypass Human Gates, lane ownership, or PR validation;
- no larger/billable GitHub runners;
- no automatic push-triggered Actions.

## Recovery Design

The authoritative bootstrap becomes:

```text
PROJECT_STATE.yaml
-> governance/RECOVERY_PRECEDENCE_v1.md
-> selected lane state (cache)
-> live lane GitHub Issue (execution truth)
-> linked PR (implementation truth)
-> Issue-required artifacts only
```

If a lane state is stale, live GitHub Issue/PR wins and the cache is repaired.

The following are explicitly non-authoritative for task selection unless the active Issue references them:

- archived checkpoints;
- legacy `tasks/*.yaml`;
- README current-phase text;
- historical validation “next work” sections;
- completed acceptance records;
- stale roadmap current/next labels;
- old proposal files;
- superseded protocols;
- historical Human-Gate `READY_FOR_PI` markers.

## G9 Repository Authority

The current ChatGPT conversation/session may use every GitHub repository action actually exposed by connected tools, including file, branch, Issue, PR, review/comment, draft/ready, merge/auto-merge, workflow/run, and other connector-exposed repository management operations.

This is an execution-capability grant, not a semantic-governance bypass.

Normal work remains:

`Issue -> branch -> PR -> validation -> merge`

Work/Codex remain optional shell/coding runtimes. Standard public GitHub-hosted runners remain approved deterministic validation runtimes under G8.

## Historical Artifact Policy

Historical evidence is preserved. It is not rewritten merely because its old “next step” is no longer current.

Where a historical governance artifact itself is dangerously ambiguous, add a prominent `HISTORICAL / SUPERSEDED / DO NOT USE FOR RECOVERY` banner and a pointer to the current contract.

For artifacts outside the active Governance lane's path ownership, the recovery contract prevents their local status words from becoming global execution commands.

## Compatibility

Compatible with:
- Repository Governance v1;
- G8 public Actions;
- Product v0.4 / Proposal #425;
- Product Knowledge dependency Proposal #491;
- Knowledge Response Semantics #419.

## Test Plan

Deterministic governance tests must verify:

- `PROJECT_STATE.yaml` names the current execution protocol and recovery-precedence file;
- G7 is explicitly historical and says not to use it for recovery;
- G8 allows pull-request Actions and first-class conversation repository authority;
- recovery contract rejects legacy status words as task selectors;
- Roadmaps/Decision Log are not treated as execution queues;
- ordinary Issue/branch/PR/validation discipline remains;
- no Product or Knowledge semantic artifact is changed.

Full repository quality gate and governance validator must pass on the exact PR head.

## Migration Plan

1. close stale/conflicted PR #377 unmerged as superseded;
2. reconstitute #374 from current main;
3. add recovery precedence;
4. apply G9 authority to G8 / AGENT_WORKFLOW;
5. quarantine G7;
6. update current governance headers/pointers;
7. add non-execution-queue warnings to Roadmaps/Decision Log/execution plan;
8. pass G8 quality gate;
9. merge and close #374.

## Human Gate

Approved by PI in chat:
- 2026-10-20: conversation mode may use full connector-exposed repository permissions;
- 2026-10-21: clean repository content that interferes with GPT task recognition so the new rules are explicit.

## Decision

**APPROVED.** Historical evidence remains preserved, but current recovery must be unambiguous and pointer-driven.

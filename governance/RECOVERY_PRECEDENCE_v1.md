# Recovery Precedence v1.0

Status: **ACTIVE RECOVERY ROUTING CONTRACT AFTER MERGE OF G9 CLEANUP**  
Scope: session bootstrap, task identification, active-work recovery, Human-Gate routing, and execution-policy selection.

## 1. Purpose

This file exists to stop historical artifacts from being mistaken for current instructions.

The repository intentionally preserves old proposals, validation reports, acceptance records, archived checkpoints, superseded protocols, and completed task files. Those artifacts are valuable evidence, but many contain words such as `ACTIVE`, `CURRENT`, `NEXT`, `READY_FOR_PI`, or old execution rules that were correct only at the time they were written.

For recovery and task selection, **current authority is determined by pointers and live GitHub state, not by whichever file contains the strongest-sounding status word.**

## 2. Mandatory recovery order

For every new ChatGPT conversation, timeout recovery, model/session change, or suspected external merge:

1. Read `PROJECT_STATE.yaml`.
2. Read the single canonical session-start instruction `CHATGPT_START_HERE.md`.
3. Read this file.
4. Read the selected lane state:
   - `product/PRODUCT_STATE.yaml`
   - `knowledge/KNOWLEDGE_STATE.yaml`
   - `governance/GOVERNANCE_STATE.yaml`
5. If the selected lane is Knowledge, select exactly one shard (`CORE` or `P01..P12`) and read the shard state referenced by the Knowledge coordinator.
6. Query live GitHub Issues for the selected lane/shard.
7. If an active/open bounded Issue exists, **the Issue is execution truth even when the state cache is stale**.
8. Read the Issue-linked PR, if any. The PR is implementation truth.
9. Read only artifacts required by that Issue/PR.
10. Use the execution protocol explicitly named by `PROJECT_STATE.yaml`; do not select a protocol by filename age or by searching for the word `ACTIVE`.
11. If the work unit is preparing to merge, read `governance/INTEGRATION_QUEUE_PROTOCOL_v1.md` and live coordination Issue #888 before running any final exact-head acceptance gate.

If GitHub live state and a state YAML disagree, **GitHub Issue/PR wins and the cache must be repaired**. The current ChatGPT conversation is permitted to operate the repository through exposed connector actions, but chat text itself is not project-state authority.

Old saved startup prompts, prior-chat instructions, and copied snippets are not authority. In particular, never follow a stale prompt that treats the G7-era Actions restriction as current; use `CHATGPT_START_HERE.md` and the current protocol pointer instead.

## 3. Current execution policy

The effective routine execution protocol is:

`governance/PUBLIC_ACTIONS_EXECUTION_PROTOCOL_v0.2.md`

Current rules:

- the current ChatGPT conversation is a first-class repository operator and may use all GitHub repository operations actually exposed by connected tools; this capability is distinct from whether chat text is authoritative project state;
- standard public GitHub-hosted runner validation is allowed; automatic `pull_request` triggers and `workflow_dispatch` are allowed, while automatic `push` triggers remain prohibited; a prohibition on automatic push triggers must never be paraphrased as a blanket Actions disablement;
- standard GitHub-hosted runners for this public repository are allowed for routine deterministic validation;
- automatic `pull_request` triggers are allowed;
- automatic `push` triggers are prohibited;
- larger/billable runners are not authorized without new PI approval;
- Work/Codex are optional execution runtimes, not prerequisites for repository writes;
- normal work remains `Issue -> branch -> PR`, with build validation during ACTIVE_BUILD and final exact-head validation only after the work unit acquires the Integration Lease and enters INTEGRATING;
- connector capability never bypasses lane ownership, Human Gates, source integrity, or validation.

The G7 protocol `governance/archive/WORK_CODEX_EXECUTION_PROTOCOL_v0.1_G7_HISTORICAL.md` is historical and must never be used to determine current Actions or repository-operator policy.

## 4. Artifacts that are NOT execution truth by themselves

The following may be read for evidence or historical context, but must **not** determine the current task unless the active Issue explicitly references them:

- `governance/archive/**`;
- historical `validation/**` reports and their “next work” sections;
- completed acceptance documents;
- legacy `tasks/*.yaml`;
- README “Current phase” text;
- old ChatGPT startup prompts or copied instructions that conflict with `CHATGPT_START_HERE.md`;
- branch/PR names from old work;
- files named `*_PROPOSAL*` or stored in proposal directories when they are not the currently approved controlling proposal;
- old roadmap “current/next” snapshots;
- stale status fields inside completed work products;
- historical `READY_FOR_PI` / Human-Gate markers.

A historical Human Gate is **not pending** merely because an old artifact says `READY_FOR_PI`. A gate is current only when the current lane state and/or active GitHub Issue identifies it as pending. In Knowledge specifically, `pending_on_main` is the recovery pointer; archived/future/superseded gates are not current PI requests.

## 5. Roadmaps, Decisions, and Proposals

Roadmaps are architectural direction, not daily queues. Words such as `CURRENT CRITICAL PATH` describe the roadmap version in which they were written; the live Issue determines what is actually being executed.

`DECISION_LOG.md` is a decision registry, not a task queue. Entries explicitly marked `Resolved`, `FROZEN`, `Approved`, `Implemented`, or superseded are not open tasks even if they appear beneath an older “Pending decisions” heading.

Proposal artifacts record design history. If a canonical implemented artifact exists, an older `*_proposal` file does not regain authority merely because search retrieves it first.

## 6. Status-word conflict rule

If a file says `ACTIVE`, `CURRENT`, `NEXT`, `PENDING`, or `READY_FOR_PI` but is not one of the current authority pointers above, treat that word as **local historical context**, not as a global execution command.

When two artifacts conflict, use this recovery precedence:

```text
PROJECT_STATE authority pointers
-> current Constitution / Governance
-> approved Human Gate / controlling approved Proposal
-> live lane GitHub Issue
-> linked PR
-> lane State cache
-> Roadmap / phase plan
-> historical validation / acceptance / task / proposal artifact
-> chat text
```

For daily execution status specifically, the live GitHub Issue/PR outranks a stale lane/shard-state cache.

For Knowledge, multiple live Issues may legitimately exist only when they belong to distinct palace shards under the G12 limits. Recovery must not treat an Issue from another palace as the current chat's work unit.

## 7. Legacy-artifact handling

Do not delete or rewrite historical evidence merely to make search cleaner.

Instead:
- current governance files carry explicit supersession pointers;
- recovery ignores non-authoritative status words;
- historical evidence keeps its original claims and timestamps;
- if a legacy artifact is dangerously ambiguous and is within the active lane's ownership, add a visible `HISTORICAL / SUPERSEDED / DO NOT USE FOR RECOVERY` banner rather than altering the underlying historical result.

## 8. Minimal bootstrap question

After recovery, the agent should be able to answer exactly:

> Which lane is selected, what live GitHub Issue is the current bounded work unit, which PR implements it, what Human Gate (if any) is actually pending now, which execution protocol controls validation, and—only if final integration is planned—who currently holds the Integration Lease in Issue #888?

If any of those cannot be answered from the authority chain above, stop task execution and repair recovery state before opening unrelated work.

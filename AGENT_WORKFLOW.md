# AGENT_WORKFLOW.md

Version: 1.1
Governance: GOVERNANCE.md

## 1. Core rule

Chat is not project state. GitHub Issues define active work; PRs define implementation; main contains accepted state.

## 2. Session bootstrap

For a new session, timeout recovery, hard checkpoint, or possible external merge:
1. read PROJECT_STATE.yaml;
2. read the active lane state;
3. open the active GitHub Issue;
4. open its linked PR if present;
5. read only Issue-required artifacts.

Do not infer current work from old chat, stale branch names or legacy PRs.

## 3. Lanes

Every execution turn has exactly one lane:
- PRODUCT_ONLY
- KNOWLEDGE_ONLY
- GOVERNANCE_ONLY

Read access may be broad. Write access follows governance/PATH_OWNERSHIP.json.

Cross-lane discoveries are recorded as dependency/gap Issues; they are not silently repaired from the wrong lane.

## 4. Issue-first execution

Normal execution requires an Issue satisfying Definition of Ready:
- lane
- goal
- non-goals
- inputs
- deliverables
- acceptance criteria
- dependencies
- risk
- Human Gate classification

One lane has at most one ACTIVE Issue.

## 5. Work-unit cycle

1. recover state;
2. confirm lane and Issue;
3. producer pass in the current ChatGPT session, ChatGPT Work, or Codex as available;
4. critic/red-team pass;
5. revision;
6. deterministic validation in an approved execution runtime: GitHub Actions standard public-repository runners, or Work/Codex when available;
7. record exact validation commands, runtime, workflow/run references when applicable, and results in the Issue/PR;
8. create/update one PR for the Issue;
9. report status;
10. stop.

After G8, GitHub Actions on standard public-repository runners is an approved routine deterministic validation runtime.

Do not automatically chain into the next Issue in the same turn.

## 6. Proposal rule

Substantial architecture/theory/governance changes follow governance/PROPOSAL_PROCESS.md.
Ordinary bugs and bounded implementation work do not create Proposals.

An implementation Issue may not broaden an approved Proposal.

## 7. Autonomy and risk

R0: mechanical bug/fixture/formatting — autonomous.
R1: normal bounded work — GPT review + deterministic validation in the approved available runtime.
R2: phase closure/cross-module integration/material ambiguity — independent review + full approved-runtime validation + PI-facing report.
R3: Human Gate/canonical meaning/architecture boundary/causal upgrade — explicit PI approval.

All PI review/Human-Gate material is written in Chinese.

## 8. Product anti-scaffolding

Interface/schema/registry existence is not product completion.
After PL3, new abstraction requires benchmark evidence, a canonical integration gap, or an approved Proposal.
Empty production registries are BLOCKED/UNCOVERED.

## 9. Knowledge integrity

Evidence priority:
1. primary/approved Zhongzhou source;
2. explicit Zhongzhou commentary;
3. transparent inference;
4. research hypothesis.

Lower-priority evidence cannot overwrite higher-priority evidence.
Empirical mismatch creates a Knowledge Gap Report; it does not rewrite source truth.

## 10. Checkpoints and timeout safety

Soft checkpoint: every user-facing execution report; no commit required.

Hard checkpoint: bounded work unit complete, source-review recoverable boundary, phase closure, Human Gate boundary, or substantial unreconstructable work.

Default source-review reasoning sub-batch remains about 50 items; durable integration ceiling remains 100 source-review items unless explicitly approved.

After timeout, inspect GitHub first. Never replay work blindly.

### 10.1 In-work-unit synchronization fast path

GitHub remains the durable source of truth. The fast path only reduces redundant reads; it never transfers authority to chat memory, a local workspace, or an execution cache.

At work-unit bootstrap, recover authoritative state once and establish a temporary execution context containing at minimum:
- lane;
- active Issue;
- active PR if present;
- working branch and observed head SHA;
- observed main/base SHA;
- state-file/version references required by the Issue;
- the current source-review/item range when applicable.

While the same bounded work unit continues and no invalidation trigger occurs, do not repeatedly re-read PROJECT_STATE, lane state, Issue, PR or unchanged repository files merely to reconfirm values already observed. Product/Knowledge reasoning, critic passes and tests should run continuously inside that bounded context.

Mandatory resynchronization occurs before continuing whenever any of the following happens:
- timeout, new session or execution-environment restart;
- lane, Issue, PR or working-branch change;
- known or suspected external merge/push;
- observed head/base SHA mismatch, rejected optimistic-concurrency write, merge conflict or stale blob SHA;
- a GitHub write returns an ambiguous/unknown outcome;
- hard checkpoint, pre-merge validation or final acceptance;
- tool/runtime failure that could have changed repository state;
- any evidence that the cached execution context may be stale.

All GitHub writes use optimistic concurrency. Fetch the target blob/ref SHA when required, write against that observed version, and on mismatch stop and resynchronize. Never force-overwrite a newer repository state merely to preserve the fast path. If a write times out or its outcome is unknown, verify whether it actually landed before retrying, so duplicate commits/comments or accidental overwrites are not created.

#### No-information-loss invariant

Execution speed may never be purchased by losing recoverability. Before leaving a bounded work unit, crossing a hard checkpoint, switching lane, or allowing an unreconstructable sub-batch to grow beyond the approved boundary, durably preserve all material progress.

A durable checkpoint must preserve enough information to restart without semantic loss, including as applicable:
- base/main SHA and working head SHA;
- lane, Issue, PR and branch;
- changed/versioned artifact paths;
- exact source-review or rule/item range completed;
- accepted, blocked, conflicted and unresolved classifications;
- source/evidence traceability needed to reproduce the conclusion;
- material decisions and their rationale;
- validation status, executed commands/workflows and known limitations;
- discovered blockers/dependencies that remain outside the current work unit.

Durable preservation means versioned repository artifacts and/or the authoritative Issue/PR record. A chat-only statement is not a durable checkpoint.

Never discard local/uncommitted source-review output merely because a resync is required. First determine whether the output already exists durably; if not, preserve it or explicitly reconstruct/verify it before proceeding. Ambiguous partial writes are verified, not blindly replayed.

For Knowledge source review, the existing batch discipline is unchanged: reasoning sub-batches remain about 50 items and durable integration remains capped at 100 items unless explicitly approved. The intended pattern is therefore one authoritative sync -> continuous bounded processing -> durable checkpoint/resync, not per-item or per-few-item Git polling.

The execution context cache is disposable and non-authoritative. On any conflict, GitHub wins; the cache is invalidated and rebuilt from authoritative state.

## 11. Execution and validation policy

Routine deterministic validation may use GitHub Actions because this repository is public and G8 explicitly authorizes standard GitHub-hosted runners. Larger/billable runners are not authorized.

Execution split:
- the current ChatGPT session performs orchestration, research, review, GitHub edits and progress synthesis;
- ChatGPT Work / Codex remain optional execution runtimes when quota is available;
- GitHub Actions standard public-repository runners may execute Python/Node/Go tests and regressions;
- GitHub remains the canonical source for Issues, PRs, commits, validation evidence and Human Gates.

At each hard checkpoint, run the validation scope required by governance/PUBLIC_ACTIONS_EXECUTION_PROTOCOL_v0.2.md and record:
- exact command(s) or workflow;
- environment/runtime used;
- pass/fail counts;
- any skipped checks and why;
- relevant generated report or workflow-run references.

Automatic pull_request triggers are allowed. Automatic push triggers remain prohibited.

One autonomous repair/retry is allowed for ordinary technical failure; repeated or conceptual failures escalate.

## 12. Pull Request discipline

A PR implements one primary Issue.
Use short-lived branches:
- product/<issue>-...
- knowledge/<issue>-...
- governance/<issue>-...

Scope creep becomes a new Issue/Proposal.
Stacked PRs are exceptional and limited to two levels.

## 13. Mandatory PI-facing Chinese progress report

The PI-facing report is domain- and project-oriented, not Git-oriented. The PI is expected to judge Ziwei theory, research boundaries, interpretation quality, and major product direction; routine Git mechanics should be hidden unless they block progress or create risk.

Default report order:

【整个项目现在到哪了】
- State the current macro stage in plain Chinese.
- Explain how the current work fits into the full path: knowledge construction -> faithful inference -> empirical validation -> personalization/productization.
- State what has already become stable and what is still only preparatory.

【这一步刚刚完成了什么】
- Explain the substantive result, not commit/branch details.
- Distinguish clearly between "framework/interface ready", "knowledge/content ready", "internally validated", and "empirically validated".

【下一步准备做什么】
- Name the next 1–2 substantive tasks and why they are next.
- Do not present a long technical backlog unless requested.

【现在需要 PI 帮助什么】
- Explicitly state whether PI input is needed.
- If YES, ask only questions that require Ziwei knowledge, source interpretation, school-boundary judgment, case interpretation, research priority, or major product/research choice.
- If NO, say "本阶段暂不需要你介入，我可以继续自动推进。"
- Never ask the PI to decide routine Git/CI/branch mechanics.

【需要你特别警惕的风险】
- Only include material risks: theory contamination, school mixing, unsupported inference, benchmark misuse, empirical/canonical boundary violation, product maturity overclaim, or a decision that may lock future architecture.
- Omit routine technical noise.

Technical appendix is optional and normally omitted. Include GitHub Issue/PR/CI identifiers only when:
- a technical failure blocks progress;
- the PI explicitly asks;
- a Human Gate/audit needs a durable reference;
- there is a repository-integrity risk.

Human Gate material remains in Chinese and must explain the Ziwei/research meaning before technical implementation consequences.
## 14. Archive / Resume rule

If `PROJECT_STATE.yaml` says `project_status: "ARCHIVED"`:
- do not start Product, Knowledge, benchmark, Proposal, or Human-Gate execution;
- first read the versioned archive checkpoint named in PROJECT_STATE;
- require an explicit PI instruction to resume the project;
- after resume, perform a repository health/recovery check and create or reopen exactly one bounded Issue for the selected lane;
- archived branch/PR progress is evidence to recover from, not canonical main truth;
- never silently merge a legacy stack just because it existed before archive.

For PI-facing archive/resume reporting, explain the research stage, preserved knowledge progress, next substantive work, and upcoming Ziwei-knowledge decisions. Omit routine Git mechanics unless they create a recovery risk.


# AGENT_WORKFLOW.md

Version: 1.0
Governance: GOVERNANCE.md

## 1. Core rule

Chat is not project state. GitHub Issues define active work; PRs define implementation; main contains accepted state.

## 2. Session bootstrap

For a new session, timeout recovery, hard checkpoint, or possible external merge:
1. read `PROJECT_STATE.yaml`;
2. read `governance/RECOVERY_PRECEDENCE_v1.md`;
3. read the selected lane state as a recovery cache;
4. for KNOWLEDGE_ONLY, select CORE or one palace shard and read the shard state referenced by `knowledge/KNOWLEDGE_STATE.yaml`;
5. query live GitHub Issues for the selected lane/shard;
6. if a bounded active/open Issue exists, treat it as execution truth even if the state cache is stale;
7. open the Issue-linked PR if present and treat it as implementation truth;
8. read only Issue-required artifacts.

Do not infer current work from old chat, stale branch names, legacy PRs, README “Current phase” text, `tasks/*.yaml`, historical validation “next work” sections, old proposal files, or superseded protocols.

Words such as `ACTIVE`, `CURRENT`, `NEXT`, `PENDING`, and `READY_FOR_PI` are local metadata unless the current authority chain names that artifact. Historical Human-Gate markers do not create a current PI request by themselves.

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

Product and Governance retain one ACTIVE work unit each. Knowledge follows `governance/KNOWLEDGE_SHARD_EXECUTION_v1.md`: Core WIP <= 1, total palace WIP <= 4, and per-palace WIP <= 1.

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

## 11. Execution and validation policy

Routine deterministic validation may use GitHub Actions because this repository is public and G8 explicitly authorizes standard GitHub-hosted runners. Larger/billable runners are not authorized.

Execution split:
- the current ChatGPT conversation/session is a first-class repository operator and may use every GitHub operation actually exposed by the connected tools, including file create/update/delete, branch operations, Issue/PR/review/comment operations, draft/ready transitions, merge/auto-merge, workflow/run operations, and other connector-exposed repository management actions; it also performs orchestration, research, review and progress synthesis;
- ChatGPT Work / Codex remain optional shell/coding execution runtimes when quota is available; they are not required merely to perform repository writes;
- GitHub Actions standard public-repository runners may execute Python/Node/Go tests and regressions;
- GitHub remains the canonical source for Issues, PRs, commits, validation evidence and Human Gates.

At each hard checkpoint, run the validation scope required by governance/PUBLIC_ACTIONS_EXECUTION_PROTOCOL_v0.2.md and record:
- exact command(s) or workflow;
- environment/runtime used;
- pass/fail counts;
- any skipped checks and why;
- relevant generated report or workflow-run references.

Automatic pull_request triggers are allowed. Automatic push triggers remain prohibited.

Repository capability does not override governance authority. Issue-first execution, lane/path ownership, PR discipline, validation gates, Human Gates, source integrity and maturity boundaries still apply. Normal work remains Issue -> branch -> PR -> validation -> merge; direct-to-main is not routine merely because a connected API could allow it.

The connected tool surface is the technical ceiling. If an operation is not exposed by the current connector/tools, report that as a technical interface limitation rather than a governance prohibition.

One autonomous repair/retry is allowed for ordinary technical failure; repeated or conceptual failures escalate.

## 12. Pull Request discipline

A PR implements one primary Issue.
Use short-lived branches:
- product/<issue>-...
- knowledge/core-<issue>-...
- knowledge/pXX-<issue>-...
- governance/<issue>-...

Knowledge palace branches are write-isolated by `governance/KNOWLEDGE_SHARDS.json`. The exact Issue #525 legacy Property branch is temporarily grandfathered.

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


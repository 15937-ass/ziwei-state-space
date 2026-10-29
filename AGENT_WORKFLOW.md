# AGENT_WORKFLOW.md

Version: 1.2
Governance: GOVERNANCE.md

## 1. Core rule

Chat text is not project state. GitHub Issues define active work; PRs define implementation; main contains accepted state. Separately, the current ChatGPT conversation is a first-class repository operator and may use every GitHub operation exposed by the connected tools. Do not confuse “chat is not state authority” with “chat cannot operate the repository.”

## 2. Session bootstrap

For a new session, timeout recovery, hard checkpoint, model/session change, or possible external merge:
1. read `PROJECT_STATE.yaml`;
2. read `CHATGPT_START_HERE.md` as the single canonical ChatGPT startup instruction;
3. read `governance/RECOVERY_PRECEDENCE_v1.md`;
4. read the selected lane state as a recovery cache;
5. for KNOWLEDGE_ONLY, select CORE or one palace shard and read the shard state referenced by `knowledge/KNOWLEDGE_STATE.yaml`;
6. query live GitHub Issues for the selected lane/shard;
7. if a bounded active/open Issue exists, treat it as execution truth even if the state cache is stale;
8. open the Issue-linked PR if present and treat it as implementation truth;
9. read only Issue-required artifacts.

Do not reuse conflicting startup instructions from prior chats or external notes. If an old prompt claims that GitHub Actions are disabled based on G7-era rules, discard that instruction and follow `CHATGPT_START_HERE.md` plus the current protocol pointer. Do not infer current work from old chat, stale branch names, legacy PRs, README “Current phase” text, `tasks/*.yaml`, historical validation “next work” sections, old proposal files, or superseded protocols.

Words such as `ACTIVE`, `CURRENT`, `NEXT`, `PENDING`, and `READY_FOR_PI` are local metadata unless the current authority chain names that artifact. Historical Human-Gate markers do not create a current PI request by themselves.

## 3. Lanes

Every execution turn has exactly one lane:
- PRODUCT_ONLY
- KNOWLEDGE_ONLY
- GOVERNANCE_ONLY

Read access may be broad. Write access follows governance/PATH_OWNERSHIP.json.

Cross-lane discoveries are recorded as dependency/gap Issues; they are not silently repaired from the wrong lane.

For a cross-lane blocker, use `governance/CROSS_LANE_HANDOFF_v1.md` to link the producer and consumer Issues, name the exact accepted-main input and unblock condition, and record work that can proceed independently. A roadmap label, an unmerged branch, or a green PR check does not by itself release a consumer.

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
3. work in `ACTIVE_BUILD`: producer pass, critic/red-team pass, revision, and bounded/relevant validation;
4. create/update one PR for the Issue and record durable checkpoints;
5. when content is complete, move to `READY_TO_INTEGRATE` and record it in coordination Issue #888;
6. only after acquiring the sole Integration Lease, enter `INTEGRATING`;
7. synchronize once to current `main`, run the final exact-head validation required by the work unit, and record exact run identity;
8. if green and still fresh, merge immediately and release the lease; if stale/failed, do not merge;
9. report status;
10. stop.

The controlling integration contract is `governance/INTEGRATION_QUEUE_PROTOCOL_v1.md`. ACTIVE_BUILD may continue in other lanes while one PR is INTEGRATING.

After G8, GitHub Actions on standard public-repository runners is an approved routine deterministic validation runtime. Automatic `pull_request` validation and `workflow_dispatch` are allowed; automatic `push` triggers remain prohibited. This is not a blanket Actions disablement.

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

Batch independent, task-required reads and state queries in one round where supported; inspect every result. Keep dependent reads, writes and acceptance decisions sequential. Load a change summary/changed-path list and relevant blob/version references first, then reload only affected or missing material. A summary cannot replace direct source inspection needed to resolve wording, prerequisites, conflicts or temporal scope. Do not load all sources, the full ontology plan or unrelated lane histories by default.

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

### 10.2 Validation reuse and combined audit

Maintain one durable validation record per validation identity: exact PR base/main and head SHAs, relevant source/input/lock versions, check scope and commands, workflow/config/dependency/runtime versions, run attempt and outcome. Reuse an existing successful record only when all these match and every required check completed. Reference its evidence rather than copying a second full report or starting an identical run merely for another progress message. Unknown, skipped, pending, failed or unavailable required evidence is not PASS.

At a hard checkpoint recheck the work unit's own live head, required inputs and gates. At final merge, first acquire the Integration Lease from Issue #888 and enter INTEGRATING; only then synchronize to current main/head and run the complete exact-head acceptance scope. This freshness check is mandatory even when a matching earlier build-stage run exists. A changed final base/head, relevant input, dependency, workflow, environment or required scope invalidates the affected final result; synchronize safely under the lease and perform the required validation again. An unchanged source blob may retain its source-review evidence, but that does not carry forward a stale whole-PR acceptance. Existing full-gate requirements remain controlling; this section grants no narrower scope or validation exemption.

For one bounded source batch, inspect provenance/source fidelity, IDs/count reconciliation and temporal layers together, but record each verdict separately with evidence and unresolved items. Preserve school boundaries, prerequisites, conflicts and UNKNOWN; aggregate success cannot hide a failed dimension. Keep source fidelity, structural consistency, internal reconstruction and empirical validity distinct. The existing ~50-item reasoning sub-batch / <=100-item durable integration limits still apply.

When CI is pending, retain its run ID and last observed status; check at meaningful completion/dependency boundaries instead of tight polling. Record a terminal outcome once. Retry a failed check only under the existing failure policy; a retry/attempt is new evidence, not a rewrite of the failed record.

### 10.3 Compact cross-chat checkpoint

Before stopping or switching work, update the existing Issue/PR with this compact payload (or link equivalent versioned evidence); do not create a second status authority:

```text
Observed at: <timestamp with timezone>; lane/shard: <one>; Issue/PR/branch: <references>
Versions: main/base=<SHA>; head=<SHA>; relevant input/lock=<versions or evidence link>
Done: <bounded source/item range, decisions and artifact paths; evidence links>
Remaining: <next precise source anchor/action; unresolved items and rationale>
Validation: <identity/run/attempt; PASS/FAIL/PENDING/UNVERIFIED; required gaps>
Blocker/handoff: <producer -> consumer; accepted input; exact unblock condition>
Ownership: <task claimant/executing session reference; allowed write set; active/waiting/released>
Next: <resume this task / wait / release; current PI gate if any>
```

On resume, read the existing checkpoint after the mandatory bootstrap/live-state recovery. Compare versions and task assignment, then load the delta; do not replay completed evidence without a reason. Update the checkpoint to supersede stale resume instructions while preserving material decisions and historical evidence. Before claiming a slot, confirm the live Issue and linked PR have no existing worker on that task; a second chat resumes only after explicit handoff, rather than duplicating the work. An observation timestamp or chat claim alone is not an atomic cross-chat lock; ambiguous ownership blocks writes until resolved. Slot availability does not itself activate a backlog Issue or satisfy its dependencies.

The controlling proposal and worked recovery/reuse examples are in [Proposal #432](governance/proposals/432-fast-sync-no-loss.md); load the examples only when needed.

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

Repository capability does not override governance authority. Issue-first execution, lane/path ownership, PR discipline, validation gates, Human Gates, source integrity and maturity boundaries still apply. Normal work remains Issue -> branch -> PR -> ACTIVE_BUILD -> READY_TO_INTEGRATE -> Integration Lease -> exact-head validation -> merge; direct-to-main is not routine merely because a connected API could allow it.

The connected tool surface is the technical ceiling. If an operation is not exposed by the current connector/tools, report that as a technical interface limitation rather than a governance prohibition.

One autonomous repair/retry is allowed for ordinary technical failure; repeated or conceptual failures escalate.

## 12. Pull Request discipline

A PR implements one primary Issue.
Use short-lived branches:
- product/<issue>-...
- knowledge/core-<issue>-...
- knowledge/pXX-<issue>-...
- governance/<issue>-...

Knowledge palace branches are write-isolated by `governance/KNOWLEDGE_SHARDS.json`. The temporary #525 legacy Property exemption expired when PR #532 merged; no legacy-form Knowledge branch remains authorized.

Scope creep becomes a new Issue/Proposal.
Stacked PRs are exceptional and limited to two levels.

## 13. Mandatory PI-facing Chinese progress and cross-lane closeout report

Protocol marker: `PI_CLOSEOUT_FINAL_GATE_REQUIRED`.

This section is a **hard final-response gate** for every repository-work conversation. Before sending the final answer, the assistant must complete the live read-only three-stream census required below and include all six default Chinese report sections. If that gate is incomplete, the repository-work final answer must not be sent. Brevity, successful completion, read-only review, validation waiting, a blocked/paused unit, or the user's failure to ask again are not exemptions.

The only exemption is an ordinary end-user QuickRead, DetailedRead, or other fortune-reading turn that performs no repository implementation, review, governance, status recovery, or other repository work. If repository work occurs anywhere in the same turn, the mandatory closeout applies. This reporting gate does not authorize writes in another lane, consume unmerged artifacts, or broaden the active Issue.

The PI-facing report is domain- and project-oriented, not Git-oriented. The PI is expected to judge Ziwei theory, research boundaries, interpretation quality, and major product direction; routine Git mechanics should be hidden unless they block progress or create risk.

At the end of **every repository-work conversation** (including read-only review, completed implementation, validation, or a blocked/paused work unit), perform a lightweight **read-only** live Issue/PR census for the current palace worker, Knowledge Core, and Product. Check accepted `main` where a delivery claim depends on it. Report all three in Chinese even though this turn executes in exactly one lane. Do not open an Issue, change another lane, rerun its tests, or consume an unmerged artifact merely to prepare the report. Live Issue/PR and accepted `main` outrank a stale state cache; if a live check fails, mark that lane **未核实** with the reason and do not recommend a dependent activation as if it were verified.

Batch this census where supported and include its observation time. For each stream, distinguish **occupied/runnable**, **occupied/waiting**, **free/no admitted task** and **unverified**, alongside its Issue/PR, next independent action, blocker and PI gate. Preserve Core WIP 1, Product WIP 1 and the PI's one-palace-at-a-time schedule within the existing palace caps; Governance remains its own one-unit write lane. Respect registered path ownership and cross-lane handoffs. Independent preparation may overlap in separate chats; canonical integration remains serial through the Integration Lease in Issue #888, ordered by dependencies and validated readiness rather than a fixed Palace -> Core -> Product cycle. Report at most one next integration candidate and its remaining gate. A status report does not launch another task or authorize unmerged Knowledge consumption.

Default report order:

【整个项目现在到哪了】
- State the current macro stage in plain Chinese.
- Explain how the current work fits into the full path: knowledge construction -> faithful inference -> empirical validation -> personalization/productization.
- State what has already become stable and what is still only preparatory.

【宫位、Knowledge Core、Product 当前状态】
- For each of the three, name the live bounded Issue/PR or say there is no verified ACTIVE unit; distinguish ACTIVE, waiting, ready, and accepted-on-main outcomes. For the palace line, name the currently admitted palace and respect the PI's one-palace-at-a-time schedule.
- In one short line per work stream, state what it can independently continue, what exact input/gate blocks its next step, and whether PI judgment is pending. A candidate ledger or green unmerged PR is not an accepted Product input.

【这一步刚刚完成了什么】
- Explain the substantive result, not commit/branch details.
- Distinguish clearly between "framework/interface ready", "knowledge/content ready", "internally validated", and "empirically validated".

【下一步准备做什么】
- Give adaptive advice: continue the selected work when runnable, switch attention to a different independently runnable work stream when blocked, and name at most **one** next integration candidate with its remaining exact-main gate. Do not call it merge-ready before validation. Independent preparation may overlap; canonical merges remain serial.
- Name the next 1–2 substantive tasks and why they are next, without restarting an existing work unit or exceeding its lane/shard WIP limit.
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
- they are the compact live work-unit references needed for the mandatory three-stream snapshot;
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


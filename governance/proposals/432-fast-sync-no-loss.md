# G11 — bounded execution, validation reuse and recoverable handoff v1.1

## Status / Tracking Issue

- Tracking Issue: [#432](https://github.com/15937-ass/ziwei-state-space/issues/432); implementation PR: [#434](https://github.com/15937-ass/ziwei-state-space/pull/434).
- Status: IMPLEMENTING — PI-authorized workflow optimization; effective only after accepted merge. Live Issue/PR determines completion, never this historical status alone.
- Lane: GOVERNANCE_ONLY; risk R2. No canonical semantic or R3 decision is included.

## Motivation

Repeatedly loading unchanged files, rebuilding prior context and polling identical CI state delays bounded work. Preserve the same evidence and acceptance standards while doing useful reasoning between recovery boundaries.

## Goals

- Batch independent task-required reads; inspect changes before reloading full artifacts.
- Reuse successful, version-matched validation evidence without duplicating reports or identical runs.
- Inspect source, counts and temporal scope together with separate auditable verdicts.
- Resume from a compact durable checkpoint; show the PI which independent stream can continue.

## Non-Goals

- No new task/status authority, autonomous scheduler, distributed lock, cache service or workflow trigger.
- No changed source truth, ontology, Product runtime/lock, probability, empirical claim, WIP cap, palace sequence or Human Gate.
- No guarantee of measured speed/cost reduction before execution data exists; no exemption from full mandatory validation.

## Current Problem

The old #434 contains a useful fast path but predates current recovery, shard and three-stream reporting contracts. Its old state-file edit would revive an obsolete active pointer. Reconstitute the existing branch with current main as an ancestor, retain its old commits and preserve current Governance state. Do not replay its old file versions over current main.

## Proposed Design

### 1. One bounded context

Follow the canonical bootstrap once, confirm the active Issue/PR and establish lane/shard, claimant, write set, branch/head, main/base and relevant input versions. Batch independent reads; perform dependent operations sequentially and inspect every result. Unchanged material stays in the temporary working context. GitHub execution truth and accepted main remain authoritative.

Known/suspected external updates, session/task changes, version mismatch, ambiguous writes, relevant runtime failure, hard checkpoints and pre-merge acceptance force resynchronization. Use optimistic concurrency for writes and verify an ambiguous outcome before retrying. Preserve unreconstructable work before any synchronization; never reset or force-overwrite someone else's newer work.

### 2. Evidence identity and invalidation

The durable validation identity is the tuple of exact base/main and head, relevant input/source/lock versions, commands/check scope, workflow/config/dependency/runtime versions and run attempt. Reuse only completed successful required evidence with that identity. A checkpoint freshness read is not an instruction to rerun an already matching successful suite. Changed identity, failed/unknown results or additional required scope needs appropriate new validation under the existing full-gate policy. Preserve failed attempts as evidence.

Keep source-level evidence distinct from integrated PR acceptance: byte-identical source evidence can survive a mainline update, while a changed base still requires safe synchronization and a fresh exact-base/head acceptance gate. Poll pending CI at meaningful boundaries, save the run reference and record its terminal result once.

### 3. One audit pass, separate judgments

For the current bounded batch, check source/span/condition fidelity, ID/count reconciliation and time-layer preservation together. Record three distinct results with evidence and unresolved items. A count match cannot establish source fidelity; a source match cannot establish time correctness; green structural checks cannot establish empirical validity. Keep ~50-item reasoning sub-batches and <=100-item durable integration unless separately approved.

### 4. Existing slots, explicit ownership and serial integration

The PI-facing streams remain palace knowledge, Knowledge Core and Product. Palace/Core are Knowledge shards, not newly invented top-level lanes. Keep Core <=1, Product <=1, Governance <=1 and the existing palace caps plus PI one-palace-at-a-time admission. Each executing chat selects one bounded work unit and its registered write set. Reuse an existing active task rather than opening a duplicate.

Before claiming or resuming work, verify the live task assignment; record the claimant/session reference and explicit handoff in the Issue/PR. This is cooperative ownership, not an atomic distributed lock. If another worker already owns the task or ownership is ambiguous, do not write in parallel on that task. Use an available independent admitted task or wait for handoff. A free slot does not make a blocked backlog task runnable.

Preparation may proceed concurrently in disjoint work units. Only one canonical integration proceeds at a time, with a final current-main/head and required-check readback. Order integration by accepted dependencies and readiness, not a permanent Palace/Core/Product ordering. If another merge wins the race, synchronize and revalidate; retain the work. Product consumes only separately accepted and authorized Knowledge contracts.

### 5. Durable checkpoint and PI report

Use the compact payload in AGENT_WORKFLOW.md §10.3 in the existing Issue/PR, linking versioned artifacts and validation evidence. Record completion range, next exact source anchor, unresolved findings, material rationale, claimant/write set, version identities, blockers and producer/consumer unblock condition. Update stale resume pointers without deleting historical evidence. Chat-only summaries are insufficient.

On resume, perform mandatory recovery, compare live versions/ownership to the checkpoint and read the changed/missing material. At closeout, batch a lightweight live census and tell the PI each stream's occupied/runnable, occupied/waiting, free/no admitted task or unverified status, next independent action and PI gate. Do not rerun another lane's checks for a report. Give one priority recommendation and at most one integration candidate with remaining gates; do not automatically activate it.

### Worked decisions

| Situation | Required behavior |
| --- | --- |
| Same session/task; already read file has the same version | Continue from context; avoid another full read merely for reassurance. |
| A version changed | Read changed paths/summary first; reload affected content and dependencies. |
| A summary omits an original prerequisite or a source-page boundary is disputed | Inspect the original source and record the unresolved/corrected finding. |
| Same base/head/inputs/environment/check scope; completed required checks PASS | Reference the existing evidence after live freshness checks; no identical suite solely for another report. |
| Main advanced, even if accepted source blobs are unchanged | Preserve source evidence, synchronize the branch, run the required fresh integrated gate. |
| Write response timed out | Verify target blob/ref or existing comment before retrying; never assume failure. |
| New chat has a detailed checkpoint | Perform bootstrap/live recovery, verify assignment/versions, then load delta; never trust the checkpoint as current authority. |
| Another chat is already executing that same Issue | Wait for explicit handoff or choose independent admitted work; do not duplicate it. |
| Core waits for PI while palace work is runnable | Report that split; palace can continue within its own task, without approving Core implicitly. |
| Product slot is free but its next KIB input is not accepted | Report free plus dependency; do not manufacture runnable work or consume a draft. |

## Alternatives

- Reload everything for every substep: recoverable but redundant and context-heavy.
- Trust a chat summary or head SHA alone: fails on stale baseline, changed inputs and ownership.
- Build a new scheduler/cache service: unnecessary for this bounded workflow correction.
- Selected: small additions to canonical workflow/bootstrap plus this conditional reference.

## Compatibility

Reuse current authority, bootstrap order, cross-lane handoff, lane/shard ownership and §13 Chinese reporting. No new required check, runner permission, automatic push trigger, second active Governance unit or global serialization of independent preparation is introduced.

## Knowledge Impact

Source-review standards, school boundaries, UNKNOWN/conflict states, source span inspection and item limits remain controlling. Accepted source evidence can be referenced by immutable identity; candidate ledgers and green unmerged PRs remain non-production inputs.

## Product Impact

No Product artifact or behavior changes. Knowledge promotion, locked dependencies and separate Product acceptance are unchanged. A released Product slot is not proof that a dependency is ready.

## Risks and Failure Modes

- Stale summary treated as live state: mandatory bootstrap/freshness reads and invalidation rules.
- Successful head check reused against a different main/input/runtime: require complete validation identity and preserve exact-main integration.
- Combined audit hides a failure: separate provenance/count/time verdicts and blockers.
- Two chats claim one task: explicit claimant/handoff, no writes on ambiguous ownership; no atomic-lock claim.
- Optimization becomes another large mandatory prompt: operational rules stay in workflow; examples/proposal load only when needed.

## Test Plan

- Inspect the final diff against current accepted main: only the three authorized Governance documentation paths change; current state cache and all other paths match main.
- Review worked decisions for stale base, source wording, ambiguous write, ownership collision and blocked free slot; check bootstrap and current reporting remain intact.
- Run full repository pytest, Product JS syntax, deterministic P0 audit and Governance validation on the final PR base/head using the current execution protocol.
- Record actual commands, runtime, counts, run references and reviewer/critic identity or limitations in PR #434. Do not claim external/independent reviewer approval without evidence.

## Migration Plan

1. Activate existing #432 after live Governance slot recovery; retain #434 and its history.
2. Merge current main into its branch; resolve the obsolete Governance-state edit to current main, preserving later accepted state.
3. Extend the fast path with this bounded policy and a short bootstrap pointer; validate and review.
4. Accept only with current-base/head evidence and applicable review requirements; release the slot on completion. No next Issue is auto-activated.

## Rollback Plan

Revert the narrow accepted documentation change in a bounded Governance PR if it causes ambiguity. Preserve Issue/PR history and validation evidence; no Product/Knowledge rollback is needed because those artifacts are unchanged.

## Graduation Criteria

- Canonical workflow has batch/delta loading, invalidation, validation identity, combined audit and compact checkpoint instructions.
- A new chat can locate the checkpoint and resume after live recovery without redoing completed background work.
- Three-stream reports distinguish availability, dependencies and PI gates; independent preparation and serial integration remain compatible.
- Required deterministic gates and applicable review requirements are satisfied on current base/head; implementation completion is recorded in live Issue/PR.

## Human Gate

PI approved the no-information-loss optimization on 2026-10-20 and authorized this concrete continuation on 2026-10-23 (“可以的，就这么做”). This authorizes the bounded Governance work, not ontology values, source interpretations or Product promotion. Existing R3 gates remain in force.

## Decision

Implement the workflow optimization within existing contracts. No new authority or semantic contract is introduced. Completion and release require live PR acceptance; this document alone cannot certify them.

## Implementation History

- 2026-10-20: original #432/#434 fast-path proposal/implementation prepared.
- 2026-10-23: resumed against accepted main cdc4fce773ea5133f2210c6ea8e87022678fff2f; retain old branch history, reconcile obsolete state edit and extend version-bound reuse/handoff under explicit PI instruction.

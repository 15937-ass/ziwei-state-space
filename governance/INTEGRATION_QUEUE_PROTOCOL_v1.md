# Integration Queue Protocol v1

Status: **APPROVED / ACTIVATES ON MERGE OF GOVERNANCE #890**  
Proposal: `governance/proposals/890-parallel-work-serial-integration-v1.md`  
Coordination ledger: GitHub Issue #888 (**NOT A WORK UNIT**)  
Scope: all Product, Knowledge, and Governance PRs that intend to change `main`.

## 1. Principle

The repository uses **parallel production + serial integration**.

Parallel work is allowed wherever lane/shard ownership and WIP limits allow it. Canonical `main` integration remains one-at-a-time. The serialization point is intentionally late: a work unit should do useful build/research work in parallel, then wait until it owns the Integration Lease before spending the expensive final exact-head validation.

This protocol changes scheduling, not truth or quality standards.

## 2. Lifecycle

### ACTIVE_BUILD

The Issue is the bounded execution truth and the branch is the workspace.

Allowed:
- source review, implementation, critic passes, bounded/local tests, schema checks, write-set checks, and relevant regressions;
- reading accepted `main` and pinned accepted checkpoints;
- recording fail-closed gaps.

Not required:
- rebasing merely because an unrelated lane advanced `main`;
- maintaining a perpetually fresh full-repository gate.

A full gate run during ACTIVE_BUILD is diagnostic evidence only, not merge authorization.

### READY_TO_INTEGRATE

Content and bounded review are complete. The PR posts `QUEUE_READY` to Issue #888 and waits.

READY_TO_INTEGRATE:
- does not hold the Integration Lease;
- does not authorize a merge;
- may remain based on an older accepted `main`;
- may continue non-semantic cleanup if that does not invalidate readiness, but material scope changes return it to ACTIVE_BUILD.

### INTEGRATING

Only the sole Integration Lease holder may enter this state.

The holder must:
1. re-read #888 and confirm it is the winning/active lease holder;
2. fetch current `main`;
3. synchronize/rebuild/rebase the PR exactly once to that current accepted head;
4. run the work unit's required final exact-head full gate;
5. confirm the tested head/base still match the intended merge;
6. merge immediately if green;
7. record the new `main` SHA and release the lease.

While a lease is held, other lanes continue ACTIVE_BUILD/READY work but must not merge `main`.

### MERGED / RELEASED

The PR is merged, its Issue may close, and the lease is released. Lane state files are recovery caches only; live Issue/PR and #888 coordination records outrank stale cache text.

## 3. Integration Lease ledger

Issue #888 is append-only coordination state and consumes no Product, Knowledge, or Governance WIP slot.

Standard comment verbs:

`QUEUE_READY issue=<n> pr=<n> lane=<lane> risk=<R0-R3> ready_main=<sha> blockers=<none|refs>`

`LEASE_ACQUIRE issue=<n> pr=<n> generation=<g> observed_main=<sha>`

`LEASE_RELEASE issue=<n> pr=<n> generation=<g+1> merged_main=<sha>`

`LEASE_ABORT issue=<n> pr=<n> generation=<g> reason=<text>`

Initial generation is 0.

An acquirer must post `LEASE_ACQUIRE` and then re-fetch #888 before running the final full gate. If multiple acquisition comments claim the same previously free generation, the lowest GitHub comment ID wins. Losers post no final acceptance claim and return to READY_TO_INTEGRATE.

A release advances the generation by one. An abort does not advance it unless a merge actually changed `main`.

## 4. Queue priority

Among eligible READY units:
1. first, a unit whose merge releases an explicitly recorded D3 hard blocker for another active lane;
2. otherwise, a bounded lower-risk/smaller integration unit;
3. otherwise, FIFO by the first valid `QUEUE_READY` comment.

Priority is scheduling policy, not semantic authority. A Human Gate or failed acceptance always overrides queue position.

## 5. Validation timing

### Build validation

Use fast, relevant checks while developing:
- unit/module tests;
- source/schema validation;
- path/write-set checks;
- targeted regressions;
- critic/reviewer checks required by the Issue.

These tests should be rerun when the work itself changes. They do not need to be invalidated merely because an unrelated disjoint lane changed `main`.

### Final exact-head validation

Only the Integration Lease holder runs the final acceptance gate intended to authorize immediate merge.

The final gate remains exactly as strict as before. If `main` changes after synchronization and before merge, the run is stale and must not be reused.

The optimization is **run the expensive final gate later and once**, not weaken it.

## 6. Cross-lane checkpoint rule

No lane consumes another lane's unmerged branch as canonical truth.

- D0: independent; no dependency.
- D1: frozen-read; consume an accepted pinned `main` checkpoint while upstream continues new work.
- D2: integration-sensitive; development is independent, but both eventually serialize through the lease.
- D3: hard dependency; downstream cannot correctly continue until a new upstream artifact is accepted.

Prefer D0–D2. A D3 dependency must be explicit in the Issue.

Product Knowledge consumption continues to use its existing lock/candidate/impact/promotion controls. A newly accepted Core artifact does not silently mutate Product.

## 7. Gap handling

A palace that finds a shared semantic gap records `KNOWLEDGE_CORE_GAP`, preserves UNKNOWN/conflict, and continues fail-closed whenever possible.

Product that cannot represent accepted Knowledge records either:
- a Product-owned adapter/interface gap; or
- a Core semantic gap if Knowledge itself is under-specified.

A gap blocks unrelated work only when the Issue explicitly classifies it as D3.

## 8. WIP and operating target

Hard limits remain:
- Product active WIP <= 1;
- Knowledge Core active WIP <= 1;
- per-palace active WIP <= 1;
- total palace ceiling unchanged by this protocol;
- final INTEGRATING work units globally <= 1.

Normal steady-state target: **one palace + one Core + one Product** in productive work. Additional palace workers are an acceleration mode, not a utilization target.

## 9. In-flight migration

At activation, Product #882/#883 and P02 #885 are grandfathered as existing work ownership. This protocol does not steal their lane slots or reinterpret old validation as current acceptance.

A final gate that began before activation is not automatically promoted into a lease-protected run. If its base is stale, it remains stale under the old and new rules alike.

## 10. Recovery

Before final integration:
1. recover the lane from PROJECT_STATE / lane state / live Issue / PR;
2. read this protocol;
3. read Issue #888;
4. determine whether the PR is ACTIVE_BUILD, READY_TO_INTEGRATE, or INTEGRATING;
5. never infer lease ownership from chat memory.

## 11. Future native merge queue

A repository-native GitHub Merge Queue may later replace #888 if admin controls and project workflow justify it. Enabling it requires a separate Governance/admin decision. Until then, #888 is the coordination ledger.

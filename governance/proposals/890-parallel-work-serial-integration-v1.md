# Proposal #890 — Parallel Work + Serial Integration Queue v1

Status: **IMPLEMENTING — PI APPROVED**  
Tracking Issue: #890  
Implementation PR: #891  
Coordination ledger: #888  
PI decision date: 2026-10-29

## Status / Tracking Issue

Proposal ID and implementation tracker: GitHub Issue #890.  
Current proposal state: **IMPLEMENTING**.  
The design was explicitly approved by the PI before repository implementation began. PR #891 implements this approved scope.

## Motivation

The repository already permits parallel Product, Knowledge Core, and palace work, but final acceptance has been coupled too tightly to a moving `main`. Recent work demonstrated validation churn: a branch can complete a full repository gate, another disjoint lane advances `main`, and the first branch must synchronize and repeat the same expensive final gate. This wastes validation time without improving semantic isolation.

The design goal is not more simultaneous writers to the same shard. It is to separate **parallel production** from **serialized canonical integration**.

## Goals

- Introduce the lifecycle `ACTIVE_BUILD -> READY_TO_INTEGRATE -> INTEGRATING -> MERGED/RELEASED`.
- Preserve one Product work unit, one Core work unit, and one work unit per palace; do not change the hard palace ceiling.
- Make one active palace + one Core + one Product the normal operating target.
- Delay the final exact-head full repository gate until a work unit owns the global Integration Lease.
- Keep build/research work running while another lane integrates.
- Require cross-lane consumers to use accepted, pinned checkpoints rather than unmerged branches.
- Make semantic/interface gaps asynchronous and fail-closed unless explicitly classified as a hard dependency.
- Preserve all existing source, semantic, Human Gate, CI, lane ownership, and final exact-head acceptance standards.

## Non-Goals

- No Product, KIB, runtime, Knowledge rule, ontology, mapping, or source-semantic change.
- No increase to Product/Core WIP.
- No automatic push workflow.
- No new required human reviewer.
- No repository-admin or branch-protection change.
- No requirement to enable GitHub native Merge Queue.
- No permission to reuse a final gate after `main` changed.

## Current Problem

The current process serializes too early in practice. Work can be developed independently, but teams often run a full repository gate before they actually own the next merge. If another PR advances `main` while that gate is running, the result becomes stale and the expensive gate must be repeated.

During implementation of this proposal the same failure mode reproduced live: Product #883 synchronized to main `1b6be411...` and started its final quality gate; P02 #885 / PR #886 then merged to `051ad822...` before that Product gate completed. The Product gate therefore became stale for merge even though the two changes were write-isolated. This is validation churn, not semantic conflict.

## Proposed Design

Two clocks govern repository work.

**Work clock:** authorized lanes operate independently in `ACTIVE_BUILD`, using bounded/local tests and their existing path ownership. A completed unit becomes `READY_TO_INTEGRATE` and posts a queue record to coordination Issue #888.

**Integration clock:** only one queued PR receives the global Integration Lease. The holder enters `INTEGRATING`, synchronizes once to current `main`, runs the required full exact-head acceptance gate, merges immediately if green, records the resulting `main` SHA, and releases the lease. Other lanes continue build/research but do not merge while the lease is held.

Issue #888 is coordination-only and consumes no lane WIP. Queue priority is: (1) a unit that releases a recorded hard blocker for another active lane; (2) otherwise a bounded lower-risk/smaller unit; (3) otherwise FIFO by READY record.

Cross-lane dependency classes are:
- D0 independent;
- D1 frozen-read from accepted pinned `main`;
- D2 integration-sensitive but build-independent;
- D3 hard dependency requiring a new accepted upstream artifact.

The project should keep normal work in D0–D2 whenever possible. D3 must be explicit.

## Alternatives

1. **Fully serial project execution.** Rejected because it removes validation churn by idling independent Product/Core/palace work and reduces throughput.
2. **Every lane continuously rebases to latest main.** Rejected because it preserves the current churn and causes repeated full-gate work.
3. **Allow parallel merges with no serialization.** Rejected because exact-head acceptance can race and canonical `main` loses a single integration order.
4. **Enable GitHub native Merge Queue immediately.** Deferred. It may be a better future implementation but requires admin/settings work and is unnecessary for the current single-PI scale.
5. **Shared YAML lock in the repository.** Rejected because acquiring/releasing the lock would itself require changing `main`, creating the synchronization problem it is meant to solve.
6. **Live GitHub Issue coordination ledger.** Selected because it is non-file state, auditable, available to all execution sessions, and does not mutate Product/Knowledge artifacts.

## Compatibility

The change is backward-compatible with existing lane ownership, branch naming, WIP limits, CI commands, and exact-head acceptance. Existing in-flight Product #882/#883 and P02 #885 retain their ownership and are not retroactively reclassified as having obtained a lease.

The protocol changes when the final full gate is run, not what that gate must prove. Historical accepted PRs remain valid under their original recorded validation.

## Knowledge Impact

No canonical Knowledge content changes. Core and palace ownership remain unchanged. Palace workers still fail closed on shared semantic gaps; Core remains the sole owner of shared semantics.

Knowledge gains scheduling decoupling: source review and Core research may continue while another lane integrates, and a Knowledge PR does not need to chase unrelated `main` movement until it receives the Integration Lease.

## Product Impact

No Product runtime, KIB, adapter, registry, reader, or semantic artifact changes. Product continues to consume Knowledge through accepted pinned checkpoints and its existing lock/candidate/impact/promotion controls.

Product gains the same scheduling decoupling: an active Product work unit may build against its pinned accepted inputs while Core/palace work proceeds, then synchronize once when it actually owns final integration.

## Risks and Failure Modes

- **Lease race:** two sessions may try to integrate. Mitigation: append-only acquisition records in #888; contenders re-read after posting, and if two acquisitions claim the same free generation the lower GitHub comment ID wins.
- **Stale full gate:** `main` changes after synchronization. Mitigation: the run is stale and must be repeated; the lease should prevent routine occurrences.
- **Queue starvation:** a large unit waits behind small work. Mitigation: hard-blocker priority first, then bounded smaller/lower-risk work, then FIFO; long waits should be surfaced to PI rather than silently reordered forever.
- **Too much WIP:** the hard palace ceiling could overload the queue. Mitigation: normal target is one palace + one Core + one Product; extra palace workers are acceleration mode only.
- **Coordination issue mistaken for Governance WIP:** #888 explicitly states NOT A WORK UNIT.
- **False optimization:** targeted build tests might be mistaken for final acceptance. Mitigation: only an INTEGRATING exact-head full gate authorizes merge.

## Test Plan

- Governance validator requires the integration protocol and PROJECT_STATE pointers.
- Deterministic test checks lifecycle markers, Issue #888, and unchanged Knowledge hard WIP limits.
- Full repository pytest.
- P0 audit.
- Governance lane/write-set validation.
- Product regression workflows run only according to their existing path filters; no Product semantic artifact changes.

## Migration Plan

- Existing in-flight Product #882/#883 and P02 #885 keep ownership and are treated as grandfathered build work.
- The protocol becomes authoritative only after its Governance PR merges.
- No in-flight branch is automatically rebased merely because the protocol is proposed.
- The first post-activation final integrator records queue/lease state in #888.
- Existing stale lane-state caches are still subordinate to live Issue/PR state and may be repaired by their next bounded owner.

## Rollback Plan

Revert the Governance PR and return to the previous serial exact-head practice. Because this proposal delays final validation rather than weakening it, rollback does not require reinterpreting accepted Knowledge or Product semantics. Any PR merged under v1 remains auditable through its exact-head run and GitHub history.

## Graduation Criteria

- Protocol and pointers are on `main`.
- #888 is live as a non-WIP coordination ledger.
- Full repository quality gate and Governance validation pass on the integration head.
- No Product/Knowledge semantic files are modified.
- A future work unit can recover the lifecycle and lease rules without relying on chat memory.

## Human Gate

**APPROVED.** PI explicitly authorized this design on 2026-10-29 after reviewing the parallelism/cardinality analysis: “可以的，就按照你说的改”.

This approval is limited to scheduling/integration governance. It does not authorize Ziwei semantic changes, Product runtime promotion, probability semantics, or new empirical claims.

## Decision

**APPROVED — implement v1 now.** Use parallel build + serialized final integration, with live coordination in Issue #888 and final exact-head acceptance only while holding the Integration Lease.

## Implementation History

- 2026-10-29: PI approved the design in chat.
- 2026-10-29: coordination Issue #888 created; duplicate #889 closed.
- 2026-10-29: implementation Issue #890 and Draft PR #891 created.
- 2026-10-29: protocol, recovery/bootstrap, execution, Knowledge integration, three-stream, Agent workflow, state-cache, validator, and regression-test changes implemented on the Governance branch.
- Final exact-head integration evidence and merge SHA are intentionally not claimed until the PR obtains the integration window and passes the final gate.

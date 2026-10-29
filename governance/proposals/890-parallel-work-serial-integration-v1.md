# Proposal #890 — Parallel Work + Serial Integration Queue v1

Status: **APPROVED BY PI / IMPLEMENTATION AUTHORIZED**  
Tracking Issue: #890  
Coordination ledger: #888  
PI decision date: 2026-10-29

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

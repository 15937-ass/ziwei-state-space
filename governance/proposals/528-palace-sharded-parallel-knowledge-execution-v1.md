# 528 — Palace-Sharded Parallel Knowledge Execution v1

Status: APPROVED
Tracking Issue: #528
Owner Lane: GOVERNANCE_ONLY
Risk: R3

## Motivation

The Knowledge lane has proven a source-first, auditable workflow through the Career Palace program and is now applying that method to other palaces. A single global Knowledge WIP limit serializes work that is naturally separable by palace and prevents independent conversations from safely advancing distinct palace corpora.

The goal is to permit bounded parallel source research without creating multiple competing definitions of Zhongzhou semantics.

## Goals

- Permit up to four simultaneously active palace-scoped Knowledge work units.
- Permit at most one active work unit for any single palace.
- Keep one Knowledge Core work unit as the only writer of shared ontology, shared semantics, shared schemas and cross-palace execution contracts.
- Give each palace an independent recovery pointer/state file.
- Make palace workers write-disjoint by construction.
- Keep live GitHub Issue/PR authority, source-first adjudication, provenance and fail-closed UNKNOWN behavior unchanged.
- Serialize canonical integration to `main`: every Knowledge PR must validate on an up-to-date base/head before merge.

## Non-Goals

- This proposal does not change Zhongzhou source truth or any canonical Ziwei rule.
- It does not authorize more than four palace workers.
- It does not allow two workers to modify the same palace simultaneously.
- It does not let palace workers redefine shared terms such as 会、同会、夹、前格、煞曜、得禄 or shared Response/Relation semantics.
- It does not make chat/session text authoritative.
- It does not change Product knowledge promotion, empirical probability, calibration or runtime semantics.
- It does not authorize parallel merges to main.

## Current Problem

Repository Governance v1 currently states `Knowledge lane: at most 1 ACTIVE work unit`, and `knowledge/KNOWLEDGE_STATE.yaml` has a single active Issue/PR pointer. That was appropriate while the Career Palace method was still being developed, but it now prevents safe horizontal reuse of the mature method.

Running multiple palace conversations under the current contract would cause three classes of risk:

1. shared-state collisions in `KNOWLEDGE_STATE.yaml`;
2. shared-semantic drift when different chats independently normalize the same cross-palace term;
3. merge races where a PR is validated against a stale main.

## Proposed Design

### 1. Execution topology

```text
Knowledge Core (WIP <= 1)
        |
        +-- P01 Life Palace worker
        +-- P02 Siblings Palace worker
        +-- P03 Spouse Palace worker
        +-- P04 Children Palace worker
        +-- P05 Wealth Palace worker
        +-- P06 Health Palace worker
        +-- P07 Migration Palace worker
        +-- P08 Friends Palace worker
        +-- P09 Career Palace worker
        +-- P10 Property Palace worker
        +-- P11 Fortune Palace worker
        +-- P12 Parents Palace worker

Total active palace workers <= 4
Active work units per palace <= 1
```

Palace workers may operate in separate ChatGPT conversations. GitHub artifacts, not chat history, synchronize them.

### 2. Knowledge Core ownership

Only a `CORE` work unit may modify shared semantic contracts, global ontology, common operator definitions, shared schema/governance state, or cross-palace normalization policy.

When a palace worker discovers that the source requires a new shared concept or a change to a shared concept, it must fail closed locally and create a `KNOWLEDGE_CORE_GAP`. It must not silently repair the shared layer.

### 3. Palace-shard ownership

Each palace worker receives:
- a shard ID `P01` … `P12`;
- one live bounded Issue;
- one short-lived shard branch;
- one palace state pointer;
- an exclusive write set.

A palace worker may read all canonical repository content, but may only write its declared palace-scoped artifacts plus its own shard-state file and bounded validation evidence.

### 4. Branch convention

New Knowledge branches use:

```text
knowledge/pXX-<issue>-<slug>
knowledge/core-<issue>-<slug>
```

The already-open Property work unit #525 / branch `knowledge/525-property-tp03-canonical` is explicitly grandfathered until it is merged or closed. No new legacy-form Knowledge branch may be opened after implementation.

### 5. State model

`knowledge/KNOWLEDGE_STATE.yaml` becomes a coordinator/index and no longer acts as the mutable per-palace execution scratchpad.

Per-palace recovery state lives under:

```text
knowledge/states/P01_LIFE_STATE.yaml
...
knowledge/states/P12_PARENTS_STATE.yaml
```

A palace worker updates only its own state file. Core/global registry changes are Core/Governance owned.

Recovery remains:

```text
PROJECT_STATE
-> RECOVERY_PRECEDENCE
-> KNOWLEDGE_STATE coordinator
-> selected palace state
-> live palace Issue
-> linked PR
```

Live Issue/PR remains authoritative over stale state caches.

### 6. Shared semantic gap protocol

A palace worker encountering a cross-palace semantic need records a Core gap containing:
- source palace and rule/span;
- exact unresolved term/relationship;
- why existing shared semantics are insufficient;
- affected local rows;
- whether work can continue fail-closed;
- no proposed universal meaning unless source support exists.

Core resolves these gaps serially through its own Issue/PR and Human Gate where required.

### 7. Canonical merge serialization

Research and PR preparation may run in parallel, but canonical integration is serialized.

Before merge, a Knowledge PR must:
1. be current with the latest `main` or be rebased/updated onto it;
2. run the governed exact-head repository quality gate;
3. pass shard-write validation;
4. preserve any newly introduced Core gaps;
5. be merged one at a time.

A green result obtained before another Knowledge PR changed main is not sufficient if the base is stale.

### 8. Initial concurrency bound

Version 1 authorizes:
- Knowledge Core active WIP <= 1;
- total palace workers active WIP <= 4;
- per-palace active WIP <= 1.

Increasing the palace-worker cap requires a new Governance decision.

## Alternatives Considered

1. **Keep global WIP=1.** Safest but wastes the now-repeatable palace workflow and makes twelve-palace completion unnecessarily slow.
2. **Unlimited palace workers.** Rejected because source/semantic integration and merge churn could exceed practical review capacity.
3. **Allow each palace to maintain its own semantics.** Rejected because it would create incompatible Zhongzhou dialects inside one canonical KB.
4. **Parallel branches with no shard validator.** Rejected because social convention alone is too weak for multi-chat operation.

## Compatibility

- Existing accepted `main` artifacts remain canonical.
- Existing Career and Property artifacts are not relocated as part of this governance change.
- Issue #525 is grandfathered so the new branch rule does not invalidate in-flight Property work.
- Product knowledge locks/promotions remain unchanged.
- Legacy archived twelve-palace material remains noncanonical candidate material.

## Knowledge Impact

No Ziwei semantic content changes. The proposal changes only how independent palace research is scheduled, recovered, validated and integrated.

## Product Impact

None directly. Product continues to consume explicitly promoted, immutable Knowledge baselines under the existing Product/Knowledge dependency contract.

## Risks and Failure Modes

- **Cross-palace semantic drift:** mitigated by Core-only shared semantics and Core gaps.
- **State-file merge conflicts:** mitigated by per-palace state files and a coordinator state.
- **Two workers on one palace:** prohibited; live Issue census and validation must detect this.
- **Stale-base merge:** prohibited by exact-head validation against latest main.
- **Path leakage:** mitigated by shard-aware governance validation.
- **Too much concurrency:** bounded at four palace workers.
- **Hidden dependency between palaces:** worker must reference canonical dependency or fail closed; it may not assume another unmerged branch.

## Test Plan

Implementation must add deterministic governance tests covering:
- branch parsing for `knowledge/pXX-...` and `knowledge/core-...`;
- rejection of unknown palace IDs;
- rejection of palace-worker writes to shared/Core paths;
- acceptance of palace-local paths and own state file;
- rejection of cross-palace state writes;
- grandfathering of the exact #525 legacy branch only;
- coordinator/per-palace state presence and recovery contract.

Repository-wide pytest, P0 audit and Governance validation must pass on the exact PR head.

## Migration Plan

1. Record this approved proposal and PI decision.
2. Open a separate Governance implementation Issue.
3. Add the shard execution contract and shard registry.
4. Add per-palace state files and convert the coordinator state contract.
5. Extend deterministic Governance validation.
6. Amend Governance WIP/recovery rules and Knowledge roadmap wording.
7. Keep #525 grandfathered through closure.
8. After merge, new palace work uses shard branches and per-palace state.

## Rollback Plan

If shard execution creates unacceptable conflicts:
- set palace active WIP cap back to 1;
- retain per-palace state files as read-only history;
- disable shard branch creation in the governance contract;
- no canonical Knowledge content needs rollback because this proposal does not alter source truth.

## Graduation Criteria

- governance documents encode Core + palace WIP rules;
- per-palace state/recovery pointers exist;
- shard path validator is deterministic and tested;
- #525 legacy work remains valid;
- exact-head CI passes;
- implementation Issue/PR merges to main;
- a new conversation can recover a selected palace without depending on another palace chat.

## Human Gate

**APPROVED.** PI approved this bounded design in chat on 2026-10-21 after explicitly asking to modify the architecture for multi-chat palace research.

The approved bounds are: one Core writer, up to four distinct palace workers, one worker per palace, shared semantics Core-only, and serialized canonical merge.

## Decision

APPROVED for implementation. This is a governance/execution architecture decision only; it does not authorize changes to Zhongzhou source truth or empirical semantics.

## Implementation History

- 2026-10-21: Proposal Issue #528 opened after PI approval.
- Implementation work unit: pending separate Governance Issue.

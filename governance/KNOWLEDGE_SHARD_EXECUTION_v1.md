# Knowledge Palace-Shard Execution Contract v1.0

Status: **ACTIVE AFTER G12 MERGE**  
Controlling Proposal: #528  
Implementation Issue: #530  
Scope: KNOWLEDGE_ONLY scheduling, recovery, write isolation, and canonical integration.

## 1. Topology

Knowledge execution is split into one shared Core plus twelve palace shards.

- Knowledge Core active WIP: **<= 1**
- Total active palace workers: **<= 4**
- Active work units per palace: **<= 1**
- Research/PR preparation may run in parallel across distinct palaces.
- Canonical merge to `main` is serialized through the repository Integration Lease in `governance/INTEGRATION_QUEUE_PROTOCOL_v1.md`.

The PI-selected twelve-palace source-audit sequence is recorded in
`governance/PALACE_AUDIT_SEQUENCE_2026-10-23.md`. During that schedule, admit
only one ACTIVE palace audit/mapping unit at a time. This operating choice is
stricter than, and does not alter, the G12 hard ceilings above. At cutover,
finish the already ACTIVE P09 #673 source-candidate-index unit before starting
P01; use live Issues/PRs rather than this document to confirm its status.

A separate ChatGPT conversation may own one palace shard. Chat history is never synchronization state; GitHub Issue/PR + shard state are.

## 2. Shards

`P01` 命宫  
`P02` 兄弟宫  
`P03` 夫妻宫  
`P04` 子女宫  
`P05` 财帛宫  
`P06` 疾厄宫  
`P07` 迁移宫  
`P08` 交友宫  
`P09` 事业宫  
`P10` 田宅宫  
`P11` 福德宫  
`P12` 父母宫

Machine-readable ownership lives in `governance/KNOWLEDGE_SHARDS.json`.

## 3. Branch identity

New branches MUST use exactly one of:

```text
knowledge/pXX-<issue>-<slug>
knowledge/core-<issue>-<slug>
```

where `XX` is 01..12.

Issue #525 / branch `knowledge/525-property-tp03-canonical` merged before G12 final integration. Its temporary grandfather window is therefore **expired**. The active registry contains no legacy branch exemption, and no new legacy-form Knowledge branch is authorized.

## 4. Write isolation

A palace worker may read the whole repository but may write only:
- its machine-declared palace artifact roots;
- its own palace state file;
- its palace-local validation/test roots.

It may not write:
- `knowledge/KNOWLEDGE_STATE.yaml`;
- another palace's state/artifacts;
- Governance files;
- Product files;
- shared Core semantics/ontology/contracts.

The deterministic Governance validator enforces these boundaries.

## 5. Knowledge Core

Core is the only Knowledge execution shard allowed to create or revise shared semantic contracts.

Examples:
- shared relation semantics;
- shared response semantics;
- universal group/category definitions;
- cross-palace ontology;
- common operator/schema definitions.

A palace worker that discovers a shared semantic gap MUST fail closed locally and record a `KNOWLEDGE_CORE_GAP`; it must not invent or silently generalize a universal rule.

## 6. Core-gap minimum record

A Core gap records:
- source palace/shard;
- source rule/span;
- unresolved shared term or relation;
- why current shared semantics are insufficient;
- affected local rule IDs;
- whether local work can continue fail-closed;
- Human Gate classification if the proposed resolution would alter a primitive/shared semantic family.

The gap may be stored palace-locally until a Core Issue adopts it.

## 7. State and recovery

`knowledge/KNOWLEDGE_STATE.yaml` is a coordinator/index, not a palace workspace.

Per-palace state:
`knowledge/states/PXX_<NAME>_STATE.yaml`

Core state:
`knowledge/states/CORE_STATE.yaml`

Recovery for a palace chat:

```text
PROJECT_STATE.yaml
-> RECOVERY_PRECEDENCE_v1.md
-> knowledge/KNOWLEDGE_STATE.yaml
-> selected palace state
-> live Issue for that palace
-> linked PR
-> Issue-required artifacts
```

Live Issue/PR always overrides stale cache fields.

## 8. Parallelism census

Before opening a new palace work unit:
1. query live KNOWLEDGE_ONLY Issues;
2. identify shard identity from the Issue body/branch;
3. reject if the same palace already has an active work unit;
4. reject if four distinct palace workers are already active;
5. Core WIP is counted separately and is limited to one.

Backlog/READY items do not count as active until explicitly promoted.

## 9. Canonical integration

Parallel research does not imply parallel canonical merge. Knowledge follows the repository-wide `governance/INTEGRATION_QUEUE_PROTOCOL_v1.md`.

During `ACTIVE_BUILD`, a shard may continue source work and bounded validation without rebasing solely because an unrelated lane advanced `main`. When the Knowledge PR is content-complete, it records `READY_TO_INTEGRATE` in Issue #888.

Before a Knowledge PR merges:
1. it must acquire the sole Integration Lease and enter `INTEGRATING`;
2. only then synchronize to the latest `main`;
3. run shard/write-set validation plus the full exact-head gate on that synchronized head;
4. unresolved Core gaps must remain explicit;
5. merge immediately after the green exact-head gate while still holding the lease;
6. record the merged main SHA and release the lease.

A stale green check is never sufficient after `main` changes. The optimization is to delay the final full gate until integration ownership, not to weaken it.

## 10. Cross-palace dependencies

A palace worker may depend only on:
- canonical `main` artifacts; or
- explicitly unresolved references recorded as such.

It may not consume another unmerged palace branch as canonical truth.

## 11. Source integrity

Parallelism changes scheduling only. It does not weaken:
- source-first re-adjudication;
- provenance;
- EXPLICIT/INFERRED/HYPOTHESIS separation;
- no invented numeric weights/probabilities;
- conflict/UNKNOWN preservation;
- Product/Knowledge separation.

## 12. Concurrency changes

The cap of four palace workers is frozen by Proposal #528. Increasing it requires a new Governance decision.

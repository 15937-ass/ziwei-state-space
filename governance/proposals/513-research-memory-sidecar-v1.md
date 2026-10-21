# Proposal #513 — Research Memory Sidecar v1

Status: **APPROVED — DESIGN ONLY; IMPLEMENTATION NOT YET STARTED**
Tracking Issue: #513
Lane: GOVERNANCE_ONLY
PI decision: approved in chat on 2026-10-21 ("可以的，就这么干")

## Motivation

The project now produces research-relevant results faster than a single manuscript can absorb them. Product and Knowledge generate source-closure findings, negative results, representation discoveries, new executable capabilities, benchmark evidence, theory changes and epistemic limitations. Reconstructing these only after V1 would lose contemporaneous rationale.

The record system must preserve research memory without becoming a dependency of Product or Knowledge execution.

## Design references

V1 combines selected ideas from mature practices:
- Architecture Decision Records: context, alternatives, decision, consequences, supersession.
- Electronic Lab Notebooks: contemporaneous rationale, method, observation/result, interpretation and major conclusion.
- W3C PROV: entity/activity/agent provenance.
- RO-Crate: future publication/research-object export.
- ML experiment tracking: run/code/data/metric/artifact lineage.
- Preregistration: freeze hypotheses, outcomes, exclusions, analysis plan and success criteria before empirical tests.
- Model Cards / Datasheets: intended use, scope, provenance, performance and limitations.
- Event Sourcing / CQRS: append-only events plus rebuildable derived views.

The project will use these ideas selectively. It will not convert the main codebase into an event-sourced application.

## Goals

Research Memory Sidecar v1 SHALL provide:
1. append-only Research Event Ledger;
2. multi-axis Claim Registry;
3. Theory Evolution Ledger;
4. Paper / Research Question Map;
5. Evidence Pack contract;
6. Concept Events for important theory ideas not yet represented by repository artifacts;
7. significance policy deciding what deserves immediate capture;
8. provenance links back to accepted repository evidence;
9. replay/checkpoint contract using last_seen_main_sha;
10. explicit correction/supersession semantics.

## Non-Goals

V1 SHALL NOT:
- introduce a fourth authoritative execution lane into ziwei-state-space;
- require Product or Knowledge PRs to wait for research capture;
- add Research checks as required Product/Knowledge CI gates;
- allow Research to modify canonical Zhongzhou knowledge;
- allow Research to modify Product runtime or active Product Knowledge locks;
- auto-rewrite manuscript prose after every PR;
- record every trivial commit;
- promote empirical or causal claims because they are theoretically attractive.

## Proposed Design

### Core architecture

Preferred topology:

    ziwei-state-space
      Product
      Knowledge
      Benchmark
      Governance
            |
            | read-only accepted evidence
            v
    ziwei-research-ledger
      Research Events
      Claims
      Theory Evolution
      Paper Map
      Evidence Packs
      Experiment Records (future)

The sidecar is a derived research-memory system, not a competing source of project truth.

Authority order for facts used by Research Memory:
1. accepted canonical source artifacts / approved Human Gates;
2. merged main repository artifacts;
3. accepted benchmark/validation evidence;
4. merged Issue/PR rationale;
5. explicitly captured Concept Events;
6. Research synthesis.

Research synthesis may organize or interpret evidence, but may not rewrite higher-authority facts.

## Non-Interference Contract

Permanent V1 invariants:
1. Product never waits for Research capture.
2. Knowledge never waits for Research capture.
3. Research capture failure never blocks Product/Knowledge merge.
4. Research jobs are not required status checks for Product/Knowledge.
5. Research has no authority to mutate Product or canonical Knowledge.
6. Research reads accepted main/merged evidence by default.
7. Research may create a gap/candidate note but cannot silently repair another lane.
8. Product/Knowledge have zero runtime or build dependency on Research Memory.
9. Research may lag and catch up by replay.
10. Historical research records are append-only; correction is by supersession.
11. A missing Research record never changes Product/Knowledge semantic status.
12. A Research summary can never upgrade UNKNOWN, SOURCE_UNDERDETERMINED, UNCALIBRATED or equivalent states.

## Event significance policy

### R0 — routine engineering
Examples: typo, test fixture repair, refactor with no semantic change.
Action: no immediate research record.

### R1 — cumulative progress
Examples: another ordinary 50/100-item review batch under an unchanged schema.
Action: accumulate counters; summarize later.

### R2 — major research milestone
Examples: one domain reaches canonical closure; first executable compiler stage; first M0 manifestation slice; benchmark family becomes operational.
Action: create Research Milestone Event.

### R3 — theory / paradigm milestone
Examples: N + E becomes N + E + S + A + C; chart->event is replaced by trajectory/state-space interpretation.
Action: Research Milestone + Theory Evolution Record.

### R4 — empirical finding
Examples: preregistered blind benchmark result, major null result, reproducible incremental signal, calibration failure.
Action: Research Milestone + Claim update + Experiment Evidence Pack.

## Research Event schema

Minimum record:

    id: RM-YYYY-NNN
    event_type: KNOWLEDGE | PRODUCT | METHOD | THEORY | BENCHMARK | EMPIRICAL
    captured_at: ISO-8601
    source_repository:
      repository: 15937-ass/ziwei-state-space
      issue: null
      pr: null
      merge_sha: null
      validation_refs: []
    research_question: ""
    before_state: ""
    result: ""
    key_insights: []
    negative_findings: []
    unexpected_findings: []
    claim_effects:
      supported: []
      weakened: []
      superseded: []
      opened: []
    boundaries:
      source_status: ""
      implementation_status: ""
      internal_fidelity: ""
      empirical_status: ""
      causal_status: ""
    paper_targets: []
    artifacts: []
    supersedes: []
    superseded_by: []

A Research Event records what changed in our understanding, not merely which files changed.

## Claim Registry

Claims use independent axes rather than one maturity score.

Source status:
- EXPLICIT
- TRANSPARENT_INFERENCE
- SOURCE_UNDERDETERMINED
- SOURCE_CONFLICT
- NOT_APPLICABLE

Implementation status:
- NOT_SPECIFIED
- SPECIFIED
- IMPLEMENTED
- DEPRECATED

Internal fidelity:
- UNTESTED
- CONTRACT_PASS
- CASE_RECONSTRUCTION_PASS
- BENCHMARKED

Empirical status:
- UNTESTED
- RETROSPECTIVE
- PROSPECTIVE
- REPLICATED
- NULL_RESULT
- INCONCLUSIVE

Causal status:
- NONE
- ASSOCIATIONAL
- PARTIALLY_IDENTIFIED
- IDENTIFIED

A paper-writing agent must never infer empirical or causal maturity from source fidelity or implementation maturity.

## Theory Evolution Ledger

Theory changes are not ordinary Claim updates.

Each record preserves:
- old model;
- observed limitation;
- new model;
- reason for change;
- which old results remain valid;
- which old claims must be weakened/reinterpreted;
- new research questions.

Records are append-only. Superseded theories remain visible.

## Concept Events

Repository replay cannot capture important conceptual discussions before implementation artifacts exist.

A Concept Event records:
- concept statement;
- mathematical/formal expression if available;
- motivation;
- current epistemic status;
- empirical support level;
- implications;
- explicit note that it is not canonical Zhongzhou truth unless separately source-supported.

Example:

    concept: Destiny is represented as a constrained trajectory space, not a fixed event sequence.
    formalization: S_(t+1)=F(S_t,N,E_t,A_t,C_t)
    status: THEORETICAL_HYPOTHESIS
    empirical_support: NONE

## Paper / Research Question Map

Maintain a many-to-many map:

    research question
    <-> claims
    <-> evidence
    <-> methods
    <-> figures/tables
    <-> limitations
    <-> candidate paper

Initial planning families:
- formalization of historical expert knowledge;
- expert reasoning / method fidelity;
- dynamic state/trajectory model;
- prospective validation of divination;
- general method for computational reconstruction of incomplete historical expert systems.

These are planning buckets, not publication commitments.

## Evidence Pack contract

For any manuscript section or major claim, synthesis should generate a bounded Evidence Pack containing:
- claim IDs;
- supporting Research Events;
- exact repository artifacts;
- benchmark/validation references;
- current limitations;
- conflicting/negative evidence;
- figures/tables that can be generated;
- wording ceiling: what the paper may safely claim.

Evidence Packs are derived views and may be regenerated.

## Historical manuscript policy

paper/manuscript_v0.1.md is a historical manuscript snapshot.

It is not current project memory or execution truth. Future manuscripts are outputs of Research Memory plus accepted repository evidence. Manuscript prose may lag without affecting the project.

## Provenance model

Research Memory uses a minimal PROV-like chain:

    Entity (source artifact/data/model)
      -> Activity (review/compiler/benchmark/analysis)
      -> Entity (result/evidence)
      -> Claim

Every R2-R4 event must contain enough references to recover accepted repository evidence. A numerical result without recoverable evidence is not a valid milestone.

## Rebuildability and checkpoints

Minimum checkpoint:

    source_repository: 15937-ass/ziwei-state-space
    last_seen_main_sha: <sha>
    last_seen_merge_time: <timestamp>
    research_schema_version: 1

Catch-up:
1. read checkpoint;
2. enumerate accepted main history after checkpoint;
3. classify events R0-R4;
4. create missing R2-R4 records;
5. update derived Claim/Theory/Paper views;
6. advance checkpoint only after durable sidecar write.

If the sidecar is unavailable, Product and Knowledge continue normally.

## Correction / supersession

Research records are append-only.

Correction uses:

    RM-OLD
      status: SUPERSEDED
      superseded_by: RM-NEW

The old record remains visible.

Canonical source changes never occur by editing Research records; they require normal Knowledge governance.

## Deferred empirical extension

Before real empirical/calibration work, add:

Experiment / Preregistration Registry:
- hypothesis;
- population;
- variables;
- target/outcome;
- time window;
- exclusions;
- model version;
- Knowledge bundle;
- baseline;
- metric;
- success criterion;
- analysis plan.

Dataset Card:
- motivation;
- composition;
- collection;
- missingness;
- consent/privacy constraints;
- intended/prohibited uses.

Model Card:
- intended use;
- training/calibration lineage;
- benchmark scope;
- performance/calibration;
- limitations;
- prohibited claims.

RO-Crate export is reserved for publication/release packaging only.

## Roles

No separately trained models are required.

Capture role: "What happened?"
- creates/updates Research Events from accepted evidence.

Claim Auditor role: "What are we justified in saying?"
- maintains multi-axis claim state and wording ceilings.

Synthesis role: "How does the evidence form a paper?"
- builds Evidence Packs, paper maps and manuscript drafts.

Synthesis cannot self-promote Claim status.

## Repository topology and technical constraint

Preferred repository:

    15937-ass/ziwei-research-ledger

Suggested layout:

    README.md
    RESEARCH_STATE.yaml
    events/
    claims/
    theory/
    paper_map/
    evidence_packs/
    schemas/
    templates/

The currently exposed GitHub connector can operate on existing repositories but does not expose repository creation.

Therefore:
- this proposal does not block on sidecar repository existence;
- Product/Knowledge gain no dependency on the sidecar;
- bootstrap is a later bounded Governance work unit once a writable target repository exists;
- no substitute research directory is injected into Product or Knowledge paths merely to simulate the sidecar.

## Compatibility

Product:
- no Product file, runtime, test requirement, Knowledge lock or benchmark dependency changes.

Knowledge:
- no canonical source artifact, rule schema or review workflow changes.

Governance:
- current three-lane model remains intact.

## Risks and Failure Modes

Research-log spam:
- mitigated by R0-R4 significance policy.

Research narrative silently becoming truth:
- mitigated by authority hierarchy and multi-axis claims.

Paper pressure contaminating Knowledge:
- mitigated by one-way read relationship and zero mutation authority.

Historical rewriting:
- mitigated by append-only supersession.

False empirical maturity:
- mitigated by empirical/causal axes separated from source/internal fidelity.

Sidecar outages:
- mitigated by eventual consistency and replay.

Over-engineering:
- V1 excludes automated ingestion, preregistry, model/data cards and RO-Crate until needed.

## Alternatives

A. Continuously update manuscript in main repository.
Rejected: creates writing churn and becomes stale.

B. Add RESEARCH_ONLY as a fourth main-repository execution lane.
Rejected for V1: expands main governance and creates unnecessary CI/PR noise.

C. Put research/ in current repository.
Rejected as the primary design: risks making derived research memory look authoritative and increases cross-lane coupling.

D. Keep everything in chat.
Rejected: chat is not durable project state.

E. Independent sidecar repository.
Selected: strongest isolation, replayability and non-interference.

## Test Plan for later implementation

Implementation must demonstrate:
1. Product and Knowledge path ownership unchanged.
2. No Product/Knowledge workflow requires sidecar status.
3. Sidecar unavailable -> main project execution unchanged.
4. Replay from a known main SHA reproduces deterministic event IDs/index.
5. Claim status cannot be empirically upgraded from source/internal fields alone.
6. Superseded record remains retrievable.
7. One Concept Event can be captured without changing main semantics.
8. A generated Evidence Pack links only to accepted evidence.
9. No Research operation modifies Product/Knowledge files.

## Migration Plan

Phase RSM-0 — this proposal:
- freeze design and non-interference boundaries;
- capture a one-time pre-deletion chat-archaeology migration seed under `governance/archive/2026-10-21-pre-delete-chat-archaeology.md`; this file is historical/non-authoritative evidence for later sidecar import, not an ongoing Research substitute inside the main repository.

Phase RSM-1 — sidecar bootstrap:
- create sidecar repository;
- install schemas/templates/state;
- seed a small curated set of historical milestones;
- set last_seen_main_sha.

Phase RSM-2 — bounded catch-up:
- backfill only major R2/R3 milestones, not every historical PR;
- initialize Claim Registry and Theory Evolution;
- classify manuscript_v0.1 as a historical snapshot in Research Memory.

Phase RSM-3 — operational capture:
- capture future major milestones asynchronously/on demand;
- build first Evidence Pack generator.

Phase RSM-4 — empirical extension:
- only when prospective/empirical work actually starts.

## Rollback Plan

Because the sidecar is non-authoritative:
- stop sidecar capture;
- preserve its history for audit;
- Product/Knowledge continue unchanged;
- no reverse migration is required.

No Product/Knowledge state should ever need rollback because of Research Memory.

## Graduation Criteria

V1 is operational when:
- writable sidecar repository exists;
- schemas/templates validate;
- checkpoint/replay works;
- at least three historical R2/R3 milestones are captured;
- at least one Concept Event is captured;
- Claim Registry contains multi-axis states;
- Theory Evolution contains an evolution/supersession chain;
- one Evidence Pack is generated from accepted evidence;
- Product/Knowledge tests and workflows remain unchanged;
- sidecar failure has no effect on Product/Knowledge.

## Human Gate

**APPROVED.**

PI approval was explicit in chat on 2026-10-21:

> 可以的，就这么干

This approval authorizes the Research Memory Sidecar architecture and its non-interference design.

It does not authorize:
- new Zhongzhou canonical meanings;
- empirical-probability claims;
- causal claims;
- Product/Knowledge semantic changes;
- bypassing future Human Gates required by those areas.

## Decision

**APPROVED: independent, non-authoritative Research Memory Sidecar v1.**

Selected principles:
- separate repository;
- one-way read dependency;
- eventual research consistency;
- append-only milestones;
- multi-axis claims;
- independent theory history;
- evidence-pack synthesis;
- no merge blocking;
- no Product/Knowledge mutation authority.

## Implementation History

- 2026-10-21: PI approved the concept in chat.
- 2026-10-21: Proposal #513 opened and formal design recorded.
- Implementation pending a bounded Governance work unit and a writable sidecar repository target.

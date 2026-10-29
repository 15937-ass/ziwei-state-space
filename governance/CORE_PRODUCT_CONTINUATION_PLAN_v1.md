# Core + Product Continuous Progression Plan v1

Status: **PI-APPROVED / ACTIVE CONTINUATION PLAN**  
Tracking Governance Issue: #896  
Product plan pointer: #900  
Core plan pointer: #901  
First Product bounded nominee: #897  
First Core bounded nominee: #898  
Integration ledger: #888

## 1. Purpose

This is the durable continuation contract for the two independent work streams the PI wants to run repeatedly in separate chats.

The user-facing commands are intentionally simple:

- **推进Core线 / 继续Core线 / 继续Core**
- **推进产品线 / 继续产品线**

A new chat must not ask the PI to restate the sequence. It recovers live GitHub state, resumes an existing bounded work unit if one exists, otherwise follows the appropriate plan pointer and admits the earliest eligible bounded nominee.

Live Issues/PRs remain execution truth. This plan is direction and continuation logic, not a substitute for bounded Issues.

## 2. Shared operating rules

Core and Product are independent lanes and may run concurrently.

- Core WIP <= 1.
- Product WIP <= 1.
- Product consumes only **accepted, pinned main checkpoints** from Core/Knowledge.
- Product never consumes an unmerged Core branch as canonical truth.
- Core does not pause merely because Product is consuming an older accepted checkpoint.
- Cross-lane feedback is explicit and typed; neither lane silently edits the other's semantics.
- Final integration is serialized through Issue #888 Integration Lease.
- Knowledge merge never auto-refreshes active Product knowledge.
- No probability, frequency, weight, score, causal claim, or predictive-validity claim is inferred from canonical mapping work.

## 3. Core continuous plan

Permanent plan pointer: **Issue #901**.

### C1 — Canonical manifestation mapping expansion

Starting accepted baseline:
- `knowledge/core/wp06b/CANONICAL_MANIFESTATION_NODE_INDEX_v0.1.json`
- `knowledge/core/wp06c/CANONICAL_MANIFESTATION_MAPPING_INDEX_v0.1.json`
- accepted canonical nodes: KMN-000001..000003
- accepted canonical mappings: KMM-000001..000003
- next mapping ID at baseline: KMM-000004
- executable mappings: 0
- Product consumption authorization: 0
- probability status: UNKNOWN

First bounded nominee: **Issue #898**.

Each Core work unit normally adds **4–8 source-backed canonical mappings**, plus only the child manifestation nodes actually required by source-supported canonical identity.

The C1 milestone is approximately:
- **15–30 accepted KMM**
- **6–10 distinct semantic structures**

Coverage is deliberate rather than bulk. Across successive batches, seek source-supported examples of:
- process;
- state;
- scene/context;
- relationship;
- conditional outcome;
- multiple antecedents;
- cross-palace dependency;
- temporal/dynamic condition;
- modifier interaction;
- explicit unresolved semantics.

Do not force every structure into one batch. Do not promote material that lacks adequate accepted evidence/review boundaries.

### C2 — Concurrent Product feedback

Product may test accepted checkpoint N while Core builds N+1.

Product feedback is classified:
- `GAP_PRODUCT`: Product interface/representation gap; Core does not change.
- `GAP_CORE`: genuine shared Knowledge semantic insufficiency; Core may adopt a bounded Core gap.
- `HOLD`: unresolved/source ambiguity that can safely remain fail-closed; do not force a definition.

Core continues C1 while Product works unless the feedback reveals a true shared semantic blocker.

### C3 — Schema stability milestone

At roughly 15–30 KMM / 6–10 semantic structures:
- review whether WP06B/WP06C node/mapping contracts survived diverse cases;
- refine only evidence-backed deficiencies;
- prefer backward-compatible migration;
- explicitly review Product crosswalk gap evidence;
- if stable, declare the manifestation mapping contract ready for broader Product crosswalk use.

Do not continue blind bulk expansion past this milestone without a stability review.

### C4 — Highest real shared blocker

After C3, select the highest real blocker among:
1. genuine Product-raised Core semantic gaps;
2. palace `KNOWLEDGE_CORE_GAP` records;
3. WP07B temporal-response gaps actually needed for the N -> E -> tau -> M0 path.

Only one Core unit at a time.

### Core permanent boundaries / Human Gates

Ordinary source-backed child nodes/mappings and fail-closed UNKNOWN/conflict preservation may proceed autonomously.

Stop for PI only when a proposed resolution would:
- create or alter a universal root/family/shared primitive;
- choose between irreducible conflicting traditional meanings instead of preserving UNKNOWN;
- materially change school/source meaning;
- introduce probability/causal semantics;
- authorize Product/runtime behavior.

Do not reopen completed fourteen-main-star basic-property research absent new evidence.

## 4. Product continuous plan

Permanent plan pointer: **Issue #900**.

### P1 — First Knowledge -> Product manifestation crosswalk pilot

First bounded nominee: **Issue #897**.

Frozen Knowledge input:
- KMN-000001..000003
- KMM-000001..000003
- accepted source/review provenance reachable from their canonical artifacts.

Existing Product baseline to preserve:
- `product/PL3M_MANIFESTATION_ONTOLOGY_ADAPTER_ACCEPTANCE.md`
- `product/PL3M_MANIFESTATION_ONTOLOGY_REGISTRY_v0.1.json`
- `product/PL3M_MANIFESTATION_MAPPING_REGISTRY_v0.1.json`
- existing KIB/lock/impact/promotion controls.

Production manifestation registries stay empty in P1.

For each relevant Knowledge field classify Product handling as:
- `DIRECT`: representable without semantic loss;
- `LOSSY`: representable only with an explicit retained loss marker;
- `GAP_PRODUCT`: Knowledge meaning is clear but Product lacks the interface;
- `GAP_CORE`: Knowledge/shared semantics are genuinely under-specified;
- `HOLD`: consumption/execution must remain blocked.

Mandatory cases:
1. KMM-000001: unresolved Fire/Bell BOTH_STARS vs EITHER_STAR -> HOLD; Product cannot choose.
2. KMM-000002: real-world prerequisite 勉强求变 is not established by chart -> Product cannot infer it; missing external-fact interface is a Product gap unless Knowledge meaning itself is unclear.
3. KMM-000003: test safe scene/context crosswalk while retaining the explicit negative boundary against person injury/illness/diagnosis/treatment.

P1 outputs:
- field crosswalk matrix;
- per-KMN/KMM verdict;
- Product-vs-Core gap register;
- lossiness / HOLD / abstention rules;
- adapter feasibility verdict;
- deterministic tests/fixtures for any implemented Product behavior.

P1 does **not**:
- populate production manifestation registries;
- promote active K_manifest/KIB;
- authorize runtime execution;
- invent probability/frequency/weight;
- make predictive-validity claims;
- rewrite Core semantics.

### P2 — Expanded-checkpoint pilot

Trigger: Core accepts a materially larger canonical checkpoint.

Product pins that accepted checkpoint and repeats the crosswalk over expanded semantic structures. Compare against P1 and classify what remained stable, disappeared, or became a genuine Core gap.

Knowledge advancement does not automatically mutate active Product baseline.

### P3 — Formal adapter/crosswalk freeze

Trigger: at least two accepted Core checkpoints have been tested and field behavior is sufficiently stable.

Freeze:
- supported fields;
- lossless/lossy mappings;
- unsupported/HOLD behavior;
- provenance/digest identity;
- fail-closed rules.

P3 is still not production knowledge promotion.

### P4 — Candidate K_manifest / KIB semantic impact

Trigger: P3 accepted.

Build a candidate only:
- candidate K_manifest/KIB component;
- semantic diff/impact report;
- affected rebuild/replay list;
- deterministic validation.

### P5 — Separate promotion

Only a separate explicit Product promotion unit may update the active Product Knowledge Lock or production manifestation registries.

Knowledge merge never auto-promotes Product.

### Product waiting behavior

If Product is waiting for the next Core checkpoint:
- it may continue an already-authorized independent Product work unit if available and within Product WIP=1;
- it must not invent filler work;
- it must not pretend an unrelated Product feature resolves the manifestation dependency.

### Product Human Gates

Stop for PI only for:
- Product runtime/promotion outside the accepted sequence;
- major Product architecture boundary change;
- probability/causal semantics;
- any proposal that would alter canonical Knowledge meaning or school boundary.

## 5. Automatic continuation algorithm

For a new Core/Product chat:

1. Run standard repository recovery.
2. Query live Issues/PRs for the selected lane/shard.
3. If an ACTIVE bounded work unit exists, resume it.
4. If no ACTIVE unit exists:
   - Core reads #901 and admits the earliest eligible Core bounded nominee (currently #898);
   - Product reads #900 and admits the earliest eligible Product bounded nominee (currently #897).
5. Ordinary authorized R0/R1 work continues without asking the PI to restate the plan.
6. Accepted R2 scope already approved by the PI may proceed within the bounded Issue.
7. Final merge follows #888 Integration Lease.
8. Stop and ask PI only for an explicit Human Gate above, an irreducible priority conflict, or a major scope change.
9. At closeout, create/record the next bounded nominee before leaving the lane with no recoverable continuation path; do not execute the next unit in the same turn.

## 6. Cross-lane handoff

The intended cadence is:

```text
Core checkpoint N accepted ─────► Product crosswalk N
Core builds N+1 in parallel       Product tests N
          │                              │
          └──── bounded GAP_CORE ◄───────┘
```

Handoffs are accepted main artifacts + explicit gap records, never unmerged branch content.

## 7. Current first nominees

- Product: **#897** — manifestation Knowledge->Product adapter/crosswalk pilot v0.1.
- Core: **#898** — canonical manifestation mapping expansion, semantic-diversity batch 1.

The durable plan pointers that remain open after individual work units close are:
- Product **#900**
- Core **#901**

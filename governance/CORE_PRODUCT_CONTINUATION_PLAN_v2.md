# Core + Product Continuous Progression Plan v2.2

Status: **PI-APPROVED / ACTIVE CONTINUATION PLAN v2.2**  
PI decision: 2026-10-30 — NATAL DetailedRead -> DECADE -> YEAR; closed-loop coordination addendum approved 2026-10-30  
Tracking Governance Issue: #949 (v2 baseline); v2.2 addendum: #963  
Product plan pointer: #900  
Core plan pointer: #901  
Integration ledger: #888  
Supersedes v1 for active continuation; v1 is retained as historical baseline.

## 1. Purpose

This plan makes the long-term work sequence explicit:

**First close a usable NATAL full-reading loop; then add DECADE analysis; then add YEAR analysis.**

Knowledge and Core build the time-layer knowledge in parallel with Product's NATAL work. Product does not wait for all Knowledge to be completed before beginning; it consumes only accepted, pinned, allowed evidence and exposes gaps rather than inventing conclusions.

Version 2.2 keeps the accepted v2 architecture and sequencing, and adds a bounded product-feedback loop, capability/evidence-based stage gates, and a small post-NATAL actual-use validation checkpoint. It does not add a lane, slot, status ledger, semantic authority, or runtime permission.

The user-facing commands remain:
- **推进宫位线**
- **推进Core线 / 继续Core**
- **推进产品线 / 继续产品线**

Live Issues/PRs and accepted `main` remain execution truth. This plan provides durable direction and continuation logic; it does not replace bounded work Issues or grant new semantic/runtime authority.

## 2. Shared operating rules

- Palace Knowledge follows its current approved one-palace-at-a-time schedule under #676 and the existing shard contract.
- Core WIP <= 1.
- Product WIP <= 1.
- Normal independent production may overlap as one palace + one Core + one Product.
- Product consumes only accepted, pinned `main` artifacts and only within their `allowed_use`.
- Product may use currently accepted RUNTIME and allowed SOURCE evidence for NATAL DetailedRead; this does not require KIB promotion.
- RUNTIME, SOURCE, MODEL_SUPPLEMENT and unresolved gaps remain separate. MODEL_SUPPLEMENT never increases canonical/runtime coverage.
- Knowledge merge never auto-refreshes Product KIB/lock or production registries.
- Core owns shared semantics; palace shards own palace-specific source research; Product owns consumption and presentation interfaces.
- Cross-lane feedback is explicit and typed. Unmerged branches are never canonical inputs.
- Final integration is serialized through #888 Integration Lease and the exact-head repository quality gate.
- No probability, frequency, weight, score, causal or predictive-validity claim is inferred from traditional source material or case reconstruction.

## 3. Palace Knowledge continuation

The current palace sequence and one-palace-at-a-time admission rule remain unchanged.

For source material relevant to time layers, palace work should progressively preserve:
- whether the source is describing NATAL, DECADE or YEAR;
- the subject and scope of the time condition;
- how the time layer relates to natal structure;
- whether decade/year conditions are simultaneous, inherited, conditional or sequential;
- palace, star, transformation, modifier and cross-palace prerequisites;
- explicit outcomes versus possible manifestations;
- exceptions, negative conditions, contradictions and UNKNOWN.

Do not turn a NATAL-only statement into a DECADE/YEAR rule. Similar wording across time layers is not proof of semantic identity. Palace work must not define shared Core semantics or promote Product execution.

The old two-palace parallelism proposal is **not approved** by the 2026-10-30 PI decision. Do not activate P06 #773 as a second slot. Any future change to the one-palace schedule requires a separate PI decision.

## 4. Core continuous plan

Permanent plan pointer: **Issue #901**.

### C0 — C9 accepted baseline

Core C9 **#945 / PR #946** is accepted and closed on main at `0d75766cc0fcf86686df196565fbd598be4b1da6`, with the bounded verdict `DESCRIPTIVE_PATH_SUBTYPES_CONFIRMED_NO_EXECUTION`. Its original scope and non-executable boundary remain unchanged; do not reopen or expand it.

### C1 — Shared NATAL / DECADE / YEAR layer semantics

After C9 is accepted and the Core WIP slot is free, the next Core priority is one bounded research package on the shared temporal-layer relationship and response semantics required for a source-grounded reading sequence. Its first checkpoint audits the accepted v0.5 NATAL structure against the Product consumption contract, identifies reusable structure versus genuine shared gaps, and avoids rebuilding existing architecture.

Research questions:
1. What role does the NATAL base structure play when reading time layers?
2. How does a DECADE environment relate to and condition the NATAL structure?
3. How does a YEAR environment relate to the NATAL structure and the selected DECADE context?
4. How should the source distinguish environment, trigger/activation, response and manifestation?
5. Which prerequisites, inherited conditions, cross-palace dependencies, modifiers and exceptions must be preserved?
6. Which relationships are source-explicit, which are safe descriptive normalization, and which remain UNKNOWN/HOLD?

Keep the approved v0.4 objects distinct:
- `N`: Natal Essence / natal base;
- `E_decade`: decade temporal environment;
- `E_year`: year temporal environment;
- `tau_t`: response of the natal structure under a specified temporal environment;
- `M0`: source-supported manifestation candidates.

Do not assume that decade and year simply add, linearly combine, share an unconditional operator, or imply a concrete event. Their dependency and ordering must be grounded in sources and cases.

Core owns shared semantics and contracts only. It does not replace palace source research, modify Product files, or authorize runtime execution.

### C2 — Cases and WP03/WP06A as validation inputs

WP03 sixty-system verification, WP06A case reconstruction and Wang Tingzhi examples remain important. Their role is to validate the reasoning chain across the stages, not to block the first Product NATAL closure as a separate standalone project.

Use source-complete examples to:
- verify single-star properties as inputs to system nature;
- reconstruct how the author moves from chart facts to NATAL conclusions;
- test decade response and year-within-decade conditions where the case actually supplies them;
- record unreconstructable steps, counterexamples, missing prerequisites and school-specific claims.

Case count is determined by source completeness and reconstructability, not a quota. Case support does not become empirical probability ground truth.

### Core permanent boundaries / Human Gates

- Preserve source qualifiers, prerequisites, negation, time layer, conflict and UNKNOWN.
- Do not create a universal root/family/shared primitive without its existing Human Gate.
- Do not resolve irreducible traditional conflicts by guesswork.
- Do not change school/source meaning.
- Do not add probability, causal semantics, weights or runtime authorization.
- Do not reopen completed fourteen-main-star basic-property research without new evidence.

## 5. Product continuous plan

Permanent plan pointer: **Issue #900**.

### P0 — Canonical Zhongzhou chart contract

Product Issue #977 is the bounded implementation unit for the PI decision dated 2026-10-31. It makes `product/CANONICAL_CHART_CONTRACT_v1.1.md` the permanent production chart authority: Zhongzhou method + pinned `iztro-js@2.6.1`, fixed configuration, all NATAL and temporal scopes generated by the same engine contract, and fail-closed production snapshot validation. Differential engines remain audit-only. No LLM/manual chart construction or post-hoc chart repair is allowed. Any future change requires explicit PI approval, a new contract version, migration plan, and full P1 regression. This work does not authorize new chart semantics or temporal inference.

### P1 — NATAL DetailedRead closed loop

First Product work unit: `PRODUCT_NATAL_DETAILED_READ_CLOSED_LOOP_V1`.

Reuse accepted:
- Product #798 QuickRead capability-aware evidence contract and current-main reader;
- Product #882 DetailedRead v0.1 planner;
- Governance #894 / PR #895 DetailedRead natural-language Skill;
- existing deterministic chart and NATAL runtime infrastructure.

Do not rebuild the planner, chart engine, rule engine, Knowledge registry or natural-language routing.

Required NATAL flow:

```
same chart
 -> deterministic chart facts
 -> all 12 NATAL atomic domain slots
 -> progressive current-main evidence retrieval
 -> separate RUNTIME / SOURCE / MODEL_SUPPLEMENT / gaps
 -> coverage and provenance report
 -> cross-domain consistency checks
 -> thematic, staged DetailedRead output
```

Acceptance:
- all twelve NATAL domains enter inspection and appear in the coverage/gap report;
- unequal domain coverage is allowed and must be visible;
- evidence retrieval is progressive, deduplicated and pinned to one main snapshot;
- runtime/source/model lanes are counted separately;
- user-facing sections synthesize life themes rather than mechanically reciting twelve palaces;
- cross-domain checks preserve genuine conditional differences and conflicts;
- unsupported domains remain brief/unknown instead of being filled;
- same-chart QuickRead continuation is reused only when its identity and main pin are verified;
- no DECADE/YEAR claim is made without matching accepted temporal evidence.

NATAL DetailedRead may use currently accepted RUNTIME and allowed SOURCE material without a new KIB promotion. This is not permission to consume non-authorized KMM, promote KIB/K_manifest, change runtime effects, or populate production registries.

### P2 — DECADE integration

Trigger: NATAL closure is accepted, the post-NATAL actual-use checkpoint is accepted, and relevant Knowledge/Core temporal evidence is on main with an explicit Product-consumption allowance. If no eligible source-complete chart/case fixture exists, record the exact blocker; do not fabricate a test or claim actual-use validation.

Product adds `E_decade` and, only where source-supported and permitted, `tau_decade`. It must keep NATAL essence, decade environment and natal response under that environment distinct. Unsupported domains remain visible gaps; no event certainty is implied.

### P3 — YEAR integration

Trigger: DECADE structure is stable and matching YEAR evidence plus its relationship to the selected DECADE context is accepted and Product-consumable.

Product adds `E_year` and, only where supported, `tau_year`. Preserve NATAL, DECADE and YEAR scopes, prerequisites, modifiers and conflicts; do not flatten them into one 吉凶 label or concrete event claim.

### P4 — M0 and later validation

M0 remains limited to source-supported possibility routing. It cannot be populated by projection wording, model supplementation or unsupported response effects. Forecast Ledger retains the existing v0.4 trigger: begin only after the first executable source-only `N -> E -> tau -> M0` vertical slice exists.

### Product waiting and Human Gates

- Product must not wait for a new KIB candidate before beginning the independent NATAL DetailedRead closure.
- Product must wait for accepted, Product-consumable temporal evidence before DECADE/YEAR runtime consumption.
- Knowledge merge never silently mutates the active Product lock.
- Product WIP <= 1.
- Stop for PI only at the existing major architecture, semantic, runtime/promotion, probability/causal or school-boundary Human Gates.

## 6. Cross-lane cadence

The intended cadence is:

```
Palace Knowledge: source-first NATAL + temporal layer research (one palace at a time)
                         │
                         ▼ accepted main evidence
Core: accepted C9 -> NATAL structure/consumption-contract checkpoint -> shared NATAL/DECADE/YEAR semantics
                         │
                         ▼ accepted, Product-consumable checkpoint
Product: NATAL DetailedRead -> actual-use validation -> DECADE -> YEAR
```

Product NATAL can proceed while Core researches shared temporal semantics and palace Knowledge continues its one-palace source review. Product consumes only current accepted main evidence; it does not wait for future temporal work to finish.

When Product finds a gap:
- Product interface/representation gap -> Product owns it;
- genuine shared temporal semantics gap -> Core receives a bounded handoff;
- palace-specific source gap -> the owning palace shard receives it;
- source ambiguity that can safely remain unresolved -> HOLD/UNKNOWN, do not force a resolution.

## 7. Expert method, cases and empirical validity

Case reconstruction validates source fidelity and expert-method fidelity. It does not prove real-world predictive validity.

Track separately:
- canonical/source fidelity;
- expert-method fidelity;
- prospective predictive validity;
- cross-school procedural robustness.

A pass in one category is not a pass in another. Other schools remain explicitly namespaced and cannot mutate Zhongzhou canonical semantics.

## 8. Automatic continuation algorithm

For a new Core/Product chat:

1. Run standard repository recovery and read the live lane Issue/PR.
2. If an ACTIVE bounded work unit exists, resume it.
3. If Core has no ACTIVE unit, read #901: C9 #945/#946 is accepted; admit one bounded Core unit whose first checkpoint audits the accepted v0.5 NATAL structure against the Product consumption contract (reuse, do not rebuild), then proceeds to shared temporal-layer semantics.
4. If Product has no ACTIVE unit, read #900: admit the NATAL DetailedRead closed-loop unit first; after its acceptance, admit the small actual-use validation checkpoint before claiming NATAL is use-validated.
5. Admit DECADE only after NATAL closure and its actual-use validation checkpoint are accepted, and matching Knowledge/Core temporal evidence is on main with explicit Product allowed-use. Exhaustive completion of all unrelated Knowledge is not required.
6. Admit YEAR only after the DECADE structure is stable and matching YEAR evidence plus its relation to the selected DECADE context is accepted and Product-consumable.
7. Continue ordinary authorized work without asking the PI to restate the route; stop only at an explicit Human Gate or major priority conflict.
8. At closeout, leave the next bounded nominee and handoff. Do not execute the next unit in the same turn.
9. All final merges follow #888 Integration Lease and the exact-head full quality gate.

## 9. Permanent boundaries

- Accepted `main` is the formal input; unmerged branches, Issue text, archived drafts and model memory are not accepted Knowledge.
- RUNTIME / SOURCE / MODEL_SUPPLEMENT / CASE_SUPPORT_ONLY remain distinct.
- Product consumption requires the explicit allowed-use and compatibility conditions already defined by the repository.
- No automatic KIB refresh or promotion.
- No unapproved runtime, probability, causal, predictive-validity or school-boundary changes.
- Palace one-at-a-time schedule and all current WIP caps remain unchanged.
- The old v1 plan remains available for historical traceability but no longer determines the active Core/Product sequence.


## 10. v2.2 closed-loop coordination addendum — active

This addendum is part of the active continuation contract. It supplements Sections 2–9 without replacing their accepted architecture, work ownership, epistemic boundaries or integration rules.

### 10.1 Three-stream production and feedback

The three streams operate as a closed loop while retaining independent ownership:

- **Knowledge** establishes source-grounded facts, conditions, temporal scope, exceptions, contradictions and UNKNOWN. It continues the approved one-palace-at-a-time sequence. At each bounded batch closeout, add a lightweight Product-availability note to the existing Issue/PR: layer (NATAL/DECADE/YEAR), prerequisites, source status, allowed-use and unresolved gaps. Product feedback may create a targeted source handoff, but does not interrupt or broaden an already active palace batch for non-blocking findings.
- **Core** organizes accepted knowledge into shared, source-bounded structures and temporal relations. It owns shared cross-palace and NATAL/DECADE/YEAR semantics; it reuses accepted models and contracts rather than rebuilding them.
- **Product** consumes only accepted, pinned, Product-allowed main evidence; demonstrates user-visible capability; and reports reproducible consumption, structure or provenance defects. Product tests do not create canonical source truth.

Normal independent concurrency remains exactly one active palace + one Core + one Product. Core WIP <= 1, Product WIP <= 1, one palace slot under #676, and serialized final integration under #888. Product feedback is not a fourth lane or an additional work slot.

### 10.2 Product finding classification and ownership

Every material Product finding receives one primary classification:

| Class | Meaning | Owner / disposition |
| --- | --- | --- |
| `KNOWLEDGE_GAP` | Palace/source-specific evidence, condition, temporal scope or source reconciliation is missing or unclear | Owning Knowledge palace shard |
| `CORE_GAP` | Accepted local knowledge exists, but a shared structural, cross-palace or temporal relation cannot be represented by the accepted Core contract | Core; use the existing `KNOWLEDGE_CORE_GAP` handoff convention where applicable |
| `PRODUCT_GAP` | Retrieval, orchestration, consumption, interface, presentation, provenance or fail-closed implementation is defective | Product |
| `HOLD_UNKNOWN` | Evidence is insufficient or irreducibly conflicting | Preserve unresolved; do not force a conclusion or artificial owner |

Classification identifies the accountable owner; it does not promote evidence, settle source conflicts, or authorize cross-lane writes. Use the existing `governance/CROSS_LANE_HANDOFF_v1.md` and producer/consumer Issues. Do not create a second global status ledger.

### 10.3 Feedback priority and interruption policy

- **P0 — immediate correctness boundary:** an affected output would otherwise make an unsupported, structurally wrong or canonical-contaminating claim. Fail closed for that claim immediately and route the demonstrated defect to its owner. Stop the affected inference, not unrelated work.
- **P1 — current-stage blocker:** the issue prevents acceptance or the next approved stage. Record the exact missing input and queue the next eligible bounded work unit for the responsible lane. Do not silently pre-empt another active work unit.
- **P2 — non-blocking improvement:** coverage, usability or quality improvement that does not invalidate the current result. Record it in the existing Issue/PR and defer it to a suitable later unit.

A P0 correctness defect may require immediate handling under the existing work unit's authority; it does not authorize a second palace, Core or Product worker. A P1/P2 finding does not interrupt a source batch that can safely continue. Priority does not override Human Gates or the Integration Lease.

### 10.4 Core next-work checkpoint: reuse the NATAL structure

With C9 #945/#946 accepted, the next admitted Core unit begins with a bounded checkpoint that compares:

1. the accepted v0.5 NATAL state-space structure and its local-palace/global-graph distinction;
2. the accepted Knowledge artifacts and their explicit allowed-use;
3. the Product NATAL DetailedRead consumption contract and the actual gaps it exposes.

The checkpoint must identify what is already represented and reusable, what is missing, and which missing item is truly shared Core semantics. It is not permission to rebuild the state-space model, create a second Product inference engine, or duplicate completed star/palace research. The same bounded Core unit then advances the shared NATAL / DECADE / YEAR temporal and response semantics specified in Section 4, preserving source qualifiers, prerequisites, modifiers, conflicts and UNKNOWN.

### 10.5 Product NATAL actual-use validation and stage gates

After Product #951 is accepted on main, Product performs one small, reproducible actual-use validation checkpoint using an eligible existing source-complete chart/case fixture or PI-authorized chart material. It checks actual evidence retrieval/consumption, provenance, twelve-domain coverage/gaps, cross-domain behavior and fail-closed handling. It does not require complete coverage of every palace rule.

If no eligible fixture exists, Product records the exact missing fixture/permission and leaves actual-use validation explicitly unpassed. It must not invent a chart, silently substitute a synthetic fixture, or describe a synthetic orchestration test as an actual chart run. This checkpoint validates implementation and source/method fidelity only; it does not establish prospective predictive validity.

Stage advancement is capability/evidence-based, not knowledge-volume-based:

- **NATAL -> DECADE:** accepted NATAL DetailedRead closure; actual-use validation accepted; natal essence and global palace relationships remain correctly represented; coverage and UNKNOWN are explicit; and matching temporal Knowledge/Core evidence is accepted on main with explicit Product allowed-use. Complete coverage of every palace, star-system or source rule is not required.
- **DECADE -> YEAR:** the DECADE structure is stable; matching YEAR evidence and its relationship to the selected DECADE context are accepted on main and explicitly Product-consumable; NATAL, DECADE and YEAR scopes remain distinct.
- **YEAR -> later M0/Forecast work:** the existing source-only executable `N -> E -> tau -> M0` vertical-slice trigger remains unchanged.

A stage may have visible gaps. It may not disguise a gap as a supported conclusion. Capability validation, source/method fidelity, production readiness and prospective predictive validity remain separate claims.

### 10.6 Minimum durable Product finding payload

Record findings in the existing consumer/producer Issue or PR, not a new ledger. Include only what is needed to reproduce and route the issue:

- chart/case fixture identifier and version (or explicitly unavailable);
- accepted main SHA and relevant Knowledge/Core/lock versions;
- user question and involved domains/palaces;
- evidence and relationships actually consumed;
- expected versus actual behavior;
- primary finding class and P0/P1/P2 priority;
- accountable producer/consumer Issue, exact missing input and allowed write set;
- accepted-main unblock evidence, retest result and unresolved limitations.

Reuse the existing cross-lane handoff fields for producer, consumer, dependency, unblock evidence, safe parallel work and ownership. Do not duplicate completed source review or rerun unchanged tests merely to produce another status report.

# Core + Product Continuous Progression Plan v2

Status: **PI-APPROVED / ACTIVE CONTINUATION PLAN**  
PI decision: 2026-10-30 — NATAL DetailedRead -> DECADE -> YEAR  
Tracking Governance Issue: #949  
Product plan pointer: #900  
Core plan pointer: #901  
Integration ledger: #888  
Supersedes v1 for active continuation; v1 is retained as historical baseline.

## 1. Purpose

This plan makes the long-term work sequence explicit:

**First close a usable NATAL full-reading loop; then add DECADE analysis; then add YEAR analysis.**

Knowledge and Core build the time-layer knowledge in parallel with Product's NATAL work. Product does not wait for all Knowledge to be completed before beginning; it consumes only accepted, pinned, allowed evidence and exposes gaps rather than inventing conclusions.

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

### C0 — Finish current C9 unchanged

Current live Core unit: **#945 / PR #946**. It must complete its original bounded WP07B persistence/path and GAP-006 overlap audit. This plan does not expand its scope or change its write set.

### C1 — Shared NATAL / DECADE / YEAR layer semantics

After C9 closes, the next Core priority is a bounded research package on the shared temporal-layer relationship and response semantics required for a source-grounded reading sequence.

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

Trigger: NATAL closure is accepted and relevant Knowledge/Core temporal evidence is on main with an explicit Product-consumption allowance.

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
Core: current C9 -> shared NATAL/DECADE/YEAR semantics
                         │
                         ▼ accepted, Product-consumable checkpoint
Product: NATAL DetailedRead -> DECADE -> YEAR
```

Product NATAL can proceed while Core completes C9 and while palace Knowledge works independently. Product consumes only current accepted main evidence; it does not wait for future temporal work to finish.

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
3. If Core has no ACTIVE unit, read #901: finish any current live C9 first; after C9, admit the earliest eligible temporal-layer semantics research unit.
4. If Product has no ACTIVE unit, read #900: admit the NATAL DetailedRead closed-loop unit first.
5. After NATAL is accepted, Product may admit DECADE only when the matching Knowledge/Core checkpoint is accepted and Product-consumable.
6. Admit YEAR only after the DECADE layer is stable and matching YEAR evidence is accepted.
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

# Product vNext Execution Plan v0.1

Status: **APPROVED EXECUTION DECOMPOSITION**  
Derived from: PRODUCT_ROADMAP.md v0.4 and Proposal #425  
Purpose: separate **NOW** from **FUTURE**, prevent framework drift, and define the first vertical-slice critical path.

## 1. Current accepted baseline

As of Product #416 / PR #418:
- Chart Trust is complete/frozen.
- Canonical Product runtime exists.
- Wealth natal provider is partial.
- Career natal provider has **190 accepted NATAL rules on main**.
- Temporal fact generation and TemporalEnvironmentProfile infrastructure exist.
- Production canonical temporal reaction content is still effectively empty.
- Manifestation ontology/mapping runtime contracts exist but canonical content is not ready.
- Empirical calibration is not started.
- Product state previously still pointed at closed #416/#418; Proposal #425 repairs that recovery state.

Knowledge-side Response Semantics is an input dependency. Semantic compatibility does **not** imply Product executability.

## 2. Critical-path rule

Until the first end-to-end dynamic vertical slice works, Product shall optimize for **capability-layer advancement**, not raw natal rule count.

Career NATAL 190 is sufficient for the first vertical slice.

Further natal expansion:
- remains valuable Knowledge/Product inventory work;
- may continue when specifically selected;
- is not the Product critical-path KPI before PL3-R / PL3-M0 works.

## 3. Architecture shorthand

Permanent separated objects:

~~~text
Kc = canonical declarative knowledge
Kr = canonical response knowledge
π  = inference policy / procedural knowledge
θ  = empirical calibration parameters
b  = individual state belief
~~~

Core near-term chain:

~~~text
Chart
-> Natal Essence N
-> Temporal Environment E_t
-> ResponseProfile τ_t
-> Canonical Manifestation Candidates M0
~~~

Expert reasoning policy π controls search/inspection order but does not own canonical truth.

## 4. NOW — immediate Product work

### NOW-0 — State recovery and architecture acceptance
**Status:** this Governance work unit.

Deliverables:
- Product v0.4 roadmap;
- Proposal #425;
- this execution plan;
- Product state no longer points at #416/#418;
- explicit NOW/FUTURE split.

Exit:
- merged governance PR;
- governance validation pass.

### NOW-1 — Expert-method data contracts
**Lane:** PRODUCT_ONLY  
**Priority:** P0

Define:
- CaseBundle;
- ExpertReasoningGraph;
- InferenceTrace;
- MethodPattern;
- SchoolCompatibility;
- trace action vocabulary.

Hard boundary:
- no free-form hidden reasoning persistence;
- persist only auditable evidence/action graph.

Exit:
- deterministic schema tests;
- one synthetic fixture;
- no change to canonical rule semantics.

### NOW-2 — Wang Tingzhi expert-case corpus
**Lane:** PRODUCT_ONLY with source read dependency  
**Priority:** P0

Transform all available Wang Tingzhi expert cases into structured demonstrations:
- input-visible facts separated from expert explanation/outcome;
- expert actions/evidence/branch/stop reconstructed with provenance;
- unresolved reconstruction explicitly marked.

Evaluation:
- 10-fold leave-one-case-out expert replay;
- every case held out once;
- no case-derived empirical probabilities.

Exit:
- complete case inventory;
- provenance coverage report;
- LOCO replay harness.

### NOW-3 — Method Policy v0.1
**Lane:** PRODUCT_ONLY  
**Priority:** P0

First implementation:
- Case-Based Retrieval;
- source-explicit procedural rules;
- deterministic/heuristic planner;
- canonical verifier;
- abstention/stop rules.

LLM may propose next actions but cannot validate its own proposal.

Do **not** fine-tune a model at this stage.

Exit:
- next-action benchmark;
- evidence-selection benchmark;
- no canonical contamination.

### NOW-4 — Response Semantics Product Adapter
**Lane:** PRODUCT_ONLY  
**Priority:** P0

Consume Knowledge artifacts while preserving:
- membership;
- activation;
- relation;
- interaction;
- ordinal;
- effect target;
- scope;
- epistemic status;
- allowed use.

Fail closed:
- SEMANTIC_ONLY -> no runtime effect;
- BLOCKED -> no runtime effect;
- local semantics do not auto-globalize;
- no ANY/ALL defaults invented.

Exit:
- adapter contract tests;
- compatibility fixtures;
- zero unauthorized execution unlock.

### NOW-5 — Source-backed Response Corpus dependency
**Primary producer:** KNOWLEDGE_ONLY  
**Consumer:** Product

Knowledge target:
- extract Natal Essence × encountered temporal structure -> response material from approved sources;
- prioritize sixty-system nature/response passages, modifier/transformation material, and palace/limit interaction examples;
- preserve UNKNOWN where source is incomplete.

Product target:
- define ingestion/readiness report;
- do not infer missing response semantics.

Important:
- Career WP05 time-layer rows are not the only source of response knowledge.

### NOW-5A — Product Knowledge Dependency Control v0.1
**Lane:** PRODUCT_ONLY after Proposal #491 governance merge  
**Priority:** P0 / reliability gate before NOW-6

Purpose:
- make the frozen Knowledge baseline machine-verifiable;
- prevent mutable Knowledge `main` from silently changing Product behavior;
- absorb later Knowledge improvements through candidate -> impact -> validation -> promotion.

Bounded implementation order:

~~~text
PRODUCT_KNOWLEDGE_LOCK_V0_1
-> PRODUCT_KNOWLEDGE_IMPACT_V0_1
~~~

`PRODUCT_KNOWLEDGE_LOCK_V0_1` must provide:
- componentized KIB over K_signal / K_response / K_manifest / K_method;
- source commit + artifact digest + semantic digest;
- active Product Knowledge Lock;
- fail-closed mismatch detection;
- migration of #462/#482 governed inputs without rewriting their historical acceptance claims.

`PRODUCT_KNOWLEDGE_IMPACT_V0_1` must provide:
- active-vs-candidate semantic diff;
- dependency propagation;
- deterministic impact classes;
- candidate/active promotion gate;
- unchanged Knowledge components do not invalidate unrelated Product artifacts.

Impact classes at minimum:

~~~text
NO_RUNTIME_EFFECT
PROVENANCE_REVALIDATION
READINESS_REBUILD
SYMBOLIC_RECOMPILE
METHOD_REPLAY
MANIFESTATION_REBUILD
DATASET_REMATERIALIZE
RETRAIN_OR_RECALIBRATE
MIGRATION_REQUIRED
~~~

Exit:
- a Product build can prove exactly which Knowledge bytes/semantics it consumed;
- a newer Knowledge main does not mutate active Product until promotion;
- Product can determine whether a Knowledge update requires rebuild, recompile, replay, rematerialization, retraining, or no action.

Hard boundary:
- this layer does not reinterpret Zhongzhou semantics;
- Product may not promote source candidates into canonical Kr merely to satisfy NOW-6.

### NOW-6 — PL3-R Response Compiler v0.1
**Lane:** PRODUCT_ONLY  
**Priority:** P0 / core capability

Scope:
- Natal Essence N;
- Decade environment;
- Year environment;
- canonical response knowledge Kr;
- symbolic ResponseProfile τ_t.

Output must support:
- activated;
- strengthen/weaken;
- transform;
- gate;
- conflict;
- ordinal;
- effect target;
- UNKNOWN;
- full provenance.

No:
- probability;
- numeric magnitude without source;
- month/day/hour requirement.

Exit:
- first deterministic N + E_decade + E_year -> τ fixtures.

### NOW-7 — PL3-M0 Canonical Manifestation Candidates
**Lane:** PRODUCT_ONLY  
**Priority:** P0 after PL3-R

Input:
- τ_t;
- source-backed manifestation ontology/mapping.

Output:
- SOURCE_SUPPORTED_POSSIBILITY;
- source evidence;
- conflict/unknown.

No empirical probability.

Exit:
- first N -> E -> τ -> M0 vertical slice.

### NOW-8 — Fidelity benchmark suite
**Lane:** PRODUCT_ONLY  
**Priority:** P0

Benchmark A — Canonical Fidelity:
- source trace;
- rule/response activation;
- unsupported inference;
- determinism;
- conflict preservation.

Benchmark B — Expert Method Fidelity:
- critical evidence recall;
- wrong evidence;
- next action;
- branch choice;
- time-depth choice;
- stop/abstention;
- partial-order trace compatibility.

Benchmark D — Cross-School Robustness:
- method transfer only;
- school-specific truth remains isolated.

### NOW-9 — Forecast Ledger activation
**Lane:** PRODUCT_ONLY / PL7 integration  
**Priority:** P1 but starts immediately after vertical slice

Start when:
- N -> E -> τ -> M0 is executable.

Lock:
- information cutoff;
- knowledge version;
- method-policy version;
- model version;
- target/window;
- prediction/abstention.

Future outcome is appended; old forecast is never rewritten.

## 5. Parallel Knowledge dependencies

Product shall consume but not own the following Knowledge programs:

1. finish Response Semantics compatibility classification;
2. resolve high-value relation/activation/category blockers through source review;
3. build source-backed response-principle corpus;
4. advance manifestation ontology/mapping;
5. keep school/source provenance explicit.

Product may create a KnowledgeGapReport when blocked.

Product may not:
- silently repair source truth;
- infer activation from membership;
- promote case-only evidence to canonical rule.

## 6. Other Sanhe case program

After Wang case schema is stable, structure additional Sanhe cases.

Each case/method fragment receives:

~~~text
IDENTICAL
SEMANTIC_EQUIVALENT
PROCEDURAL_COMPATIBLE
SCHOOL_SPECIFIC
CONFLICTING
UNKNOWN
~~~

Allowed use:
- identical/equivalent: retrieval + method support, subject to provenance;
- procedural-compatible: method-policy regularization only;
- school-specific: namespaced school adapter/case memory;
- conflicting: retained as contrastive evidence, never merged into Zhongzhou core;
- unknown: retrieval-only until reviewed.

## 7. FUTURE — not current critical path

### FUTURE-1 — Acquired State / Belief
Build:
- X_t acquired/real state representation;
- b_t system belief;
- observation provenance;
- missingness;
- contradictions;
- deterministic update first;
- simple Bayesian update second.

### FUTURE-2 — Contextual Manifestation M1
M1 <- M0 + X_t + b_t + A_t + C_t

Keep source possibility separate from contextual routing.

### FUTURE-3 — Prospective Blind Benchmark
Only pre-cutoff data allowed.
Compare:
- context-only;
- pure LLM;
- RAG;
- flat rules;
- N;
- N+E;
- N+E+τ;
- calibrated/personalized models.

### FUTURE-4 — Empirical Calibration θ
Order:
1. frequency baseline;
2. GLM / multinomial / ordinal;
3. survival / event-history when definitions fit;
4. hierarchical Bayesian.

No chart-validity claim without out-of-sample incremental value.

### FUTURE-5 — Dynamic State-Space
Only after longitudinal data justifies recursive latent state:
- dynamic Bayesian / state-space;
- observer;
- particle methods only if needed;
- neural SSM later.

### FUTURE-6 — Multi-school production
Zhongzhou remains canonical core.
Other schools enter through adapters with attribution and conflict preservation.

### FUTURE-7 — Advanced ML
Only after simpler baselines are beaten:
- MoE;
- graph models;
- neural state-space;
- learned residuals.

### FUTURE-8 — Causal / action / control
Only after identification and policy-evaluation gates:
- conditional scenarios;
- causal analysis;
- MPC;
- offline RL last.

## 8. Method-learning order

~~~text
Source-explicit procedural rules
-> Case-Based Reasoning
-> heuristic/deterministic planner
-> LLM planner + symbolic verifier
-> process mining / ILP / rule induction
-> learned policy only if held-out benefit exists
~~~

A 10-case Wang corpus is insufficient justification for neural fine-tuning.

## 9. Temporal-depth rule

v0.4 core:

~~~text
Natal -> Decade -> Year
~~~

Month:
- only after higher-level trigger;
- only where target/question requires finer timing.

Day/hour:
- future;
- not part of the first response vertical slice.

## 10. Four benchmark families

| Benchmark | Question | Data |
|---|---|---|
| A Canonical Fidelity | Did we implement source faithfully? | approved sources/fixtures |
| B Expert Method Fidelity | Did we learn how the expert reasons? | Wang expert cases |
| C Predictive Validity | Does it predict reality prospectively? | prospective real-world ledger |
| D Cross-School Robustness | Is method transferable without school contamination? | other Sanhe cases |

A/B/D never substitute for C.

## 11. Progress metrics

Until NOW-9, report capability progress with:
- number of structured expert cases / total;
- LOCO folds completed;
- method-action accuracy/coverage;
- response records ingestible/executable/blocked;
- number of N+E->τ validated fixtures;
- number of τ->M0 validated mappings;
- vertical slices completed;
- unsupported inference rate;
- abstention behavior.

Do **not** use Career natal rule count alone as Product progress.

## 12. Stop/go gates

Do not proceed to empirical calibration until:
- at least one source-grounded dynamic vertical slice exists;
- M0 ontology is stable enough to define outcomes;
- Forecast Ledger can lock prediction version and target.

Do not proceed to neural models until:
- enough data exists;
- simpler interpretable baselines are established;
- held-out gain is reproducible.

Do not proceed to causal action recommendation until:
- causal assumptions/identification are explicit;
- offline evaluation is meaningful;
- high-risk domain boundaries are preserved.

## 13. Current recovery / immediate next Product issue

Accepted Product progress now includes:
- **PRODUCT_METHOD_CASE_CONTRACTS_V0_1** / expert-method contracts (completed);
- Wang 24-case structured corpus and LOCO manifest;
- deterministic CBR + Method Policy π v0.1;
- fail-closed Response Semantics adapter;
- Product #482 / PR #484 Response Corpus ingestion/readiness.

#482 measured abundant source temporal material but **0 compiler-ready canonical Kr records on its frozen acceptance baseline**. NOW-6 therefore remains fail-closed on its canonical Knowledge dependency.

After Proposal #491, the immediate next Product work unit is:

**PRODUCT_KNOWLEDGE_LOCK_V0_1**

Then:

**PRODUCT_KNOWLEDGE_IMPACT_V0_1**

These are reliability prerequisites for safely consuming future Knowledge updates. They do not block the independent Wang blind-evidence materialization dependency from being prepared, but any promoted governed artifact must ultimately bind to the Product Knowledge Lock.

Before PL5, `DATASET_MODEL_LINEAGE_V0_1` becomes a mandatory stop/go gate: no incompatible Knowledge-derived feature/label sets may be silently combined.

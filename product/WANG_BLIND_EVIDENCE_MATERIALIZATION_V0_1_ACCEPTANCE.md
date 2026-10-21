# Wang Blind Evidence Materialization v0.1 — Acceptance

Tracking Issue: #512  
Lane: PRODUCT_ONLY  
Status: **IMPLEMENTED / VALIDATION PENDING**

## 1. Result

This work unit converts the Wang Tingzhi 24-case corpus from source-pointer-only blind inputs into a bounded machine-readable evidence layer.

The materialization is deliberately narrow:

- 24 / 24 case IDs reviewed against the source chart pages;
- target-palace identity is materialized;
- only the fourteen major stars visible in the target palace are materialized;
- when the target palace has no main star, only the source-visible opposite-palace borrowed major-star system is recorded;
- full-chart reconstruction is **not** claimed.

The blind artifact remains independent from source subject names, expert reasoning, conclusions, outcomes, and external biography.

## 2. Source review census

| Case | Domain | Palace | Direct major-star system | Borrowed opposite system | Source page(s) |
|---|---|---|---|---|---|
| WANG-CASE-001 | PARENTS | 父母宫 | 天相 | — | 7 |
| WANG-CASE-002 | PARENTS | 父母宫 | — | 太阳、天梁 | 7–8 |
| WANG-CASE-003 | LIFE | 命宫 | 天同 | — | 8–9 |
| WANG-CASE-004 | LIFE | 命宫 | 天机、太阴 | — | 9–10 |
| WANG-CASE-005 | SIBLINGS | 兄弟宫 | 太阳、太阴 | — | 10–11 |
| WANG-CASE-006 | SIBLINGS | 兄弟宫 | 廉贞、天府 | — | 11 |
| WANG-CASE-007 | SPOUSE | 夫妻宫 | 天同、天梁 | — | 11–12 |
| WANG-CASE-008 | SPOUSE | 夫妻宫 | 天府 | — | 12–13 |
| WANG-CASE-009 | CHILDREN | 子女宫 | 紫微、破军 | — | 13–14 |
| WANG-CASE-010 | CHILDREN | 子女宫 | — | 天机、巨门 | 14 |
| WANG-CASE-011 | WEALTH | 财帛宫 | 太阴 | — | 14–15 |
| WANG-CASE-012 | WEALTH | 财帛宫 | 天梁 | — | 15–16 |
| WANG-CASE-013 | HEALTH | 疾厄宫 | 破军 | — | 16–17 |
| WANG-CASE-014 | HEALTH | 疾厄宫 | 太阴 | — | 17–18 |
| WANG-CASE-015 | TRAVEL | 迁移宫 | — | 天同、巨门 | 18 |
| WANG-CASE-016 | TRAVEL | 迁移宫 | — | 天机、天梁 | 18–19 |
| WANG-CASE-017 | FRIENDS | 奴仆宫 | — | 天同、太阴 | 19–20 |
| WANG-CASE-018 | FRIENDS | 奴仆宫 | 破军 | — | 20–21 |
| WANG-CASE-019 | CAREER | 官禄宫 | 贪狼 | — | 21 |
| WANG-CASE-020 | CAREER | 官禄宫 | 贪狼 | — | 22 |
| WANG-CASE-021 | PROPERTY | 田宅宫 | 廉贞、破军 | — | 22–23 |
| WANG-CASE-022 | PROPERTY | 田宅宫 | 破军 | — | 23–24 |
| WANG-CASE-023 | FORTUNE_VIRTUE | 福德宫 | 天府 | — | 24 |
| WANG-CASE-024 | FORTUNE_VIRTUE | 福德宫 | — | 天梁 | 25 |

Census:

- direct-main-star target palaces: **18 / 24**
- empty-main-star target palaces with explicit opposite borrowing: **6 / 24**
- target-palace evidence materialized: **24 / 24**
- full charts materialized: **0 / 24**

## 3. Why v0.1 stops at the major-star system

The scanned source pages contain far more information than the target major-star system: auxiliaries, malefics, transformations, palace stems/branches, age bands, body-palace markers and other annotations.

Those fields are intentionally excluded from v0.1.

The reason is auditability rather than convenience. A partially legible chart cell must not become a machine fact merely because an extractor can make a plausible guess. This version therefore records only the narrow layer that was visually reviewable across all 24 target palaces.

## 4. Blindness / leakage boundary

The versioned blind evidence artifact does not contain:

- source subject labels;
- person-group IDs;
- expert reasoning graph;
- expert conclusions;
- outcome references;
- expert prose;
- external biography.

Each materialized fact is namespaced as:

`MATERIALIZED_FACT:WANG-CASE-xxx:TARGET_PALACE:...`

and retains the corresponding source chart-span reference.

A source pointer such as `WANG-ANXING-TUIDUAN:...:CHART` remains a source locator; it is **not itself** treated as a materialized fact.

## 5. Product Knowledge lineage

This artifact is a Product output derived under the active Product Knowledge lock:

- lock: `PRODUCT_KNOWLEDGE_LOCK_V0_2`
- active bundle: `KIB-PRODUCT-20261021-V0_2`
- K_method semantic digest: `sha256:d3d982797cba3b4c0c470c8089054b57198e93f0c138144b5a0cdeb189baa3e0`

This binds the benchmark evidence to a reproducible Method-Knowledge baseline without adding the Product output back into the Knowledge input bundle or silently changing K_signal, K_response or K_manifest.

## 6. Method Policy impact

Method Policy now receives two distinct evidence states for a real Wang held-out case:

1. `TARGET_PALACE = MATERIALIZED_FACT`
2. `TARGET_CHART = BLOCKED`

This is intentionally different from the historical v0.1 state, where the case supplied only `SOURCE_REFERENCE_ONLY` chart pointers.

The source-reference materialization blocker is therefore removed for the target-palace layer.

## 7. Critical finding after materialization

Materializing target-palace evidence does **not** make the 24 Wang cases replayable.

The six source-explicit MethodPattern records currently target:

- `GLOBAL_PROFILE`
- `TEMPORAL_INFERENCE`
- `SYMBOLIC_INFERENCE`

whereas the 24 held-out cases target the twelve individual case domains such as PARENTS, LIFE, CAREER and PROPERTY.

Therefore the correct post-materialization readiness remains:

- RETRIEVAL_READY = **24 / 24**
- ACTION_SELECTION_READY = **24 / 24**
- FULL_EXPERT_REPLAY_READY = **0 / 24**

The remaining blockers are now explicit:

- full chart is not yet materialized;
- no executable source-backed MethodPattern is currently bound to the individual case target scopes.

This work unit does **not** broaden MethodPattern scopes merely to make the benchmark pass. Doing so would invent procedural semantics not established by the accepted source-method corpus.

## 8. Maturity claim

After validation, the strongest permitted claims are:

```text
Wang target-palace blind evidence = MATERIALIZED 24/24
Wang full-chart blind evidence    = NOT_MATERIALIZED
source-reference-only target data = RESOLVED FOR TARGET PALACE
deterministic CBR                 = IMPLEMENTED
Method Policy π                   = BASELINE_IMPLEMENTED_V0_1
Wang full expert replay           = NOT_READY (0/24)
method fidelity                   = NOT_VALIDATED
predictive validity               = NOT_VALIDATED
```

No case evidence is promoted to canonical Zhongzhou truth, probability, learned weight, or empirical outcome ground truth.

## 9. Validation

Required before merge:

- focused blind-evidence provenance/leakage tests;
- Method Policy regression;
- full repository pytest;
- P0 repository audit;
- Product governance validation;
- existing Product dual-engine/calendar/zi-day/temporal regression workflows.

Exact final-head evidence will be recorded on the PR.

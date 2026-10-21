# Product Knowledge Promotion — Career Response v0.16 Acceptance

Tracking Issue: #518  
Lane: PRODUCT_ONLY  
Status: **IMPLEMENTED / VALIDATION PENDING**

## 1. Scope

This work unit performs a controlled K_response-only promotion from active Product bundle v0.2 to candidate/bundle v0.3.

Promoted Knowledge inputs:

- `knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251_v0.16.json`
- `knowledge/wp08/CAREER_COMPILER_READINESS_CENSUS_26_v0.1.json`
- `knowledge/wp08/CAREER_DEPENDENCY_IR_3_v0.1.json`
- `knowledge/wp08/CAREER_DIRECT_CONDITION_IR_9_v0.1.json`

Superseded active input:

- `knowledge/wp07c/CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251_v0.13.json`

No Knowledge files are modified.

## 2. Product Knowledge impact

Deterministic impact classification:

```text
K_response = READINESS_REBUILD
K_signal   = NO_RUNTIME_EFFECT
K_manifest = NO_RUNTIME_EFFECT
K_method   = NO_RUNTIME_EFFECT
```

K_response artifact inventory changes from 19 to 22 artifacts.

Downstream propagation is bounded to:

- RESPONSE_READINESS — DIRECT;
- RESPONSE_PROFILE_TAU — IF_PRESENT;
- MANIFESTATION_M0 — IF_PRESENT;
- EMPIRICAL_DATASET — IF_PRESENT;
- CALIBRATED_MODEL — IF_PRESENT.

Natal Essence and Method Policy are not invalidated.

## 3. Readiness correction

The central semantic correction is:

```text
LOCAL_STRUCTURE_READY
!=
Knowledge condition-IR-ready
```

Knowledge #510 classifies all 26 LOCAL_STRUCTURE_READY rows:

| Compiler-readiness band | Count | Product disposition |
|---|---:|---|
| DEPENDENCY_EFFECTIVE_UNDERDETERMINED | 11 | fail closed |
| DEPENDENCY_CONDITION_IR_READY | 3 | semantic-only compiler input |
| DIRECT_CONDITION_IR_READY | 9 | semantic-only compiler input |
| DIRECT_RELATION_OR_COMPOSITION_DEFERRED | 3 | fail closed |

Therefore:

```text
Knowledge condition-IR-ready = 12
not condition-IR-ready        = 14
```

## 4. Product adapter census after promotion

```text
KNOWLEDGE_CONDITION_IR_READY_PENDING_PRODUCT_COMPILATION   12
LOCAL_STRUCTURE_NOT_CONDITION_IR_READY                     14
BLOCKED_SOURCE_UNDERDETERMINED                            157
BLOCKED_DEPENDENCY_COMPILER                                24
BLOCKED_MULTIPLE                                           44
-------------------------------------------------------------
TOTAL                                                      251
```

The 12 compiler-input-ready rows remain:

```text
condition_compiled       = false
execution_unlocked       = false
runtime_effect_allowed   = false
```

## 5. Condition IR package

Direct IR rows:

```text
CA02-181
CA03-228
CA05-411
CA05-417
CA05-419
CA05-433
CA07-638
CA07-681
CA09-820
```

Dependency IR rows:

```text
CA05-420 -> CA05-419
CA07-639 -> CA07-638
CA07-682 -> CA07-681
```

The dependency parents are included in the direct IR set. Product validates that the dependency `condition_reference` is exactly `RULE_CONDITION(parent_id)`.

## 6. Fail-closed local-ready rows

The 14 local-ready but non-condition-IR-ready rows are not silently promoted.

Eleven retain effective inherited parent uncertainty.

Three direct rows remain relation/composition-deferred:

```text
CA05-484
CA06-582
CA07-699
```

No generic 会/同会 geometry or compound relation composition is invented.

## 7. Lock / rollback

New active candidate after validation:

```text
PRODUCT_KNOWLEDGE_LOCK_V0_3
KIB-PRODUCT-20261021-V0_3
```

Previous rollback target remains immutable:

```text
KIB-PRODUCT-20261021-V0_2
```

The v0.2 bundle Git blob remains:

```text
git-sha1:a7e4222d98b7bac8883b5094d17c8ba9e025708f
```

## 8. Non-claims

This promotion does not implement or claim:

- Product condition compilation;
- runtime evidence satisfaction;
- Response Compiler;
- ResponseProfile tau;
- M0 manifestation;
- empirical probability;
- predictive validity.

## 9. Next bounded Product work

After validation and merge, the next Product work unit should be:

```text
PL3R_CAREER_CONDITION_IR_COMPILER_PILOT_V0_1
```

It should compile only the 12 promoted Knowledge condition IR rows and must preserve semantic-only / fail-closed behavior until a separate execution authorization layer is defined.

## 10. Validation

Required before merge:

- focused Product Knowledge promotion tests;
- response-semantics adapter regression;
- full repository pytest;
- deterministic P0 audit;
- Product governance validation;
- existing Product deterministic chart/calendar/zi-day/temporal regressions.

Exact final-head evidence will be recorded on the PR.

# Response Semantics Product Adapter — promoted Knowledge baseline v0.3

Status: **PRODUCT #518 CONTROLLED K_RESPONSE PROMOTION**

## 1. What changed

Product now consumes the Knowledge #510 Career response/readiness package through an explicit K_response promotion rather than reading mutable Knowledge main.

The active K_response baseline advances from:

```text
CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251_v0.13
```

to:

```text
CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251_v0.16
CAREER_COMPILER_READINESS_CENSUS_26_v0.1
CAREER_DEPENDENCY_IR_3_v0.1
CAREER_DIRECT_CONDITION_IR_9_v0.1
```

K_signal, K_manifest and K_method retain their prior semantic digests.

## 2. The key correction: LOCAL_STRUCTURE_READY is not compiler readiness

The previous Product adapter mapped every `LOCAL_STRUCTURE_READY` row to a single semantic-only pending-compilation bucket.

Knowledge #510 proves that this is too coarse.

The 26 row-local-ready Career records partition into:

```text
DEPENDENCY_EFFECTIVE_UNDERDETERMINED       11
DEPENDENCY_CONDITION_IR_READY               3
DIRECT_CONDITION_IR_READY                   9
DIRECT_RELATION_OR_COMPOSITION_DEFERRED     3
---------------------------------------------
TOTAL                                      26
```

Only the middle two bands have Knowledge condition IR:

```text
Knowledge condition-IR-ready = 12 / 26
not condition-IR-ready        = 14 / 26
```

Therefore Product v0.3 maps them as:

```text
DEPENDENCY_CONDITION_IR_READY
DIRECT_CONDITION_IR_READY
  -> KNOWLEDGE_CONDITION_IR_READY_PENDING_PRODUCT_COMPILATION

DEPENDENCY_EFFECTIVE_UNDERDETERMINED
DIRECT_RELATION_OR_COMPOSITION_DEFERRED
  -> LOCAL_STRUCTURE_NOT_CONDITION_IR_READY
```

This is a readiness distinction only. It does not compile or execute any rule.

## 3. Condition-IR-ready set

The 12 source-rule IDs admitted to the first bounded Product compiler input surface are:

```text
CA02-181
CA03-228
CA05-411
CA05-417
CA05-419
CA05-420
CA05-433
CA07-638
CA07-639
CA07-681
CA07-682
CA09-820
```

Nine are direct source-local condition IR records.

Three are exact-parent dependency IR records:

```text
CA05-420 -> RULE_CONDITION(CA05-419)
CA07-639 -> RULE_CONDITION(CA07-638)
CA07-682 -> RULE_CONDITION(CA07-681)
```

Their parent conditions are themselves present in the promoted direct IR set, so the bounded compiler-input package is self-contained for these three dependency references.

## 4. The 14 local-ready rows that remain fail-closed

Eleven rows have no local blocker but inherit source uncertainty through explicit antecedent dependencies.

Three rows are direct but still lack deterministic relation/composition semantics:

```text
CA05-484
CA06-582
CA07-699
```

These rows remain:

```text
LOCAL_STRUCTURE_NOT_CONDITION_IR_READY
```

Product does not invent generic 会/同会 geometry or compound relation composition to move them forward.

## 5. Current 251-row Product readiness

After the v0.16 promotion:

```text
KNOWLEDGE_CONDITION_IR_READY_PENDING_PRODUCT_COMPILATION   12
LOCAL_STRUCTURE_NOT_CONDITION_IR_READY                     14
BLOCKED_SOURCE_UNDERDETERMINED                            157
BLOCKED_DEPENDENCY_COMPILER                                24
BLOCKED_MULTIPLE                                           44
-------------------------------------------------------------
TOTAL                                                      251
```

The distinction between the first two lines is now machine-verifiable.

## 6. Execution boundary

All 12 condition-IR-ready rows still satisfy:

```text
Product condition_compiled       = false
Knowledge execution_unlocked     = false
Product runtime_effect_allowed   = false
```

Promotion means only:

> Product is now allowed to consume these 12 Knowledge condition IR records as inputs to a separately implemented and validated compiler.

It does not mean that compiler already exists.

## 7. Knowledge lineage

The active Product Knowledge lock advances to:

```text
PRODUCT_KNOWLEDGE_LOCK_V0_3
KIB-PRODUCT-20261021-V0_3
```

with K_response semantic change only.

The previous immutable bundle remains:

```text
KIB-PRODUCT-20261021-V0_2
```

and remains the rollback target.

The candidate-vs-active impact is:

```text
K_response -> READINESS_REBUILD
K_signal   -> NO_RUNTIME_EFFECT
K_manifest -> NO_RUNTIME_EFFECT
K_method   -> NO_RUNTIME_EFFECT
```

Future tau/M0/dataset/model effects are marked IF_PRESENT. Natal Essence and Method Policy are not invalidated.

## 8. What this enables next

The next bounded Product work may finally implement a first real PL3-R condition compiler pilot over exactly these 12 Knowledge IR records.

That pilot must still keep separate:

```text
Knowledge condition IR
-> Product compiled condition
-> runtime evidence satisfaction
-> response semantic application
-> explicit runtime authorization
-> tau output
```

No later stage may be inferred merely because the previous stage exists.

## 9. Maturity

After Product #518 validation, the strongest allowed claims are:

```text
Career K_response active baseline       = v0.16 / condition-IR aware
Knowledge condition IR ready            = 12
Product conditions compiled             = 0
Product runtime effects authorized      = 0
Response Compiler                       = NOT_IMPLEMENTED
ResponseProfile tau                     = NOT_IMPLEMENTED
predictive validity                     = NOT_VALIDATED
```

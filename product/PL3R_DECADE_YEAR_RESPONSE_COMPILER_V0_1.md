# PL3-R Decade/Year Response Compiler v0.1

Status: **IMPLEMENTED / VALIDATION PENDING**  
Issue: **#536**  
Lane: **PRODUCT_ONLY**

## 1. Purpose

This work unit introduces the first explicit Product `ResponseProfile τ_t`:

```text
NatalStateProfile N
+ TemporalEnvironmentProfile E_t
+ active locked K_response Kr
-> ResponseProfile τ_t
```

v0.1 consumes the frozen Product v0.4 temporal depth only:

```text
NATAL -> DECADE -> YEAR
```

Month/day/hour are not required by this compiler.

## 2. Current canonical-content reality

The active Product Knowledge lock is:

```text
PRODUCT_KNOWLEDGE_LOCK_V0_3
KIB-PRODUCT-20261021-V0_3
```

Its locked K_response component includes:

`knowledge/wp07b/CAREER_TEMPORAL_REACTION_ELIGIBILITY_SUMMARY_v0.1.json`

That source-reviewed audit currently states:

```text
eligible_for_current_compiler = 0
executable_pilot_emitted = false
production_registry_should_remain_empty = true
decision = NO_ELIGIBLE_SOURCE_EXPLICIT_TEMPORAL_RULE_UNDER_CURRENT_CONTRACT
```

Therefore **a real τ object can now be compiled, but no dynamic Career temporal effect can be invented or authorized**.

The correct v0.1 result is an explicit abstaining state:

```text
UNKNOWN_NO_CANONICAL_TEMPORAL_RESPONSE_RULE
```

This is not a failure of the software contract. It is the truthful representation of the current canonical-content boundary.

## 3. Inputs

The compiler accepts:

1. one `NatalStateProfile`;
2. one exact 12-row Career condition-evaluation report from
   `PL3R_CAREER_CONDITION_EVALUATOR_V0_1`;
3. one linked `TemporalEnvironmentProfile`;
4. the active Product Knowledge lock and its frozen temporal-Kr gate.

It verifies:

- `E_t.natal_profile_id == N.profile_id`;
- `E_t.knowledge_version == N.knowledge_version`;
- DECADE and YEAR are both present;
- all 12 Career evaluation IDs match the governed condition registry;
- matched effect bindings are byte-semantically equal to the governed effect-binding registry;
- all NATAL bindings remain `SOURCE_PROJECTION_SEMANTIC_ONLY`;
- current temporal Kr remains the audited zero-eligible baseline.

## 4. Output

`ResponseProfile` records:

- deterministic `profile_id`;
- N/E lineage;
- human-readable `knowledge_version`;
- active Product Knowledge bundle + K_response source commit;
- consumed DECADE/YEAR facts and provenance;
- matched NATAL source projection descriptors and source-span provenance;
- ignored higher-resolution environment layers;
- conflicts;
- dynamic effects;
- explicit response status and rationale;
- maturity flags.

Under the current lock:

```text
dynamic_effects = []
runtime_effects_authorized = 0
response_status = UNKNOWN_NO_CANONICAL_TEMPORAL_RESPONSE_RULE
probability_used = false
numeric_magnitude_used = false
feedback_used = false
outcome_used = false
empirical_calibration_used = false
```

## 5. Production-shaped service path

`run_career_response_profile(...)` now provides the first integrated path:

```text
normalized full chart
-> run_career_inference(...)
-> NatalStateProfile N
-> DECADE/YEAR TemporalEnvironmentProfile E_t
-> exact 12 Career NATAL condition evaluation
-> ResponseProfile τ_t
```

The existing production temporal reaction registry is still empty, so the high-level service returns τ with explicit UNKNOWN rather than pretending a temporal rule matched.

## 6. Fail-closed behavior

The compiler rejects:

- missing DECADE or YEAR;
- N/E lineage mismatch;
- changed or unreviewed temporal-Kr gate semantics;
- any non-empty temporal reaction under the current zero-eligible Kr baseline;
- forged NATAL effect bindings;
- runtime authorization from the NATAL evaluator;
- probability/weight/posterior or empirical state entering the profile.

If Knowledge later promotes executable temporal Kr, v0.1 intentionally fails until a new Product migration/review explicitly binds that promoted content.

## 7. Metamorphic expectations

The tests freeze these properties:

```text
same N + same E + same Kr -> same tau

same N + changed DECADE/YEAR E
-> N unchanged
-> tau identity changes

equivalent E facts + different N
-> N-specific natal semantic evidence may differ
-> tau may differ

MONTH/DAY/HOUR present
-> not required
-> not silently promoted into v0.1 response semantics
```

## 8. Maturity claim

Allowed claim after validation:

```text
ResponseProfile tau contract             = IMPLEMENTED_V0_1_FAIL_CLOSED
N + E_decade + E_year -> tau path        = IMPLEMENTED
canonical temporal Career Kr executable  = 0
dynamic response execution               = BLOCKED_BY_CANONICAL_KR
M0                                        = NOT_IMPLEMENTED
predictive validity                       = NOT_VALIDATED
production readiness                      = NOT_READY
```

This keeps “software intermediate exists” separate from “traditional temporal response content is executable”.

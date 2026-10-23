# Product Knowledge Promotion — Career Response v0.13

Status: **IMPLEMENTED — FINAL CI REQUIRED BEFORE MERGE**  
Tracking Issue: #504  
Architecture authority: Proposal #491, Product #494, Product #500

## Purpose

This work is the first real Product-side Knowledge promotion after the Knowledge
Input Bundle / lock / impact architecture was completed.

It upgrades only the Career K_response readiness inputs that Knowledge has
explicitly superseded:

~~~text
CAREER_CONTEXTUAL_ACTIVATION_CLOSURE_251
v0.3 -> v0.13

CAREER_SEMANTIC_NORMALIZATION_36
v0.1 -> v0.2
~~~

No other Product Knowledge component is promoted.

## Knowledge result consumed

Knowledge #501 closes the blocked-row deep-source review:

~~~text
251 / 251 Career activation rows covered
228 / 228 currently blocked rows deep-source-reviewed
rows with no current activation blocker = 23
source-underdetermined rows = 201
conditions compiled = 0
execution unlocked = 0
~~~

The two latest source repairs in #501 remain Knowledge-owned facts. Product does
not reinterpret them; it consumes the versioned closure.

## Product impact

Deterministic impact classification:

~~~text
K_signal   -> NO_RUNTIME_EFFECT
K_method   -> NO_RUNTIME_EFFECT
K_manifest -> NO_RUNTIME_EFFECT
K_response -> READINESS_REBUILD
~~~

Reachable downstream invalidation is recorded as:

~~~text
RESPONSE_READINESS       DIRECT
RESPONSE_PROFILE_TAU     IF_PRESENT
MANIFESTATION_M0         IF_PRESENT
EMPIRICAL_DATASET        IF_PRESENT
CALIBRATED_MODEL         IF_PRESENT
~~~

NATAL_ESSENCE and Method Policy are not invalidated.

## Rebuilt Career Response readiness

Old Product baseline:

~~~text
SEMANTIC_ONLY_PENDING_COMPILATION       17
BLOCKED_SOURCE_UNDERDETERMINED         160
BLOCKED_DEPENDENCY_COMPILER             27
BLOCKED_STRUCTURED_PATTERN_COMPILER       1
BLOCKED_MULTIPLE                        46
TOTAL                                  251
~~~

Promoted v0.13 result:

~~~text
SEMANTIC_ONLY_PENDING_COMPILATION       23
BLOCKED_SOURCE_UNDERDETERMINED         157
BLOCKED_DEPENDENCY_COMPILER             27
BLOCKED_MULTIPLE                        44
TOTAL                                  251
~~~

The change means six additional Career rows now have enough local semantic
structure to await a future compiler. It does not mean those rows execute.

Hard guardrails remain:

~~~text
runtime effects authorized = 0
condition compiled = 0
Knowledge execution unlocked = 0
~~~

## Immutable bundle transition

Previous active Product bundle is preserved unchanged:

~~~text
product/PRODUCT_KNOWLEDGE_BUNDLE_V0_1.json
KIB-PRODUCT-20261021-V0_1
~~~

New promoted bundle:

~~~text
product/PRODUCT_KNOWLEDGE_BUNDLE_V0_2.json
KIB-PRODUCT-20261021-V0_2
~~~

The active lock points to v0.2 only on the Product #504 branch. It becomes the
canonical Product active lock only if this PR passes final validation and merges
to main.

Rollback is not "edit the old file." It means selecting the previous validated
KIB together with the matching Product artifact/code set.

## NOW-6 boundary

This promotion improves Career response/readiness semantics but does not create
canonical response knowledge Kr.

The existing Response Corpus gate remains:

~~~text
compiler-ready canonical Kr = 0
NOW-6 Response Compiler input ready = false
~~~

Therefore the architecture can now absorb Knowledge updates safely, but Product
must still wait for compiler-ready Kr before implementing a real N + E + Kr ->
tau runtime.

## Validation required before merge

- candidate KIB verifies against current repository bytes;
- checked-in impact report equals deterministic comparison;
- promotion gate requires and receives READINESS_REGRESSION;
- active KIB v0.2 verifies exactly;
- Response Semantics readiness artifact equals generated output;
- Career readiness census equals 23 / 157 / 27 / 44;
- zero runtime unlock invariants remain true;
- full repository pytest passes;
- deterministic P0 audit passes;
- Product lane governance validation passes;
- existing Product regression workflows pass.

## Human Gate

None.

This work consumes already accepted Knowledge semantics. If any validation
requires inventing a new Zhongzhou meaning, the promotion must stop instead of
guessing.

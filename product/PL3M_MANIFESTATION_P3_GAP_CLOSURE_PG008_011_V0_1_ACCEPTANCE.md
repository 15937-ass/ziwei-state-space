# Product #925 — P3 Gap Closure PG-008..PG-011

## 1. Scope

This bounded Product unit addresses exactly the four Product-owned blockers discovered by P3 audit #918:

- PG-008 — accepted single-layer `DECADE` temporal binding;
- PG-009 — source-listed non-conjunctive variants without inventing an `或` token;
- PG-010 — structured simultaneous / unless / even-if condition forms;
- PG-011 — named palace-scoped dependency beyond `OPPOSITE_PALACE`.

The accepted examples are limited to KMM-000010 and KMM-000012..000015.

KMM-000001, KMM-000004 and KMM-000011 remain explicit semantic HOLDs and are not admitted to this compiler.

## 2. Versioning decision

The implementation adds:

`src/product/manifestation_condition_binding_v0_2.py`

It does **not** modify the behavior of v0.1.

This is deliberate. P3 #918 already audited the historical fact that v0.1 supported NATAL and DECADE_YEAR but not DECADE. Changing v0.1 in place would make that accepted audit irreproducible.

## 3. PG-008 — DECADE

KMM-000010 is represented with:

`DECADE -> ("DECADE",)`

The binding is exact. It does not derive age, calendar year, duration, event occurrence, valence, probability or strength.

## 4. PG-009 — listed variants without fabricated OR

KMM-000012 lists:

- 羊陀夹;
- 火铃夹;
- 空劫夹.

The canonical negative boundary explicitly states that these are separate adverse variants and must not all be required together.

The v0.2 contract therefore uses `ListedVariantSetV02` with:

`SEPARATE_VARIANTS_NOT_ALL_REQUIRED`

It deliberately keeps `source_operator_token = null`.

The compiler rejects a fabricated `或` token because `或` does not occur in the accepted source condition.

Because the non-conjunctive interpretation comes from the accepted canonical boundary rather than the literal punctuation alone, the fixture must also pin the exact canonical `forbidden_inferences` evidence text.

## 5. PG-010 — bounded structured condition forms

### KMM-000013 — branches and simultaneous condition

Three branches remain distinct:

- talent-star preference;
- 奏书 favorable clause;
- 清客 clause.

The 清客 branch retains the source-explicit `若同时` operator and both simultaneous requirements:

- 见煞;
- 昌曲化忌.

Dropping either requirement fails validation.

The branch-separation claim is additionally pinned to the canonical forbidden-inference statement that the three clauses must not be merged into one trigger.

### KMM-000014 — unless exception

The source-explicit `除非` is represented as the bounded operator `UNLESS`.

No generic condition language is introduced.

### KMM-000015 — even-if qualifier

The source-explicit `即使` is represented as the bounded operator `EVEN_IF`.

This preserves the qualifier without inferring duration, breakup, probability or severity.

## 6. PG-011 — named palace scope

KMM-000014 requires `命宫见辅弼`.

The v0.2 contract represents:

- palace scope: `LIFE_PALACE`;
- source palace token: `命宫`;
- dependency text: `命宫见辅弼`.

The compiler rejects coercion to `OPPOSITE_PALACE`.

## 7. Anti-inference controls

v0.2 has no free-text parser or keyword-driven discovery path.

A curated fixture must provide the structure, and the compiler verifies:

- exact mapping ID from the bounded allowlist;
- exact canonical source-condition text;
- verbatim retained fragments;
- exact canonical temporal layer;
- exact allowed temporal expansion;
- structured operator token exists in both source text and canonical `modality_terms`;
- canonical boundary evidence for structures whose non-conjunctive/branch-separation meaning depends on accepted negative-boundary review.

The fixture registry must contain exactly the five admitted mappings.

## 8. Production boundary

This unit does not:

- populate production manifestation registries;
- promote active KIB/K_manifest;
- authorize runtime or evaluation;
- add probability, frequency, weight, score, severity, duration, timing or causal semantics;
- claim predictive validity;
- modify Knowledge/Core semantics.

## 9. Validation

`tests/test_product_manifestation_condition_binding_v0_2.py` checks positive compilation and fail-closed negatives, including:

- DECADE cannot collapse to YEAR;
- KMM-000012 cannot receive a fabricated `或`;
- boundary evidence cannot be invented;
- KMM-000013 cannot drop one simultaneous requirement;
- structured operators cannot exist without canonical modality support;
- KMM-000014 cannot coerce LIFE_PALACE to OPPOSITE_PALACE;
- KMM-000015 cannot reinterpret `即使` as `除非`;
- v0.1 remains unchanged and reproducible;
- production registries remain empty.

## 10. Next step

Acceptance of #925 closes the known PG-008..PG-011 representation blockers for the accepted 15-KMM corpus.

It does **not** itself declare P3 frozen. A fresh P3 re-audit is required after integration.

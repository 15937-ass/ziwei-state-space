# Product #916 — Structured Condition + Temporal Binding v0.1

## 1. Purpose

This bounded Product unit addresses only the two Product-owned gaps exposed by P2:

- **PG-006** — structured condition preservation for source-explicit alternatives and cross-palace dependencies;
- **PG-007** — explicit temporal-layer preservation for `DECADE_YEAR`.

This is a compatibility/interface layer, not a production manifestation runtime.

## 2. No free-text semantic parser

The implementation deliberately avoids a generic Chinese condition parser.

A curated Product fixture must explicitly enumerate the accepted canonical mapping and the structure to retain. The compiler then verifies:

- exact `mapping_id`;
- exact canonical `source_condition_text`;
- verbatim retained fragments;
- exact canonical `time_layer`;
- governed temporal expansion;
- unresolved semantics are absent.

This prevents Product from inventing semantic atoms from prose.

## 3. PG-006

### KMM-000007 — opposite-palace dependency

The accepted source condition is retained as:

- context: `辰戌宫破军`;
- relation: `OPPOSITE_PALACE`;
- dependency text: `对宫[紫微天相]`.

The contract requires the explicit `对宫` marker. Retaining only `紫微天相` is rejected because that would erase the palace relation.

### KMM-000008 — source-explicit OR

The accepted source condition is represented as:

- context: `子午宫破军`;
- operator: `OR`;
- source operator token: `或`;
- alternatives: `廉贞化忌` / `天相为刑忌所夹`.

Changing the governed operator to `AND` fails validation.

## 4. PG-007

KMM-000009 carries canonical `conditions.time_layer = DECADE_YEAR`.

The Product contract expands that exact declared layer to two required scopes:

- `DECADE`;
- `YEAR`.

A one-layer collapse is rejected. This binding does not imply that any event occurs in either layer.

## 5. HOLD behavior

KMM-000001 and KMM-000004 remain semantic HOLDs.

The compiler refuses mappings whose canonical `unresolved_semantics` is non-empty. Product does not use this interface to choose a missing Boolean quantifier.

## 6. Production boundary

This work unit does not:

- populate production manifestation ontology/mapping registries;
- promote active KIB/K_manifest;
- authorize runtime;
- add probability, frequency, weight, score, severity, timing, or predictive-validity claims.

The existing production registries remain empty/fail-closed.

## 7. Validation

`tests/test_product_manifestation_condition_binding_v0_1.py` verifies:

- curated registry compiles exactly KMM-000007/008/009;
- opposite-palace relation cannot be dropped;
- source-explicit OR cannot become AND;
- DECADE_YEAR cannot collapse to one scope;
- source text must match canonical input exactly;
- unresolved HOLD mappings cannot enter this compiler;
- production registries remain empty.

## 8. P3

Successful acceptance of #916 removes the two known P2-only Product interface blockers, but **P3 readiness must still be re-audited after integration**. No automatic freeze claim is made by this document.

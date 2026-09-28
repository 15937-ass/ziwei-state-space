# Review / Epistemic Schema v0.3

Status: **ACTIVE — APPROVED AT GATE A0**  
Purpose: separate source support, computational normalization, and review provenance.

## 1. Source epistemic status

`source_epistemic` answers only:

> 原始来源在多大程度上直接支持 literal claim？

Allowed values:

- `EXPLICIT`
- `INFERRED_FROM_SOURCE`
- `UNRESOLVED_SOURCE`

This field must not encode whether a QI/QR mapping, operator class, target type,
or implementation choice is correct.

## 2. Normalization epistemic status

`normalization_epistemic` answers:

> 从 literal claim 到计算表示的转换属于什么性质？

Allowed values:

- `SOURCE_PRESERVING`
- `INFERRED`
- `IMPLEMENTATION`
- `HYPOTHESIS`
- `UNRESOLVED`

Definitions:

- `SOURCE_PRESERVING`: terminology-only normalization; no new theoretical relation.
- `INFERRED`: transparent research interpretation derived from the source.
- `IMPLEMENTATION`: engineering representation choice required for machine execution.
- `HYPOTHESIS`: new modeling proposition to be tested.
- `UNRESOLVED`: historical normalization has not yet been re-audited under v0.3.

Conservative migration rule:

> Historical normalized rows default to `UNRESOLVED`; do not auto-promote them.

## 3. Review status

`review_status` is independent of epistemic status.

Allowed values:

- `MODEL_EXTRACTED`
- `MODEL_SELF_REVIEWED`
- `SOURCE_SPAN_VERIFIED`
- `HUMAN_VERIFIED`

Required companion fields:

- `reviewer_type`
- `reviewer_id`
- `reviewed_at`
- `source_span_verified`
- `normalization_verified`

Historical migration:

- legacy GPT-produced `status=reviewed` -> `MODEL_SELF_REVIEWED`
- do not infer `SOURCE_SPAN_VERIFIED` from the word `reviewed`
- do not generate `HUMAN_VERIFIED` automatically

## 4. Layer boundary

State operators belong to latent / relational / structural states.

L3 semantic/event outputs should normally use `project` or an explicitly
defined projection-strength representation. Downstream event labels must not
be silently promoted to primitive qi.

## 5. Atomicity

A rule should be independently activatable whenever the source permits it.

Composite conditions are not automatically wrong, but they require review if
they combine multiple independently sufficient triggers, exceptions, outcomes,
or source sentences into a single executable record.

## 6. Enforcement

The deterministic repository auditor is a merge gate for:

- controlled-vocabulary violations,
- duplicate IDs,
- missing v0.3 epistemic/review fields,
- invalid review/epistemic enum values.

Heuristic findings such as atomicity or layer-boundary candidates remain P1
review queues and do not fail the schema gate by themselves.

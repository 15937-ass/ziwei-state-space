# Product #918 — P3 Formal Crosswalk Freeze Readiness Audit

## Verdict

**P3_NOT_READY_NEW_PRODUCT_GAPS**

The accepted Product work through #916 is materially successful: the original P1/P2 Product gaps **PG-001..PG-007 are no longer the blocker set**. The v0.2 envelope can preserve the canonical node/mapping metadata and #916 can preserve the accepted PG-006/PG-007 examples without runtime authorization.

However, the later accepted 15-KMM corpus contains additional structured condition shapes that are not covered losslessly by the current structured binding contract. Formal P3 freeze would therefore be premature.

## What is ready to freeze

### Canonical node envelope

The v0.2 node envelope preserves open `output_kind` / `event_specificity` axes, source and normalization epistemics, provenance, identity, ambiguity/unresolved notes, lifecycle and supersession without forcing a closed vocabulary.

No new KMN-side Product gap was found in KMN-000001..000015.

### Canonical mapping metadata envelope

The v0.2 mapping envelope preserves:

- mapping/source identifiers and refs;
- separate epistemic axes;
- output/event review axes;
- source condition text;
- antecedent IDs;
- modality terms;
- real-world prerequisites;
- unresolved semantics;
- execution readiness/blockers;
- forbidden inferences / negative-boundary refs;
- supersession;
- probability `UNKNOWN`.

This is preservation only and does not authorize evaluation/runtime.

### Explicit HOLD behavior

KMM-000001, KMM-000004 and KMM-000011 are not adapter failures.

They contain accepted unresolved source semantics and should remain explicit fail-closed HOLDs. A formal crosswalk may freeze those HOLD semantics as HOLD; Product must not resolve them for convenience.

## What blocks P3 freeze

### PG-008 — accepted DECADE binding

KMM-000010 has `conditions.time_layer = DECADE`.

The current #916 temporal binding allows only:

- `NATAL -> (NATAL)`;
- `DECADE_YEAR -> (DECADE, YEAR)`.

The raw layer is preserved by v0.2, but there is no governed structured binding for the accepted single-layer DECADE case.

### PG-009 — listed variants without an explicit OR token

KMM-000012 states:

`羊陀夹、火铃夹、空劫夹皆不吉`

Its accepted forbidden-inference boundary explicitly says the three variants must **not** be required together.

The current #916 alternative contract requires a source-explicit operator token such as `或`. Because KMM-000012 does not contain that token, Product cannot simply manufacture an OR token from punctuation. A separate source-listed variant-set representation is needed.

### PG-010 — structured branches / conditional modalities

KMM-000013, KMM-000014 and KMM-000015 require more than one flat condition kind:

- KMM-000013 has distinct talent-star, 奏书, and 清客 branches; the 清客 branch includes source-explicit simultaneous conditions (`若同时`);
- KMM-000014 contains an exception (`除非`);
- KMM-000015 contains an even-if qualifier (`即使`).

The current contract preserves those words as modality text but does not give them a governed structured expression. P3 must not pretend that raw-text retention is the same as a lossless structured crosswalk.

### PG-011 — named palace-scoped dependency

KMM-000014 requires `命宫见辅弼` as a distinct cross-palace exception.

The current #916 cross-palace relation supports only `OPPOSITE_PALACE`. Generalizing this silently would be an adapter inference. A bounded palace-scoped dependency shape is required.

## Mapping disposition after #916

- HOLD: KMM-000001, KMM-000004, KMM-000011.
- Lossless non-executable/preservation: KMM-000002, 000003, 000005, 000006.
- Lossless structured non-executable: KMM-000007, 000008, 000009.
- New Product gap: KMM-000010, 000012, 000013, 000014, 000015.

## Core conclusion

No new Core semantic/schema gap is required by this audit.

Core C3 already concluded `STABLE_WITH_BACKWARD_COMPATIBLE_REFINEMENT`, and the new blockers are downstream representation problems. Product must not request a Knowledge schema rewrite merely to simplify its compiler.

## Next step

Close P3 as **not ready**, then run one bounded Product-owned gap-closure unit pinned to exactly:

- KMM-000010;
- KMM-000012;
- KMM-000013;
- KMM-000014;
- KMM-000015.

That unit may extend the non-production condition-expression/binding layer for PG-008..PG-011, but it must not add a generic free-text parser, runtime authorization, registry population, probability, or predictive-validity claims.

After that unit is accepted, run a fresh P3 freeze re-audit rather than assuming readiness automatically.

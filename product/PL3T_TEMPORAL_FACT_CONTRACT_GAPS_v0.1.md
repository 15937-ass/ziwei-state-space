# PL3-T Temporal Fact Contract Gap Report v0.1

Status: **PARTIAL PRODUCT CONTRACT IMPROVEMENT — PRODUCTION REACTION REGISTRY REMAINS EMPTY**

## Scope

This is a Product-only engineering report for the existing PL3-T adapter and reaction compiler. It does not change Knowledge artifacts, normalize canonical source rules, or approve new Zi Wei semantics.

## Implemented in this work unit

The temporal asset adapter now emits a star-bound `TRANSFORMATION_PRESENT` fact **only when the normalized PL1 star object itself contains a non-empty `mutagen` field**. The emitted fact is bound to:
- the selected temporal layer;
- the corresponding palace name from the same normalized scope;
- the star name;
- the explicitly supplied mutagen.

No atom type was added. This uses the existing `TRANSFORMATION_PRESENT` atom type with a more specific, directly observed argument set.

The adapter continues to emit scope-level `TRANSFORMATION_PRESENT(layer, mutagen)` facts from the scope's `mutagen` list. It deliberately does not join that list to any star.

## What this fixes

A future normalized reaction may ask whether a particular star carries a particular transformation at a selected time layer, but only if PL1 explicitly provides that star-to-mutagen association. Regression tests verify:
1. scope-level mutagen does not become a star-bound mutagen by inference;
2. explicit star-level mutagen is preserved;
3. the reaction compiler can match the explicit bound fact;
4. the same reaction does not match when the source snapshot does not provide the association.

## Remaining gaps — intentionally unresolved

| Gap | Current state | Required next step |
|---|---|---|
| Scope-level mutagen-to-star association | Not identifiable from a scope-level mutagen list alone | Do not infer. Require direct PL1 star-level association or leave the rule blocked |
| “煞忌冲起” / activation semantics | No approved executable fact relation | Separate Product contract proposal and source-supported definition; no keyword inference |
| Compound convergence such as “凑会” | Not represented by current simple presence facts | Explicit relation/condition design, tests, and review before activation |
| “流年大运良好 / 年限不佳 / 配合” | No non-circular, source-approved predicate in current contract | Leave as UNKNOWN until the predicate is independently defined |
| Three or four consecutive favorable years | Current target model is one temporal snapshot | No duration threshold, persistence rule, timer, or probability may be inferred |
| Production temporal reaction rules | Registry remains intentionally empty | Load only after a source-faithful rule mapping is approved and normalized |

## Guardrails

- Source-reviewed text is not automatically executable.
- No `CASE_SUPPORT_ONLY` rule or antecedent is promoted.
- No new atom type, numeric gain, probability, valence, or manifestation mapping is introduced here.
- An empty production reaction registry remains an explicit partial-result condition.
- Test-only reaction matches demonstrate plumbing, not canonical validity or predictive accuracy.
- This PR modifies Product-owned code, tests, and Product documentation only.

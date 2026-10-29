# Exact `火铃同度` canonical lexical contract v0.1

Issue: #938  
Accepted source audit: #930 / PR #933 / main `e532b8b60220d6b1f722b3aa1ca54889c0cbe4cd`  
PI gate: `HG-CORE-FIRE-BELL-SAME-PALACE-EITHER-01 = APPROVED`

## Canonical decision

For **Zhongzhou sources only**, when a consumer has pinned a source span containing the exact contiguous lexical surface **`火铃同度`**, the `火铃` pair is realized by:

- 火星 satisfying the anchored `SAME_PALACE` relation; **or**
- 铃星 satisfying the anchored `SAME_PALACE` relation.

The minimum satisfied member count is one.

This is **inclusive EITHER**, not exclusive XOR:

- both required: no;
- both forbidden: no;
- exclusive-or: no.

If both 火星 and 铃星 independently satisfy the same anchored relation, the lexical condition is still satisfied. The source contract simply does not require both.

## What “同度” is bound to

The repository already defines `同度` as `EXACT_GEOMETRY / SAME_PALACE` in `knowledge/relation/RELATION_SEMANTICS_v0.1.json`. #938 does not redefine it.

The same-palace relation is between a realized Fire/Bell member and the **contextual anchor supplied by the source clause or an accepted consumer binding**. The contract never guesses that anchor.

Therefore `破军守兄弟宫，火铃同度更见空劫` may bind the exact lexical contract in a future P02-owned migration while preserving 破军/兄弟宫 as source context. It does **not** mean that 火星 and 铃星 must be co-located with each other.

## Why this does not change generic `火铃`

The historical Career pair review already closes pair membership:

`PAIR_HUO_LING = {火星, 铃星}`

but correctly leaves its generic activation default `CONTEXTUAL_UNRESOLVED`.

That default stays unchanged. #938 adds one exact-surface semantic contract backed by the direct source audit #930 and the approved PI gate. It does not establish:

`火铃 = OR(火星, 铃星)`

as a global language rule.

## P02 handoff

`P02-SB11-GAP-C04` can now be handed to P02 as:

`CORE_SEMANTIC_RESOLVED_PENDING_PALACE_OWNED_MIGRATION`.

Only the BOTH-vs-EITHER dimension for exact `火铃同度` is resolved. The historical P02 source-audit/census files remain unchanged on this Core branch. P02 must separately decide how to migrate its own held records and must preserve:

- CASE_SUPPORT_ONLY status of concrete family-history outcomes;
- all other source/gap boundaries;
- fail-closed status for any other unresolved condition component;
- no runtime/event certainty.

## Explicit exclusions

This contract does not cover bare `火铃`, `火铃夹`, `火铃同会`, `火铃会照`, `火铃二星`, or split placement such as `各安一火、一铃`.

KMM-000001 remains HOLD because its source condition is `事业宫见火铃`, without the exact `同度` surface.

## Runtime boundary

This is canonical **Knowledge lexical semantics**, not Product/runtime authorization. It creates no generic parser, no production predicate, no KIB promotion, no probability, no score, and no empirical-validity claim.

# Issue #938 execution evidence

## Accepted input

- #930 / PR #933 accepted on main `e532b8b60220d6b1f722b3aa1ca54889c0cbe4cd`.
- Source verdict: `EXACT_PHRASE_SUPPORTS_EITHER_MEMBER_READING`.
- PI gate `HG-CORE-FIRE-BELL-SAME-PALACE-EITHER-01`: APPROVED.

## Reused repository semantics

- Pair membership compatibility reference: `PAIR_HUO_LING = {火星, 铃星}` in the accepted Career pair review.
- Generic pair activation remains `CONTEXTUAL_UNRESOLVED`; #938 does not edit that historical artifact or create a global ANY default.
- Relation semantics: accepted `同度 -> EXACT_GEOMETRY / SAME_PALACE`; #938 reuses this relation unchanged.

## New canonical minimum

The exact Zhongzhou surface `火铃同度`, when explicitly pinned by a consumer, realizes at least one of the two pair members under the same anchored SAME_PALACE relation:

`ANY_MEMBER_AT_LEAST_ONE({火星, 铃星})`

This is inclusive EITHER:
- one member is sufficient;
- both are allowed;
- both are not required;
- XOR is not claimed.

The contextual anchor is not inferred by the contract.

## P02 boundary

The Core handoff marks only `P02-SB11-GAP-C04`'s Fire/Bell quantifier dimension as semantically resolved pending P02-owned migration. Core does not edit #899/#921 historical P02 artifacts.

P02S-414 / 416 / 417 remain historical CASE_SUPPORT_ONLY / held records on this branch. A later P02 unit must decide local migration and preserve all other blockers.

## Negative controls

- bare `火铃` stays unresolved;
- KMM-000001 stays HOLD;
- `火铃夹`, `火铃同会/会照`, explicit two-object wording and split placement do not inherit this contract;
- no Product/runtime/KIB/probability/event-certainty authorization.

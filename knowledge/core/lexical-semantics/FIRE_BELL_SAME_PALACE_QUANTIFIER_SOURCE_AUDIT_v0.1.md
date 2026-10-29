# 火铃同度 quantifier semantics source audit v0.1

Status: `PROPOSAL_AUDIT_ONLY_NOT_EXECUTABLE`

Issue: #930  
Activation main: `313938e0856009aed2c9233f3da3ae02dc7ae791`

## Verdict

Source verdict: `EXACT_PHRASE_SUPPORTS_EITHER_MEMBER_READING`  
Migration verdict: `SHARED_EITHER_QUANTIFIER_CANDIDATE_REQUIRES_HUMAN_GATE`

The Zhongzhou source corpus supports a narrow lexical conclusion:

> **Within the exact phrase `火铃同度`, `火铃` functions as a paired category shorthand whose minimum condition is 火星同度 OR 铃星同度. The phrase does not require both stars to be simultaneously co-located.**

This conclusion is deliberately limited to the exact `火铃同度` pattern. It does not establish a global rule for bare `火铃`, `火铃夹`, `火铃同会`, `火铃会照`, or split-palace configurations.

## 1. Direct same-context equivalence

SRC-ZZ-003 states in the 武曲贪狼 discussion:

- `火星或铃星同度最吉`;
- immediately afterwards, the same configuration is described as `武曲贪狼与火铃同度`.

This is the strongest evidence because the explicit disjunction and the compact phrase occur in the same local discussion.

Disposition: `EXPLICIT_OR_EQUIVALENCE_IN_LOCAL_CONTEXT`.

## 2. Independent decomposition

SRC-ZZ-002 states in the 机巨 discussion:

- `不喜火铃同度`;
- then distinguishes `铃星同度最坏，火星同度次之`.

The umbrella expression is therefore directly decomposed into two member cases. If `火铃同度` required simultaneous 火星+铃星, this sentence would not be a natural decomposition of the preceding condition.

Disposition: `UMBRELLA_PHRASE_DECOMPOSED_TO_MEMBER_CASES`.

## 3. Named 火贪 / 铃贪 branches

SRC-ZZ-003 states `贪狼与火铃同度，主突发`, then separately names `火贪` and `铃贪` structures.

This independently supports the paired-category shorthand reading.

Disposition: `SEPARATE_NAMED_MEMBER_STRUCTURES`.

## 4. Negative control: source can express BOTH or split placement explicitly

The source also uses more explicit forms when the two stars are intended as two separate objects:

- `破军与火星、铃星同度`;
- `火铃二星一居父母宫，一居命宫`;
- `若二者分别各安一火、一铃`.

These expressions are not normalized into `火铃同度`. They are evidence that simultaneous/two-object semantics can be expressed explicitly and must not be back-projected into the compact phrase.

Disposition: `EXPLICIT_BOTH_OR_SPLIT_PLACEMENT_DISTINCT_FROM_COMPACT_PHRASE`.

## 5. P02-SB11-GAP-C04

Source phrase:

`破军守兄弟宫，火铃同度更见空劫`.

Descriptive disposition:

`SOURCE_QUANTIFIER_CLARIFIED_EITHER_MEMBER`

The source-level ambiguity between BOTH_STARS and EITHER_STAR is resolved for the exact `火铃同度` component: either 火星同度 or 铃星同度 satisfies that lexical component.

However, #930 does not mutate the P02 ledger or compile an executable condition. The P02 record remains fail-closed until an authorized migration applies the accepted lexical contract to the palace-owned artifact.

## 6. KMM-000001 remains HOLD

KMM-000001 contains the broader phrase `事业宫见火铃`, not the exact phrase `火铃同度`.

#930 therefore does **not** resolve KMM-000001.

Disposition:

`NO_DISPOSITION_BARE_FIRE_BELL_REMAINS_CONTEXTUAL_HOLD`.

A future source audit may test bare `火铃`, but the exact-phrase result must not be widened by analogy.

## 7. Separate relation families remain separate

The following remain outside this conclusion:

- `火铃夹`: geometry/夹 relation;
- `火铃同会` / `火铃会照`: relation/convergence wording;
- `火铃二星`: explicit two-object wording;
- `各安一火、一铃`: split-placement condition;
- bare `火铃`: context-dependent shorthand.

No cross-family inheritance is authorized.

## 8. Human Gate

The source audit itself requires no PI decision.

A PI Human Gate is required before creating or applying a shared canonical/executable quantifier such as:

`FIRE_BELL_SAME_PALACE := EITHER(FIRE_STAR_SAME_PALACE, BELL_STAR_SAME_PALACE)`.

The gate is required because this would convert a descriptive lexical finding into a shared semantic primitive / canonical migration rule.

## Conclusion

The evidence is strong enough to stop treating exact `火铃同度` as lexically ambiguous. It is **not** strong enough to authorize a repository-wide executable operator without PI approval.

No Product/runtime/KIB/probability change is made in this audit.

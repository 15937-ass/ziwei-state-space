# 冲起 / 冲会 activation-semantics source audit v0.1

Status: `PROPOSAL_AUDIT_ONLY_NOT_EXECUTABLE`

Issue: #915  
Base main: `b4ea5b3e0f19047b91b04e94936c576bab49aeaa`

## Verdict

`SHARED_DESCRIPTIVE_MINIMUM_ONLY`

The source supports a narrow descriptive minimum for **冲起**, but does not support promoting either **冲起** or **冲会** into a universal executable predicate in this work unit.

### 冲起 — descriptive minimum

Across the reviewed source uses, `冲起` is a **directed activation-like relation**: a source-specified temporal/contextual factor interacts with a source-specified target so that the target's already-supported semantics become operative, salient, or strengthened.

The strongest general statement is SRC-ZZ-002, 流曜总论, printed p239: flowing 辅佐煞化 stars that 冲起 the corresponding natal 辅佐煞化 cause the two sides' force to strengthen and form a pivot for major/annual change.

This is a **special source-backed subclass**, not permission to infer that every `冲起` means:
- the same star must be on both sides;
- the same transformation must be on both sides;
- exact opposition geometry is required;
- strength always numerically increases;
- an external event is guaranteed.

Other reviewed uses include:
- 流魁流钺在三方四正冲起原局魁钺 -> the natal support becomes operative in the period;
- 禄星冲起 -> a source-stated resource function becomes able to发挥;
- different transformations/stars using 冲起 in a context-specific way;
- an unspecified 忌星冲起廉贞化忌 -> the source preserves activation wording while the triggering subject remains unknown.

Therefore the shared minimum is **descriptive activation**, while subject, target, geometry, layer, and consequence remain source-bound.

### 冲会 — separate relation family

`冲会` is not source-supported as a synonym for `冲起`.

Reviewed uses include:
- 廉贞化忌与武曲化忌冲会 without a required natal×temporal activation framing;
- 三合宫见忌冲会之流年大运;
- 流煞同会或冲会, where `同会` and `冲会` are parallel relation alternatives;
- compound adverse conditions containing 流煞冲会.

These uses support a **relation / convergence / aspect family**, but the exact geometry and binding are source-specific. `冲会` by itself does not supply the p239 `冲起 -> 力量彼此加强` semantics.

## Source-usage taxonomy

| Family | Minimum supported meaning | Stronger meaning allowed only when source states it | Executable now? |
|---|---|---|---|
| 冲起 / corresponding-flow subclass | directed activation + mutual strengthening | p239 corresponding 流曜 ↔ 原局辅佐煞化 | No |
| 冲起 / contextual activation | target becomes operative/salient under period/context trigger | target-specific effect such as 才智发挥、化禄发挥、克应候选 | No |
| 冲起 / underspecified trigger | activation wording exists but subject/binding incomplete | none; preserve UNKNOWN | No |
| 冲会 / relation geometry | source-stated relation/convergence among factors | event/risk consequence only in the complete source condition | No |
| 流煞同会或冲会 | alternative source relation branches | do not collapse OR into one generic adverse trigger | No |

## Counterexamples to over-generalization

1. **Not strict opposition.** SRC-ZZ-002 printed p7 states 流魁流钺在“三方四正”冲起原局魁钺; therefore the token `冲起` cannot be compiled as opposition-only from wording alone.
2. **Not same-star only.** Transformation passages use one transformed star to 冲起 another transformed star; same-star identity is not a universal invariant.
3. **Not universal strengthening.** p239 explicitly states strengthening for the corresponding 流曜 ↔ natal 辅佐煞化 subclass. Other passages state context-specific realization/activation and must not inherit a numeric or universal strength operator.
4. **冲会 is not 冲起.** The source uses `冲会` in same-layer and temporal relation descriptions, and sometimes contrasts `同会或冲会`; that is insufficient for an activation-equivalence claim.
5. **No subject guessing.** “有忌星冲起廉贞化忌” does not identify which 忌星. The target is readable; the triggering subject remains UNKNOWN.

## Gap dispositions

### P02-SB06-GAP-G01

Disposition: `DESCRIPTIVE_TERM_CLARIFIED_EXECUTABLE_HOLD`

- `冲起` can now be described as activation-like.
- The phrase's triggering `忌星` subject is still not identified by the source span.
- No canonical condition, formal subject binding, or executable relation is created.
- The palace record remains fail-closed.

### WP07B-GAP-003-ACTIVATION-RELATION

Disposition: `SPLIT_TERM_FAMILY_EXECUTABLE_HOLD`

- `冲起`: descriptive activation minimum is source-supported.
- `冲会`: keep as a distinct source relation/convergence family.
- Neither term currently provides a complete executable condition contract for Product.
- Existing temporal candidates blocked only by these relations remain blocked until a future work unit defines source-faithful subject/target/geometry facts and passes a Human Gate if a shared executable primitive is proposed.

## Product / runtime boundary

This audit does **not**:
- change Product temporal registries;
- populate KIB/K_manifest;
- authorize a runtime predicate;
- infer probability, strength coefficients, hazard, or event certainty;
- merge schools;
- alter canonical KMN/KMM records.

## Human Gate

No PI decision is required for this descriptive audit.

A Human Gate becomes mandatory only if a future work unit proposes:
- one shared executable `冲起` predicate;
- one shared executable `冲会` predicate;
- an exact universal geometry/binding rule;
- a universal strengthening coefficient or causal/event semantics.

## Conclusion

The useful shared knowledge is deliberately small:

> **冲起 = source-bound directed activation at the descriptive level; p239 proves mutual strengthening only for the corresponding flowing-vs-natal 辅佐煞化 subclass. 冲会 = a separate source relation/convergence family.**

That minimum is enough to improve classification and gap ownership, but not enough to enable runtime execution.

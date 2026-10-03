# WP04 Global Source-Coverage Closure Audit

状态：**WP04 SOURCE COVERAGE CLOSED**

## Scope

WP04 source-span closure now covers the Zhongzhou upper-volume operator-related chapters reviewed in this program:

- 化曜：900 items
- 杂曜：252 items
- 流曜：108 items
- 星曜庙陷：67 items
- 辅佐八曜：103 legacy catalog rules
- 六煞：81 legacy catalog rules

## Final source-review totals

- source-reviewed items: **1511**
- SOURCE_SPAN_VERIFIED: **1511 / 1511**
- ADD_CANDIDATE: **1274**
- CASE_SUPPORT_ONLY: **237**
- new primitive qi introduced by WP04 source review: **0**
- new history-memory type: **0**
- new Human Gate: **0**
- invented continuous weights / decay / fixed persistence duration: **0**

The detailed totals are recorded in `knowledge/coverage/wp04_source_verified_coverage_v0.1.csv`.

## Closure judgment

WP04's purpose was source coverage and operator-layer decontamination, not parameter identification and not predictive validation. Under that scope, the source-review gap is closed.

The resulting architecture remains:

```text
source text
  -> source-span verified literal rule
  -> audited normalization / operator candidate
  -> state / relational / gate layer
  -> palace / event projection
```

Concrete historical marriage, family, illness, occupation, punishment, gendered and severe-event labels are not promoted to primitive qi solely because they appear in the source. They remain projection/case semantics unless later modeling evidence justifies a different representation.

## Cross-chapter model findings

1. **No universal scalar for 四化 or 六煞.** Both are subject-, system-, palace- and co-star-dependent.
2. **Modifier families are structurally heterogeneous.** Pair structures, single-star states, compatibility gates, temporal activation and projection outputs must remain distinguishable.
3. **Natal × temporal interaction is source-supported.** 冲起 and multi-layer 四化/流曜 effects justify symbolic time-layer activation without a free recurrent dynamical law.
4. **庙旺平闲陷 is a discrete environment-compatibility layer.** The source supplies ordering and lookup categories, not metric distances or numeric gains.
5. **Resource, mobility, opportunity, realization and retention are separable states.** 禄、马、魁钺、空劫 and several 四化 passages repeatedly distinguish them.
6. **History memory stays sparse and typed.** Only source-explicit cross-period dependence enters A2-R1 memory.

## Non-blocking history feedback

MAL01 found one additional source-explicit cross-period statement:

- MAL01-017 -> proposed `HG-027`, `PATH_DEPENDENT_GATE`
- status: `ADD_AFTER_OPERATOR_NORMALIZATION`

This does not create a new memory type and therefore does not open a Human Gate. It joins the existing auditable feedback mechanism rather than blocking WP04 source closure.

## Provenance policy

Legacy operator catalogs are not silently rewritten just to make their historical status fields look newer. Source verification is represented by the chapter review artifacts and v0.3 review sidecars. Raw extraction provenance remains intact.

## Next work unit

**WP05 — Twelve-Palace Projection Corpus**

The next stage should build a palace-projection corpus on top of the now source-closed operator layer. WP05 should explicitly separate:

- palace semantics / scene constraints,
- natal system state,
- modifier/operator effects,
- temporal activation,
- L3 event-language projection.

WP05 must not reinterpret CASE_SUPPORT_ONLY labels as latent states by default.

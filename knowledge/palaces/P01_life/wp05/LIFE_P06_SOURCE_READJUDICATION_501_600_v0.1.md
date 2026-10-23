# P01 / WP05 — Source-first readjudication P01-501…600

## Status
- Issue: #678
- Lane: `KNOWLEDGE_ONLY`; shard: P01 / 命宫.
- Source: `SRC-ZZ-003`, 《中州派紫微斗数深造讲义（下册）》, 下篇·宫垣论·命宫.
- Historical acceleration inputs: `validation/wp05/P06_life_palace_projection_review_part1_v0.1.csv` through `part4_v0.1.csv`; these rows were not treated as canonical truth.
- Direct scan map: PDF physical p9 = printed pp17–18; physical p10 = printed pp19–20. Physical p11 begins printed p21 and the following section 13 七杀, which is the next checkpoint.

## Disposition
- Historical candidates reviewed: **100** (`P06-501…600`).
- Canonical IDs assigned after source recheck: `P01-501…600`.
- Candidate rows promoted: **100**; duplicates promoted twice: **0**.
- Source omissions supplemented: **41** (`P01-SG-168…208`).
- New canonical records in this checkpoint: **141**.
- Reusable projection rules: **125**; `CASE_SUPPORT_ONLY`: **16**.
- Cumulative accepted P01 records after merge: **788** (655 reusable; 133 case-only).

## Source-first findings and corrections

1. **巨门 (printed p17).** The old candidate set did not cover the full section. Added the remaining 辰宫化禄/文昌化忌, 戌宫化禄/化权, 巳亥分支、十二宫见禄、同巨夹化、火铃不耐久等原子主张. Preserved the source's distinction between the 亥宫 branch and the 巳宫 branch.
2. **Candidate logic repair.** `P01-515` retains the source's “不见吉曜或不见吉化，见煞” disjunction; it must not be tightened to “both absent”. Generic `宫垣`, `运限`, and `年限` are not silently narrowed to DECADE/YEAR.
3. **天相 (printed pp18–19).** Added explicit definitions of 刑忌夹印/财荫夹印, the full clamp-family effects, the 亥宫对宫武曲化忌 exception, female-chart traditional claims (case-only), four-transformation 大运流年 hinges, the clamp-sensitive hinge list, 巳亥武破/化科 branches, and 卯酉才艺/清客 conditions. Corrected the “对宫天同化忌” dependency on `P01-563/564`; it is not an adjacent-palace claim.
4. **天梁 (printed pp19–20).** Added 白虎, 子午 relationship and relative-palace branches, 午宫 plus 财帛宫 constraint, 左辅右弼/魁钺 support gate, generic 年限 hinge, 丑未天机对拱, legal-service conditions, 夫妻宫巨门 cross-palace condition, 天巫/太阳 support, 贪狼化忌 adverse branch, and the explicit 流年或大运 hinge.
5. **Ambiguous wording.** The source phrase “天梁天马陷” is retained verbatim in `P01-590`; it is not rewritten as “巳亥天梁见天马”. “第三个大运” remains an ordinal DECADE expression and is not converted to a specific age.
6. **Event claims.** Specific marriage, health, litigation, job-loss, and other concrete traditional outcomes remain `CASE_SUPPORT_ONLY` where designated. They are source claims, not empirically validated predictions, diagnoses, or modern legal/relationship advice.

## Temporal scope

- Explicit “大运” remains DECADE; explicit “大运流年” or “流年或大运” remains DECADE + YEAR.
- “年限” and “运限” remain unresolved generic period wording.
- “宫垣” references are not automatically mapped to a decade or year.
- `P01-561` preserves “流年命宫或小限”; YEAR is recorded only for the explicit 流年 term, and 小限 is not silently converted into a new independent time scale.
- “第三个大运” is retained as an ordinal DECADE phrase; no age mapping, probability, or numerical weight is introduced.

## Boundaries and validation
- No shared semantic primitive, new memory type, independent time scale, numeric weight, probability, or decay was added.
- No Knowledge Core ontology option is selected by this source audit.
- No Product/runtime authorization is implied.
- `P01-SRC-GAP-026` is closed only for the reviewed 巨门 remainder, 天相, and 天梁 span on printed pp17–20. This is **not** whole-P01 closure.

## Next source anchor

`P01-601…P01-700 source-first checkpoint: begin section 13 七杀 at printed p21 (PDF physical p11), then continue in source order; verify the original scan images and keep generic time wording, cross-palace dependencies, case-only claims, and unresolved spans explicit.`

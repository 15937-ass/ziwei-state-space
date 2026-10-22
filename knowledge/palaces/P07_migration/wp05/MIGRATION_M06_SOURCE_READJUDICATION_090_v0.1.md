# Migration M06 Source Re-adjudication 501–590 v0.1

- **Issue:** #645
- **Shard:** P07 / 迁移宫
- **Source:** SRC-ZZ-003 / 《中州派紫微斗数深造讲义（下册）》/ printed pp.119–122
- **Scan review:** PDF scan p60 (printed pp.119–120) and p61 (printed pp.121–122)
- **Candidate input:** `validation/wp05/M06_migration_projection_final_tail_501_590.csv` (read-only)

## Results

- Candidate census: **90/90**
- Canonical records: **90**
- Source conditions normalized/expanded: **90**
- Source/semantic adjudications changed: **30**
- Printed source locations corrected: **33**
- Reusable projection/method records: **77**
- `CASE_SUPPORT_ONLY`: **13**, each with row-level rationale
- Historical `PATH_DEPENDENT_GATE`: **1**; canonical gates after review: **0**
- Current-batch history-feedback rows: **0**
- Time-layer changes: **0**

## Source-page corrections

| Candidate range | Archived location | Source-verified location | Rows corrected |
|---|---|---|---:|
| M06-501…M06-518 | printed pp.119–120 | printed p119 | 18 |
| M06-567…M06-572 | printed pp.120–121 | printed p120 | 6 |
| M06-573…M06-578 | printed p121 | printed p120 | 6 |
| M06-587…M06-589 | printed pp.121–122 | printed p121 | 3 |
| **Total** | | | **33** |

The page map was checked against the rendered scan: scan p60 contains printed pp.119–120; scan p61 contains printed pp.121–122. The p122 page opens the 交友宫（旧称奴仆宫） chapter. Candidate page labels were treated as indexing hints, not evidence.

## Major source adjudications

- **M06-501…518 — 七杀 completion:** retained the source's separate 羊陀、火星、铃星、空劫 and 禄存 contexts, plus the Life-Palace 天府 cross-palace constraint. 工艺/工业 is a source-attributed modern scene, not a guaranteed occupation.
- **M06-514/515:** the source lists 火铃、空劫 together and then adds “或主飘荡无依”. The canonical conditions do not assert that the latter outcome is caused by 空劫 alone.
- **M06-519…539 — Qisha cross-palace structures:** preserved 武曲/廉贞/紫微 opposition or co-presence, the distinct Chou/Wei 廉杀 structure, and the relative (not absolute) 酉优于卯 comparison.
- **M06-540…542 — flowing-year Qisha:** only these three rows use `YEAR`. The source's listed 廉贞化忌、武曲化忌来会 wording is preserved without inventing an OR branch.
- **M06-543…578 — 破军 general structure:** retained the baseline unfavorable migration statement, the Tianxiang clamp exceptions, specialized-skill requirement, differentiated 四煞 branches, and the distinct 子午 / 丑未 structures.
- **M06-551:** the sentence “破军、文曲同度，化忌” is kept at combination level; no new transformation-attribution rule is invented.
- **M06-579/580:** the source's awkward punctuation/line sequence concerning a major disaster or death away is a result sequence under the fully stated 寅申破军 + 武曲化忌冲拱 + adverse-star condition. It is **not** an observed prior-user-history activation gate. Both severe outcomes remain `CASE_SUPPORT_ONLY`.
- **M06-587…589:** explicitly separates unfavorable rooted settlement away without 化禄 from source-described mobility between places to earn a living.
- **M06-590:** marks the chapter boundary only; it does not become a migration outcome rule.

## CASE_SUPPORT_ONLY rows

- **M06-521** — 源文直接列出灾祸这一具体严重事件；仅保留为源文支持的事件候选，不升格为可执行或确定性预测。
- **M06-522** — 源文直接列出疾病这一具体事件；仅保留为源文支持的事件候选，不推导发生概率或时间。
- **M06-523** — 源文直接列出词讼这一具体事件；仅保留为源文支持的事件候选，不作确定性预测。
- **M06-529** — 源文在廉贞化忌分支列出意外；保留为条件化事件候选，不推导发生率。
- **M06-530** — 源文将天月同度与异乡染病相连；疾病为具体事件候选，限制为案例支持。
- **M06-531** — 源文将天刑同度与祸生不测相连；严重事件候选仅作案例支持。
- **M06-542** — 流年七杀分支下，化忌会合且见煞对应出门意外；属于具体事件候选，不作确定性年度预测。
- **M06-560** — 源文在破军与四煞同度且煞重时提及灾祸频仍；严重结果保留为案例支持。
- **M06-572** — 源文在子午破军见廉贞化忌分支提及自身灾病；仅保留为案例支持的事件候选。
- **M06-579** — 源文在寅申破军、武曲化忌冲拱及多重煞曜同会的完整条件下列出重大灾祸；不得改写成确定性预言。
- **M06-580** — 源文进一步列出死于异乡的极端结果；只保留为案例支持，不作确定性死亡预测。
- **M06-583** — 源文在廉贞破军、廉贞化忌且煞重时列出客中意外；仅作案例支持。
- **M06-586** — 源文在武曲破军并会廉贞化忌时列出灾病；仅作案例支持。

## Remaining source gaps

The following six gaps remain explicit and are not silently closed by M06:

1. **P07-M05-GAP-001** — printed p118: 天相与廉贞同度/对拱的 adverse Sha/Ji/Kong/Jie/Xing/Hao and litigation branch.
2. **P07-M05-GAP-002** — printed p118: 廉相守迁移、命宫破军化权；区分廉贞化禄跨两地事业与廉贞化忌宜留出生地。
3. **P07-M05-GAP-003** — printed p118: complete 天相 财荫夹 / 六吉夹 taxonomy and differentiated outcomes.
4. **P07-M05-GAP-004** — printed p118: general good-clamp/bad-clamp effects plus 文曲+桃花 and 羊陀+禄存+double-化禄 branches.
5. **P07-M03-GAP-001** — printed p115: 太阴与辅弼同度, source says help from others; 魁钺 is not a substitute for 辅弼.
6. **P07-M03-GAP-012** — printed p114: 廉贞守迁移见财荫夹, outside this source span.

M06 reaches the printed-p122 chapter boundary, but **P07 is not yet fully source-closed** while these gaps remain unresolved or unaccepted as residual gaps.

## Temporal and governance boundary

- Preserve only `NATAL / DECADE / YEAR / MONTH`; M06's only source-explicit flowing-year rows are M06-540…542.
- Preserve `MIGRATION_FIRST_THREE_YEARS` / `HG-P07-TEMPORAL-01-A` unchanged.
- No new qi primitive, history-memory type, shared semantics, independent time scale, generic event timer, probability, numeric weight, threshold, decay, causal claim, or Product runtime permission.
- Historical cumulative checkpoint: 500 reviewed / 443 reusable / 57 case-only. After this independently reviewed batch: **590 reviewed / 520 reusable / 70 case-only**.
- The prior canonical history-feedback gate count remains 10; M06 adds none.

## Validation status

Source review artifacts are prepared on the Issue branch. Merge remains blocked until the exact final PR head passes targeted tests, full repository pytest, Product JS adapter checks, deterministic P0 audit, Repository Governance v1, and exact-main/base/head comparison.

# Migration M05 Source Re-adjudication 401–500 v0.1

- **Issue:** #619
- **Shard:** P07 / 迁移宫
- **Source:** SRC-ZZ-003 / 《中州派紫微斗数深造讲义（下册）》/ printed pp. 117–120
- **Scan review:** PDF scan p59 (printed pp.117–118) and p60 (printed pp.119–120)
- **Candidate input:** `validation/wp05/M05_migration_projection_review_401_500.csv` (read-only)

## Results

- Candidate census: **100 / 100**
- Canonical records: **100**
- Conditions expanded/normalized: **100**
- Source-resolution changes: **56**
- Source locations corrected: **41**
- Reusable projection rules: **90**
- `CASE_SUPPORT_ONLY`: **10**, each with a row-level rationale
- Historical `PATH_DEPENDENT_GATE`: **2**; canonical gates: **0**
- M04 source gaps closed: **3**
- New printed-p118 source gaps: **4**
- Time-layer changes: **0**

## Source-page correction

The historical candidate CSV labels M05-401..404 as pp.117–118, M05-405..418 mostly as p118, M05-456..461 as pp.118–119/p119, and M05-490..500 as pp.119–120. Direct scan review shows:

- M05-401..418: printed p117
- M05-419..423: printed pp117–118
- M05-424..460: printed p118
- M05-461: printed p118
- M05-462: printed pp118–119
- M05-463..500: printed p119

Printed p117 overlaps the M04 span. This is intentional: M05-401..409 close three exact source gaps left by M04; they are not independent duplicate evidence.

## M04 gap closure

- `P07-M04-GAP-001` → M05-408/409: Jumen with Lu Cun / flowing Lu and no auspicious transformations/support.
- `P07-M04-GAP-002` → M05-401..404: Mao/You empty Life Palace opposing Tianji–Jumen and its Sha/Ji/general branches.
- `P07-M04-GAP-003` → M05-405..407: flowing-year Jumen in Migration, separating Lu permission, Sha effort-cost, and combined Sha/Ji/Xing/Hao event candidate.

The merged M04 audit remains immutable; the mapping is recorded in this M05 artifact.

## Major source adjudications

- **M05-423:** image review corrects OCR “怨罔刑耗诸星同会” to “煞曜刑耗诸星同会”. The Yang/Tuo, Fire/Bell, and Kong/Jie clamp branches remain alternatives.
- **M05-431:** expands “前述武相重凶结构” into four alternative conditions; the source's severe “客死异乡” outcome remains case-bound.
- **M05-447/448:** both inherit the full source condition “天梁与魁钺、辅弼同会”; the source grammar is not silently changed to alternatives.
- **M05-455/487:** historical personal-history gates are removed. “虽终能化解” and “因祸得福” are outcome sequences within the source condition, not prior-user-history activation gates. M05-455 remains CASE_SUPPORT_ONLY because it is tied to a specific wrongful-imprisonment scenario.
- Modern scene translations (large-enterprise administration, mobile arts/skills, academic or engineering research, overseas study) remain attributed to the source and are not universal occupational guarantees.

## Remaining source gaps

Four unrepresented printed-p118 Tianxiang claims remain explicit:

1. Same-degree Tianxiang–Lian Zhen adverse structure and its Sha/Ji/Kong/Jie/Xing/Hao litigation branch.
2. The separate Lianxiang branch: Life Palace Po Jun Hua Quan plus Lian Zhen Hua Lu permits a two-location career in the modern reading; Lian Zhen Hua Ji favors staying at the birthplace.
3. Full Tianxiang clamp taxonomy (Cai-Yin and the six auspicious clamps) with its differentiated outcomes.
4. General good-clamp/bad-clamp effects and the specific Wenqu+peach-blossom and Yang/Tuo+Lu Cun+double-Hua-Lu branches.

No new rule IDs were invented for these gaps. The two unrelated M03 gaps (Taiyin–Fu Bi on p115 and Lian Zhen–Cai Yin on p114) remain carried forward outside this source span.

## Temporal and governance boundary

- Preserve only `NATAL / DECADE / YEAR / MONTH`.
- Preserve `MIGRATION_FIRST_THREE_YEARS` / `HG-P07-TEMPORAL-01-A` unchanged.
- Flowing Jumen, flowing Lu, flowing Tianxiang and flowing Tianliang branches retain source-specific YEAR scope; no generic event timer is added.
- No new qi primitive, history-memory type, shared group semantics, probability, numeric weight, decay, causal claim, or Product runtime permission.
- No Product, Core, Governance or other-palace paths changed.

## Cumulative counts after M05

- Reviewed: **500**
- Reusable projection rules: **443**
- `CASE_SUPPORT_ONLY`: **57**
- Canonical history-feedback gates: **10**

These counts are recalculated after reclassifying M05-455 as case-bound and removing the two historical personal-history gate flags; they differ from the older historical M05 summary.

## Next source anchor

Re-adjudicate M06-501..590 against printed pp.119–122, beginning with the remaining Qisha branches, then the complete Pojun section and the chapter boundary. Keep the four p118 Tianxiang gaps in the ledger for a bounded follow-up; do not mark the chapter fully closed until they are explicitly resolved or accepted as residual gaps.

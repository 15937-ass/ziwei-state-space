# Migration M04 Source Re-adjudication 301–400 v0.1

- **Issue:** #601
- **Shard:** P07 / 迁移宫
- **Source:** SRC-ZZ-003 / 《中州派紫微斗数深造讲义（下册）》/ printed pp. 115–117
- **Scan review:** PDF p58 (printed pp. 115–116) and p59 (printed pp. 117–118)
- **Candidate input:** `validation/wp05/M04_migration_projection_review_301_400.csv` (read-only)

## Results
- Candidate census: **100 / 100**
- Canonical conditions normalized: **60**
- Substantive source-resolution changes: **40**
- Source-location corrections: **29**
- Time-layer corrections: **0**
- Reusable projection rules: **91**
- `CASE_SUPPORT_ONLY`: **9**, each with a row-level reason
- Historical `PATH_DEPENDENT_GATE`: **2**; canonical gates: **0**
- New source-coverage gaps: **3**; carried-forward M03 gaps: **2**

## Source-page correction

The historical CSV incorrectly labels M04-301..M04-326 as printed p116. The scan shows M04-301..324 on printed p115, M04-325/326 across pp115–116, M04-327..368 on p116 and M04-369..400 on p117. Canonical records preserve the archived location and correct it. Printed p118 begins the next 天相 section and is outside this batch.

## M03 gap closure

M04-301..328 close the matching earlier gaps: M03-GAP-002 → M04-301; GAP-003 → M04-302/303; GAP-004 → M04-304/305; GAP-005 → M04-309 (still CASE_SUPPORT_ONLY); GAP-006 → M04-312..314; GAP-007 → M04-315..319; GAP-008 → M04-320..323; GAP-009 → M04-324; GAP-010 → M04-325/326; GAP-011 → M04-327/328. M03-GAP-001 (Taiyin–Fu Bi) and M03-GAP-012 (Lian Zhen–Cai Yin clamp, printed p114) remain open.

## Major source adjudications

- **M04-327/328:** correct the candidate's 太阴 to the source's 太阳 for “太阳会天同化禄” and “会天机化禄”. “事业更张后即见鼎盛” is a sequence within the source claim, not a personal-history gate.
- **M04-319:** keep the separate “若太阴化忌则主无端纷扰破财，或受引诱破财” branch separate from M04-318's Solar–Taiyin + Sha/Xu-Hao/Xing dispute branch.
- **M04-325/326:** preserve the complete compound trigger: Taiyin Hua Ji, flowing-year/major-period Hua Ji activation, double Tuo Luo or double Qing Yang, or two layers of Yang/Tuo clamp, and further void/consumption stars. YEAR and DECADE are alternatives within one source clause.
- **M04-328/349:** remove the historical PATH_DEPENDENT_GATE flags. Both describe a sequence inside a traditional conditional claim, not a rule that requires prior user history.
- **M04-368:** correct NATAL to YEAR and retain the full annual antecedent: original Sha activated by flowing Sha, plus Tai Sui/Sui Po/Guan Fu/Da Hao and additional year stars.
- **M04-388/389:** correct NATAL to DECADE/YEAR. These are temporal modifiers of the same Jumen/Sun base, not generic event timers.
- **M04-377:** the favorable Lu/Hua Lu + auspicious-support branch does not cover the missing adverse “no auspicious support” source clause.
- The 9 concrete event claims remain CASE_SUPPORT_ONLY: M04-309, 314, 325, 326, 344, 345, 354, 363, 368.

## New source gaps
1. 巨门与禄存同度/流禄同度但缺少吉化吉曜时，出门受小人掣肘。
2. 卯酉命宫无正曜、对宫天机巨门所构成的移根换叶/离乡发展条件。
3. 流年巨门守迁移，见禄、见煞及煞忌刑耗凑会的年度分支。

The gaps are not executable rules and receive no invented IDs beyond the gap ledger.

## Temporal and governance boundary
- Preserve only `NATAL / DECADE / YEAR / MONTH`.
- Preserve `MIGRATION_FIRST_THREE_YEARS` / `HG-P07-TEMPORAL-01-A` unchanged.
- No new qi primitive, history-memory type, shared group semantics, probability, numeric weight, decay, causal claim or Product runtime permission.
- No Product, Core, Governance or other-palace paths changed.

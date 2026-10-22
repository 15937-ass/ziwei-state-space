# Migration M06 Source Re-adjudication 501–590 v0.1

- **Issue:** #645
- **Shard:** P07 / 迁移宫
- **Source:** SRC-ZZ-003 / 《中州派紫微斗数深造讲义（下册）》/ printed pp. 119–122
- **Scan inspection:** PDF scan p60 (printed pp.119–120) and p61 (printed pp.121–122)
- **Candidate input:** `validation/wp05/M06_migration_projection_final_tail_501_590.csv` (read-only)

## Results

- Candidate census: **90 / 90** (`M06-501…M06-590`)
- Canonical rule records: **89**
- Chapter-boundary markers (not projection rules): **1** (`M06-590`)
- Reusable projection rules: **76**
- `CASE_SUPPORT_ONLY`: **13**, each with a row-level rationale
- Conditions normalized: **89**; “前格” shorthand expanded: **24**; unresolved “前格”/“前述” shorthand: **0**
- Source wording ambiguity preserved: **1** (`M06-503`; not a coverage gap)
- Source locations corrected: **33**
- Source-resolution changes: **48**
- Historical `PATH_DEPENDENT_GATE`: **1** (`M06-579`); canonical gates: **0**
- Explicit YEAR rows: **M06-540, M06-541, M06-542**
- New source-coverage gaps in pp.119–122: **0**
- Carried-forward source gaps: **6** (four printed-p118 Tianxiang gaps plus two M03 gaps)
- New primitive / memory type / time scale / shared semantics / weight / probability / decay / Product runtime permission: **0**

## Source-page corrections

Direct scan inspection establishes:

- `M06-501…M06-518`: printed p.119, not pp.119–120.
- `M06-519…M06-578`: printed p.120.
- `M06-579…M06-589`: printed p.121.
- `M06-590`: printed p.122, where the next chapter, 交友宫（奴仆宫）, begins.

The candidate's labels for M06-567…572, M06-573…578 and M06-587…589 were corrected. Page correction is provenance repair, not an additional rule or independent evidence.

## Major source adjudications

- **Qisha movement is conditional.** 七杀 alone does not imply relocation. The text names 火铃同度（或火铃与命宫同度）或禄马交驰 as movement-related conditions, while the remaining Qisha branches distinguish external authority, instability, gain/loss, and location/occupation scene translations.
- **Source clauses are not silently rewritten.** M06-514/515 preserve the distinct source groups “火铃” and “空劫” without decomposing them into unsupported single-star OR conditions. M06-542 retains the source wording “廉贞化忌、武曲化忌来会，见煞”; the artifact does not silently change it into an OR branch.
- **Cross-palace constraints remain explicit.** The 命宫天府 / 天相 conditions are not flattened into generic migration scores. The source's special relation “羊陀夹天相 → 禄存同度且与破军对拱” remains attached to M06-547.
- **M06-551 preserves textual scope.** The source says “破军、文曲同度，化忌” without explicitly naming the star to which 化忌 attaches; the condition records that ambiguity rather than forcing an unsupported attribution.
- **M06-503 preserves scan uncertainty.** The scan reads “在迁移宫的驻突发”; the exact wording is uncertain. Only the broad “突发” scene is retained, with no inference of a specific accident or injury.
- **Specialized skill is a constraint, not a deterministic job title.** Modern technical/craft and historical performing/itinerant scenes remain attributed source translations. The “异邦开家乡菜馆” phrase is an illustrative example, not a guaranteed occupation or business outcome.
- **Severe event claims remain bounded.** The 13 CASE_SUPPORT_ONLY rows cover source-specific disaster, illness, legal-trouble, accident, or death-away outcomes. None is converted into a deterministic forecast, probability, hazard rate, or interval.
- **M06-579 is not a personal-history activation gate.** The source orders “迁居异地” and a subsequent major-disaster claim within the same star-system statement. It does not require the system to first observe an already-completed personal relocation before representing that source condition. The historical gate flag is therefore removed; the major-disaster outcome remains CASE_SUPPORT_ONLY.
- **M06-590 is a boundary marker.** It records the start of the next chapter only. It is not promoted as a P07 inference rule and does not import P08 content.

## Cumulative count reconciliation

The legacy `M06_MIGRATION_FINAL_TAIL_REVIEW.md` states cumulative **521 reusable / 69 CASE_SUPPORT_ONLY**. That count is not accepted as canonical because it predates the accepted M05 recount (443 reusable / 57 CASE_SUPPORT_ONLY) and counts M06-590's chapter boundary as a reusable projection.

The source-first accounting is:

| Category | Before M06 | M06 | After M06 |
|---|---:|---:|---:|
| Reviewed candidates | 500 | 90 | 590 |
| Reusable projection rules | 443 | 76 | **519** |
| CASE_SUPPORT_ONLY | 57 | 13 | **70** |
| Boundary markers (not rules) | 0 | 1 | **1** |
| Canonical personal-history gates | 10 | 0 | **10** |

The category totals reconcile: **519 + 70 + 1 = 590**. This is a census correction, not a source-meaning change to prior accepted batches.

## Remaining source gaps

No new gap was identified in printed pp.119–122. These remain open and explicitly carried forward:

- Four printed-p118 Tianxiang gaps from M05.
- `P07-M03-GAP-001` (printed p.115).
- `P07-M03-GAP-012` (printed p.114).

M06 does not close those gaps because its source scope begins at printed p.119. Do not advance to P08 until P07 source-first closure is completed or residual gaps are explicitly accepted.

## Temporal and governance boundary

- Preserve only `NATAL / DECADE / YEAR / MONTH`.
- Only M06-540…542 are explicit YEAR rows.
- Preserve `MIGRATION_FIRST_THREE_YEARS` / `HG-P07-TEMPORAL-01-A` unchanged.
- No new qi primitive, memory type, shared group semantics, time scale, probability, numeric weight, decay, causal claim, or Product runtime permission.
- A canonical source projection is not automatically executable or production-authorized.

## Validation status

Source review and deterministic artifact generation are complete. **Do not claim acceptance until the exact final PR head passes** targeted tests, full repository pytest, Product JS adapter checks, deterministic P0 audit, Repository Governance v1, and exact-main/base/head comparison. Record actual run references and counts after those checks execute.

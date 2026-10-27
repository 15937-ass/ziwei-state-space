# P03 SP02 — source-first re-adjudication of spouse candidates 101–200

**Status:** source review complete. Exact-head validation status is authoritative in the live [PR #796](https://github.com/15937-ass/ziwei-state-space/pull/796) and its matching GitHub Actions run; this file does not claim CI status.  
**Issue:** #794  
**Lane / shard:** `KNOWLEDGE_ONLY / P03 夫妻宫`  
**Source:** `SRC-ZZ-003`, 《中州派紫微斗数深造讲义（下册）》, 下篇·宫垣论·夫妻宫  
**Approved scan SHA-256:** `6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c`  
**Historical index SHA:** `0bc7a6f9c03790cf8b7c610a19ca55d78b3cf007`

## Source boundary

The original scan images for PDF physical pages 18–19 were inspected directly. The audited candidate span is printed pp35–37. Physical p18 contains printed pp35–36; physical p19 contains printed pp37–38. The local PDF SHA-256 was recomputed and matches the approved source pin. Text extraction was used only as a locator; the scan images are authoritative.

The historical index `validation/wp05/SP02_spouse_projection_review_101_200.csv` is read-only acceleration input. Its 100 `SOURCE_SPAN_VERIFIED` flags and historical 88/12 split are not accepted proof or target counts.

## SP02-101…200 result

| Measure | Result |
| --- | ---: |
| Historical candidate rows directly reviewed | 100 |
| Candidate rows promoted as source-grounded records | 77 |
| Source records produced | 77 |
| Reusable projection/method records | 60 |
| `CASE_SUPPORT_ONLY` records | 17 |
| Held for unsupported time-layer specificity | 23 |
| Deduplicated rows | 0 |
| Historical feedback | 0 |
| New shared semantics / primitives / quantitative weights | 0 |

All 100 historical IDs have an explicit disposition and reason. A held row does not mean the source clause is false; it means the historical mapping exceeds what the scan establishes, most notably by assigning YEAR where the source does not name YEAR versus DECADE.

## Important corrections and condition preservation

- **SP02-101:** directly confirms `见煞忌亦主离异`; this is separate from the earlier 火铃 and 禄马 branches.
- **SP02-102 / SP02-103:** record `禄权科会` and the simultaneous `巨门化忌` qualification separately. The latter remains source-stated guidance; the grammatical subject of `自我克制` is not invented.
- **SP02-104–106:** retain the 对宫天梁 prerequisite, the source's early-marriage/divorce OR delayed-marriage/premarital-setbacks branches, and `见空劫者尤然` as an intensifier.
- **SP02-118 / SP02-150 / SP02-189:** correct targets to preserve all source-stated outcomes: wife beauty plus support, spouse refinement plus career capability, and wife's-family support plus general spousal support.
- **SP02-136:** restore the source's `否则生离` branch instead of truncating the historical target to late marriage/premarital turbulence.
- **SP02-108 / SP02-111:** narrow `尚可` and `为佳`; neither is upgraded into a strong guarantee of marital stability.
- **SP02-121:** the source says `易空劫、阴煞、天虚、大耗等曜`; the historical `及` could overstate an all-required AND. The list quantifier remains explicitly unresolved.
- **SP02-137–141:** preserve the age-difference qualification and the explicit `大限夫妻宫` conditions.
- **SP02-164–167:** preserve the source's late-marriage recommendation, night-birth intensifiers, age-after-30 condition, and the precise `有名无实` phrase.
- **SP02-179:** keep the author's explicit distinction between the ancient `因妻得贵` formulation and the modern `妻子有良好事业` formulation.
- **SP02-183–192:** preserve the source's severity branches, OR alternatives, sex-specific conditions only where stated, and the relative comparison between 丑 and 未.
- **SP02-199:** restore the source's `见煞，但不重` qualifier.

## Temporal-scope residuals

The following historical YEAR assignments are held rather than compiled because the source does not specify a unique YEAR/DECADE layer:

- SP02-113…117 — `经行宫垣` / `吉凶枢纽`
- SP02-122…125 — `四垣为吉凶之枢纽`
- SP02-128…129 — `克应之期`
- SP02-135 — `[武曲天府]限为关键`
- SP02-153…155 — `吉凶克应之枢纽`
- SP02-169…170 — `不宜行巨门、[武破]二垣`
- SP02-175 — `夫妻宫行至天同坐守之垣时`
- SP02-180…181 — `不喜行天同、[廉杀]二垣`
- SP02-193…195 — `吉凶克应的枢纽`

Prior temporal residuals SP01-091…092 and SP01-097…098 remain open; the current source span does not justify forcing their layer.

## Source-coverage gap reconciliation

- **P03-SP01-GAP-001 (printed p33):** carried forward; outside this batch.
- **P03-SP01-GAP-002 (printed p35):** resolved by SP02-101.
- **P03-SP01-GAP-003 (printed p35):** resolved by separate SP02-102 and SP02-103 records.
- **P03-SP01-GAP-004 (printed p35):** resolved by the narrowed SP02-104 record.
- **P03-SP02-GAP-001 (printed p37):** carry forward the `[太阳巨门]` no-Sha / transit-to-`[机录像]`, 刑忌夹天相 and 同阴 palace clause. The scan wording is retained as transcribed; the transit layer remains unresolved.
- **P03-SP02-GAP-002 (printed p37):** carry forward the `[太阳巨门]` auspicious-transformation + 福德宫不吉 clause, with its sex-specific outcomes.
- **P03-SP02-GAP-003 (printed p37):** carry forward the `[太阳巨门]` auxiliary-auspicious-stars clause, with its sex-specific outcomes.

The index range SP03-201…236 is only a pointer for the next batch; it has not been source-audited in this Issue.

## Execution boundary

- `conditions_compiled=0`; `execution_unlocked=0`.
- No Product/runtime authorization, shared Core semantic change, other-palace write, history-feedback promotion, new qi/memory/time primitive, numeric weight, probability, or decay.
- P03 is **not complete** after this batch. The next P03 batch must inspect SP03-201…300 from the original scan and reconcile the five printed-pp35–37 source gaps before the palace stage can be closed.

## Duplicate-delivery recovery and repair — 2026-10-26

PR #796 is the single recovery implementation for Issue #794. PR #795 remains
historical comparison evidence, not a second accepted batch. The two deliveries
must never be added together.

Direct reinspection of original physical pp18–19 confirms the relevant source
clauses. Keep #796's 77-record representation, including the complete compound
P03S-190 health/heavy-sha/separation clause as one CASE_SUPPORT_ONLY record.
#795 split that same clause into three records; this accounts for its 79 versus
77 records and does not identify two additional independent source clauses.
Retain #795's conservative CASE_SUPPORT_ONLY boundary for P03S-132/145/151/152/183.
The reconciled partition is therefore 60 reusable and 17 case-only; cumulative
SP01 + SP02 totals are 167 records = 135 reusable + 32 case-only, with 32 held
candidate rows and 2 deduplications across 200 reviewed candidates.

Keep #796 GAP-001…003 and append #795's p35 female-chart complete-condition gap
as GAP-004 and p36 general Tianji baseline gap as GAP-005. The p37 申宫/寅宫
comparison is already explicit in GAP-001. There are nine gap entries: three
resolved and six open (including the p33 carry-forward); all remain traceable.
The anomalous printed-p37 string is visibly `机录像`; its interpretation is
UNRESOLVED. The former `机梁紫破` substitution is withdrawn, not accepted as source.

The obsolete SP01 state test now reconciles exact cumulative counters from all
source-review batch ledgers and rejects duplicate candidate IDs. SP01-specific
source, condition, temporal and boundary tests remain pinned to its own artifact.
The state typo is corrected to 12 temporal residual groups (two prior plus ten
new). No historical CSV, shared Core semantics, or Product/runtime is changed.

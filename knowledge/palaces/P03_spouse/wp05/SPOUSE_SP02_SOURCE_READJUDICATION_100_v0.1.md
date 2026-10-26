# P03 SP02 — source-first re-adjudication of spouse candidates 101–200

**Status:** source review complete; exact-head repository validation pending.  
**Issue:** #794  
**Lane / shard:** `KNOWLEDGE_ONLY / P03 夫妻宫`  
**Branch:** `knowledge/p03-794-spouse-audit-sp02`  
**Source:** `SRC-ZZ-003`, 《中州派紫微斗数深造讲义（下册）》, 下篇·宫垣论·夫妻宫  
**Approved scan SHA-256:** `6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c`

## Source boundary and historical inventory

The original scan images for PDF physical pp18–19 were directly inspected. They contain printed pp35–38: physical p18 contains printed pp35–36; physical p19 contains printed pp37–38. This batch re-adjudicates exactly SP02-101…SP02-200, whose historical claims fall on printed pp35–37. Text extraction was used only as a locator; the original scan is authoritative. The supplied PDF SHA-256 matches the approved source pin.

The nine historical CSV indexes remain read-only acceleration inputs. Their `SOURCE_SPAN_VERIFIED` labels are historical assertions, not canonical evidence. The full P03 section remains printed pp33–51 / PDF physical pp17–26.

## SP02-101…200 result

| Measure | Result |
|---|---:|
| Historical candidate rows directly reviewed | 100 |
| Candidate rows promoted after source review | 77 |
| Source records produced | 79 |
| Reusable projection/method records | 60 |
| `CASE_SUPPORT_ONLY` records | 19 |
| Held with explicit temporal-scope reason | 23 |
| Deduplicated rows | 0 |
| Historical feedback | 0 |
| Open source-coverage residuals carried | 7 |
| Temporal-scope residual groups | 10 (covering 23 held candidate IDs) |

The record count is 79 rather than 77 because SP02-190 combines three distinct source outcomes: husband health adversity, “煞重则见刑克”, and “否则生离”. They are represented separately so the conditions and outcomes are not collapsed.

## Carry-forward reconciliation from SP01

- **P03-SP01-GAP-002 — resolved:** SP02-101 directly matches the source wording `见煞忌亦主离异`.
- **P03-SP01-GAP-003 — resolved:** SP02-102 records the `禄权科会` branch; SP02-103 separately records the `同时见巨门化忌` qualification. These are not merged into one undifferentiated condition.
- **P03-SP01-GAP-004 — resolved:** SP02-104 directly rechecks `丑未天机独坐，对宫为天梁，于夫妻宫有所不宜` and retains both the early-marriage/divorce and late-marriage/premarital-setback branches.
- **P03-SP01-GAP-001 — still open:** it lies on printed p33, outside this batch’s direct source span. Its trigger quantifier remains unspecified.

## Important source-first corrections

- **SP02-104 / 108 / 111:** targets are narrowed to source wording. “尚可” is not promoted to a guarantee of marital harmony, and premarital turbulence is not treated as a guarantee of later stability.
- **SP02-121:** retains the source’s list “空劫、阴煞、天虚、大耗等曜”; the source does not say that every listed star must be present. No ALL/ANY quantifier is invented.
- **SP02-132 / 151:** explicit infidelity-related source statements are kept as `CASE_SUPPORT_ONLY`. SP02-151’s target is corrected to the source phrase “婚后易移情别恋”.
- **SP02-133:** “感情上的隐衷” is not over-interpreted as a specific affair; the target is refined to emotional secrecy/reservation.
- **SP02-149:** the condition retains the prerequisite from the immediately preceding sentence: 巳亥天机见昌曲并同会桃花诸曜，复见煞忌刑曜.
- **SP02-152 / 183:** concrete separation and financial-loss statements are kept as `CASE_SUPPORT_ONLY`.
- **SP02-163:** the female-chart context is restored from the preceding source clause.
- **SP02-190:** split into three source records for “主夫多灾病”, “煞重，则见刑克”, and “否则生离”.
- **SP02-199:** narrowed to the source condition “见煞，但不重”; the severe `煞忌刑凑` clause remains separate in SP02-200.

## Explicit temporal-scope holds

The following historical assignments are held because the source does not support the recorded YEAR/DECADE precision:

- SP02-113…117 — `经行宫垣` / `宫垣为吉凶枢纽`
- SP02-122…125 — `四垣为吉凶之枢纽`
- SP02-128…129 — `宫垣为克应之期`
- SP02-135 — source says `[武曲天府]限`, not explicitly `大限`
- SP02-153…155 — relevant palace walls are described as a `吉凶克应之枢纽`
- SP02-169…170 — `行巨门、[武破]二垣` has no explicit YEAR/DECADE layer
- SP02-175 — `夫妻宫行至天同坐守之垣时` has no explicit YEAR/DECADE layer
- SP02-180…181 — `行天同、[廉杀]二垣` has no explicit YEAR/DECADE layer
- SP02-193…195 — relevant palace walls are described as a `吉凶克应的枢纽`

SP02-140/141, SP02-165 and SP02-176 are retained as DECADE only because the source explicitly says `大限`.

## Open source-coverage residuals

Seven residuals remain open: the earlier printed-p33 intensifier; the full female `机巨`/fire-bell-or-Dolo-plus-Tong marriage clause; the general unfavorable baseline for 天机 in the spouse palace; the Sun–Giant Gate `经行至【机录像】` clause (preserving the scan’s anomalous glyph rather than silently correcting it); the “申宫又劣于寅宫” comparative qualifier; the 福德宫-unfavorable gender branches; and the 辅佐诸吉 gender branches. The JSON lists each claim, page, related candidates and reason. None is silently inferred from a neighboring rule.

## Execution boundary

- `conditions_compiled=0`; `execution_unlocked=0`; `history_feedback=0`.
- No Product/runtime authorization, shared Core semantics, other-palace write, new qi/memory/time primitive, independent time scale, numeric weight, probability or decay.
- P03 is **not complete** after this batch. The next bounded batch should start at printed p37, resolve the remaining Sun–Giant Gate source residuals where source-supported, and continue with SP03-201…300.

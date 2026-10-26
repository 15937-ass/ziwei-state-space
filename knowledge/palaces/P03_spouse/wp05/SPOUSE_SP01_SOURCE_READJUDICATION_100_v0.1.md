# P03 SP01 — source-first re-adjudication of spouse candidates 001–100

**Status:** source review complete; exact-head repository validation pending.  
**Issue:** #792  
**Lane / shard:** `KNOWLEDGE_ONLY / P03 夫妻宫`  
**Source:** `SRC-ZZ-003`, 《中州派紫微斗数深造讲义（下册）》, 下篇·宫垣论·夫妻宫  
**Approved scan SHA-256:** `6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c`

## Source boundary and historical inventory

The full P03 section begins at printed p33 (heading `1 紫微`) and ends on printed p51 immediately before the `子女宫` heading on the same page. It spans PDF physical pages 17–26. Physical p17 contains printed pp33–34; physical p18 contains pp35–36; physical p26 contains printed pp51–52.

The original scan images for physical pp17–26 were inspected for section boundaries and page inventory. The first candidate batch was directly re-adjudicated against the original page images for physical pp17–18 (printed pp33–35). Text extraction was used only to locate spans.

Nine historical CSV indexes contain **836 unique candidate rows** (`SP01-001`…`SP09-836`). The old index marks 136 rows as `case_support_only=true` and six as `PATH_DEPENDENT_GATE`. These files remain read-only acceleration inputs; their `SOURCE_SPAN_VERIFIED` labels are historical assertions, not accepted canonical truth.

## SP01-001…100 result

| Measure | Result |
|---|---:|
| Historical candidate rows directly reviewed | 100 |
| Candidate rows promoted after source review | 89 |
| Source records produced | 90 |
| Reusable projection/method records | 75 |
| `CASE_SUPPORT_ONLY` records | 15 |
| Held with explicit reason | 9 |
| Deduplicated/shared-prerequisite rows | 2 |
| Historical feedback | 0 |
| Path-dependent history gates carried into canonical records | 0 |

The record count is 90 rather than 89 because the source explicitly says `大运流年夫妻宫叠冲`; candidate `SP01-054` is represented as two separate records for the two existing source-named layers. No new time scale was introduced.

## Important source-first corrections

- `SP01-019`: narrowed to the stable-base 丑未紫破 branch; the source does not apply premarital turbulence identically to the 动荡 branch.
- `SP01-023`: held. The source says `大运` for the stable-base illness/career-adversity branch; it does not state a separate YEAR branch.
- `SP01-025`: retained as `CASE_SUPPORT_ONLY` because the claim concerns 婚外感情.
- `SP01-027`: held because the source says `出事` without specifying which event; the historical target `relationship_incident_window` is more specific than the source.
- `SP01-028`: deduplicated as a shared prerequisite into `SP01-029…031`; the structural prerequisite is preserved in each explicit 贪狼/破军/巨门 大运 branch.
- `SP01-029…031`: conditions expanded to retain the prerequisite that 紫府 lacks auxiliary support / has mostly single auxiliaries / or the 府库 is 空露.
- `SP01-034`: held; direct visual review of pp33–35 does not support the historical `寅申紫府天寿同躔` claim.
- `SP01-043`: target refined to preserve both source phrases `易志忑` and `善找寻刺激`.
- `SP01-053…054`: specific spouse-health claims retained as `CASE_SUPPORT_ONLY`; `SP01-054` is split into explicit 大运 and 流年 records.
- `SP01-057`: attribution corrected. `然仍各怀私心` belongs to the 卯酉紫贪有情/辅弼吉曜 paragraph, not 辰戌紫相.
- `SP01-081`: condition narrowed to the 辰戌紫相 source context.
- `SP01-088`: target corrected to post-separation partner dissatisfaction. `SP01-089` is deduplicated into that broader source claim.
- `SP01-091…092`: held because `于同梁或廉贪宫度发生事端` does not specify YEAR versus DECADE.
- `SP01-095…096`: held as unsupported by the inspected p33–35 source span.
- `SP01-097…098`: held because the source says `行太阳、太阴限`, not explicitly 大限/DECADE.

Every one of the 100 historical IDs has an explicit disposition and reason in the JSON artifact. Held or deduplicated candidates are not silently promoted.

## Explicit residuals carried forward

1. **Printed p33:** the source adds `此等宫垣，见煞忌空劫则更为生变之兆` to the 寅申紫府 condition. The historical index does not represent this intensifier as a distinct source branch. Its trigger quantifier remains unspecified.
2. **Printed p35:** the 子午天机 / 同梁 source continues with `见煞忌则主破碎`; this branch is absent from `SP01-099…100`.
3. **Printed p35:** the same source continues with `若见禄权科会，则夫妻可以白头。但若同时见巨门化忌，则仍须自我克制`; these two conditions are absent from `SP01-099…100`.
4. **Next batch anchor, printed p35:** continue with `丑未天机独坐，对宫为天梁，于夫妻宫有所不宜`. Use `SP02-101…200` only as an index and inspect the remaining source text directly.

Temporal-scope residuals for `SP01-091…092` and `SP01-097…098` remain separate from the source-coverage gaps. Do not force an unresolved time expression into a single layer.

## Execution boundary

- `conditions_compiled=0`; `execution_unlocked=0`.
- No Product/runtime authorization, shared Core semantic change, other-palace write, history-feedback promotion, new qi/memory/time primitive, numeric weight, probability, or decay.
- P03 is **not complete** after this batch. Continue source-first in P03 before admitting P11 under the PI-approved palace sequence.

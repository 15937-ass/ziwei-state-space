# P07 M07 — six residual source-gap dispositions (v0.1)

**Result:** 6 gaps directly rechecked against the original scan; 5 source-coverage gaps closed by source-native records; 1 retained unresolved because the source fragment does not state a favorable outcome.

- Issue: #669
- Lane / shard: `KNOWLEDGE_ONLY / P07 迁移宫`
- Source: `SRC-ZZ-003`, 《中州派紫微斗数深造讲义（下册）》
- Approved PDF SHA-256: `6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c`
- Directly inspected physical PDF pages 57–59, mapping to printed pp114, 115, 117–118; this issue's gap spans are printed pp114, 115 and 118.
- New source records: `M07-591` through `M07-607` (17 total: 16 reusable source-projection records and 1 `CASE_SUPPORT_ONLY` legal-event claim).

## Gap disposition table

| Gap | Printed page | Disposition | Added records |
|---|---:|---|---|
| `P07-M03-GAP-012` | 114 | **Retained unresolved** — source fragment verified, favorable outcome absent | none |
| `P07-M03-GAP-001` | 115 | Coverage closed | `M07-591` |
| `P07-M05-GAP-001` | 118 | Coverage closed; modifier-list quantifier retained unresolved | `M07-592–593` |
| `P07-M05-GAP-002` | 118 | Coverage closed; transformation alternatives kept separate | `M07-594–595` |
| `P07-M05-GAP-003` | 118 | Coverage closed; source-local clamp taxonomy represented | `M07-596–603` |
| `P07-M05-GAP-004` | 118 | Coverage closed; generic 吉夹/凶夹 membership remains open | `M07-604–607` |

## Source-first findings

### P07-M03-GAP-012 — printed p114: retained unresolved

The scan confirms the phrase `廉贞在迁移宫见财荫夹者`, but the following adverse clause contains the anomalous sequence `见刑忌夹者贞归三挫折不顺`, followed by `刑忌夹而廉贞化忌，更不利迁移`. The existing M03-233 record already covers the adverse 刑忌夹 branch. The favorable 财荫夹 fragment does not state its consequence in this span. I did not infer a favorable result from the neighboring adverse branch or repair `贞归三` by guess. The gap remains explicit.

### P07-M03-GAP-001 — printed p115: closed

The scan clearly reads `太阴与辅弼同度，不外得人助`. Added `M07-591` as a source-native support rule. The following `与魁钺同度，则机会迭来` is a distinct branch and remains outside this issue; Fu-Bi is not substituted with Kui-Yue.

### P07-M05-GAP-001 — printed p118: coverage closed, quantifier retained

The scan confirms `天相与廉贞同度，基本结构不利迁移，见煞忌空劫刑耗即主招非，重且牵涉词讼`. Added `M07-592` for the same-degree base and `M07-593` for the adverse list/outcome. Because the source does not formally specify an ALL/ANY/N_OF trigger for `煞忌空劫刑耗`, the list remains source-native and fail-closed. The specific legal-event claim is `CASE_SUPPORT_ONLY`; no probability or deterministic real-world prediction is inferred.

### P07-M05-GAP-002 — printed p118: closed with alternatives preserved

The scan confirms `廉相守迁移`, the Life-Palace `破军化权` qualifier, and the contrast between the `廉贞化禄` branch (in modern terms, career across two places) and `廉贞化忌` (staying at the birthplace favored). Added `M07-594` and `M07-595` as separate branches. The Life-Palace dependency is retained.

### P07-M05-GAP-003 — printed p118: source-local clamp taxonomy represented

The scan lists six `六吉夹` categories: `魁钺夹、辅弼夹、昌曲夹、禄权科夹、紫府夹、日月夹`, with differentiated outcomes. Added one umbrella outcome plus seven specific outcomes (`M07-596–603`). The glyph before `为` in the `财荫夹` clause is visually uncertain, so it is recorded as `若/惹` instead of silently corrected. The six `六吉夹` members are explicit in this source span only; no global clamp ontology is inferred, and `财荫夹` membership is not invented.

### P07-M05-GAP-004 — printed p118: source branches represented, open categories retained

The scan confirms the generic `吉夹` / `凶夹` contrast and two more specific branches: `昌曲夹 + 天相躔桃花`, and `羊陀夹 + 禄存叠化禄`. The latter reads `仅主人小妒忌，或小人包围`. Added `M07-604–607`. Membership for generic `吉夹` and `凶夹` is not enumerated in this span, so both remain open source-native categories rather than universal executable groups.

## Count reconciliation

- New records: **17** = 16 reusable source-projection records + 1 `CASE_SUPPORT_ONLY`.
- Cumulative P07 candidates reviewed: **607** (= 590 accepted M01–M06 + 17 new source-gap records).
- Cumulative reusable projection/method records: **536** (= 520 + 16).
- Cumulative `CASE_SUPPORT_ONLY`: **71** (= 70 + 1).
- Original M03/M05/M06 artifacts mutated: **0**.
- New qi/memory/time primitives, shared group semantics, weights, probabilities, decay, Product/runtime changes: **0**.
- `conditions_compiled=0`; `execution_unlocked=0`.

Machine-readable counterpart: `MIGRATION_M07_RESIDUAL_SOURCE_GAP_CLOSURE_6_v0.1.json`.

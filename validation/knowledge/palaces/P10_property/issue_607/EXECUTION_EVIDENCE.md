# Execution Evidence — Issue #607

Work unit: KB-WP07A-PROPERTY-RELATION-CROSS-PALACE-MAP-01  
Lane: KNOWLEDGE_ONLY / shard P10

## Dependency and activation

- Direct-star remainder Issue #597 / PR #609 merged at `2531d658b2f7d062c8a7aec5bb2c69aa32942ff9` after exact-head Actions run #2136 passed. Product PR #614 then advanced main; r1 Actions run #2143 passed on the old base but is not merge evidence for this replacement.
- This r2 branch is based on latest main `7f34532ef7e18b0d871428a97f30def7be9fee31`.
- Current active-palace census before activation: P01 #603, P05 #591, P07 #610; activating P10 #607 brings the total to 4, within the frozen cap of 4. No second P10 work unit is active.

## Source recheck

- Latest-main canonical CSV ↔ source-readjudication ↔ source-time-scope reconciliation: **PASS 3/3** for TP01-027, TP02-129, TP02-163.
- All three are `SOURCE_SPAN_VERIFIED`, `NATAL`, non-`CASE_SUPPORT_ONLY`, with `source_time_layers=[NATAL]` and no unmapped time labels.
- Source anchors are from 《中州派紫微斗数深造讲义（下册）》 printed pp156, 159, 160.

## Mapping and boundaries

- nominated: 3
- mapped to existing `PALACE_HAS_STAR` / `PALACE_RELATION`: 3
- blocked nominated: 0
- production/executable entries created: 0
- TP01-027 preserves same-palace and opposite-palace branches.
- TP02-129 identifies the opposite Tianfu context but leaves 得禄 / 府库空露 unresolved; no absent transformation fact is used as a proxy.
- TP02-163 preserves the exact comparative projection target and records the same-palace baseline; no runtime comparison operator is created.
- TP02-139 remains a direct-star rule; TP03-288 / TP03-289 and TP02-195 remain out of scope.

## Validation

- Latest-main source reconciliation: **PASS 3/3**.
- JSON exact-ID census: **PASS 3/3**.
- Resolver fact-shape and condition branch tests are included; public-runner execution is pending r2 exact-head CI.
- Changed-path allowlist is exactly five P10-scoped files.
- No canonical source row, Product runtime, production registry, shared Core semantics, probability, numeric weight, or threshold is modified.

Mapping proves representability only; it does not authorize production execution.

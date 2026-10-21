# Execution Evidence — Issue #583

Work unit: KB-WP07A-PROPERTY-DIRECT-STAR-PRESENCE-MAP-01  
Lane: KNOWLEDGE_ONLY / shard P10

## Source review

- Approved source: SRC-ZZ-003, 《中州派紫微斗数深造讲义（下册）》, 田宅宫.
- Candidate set: TP01-055, TP02-195, TP03-297, TP04-319, TP04-358; exactly 5 direct NATAL conditions.
- All five canonical rows are SOURCE_SPAN_VERIFIED and non-CASE_SUPPORT_ONLY.
- The mapping cross-checks canonical CSV rows, source-readjudication JSON, and source-time-scope sidecars.

## Mapping result

- nominated: 5
- mapped to existing `PALACE_HAS_STAR`: 5
- blocked nominated: 0
- production/executable entries created: 0

## Critical boundaries preserved

- TP04-319 is only the general Tianliang fengshui baseline; TP04-320 keeps the separate Yinsha + Huoling exception.
- TP01-018 remains excluded because `独坐` requires exclusivity/absence, not simple presence.
- TP02-139 remains reserved for opposite-palace relation mapping.
- TP02-170 preserves unresolved source-glyph uncertainty.
- TP03-261 preserves literal `中年后`; no numeric age.
- TP03-275 retains its Huaji modifier; TP03-288 retains its Tianfu cross-palace requirement.
- TP04-321 retains `独坐` and the 寅申 scope gate.

## Validation policy

Per Issue #583, automatic GitHub Actions are intentionally skipped. Deterministic validation must run in the OpenAI/Codex environment. Full repository pytest is not claimed because the current OpenAI container cannot network-mount the repository. Record artifact assertions, Python syntax compilation, P10 allowlist, P0-auditor impact, and exact base/head checks before merge.

No canonical source row, Product runtime, production registry, shared Core semantics, probability, numeric weight, or threshold is modified.

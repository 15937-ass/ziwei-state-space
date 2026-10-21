# Execution Evidence — Issue #583

Work unit: KB-WP07A-PROPERTY-DIRECT-STAR-PRESENCE-MAP-01  
Lane: KNOWLEDGE_ONLY / shard P10

## Source review

- Approved source: SRC-ZZ-003, 《中州派紫微斗数深造讲义（下册）》, 田宅宫.
- Candidate set: TP01-055, TP02-195, TP03-297, TP04-319, TP04-358; exactly 5 direct NATAL conditions.
- All five canonical rows are SOURCE_SPAN_VERIFIED and non-CASE_SUPPORT_ONLY.
- Canonical CSV rows, source-readjudication records, and source-time-scope sidecars agree on each selected row's condition, projection, NATAL scope, and source-verification status.

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

## Deterministic OpenAI/Codex validation

Automatic GitHub Actions are intentionally not used for this unit. No PR has been opened yet because the repository's current `pull_request` workflow trigger automatically starts a run on PR creation, conflicting with the PI instruction not to use Actions. This is the only remaining process decision before PR/merge.

- Mapping JSON parse and exact five-ID census: **PASS**.
- Canonical CSV ↔ source-readjudication reconciliation: **PASS** (5/5 selected rows).
- Source condition / projection domain / target / mode / source location / NATAL layer / CASE_SUPPORT_ONLY / source-span status checks: **PASS** (5/5).
- Explicit exclusion ledger vs canonical rows: **PASS** (8/8, including the TP04-320 exception and TP04-321 exclusivity/branch gate).
- Existing atom allowlist and condition shape: **PASS** (all five use only `PALACE_HAS_STAR(palace=P10, star=<source star>)`).
- Runtime emitter source inspection: **PASS**. The current resolver emits `PALACE_HAS_STAR(palace=palace_id, star=name)` for each named star in the resolved palace.
- Python syntax compilation of `tests/test_knowledge_p10_direct_star_presence_map_01.py`: **PASS** in the OpenAI Python runtime.
- P10 shard branch/write-set validation: **PASS** (branch contract and all five changed paths).
- P0-auditor impact inspection: **PASS**; no changed path or artifact stem is referenced by `src/audit_repository.py`.
- Full repository pytest: **NOT RUN**. The current OpenAI container cannot network-mount the GitHub repository; no full-suite pass is claimed.
- Product/Node/Go regression: **NOT REQUIRED**; no executable implementation or shared schema changed.

The branch was created from main commit `11f9eedd6bfcb05e5d0fcb2f17327bc3c288de86`. Recheck current main/base and exact branch head immediately before any PR/merge.

## Boundary

No canonical source row, Product runtime, production registry, shared Core semantics, probability, numeric weight, or threshold is modified. Mapping proves representability only; it does not authorize production execution.

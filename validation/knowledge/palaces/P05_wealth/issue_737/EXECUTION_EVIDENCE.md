# Execution Evidence — Knowledge P05 Issue #737

## Work identity
- Lane/shard: KNOWLEDGE_ONLY / P05 财帛宫.
- Work unit: KB-P05-SOURCE-FIRST-JUMEN-P86-P87.
- Branch: `knowledge/p05-737-source-first-jumen-p86-p87`.
- Source: SRC-ZZ-003, 《中州派紫微斗数深造讲义（下册）》.
- Source SHA-256: `6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c`.
- Scope: printed p86 heading 10 巨门 through the last 巨门 sentence before printed p87 heading 11 天相.
- Source page-image mapping: physical PDF p43 right half = printed p86; physical p44 left half = printed p87.
- Initial accepted main/base SHA: `18e72d7b63e7eb63b5b8d3ff286f8498284867a7`.

## Source review result
- Historical candidate rows reviewed: 42 (W08-701…W08-742); the CSV was used as an index only.
- Source-first records created: 42; canonical promotions: 42; source-text ambiguity rows: 0; new source gaps: 0.
- Condition/scope corrections are documented row by row in `WEALTH_W08_SOURCE_READJUDICATION_P86_P87_v0.1.json`.
- Four ordered paths are retained in the time-scope sidecar; the source phrases 早年 / 中年后 remain life-stage qualifiers, not independent time triggers.
- Prior gaps preserved: W05-SG-002 PARTIALLY_RESOLVED; W06-SG-001…005 OPEN.
- No Product, Governance, shared Core, other-palace or historical candidate files were modified.

## Validation identity and status
- Exact-head full pytest: PENDING until PR head is created and its required checks finish.
- Product JS adapter checks: PENDING.
- Deterministic P0 gate: PENDING.
- Repository Governance v1 and shard/write-set validation: PENDING.
- Final base/head SHAs and Actions run reference must be recorded after exact-head validation. A green run on an older head or a changed main is not sufficient for merge.

## Handoff
- Next source anchor after this bounded checkpoint: printed p87 heading 11 天相, opening “天相坐财帛宫，有些情形与天府相似。天府为财库。但天相却亦可为财印。”
- This checkpoint does not close the P05 source census and does not authorize Product/runtime consumption or empirical prediction claims.


## Supplemental source critic
- W08-712 explicitly inherits the 太阳化忌 clause before 天刑; W08-714 preserves the literal 火、铃星、空劫、大耗 list; W08-729 retains 禄存同度; W08-733/734 preserve the 辰戌巨门与煞曜同度 antecedent; W08-736 retains 独坐.


## Rebased replacement PR (2026-10-24)
- The Product-owned historical-snapshot test repair was merged to main at `5a7be5651f1682fe1c5c039f99d77cb1852d9ed3` after all Repository Quality Gate steps passed.
- Stale Draft PR #739 is superseded; the source-first work has been replayed onto current main in [Draft PR #744](https://github.com/15937-ass/ziwei-state-space/pull/744).
- Replacement branch: `knowledge/p05-737-source-first-jumen-p86-p87-r2`.
- Replacement PR base SHA: `5a7be5651f1682fe1c5c039f99d77cb1852d9ed3`.
- The P05 state cache and regression assertions now point to Issue #737, the replacement branch, and PR #744.
- Source scope and semantic safeguards are unchanged by this rebase. Exact-head validation remains pending; do not merge before all required checks pass.


## Exact-head validation update (2026-10-24)
- Source artifacts, state-cache reconciliation, and regression tests at pre-evidence head `6de84c7ce59d1ff80cdd621f42dc3e6b9d914630` passed Repository Quality Gate run #2521: 2,685 tests passed, 132 subtests passed; Product JS adapter checks, deterministic P0 gate, and Repository Governance v1 all passed.
- This evidence-only update records that result; it creates a new PR head and therefore requires a fresh exact-head quality-gate run before merge. The latest PR head and linked Actions result are authoritative.
- Issue #737 explicitly sets Human Gate to NONE for direct source transcription and palace-local condition-preserving adjudication; this bounded W08 batch therefore does not require an additional PI approval gate. Run #2523 passed on pre-evidence head `7486bd9f6064f3af449dd5511cd3c26b29dffd8a` (2,685 tests, 132 subtests; Product JS, deterministic P0, and Governance v1 all passed). This evidence-only edit advances the PR head, so the new exact-head run must also pass before merge. No Product/runtime authorization is implied.

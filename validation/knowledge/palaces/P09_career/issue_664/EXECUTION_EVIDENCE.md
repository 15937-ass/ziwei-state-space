# P09 Career State Reconciliation — Closure v0.16

- Tracking issue: [#664](https://github.com/15937-ass/ziwei-state-space/issues/664)
- Lane: KNOWLEDGE_ONLY
- Shard: P09 — 事业宫
- Work unit: KB-P09-CAREER-STATE-SYNC-V016
- Integration base: `033639863c0bba538c08920c51beb0598c852e79`
- Risk: R1 — bounded recovery-cache synchronization
- Human Gate: NONE

## Why the cache needed reconciliation

The P09 state cache previously pointed at the accepted dependency-IR pilot (#508 / PR #509) and closure v0.15. Canonical main also contains the later accepted compiler-readiness census (#510 / PR #511) and closure v0.16. The recovery cache therefore needed to be advanced without changing any canonical source semantics.

## Accepted checkpoint

| Check | Canonical result |
|---|---|
| Career source-ID coverage | 888 / 888 |
| Contextual activation closure | v0.16, 251 / 251 |
| Explicit antecedent graph | 65 nodes / 66 edges; 0 cycles; max depth 2 |
| Dependency condition IR | 3 records |
| Direct condition IR | 9 records |
| LOCAL_STRUCTURE_READY census | 26 / 26 partitioned exactly once |
| Dependency effective underdetermined | 11 |
| Dependency condition-IR-ready | 3 |
| Direct condition-IR-ready | 9 |
| Direct relation/composition deferred | 3 |
| Total Knowledge condition-IR-ready | 12 / 26 |
| Still not condition-IR-ready | 14 / 26 |
| Source-underdetermined closure rows | 201 |
| Knowledge-side conditions compiled | 0 |
| Knowledge-side execution unlocked | 0 |

The exact 12 IR-ready IDs are the union of the three dependency IR child IDs and nine direct condition-IR IDs. The 11 inherited-uncertainty rows and three relation/composition-deferred rows remain fail-closed. The three negative controls CA02-171, CA03-236 and CA04-323 remain unpromoted.

## Scope and boundary

Only the P09 recovery state file, its regression test, and this execution evidence are changed. No source rows, source interpretations, Product files, runtime rules, or other-palace artifacts are modified. Product compiler/runtime status is a separate lane and is not represented as Knowledge-side execution authorization.

After this bounded recovery issue closes, P09 returns to ACTIVE_NO_ACTIVE_WORK. Future P09 work must be selected from an evidence-backed gap; no source re-extraction or promotion is implied by this state synchronization.

## Validation

The previous failure on the old base was a recovery-snapshot contract mismatch: Product PR #660 changed mutable recovery caches from immutable SHA-pinned source artifacts to dated checkpoint metadata. The old failure is diagnostic history, not merge evidence. The current exact-head GitHub Actions run is authoritative for full pytest, Product JS syntax validation, deterministic P0 audit, and Repository Governance v1. This file records accepted state and scope, not a test result.

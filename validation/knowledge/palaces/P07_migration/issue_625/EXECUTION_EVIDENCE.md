# P07 Migration M05 Acceptance and State-Recovery Evidence

- Work unit: KB-P07-MIGRATION-M05-ACCEPTANCE-STATE-RECOVERY
- Tracking issue: #625
- Lane: KNOWLEDGE_ONLY
- Shard: P07 — 迁移宫
- Branch: knowledge/p07-625-migration-state-recovery
- Scope: recovery-cache synchronization and deterministic consistency checks only

## Recovery authority chain

- PROJECT_STATE.yaml selects the current recovery precedence and public Actions execution protocol.
- knowledge/KNOWLEDGE_STATE.yaml is a coordinator/index, not a palace execution pointer.
- The P07 state cache still pointed to closed Issue #619 / PR #622 and still described exact-head validation as pending.
- Issue #619 / PR #622 is merged at main commit d3eacc75fa745cef12a01ed29f899984ea10591a.
- The current P07 M05 source-first artifacts are canonical on main. This issue changes only the P07 state cache, P07-local regression test and P07-local evidence.
- No active P07 Human Gate is identified. This recovery does not alter source semantics or require a new Human Gate.

## Accepted M05 checkpoint reconciled

| Surface | Accepted result |
|---|---|
| Historical candidates | M05-401…M05-500: 100 / 100 |
| Current-batch reusable projections | 90 |
| Current-batch CASE_SUPPORT_ONLY | 10 |
| Corrected source spans | 41 |
| M04 source gaps closed | 3, traceable and non-duplicative |
| New p118 Tianxiang source gaps | 4, explicitly unresolved |
| Carried-forward M03 gaps | P07-M03-GAP-001 and P07-M03-GAP-012 |
| Cumulative reviewed | 500 |
| Cumulative reusable projection rules | 443 |
| Cumulative CASE_SUPPORT_ONLY | 57 |
| Current-batch history feedback gates | 0 |
| Product/runtime authorization | 0 |

The M05-455 and M05-487 outcomes remain source-internal sequences, not personal-history gates. Only NATAL / DECADE / YEAR / MONTH source-time layers remain, and MIGRATION_FIRST_THREE_YEARS / HG-P07-TEMPORAL-01-A is unchanged.

## State-cache repair

The state now marks P07 as ACTIVE_NO_ACTIVE_WORK with null active Issue / branch / PR pointers. The canonical checkpoint records M01–M05 as merged. The next source anchor remains M06-501…590 against printed pp119–122; the four M05 Tianxiang gaps and two carried-forward M03 gaps remain explicit. This recovery does not start M06 or authorize P08.

## Validation record

This evidence records the preflight and state reconciliation scope. The new deterministic state-recovery tests and exact-head repository quality gate must pass before merge. Do not claim final acceptance until the final PR head has a successful full pytest, Product JS adapter check, deterministic P0 audit, Repository Governance v1 result, and exact-main/base/head comparison.

## Boundaries

- No source-readjudication artifact is modified.
- No other-palace, shared audit, Core, Governance or Product path is modified.
- No new semantic primitive, probability, numeric weight, temporal mechanism, causal claim or Product runtime permission is introduced.

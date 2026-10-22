# P09 Career Acceptance and Recovery Evidence

- Work unit: KB-P09-CAREER-ACCEPTANCE-STATE-RECOVERY
- Tracking issue: [#617](https://github.com/15937-ass/ziwei-state-space/issues/617)
- Lane: KNOWLEDGE_ONLY
- Shard: P09 — 事业宫
- Scope: recovery-cache synchronization and deterministic consistency checks only

## Recovery authority chain checked

- PROJECT_STATE.yaml selects governance/RECOVERY_PRECEDENCE_v1.md and governance/PUBLIC_ACTIONS_EXECUTION_PROTOCOL_v0.2.md.
- knowledge/KNOWLEDGE_STATE.yaml is a coordinator/index, not a palace execution pointer.
- knowledge/states/P09_CAREER_STATE.yaml previously said ACTIVE_NO_ACTIVE_WORK, but its checkpoint did not identify the accepted dependency-IR pilot.
- Before opening this recovery issue, live search found no active P09 Knowledge work item. Open work for P01/P05 and Product Career is outside this P09 Knowledge work unit.
- Issues #505 / PR #507 and #508 / PR #509 are closed/merged. PR #509 records the exact-head full repository gate as PASS: 2,214 pytest passed, P0 audit PASS, Product JS syntax check PASS, and Knowledge governance validation PASS.
- No current P09 Human Gate is identified by the Knowledge state/cache. This issue does not change source semantics or require a new Human Gate.

## Accepted baseline reconciled

| Surface | Accepted result |
|---|---|
| Canonical Career source-ID universe | 888 IDs |
| Source/structured-ID closure | 888 / 888; the existing test_knowledge_career_888_closure.py verifies the full union against the canonical CSV rows |
| Contextual activation closure | v0.15; 251 / 251 unique source IDs |
| Explicit antecedent graph | 65 nodes / 66 edges; 0 cycles; maximum depth 2; 0 unresolved parent IDs |
| Dependency IR | Exactly 3 records: CA05-420 -> CA05-419; CA07-639 -> CA07-638; CA07-682 -> CA07-681 |
| Row-local structure ready | 26 |
| Dependency compiler gated | 24 |
| Rows with source underdetermination | 201 |
| Product conditions compiled | 0 |
| Runtime execution unlocked | 0 |

Negative controls CA02-171, CA03-236 and CA04-323 remain unpromoted. The 24 dependency-only rows with underdetermined parents and the wider source-underdetermined set are intentional fail-closed states, not omissions to auto-fill.

## Historical status handling

knowledge/wp07a/CAREER_888_CLOSURE_AUDIT_v0.1.json retains its original pre-gate status string. It is treated as historical artifact metadata, not the current task selector or proof of the latest run state. Its source-ID census and closure claims are cross-checked against the existing final-36 closure and deterministic full-union test. Historical source artifacts are not rewritten as part of this recovery.

## Validation record

This initial evidence file records the preflight audit only; it does not claim that the new recovery test or this PR's exact-head gate has passed. The PR's final exact-head workflow result, base/head SHAs, and workflow URL must be recorded in the PR validation record after GitHub Actions completes.

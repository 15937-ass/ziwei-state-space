# Execution Evidence — Issue #597

Work unit: KB-WP07A-PROPERTY-DIRECT-STAR-PRESENCE-MAP-REMAINDER-01  
Lane: KNOWLEDGE_ONLY / shard P10

## Activation and source review

- Dependency #583 / PR #596 merged to main at `878340f07aa820405d6acca2a5de962befc5c02e`.
- Initial branch `knowledge/p10-597-property-direct-star-presence-remainder-01` passed Actions run #2109, but main advanced 18 commits after its base. A replacement branch was created from current main: `knowledge/p10-597-direct-star-remainder-r2`.
- Source CSV ↔ source-readjudication ↔ source-time-scope recheck on latest main `d25c9217a7d0137f4e5be5021f4db89275048db9`: **PASS 6/6**.
- Selected IDs: TP02-134, TP02-139, TP03-207, TP03-214, TP04-319, TP04-339.
- All six are canonical NATAL, SOURCE_SPAN_VERIFIED, non-CASE_SUPPORT_ONLY rules with no unmapped source time labels.

## Mapping result

- nominated: 6
- mapped to existing `PALACE_HAS_STAR`: 6
- blocked nominated: 0
- production/executable entries created: 0

## Boundaries preserved

- TP02-134 is a scene translation to a financial-institution service context; no employment success or stability guarantee is inferred.
- TP02-139 is a direct single-star condition and is not dependent on 天梁对拱; the separate comparison rule is TP02-163.
- TP03-207 base institutional stability remains separate from TP03-204 forced movement/sale and TP03-209 personnel-dispute conditions.
- TP03-214 base fengshui sensitivity remains separate from TP03-215.
- TP04-319 base fengshui sensitivity remains separate from TP04-320.
- TP04-339 base fengshui sensitivity remains separate from TP04-340 (廉贞七杀 / 武曲七杀).
- TP03-299 remains deferred because its exact source condition scope needs re-adjudication; it is not silently flattened into direct star presence.

## Validation plan

- Latest-main canonical rows, source-readjudication records, and source-time-scope sidecars: **PASS 6/6** on `d25c9217a7d0137f4e5be5021f4db89275048db9`; separate exception rows reconcile **5/5**.
- Mapping JSON parse and exact six-ID census: **PASS**.
- Canonical CSV ↔ source-readjudication ↔ source-time-scope reconciliation: **PASS 6/6**; separate exception ledger matches canonical rows: **PASS 5/5**.
- Existing atom shape and resolver emitter source inspection: **PASS**; regression test asserts the resolver emits each exact palace-bound fact (runtime test execution remains pending CI).
- Python syntax parse of the current test source: **PASS**.
- Changed-path census: **PASS 5/5**; all changed paths fall within the P10 state, P10 WP07A artifacts, P10 validation, and P10 test allowlist.
- P0-auditor impact inspection: **PASS**; the four new artifact/test stems are not referenced by `src/audit_repository.py`.
- Initial branch Actions run #2109 completed **successfully** (pytest, JS adapters, deterministic P0 gate, Governance v1), but that green result is stale because main advanced 18 commits. Current-main replacement requires a fresh exact-head CI run.
- Public-runner PR quality gate must pass on the replacement branch's exact head before merge; do not reuse the old green run as merge evidence.

## Boundary

Replacement branch base: `d25c9217a7d0137f4e5be5021f4db89275048db9`. The prior P10 state on main was stale (still pointed to closed/merged Issue #583 / PR #596); this replacement updates the P10 state to Issue #597 and its current branch/PR. No canonical source row, Product runtime, production registry, shared Core semantics, probability, numeric weight, or threshold is modified. Mapping proves representability only; it does not authorize production execution.

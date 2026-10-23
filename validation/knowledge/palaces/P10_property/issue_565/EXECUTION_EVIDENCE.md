# Execution Evidence — Issue #565

Work unit: KB-WP07A-PROPERTY-DIRECT-TRANSFORM-MAP-REMAINDER  
Lane: KNOWLEDGE_ONLY / shard P10

## Source review

- Approved source: SRC-ZZ-003, 《中州派紫微斗数深造讲义（下册）》, 田宅宫.
- Directly inspected source passages: printed pp158, 160, and 163.
- Candidate set: TP01-095, TP02-148, TP03-270; exactly 3 direct NATAL conditions.
- All three canonical rows are SOURCE_SPAN_VERIFIED and non-CASE_SUPPORT_ONLY in the source-first review artifacts.
- The mapping cross-checks the canonical TP01/TP02/TP03 CSV, source-readjudication JSON, and source-time-scope sidecars.

## Mapping result

- nominated: 3
- mapped to existing `TRANSFORMATION_PRESENT`: 3
- blocked nominated: 0
- production/executable entries created: 0

Mapped:
- TP01-095 — P10 太阳化忌
- TP02-148 — P10 天同化禄
- TP03-270 — P10 巨门化忌

## Critical boundaries preserved

- TP01-096 remains the separate `太阳化忌更见煞刑虚耗` compound extension.
- TP02-149 remains the separate `天同化禄同时见煞` location-quality exception; it does not imply fewer holdings.
- TP03-271/272 remain CASE_SUPPORT_ONLY litigation/deception event candidates.
- TP03-273 remains a multi-layer CASE_SUPPORT_ONLY event candidate.
- TP02-148's literal `中晚年以后` source life-stage wording is not converted to an age threshold.

## Deterministic OpenAI/Codex validation

Validation policy: Issue-defined data-only scope; automatic GitHub Actions intentionally skipped.

- Exact branch artifact JSON parse and nominated-ID census: **PASS** (3/3 IDs).
- Canonical CSV ↔ source-readjudication ↔ time-scope comparison: **PASS** (3/3 source conditions, projections, NATAL layers, source verification, and non-case status).
- Explicit exclusion ledger vs canonical rows: **PASS** (5/5, including the TP02-149 exception and three CASE_SUPPORT_ONLY event candidates).
- Literal life-stage preservation for TP02-148: **PASS**; `中晚年以后` remains source metadata, not a numeric age threshold.
- Existing atom allowlist and condition shape: **PASS** (all three use only `TRANSFORMATION_PRESENT(palace=P10, star, mutagen)`).
- Python syntax compilation of `tests/test_knowledge_p10_direct_transform_remainder.py`: **PASS** in the OpenAI Python runtime.
- Runtime emitter source inspection: **PASS**. The current resolver emits the exact palace/star/mutagen `TRANSFORMATION_PRESENT` fact when a star object carries a mutagen. The new resolver test is committed for the repository test environment; it was not executed against a mounted repository in this session.
- P10 branch identity and changed-path allowlist: **PASS** (5/5 paths permitted by `KNOWLEDGE_SHARDS.json`).
- P0-auditor impact inspection: **PASS**; none of the changed paths are explicit inputs to `src/audit_repository.py`, and no new artifact path is referenced by that auditor.
- Product/Node/Go regression: **NOT_REQUIRED**; no executable implementation or shared schema changed.
- Full repository pytest: **NOT_RUN**. The current OpenAI container cannot network-mount the GitHub repository; this is a bounded data-only exception, not a claim that full pytest passed.
- Exact base/head equality must be rechecked immediately before merge and recorded on Issue/PR.

## Boundary

No canonical source row, Product runtime, production registry, shared Core semantics, probability, numeric weight, or threshold is modified. Mapping proves representability only; it does not authorize production execution.

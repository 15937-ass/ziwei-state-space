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

## Validation policy

This is a data-only P10 mapping work unit under Issue #565. Follow the OpenAI/Codex execution preference recorded in the Issue; automatic GitHub Actions are intentionally skipped. The mapping/test/evidence artifacts do not claim that full repository pytest ran in a repository-mounted container. Exact artifact assertions, test syntax compilation, changed-path allowlist, P0-audit impact, governance-equivalent shard checks, and exact base/head verification must be recorded before merge.

No canonical source row, Product runtime, production registry, shared Core semantics, probability, numeric weight, or threshold is modified.

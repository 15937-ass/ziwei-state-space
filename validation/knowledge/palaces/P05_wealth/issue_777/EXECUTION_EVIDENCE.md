# Execution Evidence — P05 uncovered 廉贞 tail

- Work unit: `KB-P05-SOURCE-FIRST-LIANZHEN-TAIL-P81-P82-01`
- Issue: #777
- Lane/shard: `KNOWLEDGE_ONLY / P05`
- Branch: `knowledge/p05-777-source-first-lianzhen-tail-p81-p82`
- Base/current main at activation: `0c9210855d874045f577914e8ec27e909438ecf4`
- Approved source: `SRC-ZZ-003`, 《中州派紫微斗数深造讲义（下册）》
- Verified local PDF SHA-256: `6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c`

## Bounded source and outcome

- Exact source span: printed p81 bottom `丑未宫『廉贞，七杀』同度` through printed p82 section 6 廉贞, stopping immediately before `7 天府`.
- Inspected physical PDF p41 left/right page images at full-page and enlarged-crop resolution.
- Source-first records: 41; proposed promotions: 37; held: 4 (`W10-925`, `W10-926`, `W10-929`, `W10-953`).
- New local source gaps: `W10-SG-001…004` (all OPEN, none a shared Core gap).
- Explicit annual response condition retained as YEAR on `W10-948`; no DECADE layer or numeric temporal parameter added.
- Proposed cumulative P05 total after acceptance: 844 source-first review records + 4 p81 supplements = 848 accounted; 831 reusable rules; 17 held source-first records; 26 explicit residual gap IDs plus eight separate record-level uncertainty annotations.
- `P05-COV-GAP-001` is fully accounted for on this PR head; P09 remains blocked until this PR passes exact-head validation and merges.

## Validation

Execution runtime: GitHub Actions standard public runner.
Base commit: `0c9210855d874045f577914e8ec27e909438ecf4`
Exact tested data/code head: `b8531499df62ed6972eada8ce2352b7a6696fd98`
Workflow run: [#40177461771](https://github.com/15937-ass/ziwei-state-space/actions/runs/40177461771) (run #2675).

- Full repository pytest: **PASS** — 2752 passed, 132 subtests passed in 373.92s.
- Product JS adapter / syntax check: **PASS**.
- Deterministic P0 repository audit: **PASS**.
- Repository Governance v1 and P05 write-set validation: **PASS**.
- Focused P05 source-first assertions are included in the full repository pytest run.

This evidence validates the exact data/code head above. The evidence-file update itself creates a new PR head, which must pass the same full exact-head quality gate before PR #780 is marked ready or merged.

Known limitations:
- Four source-first records remain held: `W10-925`, `W10-926`, `W10-929`, and `W10-953`; source ambiguity is preserved rather than emended.
- The census retains 26 explicit residual gap IDs (25 OPEN, one PARTIALLY_RESOLVED) and eight separate record-level uncertainty annotations.
- No Product/runtime authorization, shared Core semantic change, numeric weight, probability, duration, threshold, or empirical predictive-validity claim is implied.

No prior accepted source rule or historical candidate CSV is edited. No shared Core semantics, Product/runtime, Governance, or other-palace artifact is changed.
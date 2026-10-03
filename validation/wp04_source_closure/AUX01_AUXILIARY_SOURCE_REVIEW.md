# AUX01 — 辅佐八曜 Source Review

status: **CHECKPOINT_CLOSED_SOURCE_SPAN_VERIFIED**

## Scope

- source: SRC-ZZ-002《中州派紫微斗数深造讲义（上册）》
- printed pages: 165–171
- catalog: `knowledge/operators/auxiliary_eight_v0.1.csv`
- reviewed rules: MOD-AUX-0001 … MOD-AUX-0100

## Result

- reviewed: 100
- SOURCE_SPAN_VERIFIED: 100 / 100
- ADD_CANDIDATE: 71
- CASE_SUPPORT_ONLY: 29
- new primitive qi: 0
- new history-memory type: 0
- new Human Gate: 0
- continuous weights / decay / fixed persistence duration invented: 0

## Review semantics

The existing catalog is a legacy extraction. To preserve its raw provenance, this checkpoint does **not** silently rewrite its historical rows. The authoritative v0.3 source-review status is carried by `AUX01_auxiliary_source_review_v0.1.csv`.

All 100 rows were checked against the continuous source span on printed pp165–171. Existing computational normalizations are retained as audited `INFERRED` interpretations rather than automatically promoted to `SOURCE_PRESERVING`.

Projection-heavy historical family, relationship, health, incident, and old-character labels are marked `CASE_SUPPORT_ONLY`; they remain auditable source semantics but must not be promoted into primitive qi.

## Model feedback

1. 辅曜 / 佐曜 gives a clean source distinction between **external/opportunity support** and **self-effort-dependent support**.
2. 魁钺 and辅弼 contain explicit pair-gates; single-star behavior cannot be treated as a half-strength copy of the paired state.
3. 流魁流钺冲起原局 gives direct support for natal × temporal activation.
4. 禄马 separates resource flow from mobility: 马 alone is movement, not wealth; 禄 alone can increase resources without migration.
5. 禄马叠层 is a discrete temporal interaction. The source supplies no continuous gain coefficient.

## Next anchor

- MOD-AUX-0101
- source remains 禄存天马, printed pp170–171

# Core C2 — three source-specific temporal-scope comparisons (bounded research v0.1)

**Issue:** #975 · **Lane/shard:** KNOWLEDGE_ONLY / CORE · **status:** ACTIVE_BUILD / PRELIMINARY_ACCEPTED_EVIDENCE_COMPARISON · **accepted-main pin:** `fb3968aaae7f5bfaa29486334c2d115e17406193` · **scope:** exactly 3 historical IDs, no new extraction, no new source certification.

## Evidence identity and limitations

The accepted source basis is SRC-ZZ-003, 《中州派紫微斗数深造讲义（下）》, PDF SHA-256 `6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c`. The original PDF is **not stored in the GitHub repository** and was **not independently viewed in this C2 run**. Literal excerpts below are the *previously accepted source-review surfaces* in the pinned `GAP006` audit, not a fresh visual transcription. The legacy WP05 CSV condition fields are indexing/normalization fields, **not verbatim source proof**. No source-first re-certification is claimed.

Pinned accepted-main inputs (Git blob SHAs):
- `knowledge/core/wp07b/GAP006_GROUP_FAVORABILITY_SOURCE_AUDIT_v0.1.json` — `808debe6302f86f117246b9e41aa6616fea2ca8e` (evidence G006-E01/E02/E08).
- `knowledge/core/wp07b/GAP006_GROUP_FAVORABILITY_SOURCE_AUDIT_v0.1.md` — `06745c9f6d7a2886bbb00793dbe88ca1e2936181`.
- `knowledge/core/wp07b/TEMPORAL_REACTION_SOURCE_HANDOFF_v0.2.json` — `6fb27ae708d5ffe89a621897d1b927454a976230`.
- `validation/wp05/CA06_career_projection_review_501_600.csv` — `31c52e437bf33b795fcff735b4894a2316ce01be`.
- `validation/wp05/TP02_property_projection_review_101_200.csv` — `1ee32b609083ddb36559e891dd3e17e483ed3ef6`.
- `knowledge/wp07b/CAREER_TEMPORAL_REACTION_ELIGIBILITY_v0.1.csv` — `2529739803291b1692bb6fe985805ffefe3cc8c2`.
- `knowledge/palaces/P10_property/wp07b/PROPERTY_TEMPORAL_REACTION_ELIGIBILITY_AUDIT_v0.1.md` — `ff8ef0a35e0ff6662dad5a2258fdef3b2ee5b0b7`.
- `knowledge/core/temporal/NATAL_STRUCTURE_PRODUCT_CONSUMPTION_AUDIT_v0.1.md` — `0193149cbaf571d3d57238829cb116d45229f437` (C1 accepted conceptual boundaries).

## Three-way contrast

| ID / accepted source anchor | Explicit/recorded temporal surface | Natal/parent dependency | Safe descriptive conclusion | HOLD / no execution |
|---|---|---|---|---|
| **CA06-580**, Career printed **p147**, G006-E01 | `前格流年大运良好`; names YEAR and DECADE, **without a literal 或/及 in the accepted surface** | Accepted legacy CA06-579 (NATAL; 巳亥天府 and 命宫火贪 configuration) | Source juxtaposes two time layers and assesses period valence; legacy eligibility *normalizes* this as `DECADE_OR_YEAR_CONDITIONED_ON_FAVORABLE_PERIOD`. This normalization **is not a newly proven source-level OR operator**. | Meaning of `良好` undefined; whether either layer suffices, both are required, or precedence exists **UNKNOWN**. No `GOOD_PERIOD` predicate. |
| **CA06-600**, Career printed **p148**, G006-E02 | `前格；必须大运或流年配合`; literal `或` in previously accepted audit | Accepted legacy CA06-599 (NATAL 太阴/天机 context); `前格` requires source-context binding | Explicit **source-language alternative** of DECADE or YEAR support, conditional on prior configuration. Unlike CA06-580, the surface contains `或`. | `配合` criterion undefined, parent relation not executable, no machine `OR` condition, no priority or trigger. |
| **TP02-175**, Property printed **p161**, G006-E08 | `流年及小限吉，又见红鸾、天喜`; literal `及` | Legacy P10 YEAR-primary row also records 廉贞化忌; whole clause/antecedent must be preserved | Explicit **YEAR + SMALL_LIMIT** co-mention and star-modifier requirement. `小限` is an unmapped source-time label; **not** a DECADE/YEAR pair. | `吉` undefined; `小限` has no approved runtime primitive; no universal AND or source-independent `GOOD_YEAR`. Outcome remains non-executable. |

### Cross-row deductions (descriptive only)

1. **Three distinct surfaces, not one time-layer formula.** CA06-580 has a juxtaposition/valence phrase; CA06-600 has an explicit alternative plus `前格`; TP02-175 has a YEAR/SMALL_LIMIT compound. The common `PERIOD_VALENCE_OR_SUPPORT` audit class is a blocker taxonomy, **not an execution algebra**.
2. **Source wording ≠ historical normalization ≠ Product fact.** The legacy CA06-580/600 primary layer `DECADE` cannot erase the named YEAR branch. The TP02-175 primary layer `YEAR` cannot erase SMALL_LIMIT. This is a concrete reason to keep original surface, all named layers, and unresolved interpretation in distinct fields.
3. **Antecedent and valence remain separate.** CA06-579/599 are accepted NATAL context references, not proof that a particular decade/year is `良好` or `配合`. The missing independent criterion blocks runtime, even where `或` is literal.
4. **No generic inheritance or composition.** Nothing here establishes that YEAR inherits DECADE, that both layers are additive, or that one outranks the other. `N`, `E_decade`, `E_year`, `tau_t`, `M0`, `D_t` and `H_t` stay distinct per accepted C1.

## Gate and next evidence needed

**Current disposition:** `DESCRIPTIVE_COMPARISON_ONLY`; 3/3 `executable=false`, 3/3 `product_consumable=false`, 3/3 source-independent temporal criteria unresolved. No KIB/lock/registry/runtime change, new shared operator, time scale, probability, score, causal inference, or prediction claim.

**Unfinished source-first check:** independently inspect the approved original scan at printed pp147–148 (physical p74) and printed p161 (physical p81), confirm paragraph boundaries and literal conjunction/antecedent scope, then either amend this report or explicitly preserve the `NOT_INDEPENDENTLY_VISUALLY_REVERIFIED` limitation. No inference from the secondary excerpt can satisfy that visual gate. In particular, `CA06-580` must **not** be upgraded to literal OR solely from the eligibility CSV.

**Product availability:** accepted C1 and this branch's comparison do not grant DECADE/YEAR Product admission. All three records are HOLD for execution; Product must consume only accepted main plus an explicit future allowed-use checkpoint. This **branch is not canonical**.

**Human Gate:** none pending for this descriptive comparison. `HG-WP07B-CROSS-LAYER-REACTION-01` and `HG-WP07B-FAVORABILITY-AND-GROUPS-01` remain `FUTURE_NOT_PENDING`; activating any universal operator/predicate would require a separately scoped PI decision.

**Integration:** this is an ACTIVE_BUILD research checkpoint, **not QUEUE_READY**. After source check, Core-local validation, and content review, follow #888 exclusive lease, one sync, latest exact-head full gate, and merge/release only if fully green.

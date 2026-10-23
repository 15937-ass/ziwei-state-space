# WP06C P09 Source Candidate Index v0.1 — execution evidence

Status: **SOURCE-LINKED CANDIDATE INDEX ONLY; NOT A CANONICAL MAPPING REGISTRY**

## Scope

- Work unit: `KB-P09-WP06C-SOURCE-CANDIDATE-INDEX-01` (Issue #673).
- Source: `SRC-ZZ-003`, 《中州派紫微斗数深造讲义（下）》, 事业宫 section.
- Bounded cohort: 3 source rules, printed pages 133 and 144.
- Source attachment SHA-256: `6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c` (matches the inspected source PDF).
- Visual scan review: PDF page 67 (printed pp133–134) and PDF page 72 (printed pp143–144); the candidate page map is retained in the JSON artifact.
- Canonical source records are read-only. This work adds no source rule, no ontology node, and no executable mapping.

## Candidate dispositions

| Candidate | Source rule | Evidence treatment | Disposition |
|---|---|---|---|
| `P09-WP06C-CAND-001` | CA01-035 | `EXPLICIT` source wording; quantifier remains unresolved | Retain as a career-development pattern candidate, not a specific observed event. |
| `P09-WP06C-CAND-002` | CA01-045 | `EXPLICIT` conditional source wording; real-world action prerequisite retained | Hold because “勉强求变” is not represented by approved chart facts and the inherited context cannot be dropped. |
| `P09-WP06C-CAND-003` | CA05-469 | `EXPLICIT` career-scene source support; normalization remains scene translation | Explicitly exclude from event mapping: a blood/injury-symbolism-related industry scene is not a claim that the person will be injured or ill. |

## Source trace

- CA01-035: `validation/wp05/CA01_career_projection_review_001_100.csv`; `knowledge/wp07a/CAREER_CONTEXT_MAP_CA01_035_043_045_v0.1.json`; `knowledge/wp07a/CAREER_FIRE_BELL_SOURCE_EVIDENCE_v0.1.json#FB08`. The index keeps a short source anchor; the full reviewed passage and unresolved alternatives remain in the source context/evidence records.
- CA01-045: same canonical CA01 review CSV and context map. The index keeps only a short action anchor; the context map retains the full source context, antecedent rules CA01-042 / CA01-044, and the non-chart action prerequisite not represented by approved chart facts.
- CA05-469: `validation/wp05/CA05_career_projection_review_401_500.csv`; `knowledge/wp07a/CAREER_DIRECT_TRANSFORM_AUDIT_CA04_CA09_v0.1.md`. The index paraphrases the source rather than duplicating its longer wording; direct scan review is recorded as PDF page 72 / printed page 144. It remains a scene-translation negative control, not an observed injury/illness event.

The stable page span IDs follow the repository convention `ZZ003-P{printed_page}`. Each row retains the source rule ID, original condition, source location, source-review status, original normalized projection target/mode, and evidence references.

## Non-negotiable boundaries

1. Every `ontology_node_id` remains null pending the WP06B ontology contract and relevant root decision.
2. `probability_status=UNKNOWN`; no frequency, score, weight, posterior, or event probability is introduced.
3. The candidate evidence tier describes what the cited source supports. It does not authorize runtime or imply predictive validity.
4. Source-exact wording, transparent inference, case-only support, and hypothesis remain separate evidence tiers. This bounded cohort contains only explicit source-backed candidates; it does not promote case evidence or hypotheses.
5. The WP06B root decision is not performed in this P09 shard. Core Issue #671 remains ACTIVE, so WP06B Issue #672 remains WAITING_CORE_SLOT.
6. No Product registry, Product lock, other palace, or shared Core semantic file is changed.

## Validation

The dedicated regression test verifies source-rule identity against the accepted projection CSVs; source span and provenance presence; the unresolved Fire/Bell quantifier; the CA01-045 action prerequisite and antecedent IDs; the CA05-469 scene-versus-event exclusion; null ontology IDs; and the no-probability / non-executable boundary.

Full repository pytest, P0 audit, shard governance, Product JavaScript syntax, and exact-main/base/head checks remain required on the final PR head.

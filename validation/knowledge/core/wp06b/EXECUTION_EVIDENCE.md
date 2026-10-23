# WP06B execution evidence — manifestation root decision packet

- Issue: #672
- Branch: `knowledge/core-672-wp06b-manifestation-root-main-sync-20261023`
- Original activation/source-review base: `2143ac7030b531cd46836cf034baba6f801bdf8e`
- Current main/base after exact-main resync: `9538cad4cdf6b7c30014dbecdb82b644a61c8232`
- Main advanced by 14 accepted commits to `cb4259d4e83904b81ab556bd4e8a414471c4085e` after initial activation, then by `bee69d462a73abda1b51d3271d44f59627e3cbc6` adding the P09 WP06C source candidate index, then by `9538cad4cdf6b7c30014dbecdb82b644a61c8232` (PR #695) updating `AGENT_WORKFLOW.md` and `CHATGPT_START_HERE.md`. File-level comparisons confirm the source evidence paths referenced here were unchanged; this branch is rebuilt directly on the latest main and does not consume unmerged source artifacts.
- Lane/shard: `KNOWLEDGE_ONLY / CORE`
- Status: source-backed gate packet prepared; **Human Gate remains pending**.

## Source reconciliation

- P09 CA01-035 and CA01-045: direct scan recheck at PDF p.67 / printed p.133–134.
- P09 CA05-469: direct scan recheck at PDF p.72 / printed p.144.
- P05 W01-002 and P09 CA01-005 / CA01-007 / CA09-809: read-only reuse of accepted main canonical CSV rows marked `SOURCE_SPAN_VERIFIED`; no claim of fresh page-image re-adjudication for those rows.
- P07 M01-006: linked to the accepted source readjudication artifact `knowledge/palaces/P07_migration/wp05/MIGRATION_M01_SOURCE_READJUDICATION_100_v0.1.json` (`DIRECT_SOURCE_RECHECK_CONFIRMED`, `canonical_promotion=true`). The pre-G12 `validation/wp05/M01_migration_projection_review_001_100.csv` is historical acceleration input only and is not treated as canonical.
- P03 and P06 are not used as canonical evidence because their current palace state says `CANONICAL_REVALIDATION_NOT_STARTED`.
- The source PDF attachment SHA-256 recorded in the packet is `6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c`.
- Latest-main cross-check: main `9538cad4cdf6b7c30014dbecdb82b644a61c8232` includes the governance-only PR #695 closeout instructions and the accepted P09 index from `bee69d462a73abda1b51d3271d44f59627e3cbc6`. The index `knowledge/palaces/P09_career/wp06c/P09_WP06C_SOURCE_CANDIDATE_INDEX_v0.1.json` is `CANDIDATE_ONLY_NOT_CANONICAL`; its CA01-035 / CA01-045 / CA05-469 spans and projection values match this packet. It preserves null ontology IDs, `probability_status=UNKNOWN`, non-executable and non-Product-consumable status. It does not add root evidence or resolve the PI gate.

## Semantic findings

- Accepted source records include process/development, action-conditioned outcome, occupational scene, resource-domain semantic boundary, mobility axis, a relationship-domain cross-palace constraint, a case-only event candidate, and a methodology cross-palace constraint.
- W01-002 is a palace-semantic boundary and is explicitly excluded from manifestation-root evidence, as are the cross-palace constraints and case-only event candidate.
- This is sufficient to show that `projection_mode` cannot be blindly reused as ontology hierarchy, but it does **not** prove a universal root.
- CA09-809 is explicitly case-support-only and excluded from root evidence. CA01-005 and CA01-007 are cross-palace constraints, not manifestation nodes.
- Three root strategies are documented for PI review. Option C is only a preliminary recommendation; no option is selected or accepted.
- Every source evidence item has an unresolved `ontology_node_id=null` and `probability_status=UNKNOWN`.

## Explicit non-changes

- No accepted ontology node or universal root was created.
- No mapping registry, product registry, Product lock, palace-owned source record, or runtime artifact was changed.
- `HG-WP06B-MANIFESTATION-ROOT-01` remains `PENDING_PI_DECISION`.
- The pre-sync repository-quality-gate run (run `39921633117`, head `6aa189385f1b48fe76919002eebb9f3e193411ff`) passed, but it is not accepted as final-head validation because it used the prior base. The exact-head pytest, Product JS syntax, P0 audit, Governance v1 and base/head checks must pass again after this resync; final status is taken from the latest PR checks.

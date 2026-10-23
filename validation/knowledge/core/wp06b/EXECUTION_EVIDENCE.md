# WP06B execution evidence — manifestation root decision packet

- Issue: #672
- Branch: `knowledge/core-672-wp06b-manifestation-root-decision`
- Exact main base at activation: `2143ac7030b531cd46836cf034baba6f801bdf8e`
- Lane/shard: `KNOWLEDGE_ONLY / CORE`
- Status: source-backed gate packet prepared; **Human Gate remains pending**.

## Source reconciliation

- P09 CA01-035 and CA01-045: direct scan recheck at PDF p.67 / printed p.133–134.
- P09 CA05-469: direct scan recheck at PDF p.72 / printed p.144.
- P05 W01-002 and P09 CA01-005 / CA01-007 / CA09-809: read-only reuse of accepted main canonical CSV rows marked `SOURCE_SPAN_VERIFIED`; no claim of fresh page-image re-adjudication for those rows.
- P07 M01-006: linked to the accepted source readjudication artifact `knowledge/palaces/P07_migration/wp05/MIGRATION_M01_SOURCE_READJUDICATION_100_v0.1.json` (`DIRECT_SOURCE_RECHECK_CONFIRMED`, `canonical_promotion=true`). The pre-G12 `validation/wp05/M01_migration_projection_review_001_100.csv` is historical acceleration input only and is not treated as canonical.
- P03 and P06 are not used as canonical evidence because their current palace state says `CANONICAL_REVALIDATION_NOT_STARTED`.
- The source PDF attachment SHA-256 recorded in the packet is `6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c`.

## Semantic findings

- Accepted source records include process/development, action-conditioned outcome, occupational scene, state expression, mobility axis, relational condition, case-only event candidate, and structural constraint.
- This is sufficient to show that `projection_mode` cannot be blindly reused as ontology hierarchy, but it does **not** prove a universal root.
- D06-508 is explicitly case-support-only and excluded from root evidence. D01-003 is a structural constraint, not a manifestation.
- Three root strategies are documented for PI review. Option C is only a preliminary recommendation; no option is selected or accepted.
- Every source evidence item has an unresolved `ontology_node_id=null` and `probability_status=UNKNOWN`.

## Explicit non-changes

- No accepted ontology node or universal root was created.
- No mapping registry, product registry, Product lock, palace-owned source record, or runtime artifact was changed.
- `HG-WP06B-MANIFESTATION-ROOT-01` remains `PENDING_PI_DECISION`.
- Final exact-head pytest, Product JS syntax, P0 audit, Governance v1 and base/head checks are required on the PR's final head; no CI result is claimed by this evidence file.

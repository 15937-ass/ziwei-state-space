# WP06B execution evidence — manifestation root decision packet

- Issue: #672
- Current review branch: `knowledge/core-672-wp06b-capability-comparison-20261023` (PR #704).
- Historical predecessor branch: `knowledge/core-672-wp06b-manifestation-root-main-sync-20261023` (PR #692, closed/superseded).
- Original activation/source-review base: `2143ac7030b531cd46836cf034baba6f801bdf8e`
- Historical packet base: `9538cad4cdf6b7c30014dbecdb82b644a61c8232`.
- Current comparison branch base: `971cffc166e318b1c47184c3d297422dac1e3c2b` (includes Governance PR #703 and Product PR #698).
- Main advanced by 14 accepted commits to `cb4259d4e83904b81ab556bd4e8a414471c4085e` after initial activation, then by `bee69d462a73abda1b51d3271d44f59627e3cbc6` adding the P09 WP06C source candidate index, then by `9538cad4cdf6b7c30014dbecdb82b644a61c8232` (PR #695) updating `AGENT_WORKFLOW.md` and `CHATGPT_START_HERE.md`, then through Governance PR #703 to `3407150866a5ace99552daa674356b92610f080e`, and most recently through Product PR #698 to current main `971cffc166e318b1c47184c3d297422dac1e3c2b`. PR #703 changed `CHATGPT_START_HERE.md`, `governance/GOVERNANCE_STATE.yaml`, and `governance/proposals/700-durable-ontology-plan-and-cross-chat-handoff.md`; PR #698 changed only the five Product-owned paths recorded in the packet checkpoint. File-level comparisons confirm the four accepted source evidence paths referenced here are unchanged; PR #704 is rebuilt directly on current main and does not consume unmerged source artifacts.
- Lane/shard: `KNOWLEDGE_ONLY / CORE`
- Status: source-backed gate packet prepared; **Human Gate remains pending**.

## Source reconciliation

- P09 CA01-035 and CA01-045: direct scan recheck at PDF p.67 / printed p.133–134.
- P09 CA05-469: direct scan recheck at PDF p.72 / printed p.144.
- P05 W01-002 and P09 CA01-005 / CA01-007 / CA09-809: read-only reuse of accepted main canonical CSV rows marked `SOURCE_SPAN_VERIFIED`; no claim of fresh page-image re-adjudication for those rows.
- P07 M01-006: linked to the accepted source readjudication artifact `knowledge/palaces/P07_migration/wp05/MIGRATION_M01_SOURCE_READJUDICATION_100_v0.1.json` (`DIRECT_SOURCE_RECHECK_CONFIRMED`, `canonical_promotion=true`). The pre-G12 `validation/wp05/M01_migration_projection_review_001_100.csv` is historical acceleration input only and is not treated as canonical.
- P03 and P06 are not used as canonical evidence because their current palace state says `CANONICAL_REVALIDATION_NOT_STARTED`.
- The source PDF attachment SHA-256 recorded in the packet is `6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c`.
- Latest governance-specific checkpoint: Governance PR #703 merged at `3407150866a5ace99552daa674356b92610f080e`; its three paths are preserved in the packet. Current main has since advanced through Product PR #698 to `971cffc166e318b1c47184c3d297422dac1e3c2b`, which changed only Product-owned paths.
- Latest-main P09 cross-check: the accepted index was introduced by commit `bee69d462a73abda1b51d3271d44f59627e3cbc6` and is cross-checked against current main `971cffc166e318b1c47184c3d297422dac1e3c2b`. The index `knowledge/palaces/P09_career/wp06c/P09_WP06C_SOURCE_CANDIDATE_INDEX_v0.1.json` remains `CANDIDATE_ONLY_NOT_CANONICAL`; its CA01-035 / CA01-045 / CA05-469 spans and projection values match this packet. It preserves null ontology IDs, `probability_status=UNKNOWN`, non-executable and non-Product-consumable status. It does not add root evidence or resolve the PI gate.

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
- The pre-sync repository-quality-gate run (run `39921633117`, head `6aa189385f1b48fe76919002eebb9f3e193411ff`) passed, but it is not accepted as final-head validation because it used the prior base. The old PR #692 exact-head result is historical only. The replacement branch adds a non-production capability comparison and fixture; full pytest, Product JS syntax, P0 audit, Governance v1 and exact-base/head checks must pass on the replacement PR before acceptance.


## Non-production capability comparison checkpoint

- Comparison document: `knowledge/core/wp06b/ONTOLOGY_CAPABILITY_COMPARISON_v0.1.md`.
- Fixture: `knowledge/core/wp06b/ONTOLOGY_CAPABILITY_COMPARISON_FIXTURE_v0.1.json`.
- Source sample: 36 accepted records, stratified 9 each from P09 CA01, P09 CA05, P05 W01 and P07 M01; 5 synthetic design controls are explicitly not source evidence.
- The four source artifact blob SHAs were compared between the prior packet branch and current main and were identical.
- No A/B/C option is selected; no accepted ontology node, production mapping, Product registry, runtime artifact or probability was created. Human Gate remains `PENDING_PI_DECISION`.
- Validation for this replacement head: PENDING until the current PR's actual checks complete.


## Exact-head CI repair checkpoint

- Run `39944788602` on prior PR #704 head `4704c6583506330bb86fa2086961fcb2012d18d4` failed after 2,605 tests passed because the regression test expected the current main SHA while the packet's `latest_main_governance_check` still described PR #695 and its two changed paths.
- Corrected the packet to identify current Governance PR #703 / main `3407150866a5ace99552daa674356b92610f080e` and its three exact changed paths; retained the PR #695 history in the resynchronization note.
- Updated the regression test to check the coherent PR #703 checkpoint. No semantic gate was weakened.
- Validation on the resulting repair head is pending; the prior failed run is diagnostic evidence only.

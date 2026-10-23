# WP06B execution evidence — manifestation root decision packet

- Issue: #672
- Current review branch: `knowledge/core-672-wp06b-capability-comparison-20261023` (PR #704).
- Historical predecessor branch: `knowledge/core-672-wp06b-manifestation-root-main-sync-20261023` (PR #692, closed/superseded).
- Original activation/source-review base: `2143ac7030b531cd46836cf034baba6f801bdf8e`
- Historical packet base: `9538cad4cdf6b7c30014dbecdb82b644a61c8232`.
- Current comparison branch base after the latest mainline checkpoint: `2267c5686ce353b5f7b8a4b56f0335bf3792ac63` (includes Governance PR #703, Product PR #698, and the latest P01 source-first audit).
- Main advanced by 14 accepted commits to `cb4259d4e83904b81ab556bd4e8a414471c4085e` after initial activation, then by `bee69d462a73abda1b51d3271d44f59627e3cbc6` adding the P09 WP06C source candidate index, then by `9538cad4cdf6b7c30014dbecdb82b644a61c8232` (PR #695), then through Governance PR #703 to `3407150866a5ace99552daa674356b92610f080e`, Product PR #698 to `971cffc166e318b1c47184c3d297422dac1e3c2b`, and latest P01 source-first audit commit `2267c5686ce353b5f7b8a4b56f0335bf3792ac63`. The latest mainline commit changes only P01-owned source-review files/tests; direct blob-SHA checks confirm the four accepted WP06B source evidence files are unchanged. Its exact-head quality gate passed as run #39947533885. The decision branch is carried forward with a merge-base-preserving commit, not reset or force-pushed.
- Lane/shard: `KNOWLEDGE_ONLY / CORE`
- Status: source-backed gate packet prepared; PI has selected OPTION-C as an architecture direction only; the W5 metadata contract remains unfrozen.

## Source reconciliation

- P09 CA01-035 and CA01-045: direct scan recheck at PDF p.67 / printed p.133–134.
- P09 CA05-469: direct scan recheck at PDF p.72 / printed p.144.
- P05 W01-002 and P09 CA01-005 / CA01-007 / CA09-809: read-only reuse of accepted main canonical CSV rows marked `SOURCE_SPAN_VERIFIED`; no claim of fresh page-image re-adjudication for those rows.
- P07 M01-006: linked to the accepted source readjudication artifact `knowledge/palaces/P07_migration/wp05/MIGRATION_M01_SOURCE_READJUDICATION_100_v0.1.json` (`DIRECT_SOURCE_RECHECK_CONFIRMED`, `canonical_promotion=true`). The pre-G12 `validation/wp05/M01_migration_projection_review_001_100.csv` is historical acceleration input only and is not treated as canonical.
- P03 and P06 are not used as canonical evidence because their current palace state says `CANONICAL_REVALIDATION_NOT_STARTED`.
- The source PDF attachment SHA-256 recorded in the packet is `6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c`.
- Latest governance-specific checkpoint: Governance PR #703 merged at `3407150866a5ace99552daa674356b92610f080e`; its three paths are preserved in the packet. Current main has since advanced through Product PR #698 to `971cffc166e318b1c47184c3d297422dac1e3c2b`, which changed only Product-owned paths.
- Latest-main P09 cross-check: the accepted index was introduced by commit `bee69d462a73abda1b51d3271d44f59627e3cbc6` and is cross-checked against current main `2267c5686ce353b5f7b8a4b56f0335bf3792ac63`. The index `knowledge/palaces/P09_career/wp06c/P09_WP06C_SOURCE_CANDIDATE_INDEX_v0.1.json` remains `CANDIDATE_ONLY_NOT_CANONICAL`; its CA01-035 / CA01-045 / CA05-469 spans and projection values match this packet. It preserves null ontology IDs, `probability_status=UNKNOWN`, non-executable and non-Product-consumable status. It does not add root evidence or resolve the PI gate.

## Semantic findings

- Accepted source records include process/development, action-conditioned outcome, occupational scene, resource-domain semantic boundary, mobility axis, a relationship-domain cross-palace constraint, a case-only event candidate, and a methodology cross-palace constraint.
- W01-002 is a palace-semantic boundary and is explicitly excluded from manifestation-root evidence, as are the cross-palace constraints and case-only event candidate.
- This is sufficient to show that `projection_mode` cannot be blindly reused as ontology hierarchy, but it does **not** prove a universal root.
- CA09-809 is explicitly case-support-only and excluded from root evidence. CA01-005 and CA01-007 are cross-palace constraints, not manifestation nodes.
- Three root strategies were documented for PI review. PI has since selected Option C as the architecture direction only; no canonical root or ontology node ID is accepted.
- Every source evidence item has an unresolved `ontology_node_id=null` and `probability_status=UNKNOWN`.

## Explicit non-changes

- No accepted ontology node or universal root was created.
- No mapping registry, product registry, Product lock, palace-owned source record, or runtime artifact was changed.
- At the pre-decision checkpoint represented by this historical section, `HG-WP06B-MANIFESTATION-ROOT-01` was `PENDING_PI_DECISION`; the later PI decision checkpoint below supersedes that status.
- The pre-sync repository-quality-gate run (run `39921633117`, head `6aa189385f1b48fe76919002eebb9f3e193411ff`) passed, but it is not accepted as final-head validation because it used the prior base. The old PR #692 exact-head result is historical only. The replacement branch adds a non-production capability comparison and fixture; full pytest, Product JS syntax, P0 audit, Governance v1 and exact-base/head checks must pass on the replacement PR before acceptance.


## Non-production capability comparison checkpoint

- Comparison document: `knowledge/core/wp06b/ONTOLOGY_CAPABILITY_COMPARISON_v0.1.md`.
- Fixture: `knowledge/core/wp06b/ONTOLOGY_CAPABILITY_COMPARISON_FIXTURE_v0.1.json`.
- Source sample: 36 accepted records, stratified 9 each from P09 CA01, P09 CA05, P05 W01 and P07 M01; 5 synthetic design controls are explicitly not source evidence.
- The four source artifact blob SHAs were compared between the prior packet branch and current main and were identical.
- At this pre-decision checkpoint, no A/B/C option had yet been selected; no accepted ontology node, production mapping, Product registry, runtime artifact or probability was created.
- At this historical checkpoint, validation was pending. The later exact-head run #39946763248 passed on the previous head; the post-decision update below requires a new exact-head run.


## Exact-head CI repair checkpoint

- Run `39944788602` on prior PR #704 head `4704c6583506330bb86fa2086961fcb2012d18d4` failed after 2,605 tests passed because the regression test expected the current main SHA while the packet's `latest_main_governance_check` still described PR #695 and its two changed paths.
- Corrected the packet to identify current Governance PR #703 / main `3407150866a5ace99552daa674356b92610f080e` and its three exact changed paths; retained the PR #695 history in the resynchronization note.
- Updated the regression test to check the coherent PR #703 checkpoint. No semantic gate was weakened.
- At that historical repair checkpoint, validation was pending; the prior failed run remains diagnostic evidence only.


## PI decision and latest-main resynchronization checkpoint — 2026-10-23

- PI explicitly selected **OPTION-C — SOURCE_NATIVE_FOREST_WITH_ORTHOGONAL_AXES**. The decision is recorded in Issue #672 and PR #704 comments.
- The accepted scope is the architecture direction only: source-native root forest; independent candidate axes `output_kind`, `event_specificity`, and `source_epistemic`; `projection_mode` is not ontology hierarchy.
- W5 must still specify and validate allowed values, missing/unknown/conflict/not-applicable handling, source-supported versus inferred labels, migration, compatibility, rollback and tests. The contract is not frozen.
- No canonical root/node IDs, production mappings, Product registry/lock changes, runtime authorization, probabilities or empirical claims are authorized by this direction-only decision.
- Current main advanced one commit from `971cffc166e318b1c47184c3d297422dac1e3c2b` to `2267c5686ce353b5f7b8a4b56f0335bf3792ac63` through the P01 source-first audit. The 13 changed paths are P01-owned. The four accepted WP06B source evidence blobs are unchanged; main's quality gate #39947533885 passed.
- This branch is being carried forward with a single merge-base-preserving commit; it is not reset or force-pushed. Exact-head quality gate for the updated decision-record commit is pending.

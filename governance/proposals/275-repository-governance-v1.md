# 275 — Repository Governance v1.0 Migration

Status: APPROVED
Tracking Issue: #275
Owner Lane: GOVERNANCE_ONLY
Risk: R2
Approved by: PI
Approval date: 2026-10-06

## Motivation

The repository has strong research controls but execution state became duplicated across chat, PROJECT_STATE, product state, Roadmaps, acceptance documents, branches and PR bodies. Product work also began to confuse interface completion with actual content/calibration maturity.

## Goals

- one authoritative artifact for each type of fact;
- three isolated write lanes;
- Issue-driven bounded work units;
- Proposal-driven substantial design changes;
- Phase graduation rather than "code exists = complete";
- thin recovery state files;
- deterministic governance/path checks in CI;
- robust timeout/session recovery;
- anti-scaffolding controls for product work.

## Non-Goals

- no change to Zhongzhou canonical meaning;
- no new qi/state/temporal/manifestation theory;
- no PL4-A feature implementation during migration;
- no empirical training.

## Proposed Design

Authority hierarchy:
Constitution -> Approved Gate/Proposal -> Roadmap/Architecture -> Phase Contract -> Issue -> PR -> Chat.

Execution:
Issue -> short branch -> PR -> CI -> merge -> close.

State files become recovery pointers only. Product, Knowledge and Governance receive separate lane states.

## Alternatives Considered

1. Continue extending AGENT_WORKFLOW only: rejected because it leaves execution truth duplicated.
2. Add PRODUCT_EXECUTION_PLAN.yaml: rejected because it duplicates GitHub Issues.
3. Depend on chat memory: rejected as non-recoverable and model-dependent.
4. Copy full Kubernetes process: rejected as too heavy for one PI + GPT.

## Compatibility

Existing canonical artifacts remain valid. Legacy open PRs are frozen and migrated/reconstituted under the new branch/Issue rules after Governance v1.0 lands.

## Knowledge Impact

No canonical rule changes. Knowledge source review semantics remain unchanged.

## Product Impact

Product execution pauses at the current PL3-M exit boundary. PL4-A begins only after governance migration and clean resolution of the legacy personalized-posterior PR.

## Risks and Failure Modes

- over-bureaucratization: controlled by requiring Proposals only for substantial changes;
- duplicate status: controlled by making Issues/PR authoritative and State YAML cache-only;
- CI cost: ordinary PR gate remains deterministic; heavy closure tests are separate;
- legacy branch conflicts: handled via explicit migration/reconstitution Issues.

## Test Plan

- governance validator checks branch-lane path ownership;
- repository bootstrap/state contract checked;
- full pytest and repository P0 audit remain required;
- CI reruns on pull_request synchronize.

## Migration Plan

1. freeze product legacy PR #274 as draft;
2. install governance documents/templates/state split;
3. repair CI trigger semantics;
4. create Product/Knowledge/Governance recovery state;
5. define PL4-A phase contract;
6. open governance migration PR;
7. pass CI and governance audit;
8. merge to main;
9. reconstitute legacy Product and Knowledge open work under new Issue/branch rules;
10. configure main repository ruleset manually if connector lacks admin permission.

## Rollback Plan

Revert the governance migration merge. Canonical knowledge/product code prior to the migration is unchanged, so theory/runtime rollback is not required.

## Graduation Criteria

- governance docs and templates are present;
- state authority is unambiguous;
- three-lane path ownership is machine checked;
- CI runs on new PR commits;
- Product and Knowledge current work are recoverable without chat;
- migration PR passes all checks;
- no canonical theory changed.

## Human Gate

Not a domain Human Gate. PI explicitly approved the repository-governance migration.

## Decision

APPROVED on 2026-10-06.

## Implementation History

- #275 created as tracking Issue.
- #274 converted to draft/frozen during migration.

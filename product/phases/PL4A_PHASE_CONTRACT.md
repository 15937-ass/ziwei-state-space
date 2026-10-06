# PL4-A Internal Fidelity — Phase Contract

Status: PREPARED — NOT ACTIVE
Activation requires:
1. Repository Governance v1.0 merged;
2. legacy PL3-M personalized-posterior work reconstituted and resolved under Governance v1;
3. product state explicitly moved to PL4-A.

## Goal

Measure whether implemented product logic faithfully reconstructs approved Zhongzhou canonical knowledge. This phase does not test real-world predictive validity.

## Non-Goals

- no probability training;
- no personalized accuracy claim;
- no new canonical rule to make a benchmark pass;
- no new interface/registry unless a concrete fidelity failure demonstrates need;
- no textbook case treated as reality ground truth.

## Work Units

1. PL4A-01 Chart reconstruction fidelity — Issue #279
2. PL4A-02 W01 wealth-rule fidelity — Issue #280
3. PL4A-03 Rule -> ActiveRuleGraph -> EvidencePackage trace fidelity — Issue #281
4. PL4A-04 Temporal fidelity and Natal/Temporal boundary checks — Issue #282
5. PL4A-05 Textbook author-reasoning reconstruction — Issue #283
6. PL4A-06 Coverage/conflict/gap closure audit — Issue #284

Only one Product work unit may be ACTIVE at a time.

## Required reporting

Every benchmark report includes:
- eligible assets;
- covered assets;
- blocked_by_empty_registry;
- blocked_by_knowledge_dependency;
- trace completeness;
- deterministic reproducibility;
- contradiction preservation;
- unknown/insufficient evidence count.

PASS on a covered subset does not imply production readiness.

## Graduation Criteria

PL4-A may close only when:
- chart reconstruction suite is complete for the defined fixture set;
- W01 executable-rule inventory has full benchmark accounting;
- source-to-rule-to-runtime-to-evidence trace is audited;
- Natal/Temporal separation is regression-tested;
- selected source cases have reasoning reconstruction results;
- all uncovered/blocked assets are classified;
- no P0 fidelity defect is unresolved;
- a versioned PL4-A closure report is produced;
- Product readiness matrix is updated without claiming external predictive validity.

## Human Gate

No new Human Gate is implied by running fidelity tests. Any benchmark-driven proposal to change canonical meaning or architecture is a separate R3/Human-Gate path.

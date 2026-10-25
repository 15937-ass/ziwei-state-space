# Option C contract validation probe — execution evidence

Status: `PROBE_ONLY_NOT_CANONICAL`  
Issue: [#747](https://github.com/15937-ass/ziwei-state-space/issues/747)  
Branch: `knowledge/core-747-qi-qr-contract-probe`  
Base main at branch creation: `3f204a7908fe44749b882c8fe8662404293fb2a2`

## Scope
- Synthetic probe fixture, regression tests, capability report, historical-test cache decoupling, and Core execution cache only.
- No canonical ontology, shared schema, controlled vocabulary, source row, accepted mapping, Product/runtime, registry, lock, or consumer permission changes.
- Fixture source wording and all probe IDs are explicitly synthetic; no source claim is being promoted.

## Exact-head validation
The initial branch commit establishes the test target. The exact PR head and repository-quality-gate run must be recorded in the final Issue/PR closeout comment after the complete gate passes. This file is intentionally not rewritten after that run, because doing so would create a new unvalidated head.

## Expected checks
- Existing Review Schema v0.3 epistemic/review fields and KB Schema v0.3 target/operator/condition/provenance/rationale fields are verified against live files.
- Target-specific rationale and probe-only evidence-role metadata are kept separate for two targets sharing the same source reference.
- Missing typed `evidence_role` and `mapping_disposition` are reported as proposal-only schema gaps, not silently added.
- Source alternatives, QI-15 role slots, QR-04 resource states, four uncertainty states, and candidate/canonical/consumer gates remain distinguishable.
- Historical Issue #735 tests no longer pin mutable `CORE_STATE.yaml` pointers to a closed issue/merged PR.

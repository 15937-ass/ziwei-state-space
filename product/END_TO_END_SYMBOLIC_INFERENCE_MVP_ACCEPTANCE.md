# End-to-End Symbolic Inference MVP Acceptance v0.1

Status: IMPLEMENTATION IN PROGRESS

## Goal

Implement a deterministic, source-traceable execution path that composes existing PL1, PL2, PL3-N, and PL3-T components. This is a rule-driven inference system, not a trained life-outcome predictor.

## Target vertical slice

Final target: natal Career analysis with one selected decade and one selected year. Career-specific execution is gated on canonical CA04–CA09 closure and a Product-side provider audit. Until the Career provider is implemented, the integration harness uses the already executable Wealth provider only to verify pipeline plumbing; it must not fabricate Career evidence.

## Pipeline contract

1. Consume one normalized full chart snapshot containing natal and temporal assets.
2. Resolve only selected domains through the existing NatalDomainProviderRegistry.
3. Build the deterministic NatalStateProfile.
4. Adapt the requested temporal target to structured TemporalAssetBundle facts.
5. Compile only an explicitly normalized reaction registry.
6. Match reactions using existing natal and temporal condition atoms.
7. Build the TemporalEnvironmentProfile and LayeredEvidencePackage.
8. Return a structured run record with rule/source traces, match diagnostics, registry status, and blockers.

## Fail-closed requirements

- The same snapshot supplies both natal and temporal processing; engine provenance must match.
- Unknown domain IDs, missing targets, invalid registries, and invalid condition layers raise explicit errors.
- An empty production temporal registry returns PARTIAL_TEMPORAL_REGISTRY_EMPTY, not success.
- A test-only reaction registry can exercise the matching path but is marked TEST_FIXTURE_ONLY and blocked from canonical-ready status.
- No LLM selects rules or assigns probabilities.
- No numeric gain, probability, universal valence, or unsupported manifestation mapping is inferred.
- Personal and empirical namespaces remain empty unless a separately approved component supplies them.
- NatalStateProfile remains independent of the selected target time; only the temporal profile changes with the temporal target.

## Current implementation boundary

This work unit adds orchestration and regression tests around existing components. It does not claim that Career rules are already executable, that the production temporal reaction registry is populated, or that real-world prediction accuracy has been established.

## Exit criteria

- Deterministic run identity for the same snapshot, question, registry, and code version.
- End-to-end structured output from the current executable domain.
- Explicit handling of empty production registry and test-only registry.
- Product quality gate passes.
- A separate gap report identifies the remaining Career provider and source-normalized temporal-reaction dependencies.

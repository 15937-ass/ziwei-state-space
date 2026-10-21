# Proposal #491 — Product Knowledge Dependency, Impact and Promotion Governance

Status: **APPROVED / IMPLEMENTING**  
Tracking Issue: #491  
Lane: GOVERNANCE_ONLY  
Decision authority: PI instruction in chat on 2026-10-21  
Architecture basis: Product v0.4 / Proposal #425

## Motivation

Product v0.4 already separates canonical declarative knowledge `Kc`, response knowledge `Kr`, expert policy `π`, empirical parameters `θ`, and individual belief `b`. It also carries `knowledge_version` through multiple Product artifacts and already rejects some cross-version composition.

The remaining gap is dependency governance.

A Product work unit may currently declare a frozen Knowledge baseline while loading Knowledge files from the current checkout. A later Knowledge merge can therefore change the bytes read by a rerun even when the Product artifact still claims the old baseline. Some `knowledge_version` values are descriptive or count-based and are not content identities. Knowledge and Product also advance independently, but there is no single Product contract for deciding whether a Knowledge update requires no action, provenance revalidation, symbolic recompilation, method replay, dataset rematerialization, or model retraining.

This is acceptable while artifacts are small and mostly symbolic, but it is unsafe before PL3-R, Forecast Ledger expansion, and especially PL5 calibration/training.

## Goals

1. Make every reproducibility-critical Product dependency on Knowledge machine-verifiable.
2. Allow Knowledge to keep advancing independently without silently mutating active Product behavior.
3. Allow Product to absorb newer Knowledge deliberately through impact analysis and promotion.
4. Rebuild only affected Product artifacts instead of forcing whole-system rebuilds.
5. Preserve exact historical lineage for forecasts, datasets, models, benchmarks, and evidence packages.
6. Detect stale Product recovery state without creating a second execution truth.
7. Keep the mechanism lightweight and Git-native until data/model scale justifies external registries.

## Non-Goals

- No Zhongzhou semantic reinterpretation.
- No automatic promotion from Knowledge `main`.
- No Product ownership of canonical Knowledge.
- No Kr normalization in this Proposal.
- No Response Compiler implementation.
- No probability or numeric qi semantics.
- No DVC, MLflow, external model registry, or artifact server requirement in v0.1.
- No requirement that every Knowledge edit rebuild every Product artifact.

## Current Problem

### 1. Declared frozen baseline is not yet sufficient

A constant such as:

~~~text
FROZEN_BASELINE = <commit>
~~~

does not prove that the files actually consumed at runtime are the bytes from that commit when the loader reads mutable paths from the current checkout.

A reproducible Product artifact therefore needs both:
- a human-readable/version reference; and
- content identity for the exact Knowledge inputs it consumed.

### 2. Descriptive knowledge_version is not a content identity

Labels such as rule counts are useful for display but cannot distinguish two artifacts with the same row count and different semantics.

### 3. Knowledge main and active Product must not be the same mutable concept

Knowledge `main` is the current accepted research state.

Active Product must instead consume an explicitly promoted immutable dependency set. Newer Knowledge is a candidate until Product impact and validation complete.

### 4. Training contamination risk

Before PL5, any dataset or model derived from Knowledge must be able to answer which exact Knowledge semantics generated its features/labels. Incompatible Knowledge versions may not be silently concatenated.

## Proposed Design

## A. Knowledge Input Bundle (KIB)

Product consumes an immutable manifest called a Knowledge Input Bundle.

The bundle is componentized by Product meaning rather than one global monolithic version:

~~~text
K_signal
K_response
K_manifest
K_method
~~~

A bundle component records at minimum:

~~~yaml
component_id:
contract_version:
artifact_refs:
source_commit:
artifact_digest:
semantic_digest:
~~~

`artifact_digest` identifies the complete serialized artifact bytes/normalized document.

`semantic_digest` identifies only fields that can affect Product semantics or execution, according to a versioned per-artifact canonicalization contract.

This distinction allows a source-location/comment/provenance-only correction to be detected without automatically forcing symbolic recompilation.

KIB v0.1 is metadata; it does not duplicate Knowledge files.

## B. Product Knowledge Lock

Product maintains an explicit active lock:

~~~text
PRODUCT_KNOWLEDGE.lock
~~~

The lock references exactly one promoted KIB and its component digests.

Reproducibility-critical Product loaders/builders must fail closed when:
- a required component is missing;
- the current artifact digest does not match the lock;
- a semantic digest does not match;
- the loader cannot prove which KIB it consumed.

The display field `knowledge_version` remains allowed, but it is not sufficient proof by itself.

## C. Candidate versus Active

Knowledge merges create new accepted research state, not immediate Product mutation.

The state machine is:

~~~text
Knowledge main
-> Candidate KIB
-> semantic diff / impact report
-> affected Product rebuild/recompile/replay
-> validation
-> promotion
-> Active Product Knowledge Lock
~~~

There is no automatic `latest` consumption for production/reproducibility-critical Product artifacts.

## D. Semantic Impact Classification

A Product-side impact report compares active and candidate KIBs and classifies each changed component/rule into at least:

~~~text
NO_RUNTIME_EFFECT
PROVENANCE_REVALIDATION
READINESS_REBUILD
SYMBOLIC_RECOMPILE
METHOD_REPLAY
MANIFESTATION_REBUILD
DATASET_REMATERIALIZE
RETRAIN_OR_RECALIBRATE
MIGRATION_REQUIRED
~~~

The classifier is conservative: uncertainty escalates to the more restrictive action or BLOCKED, never to a less restrictive one.

Examples:
- source page corrected, semantic digest unchanged -> PROVENANCE_REVALIDATION;
- SEMANTIC_ONLY metadata refined but remains non-executable -> READINESS_REBUILD;
- executable activation/scope/operator/effect target changes -> SYMBOLIC_RECOMPILE;
- K_method/evidence-order contract changes -> METHOD_REPLAY;
- K_manifest mapping changes -> MANIFESTATION_REBUILD;
- feature or label semantics used by a dataset change -> DATASET_REMATERIALIZE;
- calibrated/trained model consumed a changed dataset -> RETRAIN_OR_RECALIBRATE;
- schema incompatibility without safe converter -> MIGRATION_REQUIRED.

## E. Dependency Propagation

The minimum Product dependency graph is:

~~~text
K_signal -> N
K_response + N + E -> tau
K_manifest + tau -> M0
K_method -> pi / expert replay
M0 + observations -> empirical dataset
dataset -> theta/model
all versioned components -> Forecast/Evidence lineage
~~~

When an upstream semantic identity changes, only reachable downstream artifacts become stale.

Unrelated Knowledge changes do not force global Product invalidation.

## F. Promotion Gate

Promotion from candidate KIB to active lock requires:
1. impact report complete;
2. all required affected artifacts rebuilt or explicitly marked blocked;
3. relevant canonical-fidelity/regression tests pass;
4. method replay passes when K_method is affected;
5. no incompatible stale dataset/model remains presented as current;
6. promotion writes the new active lock atomically in one Product work unit.

A failed candidate does not alter the active lock.

Rollback is moving the active lock back to a previously validated immutable KIB/Product artifact set; historical artifacts are never rewritten.

## G. Dataset and Model Lineage

Before PL5 empirical calibration, every calibration/training dataset must record at minimum:

~~~text
dataset_version
knowledge_bundle_id
knowledge_bundle_digest
compiler_version
manifestation_schema_version
feature_schema_version
label_policy_version
information_cutoff
~~~

Every trained/calibrated model must additionally record:

~~~text
model_version
dataset_version
knowledge_bundle_id
training/calibration code commit
benchmark/metrics reference
~~~

Samples generated under incompatible Knowledge semantics may not be silently concatenated. Mixing requires an explicit DatasetMigration proving compatibility or relabel/rematerialization.

## H. Forecast / Historical Immutability

Forecast Ledger records retain the KIB/model/method versions used at issuance.

A later Knowledge correction may create:
- an impact note;
- a new forecast/model version for future use;
- a research comparison.

It may not rewrite the old forecast as if the new knowledge had been available before the information cutoff.

## I. Product State Recovery

`product/PRODUCT_STATE.yaml` remains a recovery cache only.

It must carry an `as_of_main_commit` or equivalent durable freshness marker after the Product-side implementation.

Bootstrap rule:
- GitHub Issue/PR truth wins;
- stale PRODUCT_STATE is repaired;
- stale state must not cause a completed work unit to be re-executed or treated as active.

## Alternatives

### Automatic Product tracking of Knowledge main
Rejected. It destroys reproducibility and creates unreviewed behavior changes.

### Permanent pinning to one Knowledge version
Rejected. It prevents Product from benefiting from source research.

### Full Product rebuild for every Knowledge merge
Rejected. It is wasteful and does not reflect the componentized K_signal/K_response/K_manifest/K_method architecture.

### Immediate adoption of DVC/MLflow
Deferred. Their version/lineage principles are useful, but current repository-scale canonical JSON/CSV and symbolic artifacts are still manageable with Git-native manifests, digests, and promotion. External tooling may be reconsidered when dataset/model size justifies it.

## Compatibility

The design is additive.

Existing `knowledge_version` fields remain supported as human-readable compatibility fields. Existing N/E knowledge-version equality checks remain valid and are strengthened later by KIB identity.

Existing Product #462/#482 frozen acceptance records remain historical evidence; this Proposal does not retroactively claim that they were content-locked.

## Knowledge Impact

No Knowledge files or canonical meanings change.

Knowledge lane continues to merge source-reviewed improvements normally.

The Product lane consumes those improvements only through candidate KIB generation and promotion.

## Product Impact

The Product critical path gains a bounded reliability gate before NOW-6:

1. `PRODUCT_KNOWLEDGE_LOCK_V0_1`
2. `PRODUCT_KNOWLEDGE_IMPACT_V0_1`

`WANG_BLIND_EVIDENCE_MATERIALIZATION_V0_1` may proceed independently because it does not require promoting new canonical response semantics, but any Product artifact it produces must later join the same provenance contract when the lock implementation is available.

Before PL5:
3. `DATASET_MODEL_LINEAGE_V0_1` is mandatory.

## Risks and Failure Modes

### False semantic stability
If semantic canonicalization omits a behavior-relevant field, a changed rule could retain the same semantic digest.

Mitigation: semantic-field contracts are versioned, tests include mutation cases, and unknown fields fail conservatively.

### Over-invalidation
An overly broad dependency graph may rebuild too much.

Mitigation: start conservative, measure impact, refine edges only with deterministic evidence.

### Under-invalidation
A missing dependency edge could preserve stale downstream artifacts.

Mitigation: explicit lineage fields on every derived artifact and regression fixtures for known dependency paths.

### Lock drift
A Product loader may bypass the lock.

Mitigation: central lock verifier plus tests that direct mutable Knowledge consumption is rejected for governed production paths.

### Governance overhead
Too many releases could slow research.

Mitigation: Knowledge merges remain normal; candidate KIB/promotion is Product-side and occurs at meaningful integration checkpoints, not after every source-review batch.

## Test Plan

Governance implementation:
- repository quality gate;
- governance lane validator;
- static inspection that no Product/Knowledge semantics changed.

PRODUCT_KNOWLEDGE_LOCK_V0_1:
- digest determinism;
- path/order-independent canonicalization where declared;
- lock mismatch fail closed;
- active bundle exact reconstruction;
- mutation tests for semantic versus provenance-only changes.

PRODUCT_KNOWLEDGE_IMPACT_V0_1:
- no-op changes stay no-op;
- semantic changes trigger expected class;
- dependency propagation invalidates only reachable downstream artifacts;
- unknown/incompatible changes escalate safely.

Before PL5:
- dataset lineage completeness;
- incompatible-bundle mixing rejection;
- explicit migration positive fixture;
- model -> dataset -> KIB lineage reconstruction.

## Migration Plan

Phase 1 — Governance (this Issue):
- freeze the contract;
- amend Product Roadmap/execution plan;
- repair Product recovery pointer through #482/#484.

Phase 2 — Product lock:
- create KIB schema/manifest;
- create active Product lock;
- verify #462/#482 input families;
- add digest verifier and tests.

Phase 3 — Product impact:
- semantic diff;
- dependency map;
- impact report;
- candidate/active promotion gate.

Phase 4 — Existing consumers:
- migrate Response Corpus, Response Semantics Adapter, Career/Natal provider and later PL3-R to the lock.
- do not retroactively rewrite historical acceptance artifacts; record migration provenance.

Phase 5 — PL5 readiness:
- dataset/model lineage and migration gate.

## Rollback Plan

Before Product lock promotion, existing Product behavior remains unchanged.

After promotion, rollback means selecting the previous validated Product Knowledge Lock and rebuilding/reusing its already validated artifacts. Knowledge main is never reverted merely to roll Product back.

## Graduation Criteria

This governance Proposal is implemented when:
- Roadmap and execution plan contain the dependency/promotion contract;
- Product state points to the lock/impact implementation before NOW-6;
- PRODUCT_ONLY implementation work units are clearly bounded.

The Product reliability program graduates when:
- active KIB and lock are machine-verifiable;
- all governed critical-path consumers fail closed on mismatch;
- impact classification and dependency propagation are deterministic;
- candidate promotion is validated;
- PL5 cannot start without dataset/model lineage.

## Human Gate

PI approved this direction in chat on 2026-10-21 by instructing that the Product-side changes be summarized, made reliable, and applied to GitHub.

This approval covers dependency/version governance only.

It does not authorize changes to Zhongzhou source meaning, school boundaries, canonical activation rules, manifestation truth, empirical probabilities, or causal claims.

## Decision

**APPROVED.**

Adopt explicit Knowledge Input Bundle + Product lock + semantic impact + selective rebuild + validation/promotion as the Product-side mechanism for consuming Knowledge updates.

## Implementation History

- 2026-10-21: Proposal #491 created from the Product/Knowledge version-drift analysis.
- 2026-10-21: PI approval recorded in chat.
- 2026-10-21: Governance implementation started on `governance/491-product-knowledge-dependency`.

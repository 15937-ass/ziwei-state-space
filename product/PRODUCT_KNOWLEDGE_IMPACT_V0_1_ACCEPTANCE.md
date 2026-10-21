# Product Knowledge Impact v0.1 Acceptance

Status: **IMPLEMENTED — VALIDATION PENDING**  
Tracking Issue: #500  
Architecture authority: Proposal #491 / Product v0.4 NOW-5A  
Dependency: Product #494 / PR #495 Knowledge Lock v0.1

## 1. Purpose

This work closes the second Product-side version-governance gap:

> after Product can prove which Knowledge bundle it consumes, it must also
> determine what a candidate Knowledge update actually invalidates before the
> active lock can move.

The controlled path is now:

~~~text
active KIB
+ explicit candidate KIB
-> semantic/content diff
-> component impact
-> downstream invalidation
-> required validation
-> PROMOTABLE or BLOCKED
~~~

The gate itself never mutates the active lock.

## 2. Candidate construction

`src/product/knowledge_impact.py` provides an explicit candidate builder.

Default behavior:
- reuse the active component artifact inventory;
- recompute exact and semantic digests from current repository bytes;
- attach a caller-supplied candidate source commit and bundle id;
- never infer "latest Knowledge" as an active Product dependency.

For a newer versioned Knowledge artifact, Product must explicitly replace the
relevant component inventory. A new artifact path requires an explicit semantic
contract.

This prevents a newly created Knowledge file from silently entering Product
just because it exists on main.

## 3. Direct impact classes

The v0.1 classifier distinguishes:

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

Current direct component policy:

| Component | semantic change |
|---|---|
| K_signal | SYMBOLIC_RECOMPILE |
| K_response | READINESS_REBUILD |
| K_manifest | MANIFESTATION_REBUILD |
| K_method | METHOD_REPLAY |

K_response is intentionally classified as READINESS_REBUILD in the current
pre-Response-Compiler phase. The report still records tau/M0/dataset/model as
downstream IF_PRESENT invalidations.

When the Response Compiler becomes an active governed artifact, its own Product
work unit must consume this dependency edge and upgrade the concrete rebuild
step accordingly.

## 4. Provenance-only changes

An exact artifact digest may change while its semantic digest remains stable.

That case is:

~~~text
PROVENANCE_REVALIDATION
~~~

not symbolic recompilation.

The current active production bundle remains conservative
`RAW_CONTENT_FULL_V0_1`, so exact changes in today's locked artifacts also
change semantic identity. The impact engine nevertheless supports narrower
reviewed semantic contracts, and tests cover provenance-only behavior.

This avoids pretending the optimization already applies to active artifacts
before their semantic-field contracts are reviewed.

## 5. Dependency propagation

The explicit downstream graph is:

~~~text
K_signal
-> NATAL_ESSENCE
-> RESPONSE_PROFILE_TAU
-> MANIFESTATION_M0
-> EMPIRICAL_DATASET
-> CALIBRATED_MODEL

K_response
-> RESPONSE_READINESS
-> RESPONSE_PROFILE_TAU
-> MANIFESTATION_M0
-> EMPIRICAL_DATASET
-> CALIBRATED_MODEL

K_manifest
-> MANIFESTATION_M0
-> EMPIRICAL_DATASET
-> CALIBRATED_MODEL

K_method
-> METHOD_POLICY_PI
-> EXPERT_METHOD_REPLAY
~~~

Only reachable artifacts are invalidated.

Future artifacts that do not yet exist are reported as:

~~~text
IF_PRESENT
~~~

rather than being falsely described as rebuilt or retrained.

## 6. Migration boundary

Component contract-version changes, artifact semantic-contract changes, artifact
type changes, or structurally invalid candidate bundles escalate to:

~~~text
MIGRATION_REQUIRED
~~~

Promotion is blocked.

The impact engine never assumes two incompatible semantic representations are
equivalent.

## 7. Promotion gate

Each direct impact class maps to a validation gate:

| Impact | Required validation |
|---|---|
| NO_RUNTIME_EFFECT | none beyond candidate verification |
| PROVENANCE_REVALIDATION | LOCK_REVERIFY |
| READINESS_REBUILD | READINESS_REGRESSION |
| SYMBOLIC_RECOMPILE | CANONICAL_FIDELITY_REGRESSION |
| METHOD_REPLAY | METHOD_REPLAY_REGRESSION |
| MANIFESTATION_REBUILD | MANIFESTATION_FIDELITY_REGRESSION |
| DATASET_REMATERIALIZE | DATASET_LINEAGE_VALIDATION |
| RETRAIN_OR_RECALIBRATE | MODEL_VALIDATION |

Promotion returns only:

~~~text
PROMOTABLE
BLOCKED
~~~

A PROMOTABLE result means an explicit Product integration work unit is allowed
to update the active lock. It does not update the lock by itself.

Any failed candidate verification, missing required validation, or migration
blocker returns BLOCKED.

## 8. Bootstrap candidate on current main

The checked-in candidate is:

~~~text
KIB-CANDIDATE-ISSUE-500-V0_1
~~~

It advances the candidate source snapshot from the original active-bundle source
commit to the Product #494 merged main commit while retaining the same 58
governed artifact identities and semantics.

Expected result:

~~~text
source_commit_changed = true
overall_impact = NO_RUNTIME_EFFECT
downstream_invalidations = []
promotion_gate = PROMOTABLE
recommendation = SKIP_NO_RUNTIME_EFFECT
~~~

The important result is not that the candidate should replace the active lock.
It should not; that would only churn provenance.

The result demonstrates that unrelated repository/Knowledge progress does not
force Product rebuild when governed semantics are unchanged.

## 9. Controlled Knowledge-update procedure after graduation

Once this work unit is merged, a Product-side Knowledge update can use:

~~~text
1. keep active KIB/lock unchanged
2. select the newer Knowledge artifacts explicitly for one or more components
3. build candidate KIB
4. verify candidate bytes/semantics
5. compare active vs candidate
6. perform only the direct/reachable rebuilds required by the report
7. supply deterministic validation evidence
8. evaluate promotion gate
9. if PROMOTABLE, update the active lock in a separate explicit Product
   integration commit/work unit
10. preserve the previous lock/bundle for rollback and historical lineage
~~~

This is the point at which Product can safely begin consuming newer Knowledge
releases without mixing them silently into existing artifacts.

## 10. What remains outside v0.1

This work does not:
- select which newly created Knowledge files should become the next canonical
  Product component inventory;
- reinterpret or normalize Zhongzhou rules;
- create compiler-ready Kr;
- implement tau or M0;
- implement DatasetMigration;
- train or recalibrate models;
- auto-promote Knowledge main;
- update Product recovery state.

The next Product-side Knowledge integration work should therefore be a bounded
candidate-bundle update against explicit Knowledge outputs, not an uncontrolled
sync to "latest".

## 11. Acceptance tests

The new deterministic tests cover:
- current bootstrap candidate and versioned impact report agreement;
- source-commit-only advance remains NO_RUNTIME_EFFECT;
- provenance-only change -> PROVENANCE_REVALIDATION;
- K_signal semantic change -> N/tau/M0/data/model downstream only;
- K_response semantic change -> readiness/tau/M0/data/model, not N;
- K_method semantic change -> method replay only;
- K_manifest semantic change -> M0/data/model only;
- contract incompatibility -> MIGRATION_REQUIRED;
- missing validation -> BLOCKED;
- complete validation -> PROMOTABLE;
- failed candidate verification -> BLOCKED;
- new candidate artifact requires explicit semantic contract;
- explicit versioned inventory construction;
- promotion-gate evaluation does not mutate the active lock.

## 12. Graduation criterion

This architecture upgrade is complete enough to begin Product-side Knowledge
updates when:
1. this work unit is merged to main;
2. final repository/Product validation is green;
3. the active lock remains unchanged;
4. the candidate impact and promotion-gate tests pass.

After those conditions are met, the next work is no longer architecture
plumbing. It is the first controlled Product Knowledge promotion candidate.

That future candidate may still be blocked by Knowledge content quality. In
particular, NOW-6 still requires compiler-ready canonical Kr; this architecture
does not manufacture missing semantics.

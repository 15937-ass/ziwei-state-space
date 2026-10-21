# Product Knowledge Lock v0.1 Acceptance

Status: **IMPLEMENTED — INTERNALLY VALIDATED**  
Tracking Issue: #494  
Architecture authority: Proposal #491 / Product v0.4 NOW-5A

## 1. Purpose

This work unit converts the Product's previously declarative "frozen Knowledge
baseline" idea into a machine-verifiable dependency boundary.

The governing rule is:

~~~text
Knowledge main
!=
active Product Knowledge
~~~

A Knowledge merge does not silently mutate Product behavior. Product consumes
an explicitly pinned Knowledge Input Bundle (KIB), verifies the exact inputs
before governed reads, and requires a later impact/promotion work unit before
moving to a different semantic baseline.

This work does not change Zhongzhou meaning, create canonical Kr, implement
ResponseProfile tau, or claim predictive validity.

## 2. Active bundle

Active bundle:

~~~text
KIB-PRODUCT-20261021-V0_1
~~~

Source snapshot used to construct the manifest:

~~~text
dabc492895721b0ccc310b32329f4585c6d599bf
~~~

Coverage is componentized:

| Component | v0.1 coverage | Locked artifacts | Content readiness |
|---|---|---:|---|
| K_signal | Career natal/provider inputs | 11 | existing accepted Product baseline |
| K_response | Response Semantics + Response Corpus input families | 19 | source material present; compiler-ready canonical Kr remains 0 |
| K_manifest | manifestation knowledge | 0 | EMPTY_NOT_READY |
| K_method | Wang 24-case / method-policy inputs | 28 | existing method-policy baseline; full expert replay still blocked by blind-evidence materialization |

Total exact locked artifacts: **58**.

The empty K_manifest component is intentional. The lock records the absence of
ready canonical manifestation content instead of using an empty registry as a
fidelity claim.

## 3. Bootstrap promotion is non-semantic

The initial lock does not promote newer, unreviewed Knowledge into Product.

For each populated component, the exact Git blob identities were checked
against the already accepted Product baseline:

~~~text
K_signal
11 / 11 identical
accepted baseline:
720a617f6f2c9811b788af3e7b0865c1a3096e62
(Product #416 accepted Career baseline)

K_response
19 / 19 identical
accepted baseline:
16bb9b30f491afa27368e88767e5662dbdc54983
(the frozen Product #462/#482 response baseline)

K_method
28 / 28 identical
accepted baseline:
9d3e4d61bc0729693a307c96345820fec798875d
(Product #453 Method Policy baseline)
~~~

Therefore this v0.1 activation changes dependency enforcement, not canonical
content or previously accepted Product behavior.

Historical #462 and #482 acceptance artifacts remain historical records and are
not rewritten to pretend they had this lock at the time they were produced.

## 4. Exact content identity

Every governed artifact stores an exact Git blob content address:

~~~text
git-sha1:<blob-id>
~~~

The Product verifier recomputes Git's blob object hash from local bytes:

~~~text
sha1("blob " + byte_length + NUL + content)
~~~

This matches the content identity exposed by Git/GitHub and makes the lock
independently verifiable without a separate artifact store.

A single locked-byte change therefore causes fail-closed mismatch.

## 5. Semantic identity

The runtime supports versioned semantic-digest contracts:

~~~text
RAW_CONTENT_FULL_V0_1
JSON_CANONICAL_FULL_V0_1
JSON_RESPONSE_SEMANTICS_NO_PROVENANCE_V0_1
~~~

For the active production bundle, v0.1 intentionally uses
RAW_CONTENT_FULL_V0_1 for all populated components.

This is conservative:

~~~text
any byte change
->
semantic change for v0.1 impact purposes
~~~

It may over-invalidate on a provenance/format-only edit, but it cannot silently
treat a behavior-relevant edit as unchanged.

The narrower JSON contracts are implemented and unit-tested so the next Product
impact work can safely distinguish semantic changes from provenance-only
changes after their field contracts are explicitly reviewed.

Product does not guess which current Knowledge fields are "non-semantic" merely
to reduce rebuilds.

## 6. Active lock

The active lock is:

~~~text
product/PRODUCT_KNOWLEDGE.lock.json
~~~

It pins:
- one active bundle path;
- one bundle id;
- exact bundle artifact digest;
- bundle semantic digest;
- source snapshot;
- promotion state;
- auto_refresh = false.

There is no latest behavior and no automatic rewrite of the lock.

A failed or changed candidate therefore cannot silently become the active
Product dependency.

## 7. Runtime enforcement

The following existing Product paths now enforce the lock:

### Response Corpus ingestion

~~~text
src/product/response_corpus_ingestion.py
~~~

Every in-repository CSV/JSON Knowledge read used by the #482 inventory must be
registered in K_response and match its exact/semantic digest.

### Response Semantics adapter

~~~text
src/product/response_semantics_adapter.py
~~~

Every governed in-repository Response Semantics JSON read must pass K_response
artifact verification.

### Career natal provider

~~~text
src/product/career_natal_domain_provider.py
~~~

The default Career provider requires the full active K_signal component lock to
verify before consuming its Product registry/source mappings.

### Wang Method Policy

~~~text
src/product/method_policy.py
~~~

Wang fold execution and method-policy readiness audit require the full active
K_method component lock.

Test fixtures outside the repository may still exercise low-level parsers. An
in-repository path, however, cannot bypass the active lock merely by being
passed directly to a governed loader.

## 8. Fail-closed conditions

The verifier fails closed for at least:
- missing lock/bundle;
- unsupported schema;
- missing required component;
- duplicate artifact registration;
- path escape / invalid path;
- missing artifact;
- bundle exact-digest mismatch;
- artifact exact-digest mismatch;
- artifact semantic-digest mismatch;
- component semantic projection mismatch;
- lock/bundle id mismatch;
- lock/bundle semantic mismatch;
- lock/bundle source-snapshot mismatch;
- unsupported semantic contract;
- governed in-repository artifact not present in the active component.

Runtime verification never auto-generates or auto-refreshes a replacement lock.

## 9. NOW-6 remains blocked by content, not by version plumbing

This work closes a reliability gap only.

The #482 Response Corpus result remains:

~~~text
source temporal candidates = 1039
compiler-ready canonical Kr = 0
NOW-6 Response Compiler input ready = false
~~~

The Product lock must not be used as a reason to promote source candidates into
canonical Kr.

The first N + E -> tau vertical slice still requires Knowledge-owned,
source-reviewed compiler-ready Kr.

## 10. What is intentionally not implemented

This work unit does not implement:
- active-vs-candidate semantic diff;
- dependency-graph propagation;
- NO_RUNTIME_EFFECT / RECOMPILE / REPLAY / RETRAIN classification;
- candidate-to-active promotion automation;
- DatasetMigration;
- model/dataset lineage;
- full-repository coverage of every historical Product consumer;
- canonical manifestation knowledge.

Those belong to subsequent bounded Product work, beginning with:

~~~text
PRODUCT_KNOWLEDGE_IMPACT_V0_1
~~~

and later the pre-PL5 Dataset/Model lineage gate.

## 11. Reliability properties

After this work, "frozen baseline" is no longer only a human claim for the
governed Product paths.

It is backed by:

~~~text
accepted baseline
+ exact artifact identities
+ component identities
+ bundle identity
+ active lock
+ fail-closed runtime verification
~~~

A later Knowledge update may exist on main while the Product remains
reproducibly attached to the active bundle until an explicit impact analysis and
promotion occurs.

## 12. Validation evidence

Validated on PR #495 head `689fa3ca5ccd369357dbf27364e2281e8c195c0f` before this
documentation-only status update:

- repository quality gate: PASS;
- full pytest: **2152 passed / 0 failed**;
- deterministic P0 repository audit: PASS;
- Product lane/governance validation: PASS;
- product-p1-dual-engine: PASS;
- product-p1-b02-calendar: PASS;
- product-p1-b02b-zi-day: PASS;
- product-p1-b02c-temporal: PASS.

Specific mutation/regression tests cover:
- exact byte drift;
- semantic field drift;
- provenance-only semantic projection stability;
- JSON key-order / formatting invariance;
- unknown semantic contract rejection;
- unregistered in-repository input rejection;
- unrelated component drift does not invalidate an unchanged component;
- Response Corpus remains 1039 source temporal candidates / 0 compiler-ready Kr.

The final documentation-only head is required to pass the repository gate again
before merge; the PR conversation records the exact final-head evidence.

## 13. Acceptance boundary

Passing these tests means:

> Product can prove and enforce the exact v0.1 Knowledge inputs used by the
> governed critical-path consumers.

It does **not** mean:
- the Knowledge Base is complete;
- Kr is compiler-ready;
- tau/M0 exists;
- expert-method fidelity is validated;
- predictive validity is validated;
- the system is production-ready.

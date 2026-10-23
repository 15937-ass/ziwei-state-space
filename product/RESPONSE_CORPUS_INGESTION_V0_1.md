# Response Corpus Ingestion / Readiness v0.1

Issue: #482  
Lane: PRODUCT_ONLY  
Frozen Knowledge baseline: `16bb9b30f491afa27368e88767e5662dbdc54983`

## 1. Purpose

NOW-5 does **not** ask Product to invent response rules. It asks Product to answer a narrower question before NOW-6:

> What source-backed temporal-response material exists, and how much of it is actually in a canonical Kr form that the Decade/Year Response Compiler may consume?

This distinction matters because the repository already contains a large amount of temporal source material, especially in the sixty-system corpus. Raw source abundance must not be mistaken for executable dynamic inference.

## 2. Exact source families consumed

v0.1 reads only Knowledge-owned metadata and uses exact selectors:

| Family | Exact selector | Current rows |
|---|---|---:|
| Major-star canonical | `rule_family == temporal_response` | 24 |
| Sixty-system canonical | `interaction_role == temporal_reaction` | 1015 |
| Career temporal audit | all explicitly audited rows | 9 |
| Response Semantics pilot | all pilot ResponseSemanticsRecord rows | 8 |

Free-text words such as “大限”, “流年”, “decade”, “year”, “运限” are **not** production selection logic.

The sixty-system inventory also reads the v0.3 review sidecar and A0 schema-override sidecar so the Product report does not treat the immutable raw canonical CSV as the whole reviewed view.

## 3. What exists now

### 3.1 Source temporal candidates: 1039 rows

There are **24** major-star `temporal_response` rows and **1015** sixty-system `temporal_reaction` rows.

All 1039 selected rows have the basic source fields required by this inventory: identity/anchor label, source location, condition, target literal, operator and evidence text.

But this does **not** make them Kr.

Current review metadata is important:

- major-star selected rows: 24/24 `MODEL_SELF_REVIEWED`, 24/24 source epistemic `EXPLICIT`, but source-span verified = 0/24 and normalization verified = 0/24;
- sixty-system selected rows: 1015/1015 `MODEL_SELF_REVIEWED`, 1015/1015 source epistemic `EXPLICIT`, but source-span verified = 0/1015 and normalization verified = 0/1015;
- among the 1015 sixty-system candidates, normalization epistemic is `UNRESOLVED` for 980 and `IMPLEMENTATION` for 35; 35 selected rows have an A0 schema override.

These fields are reported exactly as Knowledge stores them. Product does not upgrade them.

### 3.2 Career temporal audit: 9 rows, 0 eligible

The existing Career WP07B audit already makes a stronger Knowledge-owned decision:

- 9 candidates audited;
- 8 blocked;
- 1 case-support-only exclusion;
- **0 eligible for the current compiler**;
- no executable pilot emitted;
- production registry should remain empty.

Product preserves that decision literally. It does not recover “apparently obvious” rules from the blocked prose.

### 3.3 Response Semantics pilot: vocabulary, not temporal Kr

The 8 pilot ResponseSemanticsRecord rows are useful semantic structure:

- 4 `LEXICAL_ONLY`;
- 4 `STRUCTURAL_ONLY`;
- 0 `SAFE_SYMBOLIC`;
- 0 records with a temporal scope binding.

They help define language such as groups, composites and local response patterns, but they are not an N × E temporal corpus.

## 4. Readiness classes

The Product ingestion layer uses four classes:

- `SEMANTIC_VOCABULARY_ONLY`
- `SOURCE_TEMPORAL_CANDIDATE_AWAITING_KR_NORMALIZATION`
- `KNOWLEDGE_EXPLICITLY_BLOCKED`
- `COMPILER_READY_KR`

The first three describe the current repository. v0.1 detects **0 compiler-ready Kr records**.

## 5. Why 1039 candidates still do not unlock NOW-6

A source row can contain a temporal label, a condition, an operator and a target while still lacking the canonical contract required for deterministic N + E -> tau compilation.

The missing cross-family Kr contract is currently frozen as:

1. canonical Kr record identity;
2. natal essence binding;
3. encountered temporal-structure binding;
4. response-operator contract;
5. response effect-target contract;
6. temporal-scope execution contract;
7. Kr execution-status contract.

This is a **normalization/contract gap**, not a statement that the source says nothing. Product must wait for Knowledge-owned normalization rather than reverse-engineering a new Ziwei rule from existing columns.

## 6. Permanent fail-closed boundaries

~~~text
source explicit       != compiler ready
reviewed              != executable
normalized source row != canonical Kr record
favorable/unfavorable != numeric gain
decade_or_year        != two auto-generated executable rules
case support          != reusable rule
~~~

No probability, numeric response magnitude, ANY/ALL default, or hidden temporal split is introduced.

## 7. NOW-6 gate

At v0.1:

~~~text
source temporal candidate rows = 1039
compiler-ready Kr records      = 0
NOW6 input ready               = FALSE
Response Compiler implemented  = FALSE
ResponseProfile tau            = FALSE
predictive validity            = NOT_VALIDATED
~~~

This is useful progress: Product now knows exactly **where the corpus is rich** and exactly **why it is not yet a compiler input**.

## 8. Next dependency

Knowledge remains the primary producer for NOW-5. The next useful Knowledge output is not “more raw temporal rows”; it is a bounded, source-backed Kr normalization batch that binds natal essence and encountered temporal structure without inventing missing semantics.

Once such a batch exists, this Product audit can measure it and NOW-6 can begin with deterministic Decade + Year fixtures.

# Canonical + Expert-Method Fidelity Benchmark v0.1 — Acceptance

Tracking Issue: #643  
Lane: PRODUCT_ONLY  
Work unit: CANONICAL_AND_METHOD_FIDELITY_BENCHMARK

## Purpose

This versioned baseline keeps canonical fidelity and expert-method fidelity separate. It accounts for measurable coverage, blocked dependencies, and metrics that cannot yet be scored. It is not a combined quality score and does not measure real-world prediction.

## Reproduction

From the repository root:

~~~bash
python -m src.product.fidelity_benchmark --write
PYTHONPATH="$PWD" python -m pytest -q tests/test_product_fidelity_benchmark.py
~~~

The builder pins the exact Git blob IDs of the input artifacts. If an input changes, it fails closed and requires an explicit new benchmark version rather than silently changing the meaning of v0.1.

## Baseline result

- Wang source cases: 24.
- Source-explicit MethodPatterns: 6.
- Case × MethodPattern scope assessments: 144.
- Exact target-domain matches: 0.
- Explicit case-to-pattern source links: 0.
- Justified case-to-pattern bindings: 0.
- Limited pinned-engine chart artifacts with target-anchor verification: 11/24.
- Cases without a chart materialization artifact: 13/24.
- Full expert replay ready: 0/24.
- Production temporal reaction registry: empty, blocked on source-backed Knowledge normalization.
- Production manifestation ontology and mapping registries: empty, blocked on their Knowledge dependencies.

The 11 chart artifacts verify the reviewed target-palace identity and fourteen-major-star anchor only. Full-source-chart equivalence is not verified. MethodPattern records remain SEMANTIC_ONLY.

## Scoring semantics

- Canonical fidelity score: not produced by this baseline.
- Expert-method fidelity score: blocked because no case is ready for full expert replay and no eligible expert-trace comparisons exist.
- Combined score: never produced.
- Predictive validity: not evaluated.
- Empty production registries are BLOCKED, not PASS.
- Canonical-runtime trace completeness, runtime-wide deterministic reproducibility, contradiction preservation, and canonical-runtime unknown counts remain NOT_MEASURED.
- The expert-method section separately accounts for 24 eligible cases (0 replay-covered, 24 blocked) and 144 completed source-scope assessments; scope-review coverage is not method-fidelity coverage.
- The 64 insufficient-source-evidence and 24 missing-context-binding figures are case-pattern assessment dispositions, not real-world prediction errors.

## Boundaries

This report does not promote MethodPatterns, add canonical rules, alter Knowledge, introduce probabilities/weights, or authorize runtime effects. It does not activate or close the historical PL4-A phase. It implements the current v0.4 Product benchmark work unit only.

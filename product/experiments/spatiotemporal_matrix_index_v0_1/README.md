# Product matrix-vs-index benchmark v0.1

Status: **TEST_ONLY / NOT CANONICAL / NOT PRODUCTION-CONSUMABLE**

## Research question

The v0.3 experiment proved structural equivalence between the index view and a dense permutation-matrix view for a bounded full-chart projection. It did not measure runtime, memory, serialization size, or end-to-end cost. This experiment measures those costs before considering any change to the index baseline.

## Input and provenance

- This experiment is based on main commit 0c9210855d874045f577914e8ec27e909438ecf4.
- It copies the minimal v0.3 reduced fixture byte-for-byte from experiment head a2595cb5e88f854fccd19281e14a7950604ba783; the SHA-256 is pinned in fixture_manifest_v0.1.json.
- The fixture contains two engine-generated regression projections (CR-001, CR-031), each with two target snapshots and six temporal scopes. It is not source-transcribed ground truth.
- Source-row hashes and the upstream producer artifact pins are retained in the manifest.
- The benchmark uses the fixture's actual 24 twelve-position permutations for correctness. Performance workloads use deterministic synthetic numeric payloads of width 12, 64, and 256 so that no chart interpretation or star semantics enter the timing experiment.

## Compared representations

- Index: a 12-entry permutation map. Applying it selects/reorders 12 existing rows.
- Matrix: a dense 12x12 one-hot permutation matrix represented as Python list-of-lists. Applying it uses explicit dense multiplication in pure Python.
- Operations: construction, application, inverse, composition, JSON serialization, retained-memory estimate, and a six-layer batch.

The matrix implementation is intentionally the simple pure-Python representation used for this bounded engineering comparison. These results do not generalize to NumPy/BLAS, sparse matrices, compiled kernels, or other workloads.

## Guardrails

- No production code, canonical temporal registry, PL1 exporter/schema, workflow, Knowledge/Core/Governance, or active KIB lock changes.
- The scope-level mutagen-to-glyph mapping gap remains unresolved and is not interpreted by this benchmark.
- No source-truth, traditional semantic correctness, predictive-validity, or production migration claim.
- Timing values are observational; CI checks correctness and report structure, not fragile wall-clock thresholds.

## Re-run

Run the benchmark from the repository root with:

    python product/experiments/spatiotemporal_matrix_index_v0_1/benchmark.py --write-report

This rewrites BENCHMARK_REPORT_v0.1.json with the current runtime's timing snapshot. Timing values vary by machine and runtime; compare environment and protocol before comparing results.

# Matrix-vs-index benchmark v0.1 — execution evidence

Status: **TEST_ONLY / NOT CANONICAL / NOT PRODUCTION-CONSUMABLE**.

## Pins

- Main base at activation: 0c9210855d874045f577914e8ec27e909438ecf4.
- Source experiment: Product #772 / PR #774, archived unmerged at head a2595cb5e88f854fccd19281e14a7950604ba783.
- Source fixture SHA-256: 05f1dd790faae77ce0caf34af259e0b85c597056f3e18ac207a8e581ee1d2524.
- Source row hashes and producer artifact digest are recorded in fixture_manifest_v0.1.json.
- The fixture is a reduced engine-generated regression projection, not source-transcribed chart truth.

## Measurement snapshot

The committed report uses the declared pure-Python operations and timing protocol in benchmark.py. The snapshot was measured on Python 3.13.5, platform Linux-6.18.55-x86_64-with-glibc2.41; CPU model was not captured. Timings are observational microbenchmarks and are not CI thresholds. Rerunning the script writes a new timing snapshot and may change measured values.

## Correctness coverage

- 24 actual scope permutations from the pinned fixture; 11 unique permutations.
- 72 index/matrix application comparisons across payload widths 12, 64 and 256.
- 24 inverse checks and 24 inverse roundtrip checks.
- 576 pairwise composition checks.
- The benchmark uses synthetic numeric payloads for timing. It does not interpret stars, mutagen values, temporal outcomes or traditional rules.

## Disposition

Keep the index representation as the baseline for the current pure-Python implementation. Dense matrix operations are more expensive in this measured implementation, but optimized numerical libraries, sparse matrices, compiled kernels and production workload performance were not evaluated. No production migration or semantic promotion is authorized.

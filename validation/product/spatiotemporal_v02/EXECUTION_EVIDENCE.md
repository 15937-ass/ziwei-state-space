# Product #768 — natal coordinate probe execution evidence

Work unit: PRODUCT_SPATIOTEMPORAL_NATAL_COORDINATE_PROBE_V0_2

## Scope

This is a TEST_ONLY natal-coordinate encoding experiment. It reads the pinned 11-case materialization artifact and two pinned source contracts. It does not add temporal scopes, change production code, or claim full source-chart equivalence.

## Input pins

- Artifact: Git blob 3778e5f3d66c1e5ab44461360b6d9f71b3f8be56; SHA-256 402e607e7b563f2fe12de7d0c4cc8c5bec11f26bcee7c6b4a6f9c2243b1dfff1.
- Z12 relation contract: Git blob 26e6984b386954e18604f83de038a623365c85b6; SHA-256 a4192ff3c5b3d8be41ead79db2b447cc134fe499859d626b025c94ba77576b1c.
- Branch order source: Git blob e4d0645b42c44fb737ee234960114253af23bd41; SHA-256 eeb8ade67e500e6d795912c05ad6058cce9e375cab790aaeedc1a3c615fe060c.
- Expected case ID source: Git blob 58b6ebdaf5b1e364798cec0361817dbe981d743a; SHA-256 8e9543c8a0d46f9bd0568cfa2497e356b28fb8dc947fe4ebae04d6e8d9b586a0.

## Pre-implementation session audit

A separate in-memory preflight compared the pinned input and declared Z12 contract before the repository probe was written. It observed 11 complete 12-branch maps, 11 unique palace-name sets, 11 reconfirmed target anchors, 132 index/matrix offset matches, 132 inverse checks, 1,584 cyclic composition checks, and 11 input-order invariance checks. This preflight is not a substitute for the committed probe and test suite.

## Repository validation

Status: PENDING exact-head repository-quality gate and applicable Product P1 workflows.

The final evidence record must be reconciled with the exact base/head and workflow run IDs after the implementation PR is opened. Older runs must not be represented as validation of a later commit.

## Claim boundary

The source artifact does not establish full-source-chart equivalence. This experiment does not test temporal layers, traditional cross-layer semantics, runtime performance, or predictive validity. No production effect, canonical acceptance, KIB update or registry activation is authorized.

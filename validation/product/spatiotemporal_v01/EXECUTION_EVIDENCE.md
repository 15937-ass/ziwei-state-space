# Product #764 engineering experiment — execution evidence

Status: isolated TEST_ONLY checkpoint; not canonical semantics or production migration.

## Identity and scope

- Lane/work unit: PRODUCT_ONLY / PRODUCT_SPATIOTEMPORAL_ENGINEERING_PROBE_V0_1.
- Initial base: `74864f572cdd04407c241c483f3a34c646f69d3a`.
- Branch: `product/764-spatiotemporal-probe`.
- Exact implementation head, linked PR and subsequent gate outcomes are recorded in the live Issue #764 / PR and commit-associated CI. A report cannot embed its own resulting commit SHA; use those immutable links to resolve the final validation identity.
- Runtime: Codex local isolated Python venv; GitHub Actions standard public runners for PR checks. No workflow changes or extra billable runner.
- PI authorized pausing #715 / Draft #718 and reusing Product WIP=1 on 2026-10-25. Preserved old head: `d8d65de57f66484652d80fa8b6bfe1ca7c919672`.

## Changed paths

- `product/experiments/spatiotemporal_v01/README.md`
- `product/experiments/spatiotemporal_v01/probe.py`
- `product/experiments/spatiotemporal_v01/fixture_manifest_v0.1.json`
- `product/experiments/spatiotemporal_v01/COMPARISON_REPORT_v0.1.json`
- `product/experiments/spatiotemporal_v01/COMPARISON_REPORT_v0.1.md`
- `tests/test_product_spatiotemporal_probe.py`
- `product/PRODUCT_STATE.yaml`
- `tests/test_product_source_only_vertical_slice_blocker_handoff.py` — mutable recovery assertions only; historical handoff/lock assertions preserved.
- This evidence file.

No Knowledge, Governance, workflow, existing src/product runtime, active KIB lock or production registry changes. Fixture_manifest verifies fixed baseline input hashes and the unchanged production gates.

## Executed focused checks

Command (repository root):

```bash
PYTHONPATH=. /tmp/ziwei-exp-764-env/bin/python -m pytest -q tests/test_product_spatiotemporal_probe.py tests/test_product_source_only_vertical_slice_blocker_handoff.py tests/test_product_temporal_asset_adapter.py
```

Result before publication: **209 passed**, 0 failed, 0.35s; Python 3.12.14, pytest 9.1.1. Includes all 144 combinations and 12 shifts, explicit direction/wraparound anchors, unknown/conflict masking, full three-valued AND/OR/NOT cases, negation completeness, target/snapshot/layer isolation, unchanged fixture, explicit versus scope-only star transformation binding, same-version replay, version rejection and trace tamper detection.

Deterministic artifact generation was executed with the probe CLI; checked-in JSON equals make_report() and pinned input hashes match.

## Required final gate

Full pytest, Product JS syntax, deterministic P0, Product ownership and applicable P1 regression results must be recorded for the final exact head in the live Issue/PR. At this file's preparation these full checks are **PENDING**, not PASS. Do not reuse #715's historical run or this focused result as full acceptance. If main changes, synchronize and perform the protocol's exact-base/head checks again before merging.

## Critic pass / revisions

The current session separately inspected the implementation against the seven design-audit findings. Revisions removed unnecessary matrix construction from the index path, corrected operation-count wording to actual row lookups, rejected empty rules, and added same-policy/code replay checks plus tamper detection. This is a producer/critic pass in one session, not an external or independent human review.

## Findings and limitations

The dense matrix and index views agree for the synthetic cycle. Indexing remains the engineering baseline; no runtime benchmark or production-migration benefit is established. The accepted adapter fixture is a two-slot engineering demo with empty natal, not a complete or independently verified real chart. Three-valued logic and completeness remain TEST_ONLY policy. Cross-layer reaction semantics, temporal intervals, first/persistent triggers, source-rule authoring cost and predictive validity are NOT_EVALUATED. Production registries and source-only vertical-slice gates remain unchanged.

## Recovery

Continue #764's linked PR/checks using live Issue/PR over the cache. #715/#718 stays paused. Core #757 and the palace shard remain independent. On completion stop and present a bounded research recommendation; do not automatically build a unified production engine or activate a new Product task.

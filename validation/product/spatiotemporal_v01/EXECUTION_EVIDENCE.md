# Product #764 engineering experiment — execution evidence

Status: isolated TEST_ONLY checkpoint; not canonical semantics or production migration.

## Identity and scope

- Lane/work unit: PRODUCT_ONLY / PRODUCT_SPATIOTEMPORAL_ENGINEERING_PROBE_V0_1.
- Initial base: `74864f572cdd04407c241c483f3a34c646f69d3a`.
- Branch: `product/764-spatiotemporal-probe`; Draft PR #766.
- Synchronized validation base: `5e3b26d8ad5d49152bf9cc44339f53e9db43d803` after accepted palace work advanced main; no unmerged Knowledge input is consumed.
- Implementation/report head with the completed first-round full validation: `08348cc9a352e1d436d89fc8bfc72a2a806e8c2f`. Main was still at the synchronized base when compared: branch ahead by 2 commits, behind by 0.
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

## Completed full validation on the implementation/report head

The exact code/report head `08348cc9a352e1d436d89fc8bfc72a2a806e8c2f`, against base `5e3b26d8ad5d49152bf9cc44339f53e9db43d803`, passed all five required GitHub Actions checks:

- [Repository quality gate #40159941079](https://github.com/15937-ass/ziwei-state-space/actions/runs/40159941079): **SUCCESS** — 2,920 passed, 0 failed, 132 subtests passed; 404.70s.
- [Product dual-engine P1 #40159941035](https://github.com/15937-ass/ziwei-state-space/actions/runs/40159941035): **SUCCESS**.
- [Product calendar P1 #40159941032](https://github.com/15937-ass/ziwei-state-space/actions/runs/40159941032): **SUCCESS**.
- [Product zi-day P1 #40159941065](https://github.com/15937-ass/ziwei-state-space/actions/runs/40159941065): **SUCCESS**.
- [Product temporal P1 #40159941022](https://github.com/15937-ass/ziwei-state-space/actions/runs/40159941022): **SUCCESS**.

The repository quality gate also passed JavaScript syntax, deterministic P0, and Product path-ownership checks. These results supersede the initial invalidated run; that earlier run is not counted as acceptance evidence.

This evidence-file update itself changes the PR head. Its new head must receive its own applicable checks before the checkpoint is finally disposed of or any integration is considered. The live Issue #764 should record the resulting exact head and run IDs, because a committed evidence file cannot embed its own resulting commit SHA without a circular reference.

## Critic pass / revisions

An initial full run exposed a recovery-cache inconsistency: execution.next_work_unit had advanced but critical_path.now had not. The Product state queue was corrected; governance tests were unchanged. The run was invalidated by that repair and a concurrent accepted-main advance, so no full PASS is claimed from it.

The current session separately inspected the implementation against the seven design-audit findings. Revisions removed unnecessary matrix construction from the index path, corrected operation-count wording to actual row lookups, rejected empty rules, and added same-policy/code replay checks plus tamper detection. This is a producer/critic pass in one session, not an external or independent human review.

## Findings and limitations

The dense matrix and index views agree for the synthetic cycle. Indexing remains the engineering baseline; no runtime benchmark or production-migration benefit is established. The accepted adapter fixture is a two-slot engineering demo with empty natal, not a complete or independently verified real chart. Three-valued logic and completeness remain TEST_ONLY policy. Cross-layer reaction semantics, temporal intervals, first/persistent triggers, source-rule authoring cost and predictive validity are NOT_EVALUATED. Production registries and source-only vertical-slice gates remain unchanged.

## Recovery

Continue #764's linked PR/checks using live Issue/PR over the cache. #715/#718 stays paused. Core #757 and the palace shard remain independent. On completion stop and present a bounded research recommendation; do not automatically build a unified production engine or activate a new Product task.

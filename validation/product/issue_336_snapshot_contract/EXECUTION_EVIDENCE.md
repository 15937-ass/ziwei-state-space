# Issue #336 — Codex recovery and validation evidence

Execution runtime: Codex / OpenAI cloud environment. Python 3.12.14, Node v24.19.0,
pytest 9.1.1, iztro-js 2.6.1, x-iztro 0.6.1. No GitHub Actions run was requested.

Base commit: `fa46e93ffac7a33a8385929cd7a9147327e53f4c`.
Recovered candidate: `d885740af5298f954b509673d7f797672b0c16e6` (PR #339).
The full base Git tree was reconstructed through the authenticated connector and
verified as `3c725ccc1e4d7820eaa0052fc51391084763e41a` before edits. The original
signed base commit object was recovered with its exact SHA. Direct private-repo
cloning was unavailable; no substitute/synthetic base was used.

## Commands and results

Run from repository root, in this order where dependent:

```bash
python -m pip install --upgrade pytest
PYTHONPATH="$PWD" python -m pytest -q
```

Original candidate: 478 passed, 5 failed (missing target-array position in scope
error diagnostics). One autonomous repair updated diagnostics, rejected padded
target IDs that conflict with adapter lookup, and added negative tests.

```bash
PYTHONPATH="$PWD" python -m pytest -q tests/test_product_full_chart_snapshot_contract.py
PYTHONPATH="$PWD" python -m pytest -q
node --check tools/iztro_export.mjs
node --check tools/iztro_full_export.mjs
PYTHONPATH="$PWD" python src/audit_repository.py --fail-on-p0
PYTHONPATH="$PWD" python src/audit_repository.py --fail-on-p0 --output /tmp/ziwei-336/repository_audit.json
```

23 targeted tests passed. Full suite: **486 passed, 0 failed, 0 skipped**.
Both JS syntax checks passed. P0 audit passed; 907 P1 review candidates remain,
not certified semantic errors and not resolved by this Product-only work.

```bash
npm install --no-save iztro@2.6.1
python -m pip install --upgrade "x-iztro==0.6.1"
mkdir -p /tmp/ziwei-336
PYTHONPATH="$PWD" python tools/chart_inputs_to_jsonl.py validation/product_chart_regression/regression_inputs_v0.1.csv /tmp/ziwei-336/p1_inputs.jsonl
IZTRO_VERSION=2.6.1 node tools/iztro_full_export.mjs /tmp/ziwei-336/p1_inputs.jsonl validation/product_chart_regression/temporal_targets_v0.2.json /tmp/ziwei-336/p1_iztro_js.jsonl
python tools/x_iztro_full_export.py /tmp/ziwei-336/p1_inputs.jsonl validation/product_chart_regression/temporal_targets_v0.2.json /tmp/ziwei-336/p1_xiztro_rust.jsonl
PYTHONPATH="$PWD" python tools/p1_compare_full.py /tmp/ziwei-336/p1_iztro_js.jsonl /tmp/ziwei-336/p1_xiztro_rust.jsonl --report /tmp/ziwei-336/p1_dual_engine_report.json --fail-on-diff
PYTHONPATH="$PWD" python validation/product/issue_336_snapshot_contract/validate_exports.py /tmp/ziwei-336/p1_iztro_js.jsonl /tmp/ziwei-336/p1_xiztro_rust.jsonl --report validation/product/issue_336_snapshot_contract/compatibility_report.json
```

Dual-engine comparison PASS: 100 natal records and 400 temporal snapshots,
zero differences. **Real-export input compatibility FAIL**: JS 0/400 passed;
Rust 0/400 passed. Each engine exports `age.palace_names` with 12 entries and
`age.stars=[]`; the validator incorrectly requires equal lengths. The old
adapter iterates the supplied empty array without adding or inferring stars.
This is a compatibility failure, not an engine-disagreement or Ziwei-theory claim.

The initial exploratory compatibility command also failed for the same reason;
`validate_exports.py` is the durable, compact reproducer. The report pins SHA-256
of both generated exports. Synthetic regression exports stay in `/tmp/ziwei-336`;
compact evidence is versioned alongside this document.

PR lane validation (after committing all Product paths):

```bash
python tools/validate_governance.py --base-ref origin/main --head-branch product/336-full-chart-snapshot-contract
```

The PR/Issue comment records the exact validated head SHA and lane result.
Go and B02 calendar/zi-day/temporal engine-change suites are NOT_REQUIRED for
this input-contract-only change: no exporter, chart arithmetic or engine adapter
is modified. Go is not installed; no Go pass is claimed.

## 中文审查结论及恢复边界

**本工作单元尚未通过验收，不得合并。** 单元测试通过不能替代真实导出兼容性。
按照 G7 执行协议一轮自主修复限制，将第二项失败升级记录为 Product 契约审查，
不再自动进行第二轮修复，也不改变测试断言掩盖失败。

建议下一次在同一 Issue/PR 内审查：如何忠实接受现有 exporter 的空流曜数组，
同时继续拒绝缺失字段和畸形的非空数组；随后重跑本兼容性复现及全量门禁。
这属于输入表示问题，不需要 PI 判断常规程序细节，也不构成紫微理论 Human Gate。
候选修复仅保存在 PR；生产主线保持原状。原典、Knowledge 文件、生产时间反应库、
概率和现实预测结论均未变更。当前 Product 恢复指针记录本阻塞；Knowledge 指针
滞后应由 Knowledge lane 在其原工作单元内恢复，本轮不跨 lane 修改。

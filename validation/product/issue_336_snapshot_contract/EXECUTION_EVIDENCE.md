# Issue #336 — Final Codex validation evidence

Execution runtime: Codex / OpenAI cloud environment.
Python 3.12.14, Node v24.19.0, pytest 9.1.1, iztro-js 2.6.1, x-iztro 0.6.1.
Base commit: `fa46e93ffac7a33a8385929cd7a9147327e53f4c`.
Prior blocked checkpoint: `945a58677a115f7a3dd5592d3da3ebd7f80c538c`.
Exact validated head SHA is recorded in the PR/Issue Validation Evidence block.

## 中文验收结论

**#336 输入结构契约通过验收。** 修复了既有导出器 `age.stars=[]` 被误拒绝的问题。
六个 scope 均接受明确的空数组；非空数组仍须逐宫对齐。缺失字段、null、畸形
分组、错位非空数组继续拒绝；不补齐或推算星曜，不变更原典或规则语义。
复核依据为两个固定版本引擎的实际导出、`stableFlowStars` / `normalizeScope`
及既有 `temporal_asset_adapter` 对空数组的直接遍历行为。

验收区分：结构关口通过，不等于原始引擎输出已经能直接完成全部推演。
原始盘的“仆役”别名仍不被下游本命适配器识别；主线与候选对同一原始输入
出现完全相同的 ValueError。该既有局限记录在本 Issue，未在本次扩大范围修复。
规范化测试输入的本命证据与时间限制则与主线完全一致。

## Commands and results

Dependencies were installed in this Codex environment during recovery:

```bash
python -m pip install --upgrade pytest
npm install --no-save iztro@2.6.1
python -m pip install --upgrade "x-iztro==0.6.1"
```

Final verification from repository root:

```bash
PYTHONPATH="$PWD" python -m pytest -q tests/test_product_full_chart_snapshot_contract.py
PYTHONPATH="$PWD" python -m pytest -q
node --check tools/iztro_export.mjs
node --check tools/iztro_full_export.mjs
PYTHONPATH="$PWD" python src/audit_repository.py --fail-on-p0 --output /tmp/ziwei-336/repository_audit.json > /tmp/ziwei-336/repository_audit.stdout
```

Targeted tests: **54 passed, 0 failed, 0 skipped**.
Full suite: **517 passed, 0 failed, 0 skipped**.
Both JS syntax checks PASS. P0 audit PASS; 907 existing P1 review candidates
remain unresolved by this Product-only work and are not certified semantic errors.

```bash
mkdir -p /tmp/ziwei-336
PYTHONPATH="$PWD" python tools/chart_inputs_to_jsonl.py validation/product_chart_regression/regression_inputs_v0.1.csv /tmp/ziwei-336/p1_inputs.jsonl
IZTRO_VERSION=2.6.1 node tools/iztro_full_export.mjs /tmp/ziwei-336/p1_inputs.jsonl validation/product_chart_regression/temporal_targets_v0.2.json /tmp/ziwei-336/p1_iztro_js.jsonl
python tools/x_iztro_full_export.py /tmp/ziwei-336/p1_inputs.jsonl validation/product_chart_regression/temporal_targets_v0.2.json /tmp/ziwei-336/p1_xiztro_rust.jsonl
PYTHONPATH="$PWD" python tools/p1_compare_full.py /tmp/ziwei-336/p1_iztro_js.jsonl /tmp/ziwei-336/p1_xiztro_rust.jsonl --report validation/product/issue_336_snapshot_contract/dual_engine_report.json --fail-on-diff
PYTHONPATH="$PWD" python validation/product/issue_336_snapshot_contract/validate_exports.py /tmp/ziwei-336/p1_iztro_js.jsonl /tmp/ziwei-336/p1_xiztro_rust.jsonl --report validation/product/issue_336_snapshot_contract/compatibility_report.json
```

Dual-engine comparison PASS: 100 natal + 400 temporal snapshots, zero differences.
Real-export structural compatibility PASS: JS 400/400, Rust 400/400. Both engine
export SHA-256 hashes and observed age shapes are in the compatibility report.

Raw snapshot extraction for the service smoke check:

```bash
python - <<'PY'
import json
from pathlib import Path
snapshot = json.loads(next(open('/tmp/ziwei-336/p1_iztro_js.jsonl')))
Path('/tmp/ziwei-336/real_snapshot.json').write_text(json.dumps(snapshot, ensure_ascii=False))
PY
PYTHONPATH="$PWD" python -m src.product.career_inference_cli --snapshot /tmp/ziwei-336/real_snapshot.json --target-id T1_LEAP_LATE_ZI --question '真实引擎输入结构验收' --output /tmp/ziwei-336/real_career_report.json
```

The raw CLI smoke check FAILS on the pre-existing `仆役` alias limitation.
No successful native end-to-end smoke run is claimed. Baseline comparison:

```bash
PYTHONPATH="$PWD" python validation/product/issue_336_snapshot_contract/compare_service_baseline.py --base-ref fa46e93ffac7a33a8385929cd7a9147327e53f4c --raw-snapshot /tmp/ziwei-336/real_snapshot.json --target-id T1_LEAP_LATE_ZI --report validation/product/issue_336_snapshot_contract/service_baseline_comparison.json
```

PASS: eight normalized fixture comparisons are byte-equivalent as serialized
run objects (no rule; 武曲科; 武曲忌; 破军禄; each with normal/empty-age arrays).
All retain `PARTIAL_TEMPORAL_REGISTRY_EMPTY`. Raw snapshot comparison also has
identical baseline/candidate errors; this proves no introduced behavior change,
not native exporter readiness. No input snapshot is repaired by the gate.

After committing the full Product tree:

```bash
python tools/validate_governance.py --base-ref origin/main --head-branch product/336-full-chart-snapshot-contract
```

The PR/Issue records exact head and lane validation results. All five workflows
remain manual-only. No GitHub Actions were run. Go and B02 engine-change suites
are NOT_REQUIRED: no PL1 algorithm, exporter or engine adapter changed. Go is
unavailable; no Go pass is claimed.

## Review and checkpoint

Producer: minimal empty-array compatibility fix and contract clarification.
Critic: confirmed no coercion/mutation, required fields remain required, malformed
non-empty arrays remain rejected across all six scopes, and actual downstream
service limitations are disclosed. No Knowledge-owned path changes, new atoms,
weights, probabilities, production reaction rules or empirical claims.

The prior checkpoint preserved initial failures (478 passed/5 failed; then 486
passed with JS/Rust real-export rejection). This resumed unit explicitly reviewed
that blocker against existing transport behavior and resolved it. Earlier failure
evidence remains in Git/PR history; it is superseded only for this contract check.

Durable reports: `summary.json`, `compatibility_report.json`,
`dual_engine_report.json`, `service_baseline_comparison.json`.
Raw synthetic exports remain under `/tmp/ziwei-336` and are reproducible using
versioned commands; compact reports pin their hashes.

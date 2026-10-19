# Issue #344：事业本命静态四化规则接入验收

Execution runtime: Codex / OpenAI cloud environment (Python 3.12.14, Node v24.19.0, Linux x86_64)
Base commit: b0e055022484447a94c60b74afedee63b88a74c4
Head commit: recorded in GitHub Issue/PR after publishing this tested tree.

## 实质结果与审查

正式 Career provider 从 3 条增至 17 条。新增 14 条仅来自已合并 PR #308 的静态候选；知识映射、源文、CSV 与 ontology 均未修改。旧有三条不变，默认通用 registry 仍为 Wealth-only。生产时间反应库仍为空，结果仍为 PARTIAL。

Producer：显式选择映射条目、复制精确条件/来源/投影到 Product registry；将原有单文件交接扩为互不重叠的显式选择；中文报告按每条规则的对应映射取来源摘要。

Critic：重点检查子午/巳亥门控是否丢失、同一四化下多条投影是否完整、结构约束是否保留、路径/事件式目标是否误激活、来源摘要是否错配。结果：每条新规则遍历 12 宫支及缺少四化/错星/错宫负例，API 与报告精确匹配来源；重复/遗漏选择、条件/目标/位置漂移和越界路径均拒绝。CA02-158、164、194 即使被手动加入选择也因 readiness 而拒绝。未将独立性推成富贵、职业场景推成现实事件。

## Exact commands

Run from repository root (feature branch `product/344-career-static-transform`):

```bash
PYTHONPATH="$PWD" python -m pytest -q tests/test_product_career_natal_domain_provider.py
PYTHONPATH="$PWD" python -m pytest -q tests/test_product_career_static_expansion.py
PYTHONPATH="$PWD" python -m pytest -q
node --check tools/iztro_export.mjs
node --check tools/iztro_full_export.mjs
PYTHONPATH="$PWD" python src/audit_repository.py --fail-on-p0 --output /tmp/issue344-audit.json > /tmp/issue344-audit.stdout
PYTHONPATH="$PWD" python validation/product/issue_344_static_transform/audit_native_inference.py /tmp/ziwei-336/p1_iztro_js.jsonl /tmp/ziwei-336/p1_xiztro_rust.jsonl --report validation/product/issue_344_static_transform/native_inference_report.json
PYTHONPATH="$PWD" python tools/p1_compare_full.py /tmp/ziwei-336/p1_iztro_js.jsonl /tmp/ziwei-336/p1_xiztro_rust.jsonl --report validation/product/issue_344_static_transform/dual_engine_report.json --fail-on-diff
PYTHONPATH="$PWD" python -m src.product.career_inference_cli --snapshot /tmp/ziwei-336/real_snapshot.json --target-id T1_LEAP_LATE_ZI --question '事业本命结构与来源' --output /tmp/issue344-cli.json
python tools/validate_governance.py --base-ref origin/main --head-branch product/344-career-static-transform
```

Results:
- Original provider/API/report suite: 16 passed / 0 failed / 0 skipped.
- New static expansion suite: 21 passed / 0 failed / 0 skipped (parameterized rules exercise all 12 branches internally).
- Full pytest: 550 passed / 0 failed / 0 skipped.
- Node checks: PASS.
- P0 audit: PASS; zero P0; 907 existing P1 atomicity candidates remain.
- Lane governance: PASS.
- Real raw Product API/report: JS 400/400 and Rust 400/400 target runs; all remain PARTIAL_TEMPORAL_REGISTRY_EMPTY, source traced, input unchanged, no event-prediction claim.
- P1 dual-engine: 100 natal + 400 temporal, zero differences.
- Real CLI: PASS, Chinese status and report produced; this particular input activates zero Career rules, a valid uncovered result.

## Regression inputs and limits

Reused unchanged pinned exports from #336/#342, rather than reinstalling engines or regenerating identical exports. Full input SHA256 values and engine source revisions are in native_inference_report.json; exporter reproduction commands are preserved in Issue #336 evidence. Synthetic repository fixtures are not personal cases or empirical outcomes. Cached exports cover a subset of active rules; the new API/source tests exercise every new rule, including branch-gated positives and negatives. Repeated targets share a natal chart and are not independent natal samples.

No PL1 algorithm, exporter, calendar, Zi-day or engine adapter change. Independent Go/B02 regressions NOT_REQUIRED and not claimed; Go is unavailable in this environment. Existing installed dependencies reused. No GitHub Actions executed. Empirical calibration, event prediction and production temporal-rule readiness remain unestablished.

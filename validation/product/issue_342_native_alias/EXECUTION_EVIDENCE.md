# Issue #342 — Native raw-export palace compatibility

Execution runtime: Codex / OpenAI cloud environment.
Base commit: `3ff960a032c82a103624437204e288974085bf2c`.
Python 3.12.14; pytest 9.1.1; Node v24.19.0; iztro-js 2.6.1; x-iztro 0.6.1.
Exact tested head is recorded in the PR/Issue Validation Evidence block.

## 中文完成结论

已在共享本命宫位解析器加入明确的 Product 输入别名，绑定固定版本引擎的
“仆役”到既有 P08。原始名称、输入盘、星曜、干支、四化、知识本体均保持原样。
八百次真实原始输入的事业 API 调用及来源报告验证通过；不再需要先给盘改名。

两个引擎各 100 张本命、400 个目标全部完成，报告仍统一为
`PARTIAL_TEMPORAL_REGISTRY_EMPTY`，无生产时间反应规则、无现实预测主张。
本次回归输入仅实际命中 CA04-349（每引擎八次目标运行）；其他两条规则仍由
已有定向测试覆盖，不能把这批数据说成所有事业规则的真实盘覆盖。

## Commands

Dependencies and raw exports were produced in the same Codex environment using
the existing pinned exporters. Exporters, fixtures and comparison code are not
modified by this Issue. To regenerate the synthetic export inputs:

```bash
python -m pip install --upgrade pytest
npm install --no-save iztro@2.6.1
python -m pip install --upgrade "x-iztro==0.6.1"
mkdir -p /tmp/ziwei-336
PYTHONPATH="$PWD" python tools/chart_inputs_to_jsonl.py validation/product_chart_regression/regression_inputs_v0.1.csv /tmp/ziwei-336/p1_inputs.jsonl
IZTRO_VERSION=2.6.1 node tools/iztro_full_export.mjs /tmp/ziwei-336/p1_inputs.jsonl validation/product_chart_regression/temporal_targets_v0.2.json /tmp/ziwei-336/p1_iztro_js.jsonl
python tools/x_iztro_full_export.py /tmp/ziwei-336/p1_inputs.jsonl validation/product_chart_regression/temporal_targets_v0.2.json /tmp/ziwei-336/p1_xiztro_rust.jsonl
```

Commands actually executed for this work unit (raw exports reused with SHA-256
pinned in `native_inference_report.json`):

```bash
PYTHONPATH="$PWD" python -m pytest -q tests/test_product_palace_structure.py tests/test_product_career_natal_domain_provider.py tests/test_product_career_inference_cli.py
PYTHONPATH="$PWD" python -m pytest -q
node --check tools/iztro_export.mjs
node --check tools/iztro_full_export.mjs
PYTHONPATH="$PWD" python src/audit_repository.py --fail-on-p0 --output /tmp/ziwei-336/alias_repository_audit.json > /tmp/ziwei-336/alias_repository_audit.stdout
PYTHONPATH="$PWD" python tools/p1_compare_full.py /tmp/ziwei-336/p1_iztro_js.jsonl /tmp/ziwei-336/p1_xiztro_rust.jsonl --report validation/product/issue_342_native_alias/dual_engine_report.json --fail-on-diff
PYTHONPATH="$PWD" python validation/product/issue_342_native_alias/audit_native_inference.py /tmp/ziwei-336/p1_iztro_js.jsonl /tmp/ziwei-336/p1_xiztro_rust.jsonl --report validation/product/issue_342_native_alias/native_inference_report.json
PYTHONPATH="$PWD" python -m src.product.career_inference_cli --snapshot /tmp/ziwei-336/real_snapshot.json --target-id T1_LEAP_LATE_ZI --question '真实排盘事业本命与大限流年环境' --output /tmp/ziwei-336/alias_career_report.json
```

`real_snapshot.json` is the unmodified first record from the JS JSONL export;
it was extracted during #336 and reused. It contains only synthetic repository
regression input. A compact CLI report summary is versioned here.

Results:
- full pytest: 529 passed / 0 failed / 0 skipped;
- targeted tests: 41 passed / 0 failed / 0 skipped;
- JS syntax and P0 audit: PASS; 907 existing P1 review candidates remain;
- fixed JS/Rust comparison: 100 natal + 400 temporal, zero differences;
- raw API/report path: JS 400/400, Rust 400/400 PASS;
- canonical-fact equality: 100/100 per engine;
- natal-profile equality against a separately named comparison fixture: 100/100 per engine;
- raw inputs preserved: 100/100 per engine;
- raw CLI smoke: PASS, Chinese report with event prediction disabled.

The audit uses a separate comparison copy with P08 named 交友 to check equality;
it does not pass repaired data as raw input. The actual service/report runs use
unchanged original exporter records and verify sources for every active rule.

Lane validation after committing all Product paths:

```bash
python tools/validate_governance.py --base-ref origin/main --head-branch product/342-native-palace-alias
```

Go and B02 engine-algorithm regressions: NOT_REQUIRED. No chart arithmetic,
exporter or engine adapter changed. Go is not installed; no Go pass is claimed.
GitHub Actions: NOT USED. All workflows remain manual-only.

## Producer / critic review

Producer: exact version-scoped transport mapping at the existing shared resolver,
no Knowledge changes, no raw snapshot rewrite.
Critic: checked unknown labels, unsupported engine/version/adapter tuples, malformed
metadata, ontology conflicts, explicit alias conflicts and duplicate bindings;
positive cases preserve original names and identical runtime facts. Sequential
review completed for R1 / Human Gate NONE.

Pinned metadata is a declared compatibility tuple, not source authentication.
Temporal labels remain raw and are not canonicalized by this change. The empty
production temporal registry and lack of empirical calibration remain explicit.

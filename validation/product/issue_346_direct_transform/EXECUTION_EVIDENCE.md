# Issue #346：六条事业本命四化静态规则

Execution runtime: Codex / OpenAI cloud environment
Environment: Python 3.12.14; Node v24.19.0; Linux x86_64
Base commit: 79ed544c14028bd2445dbe72a684ee643937701d
Head commit/tree: recorded in GitHub Issue/PR after publication (avoids self-reference).

## Product result and critic review

Career provider now executes 23 NATAL rules, adding exactly CA04-327, CA05-469,
CA07-671, CA07-672, CA07-673 and CA08-765 from merged Knowledge PR #315. Existing
17 entries and handoff metadata are byte-for-byte equal as JSON values. No
runtime algorithm was changed; the existing explicit multi-map loader and
report builder are reused. All six conditions bind the named star and its
transformation to P09, with no unsupported extra branch gate or lost source gate.

Producer: add six explicit IDs and their exact canonical condition/projection/
source fields to the Product registry; add their source CSV files; preserve
Chinese source summaries in the actual report.
Critic: test missing and wrong mutagen, wrong star/palace, all twelve branch
positions, exact source summaries/projections/provenance, and manual selection
of blocked timing/path targets. Specifically assert actual report text retains
“不是疾病或伤害事件预测”, “不应直接推为官非诉讼” and “不把表达优势升级为必然职业成功”.

CA05-403 remains BLOCKED_TIMING_TRIGGER_REQUIRES_TEMPORAL_SPEC. CA08-766 remains
BLOCKED_PATH_DEPENDENT_TARGET. No new time, event, numeric probability or outcome
semantics. Knowledge/canonical CSV/ontology files and workflows remain unchanged.
Product state now records PARTIAL Career content and CONTRACT internal validation
instead of the stale BLOCKED/NONE flags, with an explicit 23-rule limitation.

## Exact commands and outcomes

Run from repository root:

```bash
PYTHONPATH="$PWD" python -m pytest -q tests/test_product_career_direct_transform.py tests/test_product_career_natal_domain_provider.py
PYTHONPATH="$PWD" python -m pytest -q
node --check tools/iztro_export.mjs
node --check tools/iztro_full_export.mjs
PYTHONPATH="$PWD" python src/audit_repository.py --fail-on-p0 --output /tmp/issue346-audit.json > /tmp/issue346-audit.stdout
PYTHONPATH="$PWD" python validation/product/issue_346_direct_transform/audit_native_inference.py /tmp/ziwei-336/p1_iztro_js.jsonl /tmp/ziwei-336/p1_xiztro_rust.jsonl --report validation/product/issue_346_direct_transform/native_inference_report.json
PYTHONPATH="$PWD" python tools/p1_compare_full.py /tmp/ziwei-336/p1_iztro_js.jsonl /tmp/ziwei-336/p1_xiztro_rust.jsonl --report validation/product/issue_346_direct_transform/dual_engine_report.json --fail-on-diff
python tools/validate_governance.py --base-ref origin/main --head-branch product/346-career-direct-transform
git diff --check
git diff --exit-code origin/main -- knowledge .github
```

- Targeted: 32 passed / 0 failed / 0 skipped.
- Full pytest: 581 passed / 0 failed / 0 skipped.
- Node checks: PASS.
- P0 audit: PASS, zero P0; 907 existing P1 atomicity review candidates remain.
- Product lane governance and scope/diff checks: PASS.
- Raw JS/Rust actual API/report: 400 target runs each, 800 total; all PARTIAL_TEMPORAL_REGISTRY_EMPTY, source trace integrity PASS, raw snapshots unchanged.
- P1 dual-engine comparison: 100 natal, 400 temporal, zero differences.
- Generated durable reports: native_inference_report.json, dual_engine_report.json in this directory. Full P0 output remains reproducible temporary evidence.

The first targeted invocation had 31 pass / 1 fail because a newly written test
omitted the API's required question keyword. One repair added that required
argument; no runtime change or assertion relaxation. The rerun and full suite
passed as recorded above.

## Inputs, reproduction and limits

Reused unchanged pinned iztro-js 2.6.1 / x-iztro-rust 0.6.1 adapter-0.2 exports
from #336/#342. File SHA256 hashes and source revisions are in the raw API report.
No engine reinstall or export regeneration was needed; original reproduction
commands remain in #336 versioned evidence. These are synthetic repository
regression charts, not personal cases, observations or empirical outcomes.
Cached exports activate only a subset; all six new rules are exercised by the
actual API/report tests. Repeated time targets share their natal input.

No algorithm/exporter/calendar/engine-adapter changes: Go/B02 regressions
NOT_REQUIRED, not executed and not claimed (Go unavailable). No GitHub Actions.
Production temporal reaction registry remains empty and source-based scene
projections are not validated real-world outcomes or career recommendations.

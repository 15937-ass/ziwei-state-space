# Issue #353：三条事业跨宫复合条件

Execution runtime: Codex / OpenAI cloud environment
Environment: Python3.12.14; Node v24.19.0; Linux x86_64
Base commit: bd1e6030f24590507e7ba471bc0de959c753ca6b
Head/tree: recorded in GitHub Issue/PR after publication.

## Producer and critic

Career NATAL execution expands31 ->34. Only CA01-066, CA02-188 and CA03-255
from merged PR #322 are added. Existing31 rule entries and prior mapping handoffs
are unchanged as JSON values. No Knowledge/source CSV/ontology/workflow changes.

Producer: explicitly compile the three reviewed condition trees using existing
PALACE_HAS_STAR, BRANCH_PRESENT and TRANSFORMATION_PRESENT atoms; require exact
reviewed cross-palace status and its MAPPED_EXISTING_ATOMS marker, while retaining
the singular marker for previous handoffs. Actual reports use the matching source
summary, location and precise CROSS_PALACE_CONSTRAINT projection.

Critic: CA01-066 retains both full 子/午 alternatives, each requiring P09紫微 and
P05廉贞化禄. CA02-188 retains P09午天机化禄 and P05太阴化忌 together. CA03-255 retains
P09天机化科, P01天同 and P01巨门化忌. Tests iterate all12 branches, omit each required
star, move it into every other11 palaces, and replace/remove each required mutagen.
No isolated single-palace prerequisite can activate the cross-palace rule.
Status-marker, branch-drop, palace, projection and readiness drift fail closed.
The report retains limitations against guaranteed venture success, inevitable
investment action or inevitable work burden. No additional output is invented.

CA01-023 spouse空劫 is not selected. This unit changes no PALACE_RELATION semantics.
CA01-020/064/065 and other unresolved/complex entries remain unselected. All
Knowledge mappings remain non-executable, separate from this Product rendering.

## Commands

From repository root:

```bash
PYTHONPATH="$PWD" python -m pytest -q tests/test_product_career_cross_palace.py tests/test_product_career_natal_domain_provider.py tests/test_product_career_direct_transform.py
PYTHONPATH="$PWD" python -m pytest -q
node --check tools/iztro_export.mjs
node --check tools/iztro_full_export.mjs
PYTHONPATH="$PWD" python src/audit_repository.py --fail-on-p0 --output /tmp/issue353-audit.json > /tmp/issue353-audit.stdout
PYTHONPATH="$PWD" python validation/product/issue_353_cross_palace/audit_native_inference.py /tmp/ziwei-336/p1_iztro_js.jsonl /tmp/ziwei-336/p1_xiztro_rust.jsonl --report validation/product/issue_353_cross_palace/native_inference_report.json
PYTHONPATH="$PWD" python tools/p1_compare_full.py /tmp/ziwei-336/p1_iztro_js.jsonl /tmp/ziwei-336/p1_xiztro_rust.jsonl --report validation/product/issue_353_cross_palace/dual_engine_report.json --fail-on-diff
python tools/validate_governance.py --base-ref origin/main --head-branch product/353-career-cross-palace
git diff --check
git diff --exit-code origin/main -- knowledge .github
```

Results:
- Targeted45 passed /0 failed /0 skipped.
- Full pytest625 passed /0 failed /0 skipped.
- Node syntax PASS; P0 audit PASS (P0=0, existing907 P1 review candidates remain).
- Product lane governance and scope/diff PASS.
- Raw Product API/report: JS400/400 + Rust400/400 target runs PASS; input unchanged,
  source trace and pinned modality preserved. All runs PARTIAL with empty formal
  temporal reaction registry and real_world_event_prediction_supported=false.
- Dual-engine comparison100 natal/400 temporal, zero differences.
- Durable reports: native_inference_report.json, dual_engine_report.json.

## Boundaries / skipped scopes

Pinned raw iztro-js2.6.1 and x-iztro-rust0.6.1 adapter0.2 exports from #336/#342
are reused unchanged. The report pins SHA256 and engine source revisions; original
export-generation commands remain in #336 evidence. No dependency reinstall or
export regeneration. Raw synthetic regression charts cover a subset of rule
activations; each new rule is individually exercised in the API/report tests.
Injected star fixtures establish conditional behavior and source traces, not
physical chart reachability from a birth input. Repeated targets are not independent
natal samples. No personal cases or empirical outcome observations are used.

No calendar/Zi-day/PL1 algorithm/exporter/engine-adapter change. Go/B02 regression
NOT_REQUIRED and not claimed (Go unavailable). No GitHub Actions. No causal,
probability, investment-advice or real-world-event inference. Temporal registry
remains empty; internal validation does not establish predictive accuracy.

# Issue #350：八条星曜存在规则及来源限定语

Execution runtime: Codex / OpenAI cloud environment
Environment: Python 3.12.14; Node v24.19.0; Linux x86_64
Base commit: 9fc487192c1e46ffe58144610559e5c73bfb14a2
Head commit/tree: recorded in GitHub Issue/PR after publication.

## Product result and critic review

Career NATAL execution expands from 23 to 31 entries. Exactly CA01-026,027,031,
032,033,034,042,044 are selected from merged Knowledge PR #335. The prior23 rule
entries and handoff metadata are unchanged as JSON values; no Knowledge-owned
artifact, canonical source row, ontology, workflow or engine adapter is edited.

Producer: explicit eight-rule Product registry; recognize the reviewed
star-presence mapping status in addition to the existing transformation status;
pin nonempty source_modality_note and expose it verbatim in actual Chinese reports.

Critic: all required stars must be in P09; missing stars or stars in any of the
other11 palaces cannot complete the conjunction. API/report tests traverse all12
branches. Same-condition projections remain distinct. 禄存 does not alone trigger
the three-star rule. Empty chart matches none of these rules. Arbitrary status,
source-status drift, missing/empty/changed modality, condition drift and blocked
readiness all fail closed. Report fields for prior transformation entries remain
unchanged. No generic star valence or weight is introduced.

CA01-035,043,045 remain unselected. Active Knowledge context work #347 is a separate
lane, not authority for automatic Product activation. “往往”“有时亦主”“一般只宜”
and the warning against wealth inference remain source qualifications, never
converted into probabilities or deterministic outcomes. Each source mapping
remains non-executable; Product implements only its explicitly selected rendering.

## Exact commands

From repository root:

```bash
PYTHONPATH="$PWD" python -m pytest -q tests/test_product_career_star_presence.py tests/test_product_career_natal_domain_provider.py tests/test_product_career_direct_transform.py
PYTHONPATH="$PWD" python -m pytest -q
node --check tools/iztro_export.mjs
node --check tools/iztro_full_export.mjs
PYTHONPATH="$PWD" python src/audit_repository.py --fail-on-p0 --output /tmp/issue350-audit.json > /tmp/issue350-audit.stdout
PYTHONPATH="$PWD" python validation/product/issue_350_star_presence/audit_native_inference.py /tmp/ziwei-336/p1_iztro_js.jsonl /tmp/ziwei-336/p1_xiztro_rust.jsonl --report validation/product/issue_350_star_presence/native_inference_report.json
PYTHONPATH="$PWD" python tools/p1_compare_full.py /tmp/ziwei-336/p1_iztro_js.jsonl /tmp/ziwei-336/p1_xiztro_rust.jsonl --report validation/product/issue_350_star_presence/dual_engine_report.json --fail-on-diff
python tools/validate_governance.py --base-ref origin/main --head-branch product/350-career-star-presence
git diff --check
git diff --exit-code origin/main -- knowledge .github
```

Results:
- Targeted: 56 passed / 0 failed / 0 skipped.
- Full pytest: 605 passed / 0 failed / 0 skipped.
- Node syntax: PASS.
- P0 audit: PASS; zero P0, existing907 P1 review candidates remain.
- Product lane governance and diff/scope checks: PASS.
- Raw Product API/report: JS400/400 and Rust400/400 target runs, all source-traced,
  all input preserved; modality text is checked against pinned Product metadata
  when a star-presence rule activates. All results remain PARTIAL with empty
  production temporal reaction registry and no real-world-event claim.
- Dual-engine:100 natal/400 temporal; zero differences.
- Reports: native_inference_report.json and dual_engine_report.json in this folder.

## Validation limits

Unchanged pinned raw exports from #336/#342 were reused (iztro-js2.6.1,
x-iztro-rust0.6.1, adapter0.2). Report records exact input SHA256 and engine source
revisions. Original generation commands remain in #336 evidence; dependencies
were not reinstalled and unchanged exporters were not regenerated. Cached raw
charts activate a subset; actual API tests individually exercise all eight new
rules and conjunction failures. Repeated targets are not independent natal charts.
Fixtures are synthetic, not personal cases or empirical observations.

No PL1/calendar/Zi-day/engine algorithm change. Go/B02 regression NOT_REQUIRED and
not claimed; Go unavailable. No GitHub Actions. Source fidelity and condition
matching do not establish real-world predictive validity. Temporal production
registry remains empty, and source modality is not a calibrated probability.

## Latest-main integration

Knowledge PR #349 merged concurrently as main
`4015d6aed98f8b9f01e4b2aca6a16b23f8166123`. Its five files were retrieved and
verified by exact Git blob SHA, and its signed commit/base tree restored locally.
It completes #347 context recovery with three non-executable entries; these are
not activated by this Product unit. Existing star-presence source inputs and all
Product execution code remained unchanged during integration.

Repeated on the integrated tree:

```bash
PYTHONPATH="$PWD" python -m pytest -q
python tools/validate_governance.py --base-ref origin/main --head-branch product/350-career-star-presence
git diff --exit-code origin/main -- knowledge .github validation/knowledge
```

Final results: 612 passed / 0 failed / 0 skipped; Product governance PASS;
no Knowledge/workflow diff relative to latest main. The 605-test result above
records the original base; 612 includes the seven newly merged Knowledge tests.
Exact final head and tested tree are recorded in the Issue/PR.

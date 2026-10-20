# Issue #363：紫微／丑未紫破八条候选接入（BLOCKED）

Execution runtime: Codex / OpenAI cloud environment
Current base:dc62f6d694aa178a9ebf4f7094e1abb7d5afcd23
Original implementation base:64158b2f253e2ac5a709cdee5f44c33cd8954e56
Head/tree: recorded in draft PR/Issue after publication.
Environment: Python3.12.14; pytest9.1.1; Node v24.19.0; x-iztro0.6.1; iztro2.6.1.

## Status / counts

Implementation complete for exactly8 new rules:CA01-047,050,083,087,088,089,093,095.
Candidate registry compiles43; main accepted count remains35. No new rule is
accepted until the full-suite gate passes. Dependency #364 belongs to Knowledge
and was linked to #362. Knowledge #362 completed through PR #366 without resolving
#364, so the Product candidate was synchronized onto that new main and revalidated.
Product PR remains draft.

Current full pytest on main dc62f6d: **826 passed /1 failed /0 skipped**. Failure:
`tests/test_knowledge_career_ziwei_zipo_static_8.py::test_inherited_and_unconditional_within_paragraph_scopes_are_distinct`.
Its final historical assertion requires none of the8 IDs in the Product registry,
which conflicts with explicit Product integration. Knowledge non-executable flags
remain false. Correcting that Knowledge-owned assertion is required; Product does
not edit Knowledge tests, remove/skip assertions or merge with a failed gate.
AGENT_WORKFLOW lane rules and PATH_OWNERSHIP assign that file to Knowledge.
No PI theory decision is required by this engineering dependency.

## Producer / critic

Add the full8-entry mapping handoff and exact conditions/projections/provenance.
Existing35 rule entries and prior handoff metadata remain unchanged as JSON values.
Paragraph context is pinned and validated via PARAGRAPH_SCOPE_V0_1. Existing
spouse context retains its strict BRANCH_GATE_V0_1 fields; unknown schemas reject.
Reports preserve original source summaries and complete source contexts.

Critic tests all12 branches, each required star missing/in any other11 palaces,
wrong/missing mutagen, wrong transformation carrier, paragraph inheritance, exact
context, and invalid context/schema/condition drift.088 retains破军化禄;093 does not
inherit an extra化禄 condition;095 requires both auxiliaries in P09. Leadership,
self-employment, real return and deterministic outcomes are not inferred.

## Commands and observed results

Run from repository root:

```bash
python -m pip install 'x-iztro==0.6.1'
PYTHONPATH="$PWD" python tools/chart_inputs_to_jsonl.py validation/product_chart_regression/regression_inputs_v0.1.csv /tmp/ziwei-363/p1_inputs.jsonl
IZTRO_VERSION=2.6.1 node tools/iztro_full_export.mjs /tmp/ziwei-363/p1_inputs.jsonl validation/product_chart_regression/temporal_targets_v0.2.json /tmp/ziwei-363/p1_iztro_js.jsonl
python tools/x_iztro_full_export.py /tmp/ziwei-363/p1_inputs.jsonl validation/product_chart_regression/temporal_targets_v0.2.json /tmp/ziwei-363/p1_xiztro_rust.jsonl
PYTHONPATH="$PWD" python -m pytest -q tests/test_product_career_natal_domain_provider.py tests/test_product_career_spouse_kongjie.py tests/test_product_career_mapping_readiness.py
PYTHONPATH="$PWD" python -m pytest -q tests/test_product_career_ziwei_zipo.py
PYTHONPATH="$PWD" python validation/product/issue_359_mapping_readiness/audit_mapping_readiness.py --report validation/product/issue_363_ziwei_zipo/readiness_report.json
PYTHONPATH="$PWD" python -m pytest -q
node --check tools/iztro_export.mjs
node --check tools/iztro_full_export.mjs
PYTHONPATH="$PWD" python src/audit_repository.py --fail-on-p0 --output /tmp/issue363-audit.json > /tmp/issue363-audit.stdout
PYTHONPATH="$PWD" python validation/product/issue_363_ziwei_zipo/audit_native_inference.py /tmp/ziwei-363/p1_iztro_js.jsonl /tmp/ziwei-363/p1_xiztro_rust.jsonl --report validation/product/issue_363_ziwei_zipo/native_inference_report.json
PYTHONPATH="$PWD" python tools/p1_compare_full.py /tmp/ziwei-363/p1_iztro_js.jsonl /tmp/ziwei-363/p1_xiztro_rust.jsonl --report validation/product/issue_363_ziwei_zipo/dual_engine_report.json --fail-on-diff
python tools/validate_governance.py --base-ref origin/main --head-branch product/363-ziwei-zipo-static
git diff --check
git diff --exit-code origin/main -- knowledge .github
```

- New API/context suite:23 passed/0 failed/0 skipped.
- Legacy provider/spouse/readiness suite:37 passed/0 failed/0 skipped.
- Original-base full suite:703 passed/1 failed/0 skipped, dependency above.
- Latest-main full suite after Knowledge #366:826 passed/1 failed/0 skipped. The
  additional123 passing tests cover the new100-row Knowledge batch; the only
  failure remains the exact same #364 assertion. No narrowed replacement gate is
  claimed.
- Latest-main Product targeted suite:60 passed/0 failed/0 skipped (23 new API/
  context tests plus37 legacy provider/spouse/readiness tests).
- P0 audit PASS (P0=0, existing907 P1 candidates); Node syntax PASS; Product
  governance and scope/diff PASS.
- Fresh raw API/report: JS400/400 + Rust400/400 target runs PASS, preserved input,
  source context/modality and PARTIAL empty-temporal status; no event claim.
- Fresh dual-engine comparison100 natal/400 temporal, zero differences.
- Candidate readiness52 records:43 compiled,9 blocked,0 unselected. Historical
  #359 report retained; this candidate report does not mean main has43 rules.
- Reports:native_inference_report.json,dual_engine_report.json,readiness_report.json,
  CONTENT_CAPABILITY_REVIEW.md. The content review explains what the eight rules
  add to user-facing Career interpretation and records a non-activating preview
  of the twenty complete mappings merged by Knowledge #366.

The previous temporary exports were absent after cleanup. JS dependency remained
2.6.1; Rust package was absent, so the first Rust export failed to import.
Installed the exact0.6.1 wheel and reran Rust export successfully. This is an
infrastructure repair, separate from the unresolved full-test failure.

No Go/B02 algorithm regression required: no PL1/calendar/adapter/engine algorithm
change; Go unavailable. No GitHub Actions. Fixtures are synthetic; repeated
targets share natal inputs. Raw fixtures cover some new IDs (047/050/083/093);
all8 have synthetic API positives/negatives, which do not establish physical
reachability or empirical prediction validity. Production temporal registry empty.

## Resume

After #364 lands: retain all source/runtime tests; repeat full pytest and required
validation; update current Product readiness and
accepted43 count; mark PR ready only after passing; then merge and close #363.


## G8 revalidation checkpoint

After Knowledge dependency #364 merged and Governance G8 enabled public-repository PR validation, this Product branch must be revalidated against the current main through the automatic repository quality gate and Product P1 workflows before merge. The prior Work/Codex evidence remains historical; the new GitHub Actions run references will be recorded on PR #365 after completion.

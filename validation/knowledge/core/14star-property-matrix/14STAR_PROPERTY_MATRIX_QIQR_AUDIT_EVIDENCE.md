# Issue #712 — 14-star property matrix execution evidence

- Status: `PROPOSAL_ONLY_NOT_CANONICAL`
- Work unit: `KB-CORE-14STAR-PROPERTY-MATRIX-QIQR-AUDIT-01`
- Activation main: `bdcbf24ef85959d7a7b35014e82708bbedb329bf`
- Source corpus: `knowledge/rules/stars/major_stars_canonical_v0.1.csv`
- Source corpus blob: `df9645ab1a8c08411821b8701af85d86bfdaa277`
- Source index blob: `93bebaf4e167547769f3892abef649d323628363`
- QI/QR ontology blob: `e92f0e9492406c4d758b9bd1574bf446b1fa81fd`
- Star cores blob: `0081d4492b070d1785b0dae233d0dc12d6134bff`
- Star systems blob: `571e67987b6139a7fac05b44c1f10c9e2370ff30`
- System index blob: `ff908718fde7a1fd8c7ec8f224c06f95ff11929e`

## Deterministic census

- Rows: 430
- Unique rule IDs: 430
- Major stars covered: 14
- Source ID counts: {"SRC-ZZ-002":413,"SRC-ZZ-001":17}
- QI/QR evidence-link rows: 129
- No explicit QI/QR evidence-link rows: 283
- Multiple candidate-target rows: 15
- Rows flagged for overlap/layer/normalization review: 149
- Current star-system index: 60 systems
- Star-core empty intrinsic signature: 紫微

## Epistemic boundaries

- Source epistemic values are preserved as recorded in the accepted corpus.
- Normalization epistemic values are preserved as recorded; no UNRESOLVED value is promoted.
- Source location/evidence_text are preserved; this run does not claim to have re-OCRed or reverified every PDF page.
- Case-support-only is not a dedicated column in the source CSV; absence of source_case_ids is not treated as proof that a rule is not case-only.
- No canonical ontology IDs, new primitives, mappings, Product consumption, probabilities, or empirical-validity claims are authorized.
- Held-out reconstruction was not performed because existing QI/QR/star-core evidence references were fitted using this same corpus; a valid holdout requires blinded re-adjudication.

## Validation

### Implementation-head validation completed

- Validated implementation head: `f060ca66f43bf0e4fab4e7ead282189b76cbcab1`
- GitHub Actions run: https://github.com/15937-ass/ziwei-state-space/actions/runs/39964562997
- Overall result: **PASS**
- Full pytest suite: **2,645 passed in 216.57s**
- Product JS adapter syntax check: **PASS**
- Deterministic P0 repository gate (`python src/audit_repository.py --fail-on-p0`): **PASS**
- Repository Governance v1 (`python tools/validate_governance.py --base-ref origin/main --head-branch knowledge/core-712-14star-property-matrix`): **PASS**
- Workflow job: `test-and-audit`, completed successfully.

This validation run covers the implementation/report/test changes at the stated head. This evidence-file update is documentation-only and will produce a new PR head; the resulting exact-head CI run must also pass. Its final head SHA and run URL will be recorded in the PR review summary rather than creating a cycle of commits that each rewrite this evidence file. No gate is described as passing for a head that has not actually completed the workflow.
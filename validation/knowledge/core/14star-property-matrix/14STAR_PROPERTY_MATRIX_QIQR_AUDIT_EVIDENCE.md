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

Pending exact final PR head. Required: changed-unit pytest, full repository quality gate, Product JS adapter check, deterministic P0 audit, and Repository Governance v1. The final head SHA, run URL, pytest count, and each gate result must be appended after the workflow completes; do not report pending checks as passed.
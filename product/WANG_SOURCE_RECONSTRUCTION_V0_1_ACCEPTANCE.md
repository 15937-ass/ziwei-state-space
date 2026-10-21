# Wang Source-Input Reconstruction v0.1 — Acceptance

Tracking: Product #545

## Source review acceptance

- source cases reviewed: 24 / 24
- source-usable birth signatures: 22 / 24
- hard source blockers: 2 / 24
- exact singleton inputs: 12
- explicit day-alternative rows: 7
- unqualified 子时 rows: 3
- bounded candidate inputs: 37
- OCR guesses: 0
- biography backfills: 0
- subject-identity fields in blind reconstruction census: 0

## Reconstruction contract acceptance

The probe must:

1. use lunar input directly;
2. use the pinned Zhongzhou Product configuration;
3. enumerate only source-bounded day/time candidates;
4. compare only against `BLIND_EVIDENCE_V0_1` target-palace anchors;
5. support direct and explicit opposite-borrowed major-star anchors;
6. preserve engine errors rather than dropping them;
7. distinguish unique/multiple/no match;
8. never promote blocked or ambiguous source input to a full-chart claim.

## Full-chart promotion rule

```text
UNIQUE_ANCHOR_MATCH
-> eligible for later source-input-reconstructed full-chart materialization

anything else
-> not materialization-ready
```

This is an evidence-readiness gate, not a Ziwei accuracy metric.

## Method boundary

Product #545 does not change:

- Wang MethodPattern source scopes;
- source MethodPattern maturity;
- canonical Ziwei truth;
- empirical probability;
- method-fidelity status;
- predictive-validity status.

Final per-case reconstruction results are recorded only after the pinned engine
probe passes on the PR head.

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


## Observed pinned-engine result

The PR-head probe completed successfully under `product-p1-dual-engine`
(run 603; probe step conclusion = success).

Observed census:

```text
UNIQUE_ANCHOR_MATCH         11
MULTIPLE_ANCHOR_MATCH        6
NO_ANCHOR_MATCH              5
BLOCKED_SOURCE_INCOMPLETE    2
ENGINE_UNSUPPORTED           0
--------------------------------
TOTAL                       24
```

The eleven unique target-anchor matches are:

```text
001 003 006 009 010 012 013 015 019 021 023
```

The six source-bounded ambiguous rows are:

```text
002 008 014 018 020 022
```

The five source-usable rows that do not reproduce the independent target anchor
under the pinned engine are:

```text
005 007 011 017 024
```

Cases 004 and 016 remain blocked by source-input incompleteness.

This result is intentionally **not** upgraded to "11 charts verified against the
entire source chart." The independent anchor currently checks target-palace
identity plus its fourteen-major-star system only. The correct next maturity is:

```text
11 cases -> eligible for SOURCE_INPUT_RECONSTRUCTED_TARGET_ANCHOR_VERIFIED
13 cases -> remain withheld
```

No Human Gate is triggered by the six multiple matches because this work does
not need to choose among them. Choosing one without a stronger source anchor
would be precisely the behavior the gate is designed to prevent.

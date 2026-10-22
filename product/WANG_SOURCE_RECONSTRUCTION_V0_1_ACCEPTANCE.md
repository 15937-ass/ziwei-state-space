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

1. use `astro.byLunar` with the pinned `iztro-js 2.6.1` package;
2. set the Zhongzhou and time-boundary defaults explicitly before chart creation;
3. enumerate only source-bounded day/time candidates;
4. compare source-reviewed target-palace identity as well as its major-star anchor;
5. support direct and explicit opposite-borrowed major-star anchors;
6. preserve every candidate-level engine error in the per-case `engine_errors` list;
7. if any candidate errors, classify the entire case as `ENGINE_UNSUPPORTED`, even if another candidate matches;
8. distinguish unique/multiple/no match;
9. never promote blocked, ambiguous, partially evaluated, or engine-unsupported input to a full-chart claim.

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

The pinned-engine probe completed successfully on implementation commit
`096f82b13a635a19543105d88446b2dded44939d` under `product-p1-dual-engine`
([run 612](https://github.com/15937-ass/ziwei-state-space/actions/runs/39695779056);
probe step conclusion = success).

The final governance-cleanup commit restores the workflow file to the current
main version and updates this evidence pointer only; it does not change the
tested probe, source inputs, blind anchor, or reconstruction implementation.

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

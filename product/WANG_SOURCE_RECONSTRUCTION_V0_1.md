# Wang 24-case Source-Input Reconstruction v0.1

Status: IMPLEMENTED CANDIDATE — Product #545

## Why this work exists

The Wang 24-case benchmark already has a source-reviewed target-palace anchor for
all 24 cases, but the full charts are not materialized. The source pages contain
lunar birth signatures that can potentially reproduce the charts
deterministically.

Those signatures are not uniformly clean. The source itself contains:

- exact dates/times;
- explicit alternative days such as `10(11)`;
- ordinary `子时`, which does not distinguish early/late 子 for the Product
  time-index contract;
- a chart whose day is printed as `X`;
- a page-broken chart whose center birth signature is incomplete.

The Product must preserve those conditions instead of silently replacing them
with a single guessed birthday.

## Source-input census

```text
24 total cases
22 source-usable cases
  12 exact singleton inputs
   7 explicit day-alternative cases
   3 子时 ambiguity cases
 2 source-blocked cases
37 bounded candidate inputs
```

The seven explicit day-alternative rows are preserved as written:

```text
WANG-CASE-002  10(11)
WANG-CASE-008   8(9)
WANG-CASE-014   4(12)
WANG-CASE-018   2(12,15,21)
WANG-CASE-020   4(7,13)
WANG-CASE-022  10(20,23,29)
WANG-CASE-024  10(11)
```

The three unqualified 子时 rows expand only to Product time indices `0` and
`12`. This is a bounded ambiguity set, not an inferred correction.

## Hard blockers

Two cases are deliberately not reconstructable from source input in v0.1:

- `WANG-CASE-004`: lunar day is printed as `X`;
- `WANG-CASE-016`: the chart crosses a page break and the central birth
  signature is incomplete.

No external biography, historical birth database, OCR guess, or reverse solving
from the chart is permitted to fill these fields.

## Reconstruction probe

The probe uses the same Product chart family:

```text
engine           iztro-js 2.6.1
calendar input   lunar
algorithm        zhongzhou
astro type       heaven
fix_leap         true
day_divide       forward
year_divide      normal
horoscope_divide normal
```

Every source-bounded input candidate is reconstructed independently.

The output chart is then checked against the already source-reviewed blind
anchor:

1. target palace identity/domain;
2. direct fourteen-major-star system;
3. for an empty-main-star target, the opposite-palace major-star system that
   the source explicitly borrows.

The probe does not compare expert conclusions or outcomes.

## Readiness classes

```text
UNIQUE_ANCHOR_MATCH
MULTIPLE_ANCHOR_MATCH
NO_ANCHOR_MATCH
BLOCKED_SOURCE_INCOMPLETE
ENGINE_UNSUPPORTED
```

Only `UNIQUE_ANCHOR_MATCH` is eligible for a later full-chart materialization
artifact.

A multiple match remains ambiguous even when every surviving candidate produces
the same target-palace anchor. Target-palace agreement alone is not enough to
choose one birth input.

## Leakage boundary

The reconstruction input artifact contains no:

- source subject label;
- person-group identity;
- expert reasoning graph;
- expert conclusion;
- outcome;
- external biography.

This keeps full-chart reconstruction logically upstream of expert replay.

## What this does not solve

This work resolves only the evidence-materialization side of the Wang benchmark.

It does not broaden the six accepted MethodPattern target scopes. Even after
full-chart reconstruction, method replay may remain blocked when the source
method corpus does not explicitly authorize a procedural rule for the held-out
case target domain.

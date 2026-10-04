# HG-P07-TEMPORAL-01 — Migration Palace Event-Relative Time Window

Status: **HUMAN GATE — APPROVAL REQUIRED BEFORE P07 EXTRACTION**

## Source trigger
SRC-ZZ-003, Migration Palace opening methodology, printed p109, explicitly distinguishes:
- long-period migration: inspect decade/year Migration Palace;
- travel: month-level Migration Palace can be used;
- after moving to a distant place for settlement, **the first three years** should give greater interpretive weight to the Migration Palace, while the ordinary annual Life-Palace-based rotation remains relevant for the other palace domains;
- natal Migration Palace is the underlying nature; decade/year Migration Palace is a reaction to that nature.

## Why this is a Human Gate
The “first three years after relocation” rule is not merely another calendar YEAR rule. Its clock starts from a **relocation event**, not from birth, a decade boundary, or a standard annual transition.

Faithful execution therefore requires an event-relative elapsed-time state such as:
`years_since_distant_relocation`

with an explicit finite window:
`1 <= years_since_distant_relocation <= 3`

This is a second temporal reference frame relative to the current natal/decade/year/month stack, matching the project's Human-Gate criterion for an independent time scale.

## Options

### A — Source-faithful finite relocation window (recommended)
Add a narrowly scoped temporal state:
- event: confirmed distant relocation / settlement;
- relative clock: years since that event;
- finite gate: first 3 years only;
- effect: Migration Palace receives primary interpretive weight for overall trend during that window;
- other palace rotation continues from the ordinary annual Life Palace as the source states.

Constraints:
- no decay curve;
- no inferred weighting coefficient;
- no generic “event timer” behavior beyond this source-supported use;
- no extension beyond 3 years;
- trigger requires a relocation event, not mere travel.

### B — Qualitative-only constraint
Store “early post-relocation period emphasizes Migration Palace” without executable three-year timing.

This avoids a new time reference but loses an explicit source fact and is therefore less faithful.

### C — Treat as ordinary YEAR rules
Duplicate the rule into annual layers without tracking years-since-relocation.

This is not recommended: it cannot distinguish year 1–3 after relocation from unrelated calendar years and breaks the source semantics.

## Recommendation
Approve **Option A** as a minimal, source-bounded extension of the temporal resolver.

This approval would authorize a finite event-relative relocation window only. It would **not** authorize arbitrary persistence durations, decay functions, learned temporal weights, or generalized event-relative clocks elsewhere without new source support / later review.

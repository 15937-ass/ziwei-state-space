# EVENT_RELATIVE_TIME_SCHEMA v0.1

Status: **APPROVED — HG-P07-TEMPORAL-01 OPTION A**

## Scope

This schema implements exactly one source-supported event-relative time window:

`MIGRATION_FIRST_THREE_YEARS`

Source: `SRC-ZZ-003`, Migration Palace opening methodology, printed p109.

It does **not** introduce a general event-timer framework.

## Source semantics

For distant relocation / settlement:
- long-period migration is otherwise read through decade/year Migration Palace;
- travel can be read through month-level Migration Palace;
- during the first three years after a confirmed distant relocation/settlement, the Migration Palace receives primary interpretive priority for the overall relocation trend;
- ordinary annual Life-Palace rotation remains in force for the other palace domains;
- natal Migration Palace remains the baseline nature; temporal Migration Palace is a reaction to that nature.

## Executable state

The resolver accepts only:

```text
confirmed_distant_settlement: bool
years_since_distant_relocation: int | null
travel_only: bool
```

The relative clock is externally supplied. v0.1 does not infer it from dates, addresses, travel history, or chart data.

Activation condition:

```text
confirmed_distant_settlement == true
AND travel_only == false
AND 1 <= years_since_distant_relocation <= 3
```

When active:

```text
migration_palace_priority = PRIMARY
annual_life_palace_rotation = PRESERVED
other_palace_rotation = PRESERVED
```

`PRIMARY` is an ordinal routing label, not a numeric weight.

## Hard constraints

v0.1 MUST NOT:
- infer a relocation event from a travel signal;
- infer elapsed years from calendar dates;
- extend the window beyond year 3;
- create a decay curve;
- create a numeric priority coefficient;
- rewrite natal essence;
- suspend the ordinary annual Life-Palace rotation for other palace domains;
- generalize this rule to arbitrary events without a new source review / Human Gate.

## Machine-readable facts

The resolver may expose:

- `event:distant_relocation_settlement:confirmed`
- `event_relative:distant_relocation_year:<1|2|3|...>`
- `gate:migration_first_three_years:active`
- `projection_priority:migration_palace:primary`
- `rotation:annual_life_palace:preserved`

These facts are deterministic routing facts only.

## Relationship to A2-R1 history

This is **not** an `ACQUIRED_DISPOSITION` or `PATH_DEPENDENT_GATE` memory item.

The source gives an explicit finite event-relative observation window rather than a persistent acquired state. It therefore lives in temporal context, not in the frozen 43-row executable history table.

## Approval

Approved by PI at `HG-P07-TEMPORAL-01`, Option A.

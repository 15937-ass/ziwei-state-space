# PL3-R Career Condition Evaluator + Effect Binding Pilot v0.1

Status: **IMPLEMENTED / VALIDATION PENDING**  
Tracking Issue: #526

## 1. Purpose

Product #521 compiled twelve source-reviewed Career condition IR records into typed Product plans. This work adds the next bounded step:

```text
typed Product condition plan
        ↓
deterministic NATAL chart evaluation
        ↓
source-reviewed projection descriptor binding
        ↓
STOP
```

It does **not** yet execute a dynamic response or generate ResponseProfile τ.

## 2. Exact scope

The evaluator consumes exactly the twelve condition plans from:

```text
product/CAREER_CONDITION_COMPILER_PILOT_v0.1.json
```

and evaluates them only in the canonical Career palace:

```text
P09 = 事业宫
time layer = NATAL
```

The chart input is a normalized deterministic natal snapshot resolved through the existing palace ontology.

No free-form source text participates in condition truth.

## 3. Supported condition semantics

The pilot supports only vocabulary already present in the twelve compiled plans:

```text
STAR
TRANSFORM
PALACE_BRANCH
STAR_SYSTEM (only 天机巨门 / 天同巨门 in this bounded input)

SAME_PALACE
FOUR_DIRECTIONS_VISIBILITY [0,4,6,8]

PAIR_REQUIRED
ANY_SOURCE_LOCAL
BOTH_SOURCE_LITERAL
BOTH_SOURCE_LOCAL

LOCAL_OR:
  TRANSFORM(...)
  ATOM(...)
```

Unknown star-system identifiers or unsupported relation geometry fail closed.

The two STAR_SYSTEM identifiers are decomposed only as Product transport facts:

```text
天机巨门 -> 天机 + 巨门
天同巨门 -> 天同 + 巨门
```

This is not a generic star-system parser and does not add new Zhongzhou semantics.

## 4. Relation evaluation

### SAME_PALACE

Subject and target evidence must both occur in P09.

### FOUR_DIRECTIONS_VISIBILITY

The evaluator uses the existing deterministic palace ontology for P09's:

```text
self + two triad palaces + opposite palace
```

and preserves the compiled scope exactly. It does not narrow “见” to same-palace only.

For BOTH-source requirements, both named members must be found somewhere inside the allowed four-direction scope.

## 5. Dependency rows

The three dependency conditions remain exact parent references:

```text
CA05-420 -> CA05-419
CA07-639 -> CA07-638
CA07-682 -> CA07-681
```

A child receives the parent's condition truth only. It does not copy the parent's projection target.

Therefore the parent and child may both be true while retaining different source-reviewed projection descriptors.

## 6. Semantic effect binding

The versioned registry is:

```text
product/CAREER_CONDITION_EFFECT_BINDING_PILOT_v0.1.json
```

For each of the twelve rows it binds:

```text
source_rule_id
condition_id
time_layer
projection_domain
projection_target
source_location
source_span_ids
compatibility_band
```

from the active Product K_response compatibility corpus.

The binding is explicitly:

```text
effect_kind    = SOURCE_PROJECTION_DESCRIPTOR
binding_status = BOUND_SOURCE_PROJECTION_SEMANTIC_ONLY
runtime_effect_allowed = false
```

So “effect bound” here means “the matched condition can carry its already reviewed source projection descriptor.” It does **not** mean a state transition has been executed.

## 7. Output maturity

For one explicit evaluation run:

```text
Product condition compiled = true
condition evaluated        = true
semantic effect bound      = true only when condition matches
runtime effect allowed     = false
```

Project-level maturity after this pilot:

```text
Career conditions compiled            = 12
Career conditions structurally evaluable = 12
source projection bindings            = 12
runtime dynamic response execution    = NOT_IMPLEMENTED
Decade/Year composition               = NOT_IMPLEMENTED
ResponseProfile tau                   = NOT_IMPLEMENTED
M0                                    = NOT_IMPLEMENTED
predictive validity                   = NOT_VALIDATED
```

## 8. Why NATAL only

All twelve promoted condition plans are NATAL Career conditions.

This pilot therefore deliberately proves the first half of the chain:

```text
NATAL chart -> condition truth -> source projection descriptor
```

The next separate Product unit must combine this source-grounded natal state with:

```text
E_decade + E_year
```

before any sparse symbolic τ can be claimed.

## 9. Non-claims

This pilot does not establish:

- a completed Response Compiler;
- a completed Temporal Response layer;
- ResponseProfile τ;
- numeric effect magnitude;
- probability;
- empirical calibration;
- predictive validity;
- individualized prediction.

## 10. Next work

```text
PL3R_DECADE_YEAR_RESPONSE_COMPILER
```

That work may begin only from explicit, source-backed temporal evidence and must preserve NATAL truth separately from E_t.

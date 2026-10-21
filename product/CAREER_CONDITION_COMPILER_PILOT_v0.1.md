# PL3-R Career Condition IR Compiler Pilot v0.1

Status: **IMPLEMENTED / VALIDATION PENDING**  
Tracking Issue: #521

## 1. Purpose

This is the first Product compiler step in PL3-R.

It translates the 12 source-reviewed Career Knowledge condition-IR records promoted by Product #518 into deterministic Product condition plans.

The boundary is deliberately narrow:

```text
Knowledge condition IR
        ↓
Product typed condition plan
        ↓
STOP
```

This version does **not** yet perform:

```text
condition evaluation
response-effect binding
runtime authorization
ResponseProfile τ generation
```

Therefore “compiled” means structurally translated into a Product contract, not executed.

## 2. Exact compiler input

The active K_response baseline supplies exactly 12 condition-IR-ready rules.

Direct IR:

```text
CA02-181
CA03-228
CA05-411
CA05-417
CA05-419
CA05-433
CA07-638
CA07-681
CA09-820
```

Dependency IR:

```text
CA05-420 -> CA05-419
CA07-639 -> CA07-638
CA07-682 -> CA07-681
```

No other Career row is admitted to this compiler pilot.

## 3. Direct compilation contract

The compiler consumes only the structured `condition_ir` fields.

Supported subject term forms:

```text
STAR(...)
STAR_SYSTEM(...)
TRANSFORM(...,...)
PALACE_BRANCH(...)
```

Target-local `LOCAL_OR` may additionally carry:

```text
ATOM(...)
```

The compiler does not parse `source_condition_text` into runtime semantics.

### Relation contract

v0.1 accepts only the source-reviewed relations actually represented in the promoted IR:

```text
EXACT_GEOMETRY
  geometry = SAME_PALACE
  palace_offsets = [0]

FOUR_DIRECTIONS_VISIBILITY
  geometry = UNSPECIFIED_WITHIN_SCOPE
  palace_offsets = [0,4,6,8]
```

The second form deliberately preserves `UNSPECIFIED_WITHIN_SCOPE`. The compiler does not invent a narrower geometry.

### Member-requirement contract

The Knowledge-local member semantics are preserved verbatim:

```text
PAIR_REQUIRED
ANY_SOURCE_LOCAL
BOTH_SOURCE_LITERAL
BOTH_SOURCE_LOCAL
```

They are not silently rewritten into a global ANY/ALL policy.

## 4. Dependency compilation

The three “前格” rows compile as references:

```text
PRODUCT_CONDITION:CA05-420
  -> PRODUCT_CONDITION:CA05-419

PRODUCT_CONDITION:CA07-639
  -> PRODUCT_CONDITION:CA07-638

PRODUCT_CONDITION:CA07-682
  -> PRODUCT_CONDITION:CA07-681
```

The child condition plan contains no copied subject AST, relation AST, target AST, projection, outcome or valence.

The following inheritance remains explicitly prohibited:

```text
PARENT_PROJECTION
PARENT_OUTCOME
PARENT_TARGET
PARENT_VALENCE
TEXT_ADJACENCY
```

Only the exact parent condition scope is referenced.

## 5. Fail-closed rejection surface

The other 14 rows that are `LOCAL_STRUCTURE_READY` but not condition-IR-ready remain explicit compiler rejections:

```text
compiler_status = NOT_COMPILER_INPUT
```

with a blocker carrying their Knowledge compiler-readiness band.

This includes:

- 11 dependency-effective-underdetermined rows;
- 3 direct relation/composition-deferred rows.

The compiler cannot use row-local readiness alone as admission.

## 6. Output maturity

The versioned registry is:

```text
product/CAREER_CONDITION_COMPILER_PILOT_v0.1.json
```

Expected census:

```text
Knowledge condition IR ready          = 12
Product condition plans compiled      = 12
  direct                              = 9
  dependency reference                = 3
local-ready rows rejected             = 14

condition evaluated                   = 0
response effects bound                = 0
runtime effects authorized            = 0
```

Every compiled record therefore has:

```text
product_condition_compiled = true
condition_evaluated        = false
response_effect_bound      = false
runtime_effect_allowed     = false
```

## 7. Why this is a real compiler step

Before this work, Product only knew that 12 Knowledge rows had suitable condition IR.

After this work, Product has a deterministic, typed, versioned condition-plan registry that:

- validates the operator vocabulary;
- validates exact geometry constraints;
- validates source-local member requirements;
- parses only explicit term forms;
- resolves exact dependency references;
- rejects unsupported relations instead of guessing;
- can be consumed by a later condition evaluator.

The compiler output is therefore executable *as a contract*, but not executable *as a Ziwei response rule*.

## 8. Next PL3-R step

The next bounded work should be:

```text
PL3R_CAREER_CONDITION_EVALUATOR_AND_EFFECT_BINDING_PILOT
```

That work must separately prove:

1. which N / E facts satisfy a compiled condition;
2. which source-backed response semantic/effect record belongs to the rule;
3. that effect binding remains semantic-only until explicit runtime authorization;
4. how a sparse symbolic τ record is formed.

These stages must not be collapsed.

## 9. Non-claims

This pilot does not establish:

- a completed Response Compiler;
- a completed ResponseProfile τ engine;
- real-world event prediction;
- probability;
- numeric response magnitude;
- empirical or predictive validity.

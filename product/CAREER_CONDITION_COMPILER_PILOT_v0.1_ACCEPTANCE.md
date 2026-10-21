# Career Condition IR Compiler Pilot v0.1 — Acceptance

Tracking Issue: #521  
Lane: PRODUCT_ONLY  
Status: **IMPLEMENTED / VALIDATION PENDING**

## Scope completed

This work unit adds the first bounded PL3-R condition compiler over the active Product Knowledge v0.3 K_response baseline.

Deliverables:

- `src/product/response_condition_compiler.py`
- `product/CAREER_CONDITION_COMPILER_PILOT_v0.1.json`
- `product/CAREER_CONDITION_COMPILER_PILOT_v0.1.md`
- focused deterministic compiler tests

## Acceptance matrix

| Requirement | Status |
|---|---|
| exact compiler input = promoted condition-IR-ready set | PASS; 12 |
| direct compiled plans | PASS; 9 |
| dependency-reference compiled plans | PASS; 3 |
| local-ready non-IR rows rejected | PASS; 14 |
| direct compiler ignores free-form source prose | PASS by mutation test |
| STAR / STAR_SYSTEM / TRANSFORM / PALACE_BRANCH typed | PASS |
| LOCAL_OR ATOM/TRANSFORM typed | PASS |
| SAME_PALACE offset 0 preserved | PASS |
| FOUR_DIRECTIONS visibility offsets preserved | PASS |
| unspecified relation scope not narrowed | PASS |
| source-local member requirement preserved | PASS |
| dependency child copies no parent AST | PASS |
| prohibited parent inheritance remains explicit | PASS |
| unsupported geometry fails closed | PASS |
| Knowledge source flags rewritten | NO |
| Product conditions evaluated | NO |
| response effects bound | NO |
| runtime effect authorized | NO |
| probability / learned weight introduced | NO |
| predictive validity claimed | NO |

## Maturity

After validation, the strongest allowed claim is:

```text
Career Knowledge condition IR ready       = 12
Product typed condition plans compiled    = 12
Condition evaluator                       = NOT_IMPLEMENTED
Response effect binding                   = NOT_IMPLEMENTED
ResponseProfile tau                       = NOT_IMPLEMENTED
Predictive validity                       = NOT_VALIDATED
```

## Next work

```text
PL3R_CAREER_CONDITION_EVALUATOR_AND_EFFECT_BINDING_PILOT
```

No Human Gate is required unless that next step encounters a condition/effect mapping that is not explicitly represented by the governed Knowledge artifacts.

## Validation

Exact final-head full pytest, P0 audit, Product governance, and deterministic Product regression evidence will be appended to the PR before merge.

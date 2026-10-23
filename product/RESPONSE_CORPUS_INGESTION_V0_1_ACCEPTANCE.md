# Response Corpus Ingestion v0.1 — Acceptance

Issue: #482  
Status: **IMPLEMENTED — VALIDATION REQUIRED ON PR HEAD**

## Accepted Product result

This work unit adds a fail-closed ingestion/readiness layer for NOW-5. It does not implement NOW-6.

### Frozen inventory target

| Item | Expected |
|---|---:|
| major-star canonical rows | 430 |
| exact major-star temporal_response rows | 24 |
| sixty-system canonical rows | 2193 |
| exact sixty-system temporal_reaction rows | 1015 |
| total source temporal candidate rows | 1039 |
| Career temporal audit rows | 9 |
| Career compiler-eligible rows | 0 |
| Response Semantics pilot rows | 8 |
| source-span-verified temporal candidate rows | 0 |
| normalization-verified temporal candidate rows | 0 |
| compiler-ready Kr records | 0 |

### Sixty-system effective review metadata

| Review field | Count |
|---|---:|
| MODEL_SELF_REVIEWED | 1015 |
| source epistemic EXPLICIT | 1015 |
| normalization epistemic UNRESOLVED | 980 |
| normalization epistemic IMPLEMENTATION | 35 |
| selected rows with schema override | 35 |

### Fail-closed acceptance

- exact Knowledge metadata selectors only: **REQUIRED**
- free-text time-keyword selection: **FORBIDDEN**
- Product semantic promotion: **0**
- auto-split decade_or_year: **0**
- case-support promotion: **0**
- probability/numeric gain synthesis: **0**
- Knowledge file modifications: **0**
- NOW6_RESPONSE_COMPILER_INPUT_READY: **FALSE**

## Maturity claim

On merge:

- Response Corpus ingestion/readiness = **IMPLEMENTED_V0_1**
- source inventory = **INTERNALLY_VALIDATED**
- source temporal material = **PRESENT**
- canonical compiler-ready Kr = **0 ON FROZEN BASELINE**
- Response Compiler = **NOT_IMPLEMENTED**
- ResponseProfile tau = **NOT_IMPLEMENTED**
- predictive validity = **NOT_VALIDATED**

Passing deterministic tests does not upgrade source candidates into canonical Kr.

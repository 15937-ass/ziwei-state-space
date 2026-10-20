# Expert Method Case Contracts v0.1 — Acceptance

Tracking Issue: #431  
Lane: PRODUCT_ONLY  
Status: **IMPLEMENTED — VALIDATION EVIDENCE RECORDED IN PR #435**

## Scope completed

本 work unit 只完成 Product v0.4 的专家方法数据契约，不声称已经学会王亭之推法。

已实现：

- CaseBundle；
- ExpertReasoningGraph；
- InferenceTrace；
- MethodPattern；
- SchoolCompatibility；
- synthetic fixture；
- deterministic fail-closed validation。

## Acceptance matrix

| Requirement | Status | Evidence |
|---|---|---|
| CaseBundle separates source/input/target/expert graph/conclusion/outcome | PASS | `src/product/expert_method_contracts.py` |
| person_group_id available for leakage grouping | PASS | CaseBundle |
| outcome optional | PASS | fixture + test |
| blind input excludes expert conclusion / outcome refs | PASS | CaseBundle leakage guard + tests |
| expert graph uses bounded auditable actions | PASS | EXPERT_ACTIONS |
| graph node IDs unique | PASS | deterministic validation |
| edge endpoints exist | PASS | deterministic validation |
| graph acyclic | PASS | deterministic validation |
| STOP / ABSTAIN terminal | PASS | graph + trace validation |
| expert graph separate from machine InferenceTrace | PASS | separate dataclasses + test |
| method maturity explicit | PASS | EPISTEMIC_STATUSES |
| cross-school compatibility bounded | PASS | SCHOOL_COMPATIBILITY_BANDS |
| cross-school compatibility cannot mutate canonical truth | PASS | canonical_merge_allowed must remain false |
| case material cannot become executable canonical truth | PASS | CaseBundle + embedded graph guard |
| hidden/free-form chain-of-thought fields rejected | PASS | recursive forbidden-field gate |
| probability / learned weight absent | PASS | strict schemas |
| real Wang cases ingested | **NO — intentionally out of scope** | next work unit |
| LOCO benchmark run | **NO — intentionally out of scope** | next work unit |
| method fidelity validated | **NO** | future benchmark |

## Maturity statement

合并本 work unit 后，只允许声称：

~~~text
expert-method contract = CONTRACT_READY
expert case corpus = NOT_STARTED
LOCO expert replay = NOT_STARTED
method policy = NOT_IMPLEMENTED
method fidelity = NOT_VALIDATED
predictive validity = NOT_VALIDATED
~~~

## Architectural boundaries preserved

1. expert case != canonical theory；
2. expert conclusion != reality ground truth；
3. machine trace != expert trace；
4. other-school procedural compatibility != Zhongzhou semantic merge；
5. method maturity != allowed-use；
6. contract existence != product capability completion。

## Validation

Final deterministic validation evidence is recorded in PR #435. This acceptance file intentionally does not duplicate mutable workflow-run counts; the PR conversation is the execution-evidence record.

# Method Policy π v0.1 — Acceptance

Tracking Issue: #453  
Lane: PRODUCT_ONLY  
Status: **IMPLEMENTED / VALIDATION PENDING**

## Scope completed

本 work unit 实现 Product v0.4 第一版专家方法策略 baseline：

- deterministic same-domain CBR；
- source MethodPattern 与 runtime policy 的隔离适配；
- evidence readiness model；
- heuristic/symbolic planner；
- structural policy verifier boundary；
- Product #431-compatible InferenceTrace；
- fail-closed abstention；
- Wang LOCO-24 replay-readiness audit；
- materialized synthetic non-abstaining fixture。

## Acceptance matrix

| Requirement | Status | Evidence |
|---|---|---|
| deterministic CBR implemented | PASS | src/product/method_policy.py |
| retrieval uses LOCO allowed IDs only | PASS | retriever + tests |
| held-out person-group leakage rejected | PASS | retriever invariant |
| no expert answer/source identity in CBR payload | PASS | retrieval payload whitelist |
| no learned similarity weights | PASS | exact-domain + case-id deterministic order |
| evidence distinguishes MATERIALIZED / REFERENCE_ONLY / MISSING / BLOCKED | PASS | EvidenceItem |
| SOURCE_CHART ref not treated as fact | PASS | source-ref classifier + tests |
| SEMANTIC_ONLY source patterns do not directly execute | PASS | derived execution adapter |
| WT-003 blocked pending related-palace binding | PASS | execution disposition |
| WT-005/006 deferred to symbolic adapter | PASS | execution disposition |
| executable method requires exact target/evidence scope | PASS | pattern assessment |
| unsupported real Wang case fails closed | PASS | INSPECT -> ABSTAIN |
| synthetic materialized case can complete | PASS | WT-METHOD-001 fixture |
| machine trace compiles under Product #431 contract | PASS | compile_inference_trace tests |
| Wang retrieval-ready folds | 24 / 24 | readiness artifact |
| Wang action-selection-ready folds | 24 / 24 | readiness artifact |
| Wang full-expert-replay-ready folds | 0 / 24 | readiness artifact |
| probability / learned weight introduced | NO | strict test |
| Knowledge semantic file modified | NO | lane boundary |
| method fidelity validated | NO — intentionally out of scope | future Benchmark B |
| predictive validity validated | NO | future prospective benchmark |

## Key finding

当前 Wang 24-case corpus 已经适合做：

~~~text
metadata-safe retrieval
+
next-action fail-closed planning
~~~

但还不适合真正 expert replay，因为 blind input 仍主要是：

~~~text
SOURCE_CHART / source-span references
~~~

而不是 machine-readable chart facts。

因此版本化 readiness audit 的合法结论是：

~~~text
RETRIEVAL_READY          = 24 / 24
ACTION_SELECTION_READY   = 24 / 24
FULL_EXPERT_REPLAY_READY = 0 / 24
~~~

## Dependency recorded

Benchmark B 真正运行前需要：

~~~text
WANG_BLIND_EVIDENCE_MATERIALIZATION_V0_1
~~~

这项依赖不能通过 LLM 自行猜盘来绕过。

## Maturity statement

合并后只允许声称：

~~~text
deterministic CBR            = IMPLEMENTED
Method Policy π              = BASELINE_IMPLEMENTED_V0_1
procedural adapter           = IMPLEMENTED_V0_1
fail-closed abstention       = IMPLEMENTED
Wang readiness audit         = COMPLETE
Wang machine replay          = NOT_READY
method fidelity              = NOT_VALIDATED
predictive validity          = NOT_VALIDATED
~~~

## Next main-path Product work

按 Product v0.4 已批准 critical path，下一主线工作应继续：

~~~text
RESPONSE_SEMANTICS_FAIL_CLOSED_ADAPTER
~~~

同时将 WANG_BLIND_EVIDENCE_MATERIALIZATION_V0_1 记录为 Benchmark B 前的 Product dependency，不把它误报成已经完成的 replay。

## Validation

Repository / Product CI evidence will be appended to the PR before merge.

# Method Policy π v0.1 — CBR + Heuristic/Symbolic Planner

Status: **IMPLEMENTED IN PRODUCT #453 — VALIDATION PENDING**  
Policy version: METHOD_POLICY_V0_1_CBR_HEURISTIC_SYMBOLIC

## 1. Purpose

Product v0.4 的专家方法层现在第一次有一个可执行的 baseline：

~~~text
Blind Case View
+ LOCO allowed retrieval set
+ source-reviewed MethodPattern corpus
+ Product-side procedural execution adapter
+ evidence readiness
↓
deterministic CBR
↓
bounded next-action selection
↓
InferenceTrace
↓
STOP / ABSTAIN
~~~

它回答的是：下一步应该看什么、能不能继续、什么时候必须停。

它不回答：这个命盘最终会发生什么。

因此 π v0.1 是程序策略，不是新的中州派知识库，也不是现实预测模型。

## 2. Why v0.1 is deliberately deterministic

当前 Wang corpus 只有 24 个来源明确案例。这个规模适合 Case-Based Retrieval、显式方法规则、deterministic heuristic、blind leakage audit 与 abstention benchmark。

它不适合现在就做 neural fine-tuning、learned policy、embedding similarity as truth、reward model 或 RL。

第一版必须先建立一个“即使笨，但知道自己什么时候不知道”的 baseline。

## 3. Deterministic CBR

CBR 只看到 case_id、person_group_id、target domain 和 LOCO 允许的 retrieval IDs。

它不看到 source subject label、expert prose、ExpertReasoningGraph、expert conclusion、outcome 或 biography。

v0.1 只做：

~~~text
EXACT_TARGET_DOMAIN
~~~

并按 case_id 稳定排序。不设相似度分数，不设 learned weight，不用 LLM embedding。

王亭之当前 24 例正好是 12 个主题 × 2，因此每个 held-out case 都有 1 个同 domain 的合法 retrieval case：

~~~text
24 / 24 folds = RETRIEVAL_READY
~~~

但 retrieval ready 不等于 expert replay ready。

## 4. Evidence readiness

π v0.1 正式区分：

~~~text
MATERIALIZED_FACT
SOURCE_REFERENCE_ONLY
MISSING
BLOCKED
~~~

例如：

~~~text
SOURCE_CHART:WANG-CASE-001
~~~

只是一个可追溯引用，不等于命宫、主星、三方四正、四化等机器可读取事实。

因此 source/page/chart reference 不得直接被 planner 当成命盘事实。

当前 Wang 24-case CaseBundle 的 blind evidence 全部仍属于：

~~~text
SOURCE_REFERENCE_ONLY
~~~

结果是：

~~~text
24 / 24 folds = reference-only
0 / 24 folds  = FULL_EXPERT_REPLAY_READY
~~~

## 5. SEMANTIC_ONLY cannot directly execute

Product #441 的 6 条 Wang MethodPattern 目前仍是：

~~~text
maturity    = SOURCE_EXPLICIT
allowed_use = SEMANTIC_ONLY
~~~

Product v0.4 的硬边界要求 SEMANTIC_ONLY 不得直接产生 runtime effect。

所以本 Issue 没有把 source MethodPattern 偷偷改成 executable。新增的是独立的 Product derived artifact：

~~~text
product/METHOD_POLICY_EXECUTION_RULES_v0.1.json
~~~

它只回答某个 source-explicit method 是否可以安全地编译成“搜索/检查顺序”，不改变 source truth。

## 6. Six source methods: execution disposition

WT-METHOD-001：父母宫 -> 田宅宫。Disposition = POLICY_EXECUTABLE_DERIVED，仅限 GLOBAL_PROFILE 且 PARENTS_PALACE / PROPERTY_PALACE 都已 MATERIALIZED。

WT-METHOD-002：命宫 + 福德宫联合观察。Disposition = POLICY_EXECUTABLE_DERIVED，只控制 observation order。

WT-METHOD-003：根据前面发现的疑点继续追查相关宫位。Disposition = BLOCKED_CONTEXT_BINDING，因为 RELATED_PALACE 必须先被明确绑定，π 不允许自己猜。

WT-METHOD-004：原局 -> 大限 -> 流年。Disposition = POLICY_EXECUTABLE_DERIVED，但只有 target = TEMPORAL_INFERENCE 且 NATAL / DECADE / YEAR 都已 materialized 才能执行。

WT-METHOD-005：借星安宫/借入整组星系。Disposition = DEFER_TO_SYMBOLIC_ADAPTER，因为这会改变 symbolic interpretation。

WT-METHOD-006：对星相对位置及力量层级。Disposition = DEFER_TO_SYMBOLIC_ADAPTER，同样属于 symbolic/canonical adapter，而不是 π v0.1。

## 7. Planner behavior

只有当 target scope 明确匹配、derived execution rule 明确允许、required evidence kinds 全部 MATERIALIZED、source action sequence 与 adapter action sequence 完全一致，才允许生成非 abstaining path。

Synthetic fixture：

~~~text
GLOBAL_PROFILE
+ materialized PARENTS_PALACE
+ materialized PROPERTY_PALACE
↓
WT-METHOD-001
↓
INSPECT
→ CROSS_CHECK
→ CLASSIFY
→ STOP
~~~

这里的 CLASSIFY 是 procedural trace action，不生成新的 canonical Ziwei rule。

## 8. Real Wang cases: expected fail-closed behavior

当前真实 Wang case 的 blind chart evidence 只是 SOURCE_REFERENCE_ONLY，所以 π v0.1 的正确行为是：

~~~text
INSPECT
   ↓
发现输入只是 source reference
   ↓
ABSTAIN
~~~

而不是让模型凭记忆猜盘面。

当前 readiness：

~~~text
RETRIEVAL_READY          = 24 / 24
ACTION_SELECTION_READY   = 24 / 24
FULL_EXPERT_REPLAY_READY = 0 / 24
~~~

ACTION_SELECTION_READY 的含义只是系统能合法地选择 INSPECT -> ABSTAIN，并不意味着能完成专家推演。

## 9. Canonical verifier boundary

v0.1 verifier 只验证 target scope、evidence readiness、derived policy rule、action vocabulary、source action sequence equality 和 fail-closed terminal behavior。

它不验证新的中州派含义。因此 method-only trace 中 canonical_rule_refs 为空。

如果未来需要执行 canonical semantic action，必须通过对应 canonical verifier/adapter，而不能让 π 自己证明自己。

## 10. Readiness artifact

版本化审计：

~~~text
product/WANG_METHOD_POLICY_READINESS_v0.1.json
~~~

逐 fold 记录 held-out case、target domain、exact-domain retrieval、blind evidence status、source-method applicability、blockers 和三层 readiness。

当前结论：

~~~text
recommended dependency:
WANG_BLIND_EVIDENCE_MATERIALIZATION_V0_1
~~~

它是未来真正运行 Wang expert replay 前的工程依赖，不是 Product 架构变更。

## 11. Synthetic fixture

~~~text
product/METHOD_POLICY_SYNTHETIC_FIXTURE_v0.1.json
~~~

只用于测试 derived executable method、non-abstaining path、InferenceTrace contract 和 STOP semantics。

Synthetic facts 永远不能进入 Wang corpus、中州 canonical knowledge 或 empirical calibration。

## 12. Maturity

可以声称：

~~~text
deterministic CBR                 = IMPLEMENTED
procedural execution adapter      = IMPLEMENTED_V0_1
heuristic/symbolic planner π      = IMPLEMENTED_V0_1
fail-closed abstention            = IMPLEMENTED
Wang replay readiness audit       = COMPLETE
~~~

不能声称：

~~~text
Wang expert replay                = complete
expert method fidelity            = validated
Ziwei prediction                  = validated
probability calibration           = available
~~~

## 13. Dependency discovered

在真正进行 Benchmark B 之前，需要：

~~~text
WANG_BLIND_EVIDENCE_MATERIALIZATION_V0_1
~~~

目标是把合法 blind input 从 SOURCE_CHART 引用转换成 machine-readable chart facts，同时保证只来自推断前可见资料、不泄漏人物身份、不泄漏专家解释/结果，并与 deterministic chart engine 对齐。

在这项依赖完成前，0/24 FULL_EXPERT_REPLAY_READY 是正确状态，不是缺陷。

## 14. Next architecture step

按 Product v0.4 主 critical path，Method Policy v0.1 完成后仍可继续：

~~~text
Response Semantics Fail-Closed Adapter
~~~

Wang evidence materialization 作为 Benchmark B 前必须完成的 bounded dependency 进入 Product queue。这样不会为了等待案例 replay 而阻塞独立的 Response Engine 主线。

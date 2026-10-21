# Method Policy π v0.1 — CBR + Heuristic/Symbolic Planner

Status: **IMPLEMENTED IN PRODUCT #453 — BLIND EVIDENCE UPDATED BY PRODUCT #512**  
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

Product #512 之后，Wang 24-case 的 blind evidence 被拆成两个不同成熟度：

~~~text
TARGET_PALACE = MATERIALIZED_FACT   24 / 24
TARGET_CHART  = BLOCKED             24 / 24
~~~

v0.1 只物化目标宫位及十四主星系统；六个目标宫无正曜的案例保留来源中明确的对宫借星。辅曜、煞曜、四化、宫干支、年龄区间及全盘其他宫位均未自动补齐。

因此 SOURCE_REFERENCE_ONLY 不再是目标宫位层的 blocker，但也不能把“目标宫位已物化”误称为“全盘已物化”。

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

Product #512 后，真实 Wang case 已经能读取 source-grounded 的 TARGET_PALACE materialized fact，但完整 TARGET_CHART 仍然 BLOCKED。

同时，现有 6 条 source-explicit MethodPattern 的 target scope 是 GLOBAL_PROFILE、TEMPORAL_INFERENCE 或 SYMBOLIC_INFERENCE，而 24 个 held-out case 的 target 是十二个具体宫位 domain。于是 π v0.1 的正确行为仍然是：

~~~text
INSPECT materialized target-palace evidence
   ↓
发现 full chart 未物化 + 无 MethodPattern 直接绑定当前 case target scope
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
product/WANG_METHOD_POLICY_READINESS_v0.2.json
~~~

逐 fold 记录 held-out case、target domain、exact-domain retrieval、blind evidence status、source-method applicability、blockers 和三层 readiness。

当前结论：

~~~text
TARGET_PALACE MATERIALIZED = 24 / 24
TARGET_CHART BLOCKED       = 24 / 24
FULL_EXPERT_REPLAY_READY   = 0 / 24

remaining review:
- full-chart materialization boundary
- individual case-domain -> source MethodPattern scope binding
~~~

后续不得为了让 benchmark 变成 24/24 而擅自扩大 MethodPattern 的 target scope；若要建立这种绑定，必须从来源方法证据中另行论证。

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

Product #512 已完成第一层 Wang blind evidence materialization：24/24 目标宫位及十四主星系统成为 machine-readable facts，且不泄漏人物身份、专家解释或结果。

它同时暴露了两个此前被 SOURCE_REFERENCE_ONLY 遮住的下一层问题：完整命盘仍未物化；现有 MethodPattern 没有直接覆盖十二个 case target domain。因此 0/24 FULL_EXPERT_REPLAY_READY 仍然是正确状态，不是缺陷，也不能通过扩大方法规则适用范围来“刷通过率”。

## 14. Next architecture step

按 Product v0.4 主 critical path，Method Policy v0.1 完成后仍可继续：

~~~text
Response Semantics Fail-Closed Adapter
~~~

Wang evidence materialization 作为 Benchmark B 前必须完成的 bounded dependency 进入 Product queue。这样不会为了等待案例 replay 而阻塞独立的 Response Engine 主线。

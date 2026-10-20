# Expert Method Case Contracts v0.1

Status: **CONTRACT IMPLEMENTED — NO REAL CASES INGESTED**  
Tracking Issue: #431  
Architecture: Product v0.4 / Proposal #425

## 1. Purpose

本契约把 Product v0.4 的“专家如何调用知识”变成可执行、可验证的数据接口，供后续：

- 王亭之专家案例结构化；
- Leave-One-Case-Out expert replay；
- Case-Based Reasoning；
- Method Policy π；
- Expert Method Fidelity benchmark；
- cross-school procedural robustness。

本契约**不定义新的紫微理论，不保存模型隐藏思维过程，不训练概率，也不把案例结论升级为 canonical truth**。

---

## 2. 与旧 CaseEvidenceRecord 的关系

旧的 `training_data/CASE_EVIDENCE_SCHEMA_v0.1.md` 已经解决：

- 出生输入；
- source page；
- question；
- author claims；
- prediction；
- feedback/outcome；
- rule linking。

v0.4 新需求不是废弃这些字段，而是补足两个旧 schema 没有正式表达的对象：

1. **ExpertReasoningGraph**：专家案例中可观察、可引用、可审计的推理动作 DAG；
2. **InferenceTrace**：机器在 blind/replay 时产生的独立轨迹。

因此以后：

~~~text
source case
  -> CaseBundle
     -> ExpertReasoningGraph

machine replay
  -> InferenceTrace
~~~

二者永久分离，不能让机器 trace 覆盖作者案例证据。

本 Issue 不迁移 `training_data/**`；后续 Wang-case work unit 再使用本 contract 创建 Product-side structured cases。

---

## 3. CaseBundle

CaseBundle 是一个专家案例的最小可学习单元。

必须分离：

~~~text
identity / leakage group
source / school / author / provenance
input refs
chart snapshot ref
target question / domains / target time
information available before inference
expert reasoning graph
expert conclusion refs
outcome refs (optional)
epistemic status
allowed use
~~~

### 3.1 关键边界

`person_group_id` 用于防止同一人物的不同问法或不同时段落入 train/test 两侧。

`available_information_refs` 只记录推断开始时可见的信息。后续 outcome 不得偷偷混入 blind input。

`outcome_refs` 可以为空。专家方法学习不依赖现实 outcome。

案例整体 allowed-use 仅允许：

~~~text
RETRIEVAL_ONLY
CASE_SUPPORT_ONLY
BLOCKED
~~~

**不允许 CaseBundle 自身成为 EXECUTABLE canonical truth。**

---

## 4. ExpertReasoningGraph

### 4.1 为什么是 DAG

专家案例往往不是严格一条线：

~~~text
先看原局
  ├─ 检查事业宫
  ├─ 交叉看命宫/迁移宫
  └─ 再进入大限
       ↓
      流年
~~~

因此 v0.1 用 DAG / partial order，而不是只存一串自然语言“思维链”。

### 4.2 动作词表

v0.1 冻结：

~~~text
INSPECT
CLASSIFY
ACTIVATE
COMPARE
REFINE
CROSS_CHECK
REJECT
CONFIRM
ABSTAIN
STOP
~~~

含义：

- INSPECT：查看一个结构或证据；
- CLASSIFY：把已有证据归到某已定义类别；
- ACTIVATE：记录 source/canonical 支持的激活；
- COMPARE：比较两个结构、时间层或候选；
- REFINE：进入更细粒度层；
- CROSS_CHECK：用另一宫位/证据路径复核；
- REJECT：排除候选；
- CONFIRM：在现有证据内确认候选路径；
- ABSTAIN：证据不足，主动停止给出结论；
- STOP：推理流程完成。

### 4.3 节点必须可审计

每个 node 至少绑定以下之一：

- evidence refs；
- canonical rule refs；
- source span refs。

同时可保存：

- temporal layer；
- palace targets；
- domain targets；
- epistemic status；
- allowed use。

不允许保存：

~~~text
chain_of_thought
hidden_reasoning
private_reasoning
internal_reasoning
cot
scratchpad
analysis_trace
~~~

这些字段在任何层级出现都会 fail closed。

### 4.4 图结构约束

- node_id 唯一；
- edge_id 唯一；
- edge endpoints 必须存在；
- 图必须 acyclic；
- STOP / ABSTAIN 不能有 outgoing edge。

---

## 5. InferenceTrace

InferenceTrace 表示**机器实际走过的 replay/blind 路径**。

与 ExpertReasoningGraph 不同：

~~~text
ExpertReasoningGraph
= source-backed expert demonstration

InferenceTrace
= machine execution record
~~~

二者未来用于 Benchmark B 对齐，而不是互相替换。

v0.1 mode：

~~~text
BLIND
EXPERT_REPLAY
DEVELOPMENT
~~~

每一步保存：

- step_id；
- ordinal；
- action；
- evidence refs；
- canonical rule refs；
- temporal layer；
- palace/domain targets；
- verifier status；
- verifier refs。

机器 proposal 只有在 verifier 明确支持时才标 `VERIFIED`。

### 5.1 Terminal contract

- COMPLETED 必须以 STOP 结束；
- ABSTAINED 必须以 ABSTAIN 结束；
- STOP/ABSTAIN 不能出现在中间。

这会为以后评估“该停时有没有停”提供稳定接口。

---

## 6. MethodPattern

MethodPattern 是从 source 或多个案例中抽出的**可复用 procedure**，不是紫微事实规则。

成熟度严格区分：

~~~text
SOURCE_EXPLICIT
SOURCE_DEMONSTRATED
RECONSTRUCTED
INDUCED
EMPIRICALLY_VALIDATED
~~~

约束：

- SOURCE_EXPLICIT 必须有 source_span_refs；
- SOURCE_DEMONSTRATED / RECONSTRUCTED / INDUCED 必须有 source_case_refs；
- action_sequence 只能使用 v0.1 expert actions；
- terminal action 如出现，只能位于 sequence 末尾。

MethodPattern 可被后续 π 消费，但其 maturity 不得被隐藏。

---

## 7. SchoolCompatibility

跨流派方法材料必须先分类：

~~~text
IDENTICAL
SEMANTIC_EQUIVALENT
PROCEDURAL_COMPATIBLE
SCHOOL_SPECIFIC
CONFLICTING
UNKNOWN
~~~

v0.1 中：

~~~text
IDENTICAL
SEMANTIC_EQUIVALENT
PROCEDURAL_COMPATIBLE
~~~

可被标记为 `method_transfer_allowed=true`。

但无论哪一档：

~~~text
canonical_merge_allowed = false
~~~

即使方法兼容，也不能因此把其他派的 semantic truth 合并进中州派 canonical core。

---

## 8. Epistemic vs allowed-use

两个字段用途不同。

### epistemic_status

回答：

> 这条方法/动作是怎么知道的？

~~~text
SOURCE_EXPLICIT
SOURCE_DEMONSTRATED
RECONSTRUCTED
INDUCED
EMPIRICALLY_VALIDATED
~~~

### allowed_use

回答：

> 当前系统允许拿它干什么？

~~~text
EXECUTABLE
SEMANTIC_ONLY
RETRIEVAL_ONLY
CASE_SUPPORT_ONLY
BLOCKED
~~~

一个内容“表达得出来”不等于“可以执行”。

---

## 9. 王亭之案例后续使用方式

本 contract 完成后，下一 Product work unit 才开始真实王亭之案例结构化。

每个案例目标结构：

~~~text
CaseBundle
├─ source identity
├─ input-visible facts
├─ chart snapshot
├─ target
├─ ExpertReasoningGraph
├─ expert conclusion refs
└─ optional outcome refs
~~~

LOCO 时：

~~~text
9 cases
-> retrieval / method induction

1 held-out case
-> machine InferenceTrace
-> compare with held-out ExpertReasoningGraph
~~~

循环全部案例。

---

## 10. 了然山人 / 其他三合派

旧 Liaoran casebook 仍是有效 Product-side Case Reasoning Corpus，但不能直接假设其 procedure 与 Zhongzhou 等价。

以后迁移时必须增加 SchoolCompatibility。

其他三合派案例也遵循同一规则：

> 方法可以比较和迁移；school-specific semantics 不能静默合并。

---

## 11. 本版本故意没有的东西

v0.1 不包含：

- expert conclusion 的现实概率；
- outcome probability；
- continuous qi weight；
- expert “可信度分数”；
- learned policy weight；
- reward；
- causal effect；
- canonical rule generation；
- hidden chain-of-thought。

这是为了让第一阶段数据保持 source-grounded、auditable、non-numeric。

---

## 12. Synthetic fixture

`product/EXPERT_METHOD_SYNTHETIC_FIXTURE_v0.1.json` 只验证 contract。

它不表达真实紫微理论，也不能进入任何 canonical corpus。

Fixture 同时包含：

- 1 CaseBundle；
- 1 ExpertReasoningGraph；
- 1 machine InferenceTrace；
- 1 MethodPattern；
- 1 SchoolCompatibility。

后续真实案例必须替换 synthetic refs 为真实 source/page/span refs。

---

## 13. Maturity claim

本 work unit 完成后的能力只能写：

~~~text
expert-method contract: CONTRACT_READY
real Wang case corpus: NOT_STARTED
LOCO replay: NOT_STARTED
method fidelity: NOT_VALIDATED
predictive validity: NOT_VALIDATED
~~~

**schema/contract ready 不等于系统已经学会专家方法。**

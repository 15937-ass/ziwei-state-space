# Proposal #425 — Product v0.4：专家推理、反应动力学与分阶段验证架构

Status: **IMPLEMENTED BY PR #427**  
Tracking Issue: #425  
Risk: **R3 / Human Gate**  
Lane: **GOVERNANCE_ONLY**

## Motivation

Product v0.3 已经建立了 deterministic chart、canonical natal、temporal environment、personal state、manifestation、calibration 与 decision support 的长期方向，但现阶段出现了明显的结构性失衡：

1. Product 的最近推进主要表现为 Career NATAL rule 横向扩张，能力增长与规则数量增长不同步；
2. 现有 PL3-T 将“时间环境”与“原局如何响应时间环境”放在同一语义邻域，无法清楚表达中州派强调的“先识本质，再看运限对本质的反应”；
3. Knowledge 侧已经开始拆出 Response Semantics，但 Product 尚无独立 Response Compiler / ResponseProfile；
4. Product 只正式消费 declarative knowledge，尚未把专家如何选择证据、安排推断顺序、处理冲突、决定继续或停止的 procedural knowledge 建模；
5. 王亭之完整专家案例数量很少（约 10 个），不适合统计参数训练，但非常适合 expert reasoning distillation；
6. 其他三合派案例数量更大，可用于检验 procedural method 的泛化，但不能反写中州派 canonical truth；
7. Internal fidelity、expert-method fidelity 与 real-world predictive validity 需要进一步彻底分层，避免“复现专家”被误报成“现实预测有效”。

本 Proposal 的目的不是增加一个更复杂的黑盒模型，而是重新冻结 Product 的主轴：

```text
知识是什么
  +
知识如何响应
  +
专家如何调用知识
  +
现实数据如何校准
  +
个人状态如何更新
```

分别建模、分别验证、分别版本化。

---

## Goals

### 2.1 建立五个永久隔离的核心对象

```text
Kc   Canonical declarative knowledge
Kr   Canonical response knowledge
π    Inference policy / procedural knowledge
θ    Empirical calibration parameters
b    Individual state belief
```

### 2.2 将 ResponseProfile 设为正式中间态

把：

```text
Natal + Temporal -> Event
```

改成：

```text
Natal Essence N
+ Temporal Environment E_t
+ Canonical Response Knowledge Kr
        ↓
ResponseProfile τ_t
        ↓
Manifestation candidates
```

### 2.3 增加 Expert Reasoning / Method Layer

方法层回答的不是“什么规则是真的”，而是：

- 下一步观察什么；
- 哪些证据优先；
- 哪些证据是确认、反证或仅补充；
- 何时从大限进入流年；
- 何时需要跨宫检查；
- 何时应停止、保留冲突或 abstain。

### 2.4 把王亭之案例变成 expert demonstrations

所有案例最终都进入 Expert Case Bank，但采用 **Leave-One-Case-Out (LOCO) Expert Replay**，使每个案例至少有一次在 method induction 时保持 unseen。

### 2.5 把其他三合派案例用于方法泛化而非 canonical 校正

其他三合派案例经过 school compatibility classification 后，只允许：
- 支持 procedural pattern；
- 做 cross-school robustness；
- 帮助 case retrieval；
- 暴露 method blind spot。

不得直接改变 Zhongzhou canonical rule truth。

### 2.6 将 Forecast Ledger 前置

当第一条 source-only vertical slice：

```text
Chart -> N -> E_t -> τ_t -> M0
```

可运行时，即开始 prospective forecast lock，不等待未来复杂模型完成。

---

## Non-Goals

本 Proposal 不：

- 实现 Product runtime；
- 新增 Knowledge canonical rules；
- 将 expert cases 当 empirical probability ground truth；
- 用其他三合派结果纠正中州派 source truth；
- 训练 neural network / GNN / MoE / RL / neural state-space；
- 人工制造 continuous qi weights、decay rates 或 event probabilities；
- 把 Response Semantics compatibility 自动视为 executable；
- 修改当前 Knowledge lane 的 source review 或 compatibility review；
- 宣称斗数现实预测有效。

---

## Proposed Design

以下第 4–17 节构成 Product v0.4 的详细设计：来源与认识论隔离、六层产品架构、响应中间态、专家案例计划、Knowledge→Product contract、评估、当前/未来工作与测试。

## 4. Source and epistemic separation

### 4.1 四类知识资产

```text
K_signal
  静态结构、条件、星系、宫位、四化、投影

K_response
  本质 × 环境 -> strengthen / weaken / transform / gate / activate

K_manifest
  response -> source-supported manifestation family/channel

K_method
  专家如何组织上述知识进行推断
```

前三者的 canonical 部分来自 source-reviewed Knowledge；K_method 中只有 source-explicit method 可以进入 canonical procedural knowledge。

### 4.2 方法知识成熟度

```text
SOURCE_EXPLICIT
SOURCE_DEMONSTRATED
RECONSTRUCTED
INDUCED
EMPIRICALLY_VALIDATED
```

定义：

- **SOURCE_EXPLICIT**：作者明确陈述的方法原则；
- **SOURCE_DEMONSTRATED**：作者案例明确表现出的操作，但未宣称为普遍原则；
- **RECONSTRUCTED**：为对齐案例而重建的可能中间步骤；
- **INDUCED**：跨多个案例归纳出来的 procedure；
- **EMPIRICALLY_VALIDATED**：在 held-out / prospective evaluation 中稳定有效的方法。

低层级不得伪装成高层级。

---

## 5. Product v0.4 architecture

### L0 — Source & Provenance

保存：
- school；
- author；
- source artifact；
- source span；
- artifact type；
- source status；
- review status；
- allowed use；
- version。

### L1 — Canonical Knowledge

消费：
- K_signal；
- K_response；
- K_manifest。

Product 不得把 semantic compatibility 自动升级为 executable。

### L2 — Deterministic Symbolic Engine

```text
Birth input
  -> deterministic chart
  -> canonical signal runtime
  -> Natal Essence Graph N
  -> Temporal Environment E_t
```

N 与 E_t 分离：
- N 是 canonical natal structure / essence；
- E_t 是 target-time environment，不是 outcome。

### L3 — Expert Reasoning Layer

组件：

```text
Expert Case Bank
+ Case Retriever
+ Procedural KB
+ Inference Policy π
+ Canonical Verifier
```

π 只决定“下一步尝试什么”，不拥有 rule truth。

### L4 — Dynamic Response Layer

```text
τ_t = R_K(N, E_t)
```

第一代 ResponseProfile 必须是 sparse / symbolic / source-traceable，而不是 dense learned vector。

至少支持：
- activated tendencies；
- strengthened；
- weakened；
- transformed；
- gated；
- conflicts；
- ordinal constraints；
- effect targets；
- source evidence。

### L5 — Reality / Empirical Layer

长期对象：

```text
X_t   real/acquired latent state
b_t   system belief about X_t
A_t   user action
C_t   external context/exposure
θ     empirical calibration parameters
```

保持：

```text
X_t != b_t
```

现实反馈更新 b/θ，不修改 canonical N/K。

### L6 — Product / Explanation Layer

最终由 EvidencePackage 驱动：
- ordinary explanation；
- advanced explanation；
- expert/debug trace；
- contrastive explanation；
- abstention / uncertainty。

LLM 是 proposal + interface，不是 truth engine。

---

## 6. Revised semantic pipeline

```text
Birth / Chart
   ↓
Canonical Signal Runtime
   ↓
Natal Essence Graph N
   +
Temporal Environment E_t
   +
Canonical Response Knowledge Kr
   ↓
Expert reasoning policy π chooses inspection/search actions
   ↓
Canonical verifier validates every step
   ↓
Response Compiler
   ↓
ResponseProfile τ_t
   ↓
Canonical Manifestation Candidates M0
   ↓
X_t / b_t / A_t / C_t
   ↓
Contextual Manifestation M1
   ↓
Empirical calibration θ
   ↓
EvidencePackage
   ↓
LLM / UI
```

π 不直接生成 τ；它负责决定要检查哪些 canonical facts / response relations，τ 仍由 canonical compiler 产生。

---

## 7. Temporal hierarchy

开发和推断顺序冻结为：

```text
NATAL
  -> DECADE
  -> YEAR
  -> MONTH only when triggered
  -> DAY/HOUR later
```

原因：
- 当前 Product 的目标是先建立可验证 vertical slice；
- 更细时间层组合爆炸严重；
- 细粒度层不应在缺乏上层候选信号时无目的搜索。

v0.4 第一阶段 Response Compiler 只要求 **Decade + Year**。

---

## 8. Expert Case Program

### 8.1 CaseBundle

每个案例至少拆分：

```text
CaseBundle
├─ source/provenance
├─ ChartSnapshot
├─ target question / target time
├─ information available at start
├─ ExpertReasoningGraph
├─ expert conclusion
└─ known outcome (if source supplies it)
```

### 8.2 ExpertReasoningGraph

只保存可审计操作，不保存不可审计的自由文本思维过程。

推荐动作：
- INSPECT；
- CLASSIFY；
- ACTIVATE；
- COMPARE；
- REFINE；
- CROSS_CHECK；
- REJECT；
- CONFIRM；
- ABSTAIN；
- STOP。

表示为 DAG / partial order，而非要求系统逐字逐步复现作者。

### 8.3 Wang-10 evaluation

所有王亭之案例最终全部进入训练/案例库，但 evaluation 采用：

```text
10 folds:
  9 cases available for method induction/retrieval
  1 case held out for blind expert replay
```

循环十次。

这解决“小样本但每例都很珍贵”的矛盾。

### 8.4 Other Sanhe cases

先做 SchoolCompatibility：

- IDENTICAL；
- SEMANTIC_EQUIVALENT；
- PROCEDURAL_COMPATIBLE；
- SCHOOL_SPECIFIC；
- CONFLICTING；
- UNKNOWN。

只有 IDENTICAL / SEMANTIC_EQUIVALENT / PROCEDURAL_COMPATIBLE 的 procedure 可帮助 π；
SCHOOL_SPECIFIC / CONFLICTING 永久保留 school attribution。

---

## 9. Knowledge -> Product contract

Knowledge artifact 应逐步支持：

```text
artifact_id
school
source_ref
semantic_type

membership
activation
relation
interaction
ordinal
effect_target
scope
exceptions

epistemic_status
allowed_use
```

Product 认可的 allowed_use 至少包括：

- EXECUTABLE；
- SEMANTIC_ONLY；
- RETRIEVAL_ONLY；
- CASE_SUPPORT_ONLY；
- BLOCKED。

Product 只能：
- 消费合格 artifact；
- fail closed；
- 生成 KnowledgeGapReport。

Product 不得：
- 发明 source meaning；
- 自动解除 blocker；
- 将 empirical mismatch 回写 canonical。

---

## 10. Evaluation architecture

### Benchmark A — Canonical Fidelity

回答：
> 是否忠实实现 source-reviewed Zhongzhou knowledge？

测：
- rule activation；
- source provenance；
- response fidelity；
- conflict preservation；
- unsupported inference；
- deterministic replay。

### Benchmark B — Expert Method Fidelity

回答：
> 是否学会专家如何组织和调用知识？

测：
- critical evidence recall；
- wrong-evidence rate；
- next-action quality；
- branch selection；
- time-depth decision；
- cross-palace decision；
- stop/abstention quality；
- trace partial-order compatibility。

### Benchmark C — Prospective Predictive Validity

回答：
> 在现实世界里是否有可重复的增量预测价值？

必须 blind / prospective。
可用：
- Brier score；
- log loss；
- calibration；
- survival/event metrics；
- coverage at confidence；
- incremental predictive value。

### Benchmark D — Cross-School Robustness

回答：
> π 学到的是通用三合式 procedural intelligence，还是王亭之个体习惯？

只评估 method transfer，不覆盖 school-specific canonical truth。

**A/B 成功绝不等于 C 成功。**

---

## 11. Current work: NOW

当前 Product critical path 冻结为：

### NOW-0 — State / architecture freeze
- Product v0.4 roadmap；
- Product state recovery；
- Career NATAL 190 作为 first vertical slice 足够；
- 暂停把继续增加 Career NATAL 数量作为 Product 主 KPI。

### NOW-1 — Method contracts
定义：
- CaseBundle；
- ExpertReasoningGraph；
- InferenceTrace；
- MethodPattern；
- SchoolCompatibility。

### NOW-2 — Wang expert demonstration corpus
- 全部王亭之案例结构化；
- 先 blind machine replay；
- 再 reveal expert trace；
- error attribution；
- 10-fold LOCO。

### NOW-3 — Method Policy v0.1
首选：
- Case-Based Reasoning；
- deterministic / heuristic planner；
- source-explicit procedural rules。

暂不 fine-tune。

### NOW-4 — Response adapter
- 消费 Knowledge Response Semantics；
- preserve membership/activation/relation/interaction/ordinal；
- semantic-only remains non-executable；
- blocked remains blocked。

### NOW-5 — Response Corpus dependency
Knowledge 侧逐步提供 source-backed 本质 × 运限 response records。
Product 不再把“在 Career rows 中搜索 time_layer”当成唯一 temporal knowledge source。

### NOW-6 — PL3-R Response Compiler v0.1
只做：
- Natal Essence；
- Decade；
- Year；
- symbolic τ_t；
- provenance；
- conflict；
- UNKNOWN。

### NOW-7 — M0 manifestation candidates
只输出 source-supported possibility，不输出 probability。

### NOW-8 — Fidelity benchmarks
- Benchmark A；
- Benchmark B；
- Benchmark D 的初版。

### NOW-9 — Forecast Ledger
第一条 N -> E -> τ -> M0 vertical slice 可运行即开始 prospective locking。

---

## 12. Future architecture: LATER

只有 NOW 主线稳定以后进入：

### FUTURE-1 — Personal State Observer
- X_t / b_t 分离；
- deterministic state updater；
- missingness/conflict；
- simple Bayesian belief。

### FUTURE-2 — Contextual Manifestation M1
```text
M1 = f(M0, X_t, b_t, A_t, C_t)
```

### FUTURE-3 — Prospective Blind Benchmark
冻结 prediction cutoff、target window、model version、forbidden leakage。

### FUTURE-4 — Empirical calibration
依次：
1. frequency baseline；
2. GLM / multinomial / ordinal；
3. survival / event-history（数据定义满足时）；
4. hierarchical Bayesian。

### FUTURE-5 — State-space / observer
只有纵向数据证明需要时再引入：
- dynamic Bayesian model；
- state-space observer；
- particle / neural methods later。

### FUTURE-6 — Multi-school production
- Zhongzhou canonical core；
- Qintian / Heluo / other school adapters；
- explicit school attribution；
- conflict preserving comparison。

### FUTURE-7 — Advanced ML
只有 simpler baseline 有稳定 held-out improvement 后考虑：
- MoE；
- GNN；
- neural state-space。

### FUTURE-8 — Causal / decision support
只有因果识别、校准和 policy evaluation 都达标后：
- causal scenario analysis；
- MPC；
- offline RL。

---

## 13. AI method order

```text
Symbolic deterministic
-> Case-Based Reasoning
-> LLM Planner + Symbolic Verifier
-> Process Mining / ILP / rule induction
-> interpretable statistics
-> hierarchical Bayesian
-> dynamic Bayesian / state space
-> neural residual / graph / MoE if justified
-> causal decision support
-> MPC / offline RL last
```

每次复杂化必须：
- 有 simpler baseline；
- 有 held-out improvement；
- 有 calibration comparison；
- 有 traceability audit。

---

## 14. LLM authority

LLM 可以：
- source/case candidate extraction；
- retrieval query generation；
- next-step proposal；
- clarification；
- trace summarization；
- EvidencePackage verbalization。

LLM 不可以：
- 创造 canonical rule；
- 把 GROUP 默认解释成 ANY/ALL；
- 发明数值权重或概率；
- 直接修改 N / Kr；
- 把 case demonstration 自动升级为 source-explicit rule；
- 覆盖 symbolic verifier。

---

## 15. Forecast Ledger

当 source-only vertical slice 首次可运行，即保存：

```text
forecast_id
information_cutoff
chart_version
knowledge_version
method_policy_version
model_version
mode
target
window
prediction
abstention
later_observation
evaluation
```

预测生成后不可 retroactively 修改，只能追加评价。

---

## Risks and Failure Modes

主要风险：
- 把案例记忆误当成方法学习；
- 把其他流派的语义污染到中州 canonical core；
- 把 Response Semantics compatibility 误当成 execution eligibility；
- 让 LLM planner 越权成为 truth engine；
- 把 expert-case fidelity 误报成现实预测有效；
- 在符号垂直链未跑通前过早建设 Bayesian/neural/causal/control 层。

控制方式：source provenance、allowed-use、school namespace、canonical verifier、LOCO/cross-school benchmark、Forecast Ledger 与 stage gate。

## Test Plan

除现有 deterministic regression 外，增加：

### Metamorphic tests

- same E_t + different N -> τ should be allowed/expected to differ；
- same N + different E_t -> τ changes, N unchanged；
- remove required evidence -> confidence decreases / abstains；
- semantic-only artifact never creates executable effect；
- other-school conflicting rule never mutates Zhongzhou output；
- personalized feedback never mutates canonical Natal Essence。

---

## 17. Product maturity claims

分别报告：

```text
framework ready
canonical content ready
method fidelity validated
source fidelity validated
prospective prediction validated
empirically calibrated
personalized
production ready
```

禁止用 schema / interface 存在冒充产品能力完成。

---

## Migration Plan

本 Proposal 首次只修改：
- Product authoritative roadmap；
- Product phase execution plan；
- Product recovery state；
- Decision Log；
- governance contract tests。

不修改 Product runtime 或 Knowledge canonical artifacts。

后续实现必须拆成 PRODUCT_ONLY bounded Issues。

---

## Rollback Plan

回滚本 Proposal 实施 PR 即恢复 v0.3。
由于本 Proposal 不修改 runtime / canonical data，因此 rollback 不需迁移用户数据或知识规则。

---

## Graduation Criteria

满足全部条件：
- Product v0.4 成为 authoritative roadmap；
- NOW / FUTURE 边界清楚；
- Kc / Kr / π / θ / b 永久隔离；
- τ_t 成为正式 response intermediate；
- Wang-10 LOCO 被正式冻结；
- other-Sanhe method-only compatibility boundary 被冻结；
-四类 benchmark 被定义；
- Forecast Ledger 前置；
- Product state 不再引用已完成 #416/#418；
- governance validation PASS。

---

## Human Gate

PI 于 2026-10-20 在完整架构讨论后明确要求将该设计和安排写入 Git。

该批准解释为：
- 批准 Product v0.4 架构方向；
- 批准当前与未来工作重新排序；
- 不批准任何未审 source meaning；
- 不批准把 expert cases 当现实概率 ground truth；
- 不批准越过后续 Product Issue / validation 直接声称能力成熟。

---

## Decision

**APPROVED.**

Product 的近期关键目标由“继续横向积累更多 Career NATAL rules”转为：

```text
Natal Essence
-> Decade/Year Environment
-> source-grounded ResponseProfile
-> source-supported Manifestation Candidates
```

并增加 Expert Reasoning Policy π，使系统能够学习“如何调用知识”，同时仍由 canonical symbolic layer 决定“哪些知识是真的、哪些 effect 合法”。

## 23. Implementation history

- 2026-10-20：Issue #425 建立；PI 指令记录为 R3 Human Gate approval。
- 2026-10-20：PR #427 实施 Product v0.4 roadmap、execution plan、state recovery、decision record 与 governance contract tests。

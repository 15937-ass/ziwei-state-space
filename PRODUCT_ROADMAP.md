# 产品化路线图 — Product-First Program v0.4

状态：ACTIVE  
生效日期：2026-10-20  
替代：Product-First Program v0.3  
批准：Proposal #425 / PI Human Gate

说明：若 `product/PRODUCT_FUTURE_WORKPLAN_v0.1.md` 与本路线图或 `product/phases/PRODUCT_VNEXT_EXECUTION_PLAN_v0.1.md` 冲突，以 v0.4 路线图与新执行计划为准；旧 workplan 保留作历史参考，后续由 PRODUCT_ONLY work unit 清理或替换。

## 0. v0.4 的核心调整

v0.4 不推翻 PL1/PL2，也不否定 v0.3 的动态状态空间方向。它解决的是 v0.3 之后暴露出的三个关键缺口：

1. Product 不能继续用“累计更多 NATAL rules”代替能力层推进；
2. Temporal Environment 与“原局对时间环境的反应”必须拆开；
3. 系统除了学习“知识是什么”，还必须正式建模“专家如何调用知识”。

因此 Product 由：

~~~text
chart -> rules -> inference -> answer
~~~

进一步升级为：

~~~text
Source-grounded Canonical Knowledge
+ Dynamic Response
+ Expert Reasoning Policy
+ Case Memory
+ Empirical Calibration
+ Personal State
~~~

核心链重新冻结为：

~~~text
Birth/Chart
-> Canonical Signal Runtime
-> Natal Essence N
-> Temporal Environment E_t
-> ResponseProfile τ_t
-> Canonical Manifestation Candidates M0
-> Personal/Contextual Routing M1
-> Empirical Calibration
-> EvidencePackage
-> LLM/UI
~~~

其中 Expert Reasoning Policy π 横跨 N / E / τ / M0 的推理搜索过程，只决定“下一步看什么”，不拥有 canonical truth。

---

## 1. 五个永久隔离对象

### Kc — Canonical declarative knowledge

保存传统知识中“是什么”：
- star/system identities；
- palace structure；
- transformations；
- modifiers；
- relations；
- projection；
- named structures；
- explicit constraints。

经验数据不得改写 Kc。

### Kr — Canonical response knowledge

保存传统知识中“遇到某环境如何反应”：
- activation；
- strengthen；
- weaken；
- transform；
- gate；
- ordinal relation；
- effect target；
- scope；
- exception。

Kr 必须来自 source-reviewed evidence；Response Semantics compatibility 本身不等于 executable。

### π — Inference policy / procedural knowledge

回答：
- 先看哪里；
- 下一步看什么；
- 哪些证据优先；
- 何时跨宫；
- 何时从大限进入流年；
- 何时需要更细时间层；
- 何时停止；
- 何时 abstain。

π 可由 source-explicit method、expert demonstrations、Case-Based Reasoning、process mining / ILP 等逐步形成。

π 不拥有 rule truth。

### θ — Empirical calibration parameters

保存：
- manifestation frequency；
- conditional risk/hazard；
- context effects；
- interaction strength；
- cohort effects；
- calibrated uncertainty。

θ 可训练、可版本化、可回滚，但与 Kc/Kr 物理和语义隔离。

### b — Individual state belief

保存系统对某个具体人的现实状态估计。

~~~text
X_t = real/acquired state
b_t = system belief about X_t
~~~

X_t 与 b_t 不等价。

---

## 2. 三类知识 + 一类方法资产

Product 消费的传统知识明确拆为：

~~~text
K_signal
  静态结构 / 条件 / projection

K_response
  本质 × 环境 -> response

K_manifest
  response -> source-supported manifestation candidate

K_method
  专家如何组织和调用这些知识
~~~

K_signal / K_response / K_manifest 的 canonical truth 由 Knowledge lane 管理。

K_method 中只有明确 source-explicit 的方法原则可视为 canonical procedural knowledge；其他案例归纳必须保留 epistemic status。

---

## 3. Epistemic / allowed-use contract

方法与案例相关内容至少区分：

~~~text
SOURCE_EXPLICIT
SOURCE_DEMONSTRATED
RECONSTRUCTED
INDUCED
EMPIRICALLY_VALIDATED
~~~

Knowledge/Product artifact 的 allowed use 至少区分：

~~~text
EXECUTABLE
SEMANTIC_ONLY
RETRIEVAL_ONLY
CASE_SUPPORT_ONLY
BLOCKED
~~~

硬规则：
- SEMANTIC_ONLY 不产生 runtime effect；
- BLOCKED 不产生 runtime effect；
- case demonstration 不自动升级为 canonical rule；
- empirical mismatch 只能触发 KnowledgeGapReport，不能静默修改 source truth。

---

## 4. Product 六层架构

### L0 — Source & Provenance Layer

保存：
- school；
- author；
- source artifact；
- source span；
- artifact type；
- source/review status；
- allowed use；
- version。

### L1 — Canonical Knowledge Layer

承载：
- K_signal；
- K_response；
- K_manifest。

中州派保持 canonical core。

### L2 — Deterministic Symbolic Layer

~~~text
Birth input
-> deterministic chart
-> canonical signal runtime
-> Natal Essence Graph N
-> Temporal Environment E_t
~~~

N 是原局本质，E_t 是 target-time environment。

### L3 — Expert Reasoning Layer

~~~text
Expert Case Bank
+ Case Retriever
+ Procedural KB
+ Inference Policy π
+ Canonical Verifier
~~~

LLM 可以提议下一步，但不能自行验证自己提出的规则含义。

### L4 — Dynamic Response Layer

~~~text
τ_t = R_K(N, E_t)
~~~

第一代 ResponseProfile 必须 sparse / symbolic / source-traceable。

### L5 — Reality / Empirical Layer

~~~text
X_t
b_t
A_t
C_t
θ
~~~

负责现实状态、行动、外部环境与经验校准。

### L6 — Product / Explanation Layer

EvidencePackage 驱动：
- ordinary mode；
- advanced mode；
- expert/debug mode；
- contrastive explanation；
- uncertainty；
- abstention。

---

## 5. 统一数学接口

### 5.1 Natal Essence

~~~text
N = Kc(B)
~~~

B 是出生资料和 deterministic chart。

同一 knowledge version 下：
- N deterministic；
- feedback-free；
- 不被现实历史重写。

### 5.2 Temporal Environment

~~~text
E_t = T(B, t)
~~~

E_t 描述：
- active decade/year/month/... facts；
- transformations；
- relation facts；
- temporal context。

E_t 不等于现实事件。

### 5.3 Response

~~~text
τ_t = R_Kr(N, E_t)
~~~

τ_t 表示：
- activated tendency；
- strengthen/weaken；
- transform；
- gate；
- conflict；
- ordinal constraint；
- effect target；
- unknown。

第一阶段不要求 numeric magnitude。

### 5.4 Canonical Manifestation

~~~text
M0_t = G_K(τ_t)
~~~

M0 只表示 source-supported possibility。

### 5.5 Acquired state and belief

未来：

~~~text
X_(t+1) ~ F_theta(X_t, N, τ_t, A_t, C_t)
~~~

系统实际维护：

~~~text
b_t = P(X_t | observations up to t)
~~~

初期优先 deterministic updater，再考虑 simple Bayesian。

### 5.6 Contextual Manifestation

未来：

~~~text
M1_t ~ P(M | M0_t, X_t, b_t, A_t, C_t, θ)
~~~

必须永久区分：

~~~text
SOURCE_SUPPORTED_POSSIBILITY
EMPIRICALLY_CALIBRATED_PROBABILITY
PERSONALIZED_POSTERIOR
~~~

---

## 6. Expert Reasoning Program

### 6.1 CaseBundle

每个 expert case 拆为：

~~~text
source/provenance
ChartSnapshot
target question/time
information available before inference
ExpertReasoningGraph
expert conclusion
known outcome if supplied
~~~

### 6.2 ExpertReasoningGraph

存储可审计动作图，而非不可审计自由文本思维过程。

核心动作可包括：
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

评估使用 DAG / partial-order compatibility，不要求逐字逐步复刻作者。

### 6.3 Wang Tingzhi cases

王亭之约 10 个高质量完整案例：
- 全部最终进入 Expert Case Bank；
- 不拿来估现实 event probability；
- 不做普通 train/test 固定切分；
- 使用 10-fold Leave-One-Case-Out Expert Replay。

每一 fold：

~~~text
9 cases -> method induction / retrieval
1 case  -> unseen blind expert replay
~~~

这样每例都能参与学习，同时每例至少一次真正未见测试。

### 6.4 Other Sanhe cases

其他三合派案例用于方法泛化与 cross-school robustness，先分类：

~~~text
IDENTICAL
SEMANTIC_EQUIVALENT
PROCEDURAL_COMPATIBLE
SCHOOL_SPECIFIC
CONFLICTING
UNKNOWN
~~~

只有兼容的 procedural pattern 可 regularize π。

SCHOOL_SPECIFIC / CONFLICTING 永久保留 school namespace，不反写中州 core。

---

## 7. Temporal hierarchy

第一阶段正式冻结：

~~~text
Natal
-> Decade
-> Year
-> Month only when triggered
-> Day/Hour later
~~~

理由：
- first vertical slice 先建立最重要的长期/年度交涉；
- 避免时间层组合爆炸；
- 防止在没有上层候选信号时无目的细搜。

Product 即使已经能生成 month/day/hour facts，也不代表 inference policy 现在必须全部使用。

---

## 8. PL stages v0.4

### PL1 — Chart Trust
状态：**COMPLETE / FROZEN**

保持 deterministic chart、calendar boundary、multi-engine diff 和 ambiguity registry。

### PL2 — Executable Canonical Knowledge
状态：**ACTIVE / PARTIAL CONTENT**

目标：
- source span -> reviewed artifact -> executable/semantic status -> trace；
- fail closed；
- 不发明 numeric weight / threshold。

### PL3-N — Natal Essence Engine
状态：**PARTIAL / USABLE FOR FIRST VERTICAL SLICE**

从 flat rule collection 进一步升级为：

~~~text
Star/System Core
-> Essence Mode
-> Palace Essence
-> Domain Projection
~~~

Career 190 NATAL rules 足够支持第一条动态 vertical slice。
继续增加 Career 数量不再是当前 Product critical-path KPI。

### PL3-T — Temporal Environment
状态：**INFRASTRUCTURE READY**

负责 E_t，不负责把 E_t 直接变成 event。

### PL3-METHOD — Expert Reasoning
状态：**NEW / CURRENT CRITICAL PATH**

目标：
- CaseBundle；
- ExpertReasoningGraph；
- InferenceTrace；
- MethodPattern；
- SchoolCompatibility；
- Case-Based Retrieval；
- π v0.1；
- Wang LOCO benchmark。

### PL3-R — Response Engine
状态：**NEW / CURRENT CRITICAL PATH**

~~~text
N + E_t + Kr -> τ_t
~~~

第一版只做 decade + year。

### PL3-M0 — Canonical Manifestation Candidates
状态：**NEW / DEPENDS ON RESPONSE + MANIFEST KNOWLEDGE**

输出 SOURCE_SUPPORTED_POSSIBILITY，不输出经验概率。

### PL3-S — Personal State Observer
状态：**FUTURE AFTER SOURCE-GROUNDED VERTICAL SLICE**

实现 X_t / b_t、missingness、observation provenance。

### PL3-M1 — Contextual Manifestation Router
状态：**FUTURE**

结合 M0 + state + action + context + calibration。

### PL4-A — Canonical Fidelity
测 source implementation fidelity。

### PL4-M — Expert Method Fidelity
新增长期 benchmark：
- evidence selection；
- next action；
- branch；
- time depth；
- stop/abstain；
- reasoning graph compatibility。

### PL4-B — Predictive Blind Benchmark
严格 prospective/unseen，和 PL4-A/PL4-M 分开。

### PL5 — Empirical Calibration
顺序：
- frequency baseline；
- GLM / multinomial / ordinal；
- survival/event history where valid；
- hierarchical Bayesian；
- state-space only if justified。

### PL6 — Product UX
继续普通/高级/Expert 三层 UI，并显示 evidence type 和 uncertainty source。

### PL7 — Longitudinal Data Flywheel
继续并行。

第一条 N -> E -> τ -> M0 可运行后，立即启动 Forecast Ledger。

### PL8 — Multi-school / Production
中州派为 core；其他学校 adapter 化、source-attributed、conflict-preserving。

### PL9 — Conditional Decision Support
仅在 calibration / causal readiness 达标后进入。

---

## 9. NOW：当前真正要做的

当前 Product 主线：

~~~text
NOW-0  v0.4 architecture/state freeze
   ↓
NOW-1  Expert Case / Trace / Method contracts
   ↓
NOW-2  Wang expert cases structured + LOCO harness
   ↓
NOW-3  CBR + heuristic/symbolic Method Policy π v0.1
   ↓
NOW-4  Response Semantics fail-closed Product adapter
   ↓
NOW-5  Source-backed response corpus dependency
   ↓
NOW-5A Product Knowledge Dependency Control
       KIB + active lock + semantic impact + promotion
   ↓
NOW-6  PL3-R Decade/Year Response Compiler -> τ_t
   ↓
NOW-7  PL3-M0 source-supported manifestation candidates
   ↓
NOW-8  Canonical + Expert Method fidelity benchmark
   ↓
NOW-9  Forecast Ledger activation
~~~

### 当前明确不把这些作为主线
- 再把 Career NATAL 从 190 持续扩到 300/500；
- neural fine-tuning；
- GNN；
- neural state-space；
- particle filter；
- RL；
- MPC；
- 现实概率声称。

---

## 10. FUTURE：以后再进入的架构

当 source-grounded vertical slice 稳定后：

~~~text
FUTURE-1  X_t / b_t Personal State
FUTURE-2  Contextual M1 Router
FUTURE-3  Prospective Blind Benchmark
FUTURE-4  Interpretable Empirical Calibration
FUTURE-5  Hierarchical Bayesian
FUTURE-6  Dynamic State-Space / Observer
FUTURE-7  Multi-school Production
FUTURE-8  Advanced ML
FUTURE-9  Causal / MPC / Offline RL
~~~

每一层必须通过前一层的 stop/go gate。

---

## 11. Knowledge -> Product contract

Knowledge 侧继续拥有 canonical source interpretation。

Product 需要 Knowledge artifact 至少携带：
- artifact id；
- school；
- source；
- semantic type；
- membership；
- activation；
- relation；
- interaction；
- ordinal；
- effect target；
- scope；
- exceptions；
- epistemic status；
- allowed use。

Product 可创建 KnowledgeGapReport，但不能跨 lane 自行“补全理论”。

当前 Response Semantics 工作对 Product 的意义：
- 提供更细的表达语言；
- 重新分类 blocker；
- 不是自动 execution unlock。

### 11.1 Knowledge dependency / promotion contract

Product 不直接把 Knowledge `main` 当作可变的生产依赖。

正式消费路径冻结为：

~~~text
Knowledge main
-> Candidate Knowledge Input Bundle (KIB)
-> semantic diff / impact report
-> affected Product rebuild / recompile / replay / rematerialize
-> validation
-> promotion
-> Active Product Knowledge Lock
~~~

KIB 至少按下列组件分离：

~~~text
K_signal
K_response
K_manifest
K_method
~~~

每个组件至少记录：
- artifact refs；
- source commit；
- schema/contract version；
- artifact digest；
- semantic digest。

`knowledge_version` 可继续作为人可读标签，但不能单独充当内容身份。

永久规则：
- Knowledge merge 不自动改变 active Product；
- Product frozen baseline 必须能够由 lock/digest 机器验证；
- 无关 Knowledge 改动不得强迫全 Product rebuild；
- semantic change 只沿显式依赖图传播；
- Product 不得静默拼接 incompatible Knowledge semantics；
- Candidate 只有通过相关 fidelity/regression/benchmark 后才能 promotion；
- failed candidate 不改变 active lock；
- 历史 forecast / dataset / model / evidence artifact 保留原始 Knowledge lineage，不事后覆写。

Impact 至少区分：

~~~text
NO_RUNTIME_EFFECT
PROVENANCE_REVALIDATION
READINESS_REBUILD
SYMBOLIC_RECOMPILE
METHOD_REPLAY
MANIFESTATION_REBUILD
DATASET_REMATERIALIZE
RETRAIN_OR_RECALIBRATE
MIGRATION_REQUIRED
~~~

在 PL5 前必须建立 dataset/model lineage gate；不同 KIB 产生的 feature/label 不得无 migration 静默混合。

详细设计：`governance/proposals/491-product-knowledge-dependency-promotion.md`。

---

## 12. 四类 benchmark

### A — Canonical Fidelity
问题：有没有忠实实现中州派 source？

### B — Expert Method Fidelity
问题：有没有学会专家如何组织、筛选和调用知识？

### C — Prospective Predictive Validity
问题：有没有现实、可重复、out-of-sample 的增量预测价值？

### D — Cross-School Robustness
问题：π 学到的是可迁移 procedure，还是只记住 Wang / Zhongzhou 的局部习惯？

硬边界：

~~~text
A/B/D success != C success
~~~

---

## 13. Forecast Ledger

第一条 source-only vertical slice 可运行后即启用。

至少锁定：
- forecast_id；
- information cutoff；
- chart version；
- knowledge version；
- method-policy version；
- model version；
- mode；
- target；
- window；
- prediction；
- abstention；
- later observation；
- evaluation。

历史 prediction 不可事后改写。

---

## 14. AI / 学界方法启用顺序

~~~text
Symbolic deterministic
-> Case-Based Reasoning
-> heuristic/deterministic planner
-> LLM planner + symbolic verifier
-> process mining / ILP / rule induction
-> interpretable statistical baseline
-> hierarchical Bayesian
-> dynamic Bayesian / state-space
-> neural residual / graph / MoE if justified
-> causal evaluation
-> MPC / offline RL last
~~~

复杂模型进入条件：
- enough data；
- simpler baseline；
- held-out gain；
- calibration gain；
- traceability audit。

---

## 15. LLM 角色

LLM 可以：
- case/source candidate extraction；
- retrieval query；
- next-action proposal；
- clarification；
- error attribution candidate；
- EvidencePackage verbalization；
- contrastive explanation。

LLM 不可以：
- 创造 canonical rule；
- 解除 blocker；
- 自行把 GROUP 解释成 ANY/ALL；
- 发明 numeric qi weights；
- 发明 event probability；
- 修改 N/Kr；
- 用 expert case 自动覆盖 source meaning；
- 隐藏 uncertainty/conflict。

---

## 16. Testing strategy

除 conventional regression 外，引入 metamorphic tests：

- same E_t + different N -> τ 可以/应当不同；
- same N + different E_t -> τ 改变，但 N 不变；
- 删除关键 evidence -> confidence 降低或 abstain；
- semantic-only artifact 永不产生 executable effect；
- other-school conflict 永不修改 Zhongzhou output；
- personal feedback 永不修改 canonical Natal Essence。

---

## 17. Progress metrics

当前阶段默认报告：
- structured expert cases / total；
- LOCO folds；
- method action/evidence metrics；
- response artifacts：executable / semantic-only / blocked；
- validated N+E->τ fixtures；
- validated τ->M0 mappings；
- completed vertical slices；
- unsupported inference rate；
- abstention quality。

不再用“Career rule 总数”单独代表 Product 进度。

---

## 18. Human Gate

必须重新请求 PI 的情况包括：
- 新增 primitive qi；
- 改变 N / E / τ 边界；
- 允许 empirical feedback 修改 canonical truth；
- 将 induced procedure 宣称为 Zhongzhou source-explicit；
- 其他流派规则进入 Zhongzhou core；
- 新 universal manifestation family；
- source 未给出的 fixed numeric effect；
- 黑盒模型替代 canonical verifier；
- correlation 升级为 causal action recommendation。

---

## 19. 当前恢复点

Product #416 / PR #418 已完成 Career NATAL 首条 vertical slice 所需基线；Product #431/#435、#441/#444、#453/#455、#462/#464 已完成 expert-method contract、Wang case corpus、Method Policy 与 Response Semantics adapter；Product #482 / PR #484 已完成 NOW-5 Product-side Response Corpus ingestion/readiness。

#482 的关键结论是：source temporal material 已存在，但 frozen acceptance baseline 上 compiler-ready canonical Kr = 0；因此 NOW-6 不得通过 Product 猜测语义硬启动。

Proposal #491 之后，下一推荐 Product work unit：

**PRODUCT_KNOWLEDGE_LOCK_V0_1**

随后：
- PRODUCT_KNOWLEDGE_IMPACT_V0_1；
- Wang blind evidence materialization 可并行推进其独立依赖；
- Knowledge 提供 compiler-ready Kr 后进入 PL3-R Response Compiler；
- 再进入 M0 vertical slice。

Product 只有在 active KIB/lock 可机器验证后，才允许把更新后的 Knowledge candidate promotion 到当前 runtime。

详细执行顺序见：

product/phases/PRODUCT_VNEXT_EXECUTION_PLAN_v0.1.md

---

## 20. 产品最终定位

> 一个以中州派 source-grounded canonical knowledge 为固定知识核心，以本质—时间环境—反应为动态机制，以专家案例学习推理策略，以前瞻现实数据独立校准预测价值，并在后期支持个体状态估计与条件决策分析的可审计神经符号紫微斗数研究与产品系统。

简化技术表达：

~~~text
Canonical Symbolic Knowledge
+ Expert Reasoning Policy
+ Dynamic Response Model
+ Case Memory
+ Prospective Calibration
+ Personal State Estimation
+ AI Interface
~~~

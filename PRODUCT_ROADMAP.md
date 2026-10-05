# 产品化路线图 — Product-First Program v0.3

状态：ACTIVE  
生效日期：2026-10-05  
替代：Product-First Program v0.2

## 0. 本版本的核心调整

## 0.1 并行状态治理

从 v0.3 起，产品侧使用 \`product/PRODUCT_STATE.yaml\` 保存产品 work-unit 指针。

每个产品会话必须按顺序读取：

\`\`\`text
PROJECT_STATE.yaml
-> product/PRODUCT_STATE.yaml
\`\`\`

其中：
- 顶层 \`PROJECT_STATE.yaml\` 继续拥有知识侧 corpus / gate / repository 总状态；
- \`product/PRODUCT_STATE.yaml\` 拥有产品阶段、产品下一工作单元和产品边界；
- 产品 feature PR 默认不再修改顶层 \`PROJECT_STATE.yaml\`，避免与持续推进的 WP05 source-review checkpoint 发生无意义合并冲突；
- 只有需要跨轨冻结的重大状态变化，才单独执行 coordinated state-sync。


v0.3 不推翻 PL1/PL2 已完成工作，而是重新冻结 PL3 之后的产品目标。

旧路线较接近：

\`\`\`text
chart -> rules -> inference -> answer
\`\`\`

新路线统一为：

\`\`\`text
birth/chart facts
    -> canonical natal prior
    -> temporal environment
    -> acquired personal state
    -> manifestation routing
    -> probabilistic calibration
    -> feedback / posterior update
    -> conditional scenario / decision support
\`\`\`

关键边界：

1. **原局层**只输出由命盘与 canonical knowledge 决定的先天结构、性质与倾向，不依赖用户现实反馈；
2. **大限/流年层**表示时变环境与激活条件，不直接等同现实事件；
3. **现实反馈**更新 acquired state、个体 posterior 与经验参数，不得反写 canonical natal truth；
4. **应象概率**属于 empirical calibration，不属于传统知识本体；
5. **行动选择**是 control input，不是 noise；
6. **外部不可控条件**属于 exogenous context / disturbance；
7. **LLM**只负责结构化反馈解析、问答交互与表达，不拥有 canonical rule selection 或概率拍板权。

---

## 1. 项目三层永久隔离

### Layer A — Canonical Traditional Knowledge

来源：
- 中州派 approved source corpus；
- reviewed atomic rules；
- star cores / sixty-system modes；
- modifier / transformation / palace / temporal operators；
- source-backed named structures。

性质：

\`\`\`text
immutable by empirical learning
\`\`\`

案例数据或用户反馈发现异常时，只能触发知识缺口回源复核，不能直接改写 Layer A。

### Layer B — Empirical Calibration

保存：
- manifestation frequencies；
- conditional risks / hazards；
- interaction strengths；
- cohort effects；
- calibrated parameter intervals/posteriors；
- model versions。

性质：
- 可训练；
- 可版本化；
- 可回滚；
- 必须与 Layer A 物理和语义隔离。

### Layer C — Personal Adaptation

保存：
- 当前现实状态；
- 已发生事件；
- 用户行为与计划；
- exposure / opportunity；
- 个体 posterior；
- individual random effects / personalization state。

性质：
- 只影响当前个体；
- 不自动升级为总体经验；
- 更不能升级为 canonical traditional rule。

---

## 2. 统一数学接口

### 2.1 原局先验

\`\`\`text
N = K(B)
\`\`\`

- B：出生资料与确定性排盘；
- K：canonical symbolic engine；
- N：Natal Prior / 先天气核与结构状态。

N 在同一知识版本下必须 deterministic。

### 2.2 时间环境

\`\`\`text
E_t = T(B, t)
\`\`\`

E_t 由大限、流年、流月等时间层结构产生，是已知时变 context，不是现实结果。

### 2.3 动态现实状态

使用 augmented state，避免另立一个无法定义的 history 变量：

\`\`\`text
S_(t+1) ~ F_theta(S_t, N, E_t, A_t, C_t)
\`\`\`

- S_t：当前现实/获得性状态，包含对未来预测必要的历史摘要；
- A_t：本人选择/行动；
- C_t：外部环境、暴露机会、对手方/他人行为等上下文；
- theta：待辨识参数。

若未来发现 S_t 不能满足 Markov sufficiency，再显式升级 semi-Markov / history-dependent model，不在 v0.3 先行假定。

### 2.4 应象路由

\`\`\`text
M_t ~ P_phi(M | N, E_t, S_t, A_t, C_t)
\`\`\`

M_t 表示 manifestation family / channel，不代表宿命唯一结果。

### 2.5 观察与反馈

\`\`\`text
Y_t ~ O_psi(Y | S_t, M_t, C_t)
\`\`\`

现实观察用于更新：

\`\`\`text
P(S_t, theta_person, phi_person | Y_1:t, A_1:t-1, E_1:t)
\`\`\`

但不得更新或重写 N 的 canonical content。

---

## 3. 五类准确性继续保留，并新增第六类

原 v0.2 的五类准确性继续有效：

1. 排盘准确性；
2. 规则还原准确性；
3. 推理一致性；
4. 外部案例准确性；
5. Calibration / Abstention。

新增：

### F. Incremental Predictive Value

必须回答：

> 加入命盘结构后，是否比只知道年龄、职业、婚恋状态等一般背景信息具有额外预测价值？

至少比较：

\`\`\`text
Context-only baseline
vs
Context + Natal
vs
Context + Natal + Temporal
vs
Context + Natal + Temporal + Personal history
\`\`\`

可用指标：
- Brier score / log loss 改善；
- calibration error；
- AUC / ranking（适用时）；
- likelihood ratio / information gain；
- coverage-at-confidence。

禁止用“某象出现者中多少发生某事”替代增量价值评估。

---

## 4. 产品阶段重新编排

## PL1 — Chart Trust Layer

状态：**COMPLETE / FROZEN**

继续维持：
- deterministic chart contract；
- calendar / Zi-hour boundary；
- multi-engine diff；
- ambiguity registry；
- Chart Trust Report。

除新发现 bug 或 source/config conflict 外不重开。

---

## PL2 — Executable Canonical Knowledge

状态：**ACTIVE**

目标：
- source span -> reviewed rule -> condition/operator -> state/projection -> trace；
- 继续 fail closed；
- 不为覆盖率伪造权重、阈值或 universal valence。

当前新增工作单元：

### PL2Q — Human Gate Integration

实现：
- contextual valence/state contract；
- pattern status / pattern scale / pattern integrity 分离；
- BAIGUAN_SUPPORT_PROFILE；
- uncertainty / insufficient-evidence contract；
- regression tests；
- W01 blocker refresh。

注意：
- Human Gate 批准不自动把 8 条 W01 升为 executable；
- 百官 activation criterion 未冻结前不得人工计数判真。

---

## PL3-N — Natal Prior Engine

这是 PL2 后的第一主目标。

输入：
- NormalizedChartSnapshot；
- canonical knowledge version；
- school/config。

输出：
- NatalStateProfile；
- active natal rules；
- star cores；
- system modes；
- palace states；
- named structures；
- cross-palace dependencies；
- source-backed priors / tendencies；
- conflict / ambiguity / confidence；
- complete EvidencePackage。

硬指标：
- feedback-free；
- same input + same knowledge version -> same N；
- 无 LLM 也能完整运行；
- 每个关键状态可回溯 source/rule。

禁止：
- 通过用户现实反馈“校正原局”；
- 使用 empirical outcome frequency 改写 natal truth。

---

## PL3-T — Temporal Environment Engine

输入：

\`\`\`text
NatalStateProfile + target time layer
\`\`\`

输出：

\`\`\`text
TemporalEnvironmentProfile
\`\`\`

内容包括：
- 大限/流年/流月等 active temporal facts；
- temporal transformation / activation；
- 对 natal states 的加强、削弱、转化、触发；
- time-layer conflicts；
- candidate manifestation families（仅 source-supported）。

PL3-T 输出的是**环境与激活状态**，不是“今年必发生 X”。

---

## PL3-S — Personal State Observer

目的：把现实世界的用户状态与命盘状态分开建模。

输入：
- user-reported verified events；
- imported structured records（未来可选）；
- actions / intentions / exposures；
- previous state estimate。

输出：
- AcquiredState；
- state confidence；
- missingness；
- contradictory reports；
- observation provenance。

v0.1 优先：
- deterministic state updater；
- simple Bayesian belief update。

仅在数据形态证明有必要后，再升级：
- Dynamic Bayesian Network；
- particle filter / sequential Monte Carlo；
- neural state-space model。

---

## PL3-M — Manifestation Router MVP

输入：

\`\`\`text
N + E_t + S_t + A_t + C_t
\`\`\`

输出：

\`\`\`text
candidate manifestation channels
+ source support
+ empirical probability if calibrated
+ uncertainty
\`\`\`

v0.1 必须区分：

\`\`\`text
SOURCE_SUPPORTED_POSSIBILITY
EMPIRICALLY_CALIBRATED_PROBABILITY
PERSONALIZED_POSTERIOR
\`\`\`

三者不得混写。

---

## PL4-A — Internal Fidelity Benchmark

测“是否忠实实现中州派”，不测现实世界预测有效性。

指标：
- chart reconstruction；
- canonical rule trace coverage；
- author-reasoning reconstruction；
- temporal-layer fidelity；
- source trace completeness；
- deterministic consistency；
- conflict preservation。

教材案例主要属于此层。

---

## PL4-B — Predictive Blind Benchmark

严格使用未见过现实答案的数据。

必须预注册：
- forecast time；
- prediction target；
- model version；
- available context；
- forbidden leakage；
- observation window。

至少比较：
- population/context-only baseline；
- pure LLM；
- RAG；
- flat rules；
- symbolic natal；
- symbolic natal + temporal；
- calibrated manifestation model；
- personalized model。

Internal fidelity 与 predictive accuracy 永久分开报告。

---

## PL5 — Empirical Calibration Program

### PL5-A Manifestation Frequency Baseline

学习：

\`\`\`text
P(M | Q)
\`\`\`

只作为最简单 baseline。

### PL5-B Context-Conditioned Manifestation

学习：

\`\`\`text
P(M | Q, S, C)
\`\`\`

优先从可解释模型开始：
- logistic / multinomial；
- survival / event-history；
- competing-risks（仅在事件定义满足其统计假设时使用）。

“多个应象通道竞争”可以是产品概念，但只有满足 time-to-event / mutually exclusive risk 定义时才称正式 competing-risks model。

### PL5-C Hierarchical Bayesian Calibration

层级：

\`\`\`text
population
  -> cohort/context
     -> individual
\`\`\`

数据少时强 shrinkage 回总体；
数据增加后才允许个体 posterior 偏离总体。

### PL5-D Incremental Predictive Value

验证：

\`\`\`text
P(Y | context + chart)
vs
P(Y | context)
\`\`\`

只有 chart features 带来稳定 out-of-sample improvement，才可声称其具有增量预测价值。

### PL5-E Causal / Action Analysis

仅在数据和因果假设成熟后启用。

目标：
- 区分 chart association、selection、action、exposure、confounding；
- 不把 observational correlation 冒充“做 X 会改善 Y”。

在因果识别不足时只输出：
- conditional scenario；
- association；
- uncertainty。

不得输出伪因果建议。

---

## PL6 — Product UX

保留三层解释 UI：

1. 普通用户；
2. 高级用户；
3. Expert/Debug。

新增三个运行模式：

### Mode A — Natal Mode
只解释 N，不需要现实反馈。

### Mode B — Blind Forecast Mode
仅使用允许的 chart/time/context 信息，不读取目标期结果，用于研究与 benchmark。

### Mode C — Personalized Forecast Mode
允许加入 S_t / A_t / C_t / past feedback，输出条件化结果。

UI 必须明确标注当前模式，禁止把 Personalized Mode 的高准确度当成 Blind Forecast 能力宣传。

---

## PL7 — Longitudinal Data Flywheel

基础设施立即建设，训练延后到数据质量过关。

数据单位从“单盘 + 一个事件”改为：

\`\`\`text
Person x Time
\`\`\`

每个 observation window 至少支持：
- state_before；
- action；
- exposure / opportunity；
- external context；
- outcome；
- event time / interval；
- severity/intensity；
- EVENT_OCCURRED / EVENT_NOT_OCCURRED / UNKNOWN / CENSORED；
- source/provenance；
- observation confidence；
- linked forecast version。

### 关键数据原则

1. 必须收 negative samples；
2. 必须收“什么也没发生”的 observation window；
3. 历史回顾与前瞻 observation 分开；
4. memorable-event-only 数据不得用于无修正总体概率；
5. outcome coding schema 在预测前冻结；
6. missing-not-at-random 风险必须记录。

---

## PL8 — Multi-school / Production

中州派继续 canonical core。

\`\`\`text
Core Ontology
  ├─ Zhongzhou Adapter
  ├─ Qintian Adapter
  ├─ Heluo Adapter
  └─ future adapters
\`\`\`

跨流派一致可以形成 consensus evidence；
冲突必须保留 school attribution。

其他流派 empirical data 不得静默回写中州派 Layer A。

---

## PL9 — Conditional Scenario & Decision Support

只有在 PL4/PL5 校准达到门槛后进入。

形式：

\`\`\`text
P(S_(t+H), Y_(t:t+H) | current belief, candidate action)
\`\`\`

支持：
- 维持现状；
- 行动 A；
- 行动 B；
- 不同行动约束下的多目标轨迹。

若未来进入 MPC：

\`\`\`text
a* = argmax E[U(trajectory) | belief, constraints]
\`\`\`

但 U 必须由用户目标定义或显式多目标表示，不能把系统自己的“吉”当 universal reward。

健康、法律、金融等高风险领域不得把本系统替代专业判断；这类输出最多作为非专业的情境解释，不提供高风险决策指令。

---

## 5. AI / 控制方法启用顺序

| 阶段 | 首选方法 | 暂不优先 |
|---|---|---|
| PL2–PL3-N | symbolic / rule engine | neural end-to-end |
| PL3-T | hybrid symbolic state-space | black-box predictor |
| PL3-S | deterministic updater + Bayesian belief | particle filter by default |
| PL5-A/B | frequency / GLM / survival baseline | deep neural model |
| PL5-C | hierarchical Bayesian | per-user independent model |
| PL5-E | SCM / causal inference | RL without identification |
| large-data stage | Mixture-of-Experts / graph models / neural SSM | untraceable monolith |
| PL9 | scenario simulation / MPC | “命盘直接给行动命令” |

每引入更复杂模型，必须证明相对简单 baseline 的 out-of-sample 增益。

---

## 6. LLM 角色重新冻结

LLM 可以：
- 解析自然语言现实反馈为候选结构化事件；
- 生成澄清问题；
- verbalize EvidencePackage；
- 做 contrastive explanation；
- 展示 conditional scenarios；
- 帮助人工 source review，但不能自动升级 source status。

LLM 不可以：
- 创造 canonical rule；
- 创造未冻结数值权重；
- 用语言感觉决定 manifestation probability；
- 修改 Natal Prior；
- 隐藏 conflict / uncertainty；
- 把 correlation 改写成 causation。

---

## 7. Human Gate 新触发条件

除既有 G1–G6 / A0–A2 外，下列变化必须 PI Human Gate：

- 新增 primitive qi；
- 改变 natal vs temporal 边界；
- 允许反馈修改 canonical Natal Prior；
- 把 empirical parameter 升级为 canonical rule；
- 定义新的 universal manifestation family；
- 新增跨宫长期记忆或默认 persistence / decay；
- 对 source 未给出的效应指定固定数值；
- 让黑盒 AI 替代 canonical symbolic layer；
- 将关联模型升级为因果行动建议。

普通参数重训、posterior 更新、案例增加、UI 变化，在不越过上述边界时不触发 Human Gate。

---

## 8. 当前执行顺序

### 产品轨

\`\`\`text
PL2Q Human Gate Integration
  -> PL3-N Natal Prior Engine
  -> PL3-T Temporal Environment Engine
  -> PL3-S Personal State Observer
  -> PL3-M Manifestation Router MVP
  -> PL4-A fidelity benchmark
  -> PL4-B predictive blind benchmark
  -> PL5 calibration
  -> PL9 decision support
\`\`\`

### 与数据轨并行

\`\`\`text
Longitudinal schema
  -> prospective collection
  -> quality audit
  -> calibration-ready corpus
\`\`\`

PL7 schema 可提前做，但不得在 quality gate 前把早期反馈当稳定概率真值。

---

## 9. 产品最终定位

> 一个以中州派传统知识为固定先验，以原局气核—时变环境—行为—应象为动态机制，以纵向现实反馈进行概率校准，并支持个体化状态估计与条件轨迹分析的可解释智能紫微斗数系统。

简化技术表达：

\`\`\`text
Symbolic Prior
+ Dynamic State Space
+ Bayesian Calibration
+ Causal Evaluation
+ AI Interface
+ Conditional Decision Support
\`\`\`


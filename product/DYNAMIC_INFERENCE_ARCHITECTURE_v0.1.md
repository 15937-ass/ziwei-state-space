# Dynamic Inference Architecture v0.1

状态：ARCHITECTURE FROZEN FOR IMPLEMENTATION PLANNING  
生效日期：2026-10-05  
适用：中州派 canonical core + product dynamic inference

## 1. 目的

本文件定义原局、时间环境、现实状态、个人行动、外界上下文、应象路由和经验校准之间的边界。

目标不是建立宿命论模型，而是建立：

> **source-grounded symbolic prior + controlled stochastic dynamic model + longitudinal feedback calibration**

---

## 2. 核心对象

### N — Natal Prior

\`\`\`text
N = K(B)
\`\`\`

由出生资料 B 和 canonical symbolic engine K 产生。

包含：
- star/system state；
- named structures；
- palace projections；
- source-backed tendencies；
- conflict/uncertainty。

性质：
- deterministic under same version；
- feedback-independent；
- empirical layer 不可改写。

---

### E_t — Temporal Environment

\`\`\`text
E_t = T(B, t)
\`\`\`

包含：
- 大限/流年/流月等 active temporal facts；
- temporal transformations；
- activation / strengthening / weakening / conversion；
- time-layer conflicts。

E_t 是环境/条件，不是个人本质，也不是结果。

---

### S_t — Augmented Acquired State

现实中的动态状态。

应包含对未来预测必要的历史摘要，例如：
- relationship status；
- career status；
- resource stock / debt state；
- relocation status；
- existing commitments；
- social exposure；
- recent interventions/events；
- durable acquired dispositions（仅有证据时）。

如果某历史变量影响未来，则应被纳入 S_t，而不是另放一个无边界 history bag。

---

### A_t — Action / Choice

本人可控制或部分可控制的行为。

必须区分：
- intent；
- planned action；
- actual action；
- adherence/compliance。

“想谈恋爱”不等于“实际增加社交暴露”。

---

### C_t — External Context

本人不可完全控制的现实条件，包括：
- exposure / opportunity；
- macro context；
- counterpart behavior；
- family/work constraints；
- unexpected events。

对关系、事业等多主体场景，v0.1 将其他人的自主行为作为 structured external context；不急于上升为 stochastic game。

---

### M_t — Manifestation Channel

抽象状态/激活的现实落点。

例如一个 activation 可以：
- 通过 channel A 显化；
- 通过 channel B 显化；
- 暂无明显外显事件。

M_t 必须链接 manifestation ontology。

---

### Y_t — Observation

现实反馈 / 观察证据。

与 external context 不同：

- C_t 参与状态演化；
- Y_t 用于观察和更新模型。

同一现实事件在工程实现中可能同时产生 context record 与 observation record，但两个角色字段必须分开。

---

## 3. 动态模型

### State transition

\`\`\`text
S_(t+1) ~ F_theta(S_t, N, E_t, A_t, C_t)
\`\`\`

### Manifestation routing

\`\`\`text
M_t ~ R_phi(M | S_t, N, E_t, A_t, C_t)
\`\`\`

### Observation

\`\`\`text
Y_t ~ O_psi(Y | S_t, M_t, C_t)
\`\`\`

### Belief update

\`\`\`text
b_t = P(S_t, theta_person, phi_person | Y_1:t, A_1:t-1, E_1:t, C_1:t)
\`\`\`

v0.1 不强制具体 filter。

优先级：
1. deterministic updater；
2. Bayesian discrete/continuous belief；
3. Dynamic Bayesian Network / factor graph；
4. particle filter，仅在 nonlinear / non-Gaussian / multimodal posterior 需要时采用；
5. neural state-space，仅在大数据阶段采用。

---

## 4. 原局与反馈的硬边界

允许：

\`\`\`text
feedback -> update S_t
feedback -> update individual posterior
feedback -> update empirical calibration
\`\`\`

禁止：

\`\`\`text
feedback -> rewrite N
feedback -> change source rule truth
feedback -> change historical source span
\`\`\`

如果长期数据与 canonical rule 表面冲突：
1. 记录 empirical mismatch；
2. 检查 confound / label / exposure / selection；
3. 创建 KNOWLEDGE_GAP_REPORT；
4. 回源审查；
5. 只有 source review / Human Gate 才能改变 canonical layer。

---

## 5. 应象概率的三种层级

系统必须区分：

### Level 1 — Source-supported possibility

\`\`\`text
某 activation 在传统资料中允许投影到某 manifestation family
\`\`\`

不带概率。

### Level 2 — Population calibrated probability

\`\`\`text
P(M | Q, context)
\`\`\`

来自经过质量控制的总体/群体数据。

### Level 3 — Personalized posterior

\`\`\`text
P(M | Q, context, individual history)
\`\`\`

在总体先验基础上结合当前用户纵向数据更新。

不得把 Level 1 的文学语气“多主/往往/易”未经建模直接显示成 Level 2 数字概率。

---

## 6. “铁口直断”的现代定义

产品不把“铁口直断”定义为 100% 决定论。

形式化为：

\`\`\`text
high-confidence calibrated posterior mode
\`\`\`

即：

\`\`\`text
m* = argmax_m P(M=m | available evidence)
\`\`\`

只有在：
- calibration 良好；
- posterior concentration 足够；
- coverage / evidence quality 达标；

才允许自然语言使用更确定的表达。

否则必须保留 alternatives 和 uncertainty。

---

## 7. 非事件与竞争通道

必须把：

\`\`\`text
NO_OBSERVED_MANIFESTATION
\`\`\`

作为合法 channel / observation state。

一个 activation 未表现为事件，可能原因包括：
- 无 exposure；
- 用户未采取相关 action；
- 被另一 manifestation channel 吸收；
- external blocking；
- outcome window 尚未结束；
- source mapping 不完整；
- empirical model 错误。

因此不能看到“没发生”就自动否定某一 canonical rule。

若满足标准 time-to-event 与 mutually exclusive event 定义，可使用 competing-risks；否则只使用“competing manifestation channels”作为结构概念，不滥用统计术语。

---

## 8. 数据模型

推荐 observation record：

\`\`\`yaml
person_id:
window_start:
window_end:
chart_version:
knowledge_version:
forecast_version:

natal_state_ref:
temporal_environment_ref:
state_before_ref:

intent:
action:
action_confidence:

exposure:
external_context:
counterparty_context:

manifestation_family:
event_type:
event_status: EVENT_OCCURRED | EVENT_NOT_OCCURRED | UNKNOWN | CENSORED
event_time:
severity:
duration:

observation_source:
observation_confidence:
retrospective: true | false
notes:
\`\`\`

必须支持：
- negative sample；
- censored sample；
- no-event window；
- retrospective / prospective 区分。

---

## 9. 数据偏差控制

至少审计：

- survivorship bias；
- memorable-event bias；
- confirmation bias；
- retrospective reinterpretation；
- MNAR missingness；
- selection into feedback；
- age / occupation / relationship-status confounding；
- exposure opportunity；
- target leakage。

严禁只收“命中了的大事”训练 manifestation probability。

优先建设 prospective check-in：
- 预测在前；
- observation schema 在前；
- 结果在后。

---

## 10. Population -> Cohort -> Individual

建议 hierarchical structure：

\`\`\`text
theta_context =
theta_population
+ delta_cohort
+ delta_domain
+ delta_person
\`\`\`

使用 shrinkage / regularization。

单个用户的数据主要更新：
- S_t；
- personal posterior；
- personal random effect。

不得因为单个用户经历而修改 population parameter，更不得修改 canonical rule。

---

## 11. Causal boundary

只有关联数据时：

\`\`\`text
P(Y | A, state, context)
\`\`\`

只能称：
- conditional association；
- scenario estimate。

不能自动称：
- causal effect。

如果未来要回答：

> “做 A 会不会比做 B 更好？”

必须：
- 明确 causal assumptions；
- 处理 confounding / selection；
- 或保持为 non-causal conditional scenario。

---

## 12. Decision Support / MPC boundary

只有在 predictive calibration 和 causal assumptions 足够后，才进入 action planning。

候选：

\`\`\`text
a* = argmax_a E[U(S_(t+1:t+H), Y_(t:t+H)) | b_t, E_t, constraints]
\`\`\`

U 必须：
- 用户定义；
- 或显式多目标；
- 支持 Pareto trade-off。

禁止使用单一“吉凶分数”充当 universal reward。

---

## 13. Blind vs Personalized 模式

### Blind Forecast

可用：
- N；
- E_t；
- 预先允许的 non-outcome context。

不可用：
- 目标期结果；
- 事后用户解释；
- outcome-derived state。

用于真实 benchmark。

### Personalized Forecast

可额外使用：
- S_t；
- previous Y；
- current A / C；
- individualized posterior。

两者必须分别报指标。

---

## 14. 技术升级门槛

### Bayesian observer
在 sparse / irregular / categorical feedback 下优先。

### Particle filter
只有在：
- nonlinear；
- non-Gaussian；
- multimodal；
- sequential update；
确实使简单模型失效时启用。

### Mixture of Experts
当 manifestation families 足够稳定、样本量足够时启用。

### Graph Neural Network
仅在明确 graph representation 能带来超越 symbolic / statistical baseline 的外部增益后启用。

### Neural State-Space
仅在有足够 longitudinal trajectories 后启用。

### Offline RL
仅在有可信 action/outcome 数据、因果与 safety 约束后考虑。

---

## 15. 与现有产品资产的映射

| 现有资产 | 新架构位置 |
|---|---|
| Normalized Chart Snapshot | B / chart facts |
| Rule Runtime / ActiveRuleGraph | K |
| star cores / system modes | N |
| palace projection | N / contextual projection |
| typed history memory | S_t 的 source-explicit acquired components |
| temporal resolver | E_t |
| EvidencePackage | N/E/S/M 的可审计交付 |
| Casebook | WP06A fidelity + future calibration raw material |
| Human Gate PL2N | N 的 state/projection contract |
| Human Gate Baiguan | N 的 named structure contract |

---

## 16. v0.1 Acceptance Criteria

1. Natal Prior 不接受反馈改写；
2. Temporal Environment 不等于现实事件；
3. Action 与 external disturbance/context 分离；
4. Context 与 observation 分离；
5. state 使用 augmented-state 原则；
6. source possibility 与 empirical probability 分离；
7. population 与 personal posterior 分离；
8. negative / censored data 是一等数据；
9. Blind / Personalized benchmark 分离；
10. causal recommendation 必须经过独立 gate；
11. LLM 不决定 canonical rule 或 learned probability；
12. 所有复杂 AI 模型必须有可解释 baseline 和 out-of-sample 增益证明。


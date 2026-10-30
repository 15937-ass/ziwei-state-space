# Pre-Deletion Chat Archaeology — 紫微斗数项目重要理论/设计/哲学讨论归档

状态：**HISTORICAL / NON-AUTHORITATIVE MIGRATION SEED**  
日期：2026-10-21  
目的：在 PI 大量删除项目聊天前，保留那些曾经推动项目方向、理论结构、认识论边界、产品设计与治理方式发生实质变化的讨论脉络。

> 本文件不是项目当前状态、不是新的 Knowledge truth、不是 Product runtime truth，也不是执行队列。  
> 当前状态仍按 `PROJECT_STATE.yaml -> governance/RECOVERY_PRECEDENCE_v1.md -> live Issue/PR` 恢复。  
> 中州派 canonical truth 仍只能由 Knowledge lane 的来源审查与 Human Gate 决定。  
> 本文件将在独立 Research Memory Sidecar 建立后作为一次性 migration seed 导入；之后不应把 main 仓库变成长期研究日记。

## 1. 覆盖范围与方法

本次归档采用“重要概念考古”而非逐句备份：

- 遍历当前项目可访问的历史聊天上下文，按 2026-05、2026-09、2026-10 三个主要阶段反复检索；
- 对照项目中保存的聊天快照：
  - `分支 · 分支 · 紫微斗数命盘分析.txt`
  - `架构进展与未来期望.txt`
  - `解释两个Human Gate.txt`
- 再与 GitHub 已冻结的 `DECISION_LOG.md`、理论文件、Product Roadmap、Knowledge Roadmap、治理 Proposal/Issue/PR 交叉去重；
- 只保留 R2/R3 级别：理论转折、方法论原则、架构边界、认识论边界、长期产品/研究方向；
- 日常“完成多少条规则”、普通 bug、分支/CI 噪声不在本文件重复保存；
- 明确排除与本项目无关的小说/世界观工程讨论，防止跨项目污染。

### 完整性声明

聊天系统并未向本次工作提供“所有会话逐字导出”的单一原始接口，因此这里的“遍历”指：对**当前项目可检索的历史聊天、保存的聊天快照和 GitHub 记录进行主题化、多轮检索与交叉核对**。本文件目标是避免删除聊天后丢失重要理论脉络，而不是保存每一句原话。

---

## 2. 理论演化总览

项目的核心思想并不是一开始就完整出现，而是经历了以下演化：

```text
早期：确定性排盘 + LLM 解读
  ↓
星曜属性向量 + 图关系 + 四化算子
  ↓
“气 → 象 → 事”的生成式本体
  ↓
中州派 source-grounded 灰箱/状态空间形式化
  ↓
原局本质 + 时序环境 + 状态依赖反应
  ↓
N + E_t + S_t + A_t + C_t 的轨迹模型
  ↓
传统可能性 / 群体概率 / 个体 posterior 分层
  ↓
Kc / Kr / π / θ / b 五类长期对象隔离
  ↓
Product-first：先构建可靠系统，再由系统自然产生论文
```

这里最重要的连续性是：

> 紫微斗数不被建模为“出生盘直接查表得到固定事件”，而被建模为一个具有先天结构、条件激活、时间环境、历史状态、现实选择与外界扰动的**受约束反应系统**。

这一句是聊天中多次讨论逐渐形成的项目哲学，不应因删除聊天而丢失。

---

# 3. Concept / Theory Evolution Records

## CE-001 — 确定性计算与解释层分离

**时期：** 2026-05 早期  
**级别：** R3 架构起点

### 当时的问题

最初目标是让 GPT 做紫微论命，但很快发现：

- 排盘、历法、十四正曜、四化、三方四正等有确定规则；
- 如果让 LLM 同时负责确定计算与解释，会把“算错盘”和“解释差异”混在一起。

### 形成的原则

```text
确定性程序
  -> 排盘 / 历法 / 四化 / 宫位关系 / 时间层
图/规则算法
  -> 三方四正 / 飞化链 / 条件传播
LLM
  -> 取象、解释、语言组织、候选归纳
```

LLM 从一开始就不应该拥有排盘真值。

### 后续影响

这成为后来 Product 的基本分层，也是“LLM 不拥有 canonical rule truth”的前身。

### Git 映射

- `PRODUCT_ROADMAP.md`
- `product/DYNAMIC_INFERENCE_ARCHITECTURE_v0.1.md`
- `DECISION_LOG.md` D-006 / D-019 的方法与对象分离原则

---

## CE-002 — 从“星曜标签”转向“气 → 象 → 事”

**时期：** 2026-05  
**级别：** R3 理论起点

### 被否定的简单模型

早期可行但不够好的做法是：

```text
紫微 = 领导
武曲 = 财
天机 = 变动
...
```

这种标签库无法解释：

- 同一颗星为什么在不同组合、宫位、运限下表现不同；
- 同一“气”为什么可以映射成多种现实事件；
- 为什么不能简单地把吉煞做加减法。

### 新模型

项目逐渐形成：

```text
气（latent structure/state）
  ↓
象（contextual manifestation family）
  ↓
事（observable event）
```

其中：

- 星曜 = 气核 / 基态；
- 星系 = 非线性交互后的中尺度模态；
- 辅佐煞化 = 条件修正/激活/转化算子；
- 宫位 = 场景投影；
- 大限流年等 = 时间激活/环境；
- 现实事件 = 末端观测，而不是 primitive state。

### 重要哲学含义

“气”不是神秘物理量，也不是一个总吉凶分数，而是为了让古典自然语言规则变得可计算而定义的**操作性潜状态**。

### Git 映射

- `DECISION_LOG.md` D-002, D-008, D-009, D-010, D-011
- `theory/state_space_model.md`
- `KNOWLEDGE_BASE_ROADMAP.md`

---

## CE-003 — 四化不是统一“禄正忌负”，而是主体/情境依赖算子

**时期：** 2026-05 → 2026-09 持续强化  
**级别：** R3 知识表示原则

### 被否定的模型

```text
禄 = +1
权 = +1
科 = +1
忌 = -1
```

以及任何“吉星数 - 煞星数”的通用积分。

### 形成的原则

四化应建模为**依赖所作用星曜、原状态、宫位、组合与上下文的 transformation operator**。

一个更接近项目思想的抽象是：

[
S' = O_{	ext{化曜}}(S, context)
]

而不是给所有星统一加减固定权重。

### 后续影响

- 不允许产品自行拍脑袋设置连续权重；
- 不允许“禄忌同见”自动抵消；
- 四化特例一旦回源验证，应反向更新星核、星系、modifier、projection 等层，而不是只修一个输出句子。

### Git 映射

- `DECISION_LOG.md` D-003, D-005, D-007
- `knowledge/**` 四化/化曜 operator 体系
- `theory/state_space_model.md`

---

## CE-004 — 六十星系是非线性组合，不是两个单星向量相加

**时期：** 2026-09  
**级别：** R3

### 核心问题

若两颗主星组合只是：

[
H_{ij}=S_i+S_j
]

就无法解释“组合后出现单星中不存在的新性质”。

### 形成的模型

[
H_s = Phi(S_i,S_j,	ext{context})
]

进一步演化为：

```text
base composition
+ interaction delta
+ principal / multi-mode
+ context gates
```

其中 interaction delta 只是“当前基态组合没有解释掉的交互项”，不能被神秘化为新的 primitive qi。

### 后续影响

- 六十星系成为中尺度状态；
- principal mode 不自动升格为基础气机；
- 允许同一星系存在多模态/条件性反应；
- 防止 ontology 因每个古诀都新增一个维度而无限膨胀。

### Git 映射

- `DECISION_LOG.md` D-010
- `theory/state_space_model.md`

---

## CE-005 — 中州派先形式化，其他流派暂不混入 canonical core

**时期：** 2026-09-21 起  
**级别：** R3 研究边界

### 决策背景

项目资料中同时存在中州、河洛、钦天飞星等体系。若一开始混合：

- 相同术语可能含义不同；
- 冲突无法判断是理论差异还是抽取错误；
- Paper 1 无法明确自己的研究对象。

### 形成的边界

Paper 1：

- 只 formalize 中州派；
- 不用河洛/钦天规则去补中州派缺口；
- 不以跨流派一致性作为“真值”；
- 后续多流派只能通过 school-attributed adapter 进入，冲突保留。

### 后续影响

这既是科学可识别性问题，也是产品可审计性问题。

### Git 映射

- `DECISION_LOG.md` D-001
- `PRODUCT_ROADMAP.md` 的 multi-school future architecture
- `product/PRODUCT_FUTURE_WORKPLAN_v0.1.md` PL8

---

## CE-006 — 控制理论是形式化工具，不是声称古人“本来就在做控制论”

**时期：** 2026-09-21 起  
**级别：** R3 方法论

### 原始设想

把“气”看成不可直接观测的内部状态，把现实应象看成观测，把大限流年看成时变输入：

[
x_{t+1}=f(x_t,u_t,d_t;	heta)+w_t
]

[
y_t=g(x_t,c_t;phi)+v_t
]

随后讨论了：

- state space；
- observability；
- observer / Kalman-like update；
- sensitivity / Jacobian；
- feedback / stability；
- system identification；
- controllability；
- MPC。

### 最关键的收敛

这些概念被分成两类：

**Paper 1 可用：**

- 潜状态表示；
- 结构拓扑；
- 输入/状态/输出分离；
- observation-path / identifiability 启发式；
- 灰箱约束。

**未来才可用：**

- 连续参数辨识；
- Kalman/particle observer；
- controllability 数值结论；
- MPC / RL。

### 认识论边界

不能因为使用状态空间写法就宣称“紫微斗数已经被证明是一个真实物理动态系统”。

### Git 映射

- `DECISION_LOG.md` D-011, D-012, D-015
- `theory/state_space_model.md`
- `paper/manuscript_v0.1.md`

---

## CE-007 — 先结构、后参数；严禁凭感觉填连续权重

**时期：** 2026-09-21 起  
**级别：** R3 科学方法

### 原则

在真实纵向命例和可识别性不足时：

- 用符号参数；
- 用方向约束；
- 用序关系；
- 用定性类别；
- 用 source-supported operator；
- 不给星曜/四化/宫位“发明”连续增益。

参数只能在后续数据阶段，通过受约束系统辨识/统计模型估计。

一个早期讨论过的分解是：

[
	heta=	heta_{	ext{fixed}}+	heta_{	ext{prior}}+	heta_{	ext{learned}}
]

其核心精神最终保留为：

> 传统来源提供结构与约束，经验数据负责估计经验参数；两者不得互相冒充。

### Git 映射

- `DECISION_LOG.md` D-003, D-012
- `knowledge/FUTURE_MODELING_GUIDANCE_v0.1.md`

---

## CE-008 — “文本忠实”与“现实预测正确”永久分开

**时期：** 2026-09-21 → 后续反复强化  
**级别：** R3 认识论核心

### 最重要的区分

项目至少存在四种不同意义上的“对”：

1. 源文还原正确；
2. 逻辑/形式化一致；
3. 软件实现正确；
4. 现实预测有效。

前 3 项全部成功，仍不能自动推出第 4 项。

### 对 Paper 1 的限制

Paper 1 可以声称：

- 可执行；
- 可审计；
- 可追溯；
- 可复现；
- 可做内部案例 reconstruction。

Paper 1 不可以声称：

- 紫微斗数已被科学证明；
- 现实预测准确；
- “气”是物理实体；
- 教材案例重构等于外部预测验证。

### Git 映射

- `DECISION_LOG.md` D-004, D-012
- `paper/manuscript_v0.1.md`

---

## CE-009 — Source truth 与 empirical truth 双层认识论：数据不能静默改经典

**时期：** 2026-09 → 2026-10  
**级别：** R3

### 形成的永久边界

如果未来真实数据发现某条传统规则表现很差：

```text
empirical mismatch
  -> Knowledge Gap / empirical finding
  != rewrite source truth
```

反过来，经典明示某规则也不能直接产生“现实概率 80%”。

### 后续扩展

这进一步演化成多轴状态：

- source status；
- implementation status；
- internal fidelity；
- empirical status；
- causal status。

任何一个轴成熟都不能偷渡成另一个轴成熟。

### Git 映射

- `DECISION_LOG.md` D-014
- `knowledge/FUTURE_MODELING_GUIDANCE_v0.1.md`
- Proposal #513 Research Memory Sidecar 的 Claim Registry

---

## CE-010 — 完整知识库不是穷举组合，而是“原子规则 + 条件算子 + 生成逻辑 + provenance”

**时期：** 2026-09 Phase II  
**级别：** R3 知识工程

### 被否定的目标

“把所有星曜 × 十二宫 × 四化 × 辅煞 × 限流的句子全部提前写出来”。

这会导致组合爆炸，也会把未在原文中支持的组合推断伪装成经典规则。

### “完整”的重新定义

```text
source-span coverage
+ atomic rules
+ condition/operator semantics
+ generative composition
+ case/examples
+ provenance
+ unresolved conflicts
```

因此“完整”强调**可生成覆盖与可追溯覆盖**，而不是字符串枚举量。

### Git 映射

- `DECISION_LOG.md` D-013
- `KNOWLEDGE_BASE_ROADMAP.md`

---

## CE-011 — Artifact-centered multi-agent：Agent 是角色，不是互相争论的独立真理源

**时期：** 2026-09  
**级别：** R2/R3 工作哲学

### 用户目标

大部分机械工作由 GPT 完成，PI 只审核：

- 关键逻辑；
- 重大歧义；
- Human Gate；
- 最终结果。

### 形成的流水线

```text
Source extraction
  -> Rule normalization
  -> Ontology
  -> Mathematical formalization
  -> Implementation
  -> Independent critic/red-team
  -> Deterministic validation
  -> Human Gate when needed
```

不是训练一群自由辩论的 Agent，而是：

> **artifact-centered role separation + versioned evidence**

### 关键后果

GitHub 比“多 Agent”本身更重要，因为每一层必须留下可追溯产物。

### Git 映射

- `DECISION_LOG.md` D-006
- `AGENT_WORKFLOW.md`
- 项目聊天快照 `分支 · 分支 · 紫微斗数命盘分析.txt`

---

## CE-012 — “命不是固定轨迹”：从 N+E 演化到 N+E+S+A+C

**时期：** 2026-10，思想在 10 月初形成，10 月 20 日进一步形式化  
**级别：** R3 项目哲学与动态模型转折

### 旧的危险简化

```text
Chart + Time -> Event
```

它容易把同盘、同年理解成同一现实事件，也容易诱导“铁口直断”。

### 新的理解

原局只给出先天结构/倾向，时间层给出环境与激活，但现实轨迹还取决于：

- 当前已经发展到哪里；
- 当事人的行为与选择；
- 外部现实条件；
- 随机与不可观测因素。

因此项目形成：

[
S_{t+1}sim F(S_t,N,E_t,A_t,C_t;	heta)
]

以及 manifestation：

[
M_tsim P(Mmid N,E_t,S_t,A_t,C_t)
]

其中：

- (N)：Natal Prior / 原局；
- (E_t)：Temporal Environment / 运限环境；
- (S_t)：现实获得状态；
- (A_t)：个人行动/选择；
- (C_t)：外部条件/扰动；
- (	heta)：未来可由数据估计的经验参数。

### 哲学含义

同盘意味着可能共享某些结构与激活条件，**不意味着必须走相同事件轨迹**。

“命”在项目中更接近一个受约束的 trajectory space / response structure，而不是预写好的事件序列。

### Git 映射

- `product/DYNAMIC_INFERENCE_ARCHITECTURE_v0.1.md`
- `product/PRODUCT_FUTURE_WORKPLAN_v0.1.md`
- `DECISION_LOG.md` D-019 的后续对象分离
- Proposal #513 Concept Event 示例

---

## CE-013 — 原局、时间环境、现实状态永久分层

**时期：** 2026-10  
**级别：** R3 Product architecture

### 三层意义

```text
N = Natal Prior
E_t = Temporal Environment
S_t = Personal / Acquired State
```

关键边界：

- 用户反馈不能回写原局；
- 大限流年首先是 environment，不直接等于 event；
- 现实反馈更新 (S_t) / (b_t)，而不是改写经典规则；
- historical state 必须有来源/观测条件，不可自由“脑补”。

### 与中州派方法的连接

中州派推断强调先认识原局各宫本质，再看运限宫位对这种本质产生何种反应。现代模型的 N/E 分层不是把古文硬套进控制论，而是试图保留这种“本质—反应”区别。

### Git 映射

- `product/DYNAMIC_INFERENCE_ARCHITECTURE_v0.1.md`
- `product/PRODUCT_FUTURE_WORKPLAN_v0.1.md`
- `DECISION_LOG.md` D-016, D-017, D-019

---

## CE-014 — 传统可能性、群体概率、个人 posterior 三层永久隔离

**时期：** 2026-10-05 起  
**级别：** R3

### 三类不同对象

**传统知识：**

[
	ext{source rules}Rightarrow	ext{what manifestations are allowed/supported}
]

它回答“可以怎么应”。

**群体经验：**

[
P(Mmid Q,S,C)
]

它回答“在某类条件下通常怎么应”。

**个人历史：**

[
P(Mmid Q,S,C,	ext{person history})
]

它回答“对这个具体人，过去反馈后现在怎么更新”。

### 永久边界

- source wording 中的“多、易、往往”不能直接翻译成数值概率；
- population probability 不等于 personal posterior；
- personalized accuracy 不能冒充 blind accuracy；
- 第一次使用时个人 posterior 应强烈回缩到群体/无信息先验；
- 用户没有报告某事 ≠ 某事没发生。

### Git 映射

- `product/DYNAMIC_INFERENCE_ARCHITECTURE_v0.1.md`
- `product/PRODUCT_FUTURE_WORKPLAN_v0.1.md`
- `knowledge/FUTURE_MODELING_GUIDANCE_v0.1.md`

---

## CE-015 — Blind Forecast 与 Personalized Forecast 必须是两个不同科学问题

**时期：** 2026-10  
**级别：** R3 验证设计

### Blind

[
P(Ymid Chart,Time,	ext{preregistered allowed context})
]

用于回答：

> 命盘与时间结构本身有没有额外预测信息？

### Personalized

[
P(Ymid Chart,Time,History,Action,Context)
]

用于回答：

> 在已知道这个人过去状态与反馈以后，系统能否更好地服务这个具体人？

### 为什么必须分开

如果把个人历史、既往事件和反馈放进预测再报一个“准确率”，模型可能只是利用现实状态，而不是命盘结构。

未来真正重要的是 incremental value：

[
Delta I = I(Y;Nmid S,C,A)
]

或同类严格的 held-out comparison。

### Git 映射

- `product/PRODUCT_FUTURE_WORKPLAN_v0.1.md` PL4-B / PL5-D
- `knowledge/FUTURE_MODELING_GUIDANCE_v0.1.md`

---

## CE-016 — Product-first 转折：“论文来自产品建设”，不是“产品服从论文”

**时期：** 2026-10  
**级别：** R3 战略转折

### 新的最高目标

产品目标被重新表述为：

> 做排盘可靠、推理稳定、可解释、可审计、能在外部 benchmark 中被真正检验的紫微系统。

论文成为副产物：

```text
可靠排盘
 -> 完整知识库
 -> 可执行规则
 -> 专家方法
 -> benchmark / calibration
 -> 可解释产品
       ↓
formalization / benchmark / knowledge engineering / identification papers
```

### “准确率”被拆成至少五种

1. 排盘准确；
2. 中州派规则还原准确；
3. 推理一致性；
4. 外部盲测准确；
5. calibration / abstention 能力。

这防止“说得越详细、用户越觉得准”被错误当成 accuracy。

### Git 映射

- `PRODUCT_ROADMAP.md` Product-First Program v0.4
- `product/PRODUCT_FUTURE_WORKPLAN_v0.1.md`
- 项目聊天快照 `架构进展与未来期望.txt`

---

## CE-017 — 专家知识不只有“规则是什么”，还有“专家如何推”

**时期：** 2026-10-20  
**级别：** R3 Product v0.4

### 新发现

仅有 declarative rules 仍不足以重建王亭之式推断。还需要分离：

- `Kc`：canonical declarative knowledge；
- `Kr`：canonical response knowledge；
- `pi`：inference policy / procedural knowledge；
- `	heta`：empirical calibration parameters；
- `b`：individual state belief。

### Expert Case Bank 的作用

王亭之约 10 个完整案例：

- 用于学习/验证专家推理程序；
- 用 Leave-One-Case-Out replay 防止直接背答案；
- 属于 method fidelity / internal reconstruction；
- **不能当现实概率 ground truth**。

其他三合派案例只有在 school compatibility 审查后才能用于 procedural generalization / robustness，不能反向污染中州派 canonical truth。

### Git 映射

- `DECISION_LOG.md` D-019
- Proposal #425
- `PRODUCT_ROADMAP.md` v0.4

---

## CE-018 — AI 技术升级必须“窄而可审计”地逐级发生

**时期：** 2026-10  
**级别：** R3 方法原则

### 冻结的顺序

```text
Symbolic / deterministic
 -> interpretable statistics
 -> Bayesian
 -> hierarchical Bayesian
 -> causal evaluation
 -> Mixture of Experts
 -> neural state-space / GNN
 -> MPC
 -> offline RL only if justified
```

### 为什么

不是因为神经网络/RL“不先进”，而是太早使用会：

- 把 source rule truth 与 learned pattern 混在一起；
- 让可审计系统重新变黑箱；
- 在数据不足时制造虚假精度；
- 难以知道性能提升来自哪里。

每一次复杂化都必须至少有：

- simpler baseline；
- held-out improvement；
- calibration comparison；
- traceability audit。

### Git 映射

- `product/PRODUCT_FUTURE_WORKPLAN_v0.1.md`
- `knowledge/FUTURE_MODELING_GUIDANCE_v0.1.md`
- 项目聊天快照 `解释两个Human Gate.txt`

---

## CE-019 — 纵向反馈数据必须保存 negative / unknown / censored，而不是只收“算准的大事”

**时期：** 2026-10  
**级别：** R3 数据哲学

### 核心原因

只记录“发生了的大事”会产生严重选择偏差。

因此 Person × Time 数据必须区分：

- positive；
- confirmed negative；
- unknown / not asked；
- censored / lost-to-follow-up；
- interval event time。

并坚持：

> 用户没说，不等于没发生；只有完整观察窗才能形成可靠 negative。

### 后续影响

未来 calibration、event-history、hierarchical Bayesian 都必须建立在这类数据质量之上。

### Git 映射

- `product/PRODUCT_FUTURE_WORKPLAN_v0.1.md` PL7
- Product longitudinal/check-in artifacts

---

## CE-020 — 外部 benchmark 的意义是“让系统有机会失败”

**时期：** 2026-10  
**级别：** R2/R3 验证哲学

### 原则

训练/构建规则时使用的文本和案例不能同时被包装成外部预测证据。

因此未来应同时保留：

- internal fidelity benchmark；
- public/external blind benchmark；
- preregistered future prospective evaluation。

应比较：

```text
Context-only
Pure LLM
RAG
Flat rules
Symbolic model
Natal + Temporal
Calibrated model
Personalized model
```

并使用 calibration / Brier / log loss / coverage-at-confidence / abstention 等，而非只报一个 Accuracy。

### Git 映射

- `product/PRODUCT_FUTURE_WORKPLAN_v0.1.md` PL4-A / PL4-B / PL5
- `PRODUCT_ROADMAP.md`

---

## CE-021 — 多流派未来可以加入，但必须 school-attributed、独立 calibration、冲突保留

**时期：** 2026-10  
**级别：** R3

### 原则

中州派是 canonical core，不代表其他派别“错误”。

未来河洛、钦天等应通过：

- school adapter；
- school-attributed evidence；
- independent namespaces；
- conflict-preserving comparison；
- school-specific calibration

接入。

禁止：

- 用别派规则静默填中州派的空缺；
- 因外部案例“看起来准”就改中州 canonical；
- 把不同派别同名概念强行统一。

### Git 映射

- `product/PRODUCT_FUTURE_WORKPLAN_v0.1.md` PL8
- `DECISION_LOG.md` D-001 / D-019

---

## CE-022 — GitHub 从“代码仓库”升级为项目的唯一耐久状态；Chat 降级为工作空间

**时期：** 2026-09 → 2026-10-06 正式治理冻结  
**级别：** R3 治理哲学

### 形成的权威链

```text
Constitution / approved Human Gate / Proposal
 -> Roadmap / Architecture
 -> Phase Contract
 -> live GitHub Issue
 -> PR
 -> validation
 -> main
 -> historical/chat evidence
```

简化表达：

- Issue = execution truth；
- PR = implementation truth；
- main = accepted state；
- Chat = 可丢失工作空间，不再是项目状态。

### 为什么重要

项目早期已经出现“聊天里说过，但三周后忘了为什么”的理论漂移风险。

Git 的价值不是只存代码，而是让：

```text
source
 -> rule
 -> ontology
 -> model
 -> implementation
 -> validation
 -> paper claim
```

都能追踪版本与理由。

### Git 映射

- `PROJECT_STATE.yaml`
- `AGENT_WORKFLOW.md`
- `governance/RECOVERY_PRECEDENCE_v1.md`
- `DECISION_LOG.md` D-018

---

## CE-023 — Fail-closed：未知、冲突、不支持都必须是“一等状态”

**时期：** 2026-09 → 2026-10  
**级别：** R3 质量原则

### 原则

系统不得为了让结果“更完整”而：

- 自动补不存在的 condition semantics；
- 把 UNKNOWN 当 false；
- 把 source conflict 自动投票；
- 把不可执行规则降级为模糊自然语言“猜测”；
- 把 candidate 当 canonical。

关键区分包括：

```text
expressible != resolved != executable
source-reviewed != product-active
internal reconstruction != empirical validation
```

### 后续影响

“不知道”不是产品缺陷，而是可校准系统必须具备的输出能力。

### Git 映射

- `AGENT_WORKFLOW.md`
- `KNOWLEDGE_BASE_ROADMAP.md`
- `product/DYNAMIC_INFERENCE_ARCHITECTURE_v0.1.md`
- `DECISION_LOG.md` D-014

---

## CE-024 — Knowledge 可以并行，但共享语义必须串行治理

**时期：** 2026-10-21  
**级别：** R2/R3 执行架构

### 问题

单一 Knowledge WIP=1 太慢，但完全并发会产生：

- 不同宫位各自发明同一个 ontology；
- schema 漂移；
- 交叉污染。

### 方案

```text
Knowledge Core WIP <= 1
Palace workers <= 4
Per-palace WIP <= 1
```

宫位 worker：

- 只能在自己 shard 范围工作；
- 遇到共享语义问题 fail-closed；
- 提交 `KNOWLEDGE_CORE_GAP`；
- 不能自己改 global ontology；
- canonical merge 仍逐个在最新 main 上串行验证。

### Git 映射

- `DECISION_LOG.md` D-020
- Proposal #528
- `governance/KNOWLEDGE_SHARD_EXECUTION_v1.md`

---

## CE-025 — Research Memory Sidecar：研究记忆与项目真相再次分层

**时期：** 2026-10-21  
**级别：** R3 元治理

### 新问题

当 Product / Knowledge 发展速度超过论文写作速度，重要的：

- 理论转折；
- negative findings；
- 研究问题；
- claim maturity；
- 论文映射

会散落在聊天、Issue、PR、报告中。

### 形成的架构

独立 `ziwei-research-ledger`（未来创建）：

- append-only Research Events；
- multi-axis Claim Registry；
- Theory Evolution Ledger；
- Paper/RQ Map；
- Evidence Packs；
- Concept Events；
- last_seen_main_sha replay。

### 永久边界

Research Memory：

- 只读已接受证据；
- 不阻塞 Product / Knowledge；
- 不拥有 canonical 权威；
- 不自动提高 empirical/causal claim；
- 修正通过 supersession，不改写历史。

### 当前文件的身份

本文件正是 Sidecar 尚未建仓前的**一次性 pre-deletion migration seed**。

### Git 映射

- Issue #513
- PR #514
- `governance/proposals/513-research-memory-sidecar-v1.md`

---

# 4. 已经进入 canonical Git 的内容 vs 本文件特意保留的“讨论脉络”

| 主题 | canonical / frozen Git 已覆盖 | 本文件额外保存的价值 |
|---|---|---|
| 气=操作性潜状态 | D-002 | 记录它如何从“星曜标签”问题中产生 |
| 气→象→事 | D-011 / theory | 记录早期生成式本体动机 |
| 非线性星系 | D-005 / D-010 | 记录为何拒绝简单向量相加 |
| 不发明连续权重 | D-003 | 记录“先结构后参数”的研究哲学 |
| 内部/外部效度分离 | D-004 / D-012 | 记录四种“正确”概念 |
| N/E/S/A/C | Product architecture | 记录“命不是固定轨迹”的哲学转折 |
| Kc/Kr/π/θ/b | D-019 | 记录从“规则库”升级为“专家推理系统”的原因 |
| Product-first | Product Roadmap | 记录论文主线→产品主线的战略转折 |
| GitHub durable truth | D-018 / governance | 记录为什么不再让聊天承担记忆 |
| Research Sidecar | Proposal #513 | 记录它直接源于“重大理论会被聊天删除/遗失”的风险 |

---

# 5. 明确保留的长期哲学边界

以下内容即使未来架构多次升级，也不应被普通工程工作静默推翻：

1. **“气”是操作性潜状态，不是已证明的物理能量。**
2. **传统文本忠实度不等于现实预测有效性。**
3. **软件执行正确不等于命理正确。**
4. **原局不是现实事件清单，而是先天结构/倾向。**
5. **大限流年首先是时变环境/激活，不直接等于事件。**
6. **同盘不意味着同一现实轨迹。**
7. **现实历史与用户反馈更新个人状态/posterior，不改写 natal truth。**
8. **传统可能性、群体概率、个人 posterior 永久分开。**
9. **用户没报告某事，不等于某事没发生。**
10. **经验数据可以证伪/削弱 empirical claim，但不能静默篡改 source truth。**
11. **canonical Knowledge、专家推理 policy、经验参数、个体 belief 必须可区分。**
12. **LLM 不拥有排盘真值、经典规则真值或概率真值。**
13. **未知与冲突必须显式保留，不能为了“神准感”强行补全。**
14. **模型复杂度升级必须由数据和 held-out evidence 驱动，而不是技术时髦驱动。**
15. **多流派可以比较，但不能静默混派。**
16. **控制理论是现代形式化工具，不是对古代文本作历史事实断言。**
17. **产品的高可用性与科学验证都需要允许模型拒答/低置信，而不是强迫每题给确定结论。**
18. **GitHub 是项目耐久真相；聊天可以删除，项目状态不应因此丢失。**

---

# 6. 删除聊天后的恢复路径

批量删除聊天后，新会话不应尝试“凭记忆恢复项目”。

按以下顺序：

```text
PROJECT_STATE.yaml
 -> governance/RECOVERY_PRECEDENCE_v1.md
 -> selected lane state
 -> live GitHub Issue
 -> linked PR
 -> Issue-required artifacts
```

若要恢复**理论历史而不是当前执行状态**：

```text
DECISION_LOG.md
 -> theory/**
 -> PRODUCT_ROADMAP.md / KNOWLEDGE_BASE_ROADMAP.md
 -> approved governance proposals
 -> this pre-delete archaeology seed
 -> future ziwei-research-ledger
```

本文件永远排在 canonical artifacts 之后。

---

# 7. 待未来 Research Sidecar 导入的首批 Concept/Theory 节点

建议 RSM-1 / RSM-2 首批至少形成以下节点，而不是简单把本文件整篇复制：

1. `THEORY-QI-AS-LATENT-STATE`
2. `THEORY-QI-XIANG-SHI-GENERATIVE-CHAIN`
3. `THEORY-NONLINEAR-STAR-SYSTEMS`
4. `METHOD-SOURCE-CONSTRAINED-GREYBOX`
5. `EPISTEMIC-INTERNAL-VS-EMPIRICAL-VALIDITY`
6. `EPISTEMIC-SOURCE-VS-EMPIRICAL-TRUTH`
7. `THEORY-DESTINY-AS-CONSTRAINED-TRAJECTORY-SPACE`
8. `THEORY-N-E-S-A-C-DYNAMIC-MODEL`
9. `PRODUCT-POSSIBILITY-POPULATION-PERSONAL-POSTERIOR`
10. `METHOD-BLIND-VS-PERSONALIZED-EVALUATION`
11. `METHOD-EXPERT-PROCEDURAL-KNOWLEDGE`
12. `PRODUCT-KC-KR-PI-THETA-B-SEPARATION`
13. `METHOD-COMPLEXITY-ESCALATION-LADDER`
14. `GOVERNANCE-GITHUB-DURABLE-TRUTH`
15. `GOVERNANCE-RESEARCH-MEMORY-SIDECAR`

每个节点导入 Sidecar 时必须继续保留 source/internal/empirical/causal 多轴状态；本文件中的概括不能自动升级为 canonical Zhongzhou meaning。

---

# 8. 结论

截至 2026-10-21，项目最值得从聊天中抢救的，不是某一次“算对了什么”，而是以下三条演化主线：

**理论线：**

[
	ext{星曜标签}
ightarrow
	ext{气机潜状态}
ightarrow
	ext{非线性星系}
ightarrow
	ext{气→象→事}
ightarrow
	ext{动态轨迹空间}
]

**科学线：**

[
	ext{传统断语}
ightarrow
	ext{来源可追溯规则}
ightarrow
	ext{可执行形式化}
ightarrow
	ext{内部 fidelity}
ightarrow
	ext{外部 blind validation}
ightarrow
	ext{calibration / personalization}
]

**产品线：**

[
	ext{LLM 解盘}
ightarrow
	ext{确定性排盘+规则}
ightarrow
	ext{source-grounded symbolic engine}
ightarrow
	ext{expert procedural reasoning}
ightarrow
	ext{population calibration}
ightarrow
	ext{personal state belief}
ightarrow
	ext{conditional decision support}
]

这些主线已经足以让未来项目在大量旧聊天被删除后，仍然知道**我们为什么走到今天，以及哪些边界不能因为聊天消失而被忘掉**。

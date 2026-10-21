# 紫微斗数项目聊天理论／设计／哲学保全归档 — 2026-10-21

状态：**HISTORICAL SYNTHESIS / NON-EXECUTION-AUTHORITY**  
治理工单：Issue #558  
用途：在 PI 大规模清理项目聊天之前，保全聊天中形成、但分散在多个会话里的重要理论脉络、设计理由、研究哲学与方法论。  
权威边界：本文件**不是当前执行队列，也不覆盖已冻结决策**。发生冲突时，仍按 `PROJECT_STATE.yaml -> GOVERNANCE / approved Gate or Proposal -> live Issue/PR -> lane state` 的现行权威链处理。

---

## 0. 为什么需要这份归档

项目早期大量真正重要的内容并不是“某个文件最终长什么样”，而是：

- 为什么决定只用中州派做第一阶段；
- 为什么把“气”定义成潜状态而不是物理实体；
- 为什么不用一个 prompt 让 GPT 直接解盘；
- 为什么把原局、时间环境、现实状态、个人选择、外界扰动拆开；
- 为什么不把教材命例当现实预测准确率；
- 为什么后面才考虑 Bayesian、GNN、MPC、RL；
- 为什么同一命盘不应被理解成一条固定轨迹；
- 为什么 Chat 不能再承担项目状态真相。

这些“为什么”在 `DECISION_LOG.md`、Roadmap、Proposal 和代码里往往只保留最终结论。若删除聊天而不保存其生成逻辑，未来虽然能够恢复“做什么”，却可能丢掉“为什么这样做”。

本文件因此保留**概念史与设计 rationale**，而不是逐字聊天 transcript。

### 0.1 恢复来源

本归档综合了：

1. 项目历史聊天的可检索上下文；
2. 项目内保存的聊天导出／阶段总结文本；
3. 当前 GitHub 的 `DECISION_LOG.md`、Roadmap、Proposal、State、Architecture、Validation 等正式记录；
4. 对二者进行互校后的去重结果。

### 0.2 记录状态标签

- **CANONICAL_ALREADY_RECORDED**：已在 GitHub 正式冻结／批准，不靠本归档获得权威。
- **APPROVED_RATIONALE**：方向已被 PI 明确认可，Git 中已有实现或约束，但聊天中的“为什么”值得保留。
- **PROVISIONAL_RESEARCH_NOTE**：重要理论思想，但不应自动升级为中州派 canonical truth 或论文定论。
- **OPEN**：仍应由未来资料、benchmark、Human Gate 或系统辨识解决。
- **SUPERSEDED / REJECTED**：曾讨论过，但后来明确不作为当前路线。

---

# 1. 2026-05：最早期的核心直觉——不是让 AI 猜命盘，而是构造可审计推演系统

状态：**APPROVED_RATIONALE**，后续被正式架构吸收。

早期讨论已经形成了后来整个项目的核心分工：

```text
出生信息
-> 确定性排盘 / 四化 / 宫位关系 / 限流
-> 规则与图结构推理
-> 结构化证据
-> LLM 解释与表达
```

而不是：

```text
出生信息
-> prompt
-> LLM 自由解盘
```

最初的产品思想可概括为：

> **规则引擎 + 图算法／知识图谱 + 案例库 + LLM 的神经符号混合系统。**

其中：

- 排盘、宫位、四化、飞化链、限流等可确定部分必须程序化；
- LLM 不承担底层事实真值；
- LLM 更适合做语言化、取象候选、知识检索辅助、未结构化反馈解析与解释；
- 任何最终结论都应尽可能回到可追溯的规则与状态变化。

这条分工后来成为 Product 的根本边界：**LLM 可以 verbalize，但不能拥有 rule truth 或 probability truth。**

### 1.1 早期“矩阵／张量／图”直觉

项目最初并未把紫微看成一堆自然语言标签，而是尝试将其拆为：

- 星曜：属性／气机向量；
- 星系：非线性组合，而非简单相加；
- 四化／辅煞：状态变换算子；
- 三方四正、会照、飞化：关系图与传播；
- 十二宫：情境／场景投影；
- 大限流年：时变外生输入；
- 应象：潜状态在现实场景中的投影结果。

早期曾讨论“命盘二级矩阵”“星曜一级矩阵”“张量”“群论”等表述。最终保留的不是具体数学名词，而是更稳健的原则：

> **局部属性 + 关系结构 + 非线性交互 + 时变输入 + 场景投影。**

群论只被认为适合描述某些循环／对称结构，不能作为完整模型基础。

---

# 2. “气 → 象 → 事”：项目最重要的知识表示思想之一

状态：**CANONICAL_ALREADY_RECORDED / APPROVED_RATIONALE**。  
对应：D-002、D-007、D-008～D-012、`theory/state_space_model.md`、Knowledge schema。

早期讨论明确反对把星曜直接编码成“十个标签”或“吉／凶”“有钱／没钱”一类事件词。更成熟的思路是：

```text
气（latent structure / disposition）
-> 象（contextual manifestation pattern）
-> 事（real-world event candidate）
```

核心理由有三点。

第一，**同一气机可以在不同宫位、时代、职业和现实条件下显成不同事件**。如果直接用“事件词”做底层标签，就会把传统知识的生成结构压扁。

第二，星曜本身应被视为**多个基础气机维度的复合状态**，星系再在此基础上产生 interaction delta / principal mode，而不是把每个星系当完全独立的标签。

第三，“吉凶”不能和状态变化混成一个字段。一个结构可能同时：

- 增加某种能力；
- 增加某种代价；
- 在某情境有利；
- 在另一情境不利。

因此后来正式冻结为：**latent-state change 与 contextual valence 分离；source wording 与 research normalization 分离。**

### 2.1 “气”的本体论边界

聊天里一度使用了较强的“气机”“能量”等传统语言。Paper 1 最终主动降格：

> “气”只作为**操作性潜状态 representation**，不主张它是已被物理学证明存在的能量实体。

这不是弱化项目，反而是重要的认识论清洁：允许我们研究“传统系统能否被机器可读地形式化”，而不需要先证明传统本体论是真实物理世界。

---

# 3. 2026-09：第一篇论文的真正边界——先形式化，不抢着证明“算得准”

状态：**CANONICAL_ALREADY_RECORDED**。  
对应：D-001～D-006、D-011、D-012、PROJECT_CONSTITUTION。

第一篇研究正式收缩为：

> **将中州派知识形式化为机器可执行、可审计、可追溯的层级潜状态系统。**

明确不做：

- 不混钦天、河洛等流派；
- 不把预测准确率作为 Paper 1 的主要贡献；
- 不把“气”声称为物理实体；
- 不用作者拍脑袋给连续数值权重；
- 不把内部复现等同现实预测验证。

第一阶段研究链被固定为：

```text
知识本体化
-> 规则原子化
-> 星曜 / 星系 / 辅佐煞化形式化
-> 宫位投影
-> 状态空间表达
-> 可执行实现
-> 内部忠实度 / 可复现性验证
```

连续参数、概率和增益系数留给后续系统辨识。

---

# 4. G1–G6 形成的理论骨架

状态：**CANONICAL_ALREADY_RECORDED**。  
正式权威：`DECISION_LOG.md` D-007～D-012。

## 4.1 G1：规则不是一句话，而是带证据链的原子对象

形成了后续最关键的链：

```text
source span
-> atomic rule
-> normalized condition/operator
-> inference trace
-> conclusion
```

一条规则必须能回答：

- 原文在哪里；
- 原文到底说了什么；
- 我们做了什么归一化；
- 哪些条件才激活；
- 改变的是哪个状态／关系；
- 哪个部分只是研究者解释；
- 最后输出为何能回溯到它。

## 4.2 G2：气机本体采用分层，而不是一锅属性

批准 L0–L4 分层思想：

- L0：结构底座；
- L1：内在状态；
- L2：关系状态；
- L3：场景／宫位投影；
- L4：评价／语义结果。

重要原则：

- 允许非单调变量；
- 阴阳五行可作结构底座，但不能粗暴等于全部状态；
- 具体 QI 维度是可修订候选，不是先验真理。

## 4.3 G3：十四正曜气核是基态，不是完整命断

单星采用统一结构：

```text
L0 base
+ L1 intrinsic core
+ L2 relational core
+ contextual modifiers
```

单星只能提供基态。真正推断必须进入：

- 星系组合；
- 三方四正；
- 辅佐煞化；
- 宫位；
- 时序环境。

## 4.4 G4：六十星系不是两颗星简单相加

正式采用：

```text
base composition
+ interaction delta
+ principal mode
+ context gates
```

关键哲学是：

> **星系具有涌现性。**

`principal mode` 是中尺度模态，不自动升格成新的 primitive qi；`Delta_s` 只表示尚未被低阶分解解释的交互残差，不代表神秘新实体。

## 4.5 G5：状态空间采用“固定原局本质 + 时序外生输入 + 状态依赖反应”

Paper 1 的核心结构被定为：

- 十二宫：12 个局部节点；
- 整体命盘：全局稀疏关系图；
- 原局：相对固定的先天结构；
- 大限／流年：外生时间环境；
- 人的选择：独立输入；
- 外部现实条件：独立扰动；
- 应象：输出层，不等于潜状态本身。

同时明确：

- 不默认一切效应线性可加；
- 不把所有路径依赖都塞进一个递归神经状态；
- Paper 1 先做结构支持／可区分性审计；
- 真正的 observer、controllability、optimal control 留作后续。

## 4.6 G6：认识论边界

Paper 1 最终只允许主张：

> 在当前中州派语料范围内，这套传统知识可以被形式化为可执行、可审计、可追溯的层级潜状态系统。

不能主张：

- 已证明紫微斗数现实预测有效；
- 已证明“气”是客观物理量；
- 内部一致性等于外部预测效度；
- 控制理论术语本身能给术数增加科学真实性。

现代控制、灰箱系统、hybrid system、observer 等，在第一篇里都是**形式化工具**，不是“验证命理”的证据。

---

# 5. A0 / A1 / A2：项目为什么后来越来越强调“去污染”

状态：**CANONICAL_ALREADY_RECORDED**。  
对应 D-014～D-016。

随着规则规模扩大，项目发现最大的危险不是“规则不够多”，而是**研究者自己的归一化悄悄冒充原文**。

## 5.1 A0：双层认识论

明确分离：

- `source_epistemic`：源文本身能支持到什么程度；
- `normalization_epistemic`：研究者为可计算化做了什么抽象。

并把历史上笼统的“REVIEWED”拆为：

- MODEL_EXTRACTED；
- MODEL_SELF_REVIEWED；
- SOURCE_SPAN_VERIFIED；
- HUMAN_VERIFIED。

这一步的意义是：**模型自己审过不等于原文已经逐条核验。**

## 5.2 A1：不允许为了旧 ontology 强行解释新材料

全文反向审计的原则是：

> ontology 应被语料修正，而不是让语料屈从 ontology。

因此发生了：

- 某些状态维度正式升格；
- 某些原先合并的维度被拆开；
- 某些概念被收窄；
- “structural observability”被降格为更保守的 observation-path support。

这体现了项目重要的方法论：

> **术语越现代，不代表证据越强。**

## 5.3 A2：路径依赖必须有类型

历史记忆没有被做成自由向量，而是拆成至少：

- `ACQUIRED_DISPOSITION`：后天形成／强化／固化的倾向；
- `PATH_DEPENDENT_GATE`：过去关键阶段使后续某规则取得资格或进入不同分支。

只有 source-explicit persistence/path dependence 才能进入历史层。

禁止自动发明：

- 衰减率；
- 学习率；
- 连续记忆权重；
- 永久保持假设。

一般连续递归动力学继续留在 Paper 2+。

---

# 6. “完整知识库”不是穷举宇宙，而是生成式完整

状态：**CANONICAL_ALREADY_RECORDED / APPROVED_RATIONALE**。  
对应 D-013、`KNOWLEDGE_BASE_ROADMAP.md`、KB completeness audits。

项目曾经有一个自然诱惑：把“60 星系 × 12 宫 × 辅佐煞化 × 四化 × 运限”全部枚举完。

后来明确否决这种完整性定义，因为组合会爆炸。

当前真正的“完整”是：

```text
原子规则覆盖
+ 条件算子覆盖
+ 组合生成逻辑
+ 案例/例证关联
+ provenance
+ 冲突保留
+ 可执行与回归验证
```

因此：

> **完整知识库 = 能生成并审计传统推断，而不是把所有理论组合预先写成句子。**

冲突必须进入 registry，不能为了输出“干净”而静默合并。

教材命例可以：

- 发现规则；
- 验证程序是否重建作者推理；
- 帮助提炼 procedural method；

但不能自动升级为现实概率 ground truth。

---

# 7. 从“论文项目”转向“产品第一，论文自然产出”

状态：**APPROVED_RATIONALE**，已被 Product Roadmap / v0.4 架构吸收。

项目后来主动调整优先级：

> **优先做一个排盘可靠、推理稳定、可解释、可追溯、能被外部 benchmark 检验的系统；论文从产品建设产生的本体、规则、benchmark、消融和验证结果中自然产出。**

这并不是放弃学术，反而避免“为了论文结构漂亮而造一个没有产品价值的模型”。

形成了一个重要选择原则：

> 如果 A“论文写起来漂亮但对正确率／可靠性帮助有限”，B“学术上不花哨但显著提高可信度”，优先 B。

这也是后来研究 sidecar 的意义：**论文记忆旁路记录产品成熟过程中自然出现的研究贡献，而不让论文重新阻塞产品主线。**

---

# 8. “准确”必须拆成至少五件不同的事

状态：**APPROVED_RATIONALE / PRODUCT DOCTRINE**。

聊天中形成的五层准确性定义应长期保留：

## 8.1 排盘准确率

目标接近确定性 100%。

包括：

- 公历／农历／闰月；
- 早子晚子；
- 真太阳时／DST；
- 主星、辅煞杂曜；
- 四化；
- 大限、流年、流月、流日、流时；
- 宫干、飞化、关系。

这一层禁止 LLM 参与真值生成。

## 8.2 中州派规则还原准确率

问题是：

> 给定一个盘和问题，系统调用的规则是否真是中州派来源允许的规则？

这是知识工程准确性，不是现实预测准确性。

## 8.3 推理一致性

```text
same input
-> same active rules
-> same state transitions
-> compatible conclusion
```

今天和明天不能因为 LLM 风格不同就换一套底层逻辑。

## 8.4 外部案例／盲测准确率

必须使用：

- 系统没见过的人；
- 系统没见过的事件答案；
- 预先冻结 target/window/context；
- 禁止 outcome leakage。

## 8.5 Calibration / 拒答能力

强模型不是“每次都断一句”，而是能区分：

- HIGH；
- MEDIUM；
- LOW；
- CONFLICTED；
- INSUFFICIENT_EVIDENCE。

真正有意义的是：

> 高置信预测是否在 held-out 数据上真的比低置信预测更准。

因此 coverage、abstention、calibration 和 accuracy 同样重要。

---

# 9. 双引擎与外部项目策略——把壁垒花在最值得花的地方

状态：**APPROVED_RATIONALE / IMPLEMENTED IN PART**。

项目形成了“拆着借，不整套抄”的策略：

- 别人擅长排盘工程，就用来做独立对照；
- 别人擅长大规模数据，就用来做压力测试／数据审计；
- 我们自己的壁垒集中在：
  - 中州派 source-grounded knowledge；
  - executable symbolic inference；
  - state / response architecture；
  - evidence trace；
  - expert-method fidelity；
  - empirical calibration。

典型结论：

### iztro 等排盘引擎

不立即替换自有系统，而是做双引擎：

```text
Our Chart Engine
       \
        Comparator
       /
Independent Engine
```

出现差异后才判定：

- 流派差异；
- 规则约定差异；
- 程序 bug。

### 大规模生成命盘数据

可用于：

- parser；
- schema；
- stress test；
- UI；
- embedding；
- crash coverage。

但“用同一体系生成标签，再训练再测试”只能证明学会了那个体系，不能证明现实预测有效。

---

# 10. 最重要的哲学转折：命盘不是固定轨迹

状态：**APPROVED_RATIONALE + PROVISIONAL_RESEARCH_NOTE**。  
与 Product 的 N/E/S/A/C 架构一致，但“结构性生成主义”本身不自动升级为中州派 canonical doctrine。

项目越来越明确拒绝一种产品想象：

> 同一个命盘对应一条预写好的人生剧本。

更合适的解释是：

> 命盘描述一种先天结构／倾向场；现实轨迹还受当前状态、环境、个人选择、外部扰动和历史反馈影响。

这最终被程序化为：

```math
S_{t+1} ~ F(S_t, N, E_t, A_t, C_t; theta)
```

其中：

- `N`：Natal Prior，原局先天结构；
- `E_t`：Temporal Environment，大限／流年等时变环境；
- `S_t`：现实已经发展到哪一步；
- `A_t`：主体行动／选择；
- `C_t`：外部条件、冲击、机会与未建模扰动；
- `theta`：未来由数据识别的经验参数。

现实表现则更接近：

```math
M_t ~ P(M | N, E_t, S_t, A_t, C_t)
```

因此“同一个象”可能：

- 显成手术；
- 显成轻微磕碰；
- 显成职业变化；
- 显成关系压力；
- 没有清晰可观察外显。

关键不是事后解释一切，而是逐步建立：

- 候选应象空间；
- 状态门控；
- 现实 context；
- 概率与校准；
- 可拒答能力。

---

# 11. 结构性生成主义：保留为研究哲学，不伪装成源文

状态：**PROVISIONAL_RESEARCH_NOTE**。

早期聊天形成过一个更一般的“结构性生成主义”：

```text
先在结构
-> 情境 / 环境
-> 当前状态
-> 主体感知与解释
-> 决策
-> 行动
-> 现实反馈
-> 结构沉淀
-> 下一轮生成
```

可以概括为：

> **命运 = 结构约束下，主体在情境中持续实践与反馈所生成的轨迹。**

这里的“自由”不是无约束自由，而是：

> 在既有结构与现实边界内，主体可以改变自己的响应方式、选择策略与后续状态。

聊天中曾用“观照 → 重构 → 抉择 → 沉淀”描述反身性。

对本项目最有价值的不是它作为一个宏大哲学理论，而是它提供了几个产品设计约束：

1. 不把命盘当最终结果；
2. 不把个人选择自动归入“命”；
3. 不把所有未知差异解释成自由意志；
4. 必须保留 external / stochastic / unmodeled variance；
5. 个体反馈可以改变 personal belief，不应直接改写传统 canonical truth。

**重要降格：**这一套哲学是研究者的解释框架，不是王亭之原文的一部分。它可以作为未来论文讨论／产品哲学，但不能反向写进中州派规则库。

---

# 12. N / E / S / A / C 五类对象为什么必须分开

状态：**APPROVED_RATIONALE / PRODUCT ARCHITECTURE**。

## N — Natal Prior

- 由原局与 canonical knowledge 构成；
- 是先天先验；
- **永远不能被现实反馈改写。**

现实数据如果和它不合：

- 可以说明规则表现不好；
- 可以生成 Knowledge Gap Report；
- 可以影响经验层校准；

但不能悄悄把原典规则改掉以“迎合数据”。

## E_t — Temporal Environment

大限／流年首先是**环境**，不是事件。

因此禁止：

```text
某大限结构
=> 必然结婚 / 必然手术 / 必然破产
```

更合理的是：

```text
某时段使某类状态/反应更容易被激活
```

## S_t — Acquired / Personal State

描述“这个人现实已经走到哪里”：

- 婚恋状态；
- 职业状态；
- 资源状态；
- 迁移／定居；
- 暴露与承诺；
- 既往形成的 disposition。

## A_t — Action

人的选择与行动独立表示。

## C_t — Context / Disturbance

外部现实、社会条件、机会、冲击、随机与未建模成分独立表示。

**永久边界：`A_t != C_t`。**

---

# 13. “传统可能性 / 群体概率 / 个人后验”必须永久分层

状态：**CANONICAL_PRODUCT_BOUNDARY**，已进入 Product 规划。

最终专家系统应拆成三层：

```text
Traditional canonical knowledge
-> 这个象传统上允许怎样表现
```

```text
Population data
-> P(M | Q, S, C)
```

```text
Person history
-> P(M | Q, S, C, person history)
```

因此：

- source-supported possibility 不是概率；
- 群体频率不是个人命运；
- personal posterior 不能冒充 blind forecast；
- 第一次使用时，应强 shrink 到群体；
- 长期个人历史充分后，个体 posterior 才允许逐渐偏离总体。

这才是项目对“经验丰富的算命先生”的现代解释：不是 LLM 靠语感，而是**传统结构 + 群体经验 + 个体历史**分层积累。

---

# 14. Product v0.4：从“规则系统”进一步升级为“专家推理系统”

状态：**CANONICAL_ALREADY_RECORDED**。  
对应 D-019 / Proposal #425。

产品长期对象被拆为：

- `Kc`：canonical declarative knowledge；
- `Kr`：canonical response knowledge；
- `pi`：expert inference policy / procedural knowledge；
- `theta`：empirical calibration parameters；
- `b`：individual state belief。

同时把：

- `E_t`：时间环境；
- `tau_t`：ResponseProfile；

正式分层。

这一步解决了一个长期混淆：

> “书里写了什么”与“专家实际上按什么顺序、如何综合这些信息”不是同一种知识。

因此王亭之完整命例进入 **Expert Case Bank**，用途是：

- 学 procedural method；
- 重建推断路径；
- 做 expert-method fidelity benchmark。

但采用 **Leave-One-Case-Out**：

> 用其余案例归纳方法，再看能否重建被留出的案例。

这样可以减少“读了答案再解释答案”的自我验证。

**命例不是现实概率标签。**

---

# 15. 内部忠实度与现实预测必须分成两条 benchmark

状态：**CANONICAL_PRODUCT_BOUNDARY**。

## PL4-A Internal Fidelity

回答：

> 我们有没有忠实实现这个传统体系？

测：

- chart reconstruction；
- rule trace；
- author-case reasoning reconstruction；
- temporal fidelity；
- conflict preservation；
- determinism。

## PL4-B Predictive Blind Benchmark

回答：

> 这套系统对现实未知事件有没有可重复的增量信息？

要求：

- target preregistration；
- fixed time window；
- held-out subjects；
- forbidden leakage；
- context-only baseline；
- pure LLM / RAG / flat rules / symbolic / calibrated 等基线对照；
- Brier / log loss / calibration / coverage-at-confidence；
- abstention。

必须做增量比较：

```text
Context only
vs + Natal
vs + Temporal
vs + Personal history
```

否则无法知道“准”到底来自：

- 常识；
- 年龄／职业；
- 用户已经透露的信息；
- 还是命盘本身。

---

# 16. 数据飞轮必须记录负样本、未知和删失，而不是只收“算准的大事”

状态：**APPROVED_RATIONALE / PARTLY IMPLEMENTED**。

如果用户只在“发生大事”时回来反馈，系统会得到严重 selection bias。

因此长期数据层必须支持：

- positive；
- negative；
- unknown；
- censored；
- interval event time；
- follow-up completeness；
- missing-not-at-random flags。

永久提醒：

> **用户没说 ≠ 没发生。**

只有观察窗口真正完成时，negative 才能安全成立。

反馈不能自动改写 canonical knowledge。它只能进入：

- observation；
- personal state；
- calibration dataset；
- knowledge gap report。

---

# 17. AI / 统计 / 控制技术的启用顺序

状态：**APPROVED_RATIONALE**。

项目后来明确固定复杂化顺序：

```text
Symbolic / deterministic
-> interpretable statistical baseline
-> Bayesian
-> Hierarchical Bayesian
-> causal evaluation
-> Mixture of Experts
-> GNN / neural state-space
-> MPC
-> offline RL (last)
```

每次升级都必须有：

- simpler baseline；
- held-out improvement；
- calibration comparison；
- traceability audit。

为什么 GNN / 深度状态空间 / RL 现在不优先？

不是因为它们不先进，而是：

> **过早使用会把一个本来可审计的系统重新变黑箱。**

MPC／决策支持只有在三件事同时成熟后才有意义：

1. 状态估计可信；
2. 预测校准可信；
3. 行动的因果识别可信。

否则最多只能做 conditional scenario，不能说“做 A 一定比做 B 好”。

---

# 18. 产品 UX 的理论边界

状态：**APPROVED_RATIONALE / PRODUCT PLAN**。

长期至少区分：

- Natal Mode；
- Blind Forecast Mode；
- Personalized Forecast Mode。

解释层至少区分：

- 普通用户；
- 高级用户；
- Expert / Debug。

Expert 输出应能看出：

- source；
- activated rule；
- conflict；
- temporal evidence；
- personal observation；
- probability source；
- uncertainty。

并支持 contrastive explanation：

> 为什么系统倾向 A，而不是 B？

答案必须能拆成：

- canonical；
- temporal；
- personal；
- empirical；
- counterevidence。

---

# 19. QuickRead / 话术层为什么只能是旁路

状态：**APPROVED_RATIONALE**。

聊天中曾专门讨论“真人简批”“话术研究”等用户体验。

最终边界是：

> QuickRead 只是 read-only verbalizer / filter / audit sidecar，不是新的命理引擎。

它只能消费：

- Canonical Runtime；
- Temporal Profile；
- EvidencePackage。

并对句子打 provenance：

- RUNTIME_CANONICAL；
- RUNTIME_TEMPORAL；
- SOURCE_BACKED_FALLBACK；
- LLM_VERBALIZATION；
- LLM_ADDED_UNSUPPORTED；
- OBSERVATION。

`LLM_ADDED_UNSUPPORTED` 应被阻断，而不是因为“像真人”就放行。

话术研究和 Gold Examples 可以改善表达，但不能成为规则真值。

---

# 20. 多流派长期路线：Adapter，不混库

状态：**CANONICAL_ALREADY_RECORDED / PRODUCT FUTURE**。

第一阶段继续坚持：

> **Zhongzhou canonical core。**

未来钦天、河洛等应通过 adapter 加入：

```text
Core infrastructure
   |- Zhongzhou namespace
   |- Qintian namespace
   |- Heluo namespace
   |- other school namespace
```

要求：

- school-attributed evidence；
- school-specific calibration；
- 冲突保留；
- 不静默平均；
- 不用另一流派规则“修正”中州 canonical truth。

跨流派一致时可以报告 consensus，冲突时必须报告 school-specific disagreement。

---

# 21. GitHub 治理为什么最终变成项目本身的一部分

状态：**CANONICAL_ALREADY_RECORDED**。  
对应 D-018、D-020、G8/G9/G12。

最初用户希望：

> GPT 做绝大部分机械工作，自己只审核逻辑与最终结果。

因此形成的不是“训练一群永久 Agent”，而是角色化流水线：

```text
GPT producer
-> GPT independent reviewer / red team
-> deterministic tests
-> only material dispute to PI
-> approved version freeze
```

关键改变是：

> **所有角色共享 GitHub artifact，而不是共享聊天记忆。**

这解决理论漂移：

```text
v0.1
-> critic finds issue
-> v0.2
-> PI approval
-> freeze
```

同时形成当前权威链：

```text
Issue = execution truth
PR = implementation truth
main = accepted truth
State YAML = recovery cache
Chat = non-authoritative working conversation
```

## 21.1 三条 lane

- PRODUCT_ONLY；
- KNOWLEDGE_ONLY；
- GOVERNANCE_ONLY。

跨 lane 发现只能开 dependency / gap，不允许顺手修改。

## 21.2 为什么坚持 bounded work unit

因为长聊天里连续做大量 Git 操作会增加：

- 状态漂移；
- 重复读取；
- 错误分支；
- 误把旧 artifact 当当前任务。

所以长期采用：

> 一批工作 -> durable checkpoint -> validation -> merge -> next bounded unit。

## 21.3 知识侧并行为什么采用“宫位 shard + Core 串行”

后来为提高速度，知识侧从全局 WIP=1 变为：

- Knowledge Core WIP <= 1；
- 最多 4 个不同宫位 worker；
- 每宫 WIP <= 1；
- 公共 ontology / schema / semantics 只能由 Core 修改；
- 宫位发现跨域语义问题必须 fail-closed；
- main 合并仍串行 exact-head。

这使多聊天并行成为可控工程，而不是“多个 Agent 同时改世界观”。

---

# 22. PI 与 AI 的长期职责分工

状态：**CANONICAL_ALREADY_RECORDED / APPROVED_RATIONALE**。

AI 应自动承担：

- 文献抽取；
- 规则原子化；
- source span 核验；
- schema 归一化；
- 代码与测试；
- critic / red-team；
- benchmark 运行；
- GitHub checkpoint；
- 论文技术写作草案。

PI 只应在真正需要研究判断的地方介入：

- 中州派语义争议；
- 流派边界；
- 新基础气机；
- source 无法唯一解释；
- 产品重大目标；
- 研究 claim 强度；
- causal / empirical 重大升级；
- Human Gate。

PI 汇报应优先说：

- 新增加了什么知识；
- 修正了什么理论；
- 当前真正能做什么；
- 还不能声称什么；
- 下一步研究意义；

而不是把 commit、branch、CI 噪音当主体。

---

# 23. 被明确否决／降级／后移的路线

状态：**SUPERSEDED / REJECTED**。

以下想法应保留为历史，防止未来重新“发明”：

### 23.1 “命盘 -> prompt -> GPT -> 答案”

否决。不可审计、不可复现、规则会漂移。

### 23.2 Paper 1 直接给连续权重

否决。没有系统辨识数据前只允许符号、序关系、定性类别。

### 23.3 把所有效应做线性相加

否决。源文存在组合、门控、反格、转化与状态依赖。

### 23.4 Paper 1 直接做完整递归动力学／观测器／能控性

后移。先把源文支持的状态、输入、输出、历史记忆结构搭好。

### 23.5 用“structural observability”强称路径计数结果

降级为 observation-path support。

### 23.6 把所有路径依赖存成一个自由 history vector

否决。改为 typed memory。

### 23.7 教材案例 = 现实预测 ground truth

否决。只能用于 fidelity / method reconstruction。

### 23.8 用生成数据训练，再用同源生成标签宣称“准确”

否决。只能证明体系复现。

### 23.9 一个总 Accuracy

否决。至少拆排盘、规则忠实、推理一致、外部盲测、calibration。

### 23.10 用户反馈自动修改经典规则

否决。反馈只能更新个人状态／经验模型／gap report。

### 23.11 现在就上 GNN / RL

后移。必须先有简单基线、足够数据、预测增量和可审计性。

### 23.12 多流派现在混成一个知识库

否决。中州 core 先闭合，其他流派 adapter 化。

### 23.13 Chat 作为项目状态

彻底否决。聊天可以消失，项目必须仍能从 GitHub 恢复。

---

# 24. 当前仍应视为 OPEN 的理论问题

这些问题不因聊天删除而消失：

1. **QI ontology 最终维度**：当前候选由全文证据持续校正。
2. **modifier operator order**：哪些算子可交换、顺序是否重要。
3. **principal mode 的最终表示**：离散、连续、混合还是概率。
4. **参数可辨识性**：star core、interaction delta、modifier、projection 是否混淆。
5. **一般递归状态是否必要**：需纵向数据检验，不应先验假设。
6. **真正 structural observability / identifiability**：需正式状态—输出图与数学条件。
7. **manifestation ontology 的顶层结构**：应尽量 source-derived，不应先套现代社会／心理分类。
8. **Kr / expert procedural policy 的闭合**：当前是 Product v0.4 关键知识缺口。
9. **现实预测增量**：只有 PL4-B / PL5 held-out benchmark 能回答。
10. **行动因果效应**：没有 causal identification 不能升级为趋吉避凶因果建议。
11. **个体化速度与 shrinkage**：需要长期数据决定。
12. **多流派冲突的产品呈现**：保留 disagreement，但未来 UI 仍需验证。

---

# 25. 删除聊天后，项目应靠什么恢复

聊天删除后，一个新的会话不应依赖“记得我们以前聊过什么”。

恢复分为两层：

## 25.1 执行状态恢复

严格按：

```text
PROJECT_STATE.yaml
-> RECOVERY_PRECEDENCE
-> selected lane state
-> live Issue
-> linked PR
```

本归档不能选任务。

## 25.2 理论／设计理由恢复

按：

```text
DECISION_LOG
+ approved proposals / Human Gates
+ Roadmaps / architecture
+ 本聊天理论保全归档
```

理解“为什么形成这些决策”。

---

# 26. 与现有 canonical Git 记录的映射

| 本归档主题 | 当前主要正式载体 |
|---|---|
| Paper 1 中州派边界 / qi latent / 无任意权重 | `PROJECT_CONSTITUTION.md`, D-001～D-006 |
| Rule schema 与状态/valence 分离 | D-007, `RULE_SCHEMA.md` |
| L0-L4 qi ontology | D-008 |
| 十四正曜基态 | D-009 |
| 六十星系 interaction / principal mode | D-010 |
| 状态空间、十二宫稀疏图、气→象→事 | D-011, `theory/state_space_model.md` |
| Paper 1 认识论 | D-012 |
| 完整中州派知识库 | D-013, `KNOWLEDGE_BASE_ROADMAP.md` |
| A0 去污染 | D-014 |
| A1 ontology 反向审计 | D-015 |
| typed history memory | D-016 |
| event-relative temporal window | D-017 |
| GitHub 治理 | D-018 |
| Kc/Kr/pi/theta/b + expert reasoning / response | D-019 / Proposal #425 |
| 宫位 shard 并行 | D-020 / Proposal #528 |
| N/E/S/M、盲测、数据飞轮、MPC 路线 | `product/PRODUCT_FUTURE_WORKPLAN_v0.1.md` |
| Chat 权威降级与恢复 | Proposal #374, `RECOVERY_PRECEDENCE_v1.md` |
| Product knowledge promotion | Proposal #491 |

---

# 27. 本次聊天清理后的保全结论

可以删除大量聊天，但需要坚持一个原则：

> **删聊天不能等于删研究历史。**

当前正式项目真相已经主要在 GitHub；本次归档补齐的是聊天里分散的设计理由与哲学脉络。

因此后续新的 ChatGPT 会话不应尝试“重新回忆所有旧聊天”，而应：

1. 从 GitHub 恢复正式状态；
2. 需要理解研究意图时读取本归档；
3. 新的重要理论讨论继续通过 Issue / Proposal / Decision / archive 方式持久化；
4. 不再让一段超长聊天成为不可替代的单点记忆。

---

## 28. 一句话保留整个项目的思想核心

> **把紫微斗数当作一个历史形成的符号—规则系统来严格形式化：用确定性程序负责可确定事实，用可追溯知识负责传统语义，用动态状态模型表示先天结构、时序环境与现实状态的交互，用数据而不是想象学习概率，让 LLM 负责表达而不拥有真值；最终研究的不是“一张盘写死一个人生”，而是一个结构约束下会因环境、历史与主体行动产生分叉的可审计轨迹空间。**


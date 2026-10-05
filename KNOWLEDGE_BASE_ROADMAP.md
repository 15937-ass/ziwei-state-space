# Phase II：中州派完整知识库工程路线图

版本：0.2  
状态：ACTIVE  
生效日期：2026-10-05  
替代：v0.1

## 1. 目标重述

本知识侧的任务不是直接训练“算命模型”，而是建立一个尽可能完整、可追溯、可执行、可生成、可用于后续状态推演和经验校准的**中州派 canonical knowledge system**。

“完整”仍不定义为穷举所有盘，而定义为：

1. Source Coverage 完整；
2. Atomic Rule Coverage 完整；
3. Concept / Operator Coverage 完整；
4. Palace / Temporal Projection 完整；
5. Manifestation Possibility Ontology 完整；
6. Case Reconstruction 完整；
7. Inference Interface 完整；
8. 冲突、未知与不可判定状态完整保留。

知识侧只回答：

> 传统资料允许我们说什么？在什么条件下说？它作用到什么状态/结构/候选应象？

知识侧不回答：

> 某个应象在现实中究竟有 63% 还是 71% 概率？

概率属于产品侧 empirical calibration。

---

## 2. 三层知识边界

### A. Canonical Traditional Knowledge

包括：
- source spans；
- reviewed rules；
- ontology；
- star cores；
- sixty-system modes；
- operators；
- palace projections；
- source-backed temporal reactions；
- source-backed manifestation possibilities。

性质：不受用户反馈和统计训练自动修改。

### B. Empirical Calibration

不是 canonical KB 的一部分。

包括：
- manifestation probability；
- learned gain；
- cohort effect；
- posterior distribution；
- empirical interaction。

知识侧只可提供约束/先验方向，不存训练结果为传统真理。

### C. Personal Adaptation

完全不进入 canonical KB。

包括：
- 当前现实状态；
- 既往事件；
- 选择与计划；
- individual posterior。

---

## 3. 知识库六层结构

### KB-L0 — Source Layer
保存：
- source_id；
- 文件/版本；
- 页码/章节；
- source span；
- provenance；
- 使用状态。

### KB-L1 — Atomic Rule Layer
保存：
- 单星；
- 星系；
- 辅佐煞化杂曜；
- 宫位；
- 庙旺利陷；
- 四化；
- relation；
- natal / decade / year / month 等层级条件。

### KB-L2 — Concept & Operator Layer
保存：
- qi / state dimensions；
- relational state；
- star core；
- star-system mode；
- modifier；
- transformation；
- palace projection；
- temporal reaction；
- pattern qualification / break condition。

### KB-L3 — Generative Inference Layer
保存：
- dependencies；
- prerequisites；
- conflict sets；
- operator composition；
- cross-palace relations；
- temporal inheritance/reaction；
- contextual projections；
- UNKNOWN / INSUFFICIENT_EVIDENCE path。

### KB-L4 — Manifestation Ontology Layer
新增。

保存：
- abstract activation / symbolic manifestation family；
- source-supported manifestation channels；
- event specificity；
- allowed / disallowed normalization；
- source evidence；
- probability_status=UNKNOWN。

L4 只规定“可应为什么”，不规定“最常应为什么”。

### KB-L5 — Case & Validation Layer
保存：
- 教材案例；
- 对比案例；
- 反例；
- 作者 reasoning steps；
- rule linking；
- chart reconstruction；
- model reconstruction；
- unresolved spans；
- case-derived candidates。

教材案例首先服务于 fidelity / reconstruction，不自动成为现实 prediction ground truth。

---

## 4. 原局与时序的知识边界

### 4.1 Natal Canonical Knowledge

原局层负责生成：
- innate star/system properties；
- natal named structures；
- natal palace projections；
- source-backed prior tendencies；
- stable cross-palace dependencies。

知识侧必须保证：
- 不需要现实反馈；
- 同输入同知识版本得到同一结构输出；
- 用户反馈不能反向重写原局 rule truth。

### 4.2 Temporal Canonical Knowledge

时间层负责描述：
- 大限/流年/流月等环境条件；
- 对原局状态的加强、削弱、转化、激活；
- source-explicit persistence / path dependence；
- candidate temporal manifestation families。

时间层不得直接将“环境/激活”同义化成唯一现实事件。

---

## 5. Phase II 工作包重编排

## KB-WP01 — 全语料目录与覆盖矩阵

状态：沿用。

目标：
- source inventory；
- chapter coverage；
- source-binding；
- corpus provenance。

---

## KB-WP02 — 十四正曜全文规则

状态：沿用。

目标：
- star intrinsic / relational / conditional signatures；
- source-backed modifiers；
- interaction boundaries；
- no invented weights。

---

## KB-WP03 — 六十星系全文规则

状态：沿用。

目标：
- system modes；
- special reactions；
- temporal interactions；
- contrastive systems；
- rule dependencies。

已完成 extraction 的系统只有在案例 reconstruction 与 inference regression 通过后才升级 COMPLETE。

---

## KB-WP04 — 辅佐煞化/杂曜算子库

状态：source closure 已完成，后续仅处理新缺口或反向审计。

目标：
- source-backed modifier/operator；
- strengthen / weaken / transform；
- structure-specific effect；
- ordinal relation where source explicit。

禁止：
- 将文字“最喜/次喜/尤忌”擅自数值化。

---

## KB-WP05 — 十二宫全文 Projection Corpus

状态：ACTIVE。

当前继续：
- 事业宫 CA05 起后续批次；
- 按现行 100-item recoverable checkpoint；
- 用户侧每 200 items 汇报一次；
- 每批抽取 palace-specific projection、cross-palace dependency、history feedback、temporal boundary。

WP05 不因产品 PL3 启动而暂停。

---

## KB-WP06A — Source Case Reconstruction

从旧 WP06 拆出。

目标：
- 结构化教材案例；
- 重建出生资料/命盘；
- 抽取作者 claim / reasoning / feedback；
- link canonical rule IDs；
- 检查 author conclusion 是否可由当前 KB 重建。

输出：
- CaseEvidenceRecord；
- reconstruction result；
- missing-rule report；
- contradiction report。

边界：
- 作者结论不是 reality ground truth；
- case-derived rule 只能进入 candidate，不能自动 canonicalize。

---

## KB-WP06B — Manifestation Ontology

新增核心工作包。

目标：
把传统断语中的“应象”从最终自然语言事件中抽象成分层 ontology。

建议层级：

\`\`\`text
latent activation
  -> manifestation family
     -> channel
        -> observable event label
\`\`\`

例如（仅作为 schema 说明，不预设具体中州 mapping）：

\`\`\`text
physical disruption
  -> medical/procedural
  -> accidental
  -> minor external injury
  -> no observed external event
\`\`\`

每个节点至少保存：
- manifestation_id；
- parent_id；
- domain；
- abstraction_level；
- source-supported labels；
- source rule IDs；
- event specificity；
- ambiguity notes；
- probability_status。

默认：

\`\`\`text
probability_status = UNKNOWN
\`\`\`

---

## KB-WP06C — Manifestation Hypothesis Registry

目标：
建立：

\`\`\`text
source-backed symbolic activation
  -> allowed candidate manifestation channels
\`\`\`

每条 mapping 必须区分：
- EXPLICIT；
- TRANSPARENT_INFERENCE；
- CASE_SUPPORT_ONLY；
- HYPOTHESIS。

禁止：
- 从案例频次直接提升 canonical mapping；
- 把“常见”写成概率，除非 source 本身明确且只作为 source claim 保存。

---

## KB-WP07A — Natal Inference Specification

从旧 WP07 拆出。

目标：
定义 canonical natal inference contract：

\`\`\`text
chart facts
 -> active natal rules
 -> star/system state
 -> named structures
 -> palace/context projection
 -> NatalStateProfile
\`\`\`

知识侧负责 schema 与 semantic correctness；
产品侧负责 runtime implementation。

---

## KB-WP07B — Temporal Reaction Specification

目标：

\`\`\`text
NatalStateProfile
+ temporal chart facts
 -> temporal activation / strengthening / weakening / transformation
 -> TemporalEnvironmentProfile
\`\`\`

需明确：
- natal essence 与 temporal environment 分离；
- source-explicit path dependence；
- time-layer precedence / conflict；
- unresolved state。

不得把 temporal activation 直接等同现实事件。

---

## KB-WP07C — Manifestation Interface Contract

目标：
规定知识侧如何把候选应象交给产品侧：

\`\`\`text
symbolic activation
 -> manifestation candidates
 -> evidence tier
 -> source trace
 -> unresolved alternatives
\`\`\`

知识侧在此停止，不输出 population probability。

---

## KB-WP08 — Ordinal / Constraint Knowledge Registry

新增。

目的：保存传统资料已经给出的**相对强弱或顺序信息**，为未来系统辨识提供约束，但不造数值。

可保存：

\`\`\`yaml
relation_type: stronger_than | weaker_than | preferred_over | especially_avoid
lhs:
rhs:
scope:
source:
review_status:
\`\`\`

例如 source 明确出现“以 A 为上、B 次之、C 又次之”时，可冻结：

\`\`\`text
A > B > C
\`\`\`

但绝不能自行设：
- A=0.9；
- B=0.6；
- C=0.3。

未来 empirical layer 可使用 monotonic / order constraints。

---

## 6. “气核—应象”在知识侧的正式位置

知识侧不直接把“气核”定义为一个神秘总分。

它应由：

\`\`\`text
star core
+ system mode
+ palace context
+ modifiers
+ structures
+ relational dependencies
\`\`\`

共同形成可追溯 state bundle。

“应象”不是从星曜直接跳到事件：

\`\`\`text
star -> event
\`\`\`

而是：

\`\`\`text
facts
 -> structure/state
 -> activation
 -> manifestation family
 -> candidate channel
\`\`\`

最后“哪个 channel 最常发生”留给 empirical calibration。

---

## 7. 不确定性与证据等级

所有新增 manifestation / ordinal / dynamic knowledge 必须保留：

- source_epistemic；
- normalization_epistemic；
- review_status；
- case_support_only；
- human_gate_required；
- conflict group；
- unresolved alternatives。

知识侧允许最终结论为：

\`\`\`text
NO_UNIVERSAL_RULE
NO_UNIVERSAL_THRESHOLD
INSUFFICIENT_SOURCE
SOURCE_CONFLICT
\`\`\`

这些是合法成果，不是失败。

---

## 8. Human Gate 触发条件

继续沿用既有 G1–G6 / A0–A2。

新增明确触发：

1. 新增 primitive qi；
2. 修改 natal essence 定义；
3. 修改 natal / temporal 边界；
4. 新增 universal manifestation family；
5. 新增长期 memory / persistence / decay 机制；
6. 将 empirical result 提升为 canonical source rule；
7. 为 source 未给出的 effect 指定数值；
8. 新增会改变核心 operator 语义的结构。

不触发 Human Gate：
- source-explicit 新 rule；
- source-explicit manifestation label；
- 普通 case linking；
- ordinary ontology child node；
- empirical model retrain（产品侧负责）。

---

## 9. 知识侧完成度指标升级

除原指标外，新增：

- Natal Inference Coverage %
- Temporal Reaction Coverage %
- Manifestation Ontology Coverage %
- Manifestation Mapping Evidence Mix
- Ordinal Constraint Coverage %
- Case Reconstruction %
- Inference Interface Trace Completeness %
- Unknown / No-Universal-Rule Rate

“完整”不要求 Unknown=0。

相反，如果 source 本身没有提供阈值或唯一映射，正确的 COMPLETE 可以包含显式 UNKNOWN。

---

## 10. 当前知识侧执行顺序

当前不改正在运行的 source-review 节奏：

\`\`\`text
WP05 Career CA05
 -> remaining Career batches
 -> remaining palace closure
\`\`\`

与 WP05 后半程并行准备：

\`\`\`text
WP06A Case Reconstruction schema hardening
WP06B Manifestation Ontology schema
WP06C Manifestation Mapping registry
\`\`\`

WP07A/B/C 在对应 WP05 / WP06 覆盖足够后进入规范冻结。

WP08 可随 source review 发现明确 ordinal language 时增量积累，不需要等待 WP05 完成。

---

## 11. Knowledge -> Product Contract

以后知识侧只通过版本化 canonical artifact 向产品侧输出：

\`\`\`text
Source-reviewed facts/rules
    ↓
Canonical structures/states
    ↓
Natal/Temporal inference contracts
    ↓
Manifestation candidates + evidence
    ↓
[STOP]
\`\`\`

产品侧在此之后处理：
- runtime；
- posterior state estimation；
- empirical probability；
- personalization；
- scenario simulation。

现实反馈若暴露知识缺口，只生成：

\`\`\`text
KNOWLEDGE_GAP_REPORT
\`\`\`

再回源复核。

不得执行：

\`\`\`text
bad prediction -> silently edit canonical rule
\`\`\`


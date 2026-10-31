# Product Architecture v0.3

状态：IMPLEMENTATION DESIGN  
生效日期：2026-10-05  
配套规范：product/DYNAMIC_INFERENCE_ARCHITECTURE_v0.1.md

本版本不改变 G1–G6 / A0–A2-R1 已冻结领域理论；它把既有产品架构与新的 Natal Prior / Temporal Environment / Acquired State / Manifestation Routing 分层对齐。

## 1. 总体架构

产品核心链路更新为：

~~~text
Birth Input
  -> Deterministic Chart Layer
  -> Normalized Chart Snapshot
  -> Canonical Rule Runtime
  -> Natal Prior Engine
  -> Temporal Environment Engine
  -> Personal State Observer
  -> Manifestation Router
  -> Confidence / Conflict / Calibration Layer
  -> EvidencePackage
  -> LLM Verbalizer
  -> UI
~~~

其中：

- Natal Prior 可以独立运行，不需要现实反馈；
- Temporal Environment 只描述时间层环境/激活，不直接输出宿命事件；
- Personal State Observer 只处理现实获得性状态；
- Manifestation Router 才把 symbolic activation 映射到候选现实通道；
- empirical probability 与 canonical source evidence 必须分别标注；
- LLM 始终在结构化推理链末端。

---

## 2. Deterministic Chart Layer

接口继续保持：

~~~python
ChartAdapter.render(birth_input, config) -> NormalizedChartSnapshot
~~~

至少保留：
- internal adapter；
- iztro reference/export；
- 第二外部引擎 reference/export。

所有 adapter 显式携带：
- engine/version/commit；
- school/config；
- timezone/solar-time policy；
- Zi-hour policy；
- calendar-conversion policy。

外部引擎只作为差异发现器，不是 ground truth。

**生产排盘硬约束：** 所有正式 NATAL 与 DECADE / AGE / YEAR / MONTH / DAY / HOUR 快照必须遵循 `product/CANONICAL_CHART_CONTRACT_v1.1.md`：中州派 + `iztro-js@2.6.1`，固定 heaven / 闰月 / 日界 / 年界 / 运限配置。x-iztro 与 Go 只做差分审计，不得成为生产 fallback。LLM 和人工不得生成、补算或修改排盘事实；生产入口必须在加载 Provider / Runtime 前执行 canonical chart fail-closed 校验。更改方法必须经 PI 明确批准、升级契约版本、制定迁移并重跑完整 P1 回归。

---

## 3. Canonical Rule Runtime

接口：

~~~python
RuleRuntime.match(
    chart_state,
    temporal_state,
    question_scope
) -> ActiveRuleGraph
~~~

ActiveRuleGraph 节点至少包含：
- rule_id；
- school；
- source pointer；
- review status；
- matched conditions；
- operator；
- target state；
- before/after state；
- conflict group；
- evidence status。

禁止运行时从自由文本临时生成不存在的 canonical rule。

---

## 4. Natal Prior Engine

新正式接口：

~~~python
NatalPriorEngine.build(
    normalized_chart,
    canonical_knowledge_version
) -> NatalStateProfile
~~~

NatalStateProfile 至少包含：
- active natal rules；
- star cores；
- sixty-system modes；
- named structures；
- palace/domain states；
- cross-palace dependencies；
- pattern status / scale / integrity；
- contextual valence candidates；
- conflict/ambiguity；
- evidence provenance；
- confidence。

硬约束：

~~~text
same chart
+ same school/config
+ same canonical knowledge version
=> same NatalStateProfile
~~~

用户反馈不得修改 NatalStateProfile 中的 canonical truth。

---

## 5. Temporal Environment Engine

接口：

~~~python
TemporalEngine.resolve(
    natal_profile,
    target_time,
    temporal_config
) -> TemporalEnvironmentProfile
~~~

TemporalEnvironmentProfile 包含：
- decade/year/month/day/hour facts（按已批准范围）；
- temporal transformations；
- activated natal rules；
- strengthening / weakening / transformation；
- temporal conflicts；
- source-supported manifestation candidates；
- unresolved alternatives。

它描述：

> 这个阶段有哪些结构被激活、怎样改变当前推演条件。

不直接等同：

> 这个阶段现实一定发生什么。

---

## 6. Personal State Observer

接口概念：

~~~python
StateObserver.update(
    prior_state,
    observations,
    actions,
    external_context
) -> StateBelief
~~~

StateBelief 属于 acquired / empirical layer，不属于 canonical rule layer。

必须区分：
- intent；
- planned action；
- actual action；
- exposure；
- external constraint；
- observation；
- observation confidence。

v0.1 优先简单、可审计：
- deterministic updater；
- Bayesian belief。

复杂 filtering 只有在数据证明必要时再加入。

---

## 7. Manifestation Router

接口：

~~~python
ManifestationRouter.route(
    natal_profile,
    temporal_profile,
    state_belief,
    action_context,
    external_context,
    calibration_model=None
) -> ManifestationDistribution
~~~

输出必须分别标注：

### A. Source-supported possibilities
传统资料支持哪些 candidate manifestation channels。

### B. Empirical population probabilities
在 calibration corpus 上学习的群体概率。

### C. Personalized posterior
结合当前个体纵向数据后的 posterior。

禁止把 A 的传统描述直接伪装成 B/C 的数字概率。

---

## 8. BAIGUAN / contextual valence integration

PL2 Human Gate 后：

- BAIGUAN_SUPPORT_PROFILE 属于 Natal/Structure layer；
- contextual valence 属于 projection layer；
- pattern scale 与 pattern integrity 分离；
- structure 不自动等于 GOOD/BAD；
- UNKNOWN / INSUFFICIENT_EVIDENCE 是合法运行结果。

百官 activation criterion 未 source-backed 冻结前，不得使用人工成员数量阈值。

---

## 9. EvidencePackage vNext

EvidencePackage 后续应能承载四类证据：

~~~text
CANONICAL
TEMPORAL
EMPIRICAL
PERSONAL
~~~

建议字段族：

~~~yaml
canonical:
  chart_facts:
  rule_ids:
  structures:
  natal_states:

temporal:
  active_layers:
  temporal_rules:
  environment_states:

personal:
  acquired_state:
  actions:
  exposures:
  observation_refs:

empirical:
  calibration_model:
  cohort:
  probability:
  interval:
  calibration_metrics:

conflicts:
alternatives:
confidence:
~~~

LLM 只能 verbalize 这些已计算内容。

---

## 10. Confidence 必须分解

不再用一个模糊 confidence 覆盖所有不确定性。

至少区分：

- source confidence；
- normalization confidence；
- structure qualification confidence；
- state-estimation confidence；
- empirical calibration confidence；
- outcome uncertainty。

用户界面可以压缩成 HIGH/MEDIUM/LOW，但 Expert/Debug 层必须能看到来源。

---

## 11. Blind 与 Personalized runtime

### Blind Mode

允许：
- chart；
- canonical knowledge；
- target time；
- 预注册可用背景变量。

禁止：
- target-period result；
- after-the-fact explanation；
- outcome-derived personal state。

### Personalized Mode

可以额外使用：
- acquired state；
- past feedback；
- current action；
- exposure；
- context；
- personal posterior。

两者使用独立 benchmark / metric namespace。

---

## 12. Contrastive Explanation

继续支持：

> 为什么是 A，而不是 B？

但解释现在分层为：

1. canonical support；
2. temporal support；
3. personal/context modifiers；
4. empirical likelihood；
5. missing gate / counterevidence。

如果用户问“如果我选择另一条路呢”，默认输出 conditional scenario；只有存在合格 causal model 时才使用因果措辞。

---

## 13. Longitudinal Data Interface

产品必须支持 Person x Time 数据，不只支持孤立大事件。

事件窗口需支持：

~~~text
EVENT_OCCURRED
EVENT_NOT_OCCURRED
UNKNOWN
CENSORED
~~~

必须保存：
- forecast version；
- knowledge version；
- model version；
- window；
- action；
- exposure；
- state-before；
- outcome；
- observation provenance。

没有 negative/censored data 的集合不得用于总体 manifestation probability。

---

## 14. Multi-school Boundary

中州派保持 canonical core：

~~~text
Core Ontology
  -> Zhongzhou Adapter
  -> Qintian Adapter
  -> Heluo Adapter
  -> future adapters
~~~

不同流派：
- 可以共享 chart substrate；
- 不共享未经对齐的 rule truth；
- 不把一派经验参数静默迁移到另一派。

---

## 15. 技术升级政策

### 初期
- symbolic；
- rule graph；
- Bayesian simple models；
- GLM / survival baseline。

### 中期
- hierarchical Bayesian；
- DBN / factor graph；
- statistically valid competing risks；
- interpretable mixture model。

### 后期
- Mixture of Experts；
- GNN；
- neural state-space；
- offline RL / MPC。

每次升级必须提供：
- simpler baseline；
- held-out improvement；
- calibration comparison；
- traceability impact；
- failure cases。

---

## 16. 产品安全边界

本系统可以用于：
- symbolic interpretation；
- uncertainty-aware forecasting research；
- personal reflection；
- scenario comparison。

不得把命理模型包装成：
- 医学诊断；
- 法律意见；
- 投资保证；
- 高风险专业决策替代。

健康等 domain 的 manifestation label 只能表示传统模型中的候选应象/研究标签，不能作为现实医学判断。

---

## 17. 近期实现顺序

~~~text
PL2Q
  contextual valence / pattern contract
  BAIGUAN_SUPPORT_PROFILE
       ↓
PL3-N
  NatalStateProfile
       ↓
PL3-T
  TemporalEnvironmentProfile
       ↓
PL3-S
  StateBelief
       ↓
PL3-M
  ManifestationDistribution
       ↓
PL4/PL5
  blind benchmark / calibration
~~~

不在 PL3-N 未稳定前直接开发“AI 流年铁口直断”。


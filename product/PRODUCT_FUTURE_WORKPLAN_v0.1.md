# Product Future Workplan v0.1

状态：**EXECUTION DECOMPOSITION — DERIVED FROM PRODUCT_ROADMAP v0.3**

本文件不替代 `PRODUCT_ROADMAP.md`、`product/PRODUCT_ARCHITECTURE.md` 或 `product/DYNAMIC_INFERENCE_ARCHITECTURE_v0.1.md`。

它只把既有 PL1–PL9 总路线拆成产品侧可连续执行的 work units，并记录当前依赖。

## 1. 当前状态

- PL1 Chart Trust：COMPLETE / FROZEN；
- PL2 Executable Canonical Knowledge：主干已可运行，Human Gate v0.1 已冻结；
- PL3-N Natal Prior：核心、wealth provider、domain registry、fixture benchmark 已完成；
- Career provider：等待知识侧 CA09 closure + CA04–CA08 schema repair；
- PL7 minimum data-entry loop：v0.2 interval-time bridge 完成；
- PL3-T TemporalEnvironmentProfile core：完成；
- PL3-T Existing temporal asset adapter：完成；
- PL3-T Natal × Temporal reaction compiler：完成（production registry 等待 KB-WP07B structured normalization）；
- PL3-T Event-relative window support：完成，仅实现 HG-P07 批准的 `MIGRATION_FIRST_THREE_YEARS`；
- PL3-T Temporal fixture benchmark：完成；
- PL3-T TEMPORAL EvidencePackage namespace：完成；
- 下一主工作单元：`PRODUCT_PL3S_ACQUIRED_STATE_SCHEMA_V0_1`。

## 2. 主线执行顺序

~~~text
PL3-T Temporal Environment
  -> PL3-S Personal State Observer
  -> PL3-M Manifestation Router
  -> PL4-A Internal Fidelity Benchmark
  -> PL4-B Predictive Blind Benchmark
  -> PL5 Empirical Calibration
  -> PL6 Product UX hardening
  -> PL8 Multi-school / Production
  -> PL9 Conditional Scenario / Decision Support
~~~

PL7 Longitudinal Data Flywheel 作为并行轨长期运行，不替代主线。

## 3. PL3-N remaining work

### PL3N-C1 Career canonical repair re-audit

触发条件：知识侧完成 CA09 final closure 与 CA04–CA08 schema repair。

交付：
- readiness re-audit；
- row-count / source-span / schema validation；
- executable-normalization eligibility decision。

### PL3N-C2 Career executable normalization

只处理 source-reviewed reusable rows；case-support-only 不自动升级。

### PL3N-C3 CareerNatalDomainProvider

接入 generic NatalDomainProviderRegistry。

### PL3N-X Multi-domain expansion

按知识侧宫位 closure 逐宫增加 provider，不以“十二宫全部完成”阻塞已成熟 domain。

## 4. PL3-T — Temporal Environment Engine

### PL3T-01 TemporalEnvironmentProfile core

定义：target time、active temporal layers、transformation facts、activation / strengthen / weaken / transform、conflicts、source provenance。

硬边界：E_t 是 environment，不是 outcome。

### PL3T-02 Existing temporal asset adapter

复用 PL1 已验证的 decade/year/month/day/hour chart facts 和现有 temporal schemas，不重新发明排盘。

### PL3T-03 Natal × Temporal reaction compiler

把 source-backed temporal reaction 映射到 NatalStateProfile；保留 state dependence 与 nonlinear interaction。

### PL3T-04 Event-relative window support

仅实现已批准、source-explicit 的 event-relative windows；不得泛化成任意事件计时器。

### PL3T-05 Temporal fixture benchmark

验证 same natal + same time + same knowledge version -> same TemporalEnvironmentProfile。

### PL3T-06 Temporal EvidencePackage integration

EvidencePackage 增加 TEMPORAL evidence namespace。

## 5. PL3-S — Personal State Observer

### PL3S-01 AcquiredState schema

定义 relationship/career/resource/relocation/commitment/exposure 等现实状态容器；状态是 acquired，不属于 natal truth。

### PL3S-02 Deterministic state updater

由 confirmed observation/action/context 更新 state，不使用黑盒推断。

### PL3S-03 Missingness / contradiction model

显式记录 UNKNOWN、conflict、observation confidence。

### PL3S-04 Bayesian belief v0.1

只在离散/稀疏反馈层做简单 posterior；不默认 particle filter。

### PL3S-05 StateBelief benchmark

固定 observation sequence -> deterministic / reproducible state belief。

## 6. PL3-M — Manifestation Router MVP

### PL3M-01 Manifestation ontology adapter

消费知识侧 WP06B/WP06C；没有 ontology 的 domain fail closed。

### PL3M-02 Source-supported possibility router

输出 `SOURCE_SUPPORTED_POSSIBILITY`，不输出伪概率。

### PL3M-03 Context gate

把 N + E_t + S_t + A_t + C_t 组装为 routing context。

### PL3M-04 Probability interface

预留 empirical calibration plugin；没有 calibrated model 时 probability=null。

### PL3M-05 Personalized posterior interface

与 population probability 永久分 namespace。

## 7. PL4-A — Internal Fidelity Benchmark

测：chart reconstruction、canonical rule trace、author-case reconstruction、temporal fidelity、conflict preservation、determinism。

教材/书中案例优先属于本层，不等于现实预测 ground truth。

## 8. PL4-B — Predictive Blind Benchmark

### PL4B-01 Target preregistration

冻结 target、window、model version、available context、forbidden leakage。

### PL4B-02 Baselines

至少比较：context-only、pure LLM、RAG、flat rules、symbolic natal、natal+temporal、calibrated model、personalized model。

### PL4B-03 Metrics

Brier/log loss、calibration、coverage-at-confidence、ranking（适用时）、abstention。

### PL4B-04 Incremental value

必须比较 `Context` vs `Context+Natal` vs `+Temporal` vs `+Personal history`。

## 9. PL5 — Empirical Calibration Program

### PL5-A Frequency baseline

学习 P(M|Q)，只作最简单经验 baseline。

### PL5-B Context-conditioned model

学习 P(M|Q,S,C)，优先 GLM / multinomial / event-history；只有满足定义才使用 competing risks。

### PL5-C Hierarchical Bayesian

population -> cohort/context -> individual，强 shrinkage 起步。

### PL5-D Incremental predictive value

只有稳定 out-of-sample improvement 才可声称 chart features 带来增量信息。

### PL5-E Causal/action analysis

关联模型不升级为因果建议；需独立 causal assumptions / identification gate。

## 10. PL6 — Product UX

### PL6-A Natal Mode

纯 N；无需反馈。

### PL6-B Blind Forecast Mode

只使用预先允许输入；用于研究和真实性 benchmark。

### PL6-C Personalized Forecast Mode

加入 S_t / A_t / C_t / past feedback。

### PL6-D Three-layer explanation

普通 / 高级 / Expert-Debug；Expert 层显示 source、conflict、calibration、uncertainty。

### PL6-E Contrastive explanation

回答“为什么 A 而不是 B”，分 canonical / temporal / personal / empirical / counterevidence。

## 11. PL7 — Longitudinal Data Flywheel（并行长期轨）

已完成最低入口：
- observation v0.1/v0.2；
- prospective target lock；
- neutral check-in；
- check-in -> observation bridge；
- negative / unknown / censored；
- interval event time。

后续：

### PL7-Q1 Data quality audit

重复记录、窗口冲突、target ontology version、follow-up completeness、MNAR flags。

### PL7-Q2 Prospective cohort manager

创建/关闭 windows、follow-up completeness、dropout/censoring。

### PL7-Q3 Raw-text parser candidate layer

LLM 只生成 candidate，必须用户确认 + deterministic validation。

### PL7-Q4 Calibration-ready corpus builder

按 model/knowledge/ontology version 冻结训练快照。

### PL7-Q5 Privacy / deletion / consent boundary

真实产品化前必须完成；person_key 与 raw narrative 分存。

## 12. PL8 — Multi-school / Production

中州派保持 canonical core；钦天、河洛等通过 adapter 加入。

工作单元：school adapter contract、school-attributed evidence、conflict-preserving comparison、school-specific calibration namespace、production versioning/rollback。

## 13. PL9 — Conditional Scenario & Decision Support

### PL9-01 Scenario simulator

比较维持现状 / 行动 A / 行动 B 的条件轨迹，不宣称因果。

### PL9-02 User utility / multi-objective contract

禁止 universal 吉凶 reward；支持用户目标与 Pareto trade-off。

### PL9-03 Causal readiness gate

只有识别条件满足后，才允许“做 A 比 B 更好”的因果措辞。

### PL9-04 MPC prototype

在 predictive calibration、state estimation、causal assumptions 都达标后才启用。

### PL9-05 Offline RL

最晚期可选项；需要可信 action/outcome 数据、policy evaluation 与 safety guard。

## 14. AI 技术升级顺序

~~~text
Symbolic / deterministic
-> interpretable statistical baseline
-> Bayesian / hierarchical Bayesian
-> causal evaluation
-> Mixture-of-Experts
-> GNN / neural state-space (only if data justifies)
-> MPC / offline RL (last)
~~~

每次复杂化都必须有 simpler baseline、held-out improvement、calibration comparison、traceability audit。

## 15. 永久边界

1. Natal Prior 不接受经验反馈改写；
2. Temporal Environment 不等于事件；
3. source possibility != empirical probability != personalized posterior；
4. action != disturbance；context != observation；
5. negative sample 必须完整观察；
6. Blind 与 Personalized 永久分开；
7. LLM 不拥有 rule truth 或 probability truth；
8. empirical mismatch 只能触发 Knowledge Gap Report，不能静默改 source；
9. source 未给出的 numeric weight 不得产品侧拍脑袋补；
10. 高风险专业领域不允许把命理输出替代医学/法律/金融专业判断。

## 16. 当前下一步

PL3-T v0.1 主线六个工作单元已经完成：core、Temporal Asset Adapter、Natal × Temporal Reaction Compiler、单一批准的 Event-relative Window、Temporal Fixture Benchmark、TEMPORAL EvidencePackage namespace。当前主线正式进入：

**PRODUCT_PL3S_ACQUIRED_STATE_SCHEMA_V0_1**

PL3-S 开始承载现实中已经发生并确认的 acquired state，继续与 Natal Prior 和 Temporal Environment 分层。production temporal reaction registry 在 KB-WP07B structured normalization 到位前继续保持为空，不阻塞 PL3-S。PL7 后续质量工程继续并行；Career provider 等知识侧 unblock 后插回 PL3-N domain expansion，不打乱主线。

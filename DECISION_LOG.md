# DECISION_LOG.md

All important conceptual decisions are recorded here.

## Frozen decisions

### D-001 — Paper-1 scope
**Decision:** Use Zhongzhou-school theory as the formal core.  
**Status:** FROZEN  
**Rationale:** Limits model complexity and school mixing; permits later ablation/extension.

### D-002 — Qi operational definition
**Decision:** Treat qi as a latent state representation, not as a proven physical energy.  
**Status:** FROZEN

### D-003 — No arbitrary empirical weights
**Decision:** Before system identification, use symbolic parameters, signs, order constraints, and qualitative classes rather than invented continuous weights.  
**Status:** FROZEN

### D-004 — Internal/external validity separation
**Decision:** Paper 1 evaluates formalization fidelity and reproducibility, not real-world predictive accuracy.  
**Status:** FROZEN

### D-005 — Nonlinear response assumption
**Decision:** Do not assume that star-system or temporal effects are simple additive linear combinations. Preserve state-dependent and interaction effects when texts require them.  
**Status:** FROZEN

### D-006 — Multi-agent method
**Decision:** Use artifact-centered role separation with producer/reviewer gates rather than training separate agents or allowing uncontrolled agent debate.  
**Status:** FROZEN

### D-007 — Rule schema v0.2
**Decision:** Separate latent-state change from favorable/unfavorable contextual valence, and separate source wording from research normalization.  
**Status:** FROZEN  
**Rationale:** The 100-rule pilot showed that a single positive/negative field conflates dynamics and evaluation.  
**Approved at:** G1

### D-008 — G2 气机本体架构批准
**Decision:** 批准 L0-L4 分层气机本体；内在状态、关系网络、场景投影、评价层分离；允许非单调变量；阴阳五行暂作为结构底座；QI-01 至 QI-15 与 QR-01 至 QR-04 作为可修订 v0.2 候选集，而非最终气全集。  
**Status:** FROZEN（架构原则）；候选维度 PROVISIONAL  
**Approved at:** G2

### D-009 — G3 十四正曜气核结构批准
**Decision:** 批准十四正曜统一采用 L0结构底座 + L1内在气核 + L2关系气核 + 条件修正层；单星气核视为基态而非完整解释；本命与运限表现分层；六十星系阶段必须允许非线性交互项。  
**Status:** FROZEN（结构与方法原则）；具体维度映射 PROVISIONAL  
**Approved at:** G3

### D-010 — G4 六十星系交互架构批准
**Decision:** 批准六十星系完整索引与统一交互架构；principal mode 属于中尺度模态，不自动升格为 primitive qi；采用 base composition + interaction delta + mode + context gates；Delta_s 仅为未解释交互残差；z_s 为由完整星系状态派生的模态；允许混杂/多模态表示但暂不数值化；QI-16/QI-17仅进入候选池。  
**Status:** FROZEN（结构与方法原则）；具体交互函数与候选维度 PROVISIONAL  
**Approved at:** G4

### D-011 — G5 状态空间与结构能观性架构批准
**Decision:** 批准 Paper 1 主模型采用“固定原局本质 + 时序外生输入 + 状态依赖反应”；十二宫采用局部节点 + 全局稀疏图；外生时序输入、人类行为输入、外部扰动分开；气→象→事分层；Paper 1 只做结构能观性/潜在不可辨识审计；递归动力学、observer、controllability、optimal control 只作为未来接口；QI-16 暂不升格，QI-17 保持高优先候选。  
**Status:** FROZEN（Paper-1 核心架构）；连续参数与递归扩展 PROVISIONAL  
**Approved at:** G5

### D-012 — G6 论文结论与认识论边界批准
**Decision:** 批准 Paper 1 的最终认识论边界：只主张中州派知识在当前语料范围内可被形式化为可执行、可审计、可追溯的层级潜状态系统；内部形式化验证不等于现实预测验证；“气”仅作操作性潜状态；现代控制/灰箱/hybrid/observer 等属于形式化工具或未来研究接口；不把预测准确或证明命理有效列为本文贡献。  
**Status:** FROZEN（Paper-1 结论与表述边界）  
**Approved at:** G6

### D-013 — Phase II 中州派完整知识库扩展
**Decision:** 在不改变 G1–G6 已冻结 Paper-1 架构的前提下，启动“中州派知识库工程”：对初级讲义、深造讲义上/下册及可合法使用的中州派补充材料进行更完整的规则抽取、条件归一化、跨章冲突审计、案例关联与可生成推演规则构建。知识库的“完整”定义为：源文规则覆盖 + 生成规则覆盖 + 案例/例证覆盖，而不是穷举所有理论组合。  
**Status:** ACTIVE PHASE-II PROGRAM  
**Rationale:** 六十星系原文明确指出，若逐一枚举星系×十二宫×辅佐煞化等组合将爆炸式增长，因此完整知识库必须采用“原子规则 + 条件算子 + 生成式组合 + provenance”的架构。  
**Approved after:** G6

## Pending decisions

### P-001 — Candidate qi ontology dimensionality
The 100-rule pilot is complete. Next step is to propose Qi Ontology v0.1 for G2.

### P-002 — Representation of five-element structure
Candidates: 5D simplex/vector + directed generation/control relations; graph-algebra representation.

### P-003 — Palace state organization
**Resolved at G5:** 采用 12 个局部宫位本质 + 全局稀疏图。

### P-004 — First formal state equation
Candidate:
`x_(t+1) = F_theta(x_t, u_t^astro, G_t)`
Need ontology and star-system extraction before choosing decomposition.

### P-005 — Observation-path support / future structural observability
**Resolved at A1:** 当前只报告 observation-path support 与可区分性启发式审计，不称 structural observability；真正结构能观性须等待正式状态—输出结构图及 generic-rank / matching 条件。

### P-006 — Modifier operator order
算子是否交换、作用顺序、饱和形式仍开放，待更完整规则或数据。

### P-007 — Will-control / persistence split
**Resolved at A1:** 原 QI-17 persistence/resilience 合并候选废止；QI-17-CAND=意志控制强度，QI-18-CAND=毅力/持续性，恢复力/韧性仅保留 derived/system-level。

### P-008 — Star-system mode representation
连续/离散/概率混合形式留待后续数据决定。

### P-009 — Parameter identifiability
Paper 2 需要处理 star-core / Delta / modifier / projection 参数混淆。

### P-010 — Recursive dynamics necessity
是否需要 x_(t+1) 递归状态由纵向命例数据检验。

### D-014 — Gate A0 去污染与双层认识论审计
**Decision:** 批准 source_epistemic 与 normalization_epistemic 分离；批准 review_status 四级化（MODEL_EXTRACTED / MODEL_SELF_REVIEWED / SOURCE_SPAN_VERIFIED / HUMAN_VERIFIED）；历史仅由 GPT 生成并自审的 reviewed 默认迁移为 MODEL_SELF_REVIEWED；批准 L1/L2 状态算子与 L3 projection 重新分层；批准 deterministic linter 作为进入 main 的强制 schema gate。  
**Status:** FROZEN（审计与质量控制原则）；具体规则语义修订仍须 source-span 复核  
**Approved at:** Gate A0


### D-015 — Gate A1 全文反向本体审计批准
**Decision:** 批准保留 G2 的 L0-L4 分层架构并以全文语料重新拟合具体 QI/QR evidence 与边界；批准 QI-16「目标导向性」正式升格为 L1 状态；否决原合并式 QI-17「持续意志/韧性」并拆为「意志控制」与「毅力/持续性」两个独立候选，恢复力暂留 derived/system-level；批准保留 QI-14 但收窄为「信息/状态遮蔽—显露」，与 QI-01 发射—收敛分离证据；批准 G3-R，以 direct-star > modifier > system-context 的优先级重拟合十四正曜气核，禁止为适配旧 ontology 强填气核；批准将当前路径计数式 structural observability 改称 observation-path support，严格结构能观性留待正式状态—输出结构图后。
**Status:** FROZEN（A1 方法与边界）；QI-17/QI-18 候选是否升格仍 PROVISIONAL
**Approved at:** Gate A1


### P-011 — Acquired/history state for source-explicit path dependence
**Resolved at A2-R1.** See D-016 below.

### D-016 — Gate A2-R1 typed history-memory architecture
**Decision:** 批准在固定原局本质 `E` 之外新增 source-gated 历史记忆层，但不得把所有路径依赖混成单一自由向量。Paper 1 将历史记忆分为两类：`ACQUIRED_DISPOSITION`（后天形成/强化/固化的倾向）与 `PATH_DEPENDENT_GATE`（过去关键阶段/事件对后续规则资格或分支的门控）。只有 source-explicit persistence/path-dependence 证据才能写入历史记忆；无明确 persistence 证据时不得假设永久保存。Paper 1 只实现 symbolic/ordinal/source-gated transition，不引入任意连续记忆权重、衰减率、学习率或一般神经网络递归。一般连续递归动力学继续保留为 Paper 2+ hypothesis。
**Correction:** Gate 审核回源发现 `ZZ-SYS-38-034` 的“七杀运检验先前意志结构”归一化不受对应源文支持；该 raw canonical 保留审计历史但退出有效推理。系统 38 的路径依赖由已存在且回源匹配的 `ZZ-SYS-38-021`（武曲破军考验性大限影响后运）承接。
**Status:** FROZEN（A2-R1 架构与边界）
**Approved at:** Gate A2-R1
**Approved by:** PI



### D-017 — HG-P07-TEMPORAL-01 event-relative relocation window
**Decision:** 批准方案 A。迁移宫对“远地定居后头三年”的明示规则，形式化为一个极窄、来源约束的事件相对时间窗：仅当“远地定居事件已确认”且 `1 <= years_since_distant_relocation <= 3` 时，迁移宫对迁移后总体趋势取得 PRIMARY 路由优先级；其他宫位仍按通常流年命宫轮排。该窗口不改写原局本质，不进入 A2-R1 历史记忆，不设置数值权重、衰减函数或概率，也不得泛化为任意事件计时器。
**Status:** FROZEN（HG-P07-TEMPORAL-01 Option A）
**Approved at:** HG-P07-TEMPORAL-01
**Approved by:** PI

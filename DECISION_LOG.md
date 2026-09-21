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

## Pending decisions

### P-001 — Candidate qi ontology dimensionality
The 100-rule pilot is complete. Next step is to propose Qi Ontology v0.1 for G2.

### P-002 — Representation of five-element structure
Candidates: 5D simplex/vector + directed generation/control relations; graph-algebra representation.

### P-003 — Palace state organization
Candidates: 12 local latent states vs global latent state with palace projection operators.

### P-004 — First formal state equation
Candidate:
`x_(t+1) = F_theta(x_t, u_t^astro, G_t)`
Need ontology and star-system extraction before choosing decomposition.

### P-005 — Structural observability criterion
To define after observation/projection schema exists.

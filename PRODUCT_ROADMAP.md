# 产品化路线图 — Product-First Program v0.2

状态：ACTIVE  
生效日期：2026-10-04  
主目标：在继续完成中州派知识工程的同时，把项目推进为**排盘可靠、推理稳定、外部基准可测、证据链可审计、用户体验可用**的产品。

## 1. 目标优先级

从本版本起，项目采用双轨：

1. **产品主轨**：准确性、可靠性、可解释性、可复现性、用户体验优先；
2. **学术副轨**：把产品建设自然产生的本体、规则系统、benchmark、ablation、系统辨识结果整理为论文。

学术表述不得阻碍产品工程，但产品也不得通过伪造权重、混合证据层或回看答案来制造“高准确率”。

## 2. 五类准确性

产品不得使用单一“准不准”指标。

### A. 排盘准确性
- 公历/农历转换
- 闰月、早晚子时
- 真太阳时与夏令时口径
- 星曜、宫位、四化
- 大限/流年/流月/流日/流时

要求：确定性计算；LLM 不参与排盘事实生成。

### B. 规则还原准确性
给定命盘结构，系统是否激活了正确的中州派规则、条件、算子和宫位投影。

### C. 推理一致性
同输入、同知识版本必须产生同一 active-rule graph 与兼容的语义结论；LLM 只能表达，不得自行补规则。

### D. 外部案例准确性
只在系统未见过答案的真实案例/公开 benchmark 上统计。训练、规则修订、提示优化与测试集必须隔离。

### E. Calibration / Abstention
产品需要区分：
- HIGH_CONFIDENCE
- MEDIUM_CONFIDENCE
- LOW_CONFIDENCE
- CONFLICTED
- INSUFFICIENT_EVIDENCE

高置信集合应在外部测试上显著优于低置信集合，否则置信机制无效。

## 3. 产品技术主链

```text
birth input
  -> deterministic chart engine
  -> normalized chart snapshot
  -> natal-state builder
  -> star cores / system modes / palace graph
  -> modifier + transformation engine
  -> temporal resolver
  -> typed history memory
  -> evidence-first inference graph
  -> confidence/conflict resolver
  -> EvidencePackage
  -> LLM verbalizer
  -> user-facing explanation
```

硬原则：**LLM 位于推理链末端，不拥有底层规则选择权。**

## 4. 产品工作包

### PROD-P0：竞品与依赖审计
- 建立 GitHub/产品 registry；
- 许可证台账；
- 功能矩阵；
- 可复用能力与不可直接复用边界；
- 持续跟踪竞品版本变化。

### PROD-P1：双/多排盘引擎交叉验证
目标不是把“多数一致”当真理，而是自动发现差异。

```text
our chart engine
      \
       -> normalized snapshot -> diff -> disagreement ledger
      /
external engine adapter(s)
```

每个差异最终归类为：
- OUR_BUG
- EXTERNAL_BUG
- SCHOOL_DIFFERENCE
- CONFIG_DIFFERENCE
- INPUT_AMBIGUITY
- UNRESOLVED

首批参考：iztro、Renhuai123/ziwei-doushu。

### PROD-P2：中州派知识库继续 closure
与现有 KB-WP05/06 并行推进；不得为产品速度降低 provenance 标准。

### PROD-P3：Inference MVP
先做窄域 end-to-end：
- 本命；
- 一个大限；
- 一个流年；
- 优先事业/财帛两个主题。

最小链路：
```text
chart -> rules -> latent states -> modes -> operators
-> palace projection -> temporal reaction -> evidence package
```

### PROD-P4：Benchmark Harness
至少支持：
- 内部教材 case reconstruction；
- Fate-Bench 等外部盲测；
- pure LLM baseline；
- RAG baseline；
- flat-rule baseline；
- symbolic engine；
- symbolic engine + LLM verbalizer。

### PROD-P5：真实案例校准
只在版本冻结后的训练/开发集合上学习可学习参数；测试集保持盲态。

### PROD-P6：产品 UI/UX
三层解释：
1. 普通用户摘要；
2. 高级用户推理链；
3. 专家/debug rule + source trace。

### PROD-P7：数据飞轮
结构化、可撤回、可匿名反馈；优先可验证事件，不用模糊“感觉准”。

### PROD-P8：学术输出
在产品证据成熟后生成：
- formalization paper；
- benchmark/ablation paper；
- empirical calibration/system-identification paper。

## 5. 竞品借鉴原则

### 可以复用
- MIT/兼容许可代码，在台账中记录版本与用途；
- CC BY 数据，按协议署名；
- API/schema/测试方法/交互思路；
- 开放 benchmark。

### 不可以偷换
- 外部项目的断语不能自动升级为中州派 canonical truth；
- 外部引擎与本项目一致不等于“真实正确”；
- GPL 代码不得在不了解传播义务时复制进入未来闭源产品；
- 托管模型的不可见内部实现不能被当成可复现实验。

## 6. 产品成功判据

产品真正形成竞争力时，应同时满足：

- chart regression：核心排盘域有系统性双引擎差异审计；
- source trace：关键判断可追至 rule/source；
- deterministic reasoning：同版本输入稳定；
- conflict-aware：冲突不被 LLM 静默消解；
- benchmarked：有外部盲测；
- calibrated：高置信预测优于低置信预测；
- explainable：可回答“为什么这样判断”和“为什么不是另一种判断”；
- reproducible：版本、模型、知识库和测试集可复现。

## 7. 与 Phase II 的关系

现有 Phase II 不停止。当前 KB-WP05 十二宫投影语料继续执行。

产品轨不是另起炉灶，而是把已有：
- star core；
- sixty-system mode；
- operator catalog；
- typed history；
- palace projection；
- provenance；

尽早接成可运行系统，让案例和 benchmark 反向暴露知识工程缺口。


## 8. 执行责任边界（2026-10-04 冻结）

产品与知识抽取采用并行会话，避免一个会话同时承担大规模 source review 与产品工程。

- **本产品会话**：只负责 productization、chart/adapters、regression、Rule Runtime、Inference MVP、EvidencePackage、benchmark、calibration、UI/UX、产品数据与发布治理。
- **其他知识工程会话**：继续负责 source-span review、十二宫 projection corpus、规则抽取、回源核验与知识库 closure。
- 产品会话只消费已经进入 GitHub canonical state 且满足 provenance/review gate 的知识资产；不得在产品代码里偷偷补写传统规则。
- 知识工程会话不得因为产品需要而降低 provenance 标准或回看 benchmark answer。

## 9. 产品层八阶段执行路线

### PL1 — Chart Trust Layer
目标：把排盘从“能用”提升到“可审计、可回归、边界可解释”。

交付：
- Normalized Chart Contract；
- deterministic regression seeds；
- calendar / temporal boundary registry；
- multi-engine diff CI；
- mismatch ledger；
- ambiguity registry；
- Chart Trust Report v1.0。

### PL2 — Executable Knowledge
目标：把 canonical knowledge 编译成产品可执行的 Rule IR。

最小链路：
```text
source span -> reviewed atomic rule -> condition -> operator
-> target state -> executable rule -> trace
```

任何运行时规则必须保留 rule_id、source pointer、review status 与 school namespace。

### PL3 — Inference MVP
第一版只做窄域端到端：
- 本命；
- 一个大限；
- 一个流年；
- 事业 + 财帛；
- EvidencePackage；
- deterministic confidence/conflict 输出。

MVP 在没有 LLM 的情况下也必须能输出结构化结论；LLM 只负责 verbalization。

### PL4 — Evaluation Harness
同一测试集并行比较：
- Pure LLM；
- RAG；
- Flat rules；
- Symbolic engine；
- Symbolic + LLM。

至少统计 Accuracy、High-confidence Accuracy、Coverage、Consistency、Traceability、Conflict Detection 与 Calibration。

### PL5 — Empirical Calibration
严格分层：
- Layer A：Traditional Knowledge；
- Layer B：Empirical Calibration；
- Layer C：User/Context Adaptation。

B/C 不得回写或篡改 A。

### PL6 — Product UX
三层界面：
1. 普通用户：结论 + 核心证据 + 不确定性；
2. 高级用户：原局/星系/四化/宫位/时序链；
3. Expert/Debug：Rule ID / source / operator / state delta / conflict / version。

### PL7 — Data Flywheel
只收结构化、带时间窗、可验证的事件反馈；禁止把“感觉很准/不准”直接当训练标签。

### PL8 — Multi-school / Production
中州派保持 canonical core；其他体系以 Adapter 接入：
```text
Core ontology
  ├─ Zhongzhou Adapter
  ├─ Qintian Adapter
  ├─ Heluo Adapter
  └─ other adapters
```

产品输出区分 cross-school consensus 与 school-specific disagreement。

## 10. 边界歧义与多模型状态

B02-B 后，产品正式承认某些输入不是单一确定状态。晚子时是第一类：

```text
SCHOOL_SENSITIVE_BOUNDARY
  -> same-day candidate
  -> next-day candidate
  -> dual-chart/composite candidate
```

排盘层负责保留候选，不负责伪造“唯一真值”；后续可由 school selection、source evidence、history evidence 与 empirical calibration 做显式 resolution。

## 11. 当前立即执行顺序

1. 关闭 P1 B02-B 并冻结子时 boundary policy；
2. 执行 P1 B02-C：大限/小限/流年/流月/流日动态切换边界；
3. 形成 P1 FINAL acceptance + Chart Trust Report v1.0；
4. 开始 PL2 Rule Runtime；
5. 立即进入 PL3 首个事业/财帛 Inference MVP；
6. MVP 一跑通就建立 PL4 benchmark harness，而不是等十二宫全部抽取完成。

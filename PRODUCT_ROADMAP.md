# 产品化路线图 — Product-First Program v0.1

状态：ACTIVE  
生效日期：2026-10-03  
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

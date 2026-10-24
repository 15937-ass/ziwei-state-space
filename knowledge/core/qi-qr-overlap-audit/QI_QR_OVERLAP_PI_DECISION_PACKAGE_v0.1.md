# QI/QR 八组重叠审计：PI 决策包 v0.1

状态：PROPOSAL_ONLY_NOT_CANONICAL  
关联工作单：[Issue #735](https://github.com/15937-ass/ziwei-state-space/issues/735)  
依据审计：[QI/QR 重叠对来源与层级审计 v0.1](QI_QR_OVERLAP_PAIR_AUDIT_v0.1.md)  
Option C 背景：[最小元数据契约提案 v0.1](../wp06b/OPTION_C_METADATA_CONTRACT_PROPOSAL_v0.1.md)

## 1. 决策范围

PI 已同意采用以下研究处理方向：

1. 不因词面相似、共享规则 ID 或概念相关而自动合并。
2. 不因名称不同或没有共享规则 ID 就声称概念已被证明正交。
3. 先定义语义问题和证据角色，再讨论映射。
4. 保留来源原文的条件、范围、模态与比较对象。
5. 继续保留 QI-17-CAND / QI-18-CAND 的候选身份。
6. 本工作只形成决策包与契约修订提案；不修改 canonical ontology、规则源行、Product/runtime、注册表、锁或消费权限。

本文的“建议”是本次 PI 已授权的研究方向的具体化，不等于已批准 canonical ontology 修改。所有维度定义改动均为提案，须另行通过正式契约/本体实施门。

## 2. 证据与方法边界

### 2.1 项目内证据

主要输入是当前 main 的：
- QI/QR 八组审计报告；
- knowledge/qi_ontology.yaml 的现有定义、层级和证据规则；
- REVIEW_SCHEMA_v0.3.md 对 source_epistemic、normalization_epistemic 与 review_status 的区分；
- KB_SCHEMA.md 中 operator、target_type、projection evidence、Conflict object 等现有机制；
- 两批 direct-star 来源复核及十四主星矩阵。

本文件不重复抄录古籍长段原文。具体规则 ID 与来源定位以八组审计报告为准；其 evidence_text 只是摘要，不代替原始来源跨度。特别是 ZZ-PJ-X06 的条件差异继续未解决，本包不改写该规则。

### 2.2 外部方法论依据（只借用方法，不作为紫微斗数的实证证明）

- Noy, N. F. & McGuinness, D. L. (2001), *Ontology Development 101*. 迭代建模、根据用途与能力问题定义概念：https://protege.stanford.edu/publications/ontology_development/ontology101-noy-mcguinness.html
- W3C, *SKOS Simple Knowledge Organization System Reference*. 区分 exactMatch、closeMatch、broader/narrower 与 relatedMatch；语义相近不等于完全等价：https://www.w3.org/TR/skos-reference/
- Cronbach, L. J. & Meehl, P. E. (1955), *Construct Validity in Psychological Tests*. 构念须放在理论关系网络中，并接受证据检验：https://doi.org/10.1037/h0040957
- Campbell, D. T. & Fiske, D. W. (1959), *Convergent and Discriminant Validation by the Multitrait-Multimethod Matrix*. 区分效度需要证据，不是仅靠定义不同：https://doi.org/10.1037/h0046016
- House, J. S., Umberson, D. & Landis, K. R. (1988), *Structures and Processes of Social Support*. 区分社会关系结构/整合与支持功能：https://doi.org/10.1146/annurev.so.14.080188.001453
- Duckworth, A. L. et al. (2007), *Grit: Perseverance and Passion for Long-Term Goals*. 作为毅力/长期目标研究的参考，不代表“毅力”已在本项目中获得独立效度：https://doi.org/10.1037/0022-3514.92.6.1087
- Basic Formal Ontology (BFO 2020). 为区分实体、过程、倾向、功能与角色提供上层建模参考：https://github.com/BFO-ontology/BFO-2020

限制：外部文献只帮助我们改善建模方法。它们不证明紫微斗数概念的真实性、唯一解释、心理测量效度或现实预测准确率。当前项目没有可支持统计区分效度结论的独立测量数据；不得捏造相关系数、因子载荷、HTMT、正交分数或权重。

## 3. 八组逐项处理提案

### OVERLAP-01 — QI-01 / QI-14

**建议处置：保留为不同候选维度，不合并。**

- QI-01 当前关注气机向外扩散/显发与向内潜藏/收束的动力学方向。
- QI-14 当前关注信息、意图、能力或状态被遮蔽或显露、可辨识的程度。
- 语义边界：方向/收束不是可见性；潜藏不自动等于遮蔽，外放也不自动等于显露。
- 映射要求：同一规则若支持两者，分别写出映射理由和来源语义；不将一次源文引用计为两份独立证据。
- 后续证据：寻找同一来源内能区分“收敛但显露”与“外放但遮蔽”的反例或对照。找不到时维持未决，不宣称正交。
- canonical 影响：无。

### OVERLAP-02 — QI-03 / QI-04

**建议处置：保留两者；提议收窄 QI-04 的定义，不立即改 canonical 名称或定义。**

- QI-03 回答“结构是否发生迁移、转换或重组”。
- QI-04 回答“相对既有结构，是偏向维护还是主动突破”。
- 当前 QI-04 名称中的“冲刺”可能还表达速度、行动强度或推进方式，不一定与守成/结构突破位于同一语义轴。
- 提案：将 QI-04 的核心语义收窄为“守成—结构突破”；“冲刺/推进强度”仅在来源确实表达时作为独立描述或作用修饰，不创建新 QI ID。
- 映射要求：破军“冲锋/不主退守”等共享证据应标记为多义/复合候选；同一条规则同时出现在 QI-03 与 QI-04，不证明两者等价或独立。
- 后续证据：寻找“变化但非开创”与“维持结构但主动创新”的来源案例。
- canonical 影响：无；该定义调整需另行审批。

### OVERLAP-03 — QI-02 / QI-15

**建议处置：保留概念区分；对 QI-15 强制记录作用主体、对象、条件与语义角色。**

- QI-02 描述刚柔状态/作用方式。
- QI-15 描述缓冲、调节、吸收冲突或化解极端的能力/作用。
- 核心风险：某星曜使另一星曜的刚烈减弱，首先可能是外部 modifier 或星系交互，不自动证明被修饰星曜本身具有缓冲能力。
- 每项证据至少记录：bearer/作用主体、target/作用对象、condition/条件、role/直接性质/修饰功能/交互结果，以及来源与归一化的认识论状态。
- 复用 KB_SCHEMA 既有 operator（如 weaken、transform、couple、condition）表达可表达的关系；不因这组审计直接创建全局共享 primitive。
- 后续证据：寻找能够支持单体缓冲能力、外部修饰和交互结果三者差异的独立来源。
- canonical 影响：无；不接受现有双重映射。

### OVERLAP-04 — QI-08 / QI-06

**建议处置：保留两者；提议收窄 QI-06 的语义边界。**

- QI-08 描述意图转为主动行动、执行和实际推进的驱动力。
- QI-06 当前被定义为从迟疑到适度审慎再到躁决的非单调激活度；“审慎”带有决策质量/评价色彩，可能不适合与决策启动/迟疑放在同一条描述轴中。
- 提案：将 QI-06 的核心问题收窄为“决策启动/迟疑—决断方式”；把“审慎是否恰当”视为单独的语境/评价描述，不立即新增正式维度，也不将其写入 QI-06 的定义轴。
- 区分要求：决得快不等于执行强；行动多不等于决策审慎；描述躁决不能自动推导出行动驱动高。
- 后续证据：分别检查决策延迟/躁决和行动启动/执行的来源例子。
- canonical 影响：无；现有 non-monotonic scalar 定义保持不变，直至正式审批。

### OVERLAP-05 — QI-04 / QI-16

**建议处置：保留两者；提议将 QI-16 的核心语义收窄为目标明确性/目标组织程度。**

- QI-04 关注维护既有结构或主动突破。
- QI-16 当前定义包含“明确目标、方向与建设性组织”；“建设性”可能把目标是否明确与目标内容/结果的价值判断混在一起。
- 提案：QI-16 主要回答“行动或资源投入是否围绕明确目标组织”；建设性/破坏性是目标内容或结果描述，不能自动等同于目标明确性。不得因此创建新原语。
- 关键来源限制：审计指出 ZZ-PJ-X06 的 canonical 条件比已核验原文更具体；原文“或”不能无依据地变成更强的合取条件。此差异继续标记 unresolved，不能靠改定义绕过。
- 后续证据：逐条核对六十星系来源条件和目标描述；条件复核通过后再评价 QI-16 映射。
- canonical 影响：无；不改写 ZZ-PJ-X06。

### OVERLAP-06 — QI-08 / QI-16

**建议处置：保留两者。**

- QI-08 回答“行动是否容易启动并推进”。
- QI-16 回答“行动是否围绕明确目标组织”。
- 高行动驱动可以用于建设、探索，也可以用于没有清楚目标或破坏性行动；目标明确也不必然代表行动驱动力强。
- 映射要求：承担困难任务、独行或行动强的描述，不能自动映射到 QI-16；明确目标的描述也不能自动映射到 QI-08。
- 后续证据：寻找行动强度相近而目标清晰度不同的来源对照。
- canonical 影响：无。

### OVERLAP-07 — QI-17-CAND / QI-18-CAND

**建议处置：保留为两个候选概念；不晋升、不分配正式 ID、不接受映射。**

- QI-17-CAND：面对诱因、欲望、情绪或压力时的自主约束与方向维持。
- QI-18-CAND：面对时间、阻力、延迟或反复挫折时持续行动的程度。
- 审计报告记录了天同巳亥相关来源对意志强弱与毅力不足的直接区分；这支持分开研究，但不自动证明跨星曜复用性或独立解释价值。
- 后续证据：复核更多独立星系/条件；检查与 QI-03、QI-06、QI-08 的边界；通过单独 PI/Human Gate 后才能考虑正式化。
- canonical 影响：无；CAND 标记必须保留。

### OVERLAP-08 — QR-01 / QR-04

**建议处置：保留两者；收窄 QR-01 的“支持”用语并拆清 QR-04 的资源状态。**

- QR-01 主要描述关系网络的嵌入、联系、协同或孤离状态。
- QR-04 主要描述可获得的支持资源。
- 提案：QR-01 定义中“支持”仅能指关系网络中的联系/协同语义，不能替代实际支持功能；正式定义需避免与 QR-04 重叠。
- QR-04 证据至少区分：资源存在、资源在条件下可用、支持实际发生。它们是不同事实，不默认新增三个 QR 维度，可先作为证据/输出角色。
- “属下众多”或“外部助力”不能单独证明关系整合、互惠或资源在具体情境下可用。
- projection-tier 证据不得与 L1/L2 直接证据等权；引用时必须标明 projection 角色。
- 后续证据：复核紫微、天梁、武曲相关规则的层级、主体和条件。
- canonical 影响：无。

## 4. 横向契约规则

1. **映射原子性**：一个规则可映射多个概念，但每个目标必须有单独理由；共享规则 ID 不能当作两份独立证据。
2. **双向谨慎**：无共享规则 ID不证明正交；共享规则 ID不证明等价。
3. **角色显式化**：区分来源断言、归一化解释、语义目标、作用主体/对象、条件/模态、证据层级、审核状态和 canonical 批准。
4. **来源条件保真**：不把“或”变成“且”、可能变成必然、结果投影变成直接性质，或模型推断变成原文断言。
5. **认识论分离**：复用 REVIEW_SCHEMA_v0.3 的 source_epistemic、normalization_epistemic 和 review_status；不互相推导。
6. **未知状态分离**：UNKNOWN、MISSING、CONFLICT、NOT_APPLICABLE 不可互换；优先复用既有 schema 和 Conflict object，若需新共享 primitive 必须另行审批。
7. **候选与正式分离**：研究处置不改变 canonical ontology；候选概念不进入 Product/runtime。
8. **不伪量化**：不计算无数据支撑的正交分数、权重、概率或现实预测准确率。

## 5. 建议验收用例

- 同一 rule ID 同时映射两个候选概念时，必须存在两个映射理由；不能把一条来源当成两份独立证据。
- 没有共同 rule ID 时，系统不能自动生成“已证明独立”的状态。
- projection evidence 不能自动晋升为 direct-state evidence。
- 未核对的源文条件差异（尤其 ZZ-PJ-X06）不能被自动修正或忽略。
- QI-17-CAND / QI-18-CAND 保持候选状态，不产生正式 ID。
- 未知、缺失、冲突、不适用保持可区分；缺少证据不能默认填成否定值。
- 任何本包提议都不应改变 canonical ontology、源规则、Product/runtime 或消费权限。

## 6. 本包之后的决策门

本包通过后，下一步是审阅 Option C v0.2 的非 canonical 契约提案。该提案通过不等于正式 schema 已冻结。若需要修改 QI/QR canonical 定义、分配 ID、接受映射或改变 Product 消费权限，必须另开工作单、列明具体差异和回滚方案，并经过适用 Human Gate。

本包不主张八组概念已经正交，也不主张紫微斗数具备经验预测效度。
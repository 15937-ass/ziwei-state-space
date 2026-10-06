# 项目封存检查点 — 2026-10-06

状态：ARCHIVED  
封存原因：PI 主动要求暂停项目一段时间，待未来显式恢复。  
治理版本：Repository Governance v1.0

## 1. 整个项目封存时处于哪里

项目长期路径仍然是：

中州派知识库建设  
→ 可执行、可追溯的中州派推演系统  
→ 内部忠实度验证（PL4-A）  
→ 现实盲测 / 外部预测验证（PL4-B）  
→ 统计校准与个体化（PL5+）  
→ 成熟产品

封存时：
- **治理体系已经升级到 v1.0**，以后 Chat 不再承担项目状态真相。
- **产品正式 main** 已完成到 PL3-M 的人口层 manifestation probability interface；个体后验接口仍只在未合并分支中。
- **知识正式 main** 仍停在事业宫 CA08（800 条正式进入 main）。
- **知识非正式分支** 已经大幅向前推进：完整十二宫 WP05 closure 已做完，并进一步准备了 WP06B manifestation ontology schema；这些成果**未进入 canonical main**，不能当成正式知识库状态。

这一区分是未来恢复时最重要的事实。

## 2. 正式 canonical main 已经稳定的内容

### 治理
Repository Governance v1.0 已进入 main：
- Constitution / Proposal / Roadmap / Phase Contract / Issue / PR / CI 权威分层；
- PRODUCT / KNOWLEDGE / GOVERNANCE 三轨写入边界；
- State YAML 只做恢复指针；
- 产品能力采用 readiness matrix，禁止“接口完成 = 产品成熟”；
- PI 汇报以研究阶段、下一步和紫微知识决策为中心。

### 产品
main 中可视为正式的核心：
- deterministic chart / Chart Trust 基础；
- Rule Runtime 与 EvidencePackage 主干；
- PL3-N Natal State；
- PL3-T Temporal Environment；
- PL3-S Acquired State；
- PL3-M manifestation ontology/router/context gate/人口概率接口的**架构与接口层**。

注意：
这些并不等于完整论命能力，也不等于现实预测有效。

### 知识
main 中正式知识推进点仍是：
- WP04 source closure 已完成；
- WP05 事业宫 CA08；
- 事业宫 canonical main：800 reviewed / 786 reusable / 14 case-support-only / 28 history feedback。

## 3. 必须保留、但不能冒充 canonical 的分支成果

### 产品未合并成果
PR #274  
分支：`agent/product/pl3m-personalized-posterior-v0.1`  
Head：`8efbeb9efc31fa73986fd8f4cdfd6ad033e0f901`

内容：PL3-M personalized posterior 接口实现及测试。  
判断：理论边界总体安全，但因为治理迁移中断，未来恢复时应从最新 main 重新构造干净 Product Issue/branch，而不是直接把旧 PR 合入 main。

### 知识未合并成果：WP05 十二宫
PR #272  
分支：`knowledge/wp05-twelve-palace-final-closure`  
Head：`6be1fb79875d3caf56893792eec42d3171110ebc`

该分支是一个**累积快照**，包含旧 stacked chain 上的完整十二宫 WP05 工作。该分支报告：
- 7,713 reviewed
- 6,289 reusable
- 1,424 CASE_SUPPORT_ONLY
- 192 source-explicit history feedback

这些数字是 branch/PR 结果，不是当前 main 的 canonical 统计。

### 知识未合并成果：WP06B 准备
PR #273  
分支：`knowledge/wp06b-manifestation-ontology-prep`  
Head：`d453d0b56a6d6c36b0002dc69d7d8b525f760e30`

该分支建立在 #272 之上，因此包含完整 WP05 stack，并额外完成：
- manifestation ontology schema 准备；
- 不创建 canonical manifestation nodes；
- 不创建概率；
- 打开未来 Human Gate：`HG-WP06B-MANIFESTATION-ROOT-01`。

**这一 Human Gate 是未来最早需要 PI 紫微知识判断的重要节点之一。**

## 4. 为什么这些分支现在不合并

封存前不为了“看起来完成”而把大型旧 stack 强行塞进 main。

原因：
1. 旧知识 PR 链产生于 Governance v1 之前，存在长 stacked topology；
2. main 已经发生治理结构变化；
3. 知识成果本身值得保留，但需要未来在新治理下重新审计、分段整合；
4. 强行合并会把“成果保存”和“成果正式批准”混为一谈。

因此：
**branch progress 被保存，canonical approval 被保留到未来恢复时完成。**

## 5. 未来恢复时的推荐顺序

### 第 0 步：恢复项目
用户必须明确说“恢复/继续紫微斗数项目”。

新会话只需要：
1. 读 `PROJECT_STATE.yaml`；
2. 读本封存检查点；
3. 读对应 lane state；
4. 不需要读取旧聊天。

### 第 1 步：先做一次仓库健康检查
确认：
- main 仍以 Governance v1 为基线；
- 历史分支 head 仍可访问；
- repository quality gate 正常；
- 若尚未配置 main protection/ruleset，先完成治理管理员项。

### 第 2 步：重新接回知识侧成果
不要逐条重做十二宫，也不要直接 merge #273。

先以 #272/#273 为“非 canonical 研究快照”，对比当前 main：
- 验证 source provenance；
- 验证 schema；
- 检查是否有跨 Governance v1 的状态/文件冲突；
- 按 bounded Work Unit 分段进入 canonical main。

### 第 3 步：重新接回产品侧 PL3-M
从 #274 提取有效 personalized-posterior 设计，在新的 Product Issue/branch 上重建并验证。
完成后正式关闭 PL3-M interface layer。

### 第 4 步：进入 PL4-A
依次做：
- chart reconstruction fidelity；
- W01 wealth-rule fidelity；
- Evidence trace fidelity；
- Temporal fidelity；
- textbook reasoning reconstruction；
- PL4-A closure audit。

## 6. 未来什么时候需要 PI 的紫微知识

### 近期不需要 PI 的内容
恢复后的：
- branch/rebase/CI/代码整理；
- source provenance 机械验证；
- 已明确 schema 的数据迁移；
这些应由 GPT 自动完成，不要求 PI 处理 Git 技术细节。

### 第一处重要 PI 决策
`HG-WP06B-MANIFESTATION-ROOT-01`

核心问题不是代码，而是：

> 是否应该人为预先规定一组“现实表现的普适顶层类别”，还是应该让 manifestation family 从中州派源文与案例中逐步归纳出来？

旧 WP06B 准备工作的推荐方向是：
- 不预设一个现代心理学/社会学式的总 ontology；
- 采用 source-derived / federated roots；
- `domain` 作为独立标签；
- 不把现代分类系统反向套进中州派。

恢复到这里时，应重新向 PI 用中文展示源文证据和选项，再作决定。

### 第二类 PI 参与
PL4A-05 教材案例推理重构。

需要 PI 判断：
- 某些作者省略的推理步骤是否符合中州派习惯；
- 看似冲突的判断究竟是宫位层级、三方四正、四化/煞曜条件差异，还是资料本身存在冲突；
- 哪些属于普遍规则，哪些只是具体案例语境。

## 7. 封存期间禁止做什么

项目状态为 ARCHIVED 时：
- 不自动继续 Product 或 Knowledge work；
- 不自动推进 PL4-A；
- 不自动合并历史知识 stack；
- 不自动回答/通过 Human Gate；
- 不因外部经验或案例修改 canonical knowledge；
- 不把 branch progress 当 main truth。

只有 PI 明确要求恢复，项目才重新进入 ACTIVE。

## 8. 恢复时最短指令

PI 未来只需要说：

> “恢复紫微斗数项目，从封存检查点继续。”

GPT 应按本文件和状态文件恢复，不要求 PI 重述技术背景。

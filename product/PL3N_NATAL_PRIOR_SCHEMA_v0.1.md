# PL3-N Natal Prior Contract v0.1

状态：IMPLEMENTATION CONTRACT

## 1. 目的

PL3-N 把已经通过 PL1/PL2 的确定性排盘与 canonical executable knowledge 组合成一个**不依赖用户现实反馈**的原局状态对象：

\`\`\`text
Normalized Chart
  -> canonical chart facts
  -> source-backed structures
  -> canonical natal rule evidence
  -> NatalStateProfile
\`\`\`

PL3-N 不负责：
- 大限/流年；
- acquired state；
- 用户反馈；
- manifestation probability；
- personalization；
- action planning。

## 2. 核心不变量

\`\`\`text
same chart
+ same engine/config
+ same canonical knowledge version
=> same NatalStateProfile
\`\`\`

反馈不得改变 profile。

## 3. NatalStateProfile v0.1

字段：

- schema_version
- profile_id
- engine_version
- knowledge_version
- canonical_facts
- named_structure_facts
- baiguan_profiles
- pattern_assessments
- contextual_valences
- domains
- feedback_used=false
- empirical_calibration_used=false

### canonical_facts

来自 PL2-G palace structure：
- palace presence；
- branch；
- stars；
- natal transformations；
- explicit palace relations。

### named_structure_facts

只来自已经批准为 executable truth predicate 的 source-backed primitives。

PL3-N 当前不会把 BAIGUAN_SUPPORT_PROFILE 转成 STRUCTURE_PRESENT。

### baiguan_profiles

保存 Human Gate 批准的 evidence profile：
- PARTIAL_SUPPORT / CONFLICTED / ABSENT；
- 不进行完整百官 activation。

### pattern_assessments / contextual_valences

PL3-N 只消费上游已经 source-backed 生成的产品对象；本层不得自行评分。

### domains

将 NATAL EvidencePackage 冻结成 canonical domain evidence。

如果 EvidencePackage 携带 history_state，PL3-N 必须拒绝。

## 4. profile_id

profile_id 由以下内容的 canonical serialization 计算：

- engine version；
- knowledge version；
- canonical chart facts；
- approved named structure facts；
- domain canonical evidence。

因此：
- mapping 输入顺序变化不应改变 profile_id；
- knowledge version 改变必须允许 profile_id 改变；
- feedback 不存在于 hash 输入。

## 5. v0.1 范围

v0.1 首先建立**通用容器 + 当前已有 PL2 domain adapter 接口**。

当前完整 executable coverage 最成熟的是财帛 W01，因此早期集成测试可以使用 wealth EvidencePackage，但 NatalStateProfile 本身不绑定财帛宫。

未来事业、夫妻等 domain 在其 executable registry 准备好后，以同一 NatalDomainEvidence 接口接入。

## 6. 禁止项

PL3-N 禁止：
- user profile correction；
- outcome leakage；
- empirical frequencies；
- individual posterior；
- temporal outcome；
- universal palace score；
- source 未支持的 pattern inference；
- LLM-generated rule。

## 7. PL3-N 完成标准

v0.1 至少满足：

1. 12 宫结构事实可确定生成；
2. source-backed named structures 可进入 profile；
3. Baiguan 只以 profile evidence 存在；
4. NATAL EvidencePackage 可冻结为 domain evidence；
5. history/acquired evidence 被拒绝；
6. 同输入同版本 profile_id 稳定；
7. snapshot mapping 顺序变化不改变输出；
8. 无 empirical probability 字段；
9. pytest / repository audit 通过。

# Epistemic / Review Schema v0.3 — 去污染提案

状态：**APPROVED AT GATE A0 / SUPERSEDED BY knowledge/REVIEW_SCHEMA_v0.3.md**  
用途：A0 去污染审计后的 schema 修复候选。  
本文件不修改 G1–G6 已冻结的理论结论；是否正式采用，须经 A0 人工 Gate。

## 1. 当前问题

当前规则记录把“源文是否明确说过”与“研究者如何把源文映射到气机、算子、模式或投影”压在同一个 `epistemic_type_source` 字段中。

这会造成如下混淆：

- 源文陈述本身可能是 EXPLICIT；
- 但 `target_normalized`、`QI/QR` 映射、operator 分类可能只是研究者解释；
- 当两者都只标成 `EXPLICIT` 时，会把“来源明确”误写成“归一化也由来源明确规定”。

另外，当前 `status=reviewed` 无法区分：
- 模型生成；
- 同一模型第二遍自审；
- 已回到原始页段核对；
- 独立人工核验。

## 2. 建议拆分认识论字段

### 2.1 source_epistemic

只回答：

> 原始中州派文本对这条 literal claim 的支持强度是什么？

允许值：

- `EXPLICIT`
- `INFERRED_FROM_SOURCE`
- `UNRESOLVED_SOURCE`

原则：

- `EXPLICIT` 只赋给可直接回溯到 source span 的 literal claim；
- 不因为 normalization 看起来合理，就提高 source_epistemic。

### 2.2 normalization_epistemic

只回答：

> 从 literal claim 到计算表示的转换属于什么性质？

允许值：

- `SOURCE_PRESERVING`：只做术语标准化，不增加新的理论关系；
- `INFERRED`：研究者根据原文解释得到；
- `IMPLEMENTATION`：为了计算表示而做的工程选择；
- `HYPOTHESIS`：研究新增的可检验建模假设；
- `UNRESOLVED`：目前无法稳定映射。

典型例子：

~~~text
literal_claim: 化科表示聪敏且归于正道
source_epistemic: EXPLICIT

target_normalized: QI-10 原则规范约束 increase
normalization_epistemic: INFERRED
~~~

除非原文自身明确使用了与模型维度等价的定义，否则不得把 QI/QR 映射自动标成 SOURCE_PRESERVING。

## 3. 建议拆分 review 状态

废止单一 `reviewed` 作为质量结论，改为以下四层：

- `MODEL_EXTRACTED`
- `MODEL_SELF_REVIEWED`
- `SOURCE_SPAN_VERIFIED`
- `HUMAN_VERIFIED`

并增加独立字段：

~~~yaml
review_status:
reviewer_type:
reviewer_id:
reviewed_at:
source_span_verified: true | false
normalization_verified: true | false
~~~

历史迁移建议：

- 当前所有仅由 GPT 生产/红队的 `reviewed`，默认降级为 `MODEL_SELF_REVIEWED`；
- 只有已有明确 PDF 视觉核验记录者可升为 `SOURCE_SPAN_VERIFIED`；
- 不自动生成 `HUMAN_VERIFIED`。

## 4. 规则对象建议增加 source / normalization 双层

~~~yaml
source_claim:
  literal_claim:
  source_id:
  source_location:
  source_epistemic:

normalization:
  target_type:
  target_normalized:
  operator:
  state_change:
  valence:
  normalization_epistemic:
  rationale:
~~~

这样可以明确区分：

~~~text
“王亭之说了什么”
≠
“本研究如何把它表示成状态/算子”
~~~

## 5. L1/L2 与 L3 投影边界

A0 扫描发现六十星系 canonical 中大量 `outcome_descriptor` 同时使用
`enhance/weaken/transform` 等状态方向算子。

后续建议：

- 对潜状态、关系状态：使用状态算子；
- 对事件/语义输出：优先使用 `project`；
- 若源文确实描述“某类事件风险增加”，应显式建立中间状态或将其标为
  `projection_strength`，而不是把事件本身当作可直接增减的 primitive state。

本提案暂不自动改写任何现有规则，只将其列为 source-span + layer-boundary review 候选。

## 6. 原子性规则

复合条件并不自动等于错误，但以下情况必须进入 P1 原子性复核：

- 一条 condition 内含多个彼此可独立成立的条件；
- 一条规则把多个不同星曜组合压缩成同一个 effect；
- 一条规则同时包含前提、例外、结果与解释；
- 多个 source sentences 被压成一条无法单独激活/失活的规则。

最终目标：

> 每个规则应尽量对应一个可独立判断的逻辑单元，同时保留组合 gate。

## 7. Gate A0 需要 PI 决定的事项

A0 不要求逐条审核全部规则，只需决定：

1. 是否批准 source_epistemic / normalization_epistemic 拆分；
2. 是否批准 review_status 四级化；
3. 是否批准历史 `reviewed` 默认降级为 `MODEL_SELF_REVIEWED`；
4. 是否批准 L1/L2 状态算子与 L3 投影算子重新分层；
5. 是否批准用 deterministic linter 阻止 schema 越界值进入 main。

批准后，再进入自动迁移 + 高风险 source-span 回查。

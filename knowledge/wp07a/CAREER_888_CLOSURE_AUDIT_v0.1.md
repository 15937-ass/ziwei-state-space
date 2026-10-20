# 事业宫 888 条最终闭合审计

Issue #403。事业宫 canonical source review 共 888 条；在百条严格复核制度建立前已有 52 个专项 structured IDs，随后完成 8 个百条批次（800 条）与最终尾批 36 条。合并后目标是 **888 / 888 unique structured IDs**。

## 最终尾批 36 条

范围为 CA09-853 至 CA09-888。CA09-852 已在早期原子化试点中完成，因此不重复计数。

尾批结果：
- 完整条件映射：7
- 方法／语境：2
- 阻塞：27
- 生产新增：0
- unique structured IDs：852 → 888

完整映射为：
CA09-853、CA09-857、CA09-870、CA09-873、CA09-878、CA09-880、CA09-882。

其中 CA09-853 虽可把盘面前件精确保存为“破军化禄”，canonical history_feedback 已明确标记 PATH_DEPENDENT_GATE，所以它仍不是静态自动执行结论。

## 九次严格复核累计

8 个百条批次 + final36，共严格复核 836 条：

- COMPLETE_CONDITION_MAPPING：216
- METHODOLOGY_OR_CONTEXT_ONLY：107
- BLOCKED_OUTCOME_MAPPING：513

另外 52 条是在百条制度建立前通过专项映射进入 structured baseline。closure test 必须验证这 52 条与后续 836 条的 union **恰好等于 canonical 888 IDs**，既不能缺失，也不能多出非 canonical ID。

## 513 条 blocker 的全量分布

- GROUP：171
- COMPOSITE：92
- RELATION：74
- RELATION_AND_GROUP：59
- CONTEXT_STATE：43
- TEMPORAL：17
- ABSENCE_AND_GROUP：16
- DIGNITY：13
- ACTION：6
- ABSENCE：6
- VALENCE：5
- DIGNITY_AND_GROUP：5
- EXAMPLE：3
- UNMODELED_STATE：2
- DIGNITY_AND_RELATION：1

这些数字不是“失败数”，而是下一阶段 ontology backlog 的直接统计依据。

## 最后 36 条的具体知识内容

### 1. 破军化禄与路径依赖

原文不仅说破军化禄多兼职、兼差、兼业，还说常由原来不以为重点的行业或职务起家。这里的“破军化禄”是盘面前件，而“非重点行业后来成为事业基础”是发展路径。

因此两者被拆成：
- Natal 条件：破军化禄；
- Path-dependent target：非核心路径后续成为事业基础。

不能把后者伪装成出生时已经确定的静态事实。

### 2. 破军的创新轴

原文把七杀与破军作明确比较：七杀偏管理，破军偏创新。因此新产品、新技术、冒险性行业属于破军创新轴的现代场景翻译。

比较语句 CA09-856 保留在 methodology/context；由该比较引出的 CA09-857 才保留为破军 source scene candidate。它仍只是传统体系中的可能场景，不是职业概率。

### 3. 群组与命名结构继续严格阻塞

火贪、铃贪、辅弼、魁钺、昌曲、桃花诸曜、羊陀、火铃、空劫等，在最后一段仍大量出现。

当前不把“火铃”“羊陀”“空劫”等传统合称机械解释成：
- 两颗都必须出现；
- 任一颗出现；
- 固定数量阈值。

来源未给出的量词不由系统自行补齐。

### 4. 子午破军：盘面倾向与现实行为分开

子午破军“无论行业均喜政治手腕”可以作为母结构下的功能倾向保存。

但“从政”“从工从商”“行业虽多而不专”“命宫有煞而无禄”等条件分别涉及现实职业路径、行为状态、跨宫与缺席语义，因此继续阻塞。

“年限不佳时引起大风波”明确进入 YEAR temporal layer，不能静态化。

### 5. 女命条件暴露新的事实缺口

“女命破军于子午守事业宫”有明确性别限定。现有获批准 condition atoms 中没有 sex/gender fact。

本批没有删除“女命”两个字来提高映射率，而是以 UNMODELED_STATE 阻塞。是否建设性别事实层，应该是后续 ontology 工作，而不是在 closure 阶段临时加字段。

### 6. 寅申破军

寅申破军的三条母结构性质可直接保存：
- 倾向合作创业；
- 事业场面可以较大；
- 忌过度出锋头。

但武曲化禄/化忌、贪狼化权、文曲化忌的“来会/不会”等条件同时牵涉空间关系和缺席语义，所以没有借宫位模板擅自指定载体。

### 7. 辰戌破军

辰戌破军落罗网，对应至少一次重大事业挫折 candidate。辰戌本身可作为明确宫支事实保存。

但“重大挫折之后改行改业”存在先后路径：
先有挫折 → 后有改行。

所以改行不是“辰戌破军”的静态直接结论。

同样，“借别人财力势力”“无吉无煞”“有吉化吉曜”“煞重”“过分计较钱财”等分别涉及现实输入、群组、缺席与行为状态，继续严格保留 blocker。

## Closure 的含义

本次 closure 只确认三件事：

1. canonical Career source review 已是 888 / 888；
2. 888 个 canonical rule IDs 全部进入可追溯的 structured disposition；
3. 每条无法完整表达的语义都被显式阻塞，而不是丢失或猜测。

它**不代表**：
- 888 条都已经可执行；
- 中州派传统规则已经得到现实经验验证；
- blocker 可以由 LLM 自行补全；
- Product 可以自动吸收所有 Knowledge 条目。

## 下一阶段

从 blocker census 看，后续不应该再逐条打补丁。优先级应由共性缺口驱动：

**星曜群组/量词 → 会照/借会/同拱空间关系 → 复合格局/夹宫 → 缺席语义 → 庙陷 → 现实 context-state → temporal/path-dependent → 其他未建模事实。**

任何新 ontology semantics 都应另开工作单元；若改变 canonical meaning 或默认解释，需要 Human Gate。

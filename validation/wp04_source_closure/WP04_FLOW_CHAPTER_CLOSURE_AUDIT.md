# WP04 流曜章节 Source-Coverage Closure Audit

状态：**CHAPTER SOURCE CLOSURE COMPLETE**

## 审计范围

- 源：SRC-ZZ-002《中州派紫微斗数深造讲义（上册）》流曜总论。
- checkpoint：FC01–FC02。
- 起点：流曜总论。
- 终点：岁前十二神“病符”。
- 下一明确章节标题：星曜庙陷。

## 累计结果

- checkpoints：2
- source-reviewed items：108
- SOURCE_SPAN_VERIFIED：108 / 108
- ADD_CANDIDATE：82
- CASE_SUPPORT_ONLY：26
- 新 primitive qi：0
- 新 history-memory type：0
- 新 Human Gate：0
- 人工连续权重 / 默认衰减 / 固定持续年数：0

## 连续性审计

FC01 从“流曜总论”开始，覆盖辅佐煞化流曜总则、博士十二神、将前十二神并推进岁前十二神；FC02 从白虎余段接续至病符，随后源文进入“星曜庙陷”。未把庙陷规则混入流曜统计。

## 模型反馈

1. 流曜更适合作为 temporal-layer operator，而不是重建一套新的星曜本体。
2. “流曜冲起原局”应编码为 natal–temporal interaction，属于时间层激活/加强机制。
3. 博士、将前、岁前三组在小限中主要充当短时状态、门控、事件候选与场景投影。
4. 明确的疾病、刑罚、孝服、家庭与性别化旧例继续保留为 CASE_SUPPORT_ONLY，不直接进入底层气核。
5. 同名流曜在不同体系中的强度与适用时间不同，例如岁前小耗/大耗仅用于流月流日，不能与博士十二神同名曜简单合并。

## 下一工作单元

WP04 流曜 source closure 到此关闭。下一步进入 **星曜庙陷 source-coverage closure**，从庙、旺、平、闲、陷的定义及环境适配机制开始。

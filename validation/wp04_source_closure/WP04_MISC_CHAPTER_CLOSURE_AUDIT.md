# WP04 杂曜章节 Source-Coverage Closure Audit

状态：**CHAPTER SOURCE CLOSURE COMPLETE**

## 审计范围

- 源：SRC-ZZ-002《中州派紫微斗数深造讲义（上册）》杂曜总论。
- checkpoint：MC01–MC03。
- 起点：杂曜总论 / 天伤天使。
- 终点：长生十二神“养”。
- 下一明确章节标题：流曜总论。

## 累计结果

- checkpoints：3
- source-reviewed items：252
- SOURCE_SPAN_VERIFIED：252 / 252
- ADD_CANDIDATE：193
- CASE_SUPPORT_ONLY：59
- 新 primitive qi：0
- 新 history-memory type：0
- 新 Human Gate：0
- 人工连续权重 / 默认衰减 / 固定持续年数：0

## 连续性审计

MC01→MC02→MC03 均以前一 checkpoint 的 next_anchor 接续。MC03 从“截空主障碍 / 不喜与禄存化禄同度”继续，到“养”结束，随后源文进入“流曜总论”。未把流曜规则混入杂曜章节统计。

## 模型反馈

1. 杂曜以 modifier / gate / projection / temporal trigger 为主，不宜与十四正曜或四化同层处理。
2. 成对杂曜与独立杂曜需分开编码：前者常依赖 pair-gate，后者可以单星直接修饰原系统。
3. 具体疾病、婚姻、职业、家世、异性等传统断语继续保留为 CASE_SUPPORT_ONLY，不直接写入底层气核。
4. 截空、旬空、天空、破碎等“空/耗/阻”类杂曜并非同义，需要保留 obstruction、unrealization、depletion、fantasy 等不同机制。
5. 长生十二神更适合作为低层状态修饰与宫位 gate，而不是新增独立 primitive qi。

## 下一工作单元

WP04 杂曜章节 source closure 到此关闭。下一步为 **流曜 source-coverage closure**，从“流曜总论”开始，继续遵守 source-span review、provenance 和 100 条硬上限规则。

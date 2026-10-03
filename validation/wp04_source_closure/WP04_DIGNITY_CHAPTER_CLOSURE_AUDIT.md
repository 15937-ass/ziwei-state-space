# WP04 星曜庙陷 Source-Coverage Closure Audit

状态：**CHAPTER SOURCE CLOSURE COMPLETE**

## 审计范围

- 源：SRC-ZZ-002《中州派紫微斗数深造讲义（上册）》
- 章节：星曜庙陷
- checkpoint：DG01
- 起点：庙、旺、平、闲、陷定义
- 终点：吉凶杂曜庙陷表
- 文本边界：上册结束

## 累计结果

- source-reviewed items：67
- SOURCE_SPAN_VERIFIED：67 / 67
- ADD_CANDIDATE：67
- CASE_SUPPORT_ONLY：0
- 其中 source-preserved table rows：60
- 新 primitive qi：0
- 新 history-memory type：0
- 新 Human Gate：0
- 人工连续权重 / 默认衰减 / 固定持续年数：0

## 核心结论

1. 庙旺平闲陷应先建模为**离散环境适配/表达门控层**，不能直接视为固定线性增益。
2. 同一环境等级对吉曜与凶曜的作用方向并不相同：源文明确给出“入庙使吉曜易发挥、凶煞减暴；落陷则相反”的非统一标量结构。
3. 源文只给出类别次序和表格映射，没有提供类别之间的数值距离，因此当前不得赋予 +2/+1/0/-1/-2 等连续或等距参数。
4. 表格中的空白单元格按原样保留，不作插值；个别印刷为“地”的字样亦按源文保留，等待后续版本校勘，不静默修正。
5. 生时页以分支—星曜组合图出现，当前仅保存原始 branch/star association，不额外推断其计算语义。

## WP04 剩余 source-span gap

星曜庙陷章节已闭合，但 WP04 **整体尚未关闭**：现有 `auxiliary_eight_v0.1.csv` 与 `six_malefics_v0.1.csv` 虽已 legacy reviewed，却仍是 `MODEL_SELF_REVIEWED`，其 `source_span_verified=false`、`normalization_verified=false`。因此下一步应回补：

1. 辅佐八曜 source-span closure；
2. 六煞 source-span closure。

两者完成后，才可宣告 WP04 operator source coverage 全闭合并进入 WP05。

# WP04 辅佐八曜 Source-Coverage Closure Audit

状态：**CHAPTER SOURCE CLOSURE COMPLETE**

## 审计范围

- 源：SRC-ZZ-002《中州派紫微斗数深造讲义（上册）》
- 章节：辅佐八曜
- printed pages：165–171
- checkpoints：AUX01–AUX02
- legacy catalog：`knowledge/operators/auxiliary_eight_v0.1.csv`

## 累计结果

- source-reviewed legacy rules：103
- SOURCE_SPAN_VERIFIED：103 / 103
- ADD_CANDIDATE：73
- CASE_SUPPORT_ONLY：30
- 新 primitive qi：0
- 新 history-memory type：0
- 新 Human Gate：0
- 人工连续权重 / 默认衰减 / 固定持续年数：0

## 关键模型反馈

1. 辅曜与佐曜应区分 support source：辅曜偏外部机会/制度/他力，佐曜偏本人努力才能实现的自力。
2. 魁钺、辅弼存在明确 pair-gate 与 single-star branch，不能将单星机械视作成对结构的半强度版本。
3. 原局魁钺被运限/流年魁钺冲起，是明确 natal × temporal activation 结构。
4. 禄马清楚区分资源与移动：有马无禄只主移动/奔波，有禄无马可得财而无迁动。
5. 传统家庭、婚恋、健康、事故与旧式性格标签均保留为 CASE_SUPPORT_ONLY，不进入 primitive qi。

## Provenance policy

为保持 legacy catalog 原始抽取不被静默改写，AUX01/AUX02 review CSV 作为 v0.3 权威 source-review overlay；不把旧字段自动改写为 HUMAN_VERIFIED 或 SOURCE_PRESERVING。

## 下一工作

进入六煞 source-span closure，从 printed p171 的“煞曜”开始。

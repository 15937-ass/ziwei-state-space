# WP04 化禄专章 source review v0.1

Status: **10/10 SOURCE SPANS REVIEWED — CANONICAL RECONCILIATION NEXT**

## 范围

本轮按《中州派紫微斗数深造讲义（上）》化曜专章的“化禄”十个子节逐段复核：

廉贞、天机、天同、太阴、贪狼、武曲、太阳、巨门、天梁、破军。

源文已从廉贞化禄起始段连续复核至破军化禄结束、化权章节开始为止。

## 结果

- source units reviewed: **10/10**
- source-supported atomic closure rows: **45**
- source mismatch: **0**
- architecture Gate: **NO**
- raw legacy transformation catalog overwritten: **NO**

专章证据再次确认：四化不是固定符号增益。即使只看化禄，也同时出现：

- 状态增强与状态转换；
- 获得资源与保存资源分离；
- natal / 大运流年的语义差异；
- 煞曜、桃花、科文、宫位和星系造成的 gate / reversal；
- 名誉→资源、关系→资源等 L3 projection；
- “化禄但更安逸/更烦扰/更不稳定”等非单调结果。

## 重要修正

现有 56 条 transformation rules 不能承担“化曜专章已经覆盖”的证明。本轮新建：
`knowledge/operators/transformation_source_closure_v0.1.csv`

它作为**source-coverage sidecar**保存专章逐段抽取结果，暂不直接覆盖 legacy canonical。

武曲化禄标题在 PDF 文本提取中呈现为“武曲(巳干化禄)”字形；本轮只记录为 OCR/文本异常，不据此擅自修改传统干支映射。

## 下一步

1. 将 45 条化禄 closure rows 与 legacy 56 条逐条语义对齐；
2. 标记 REUSE / PROVENANCE_UPGRADE / NEW_CANONICAL / NORMALIZATION_REPAIR；
3. 无冲突后把化禄 source units 从 reconciliation 状态推进到 CLOSED；
4. 进入化权十个 source units。

当前没有证据要求新增 primitive qi 或修改核心 operator 架构。

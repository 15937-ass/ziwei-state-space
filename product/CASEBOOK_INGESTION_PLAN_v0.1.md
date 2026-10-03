# Liaoran Casebook Ingestion Plan v0.1

状态：ACTIVE

## Scope

三本《紫微斗数论命技巧及实例解析》均已在 Project 文件面确认：

- 上册：250 PDF pages，案例 1–15；
- 中册：298 PDF pages，案例 16–56；
- 下册：270 PDF pages，案例 57–100。

合计 **100 个编号案例**。

本工作包属于产品侧 Case Reasoning Corpus，不改变中州派 canonical source 的权威层级。

## Stage 0 — Source binding

三册均绑定实际 Project 文件名。内部训练数据只保存稳定 source_id + 文件名 + page provenance，不依赖临时聊天引用。

## Stage 1 — Case index

`CASEBOOK_CASE_INDEX_v0.1.csv` 记录 100 个案例的：

- case_id
- source_id
- 卷别
- 目录印刷起始页
- PDF 起始页
- PDF 结束页

当前三册均观察到“印刷页码 + 2 = PDF page”的稳定偏移；索引由目录起始页计算，后续每个案例实际抽取时仍要做页面级复核。

## Stage 2 — Pilot 20

`CASEBOOK_PILOT20_v0.1.csv` 采用分层抽样，不直接取前 20 个编号。

覆盖：

- 事业 / 转职 / 创业
- 财运
- 婚恋 / 桃花
- 考运
- 健康 / 子女
- 流年比较
- 外出 / 迁移
- 综合人生状态

并覆盖上、中、下三册，目的是尽早暴露 parser、schema、temporal resolver 和 rule-linking 的结构缺口。

## Stage 3 — Case extraction

每个 pilot case 输出一份 `CaseEvidenceRecord`，分离：

1. birth input；
2. question facts；
3. author claims；
4. author reasoning steps；
5. chart references；
6. temporal layers；
7. prediction claims；
8. immediate feedback；
9. later outcomes；
10. unresolved / ambiguous spans。

禁止把作者结论直接写入 reality ground truth。

## Stage 4 — Deterministic chart rebuild

当出生资料足够时，通过 Normalized Chart Snapshot adapter 重建命盘。

若时间、历法、性别或地点不足：

- 不猜；
- 标记 `CHART_INPUT_INCOMPLETE`；
- 作者书中命盘只保留为 `SOURCE_CHART_REFERENCE`。

## Stage 5 — Rule linking

作者每一条关键推理只允许链接到：

- 已存在 canonical rule_id；
- 或 CASE_DERIVED candidate。

CASE_DERIVED 不得自动升级 canonical。

## Stage 6 — Product metrics

Pilot 20 首轮只测：

- extraction completeness
- chart rebuild coverage
- canonical rule trace coverage
- temporal-layer coverage
- unresolved inference gap rate
- author-conclusion reproducibility

**不测现实预测准确率。**

现实 accuracy 只能使用外部盲测 / 后验事实数据。

# PL2-D EvidencePackage Bridge v0.1

状态：IMPLEMENTED — NO-LLM STRUCTURED INFERENCE

## 1. 本 checkpoint 解决什么

PL2-C 已经可以得到 `ActiveRuleGraph`，但图本身仍属于 runtime/debug 结构。

PL2-D 增加确定性 bridge：

```text
Normalized Chart Snapshot
 -> wealth facts
 -> RuleIR
 -> ActiveRuleGraph
 -> EvidencePackage
 -> later UI / LLM verbalizer
```

LLM 仍然不参与：

- 排盘；
- rule selection；
- condition matching；
- confidence band；
- conflict detection；
- contrastive gate analysis。

## 2. EvidencePackage 新增

在兼容原 contract 的前提下增加：

- `contrastive`：未激活 executable rule 的缺失/阻断 gate；
- `coverage`：当前知识执行覆盖；
- `confidence_rationale`：置信档位的确定性原因。

现有 `active_rules`、`projections`、`conflicts` 继续保留。

## 3. Active evidence

每条 active rule 输出：

- rule_id；
- normalized claim / projection target；
- source_id；
- source_location；
- source epistemic marker；
- review_status；
- matched conditions；
- projection domain/mode；
- source pointer。

Bridge 不创造新的传统断语。

## 4. Contrastive

对每条“已经 executable、但本次没有激活”的规则，输出：

- `missing_all_of`；
- `unsatisfied_any_of`；
- `blocked_by`。

例如“禄存且无天马”在同时见天马时，不会被描述成“错误”或“反向结论”，而只记录：

```text
candidate W01-026
required gate satisfied
blocked_by = 天马
```

这使后续 UI 能回答“为什么这条没有触发”，而不需要 LLM 猜理由。

## 5. Confidence policy

PL2-D 的 symbolic confidence 非预测概率。

规则：

1. 有 explicit conflict -> `CONFLICTED`；
2. 无 active rule -> `INSUFFICIENT_EVIDENCE`；
3. 有 active rule，但还有 NORMALIZATION_PENDING / PATH_DEPENDENT_HOLD -> `LOW_CONFIDENCE`；
4. symbolic coverage 全闭合且无冲突 -> 最多 `MEDIUM_CONFIDENCE`；
5. `HIGH_CONFIDENCE` 在本层不可达，保留给后续外部 benchmark/calibration 后的产品层。

因此当前 13/100 pilot 即使命中多条，也不会假装成高置信预测。

## 6. 无 LLM 样例

运行：

```bash
PYTHONPATH=. python tools/pl2d_wealth_sample.py
```

会从同一个 W01 canonical checkpoint + PL2-C registry 生成完整 JSON EvidencePackage。

示例输入包含：

- 武曲化禄；
- 紫微化科；
- 擎羊；
- 财帛宫 P05。

输出完全由 Python deterministic runtime 生成，不调用模型。

## 7. 验收

测试覆盖：

- source trace preservation；
- bounded coverage -> LOW_CONFIDENCE；
- zero active -> INSUFFICIENT_EVIDENCE；
- negative gate contrastive；
- EvidencePackage deterministic equality；
- 原 EvidencePackage contract 向后兼容。

## 8. 下一步

下一工作单元建议为 **PL2-E / PL3-ENTRY**：

1. 给财帛 pilot 建立语义聚合层，避免直接把多个 rule target 当成自然语言结论；
2. 明确 support / constraint / risk / earning-mode 等 domain 的组合关系，但不引入数值权重；
3. 扩第二批 W01 normalization；
4. 建立第一个“本命财帛结构报告”无 LLM 输出；
5. 然后接入大限 + 流年 temporal state，进入真正的 PL3 Inference MVP。

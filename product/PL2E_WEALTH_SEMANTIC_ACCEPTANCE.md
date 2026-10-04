# PL2-E 财帛语义聚合层 v0.1

状态：IMPLEMENTED — DETERMINISTIC NATAL REPORT

## 1. 目标

PL2-D 已经能输出 EvidencePackage，但仍是 rule-level evidence。

PL2-E 将已激活证据按照财帛宫 closure audit 已确认的**多状态财务子系统**组织成面向产品的结构报告：

```text
EvidencePackage
 -> source-supported semantic sections
 -> rule findings
 -> shared-trigger groups
 -> coverage / limitations
 -> deterministic Chinese report
```

仍然不使用 LLM。

## 2. 语义基础

本层的栏目直接以 `WEALTH_PALACE_CLOSURE_AUDIT.md` 的 semantic closure 为边界：

- 获取能力与机会；
- 生财方式；
- 投入与心力成本；
- 资金流动；
- 管理与调度；
- 积累与留存；
- 波动性；
- 损失与竞争风险；
- 财务权力与控制；
- 名誉与地位介导收入；
- 流动与异地收入。

另设“结构约束与解释”用于承载 `STRUCTURAL_CONSTRAINT / interpretation`，避免把限制条件硬塞进财富高低维度。

## 3. 不做单一财富分数

closure audit 已明确：

> P05 remains a multi-state financial subsystem rather than one latent fortune variable.

因此 PL2-E 明确禁止：

- wealth score；
- 净吉凶；
- 正负相加；
- 数值权重；
- 概率；
- “综合来看你很有钱/没钱”式自动结论。

产品输出保留各维度并列结构。

## 4. Presentation registry

`product/PL2E_WEALTH_SEMANTIC_REGISTRY_v0.1.json`

为当前 13 条 executable rule 提供：

- section；
- 中文 display claim。

这些 display claim 是一对一的产品展示 normalization，必须绑定已有 RuleIR，不产生新 rule，不参与 rule matching。

未知 active rule 默认 `FAIL_CLOSED`，防止新增 executable rule 后被旧 UI 静默错误归类。

## 5. 共同触发，不等于冲突

如果多条规则由完全相同的 runtime facts 触发，系统输出 `shared_trigger_groups`。

例如紫微守财帛宫可同时激活：

- W01-090：收入/资源较充足；
- W01-091：充足不等于积累；
- W01-092：紫微偏名誉权力，不直接等同财星。

PL2-E 把它们标记为“共同触发”，不会自动判成冲突，也不会擅自做主次权重。

## 6. 第一个无 LLM 本命财帛报告

运行：

```bash
PYTHONPATH=. python tools/pl2e_wealth_report.py
```

输出：

1. machine-readable JSON；
2. deterministic Chinese report。

每条中文 finding 都保留：

- rule_id；
- source pointer。

因此 UI 展示仍可回溯到 canonical evidence。

## 7. 当前限制

W01 当前仍是：

- 13 EXECUTABLE；
- 87 NORMALIZATION_PENDING。

所以报告继承 PL2-D 的 LOW_CONFIDENCE，而不是因为“文字看起来像完整报告”就提高置信等级。

## 8. 下一步

建议进入 **PL2-F Wealth Normalization Batch 2**：

1. 扩充第二批低歧义 W01 条件；
2. 优先覆盖当前空缺维度和跨维度约束；
3. 保持每批 bounded + source-drift guard；
4. 每批自动更新 semantic registry coverage；
5. 达到足够本命覆盖后，再进入 PL3 的大限/流年联合 temporal inference。

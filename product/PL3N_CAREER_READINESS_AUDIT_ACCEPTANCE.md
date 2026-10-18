# PL3-N Career Readiness Audit v0.1

状态：**MIGRATION-AWARE AUDIT — READINESS DERIVED FROM CANONICAL ARTIFACTS**

## 1. 目的

在把事业宫接入 PL3-N domain provider 之前，先检查当前 WP05 Career corpus 是否具备产品化的结构条件。

本批只做 product-side readiness audit，不解释源文、不改知识库、不自动编译规则。

## 2. 当前知识状态

依据当前 top-level PROJECT_STATE：

- Career corpus 已到 CA08；
- 800 条已审；
- 786 reusable；
- 14 case-support-only；
- 28 history feedback；
- CA09 / final closure 尚未完成。

因此事业宫目前本来就不应直接进入 executable provider。

## 3. 新发现：CA04–CA08 存在列顺序漂移

产品审计检测到：

- CA01–CA03：300 行符合 header 语义；
- CA04–CA08：500 行出现 time_layer / condition 值位置互换；
- header 仍声明为 time_layer, condition；
- 行数据却实际为 condition, time_layer。

产品层不得静默交换这两个字段，因为这会把产品代码变成 canonical knowledge 的隐藏修复器。

正式 blocker：

\`\`\`text
TIME_LAYER_CONDITION_COLUMN_ORDER_DRIFT
\`\`\`

必须由知识侧以 auditable migration / source-preserving repair 处理。

## 4. 当前裁决

\`\`\`text
ready_for_executable_normalization = false
\`\`\`

原因同时有两个：

1. CAREER_CORPUS_CLOSURE_PENDING；
2. TIME_LAYER_CONDITION_COLUMN_ORDER_DRIFT。

所以当前不创建 CareerNatalDomainProvider，不把任何 CA row 直接升级 executable。

## 5. 对产品路线的影响

PL3-N wealth provider 与 Natal fixture benchmark 不受影响。

事业宫路径变成：

\`\`\`text
WP05 CA09 final closure
+ knowledge-side schema repair
    ↓
product re-audit
    ↓
career executable normalization
    ↓
CareerNatalDomainProvider
    ↓
generic NatalDomainProviderRegistry
\`\`\`

## 6. 为什么这是正确的 fail-closed

如果产品侧直接兼容“有时 time_layer 在第 5 列、有时在第 6 列”，短期能继续跑，但会破坏：

- source-to-runtime parity；
- schema determinism；
- future migration audit；
- blind benchmark reproducibility。

因此 v0.1 明确选择阻断而不是猜测。

## 7. 下一步

知识侧需要：

- 完成 CA09 final closure；
- 对 CA04–CA08 的列顺序问题做 canonical repair/migration；
- 保持 rule IDs 与 source provenance 不变。

产品侧在等待期间可以继续不依赖 Career provider 的基础设施工作，但事业宫 executable normalization 必须等待上述两个 blocker 消失。


## 8. Migration-aware regression contract

The initial audit above recorded the pre-migration state: CA04–CA08 had a 500-row `time_layer` / `condition` column-position drift, and CA09 closure was pending. That finding is historical evidence and must not be rewritten.

After the Knowledge lane lands `validation/wp05/CAREER_CA04_CA08_SCHEMA_REPAIR.md` and the CA09 closure artifacts on canonical main, the Product audit must:
- observe zero schema-drift rows in CA04–CA08;
- preserve the same rule IDs, source locations, review status, CASE_SUPPORT_ONLY flags, and history-feedback markers;
- continue to block career executable normalization until the canonical CA09 closure is present and the audited totals reconcile;
- never repair or normalize the Knowledge CSVs inside Product code.

The migration marker is a status signal, not a substitute for parsing and validating the actual rows. The Product audit continues to calculate schema drift from the data itself.


## 9. Canonical CA09 re-audit (2026-10-18)

After the Knowledge lane merged the source-preserving CA04–CA08 schema repair and CA09 closure, the Product audit was rerun against all nine canonical batches:

- 888 reviewed rows and 888 source-verified rows;
- 869 reusable projection rows and 19 CASE_SUPPORT_ONLY rows;
- 37 history-feedback markers;
- zero schema-drift rows;
- no remaining corpus-closure or schema blockers.

Decision: **ELIGIBLE_FOR_EXECUTABLE_NORMALIZATION_REVIEW**.

This is not the same as provider-ready or executable. Product still must normalize only a small source-faithful subset into the existing condition-atom contract, validate its rule registry, and keep every unsupported condition blocked. The 19 CASE_SUPPORT_ONLY rows remain excluded.

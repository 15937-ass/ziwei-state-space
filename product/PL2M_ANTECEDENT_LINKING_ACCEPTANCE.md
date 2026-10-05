# PL2-M Antecedent Linking v0.1

状态：IMPLEMENTED — EXPLICIT RULE DEPENDENCY / REFERENCE LAYER

## 1. 目标

PL2-K 识别出 10 条 `ANTECEDENT_ENGINEERING` 记录。它们不是“再猜一次条件”，而是显式引用前文结构、比较既有规则，或在既有结构上继续做场景投影。

PL2-M 的目标是把这种关系从中文短语中拿出来，变成可审计的 product metadata。

## 2. 两类不能混淆的关系

### INHERIT_ACTIVE

当前规则只有在其 antecedent rule 已经在同一张盘、同一 runtime evaluation 中激活时才能激活。

本批可立即执行：

- W01-007 <- W01-006
- W01-008 <- W01-006
- W01-009 <- W01-006
- W01-015 <- W01-014
- W01-062 <- W01-061

### COMPARE_REFERENCES

文本在比较两个已经定义的规则/结构，但不表示两者必须在同一张盘同时出现。

因此：

- W01-027 比较 W01-024 与 W01-026
- W01-030 比较 W01-028 与 W01-029

**这两条不被提升为 chart trigger。**

否则“武曲与太阴比较”会被错误实现成“武曲和太阴必须同时出现”。

## 3. 仍被上游挡住的 antecedent rows

- W01-034 <- W01-033：W01-033 的火铃格等结构尚未冻结
- W01-044 <- W01-043：W01-043 的 dignity/disjunction 尚未完整 normalization
- W01-094 <- W01-093：W01-093 的见煞未冻结，同时“从事持利器行业”还需要 typed scene condition

这些 link 可以记录，但不能因为 antecedent engine 已完成就提前执行。

## 4. RuleIR 扩展

`RuleIR` 新增：

```text
antecedent_rule_ids: tuple[str, ...]
```

它不是 chart fact，不进入 condition atom ontology。

Runtime 规则：

1. 普通 chart facts / scope 先匹配；
2. antecedent rule 必须已经 active；
3. 所有 declared antecedents 都满足后，dependent rule 才 active；
4. missing reference -> fail closed；
5. self reference -> fail closed；
6. dependency cycle -> fail closed。

## 5. EvidencePackage 可追溯性

Active node 新增：

```text
matched_antecedents
```

projection payload 同步输出该字段。

未激活的 dependent rule 在 contrastive evidence 中新增：

```text
missing_antecedents
```

因此解释层能明确区分缺 chart fact 与缺上游 rule activation。

## 6. 财帛覆盖

新增 5 条 inherited executable rules 后：

```text
EXECUTABLE            54
NORMALIZATION_PENDING 46
PATH_DEPENDENT_HOLD    0
EXCLUDED               0
```

confidence policy 不变，仍为 `LOW_CONFIDENCE`。

## 7. Human Gate

本工作单元不定义新的传统结构、不新增 palace valence、不改变 temporal theory，因此无需 Human Gate。

PL2-K 已登记的未来 gate 保持未批准：

- HG_PL2N_PALACE_VALENCE_MODEL
- HG_PL2L_BAIGUAN_STRUCTURE

## 8. 下一步

推荐：

**PRODUCT_PL2L_SOURCE_BACKED_STRUCTURE_PRIMITIVES**

优先只做已有 source-verified operator/dignity 资产支持的 bounded structure family：

- 禄马交驰
- dignity lookup
- 夹宫/flanking
- 羊陀夹

若实施过程中需要越过已有 source-backed family、定义新的传统结构语义，则立即停下并提交 Human Gate 给用户审核。

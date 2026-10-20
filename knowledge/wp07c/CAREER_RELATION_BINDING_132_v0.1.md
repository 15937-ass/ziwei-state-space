# Career Relation Binding 132 v0.1

Status: **132/132 BINDING DISPOSITIONED — NO EXECUTION UNLOCK**  
Issue: #436

## 1. 覆盖

在 Relation Semantics v0.1 的 132 条 residual 上，本轮建立 **142 个 relation claims**，132/132 source rules 均获得 binding disposition。

| Row disposition | 数量 |
|---|---:|
| RB1 single target bound | 99 |
| RB2 multi-target expression bound | 16 |
| RB3 compound clause graph bound | 14 |
| RB4 relation-surface bundle bound | 2 |
| RB5 target bound / source relation recheck | 1 |

Binding resolution：114 个 claim 已绑定现有 semantic node；25 个 claim 含 `SOURCE_LITERAL_EXPRESSION_NODE`；2 个为 relation-surface bundle；1 个 target 已绑定但 relation surface“照射”仍需 source recheck。

## 2. 这一轮真正解决了什么

以前一个 blocker 可能同时写成“火铃 + 同度 + activation 未决”。现在可以明确拆开：

```text
火铃             -> GROUP_SYMBOL_NODE
同度             -> delta={0}
relation binding -> 已解决：同度作用于火铃这个 source symbol
member activation -> 仍未解决
```

所以 `relation_binding=resolved` 不会产生 `火星 AND 铃星`。

## 3. Binding target 分布

当前 claim target 中，GROUP_SYMBOL 69、OPEN_CATEGORY 59、SOURCE_LITERAL 25、NAMED_COMPOSITE 4、EXPLICIT_MEMBER_SET 4；另有少量 scoped group、structured pattern、severity modifier、generic shorthand。

这些计数允许同一 claim 包含多个 node。

特别值得注意：**59 个 OPEN_CATEGORY target 已经能完成 relation binding，但仍不能展开成员。** 这说明 Relation workstream 与 Category Lexicon workstream 已经真正解耦，下一阶段无需等待所有 category 成员先定义完才继续建句法结构。

## 4. Compound clause 的几个关键结果

- `武曲天府三方见煞`：保存为三方 scope 限制 visibility，effective delta={0,4,8}。
- `太阴与天机同度或相对且见吉化吉曜`：天机关系为 delta={0,6} alternative，吉化吉曜另建 visibility claim。
- `前格见辅弼或不见辅弼`：保存为两个 polarity 相反的 alternative claim，并使用两个不同的 source relation occurrence。
- `七杀得辅弼魁钺三台八座朝拱同会`：保存 `朝拱同会` relation-surface bundle，统一绑定辅弼、魁钺、三台八座；不机械宣称三组 target 各自分别满足同一个精确 geometry。

## 5. Surface audit 修复

为支持 binding，本轮对 derived relation map 做了 v0.2 审计。完整 standalone relation surface 为 **150 个**，另有 **1 个**位于 `百官朝拱` structured pattern 内部的 `朝拱` 被明确排除为 standalone relation。

相较 v0.1，共 13 条记录的 atom 序列发生变化：5 条补齐了遗漏的 standalone 次级 relation，1 条明确处理 structured-pattern internal surface，其余 7 条恢复 source surface 顺序。v0.2 分类为 R1=104、R2=27、R3=1。

## 6. 仍然没有解决的东西

当前最重要的后续 blocker 不再是“关系词作用于谁”，而是：

```text
OPEN_CATEGORY membership
GROUP contextual activation
NAMED_COMPOSITE internal relation contract
前格 dependency
absence/open-world
```

也就是说 Relation 层正在收口，而不是继续膨胀。

## 7. Guardrails

source resolution changes=0；conditions compiled=0；execution unlocked=0；Product runtime changes=0；numeric weights/probabilities=0。

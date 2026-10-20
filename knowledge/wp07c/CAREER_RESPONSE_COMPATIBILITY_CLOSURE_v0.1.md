# Career Response Semantics Compatibility Closure v0.1

Status: **251/251 COMPLETE — NEXT ONTOLOGY MAP READY**  
Issue: #426

## 1. 全量结果

三批合计 **251 条，251 个唯一 source_rule_id**。

| 档位 | 数量 |
|---|---:|
| RS1 — known response structure can be represented | 55 |
| RS2 — partial response gain | 34 |
| RS0 — no direct response gain | 162 |

其中 RS1 + RS2 = **89**，约 **35.5%** 的原 GROUP-related blocker 从新层获得了至少部分结构表达收益；但 **0 条**因为 compatibility 工作自动变成 executable。

## 2. 真正的 residual blocker map

| 排名 | residual | 条数 |
|---:|---|---:|
| 1 | RELATION_SCOPE_SEMANTICS | 132 |
| 2 | CATEGORY_OR_COMPOSITE_LEXICON | 123 |
| 3 | CONTEXTUAL_ACTIVATION_SEMANTICS | 78 |
| 4 | INHERITED_ANTECEDENT_GRAPH | 65 |
| 5 | ABSENCE_SCOPE_OPEN_WORLD | 23 |

其他低频但必须保留的 residual：DIGNITY_CARRIER_SEMANTICS 5、SEVERITY_ORDINAL_SEMANTICS 4、COMPOSITE_RELATION_BINDING 6、STRUCTURED_PATTERN_INTEGRATION 4、UNTOKENIZED_SEMANTIC_RECHECK 10、REVIEW_REASON_ONLY_RECHECK 1。

计数允许重叠；一条规则可能同时被多个语义边界阻塞。

## 3. 这 251 条告诉我们的核心事实

原来所谓 GROUP blocker 实际至少混合了：

```text
membership
activation
relation
category
dependency
absence
(+ severity / dignity / named-composite binding)
```

因此未来不再使用“GROUP 全局量词选择”作为主工作流。

## 4. 下一主攻方向

### Priority 1 — Relation Scope Semantics

全量最高频 residual 是 relation scope。下一阶段优先研究：
- 同度；
- 同宫；
- 见；
- 会；
- 同会；
- 会照；
- 朝拱；
- 相对；
- 夹。

这些词在 source 中如何绑定具体 star/member/group/composite 与 palace scope。

**禁止预设它们彼此同义。**

### Priority 2 — Domain/Context-scoped Category Lexicon

吉曜、煞曜、凶曜、桃花、辅佐吉曜、煞忌刑耗等类别仍高频。应按章节、主星系与宫位建立 scoped evidence，不造全局固定“吉曜表/煞曜表”。

### Priority 3 — Contextual Activation

在 membership 与 relation 能正确表达后，再研究 single-member、pair-required、pair-enhanced、qualitative-switch 等机制。

### Priority 4 — Inherited Antecedent Graph

“前格”应显式指向前一 source-rule structure，通过 dependency graph 展开，不能通过文本默认猜测。

### Priority 5 — Absence / Open-world Boundary

“无吉曜”“不见辅弼”等必须依赖显式观测范围，UNKNOWN 不得当 FALSE。

## 5. 与未来模型的连接

本 closure 不做权重训练，但已经把未来定性响应模型真正需要的输入边界分开：

```text
Source condition
 -> membership
 -> relation
 -> activation / interaction
 -> qualitative response
 -> future learned magnitude
```

这使“来源给结构和方向、训练给幅值”的长期原则可以在不污染当前 canonical KB 的情况下继续推进。

## 6. 严格边界

- source truth rewritten = false
- global ANY default = false
- global ALL default = false
- Product runtime modified = false
- numeric weights/probabilities added = false
- automatic execution unlock = false

# Career Response Semantics Compatibility 01 — 前 100 条

Status: **COMPATIBILITY CLASSIFICATION COMPLETE — NO EXECUTION UNLOCK**  
Issue: #421  
范围：CA01-057 → CA04-382，共 **100/100** 条。

## 1. 这一步解决的不是“规则能不能直接跑”

本批只回答：Response Semantics v0.1 对原来的 GROUP blocker 到底提供了多少新的、忠实的表达能力？

因此 **schema-compatible / response gain 不等于 source-resolved，更不等于 executable**。

本批没有：新设 ANY / ALL 默认；新增数值权重或概率；改写 251 closure；修改 Product runtime；解锁任何 condition。

## 2. 三档结果

| 档位 | 数量 | 含义 |
|---|---:|---|
| RS1 — response layer covers known group semantics | 18 | 已知 membership / named-composite / scoped semantics 可以忠实装入新层；仍可因 activation / relation 未定而 blocked |
| RS2 — partial response gain | 17 | 新层解决了一部分表达，但仍有 open category、前格、absence、dignity 或 structured pattern 等外部问题 |
| RS0 — no direct response gain | 65 | 新层没有为该条提供足够的新 canonical 语义，继续沿原 blocker 处理 |

最重要的结论是：**Response Semantics 有价值，但不是“251 blocker 一键解锁器”。** 它把真正的问题拆出来以后，反而能看清下一步该做什么。

## 3. 当前最大真实阻塞

| 剩余 blocker | 条数 |
|---|---:|
| CATEGORY_OR_COMPOSITE_LEXICON | 46 |
| INHERITED_ANTECEDENT_GRAPH | 30 |
| CONTEXTUAL_ACTIVATION_SEMANTICS | 30 |
| RELATION_SCOPE_SEMANTICS | 25 |
| ABSENCE_SCOPE_OPEN_WORLD | 6 |
| STRUCTURED_PATTERN_INTEGRATION | 3 |
| DIGNITY_CARRIER_SEMANTICS | 1 |
| COMPOSITE_RELATION_BINDING | 3 |
| REVIEW_REASON_ONLY_RECHECK | 1 |

这里已经能看到一个重要架构结果：原来很多东西都被笼统叫做 GROUP blocker；现在前 100 条里，真正大量卡住我们的其实是 **开放类别定义（46）** 和 **前格继承（30）**。‘单星还是双星’的 contextual activation 仍有 30 条，但它已经只是多个阻塞维度之一。

## 4. 已获得的具体表达能力

### 4.1 Pair membership 可以与 activation 分开

昌曲、火铃、空劫、辅弼、魁钺、四煞都可以先保存成员 identity，同时继续保持 activation = UNSPECIFIED，而不是强迫选择 ANY / ALL。

### 4.2 Named composite 与 generic shorthand 分开

CA02-181“天机与龙池凤阁同度”已经能保存：龙池凤阁为 named composite，存在 pair requirement；但目标句的“同度”与来源“成对会入”的 relation binding 尚未冻结，所以仍不解锁。

### 4.3 Scoped category 可以有成员而没有触发量词

科文诸曜在事业宫已有域内直接定义，因此成员可保存；但“诸曜”到底要求几个、怎样会入，不能由 membership 自动推出。

### 4.4 Local response evidence 不自动迁移

CA03-228“天机巨门与火铃同度”与 pilot 中“天机巨门卯酉”的局部火铃证据存在候选关联。但 pilot scope 有“卯酉”限定，因此这里只记录 CANDIDATE_ONLY_NEEDS_CONTEXT_BINDING，不自动迁移 single-member valid 或“铃 > 火”的 ordinal 语义。

## 5. 对后续 Knowledge lane 的影响

本批说明后续不宜继续笼统处理 GROUP。先完成剩余 151 条相同 compatibility classification，再用全量统计决定 WP07C 的下一主攻方向。当前前 100 条显示，优先候选是 open/category lexicon、inherited antecedent dependency、relation scope、contextual activation。

## 6. 边界

本批 source resolution change = 0；condition compiled = 0；execution unlocked = 0；Product change = 0；numeric weight / probability = 0。

因此这是一次**知识架构去混淆 + backlog 重分型**，不是 production-rule 扩张。

# 事业宫 GROUP / quantifier 来源词典审查 03（最后 51 条）

Issue #415。本批完成 **CA07-692 → CA09-887**，GROUP / quantifier source review 正式达到 **251 / 251**。本批 51 条由 27 GROUP、16 RELATION_AND_GROUP、7 ABSENCE_AND_GROUP、1 DIGNITY_AND_GROUP 构成；7 条以“前格”继承已有条件。

本批仍然没有创建任何 executable default，规则解锁数为 **0**。其任务是把最后的 source semantics 边界收齐，并将真正需要 PI 决定的 canonical semantics 压缩为一个 Human Gate。

## 最重要的新发现：事业宫自己的“科文诸曜”有直接定义

《深造讲义（下）》事业宫太阴段明确写：

> 所谓科文诸曜，乃指昌曲、龙凤、天才、化科而言。

因此，Career domain 中“科文诸曜”的最强来源候选应展开为：

- 昌曲 → 文昌、文曲；
- 龙凤 → 龙池、凤阁；
- 天才；
- 化科。

这比第 2 批从其他章节得到的“昌曲、魁钺、龙凤”宽泛候选更直接。**第 2 批没有冻结那个候选，因此不存在 canonical 冲突；在本次 closure 中把它明确降级为跨章节参考，不再作为事业宫成员定义。**

另一个重要点是“化科”不是普通星曜，而是化曜/转换操作。说明未来 group schema 不能假定成员全部都是 STAR，必须允许 heterogeneous member types。

## 禄马交驰可以明确，但“禄马”不能顺手一起明确

来源直接定义：

> 禄马交驰，即禄存与天马同度或相对。

因此“禄马交驰”是一个非常干净的命名 composite：
- members = 禄存 + 天马；
- BOTH_REQUIRED；
- relation = 同度 OR 相对。

但 CA07-697 之类只写“见禄马”，没有写“交驰”。所以不能把“禄马交驰”的精确定义自动迁移成所有“禄马” shorthand 的默认解释。

## 七杀 / 破军段进一步证明必须分层

事业宫七杀段直接同时出现：

- 辅弼、魁钺、三台八座；
- 朝拱、同会；
- 煞曜；
- 火铃；
- 同度。

同一段甚至分别说“七杀不宜与煞曜同度”“火铃同会者更不宜”“七杀与火铃同度……”。这已经足够证明：

**membership、group shorthand、spatial relation 和 clause composition 是四个不同语义层，不能压缩为一个 group-present tag。**

破军相关来源又出现“煞曜重而吉曜轻”这一类比较式条件。这说明“吉曜/煞曜”还带有 severity / cardinality 问题；把“重”“轻”直接数字化为 N>=2 或 N>=3 都属于无来源发明。

## 本批显式 OR / NOT

最后 51 条中有 4 条直接出现“或”。其中 CA09-871 是非常有用的反例：

> 前格见辅弼或不见辅弼

这里 OR 连接的是“见辅弼”与“NOT 见辅弼”两个 clause。它绝不意味着“辅弼内部是左辅 OR 右弼”。

所以 closure 的原则是：
- 原文写了 OR，就保留 OR；
- 原文写了 NOT，就保留否定作用域；
- 原文没有写 group-internal cardinality，就不替作者补 ANY/ALL。

## 251 / 251 后的结论

现在已经可以明确区分三类东西：

**可以进入 Human Gate 建议冻结的：**
1. 来源明确的 group membership；
2. 事业宫域内直接定义；
3. 命名 composite 的明确 pair/relation；
4. 原句明写的 AND / OR / NOT / relation。

**仍必须保持 UNSPECIFIED 的：**
1. 昌曲、辅弼、魁钺、火铃、空劫等 shorthand 在没有量词时究竟 ANY 还是 ALL；
2. 吉曜、煞曜、凶曜、桃花诸曜、辅佐吉曜等开放类别的全局封闭集合；
3. 煞轻、煞重、重重等如何转成数值阈值；
4. “前格”如何在执行层展开——应建 dependency graph，不应靠文字猜测。

因此 **HG-KB-GROUP-QUANTIFIER-01 已 READY_FOR_PI**。推荐方案是保守方案 A：冻结来源明确的 membership 与 term-specific semantics，所有来源没有给出的 cardinality 一律保持 UNSPECIFIED。

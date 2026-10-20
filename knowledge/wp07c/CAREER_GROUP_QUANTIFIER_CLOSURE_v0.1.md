# Career GROUP / Quantifier Closure — 251 / 251

Status: **SOURCE REVIEW COMPLETE — HUMAN GATE READY**

三批来源审查已完整覆盖 Career blocker ontology 中所有 **251 条 GROUP-related blockers**：

| 批次 | 范围 | 数量 | 状态 |
|---|---|---:|---|
| 01 | CA01-057 → CA04-382 | 100 | merged #411 |
| 02 | CA04-383 → CA07-691 | 100 | merged #414 |
| 03 | CA07-692 → CA09-887 | 51 | Issue #415 |
| 合计 | — | **251** | **complete** |

## HG-KB-GROUP-QUANTIFIER-01

### 推荐 PI 批准：A — Conservative Source-Preserving

该方案只做四件事：

1. **冻结来源明确的 membership，但不附送默认 cardinality。**
   - 昌曲 = 文昌、文曲
   - 辅弼 = 左辅、右弼
   - 魁钺 = 天魁、天钺
   - 火铃 = 火星、铃星
   - 空劫 = 地空、地劫
   - 四煞 = 擎羊、陀罗、火星、铃星
   - 六煞曜 = 擎羊、陀罗、火星、铃星、地空、地劫

2. **允许 domain-scoped group definition。**
   - 在事业宫语境，科文诸曜 = 昌曲、龙凤、天才、化科。
   - 展开后为文昌、文曲、龙池、凤阁、天才、化科。
   - 不把这个定义无条件推广到所有宫位、所有章节。

3. **允许 term-specific named composite。**
   - 三台八座：PAIR_REQUIRED；来源关系为成对会照。
   - 龙池凤阁：PAIR_REQUIRED；来源关系为成对会入。
   - 禄马交驰：禄存 + 天马 BOTH_REQUIRED，且同度 OR 相对。
   - 这些规则不能推广成“所有两字 pair shorthand 都要求双星齐见”。

4. **显式逻辑只按原文编译。**
   - 原文写“或”才 OR；
   - 写“同时/且”才 AND/同时；
   - 写“无/不见”才 NOT；
   - 写同度、同会、相对、夹、朝拱才建立对应 relation。

### A 不会做什么

A **不会**规定：
- 昌曲 = ANY 或 ALL；
- 辅弼 = ANY 或 ALL；
- 魁钺 = ANY 或 ALL；
- 火铃 = ANY 或 ALL；
- 空劫 = ANY 或 ALL；
- 吉曜、煞曜、桃花诸曜等有一个全局固定名单；
- “煞重”就是 >=2 或 >=3；
- “前格”靠最近一句文字自动继承。

这些全部继续 BLOCKED，直到各自后续 ontology 工作流获得来源支持。

### 不推荐的两个方案

**B：全局 ANY 默认**  
优点是能立刻解锁很多规则；缺点是没有来源根据，会把“火铃”“空劫”“辅弼”等全部解释为任一成员即可，语义污染范围很大。

**C：全局 ALL 默认**  
同样没有来源根据，而且会把很多自然语言 shorthand 过度收紧。

因此知识侧推荐 **A**。

PI 若同意，只需回复：**批准 A** 或 **批准保守方案**。批准后下一工作单元才会真正建立 canonical group ontology/schema，并测算 251 条中有多少可安全从 BLOCKED 转成可编译条件。

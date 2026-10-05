# PL2-O Wealth Normalization Review

状态：COMPLETE — SOURCE-GROUNDED NORMALIZATION REVIEW

## 1. 范围

基于当前 57/100 executable state，对 PL2-K 中 15 条 `SOURCE_NORMALIZATION_REQUIRED` 记录做逐条复核。

本轮使用：

- W01 canonical source rows；
- SRC-ZZ-003 对应的中州派深造讲义下册财帛宫原文；
- WP04 已 source-verified 的 operator / dignity 资产；
- 已冻结的 pair shorthand 和 PL2-G/PL2-L 产品能力。

原则仍然是：**可以从原文澄清的就澄清；原文未给出唯一 executable 语义的地方不猜。**

## 2. 结论

15 条被分成 6 类：

| disposition | 数量 |
|---|---:|
| EXECUTABLE_NORMALIZATION_READY | 2 |
| SOURCE_CLARIFIED_RELATION_PENDING | 9 |
| SOURCE_CLARIFIED_STRUCTURE_PENDING | 1 |
| SOURCE_SPAN_RECHECK | 1 |
| SOURCE_SPLIT_REQUIRED | 1 |
| OPEN_SET_UNRESOLVED | 1 |

### 可直接进入下一产品批次

只有：

- W01-067
- W01-071

二者都能被现有 P05 local facts + any/all boolean 表达，不增加传统结构 primitive。

### 仍不能执行

其余 13 条并非“资料不存在”，而是以下问题之一仍未冻结：

- `会 / 会照 / 冲会 / 见煞 / 受羊陀` 的 relation semantics；
- named structure 的精确边界；
- source row 混合 base trigger 与 stronger modifier；
- “等”造成 open set；
- 当前检索不足以唯一确认 source-span 归属。

## 3. 关键 source clarification

### W01-010

原文不是笼统的“天相受羊陀”，而是：

`羊陀会照 OR 擎羊同度`

所以星曜分支已清楚；剩余问题仅是 `会照` 的 executable relation。

### W01-018

原文明确：

- 财帛宫武曲贪狼；
- 武曲化禄；
- 贪狼化权；
- 事业宫廉贞破军会命宫紫微七杀及文曲化忌。

因此“武贪禄权”的四化归属不再模糊。但“会命宫”仍应使用经过审核的 relation normalization，而不是产品代码自行解释。

### W01-071

原文明确：

`铃星 + 空劫 同度`
或
`火星 + 地劫 同度`

所以旧 W01 摘要中的“空曜”可以被 source span 澄清为这里的“空劫”，本条可以安全 executable。

### W01-076

原文实际上有两层：

1. 天同在财帛宫 -> 白手兴家；
2. 与孤辰同度 -> 性质更明显。

这不是一个简单 AND 条件。后续应该做 source-preserving rule split，而不是把“孤辰”硬设成必要条件，也不能完全丢掉增强支。

### W01-077

原文是“恩光、天贵、天官、天福等杂曜”。

`等` 使集合保持开放。产品侧不能把四个显式名称自动宣布为 exhaustive set。

## 4. Human Gate

本轮 **没有新增 Human Gate**。

这里的问题属于 source normalization / relation formalization，而不是需要用户选择新的理论模型。

如果未来要把“见/会/会照/冲会”统一定义成一个新的通用 relation algebra，而不是逐条 source-preserving 映射，则应另开 Human Gate；PL2-O 不做这件事。

## 5. 下一步

下一单元：

**PRODUCT_PL2O2_NORMALIZATION_SAFE_BATCH**

只消费 W01-067 与 W01-071。

执行后预计：

`57/100 -> 59/100`

其余 13 条继续 fail closed。

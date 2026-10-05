# PL2-L Source-Backed Structure Primitives v0.1

状态：IMPLEMENTED — BOUNDED SOURCE-PRESERVING STRUCTURE LAYER

## 1. 范围

PL2-K 标出了 4 条可以从既有 source-verified 资产出发的结构候选：

- W01-024 禄马交驰
- W01-043 dignity / 入庙
- W01-050 魁钺夹 / 辅弼夹 / 昌曲夹
- W01-057 叠禄 + 羊陀夹

PL2-L 的原则是：

> 只实现已经有明确来源定义的机械结构；不能因为“传统上大概如此”就扩写新格局。

## 2. 本批新增的结构 primitive

### LU_MA_JIAO_CHI

财帛宫原文已明确冻结：

`禄马交驰 = 禄存与天马同度或相对`

运行时只认两种情形：

1. 目标宫同时有禄存与天马；
2. 目标宫与其对宫分别有禄存、天马，顺序不限。

如果禄存和天马都只在对宫，而目标宫本身不参与，则不把它自动记为目标宫的禄马交驰。

### LU_STACK

财帛章节紧接着明确：

`叠禄 = 化禄与禄存同度或相对`

同样要求目标宫参与，不把对宫内部独立结构倒灌给目标宫。

### FLANKING / 夹

只实现四个有 source-backed 依据的 pair：

- KUI_YUE_FLANK = 天魁 / 天钺
- FU_BI_FLANK = 左辅 / 右弼
- CHANG_QU_FLANK = 文昌 / 文曲
- YANG_TUO_FLANK = 擎羊 / 陀罗

“夹”的产品实现严格定义为：

> 两颗指定成员分别落在目标宫地支的前后两个相邻宫位，顺序不限。

不接受两星落在同一侧，也不提供“任意两颗星都可以组成夹”的启发式。

## 3. W01 executable promotion

本批安全提升 3 条：

- W01-024 -> LU_MA_JIAO_CHI
- W01-050 -> KUI_YUE_FLANK OR FU_BI_FLANK OR CHANG_QU_FLANK
- W01-057 -> LU_STACK AND YANG_TUO_FLANK

累计：

```text
EXECUTABLE            57
NORMALIZATION_PENDING 43
PATH_DEPENDENT_HOLD    0
EXCLUDED               0
```

## 4. W01-043 为什么仍不提升

源文支持两个重要事实：

1. “入庙”可以由 source-preserving 庙旺表查表；
2. “太阳天梁或入庙的天梁与文曲化忌同踞”是财帛判断条件。

但仅有 dignity lookup 还不足以唯一回答：

- `太阳天梁` 在该句中应作为哪个 canonical system predicate；
- “与文曲化忌同踞”的作用域如何精确分配到两个分支。

因此 PL2-L 新增 **离散 dignity lookup infrastructure**，但 W01-043 继续 pending，避免产品擅自选择一种语法解释。

## 5. Dignity lookup

数据源：

`validation/wp04_source_closure/DG01_dignity_tables_v0.1.csv`

只加载：

- SOURCE_SPAN_VERIFIED
- source_span_verified=true
- normalization_verified=true

并原样返回 source category。

不做：

- 庙=5、旺=4 等数字化；
- 自动推导“吉/凶”；
- 将 dignity 当作宫级 valence。

## 6. Human Gate 边界

本批不需要 Human Gate，因为：

- 禄马交驰定义在财帛源文中已经直接给出；
- 叠禄定义也直接给出；
- 夹宫只实现 source-backed pair + 十二地支机械邻接；
- dignity 只是 source-preserving lookup。

明确**没有**实现：

- 百官朝拱；
- 宫吉/不吉；
- 格局大/小。

这两类仍分别保留给：

- `HG_PL2L_BAIGUAN_STRUCTURE`
- `HG_PL2N_PALACE_VALENCE_MODEL`

## 7. 下一步

建议进入：

**PRODUCT_PL2O_NORMALIZATION_REVIEW**

先处理剩余 source-normalization blocker，尤其 W01-043 这类“数据能力已经有了，但句法/结构作用域仍需冻结”的记录。

若 PL2-O 遇到必须在多个传统结构定义中作规范性选择的情况，再提交 Human Gate 给用户。

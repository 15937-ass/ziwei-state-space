# PL2-O2 Normalization Safe Batch

状态：IMPLEMENTED — 59/100 EXECUTABLE

## 1. 目标

PL2-O 的 15 条 normalization backlog 中，只有 W01-067 与 W01-071 被评为 `EXECUTABLE_NORMALIZATION_READY`。

本批只消费这两条。

## 2. W01-067

source condition：

`火铃与忌星空劫同度`

冻结为：

```text
(火星 OR 铃星)
AND 任一 P05 化忌
AND (地空 OR 地劫)
```

全部是本宫已观测事实，不引入“见/会/会照”关系推断。

## 3. W01-071

原文澄清为：

```text
(铃星 AND 地空)
OR
(铃星 AND 地劫)
OR
(火星 AND 地劫)
```

特别注意：

`火星 + 地空` **不能**触发本条。

## 4. boolean alternatives

原来的 `all_of + any_of + none_of` 可以表达 CNF 风格条件，但不能无损表达“OR-of-ANDs”。

因此本批给 `CompiledCondition` 增加通用的：

`alternatives: list[list[atom]]`

语义为：

> 至少一个完整 conjunction branch 全部命中。

这是纯工程 boolean 表达能力，不包含紫微斗数理论，不创建新传统 primitive，也不需要 Human Gate。

旧 registry 不包含该字段时行为完全不变。

## 5. 覆盖

```text
EXECUTABLE            59
NORMALIZATION_PENDING 41
PATH_DEPENDENT_HOLD    0
EXCLUDED               0
```

confidence 仍按现有 policy 计算，不因 59/100 自动升级。

## 6. 后续

PL2-O 剩余 13 条都仍有显式 blocker：

- relation normalization；
- named structure boundary；
- source-span recheck；
- rule split；
- open set。

下一步不应继续由产品侧猜测。

建议进入：

**PRODUCT_PL2P_BLOCKER_HANDOFF**

把 13 条分别生成知识侧复核任务，并把已经存在的 8 条 Human Gate requirement 整理成用户可直接审核的 GitHub gate 页面。

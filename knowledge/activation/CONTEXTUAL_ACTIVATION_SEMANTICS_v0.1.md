# Contextual Activation Semantics v0.1

Status: **SOURCE-PRESERVING STRUCTURAL LAYER — NO EXECUTION UNLOCK**  
Issue: #445

## 1. 为什么还需要 Activation 层

前几层已经回答：
- group/category 是什么；
- relation 是什么几何；
- relation 作用于哪个 source node。

但仍不能把 `火铃同度` 自动写成“火星 AND 铃星同宫”，也不能把 `见吉曜` 自动解释成任一预设吉星出现。Activation 层只保存原文明确给出的局部触发结构。

## 2. 本层保留的局部结构

- `或` -> EXPLICIT_OR，只连接原句写出的 alternatives；
- `且` -> EXPLICIT_AND；
- `又/更/再` -> ADDITIVE；
- `同时` -> SIMULTANEOUS，但不自动推出 shorthand 内所有成员 ALL；
- `无/不见` -> NEGATION，执行前要求对应 scope 有闭世界/完备事实证据；
- `前格` -> antecedent dependency；只有已有显式 source-rule edge 才可继承，禁止按邻近文本猜测。

## 3. Member realization

`EXPLICIT_MEMBER_SET_LOCAL` 只允许原句明确列名成员；`NAMED_COMPOSITE_CONTRACT` 保留来源支持的固定复合；普通 shorthand 与开放类别继续分别保持 `SYMBOLIC_GROUP_UNSPECIFIED` / `OPEN_CATEGORY_UNSPECIFIED`。

## 4. 与前层的边界

```
membership known
  != activation quantifier known
relation bound
  != members realized
source negation present
  != database omission proves absence
前格 written
  != previous row may be guessed automatically
```

## 5. Execution boundary

本层仍不编译 Product condition，不设 ANY/ALL/N_OF 全局默认，不增加权重或概率。

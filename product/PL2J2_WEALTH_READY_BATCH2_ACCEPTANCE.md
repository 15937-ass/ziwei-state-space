# PL2-J2 Wealth Ready Rule Batch 2 — B05

状态：IMPLEMENTED — REMAINING READY SET CONSUMED

## 1. 目标

PL2-I 共识别 21 条当前基础设施已经足够、且没有 secondary blocker 的 READY 规则。

PL2-J B04 已消费其中 10 条。

PL2-J2 B05 消费剩余 **11 条**。完成后，PL2-I 定义的 READY backlog 归零。

## 2. 本批 11 条

```text
W01-004  财富持有与享用需结合福德宫区分
W01-045  辅弼：他人助力生财
W01-056  三合宫之间的叠禄作用较弱
W01-060  擎羊 + 天刑/大耗/空劫
W01-072  地空/地劫：突发挫折变化
W01-075  空劫 + 武曲化忌
W01-078  龙池/凤阁：专业技能收入
W01-079  天厨：饮食行业收入
W01-080  红鸾/天喜：异性客户场景
W01-081  天刑/蜚廉：法律纠纷类收入
W01-082  天姚/阴煞：谋略型收入或损失
```

累计 W01：

- EXECUTABLE: 49
- NORMALIZATION_PENDING: 51
- PATH_DEPENDENT_HOLD: 0
- EXCLUDED: 0

## 3. 本批仍然不新增 runtime primitive

B05 继续只使用：

- PALACE_PRESENT
- PALACE_HAS_STAR
- TRANSFORMATION_PRESENT
- PALACE_RELATION
- all_of / any_of

不修改：

- RuleRuntime
- atom schema
- PL2-G topology
- EvidencePackage
- confidence policy

## 4. W01-056 的 2-of-3 编码

W01-056 的条件是“叠禄仅在三方宫相叠”。

当前 approved P05 triad 是：

`P05 财帛 + P01 命 + P09 事业`

B05 不新增 `TRIADIC_STACKED_LU` primitive，而是用现有 boolean groups 编码“至少两个三合宫有禄”：

```text
(P05有禄 OR P01有禄)
AND
(P05有禄 OR P09有禄)
AND
(P01有禄 OR P09有禄)
```

每个“有禄”固定为：

`禄存 OR 任一化禄`

再加上 P05↔P01、P05↔P09 的 TRIAD relation facts。

因此单独一个宫同时有禄存和化禄，也不会错误满足“两个三合宫相叠”。

## 5. Pair shorthand

本批沿用产品侧显式 pair normalization：

- 空劫 -> 地空 OR 地劫
- 辅弼 -> 左辅 OR 右弼
- 龙池凤阁 -> 龙池 OR 凤阁
- 红鸾天喜 -> 红鸾 OR 天喜
- 天刑蜚廉 -> 天刑 OR 蜚廉
- 天姚阴煞 -> 天姚 OR 阴煞

这些只用于当前 source-span verified rows，不建立全局“所有成对星名都等于 OR”的启发式规则。

## 6. W01-079

“天厨或火星天厨在财帛宫”的两个分支都包含天厨，且 projection target 相同。

因此 executable gate 归约为：

`P05 有天厨`

火星单独存在不会触发；火星+天厨会触发，但不会被赋予额外权重。

## 7. Semantic sections

B05 新增两个产品展示 section：

- `consumption / 财富持有与享用`
- `support / 外部助力`

它们直接来自 W01 已 source-span verified 的 projection_domain，不是新增命理理论。

## 8. Confidence

即使达到 49/100，仍有 51 条未执行化，因此：

`LOW_CONFIDENCE`

不因为接近半数覆盖而人为抬升。

## 9. 下一步

PL2-I 原始 READY backlog 已归零。剩余 51 条都至少存在一个明确 capability blocker。

建议下一工作单元：

**PRODUCT_PL2K_WEALTH_BLOCKER_REFRESH**

重新基于 49/100 executable state 生成 blocker-only roadmap，然后再决定：

- 哪些 structure primitive 可以只靠已审核知识库定义；
- 哪些必须进入 Human Gate；
- 哪些直接等待 PL3 temporal state。

这一步应先于继续扩规则，避免重新回到“挑一条做一条”的模式。

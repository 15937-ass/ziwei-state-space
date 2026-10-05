# PL2-K Wealth Blocker Refresh

状态：COMPLETE — 49/100 BLOCKER-ONLY ROADMAP

## 1. 基线

PL2-J2 已把 PL2-I 的 21 条 READY backlog 全部消费。

当前 W01：

```text
total                 100
EXECUTABLE              49
NORMALIZATION_PENDING   51
READY backlog            0
```

PL2-K 不再寻找“顺手再加几条”的规则，而是只回答：

> 剩余 51 条为什么不能执行，下一步应该去哪里，以及哪几类必须经过 Human Gate。

本审计不新增规则、不修改 runtime、不改变传统理论。

## 2. blocker-only routing

| route_class | 数量 | 处理方式 |
|---|---:|---|
| ANTECEDENT_ENGINEERING | 10 | 纯工程引用/依赖机制，可继续 PL2-M |
| STRUCTURE_SOURCE_BACKED | 4 | 已有 source-verified operator/dignity 支持，可做 bounded source-preserving primitive |
| SOURCE_NORMALIZATION_REQUIRED | 15 | 条件词或简称仍非唯一，退回知识/normalization review |
| HUMAN_GATE_REQUIRED | 8 | 会引入新的 palace valence 或 named structure runtime 语义 |
| DEFER_PL3_TEMPORAL | 14 | 需要 natal/decade/year 分层状态，退出 PL2 |

合计 51。

## 3. 10 条 antecedent engineering

这 10 条的主 blocker 不是命理理论，而是 RuleIR 缺少“引用前述规则/结构”的显式机制：

```text
W01-007
W01-008
W01-009
W01-015
W01-027
W01-030
W01-034
W01-044
W01-062
W01-094
```

其中部分 antecedent 本身仍被其他 blocker 卡住，但实现 antecedent linking 不需要创造新传统语义，因此是当前最安全的产品工程下一步。

建议：

**PRODUCT_PL2M_ANTECEDENT_LINKING_V0_1**

## 4. 4 条 source-backed structure candidates

### W01-024 — 禄马交驰

已有：

- `knowledge/operators/auxiliary_eight_v0.1.csv`
- `MOD-AUX-0026`
- AUX01 source-span review

明确存在“禄马交驰” source-backed operator。

可以设计 bounded `STRUCTURE_PRESENT` 映射，不需要由产品重新发明其意义。

### W01-043 — 入庙 / dignity

已有：

- `validation/wp04_source_closure/DG01_dignity_tables_v0.1.csv`
- SOURCE_PRESERVING
- SOURCE_SPAN_VERIFIED
- normalization_verified=true

因此“星曜 dignity lookup”本身属于 source-backed discrete lookup，不需要发明数值强度。

但 W01-043 的完整 disjunction 仍需逐条 normalization 后才能执行。

### W01-050 — 夹宫 family

WP04 operator 层已有多条 source-backed 夹结构：

- 魁钺夹
- 辅弼夹
- 昌曲夹
- 其他 flanking patterns

canonical palace order 也已经冻结。

因此可以做一个**离散 adjacency/flanking resolver**，但只能服务有明确 source-backed pair 的结构；不能推出“任意两星都可以夹”。

### W01-057 — 羊陀夹

`six_malefics_v0.1.csv` 已有：

- 羊陀夹禄存
- 羊陀夹忌
- 羊陀夹紫微七杀

并且 MAL01 已完成 source-span review。

所以羊陀夹属于 source-backed structure family。

以上四条的结论是：

> primitive 家族已有审核依据，可以做 bounded implementation；但本 PL2-K 只做 roadmap，不在同一 PR 中顺手实现。

## 5. 15 条必须先做 source normalization

其中 6 条原本就是 `NORMALIZATION_AMBIGUOUS`。

另外 9 条虽然 primary blocker 被写成 structure primitive，但真正问题是“结构词没有唯一 executable 含义”，例如：

- 受羊陀
- 火铃格
- 会其他煞星
- 陀罗会照
- 空劫会……
- 冲会忌星
- 见煞

WP04 已有相关煞曜和 pair operator 材料，并不代表产品可以自行决定“会/会照/见”到底等于同宫、三合、对宫还是其组合。

因此这些记录统一路由到：

**KNOWLEDGE_NORMALIZATION_REVIEW**

在 source-preserving normalization 完成前，产品侧不猜。

## 6. 8 条 Human Gate

### Palace valence — 5 条

```text
W01-016
W01-017
W01-022
W01-023
W01-035
```

涉及：

- 财帛宫吉 / 不吉
- 事业宫大
- 格局大 / 不大

当前系统没有 approved palace-level scalar、ordinal valence 或“格局大小”状态。

如果要执行这些规则，就必须先批准新的 palace valence representation。

因此：

**HG_PL2N_PALACE_VALENCE_MODEL**

在批准前绝不使用“吉星数量减煞星数量”、LLM 打分或任意数值权重替代。

### 百官朝拱 — 3 条

```text
W01-095
W01-096
W01-098
```

`star_cores.yaml` 已明确指出紫微性质高度依赖“同度、会合与百官朝拱”，但当前 canonical runtime 没有“百官朝拱”的可执行组成定义。

把它做成 reusable named structure 会扩展 runtime 的传统结构语义，因此在 implementation 前应走：

**HG_PL2L_BAIGUAN_STRUCTURE**

本轮只登记 gate requirement，不代替用户批准。

## 7. 14 条直接进入 PL3

14 条需要：

- natal / decade / year 分层；
- 跨层四化；
- 重化；
- 叠禄；
- temporal baseline guard；
- 某些跨层冲会。

这些不应继续污染 natal PL2。

统一路由：

**PRODUCT_PL3_TEMPORAL_STATE**

其中 Human Gate 是否需要新增，等 PL3 设计明确后再判断；PL2-K 不预先批准。

## 8. 为什么下一步选 PL2-M 而不是立刻 PL2-L

PL2-L 的结构工作已经被拆成三类：

1. source-backed，可安全设计；
2. 需要 source normalization；
3. 明确需要 Human Gate。

而 PL2-M antecedent linking 是纯工程关系层，不增加命理 primitive，并且能为后续 scene translation / comparison / 前述结构复用建立通用能力。

因此当前最佳 next unit 是：

**PRODUCT_PL2M_ANTECEDENT_LINKING_V0_1**

完成后再回到 source-backed PL2-L 子集，可以避免把结构工程和领域定义混在一个 PR 里。

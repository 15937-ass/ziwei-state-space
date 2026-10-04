# P1 B02-B — 子时日界语义策略 v0.2

## 结论

晚子时（time_index=12）不是一个可以跨流派强行冻结成“必定当天”或“必定次日”的普通边界条件。

本项目从 B02-B 起把它定义为 **SCHOOL_SENSITIVE_BOUNDARY**：

- 排盘工程层必须记录所使用的日界口径（如 `day_divide=forward`）；
- 同一口径下的两个实现（iztro JS / x-iztro）仍要求严格一致；
- 不同体系或独立引擎在晚子时出现不同日归属，不自动判为程序错误；
- civil date、lunar display date、effective calculation day 必须分开保存；
- 晚子时样本不得因为“选定一个流派”而把另一种候选结构永久丢掉。

## 为什么改动

B02-B v0.1 曾把：

```
当日晚子
==
次日早子
```

扩展成 yearly / monthly / daily / hourly 整个 DTO 必须完全相同。

这个断言过强。它把“某个配置下的实现行为”误写成了“紫微斗数所有体系都必须满足的真值”。

因此 v0.2 不再要求 universal equivalence，而改成：

```
boundary pair
  -> relation probe
  -> equal / different signature
  -> artifact
```

差异首先被记录和分类，再结合流派来源、实现配置和后续案例证据解释。

## 三层验证

### 1. Civil-date layer

继续严格验证公历 / 农历显示日期与边界 marker，防止纯历法错误。

### 2. Same-contract implementation layer

iztro JS 2.6.1 与 x-iztro 0.6.1 在相同 zhongzhou + day_divide 配置下做 full normalized diff。

这一层仍是 hard gate。

### 3. Cross-school / independent layer

独立 Go core 对普通目标继续做 hard core audit。

晚子时 target 被标记为 school-sensitive，不进入“必须逐字段相等”的 hard gate；其差异保留为诊断信息，而不是直接贴上 OUR_BUG / EXTERNAL_BUG。

## 对后续推演引擎的要求

子时尤其晚子时要允许保留候选状态：

```
Candidate A: same-day chart state
Candidate B: next-day chart state
Candidate C: dual-chart/composite interpretation
```

后续 inference engine 不应直接把 A 或 B 删除，而应结合：

- 明确的流派选择；
- 原典规则与 provenance；
- 用户已知历史事件；
- 大限 / 流年 / 流月等后续证据；
- empirical calibration；

决定：

```
single-school resolution
或
weighted composite state
```

这意味着“子时复合盘”应成为未来 Temporal Resolver / History Memory 的一类正式 ambiguity state，而不是 UI 里一个临时备注。

## 当前 P1 验收边界

B02-B 的目标不是证明哪一种子时理论“唯一正确”。

它只负责证明：

1. civil 日期边界没有工程错误；
2. 同一配置的双实现结果一致；
3. school-sensitive 差异被明确标记、不会误报；
4. 子时歧义能够被后续推演层保留下来。

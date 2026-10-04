# P1 B02-C 验收记录：运限动态切换边界

状态：**PASS**

验证运行：GitHub Actions `product-p1-b02c-temporal` run #13（run id 37175612443）。

## 1. 范围

固定 100 个 natal regression seeds，全部使用日间 `time_index=6`，避免把子时流派分歧混入动态切换测试。

三批有界矩阵：

- C1：2027–2030 四个连续农历年界；
- C2：2031–2034 四个连续农历年界；
- C3：2035–2036 两个农历年界 + 一个流月边界 + 一个普通流日边界。

总计 24 targets / 12 transition pairs / 2400 horoscope snapshots。

## 2. 工程一致性

三批均满足：

```text
structural_errors = 0
semantic_errors = 0
iztro JS ↔ x-iztro full diff = 0
independent Go core diff = 0
exact agreement rate = 1.0
```

## 3. 冻结的时间层级不变量

### YEAR boundary

对全部 100 seeds：

- age scope 必变；
- nominal age 必为 +1；
- yearly / monthly / daily / hourly 必变；
- decadal 仅在跨入新的大限范围时变化。

允许的 changed-scope pattern 只有：

```text
age|yearly|monthly|daily|hourly
decadal|age|yearly|monthly|daily|hourly
```

### MONTH boundary

100/100：

```text
decadal = equal
age     = equal
yearly  = equal

monthly = different
daily   = different
hourly  = different
```

### DAY boundary

100/100：

```text
decadal = equal
age     = equal
yearly  = equal
monthly = equal

daily   = different
hourly  = different
```

## 4. 大限范围一致性

在 natal decadal range 能唯一确定 active range 的目标点上：

- C1：708 checkable targets，active-scope mismatch = 0；348 checkable YEAR transitions，transition mismatch = 0；
- C2：794 checkable targets，active-scope mismatch = 0；394 checkable YEAR transitions，transition mismatch = 0；
- C3：752 checkable targets，active-scope mismatch = 0；200 checkable YEAR transitions，transition mismatch = 0。

合计：

```text
2254 checkable target states
0 active decadal mismatches

942 checkable year-transition pairs
0 decadal transition mismatches
```

## 5. 十年窗口的大限切换覆盖

聚合 C1/C2/C3 的 2027–2036 连续十个农历年界：

```text
100 / 100 cases
至少观察到一次 decadal transition
```

transition count distribution：

```text
1 次：84 cases
2 次：4 cases
3 次：6 cases
5 次：6 cases
```

多次 transition 的 16 个 case 全部属于同时存在“目标虚岁尚未落入任何 natal decadal range”的年轻 seed 集合；聚合校验结果：

```text
multiple_transition_cases_without_unmatched_ranges = []
```

因此这些记录保留为 **pre-first-decadal diagnostic**，不作为引擎 mismatch；进入正式可定义 natal range 后，已检查范围与 active decadal 完全一致。

## 6. 结论

B02-C 通过。

本批证明：
1. 六层运限在年/月/日边界上的层级切换关系稳定；
2. 两个同配置实现逐字段一致；
3. 独立 Go core 在共享语义上无差异；
4. 100 个 seed 均覆盖到大限切换；
5. 对可判定 natal range 的大限状态与切换均为 0 mismatch。

B02-C 后，PRODUCT-P1 的 A/B/C boundary validation 条件全部满足。

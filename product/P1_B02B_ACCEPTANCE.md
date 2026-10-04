# P1 B02-B 验收记录：早子 / 晚子与日界语义

状态：**PASS — B02-B complete，P1 尚未关闭**

## 1. 目的

B02-B 专门验证子时换日这一高歧义边界。

本批不再把“晚子一定属于当天”或“晚子一定属于次日”写成跨流派 universal truth，而是把晚子时定义为：

```text
SCHOOL_SENSITIVE_BOUNDARY
```

工程层验证目标变为：

1. civil lunar-date marker 正确；
2. 相同配置下 iztro JS / x-iztro 全字段一致；
3. 晚子边界行为被结构化记录为 relation signature；
4. 独立跨流派引擎不因日界传统不同而被误标为 bug；
5. downstream inference 必须保留 same-day / next-day / composite 候选。

## 2. 执行规模

固定 100 个 natal regression seeds。

8 个目标时点：

- 农历年界：亥、当日晚子、次日早子、次日丑；
- 农历月界：亥、当日晚子、次日早子、次日丑。

总计：

- 100 natal records；
- 800 horoscope snapshots；
- 每份含大限/小限/流年/流月/流日/流时。

## 3. 验证结果

GitHub Actions run #4（product-p1-b02b-zi-day）：

```text
civil boundary errors = 0
semantic profile structural_errors = 0

iztro JS 2.6.1 vs x-iztro 0.6.1:
cases_with_differences = 0
total_differences = 0
exact_case_agreement_rate = 1.000000

independent Go school-neutral hard gate:
cases_with_differences = 0
total_differences = 0
exact_case_agreement_rate = 1.000000
school_sensitive late-Zi targets excluded = 2
```

## 4. 冻结的 relation signature

100/100 seeds 的观察结果：

### 农历年界：当日晚子 vs 次日早子
- yearly: different
- monthly: different
- daily: different
- hourly: different

### 农历月界：当日晚子 vs 次日早子
- yearly: equal
- monthly: different
- daily: different
- hourly: different

### 亥时 vs 当日晚子（两组边界）
- yearly: equal
- monthly: equal
- daily: different
- hourly: different

这些结果是**实现行为画像**，不是跨流派理论裁决。

## 5. 产品语义

晚子时进入产品后必须允许：

```text
Candidate A: same-day state
Candidate B: next-day state
Candidate C: dual-chart / composite interpretation
```

后续可由：
- 明确 school selection；
- canonical source evidence；
- 已知历史事件；
- temporal consistency；
- empirical calibration；

进行显式 resolution。

## 6. 验收结论

**B02-B = PASS。**

它证明：
- 当前 civil 边界数据无工程错误；
- 同一 zhongzhou + day_divide=forward 配置的 JS/Rust 双实现完全一致；
- 子时的流派歧义不会再被错误地强制成单一真值；
- ambiguity 已获得正式产品语义和后续 inference contract。

下一工作单元：`PRODUCT_P1_B02C_TEMPORAL_TRANSITION_BOUNDARY_MATRIX`。

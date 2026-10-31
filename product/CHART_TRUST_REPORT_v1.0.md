# Chart Trust Report v1.0

状态：**FROZEN FOR PRODUCT-P1 CLOSURE**

## 1. 目的

Chart Trust Layer 的目标不是宣称某一排盘程序等于“命理真理”，而是证明产品底座具有：

- deterministic output；
- explicit config；
- cross-implementation reproducibility；
- boundary-aware validation；
- mismatch taxonomy；
- school/config ambiguity preservation；
- regression-ready artifacts。

外部引擎始终是 differential reference，不是 ground truth。

## 2. 冻结配置

当前 canonical 产品验证口径：

```text
algorithm          = zhongzhou
astro_type         = heaven
fix_leap           = true
day_divide         = forward
year_divide        = normal
horoscope_divide   = normal
language           = zh-CN
```

主要跨实现：

- iztro JS 2.6.1；
- x-iztro 0.6.1 Rust/Python。

独立共享核心审计：

- pinned dawang Go core revision
  `947166fc45cd7c8c0849da1bd870f570972a7172`。

## 2.1 Permanent production chart method

P1 establishes deterministic chart trust and cross-implementation regression. Production admission is additionally governed by the permanent `product/CANONICAL_CHART_CONTRACT_v1.0.md`: Zhongzhou + pinned `iztro-js@2.6.1`, fixed config, and fail-closed inference validation. x-iztro and the independent Go core remain audit-only; agreement never authorizes them as production fallbacks.

## 3. P1 回归层

### B01 — full snapshot baseline

- 100 natal；
- 400 horoscope snapshots；
- 每个 horoscope 含 decadal / age / yearly / monthly / daily / hourly；
- JS/Rust full diff = 0；
- independent core diff = 0；
- mismatch ledger 中 UNRESOLVED = 0。

### B02-A — calendar boundaries

- 100 seeds × 12 boundary targets；
- 1200 horoscope snapshots；
- lunar year/month、闰月、公历闰日等边界；
- authoritative calendar marker errors = 0；
- JS/Rust full diff = 0；
- independent core diff = 0。

### B02-B — Zi/day boundary

- 100 seeds × 8 targets；
- 800 horoscope snapshots；
- civil marker errors = 0；
- JS/Rust full diff = 0；
- non-school-sensitive independent core diff = 0。

关键语义：

```text
late Zi = SCHOOL_SENSITIVE_BOUNDARY
```

产品不强行把“当天/次日”其中一个升级为跨流派唯一真值，而保留 same-day / next-day / composite candidates。

### B02-C — temporal transition boundaries

- 100 seeds；
- 24 targets / 12 transition pairs；
- 2400 horoscope snapshots；
- 10 consecutive lunar-year boundaries；
- 1 month boundary；
- 1 ordinary day boundary；
- structural errors = 0；
- semantic errors = 0；
- JS/Rust full diff = 0；
- independent core diff = 0；
- 2254 uniquely checkable decadal target states：0 mismatch；
- 942 uniquely checkable year-transition pairs：0 mismatch；
- 100/100 seed cases 至少覆盖一次 decadal transition。

## 4. 已冻结的 mismatch taxonomy

```text
OUR_BUG
EXTERNAL_BUG
SCHOOL_DIFFERENCE
CONFIG_DIFFERENCE
INPUT_AMBIGUITY
SERIALIZATION_ONLY
UNRESOLVED
```

任何未解决差异不得直接升级为 golden assertion。

## 5. 当前已知非单值语义

第一类正式 ambiguity：

```text
ZI_DAY_BOUNDARY
classification = SCHOOL_SENSITIVE_BOUNDARY
```

这类输入由 Temporal Resolver 保留多候选状态，而不是在 chart layer 静默选择。

后续如果发现新的：
- school-sensitive boundary；
- true-solar-time ambiguity；
- DST / historical timezone ambiguity；
- leap-month school convention；

沿用相同 registry 处理，不重写 P1 的工程原则。

## 6. P1 closure 判据

| Gate | Result |
|---|---|
| Deterministic normalized snapshot | PASS |
| 100 deterministic seed set | PASS |
| Full cross-implementation natal diff | PASS |
| Six temporal layers diff | PASS |
| Calendar boundary matrix | PASS |
| Zi/day ambiguity handling | PASS |
| Year/month/day transition matrix | PASS |
| Decadal range consistency | PASS |
| Independent shared-core audit | PASS |
| Mismatch taxonomy / ledger | PASS |
| UNRESOLVED engineering mismatch | 0 |

## 7. 产品边界

本报告证明的是 **Chart Trust Layer 的工程可靠性**，不证明：

- 紫微斗数现实预测有效；
- 中州派与其他流派理论等价；
- 两个同源实现的一致性等于传统真值；
- 后续 inference 的准确率已经成立。

这些分别由知识 provenance、Rule Runtime、benchmark、empirical calibration 处理。

## 8. 下一阶段

Chart Trust Layer v1.0 冻结后，产品主线进入：

```text
PL2 Executable Knowledge / Rule Runtime
    ↓
PL3 Inference MVP
    ↓
PL4 Benchmark Harness
```

第一版 inference MVP 范围仍冻结为：事业 + 财帛，本命 + 一个大限 + 一个流年。

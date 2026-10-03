# P1 B01 验收记录：100例全层双/三实现差分

状态：**PASS — B01 complete，P1 尚未关闭**

## 本轮实跑规模

固定 100 个 natal regression seeds。每个 seed 计算 4 个目标时点，因此：

- 本命天盘：100 份；
- 完整运限快照：400 份；
- 每份运限含：大限、小限、流年、流月、流日、流时；
- 等价于 2400 个 temporal scope 被逐字段覆盖。

## Engine A / B：全字段兼容验证

- A：iztro JS 2.6.1，source revision `2c7ef9be669df7b19d1799f4dce335fed3794f78`
- B：x-iztro 0.6.1 Rust core / Python binding，source revision `17e35b48dcbf63ded819d96f563a66d1f9e3494c`
- 配置：`zhongzhou / heaven / fixLeap=true / yearDivide=normal / horoscopeDivide=normal / dayDivide=forward`

最终 CI：

```text
cases=100
natal=100
horoscope=400
cases_with_differences=0
total_differences=0
exact_case_agreement_rate=1.000000
```

验证内容包含本命宫位、星曜、亮度、四化、大限，以及大限/小限/流年/流月/流日/流时的落宫、干支、十二宫重排、四化、流曜和流年十二神。

## Engine C：独立实现交叉审计

另以固定 commit 的 Go 引擎 `dawang20250107/ziweidoushu@947166f...` 做 school-neutral/core projection audit。

它不是中州派实现，因此明确剔除/规范化门派专属显示差异，只比较双方声称共同遵循的核心排盘结构。

最终 CI：

```text
cases=100
cases_with_differences=0
total_differences=0
exact_case_agreement_rate=1.000000
```

这提高了“不是同一个 JS 实现自己和自己比较”的可信度，但仍不把软件共识冒充为古法真值。

## 本轮发现并解决的假差异

详见 `mismatch_resolution_v0.1.csv`。本轮共解决 5 类：

1. 星曜数组排序方式；
2. 日期零填充；
3. adapter projection 字段不对称；
4. 小限无流曜的 null / empty-array 表示差异；
5. 中州派“岁破”与通行版“大耗”的门派命名差异。

当前 **UNRESOLVED = 0**。

## 为什么 P1 还不关闭

B01 已证明普通样本 + 四个固定目标时点的全层结果稳定，但用户要求的目标是“先保证排盘正确，而且不只天盘，流年流月流日也正确”。

因此 P1 最终关闭前必须再做 B02 边界矩阵，至少覆盖：

- 农历年界：除夕 / 正月初一；
- 普通月初一与月底；
- 闰月前半 / 后半分界（15/16）；
- 闰月进入与退出；
- 早子 / 晚子；
- 公历闰日；
- 流月、流日、流时的组合边界。

B02 全绿且 mismatch ledger 仍为 unresolved=0 后，才把 PRODUCT-P1 标成 CLOSED。

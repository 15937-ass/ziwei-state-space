# P1 B02-A 验收记录：历法边界矩阵

状态：**PASS — B02-A complete，P1 尚未关闭**

## 1. 目的

B01 已验证普通样本及固定目标时点下的本命与六层运限一致性。
B02-A 专门压测容易导致流年、流月、流日错位的历法边界：

- 农历年末 / 正月初一；
- 普通农历月末 / 初一；
- 闰月进入；
- 闰月十五 / 十六；
- 闰月退出；
- 公历闰日。

本批只用白天时辰（time_index=6），主动隔离子时换日因素；子时边界留给 B02-B。

## 2. 执行规模

固定 100 个 natal regression seeds。

### A1：农历年 / 普通月边界
4 个目标时点 × 100 seeds：

- horoscope snapshots：400
- temporal scopes：2400（每份含大限/小限/流年/流月/流日/流时）

结果：

```text
calendar marker records=100
targets=4
errors=0

JS/Rust:
cases=100
natal=100
horoscope=400
cases_with_differences=0
total_differences=0
exact_case_agreement_rate=1.000000

Independent Go:
cases=100
cases_with_differences=0
total_differences=0
exact_case_agreement_rate=1.000000
```

### A2：闰月 / 公历闰日边界
8 个目标时点 × 100 seeds：

- horoscope snapshots：800
- temporal scopes：4800

结果：

```text
calendar marker records=100
targets=8
errors=0

JS/Rust:
cases=100
natal=100
horoscope=800
cases_with_differences=0
total_differences=0
exact_case_agreement_rate=1.000000

Independent Go:
cases=100
cases_with_differences=0
total_differences=0
exact_case_agreement_rate=1.000000
```

### B02-A 合计

- 100 个固定 natal seeds；
- 12 个历法边界 target；
- 1200 份 horoscope snapshots；
- 7200 个 temporal scope instances；
- JS/Rust exact diff = 0；
- independent Go shared/core diff = 0；
- calendar marker errors = 0；
- unresolved mismatch = 0。

## 3. 本轮实际暴露并修复的测试框架问题

B02-A 不是“一次写对”，而是故意让边界测试去攻击测试框架。本轮发现：

1. **农历月份别名**
   - 引擎输出“腊月”；
   - 初始 assertion 写“十二月”；
   - 语义一致，属于表示差异；
   - validator 现只在 assertion 层规范化 腊月↔十二月、冬月↔十一月。

2. **pre-birth temporal target**
   - 初始历史边界 target 早于最新 natal seed；
   - 会让部分案例产生无效运限比较；
   - CI 现强制：earliest target >= latest birth，否则 preflight 直接失败，不进入大规模 diff。

3. **validation-only target metadata**
   - boundary manifest 含 expected_lunar_marker；
   - JS/Rust adapter 原样保存该字段，而独立 Go DTO 只保存可执行 target keys；
   - independent comparator 现只比较 target_id / solar_date / time_index；
   - 该问题记为 SERIALIZATION_ONLY，不污染 engine correctness。

详见 mismatch ledger M-006 / M-007。

## 4. 执行防卡死机制

本批首次正式执行 `product/EXECUTION_GUARDRAILS.md`：

- natal inputs <= 100 / batch；
- targets <= 8 / manifest；
- horoscope snapshots <= 800 / job；
- job timeout = 15 min；
- install/export/compare 各有独立 timeout；
- total diff >= 500 立即 fail-fast；
- 单 case 最多保留 100 条详细 diff；
- boundary expectation errors >= 10 立即停止；
- 同 commit 自动重试最多 1 次；
- 第二次同类失败必须先诊断并产生新 commit。

这些限制已经在开发过程中实际触发：错误 target 造成大规模差异时，comparator 在 hard cap 到达后主动终止，而不是继续刷屏或占用 runner。

## 5. 验收结论

**B02-A = PASS。**

它证明在已测的年/月/闰月/闰日边界上，三套实现的共同排盘结构保持一致，并且权威历法 marker 检查无错误。

这仍不等于 P1 完成。P1 还必须完成：

- B02-B：早子 / 晚子 / 换日边界；
- B02-C：大限 / 小限 / 流年 / 流月 / 流日动态切换边界；
- 最终冻结 regression contract；
- FINAL acceptance；
- unresolved = 0。

下一工作单元：`PRODUCT_P1_B02B_ZI_DAY_BOUNDARY_MATRIX`。

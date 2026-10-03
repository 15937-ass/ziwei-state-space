# P1 B02 时间边界矩阵

目标：专门验证用户要求的 **流年 / 流月 / 流日** 正确性，同时保留大限、小限、流时作为完整上下文。

B02 不随机抽日期。它用固定版本 `lunar-lite@0.2.8` 在 2032–2035 扫描并选择真实历法边界，再把同一批目标日期交给三个实现。

每个 100 个 natal seed × 18 个 target = **1800 个完整 horoscope snapshots**。

每份 snapshot 同时包含：
- 大限；
- 小限；
- 流年；
- 流月；
- 流日；
- 流时。

因此 B02 实际覆盖 **10,800 个 temporal scopes**。

边界类别：
- 公历闰日；
- 农历除夕 → 正月初一；
- 普通农历月末 → 初一；
- 闰月进入；
- 闰月第15/16日分界；
- 闰月退出；
- 早子 / 晚子；
- 公历年末 / 年初；
- 一个普通白天控制点。

验收条件：
1. iztro JS 与 x-iztro Rust 全字段 diff = 0；
2. independent Go school-neutral/core diff = 0；
3. 任何差异必须进入 mismatch ledger；
4. UNRESOLVED 必须为 0；
5. B01 + B02 都通过后才能关闭 PRODUCT-P1。

# Chart Regression Inputs v0.1

该目录保存**排盘工程回归输入**，不是命理事件标签。

当前 100 条 seed：
- 10 个有效公历日期；
- 5 个时辰 index：0 / 1 / 6 / 11 / 12；
- 男/女各一；
- 固定以中州算法配置做第一轮外部 differential；
- 特别包含多个闰年 2 月 29 日和早/晚子时边界。

这 100 条目前**不是 golden expected output**。

流程：

seed input -> internal engine -> iztro adapter -> diff -> resolve mismatch -> promote to golden case

任何未解决 mismatch 不得通过多数投票自动决定真值。

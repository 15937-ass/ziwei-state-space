# P1 Zhongzhou Chart Conventions v0.2

状态：P1 VALIDATION CONTRACT  
目标：在产品层冻结“排盘正确性”的可检验口径，覆盖本命天盘、大限、流年、流月、流日；流时作为额外完整性检查。

## 1. 主产品口径

- 星盘类型：天盘（heaven / SKY）
- 主排盘参考：中州派
- 农历闰月：十五日（含）以前仍作本月，十六日起按下月安星（fixLeap=true）
- 年界：正月初一（yearDivide=normal）
- 运限年/月干支分界：正月初一口径（horoscopeDivide=normal）
- 晚子时：forward，23:00–23:59 归入次日
- 性别：male / female
- 所有引擎版本、配置、target date/time 必须进入回归记录

## 2. 中州派十干四化

P1 不直接采用 iztro 通行版默认四化，而在 iztro 上显式覆盖为中州派表：

| 天干 | 禄 | 权 | 科 | 忌 |
|---|---|---|---|---|
| 甲 | 廉贞 | 破军 | 武曲 | 太阳 |
| 乙 | 天机 | 天梁 | 紫微 | 太阴 |
| 丙 | 天同 | 天机 | 文昌 | 廉贞 |
| 丁 | 太阴 | 天同 | 天机 | 巨门 |
| 戊 | 贪狼 | 太阴 | 太阳 | 天机 |
| 己 | 武曲 | 贪狼 | 天梁 | 文曲 |
| 庚 | 太阳 | 武曲 | 天府 | 天同 |
| 辛 | 巨门 | 太阳 | 文曲 | 文昌 |
| 壬 | 天梁 | 紫微 | 天府 | 武曲 |
| 癸 | 破军 | 巨门 | 太阴 | 贪狼 |

该表同时与独立中州派开源实现 fortel-ziweidoushu 的 StarDerivative 实现交叉检查。
项目资料中《中州派紫微斗数深造讲义（上）》明确出现“天府（庚干化科）”、“紫微（壬干化权）”、“武曲（壬干化忌）”，并在壬年案例中使用天府化科，因此庚/壬口径不可直接使用其他流派的默认表。

## 3. P1 三层验证

### A. Zhongzhou independent cross-engine
- Engine A: iztro 2.6.1，algorithm=zhongzhou + 本文件四化覆盖
- Engine B: fortel-ziweidoushu 1.3.4（中州派独立实现）

比较共享、可同义归一化的字段：
- 五行局
- 命主、身主
- 命宫、身宫
- 十二宫宫干宫支与宫名
- 十四正曜落宫
- 14 个共享辅煞曜落宫
- 生年四化
- 十二宫大限年龄区间
- 大限宫干支与四化
- 流年宫干支与四化
- 流月宫干支与四化
- 流日宫干支与四化
- 大限/流年/流月/流日七颗共享流曜（引擎均可表达时）

### B. Full temporal implementation sanity
用 iztro 与一个独立重写、开发期以 iztro 校验的引擎做：
- 本命
- 大限
- 小限
- 流年
- 流月
- 流日
- 流时

此层用于发现 adapter / 时间层实现错误，不取代 A 层的中州派独立交叉验证。

### C. Source / invariant audit
任何 A 层差异不得“多数投票”处理。最终必须归类：
- OUR_CONFIG_OR_ADAPTER_BUG
- EXTERNAL_ENGINE_BUG
- SCHOOL_DIFFERENCE
- CONFIG_DIFFERENCE
- LATE_ZI_CONVENTION
- DISPLAY_ONLY
- SOURCE_RESOLVED
- UNRESOLVED

## 4. P1 closure gate

只有同时满足以下条件才可关闭 P1：

1. 100 个固定 birth cases 全部实际运行；
2. 每例至少有一个 target date，并覆盖大限/流年/流月/流日；
3. 100 例无 crash；
4. 所有 shared-core mismatch 都进入 ledger；
5. UNRESOLVED core mismatch = 0；
6. 晚子时、闰日、月/年边界单独保留回归；
7. 输出静态 closure report，记录引擎版本/commit/config；
8. golden cases 只来自已裁决结果。

“两个引擎一致”只证明独立实现一致性，不等于经验意义上的命理预测有效。

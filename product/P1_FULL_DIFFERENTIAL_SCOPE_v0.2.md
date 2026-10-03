# P1 full differential scope v0.2

本阶段把“排盘正确性”从仅本命天盘扩展到完整时间层。

## 主比较

- Engine A: iztro JS 2.6.1
- Engine B: x-iztro 0.6.1 Rust core / Python binding
- 口径：zhongzhou + heaven chart + yearDivide=normal + horoscopeDivide=normal + dayDivide=forward + fixLeap=true

每个 100 个 natal seed 都比较：

1. 本命天盘
   - 阳/农历日期
   - 干支日期
   - 命主/身主
   - 五行局
   - 命宫/身宫
   - 十二宫宫干支
   - 主星 / 辅星 / 杂曜
   - 亮度 / 生年四化
   - 大限宫内 range

2. 四个目标时点的完整运限
   - 大限
   - 小限
   - 流年
   - 流月
   - 流日
   - 流时（超出用户最低要求，作为额外保护）
   - 各层宫位 index / 干支 / 十二宫重排
   - 各层四化
   - 各层流曜
   - 流年岁前/将前十二神

因此本轮一次 CI 实际比较：

- 100 natal snapshots
- 400 horoscope snapshots
- 每个 horoscope 内含 6 个运限层

## 重要限制

x-iztro 明确以 iztro 为算法兼容目标，因此这组比较非常适合发现：
- JS/Rust 实现漂移；
- 序列化错误；
- 配置传递错误；
- 时辰/运限层实现不一致。

但它不是完全独立的传统规则来源，不能单独证明共享算法不存在同源错误。

所以 P1 关闭前还必须加第二道 independent audit：
- 使用独立实现的 Go engine 对本命/大限/流年/流月/流日关键结构做交叉检查；
- 对中州派专属差异单独建立 source/rule adjudication；
- unresolved mismatch = 0 才能 CLOSED。

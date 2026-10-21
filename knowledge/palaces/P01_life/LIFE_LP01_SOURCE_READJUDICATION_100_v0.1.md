# Life Palace LP01 Source Re-adjudication 100 v0.1

100 条历史候选均已直接回读 SRC-ZZ-003 命宫 printed pp3–6。

本批确认 79 条可复用 projection、21 条 CASE_SUPPORT_ONLY、3 条跨期 history feedback。没有因历史候选存在而直接继承 canonical 身份；本文件只记录经过本轮源文复核后可晋级的结果。

最值得保留的修正不是改写规则本身，而是**纠正时间范围表达**：若源文说“运限流年”“年限”“大运或流年”，不能让历史单值 `time_layer` 静默缩窄证据。相关范围已经放入 `LIFE_LP01_SOURCE_TIME_SCOPE_v0.1.json`。

没有新增底层气维、记忆机制、独立时间尺度、数值权重、概率或衰减参数。
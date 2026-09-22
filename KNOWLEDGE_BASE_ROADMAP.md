# Phase II：中州派完整知识库工程路线图

版本：0.1  
状态：ACTIVE

## 1. 目标

在 G1–G6 已冻结的 Paper-1 形式架构基础上，建立一个尽可能完整、可追溯、可执行、可供后续推演与系统辨识使用的**中州派知识库**。

这里的“完整”不定义为穷举所有可能组合，而定义为：

1. **规则覆盖完整**：核心中州派文本中的可执行规则均被抽取、归一化并带来源；
2. **生成逻辑完整**：能够通过星曜、星系、宫位、辅佐煞化、时序层等规则组合生成复杂推演；
3. **案例覆盖完整**：教材中的例证、反例、对比案例都被结构化，作为规则解释和测试样本；
4. **冲突记录完整**：互相冲突、条件不清或版本差异不被强行消解；
5. **推演链完整**：每个结论可以反向追溯到“源文 -> 原子规则 -> 状态/算子 -> 星系/宫位 -> 时序反应 -> 输出”。

## 2. 为什么不能靠穷举组合建库

中州派《深造讲义（上）》明确指出，若把六十星系放入十二宫并逐一说明特殊反应，仅基本组合就可达到数千条，再叠加辅佐煞化、流曜等会合将无法穷举。

因此知识库采用：

~~~text
原子规则
+ 条件算子
+ 结构关系
+ 生成式组合
+ 案例校验
~~~

而不是：

~~~text
把所有命盘组合全部写死
~~~

## 3. 知识库五层结构

### KB-L0：Source Layer
保存：
- source_id
- 文件版本
- 页码/章节
- OCR 状态
- SHA-256（条件允许时）
- 引用片段
- 版权/使用状态

### KB-L1：Atomic Rule Layer
保存：
- 单星性质
- 星系本质
- 辅佐煞化
- 宫位投影
- 三方四正
- 庙旺落陷
- 昼夜/性别等条件
- 本命/大限/流年层级规则

每条规则遵循 Rule Schema v0.2+。

### KB-L2：Concept & Operator Layer
保存：
- 气机维度
- 关系状态
- 星曜气核
- 星系模态
- modifier operators
- palace projection operators
- temporal reaction operators

### KB-L3：Generative Inference Layer
保存：
- rule dependencies
- prerequisite conditions
- conflict sets
- operator composition
- cross-palace dependencies
- temporal inheritance/reaction
- inference templates

### KB-L4：Case & Validation Layer
保存：
- 教材案例
- 对比案例
- 反例
- 原书“此例说明什么”
- 模型重构结果
- 是否能由规则库自动重现

## 4. “完整中州派知识库”覆盖域

### A. 星曜本体
- 十四正曜全文
- 辅曜
- 佐曜
- 煞曜
- 化曜
- 杂曜/小星（中州派真正用于推断者）

### B. 六十星系
每个星系：
- principal mode
- 三方四正结构
- 庙陷条件
- 四化响应
- 辅煞响应
- 运限反应
- 典型例证
- 对比星系
- 可约化/涌现性质

### C. 十二宫
每个宫：
- 基本语义域
- 主星/星系在该宫的投影规律
- 与其他宫的依赖
- 三方四正作用
- 特殊跨宫规则
- 本命 vs 运限差异

### D. 时序体系
- 本命
- 大限
- 流年
- 流月（如核心中州派材料支持）
- 原局本质与运限反应
- 原局四化/运限四化关系
- 触发/响应条件

### E. 规则元知识
- “何时不能机械套规则”
- 规则优先级
- 规则适用范围
- 反例
- 例外
- 规则冲突
- 文本版本差异

## 5. 推演知识库不是“关键词搜索库”

最终需要支持如下查询：

~~~text
输入：
命盘结构 + 时间层

系统：
1. 找出相关原局星系
2. 构建原局宫位本质
3. 应用辅佐煞化算子
4. 找出当期时序输入
5. 激活相关星系模态
6. 跨宫传播
7. 生成语义输出
8. 给出完整证据链
~~~

输出必须包含：

- conclusion
- latent-state explanation
- active rules
- source provenance
- conflict/uncertainty
- alternative interpretations

## 6. Phase II 工作包

### KB-WP01：全语料目录与覆盖矩阵
建立每本中州派核心材料的章节级 coverage matrix。

### KB-WP02：十四正曜全文穷尽抽取
从当前代表性 200 条扩展到十四正曜全文级规则库。

### KB-WP03：六十星系全文规则抽取
不是只保留 principal mode，而是抽取每个星系的所有条件性规则、四化、辅煞、运限和案例。

### KB-WP04：辅佐煞化/杂曜完整算子库
对所有中州派实际使用的小星与辅煞化建立可执行 operator catalog。

### KB-WP05：十二宫全文投影规则库
对《深造讲义（下）》十二宫逐章抽取，建立 palace-specific projection rules 与 cross-palace rules。

### KB-WP06：案例库与对比案例库
把讲义案例转成结构化 test cases，并建立“案例证明的是哪条规则/反应原则”。

### KB-WP07：推演引擎
把上述知识串成 evidence-first inference graph，支持输入命盘后自动生成规则链，而不是直接让 LLM自由发挥。

## 7. 人工审核原则

Phase II 不再每个工作包都要求 PI 审核。

仅以下情况升级人工审核：

1. 发现需要改变 G1–G6 冻结原则；
2. 出现中州派内部无法自动解决的重大冲突；
3. 需要新增 primitive qi；
4. 要改变某类核心 operator；
5. 某一知识域准备声明“完整覆盖”时。

其余：
~~~text
extract -> critic -> normalize -> test -> commit
~~~
自动执行。

## 8. 完整度指标

未来知识库不只报告“规则条数”，而报告：

- Source Coverage %
- Chapter Coverage %
- Rule Extraction Coverage %
- Provenance Completeness %
- Conflict Resolution/Logging %
- Case Reconstruction %
- Inference Trace Completeness %
- Unknown/Unresolved Rate

只有这些指标达到预设阈值，才把某一模块标成 COMPLETE。

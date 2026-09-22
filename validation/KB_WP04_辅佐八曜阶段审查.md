# KB-WP04 阶段审查：辅佐八曜算子库

状态：REVIEWED（辅佐八曜完成）；KB-WP04继续

## 一、来源范围

《中州派紫微斗数深造讲义（上）》印刷页165–171：
- 辅佐八曜总论
- 天魁天钺
- 左辅右弼
- 文昌文曲
- 禄存天马

本轮严格把自然语言规则拆为条件算子，不把吉曜简化为固定正分。

## 二、结果

- operator rules：103
- 总论：2
- 天魁天钺：19
- 左辅右弼：19
- 文昌文曲：32
- 禄存天马：31
- required fields缺失：0
- duplicate operator_rule_id：0
- 全部 epistemic_type_source = EXPLICIT
- 全部 status = reviewed

## 三、算子类型分布

- projection：30
- transform：25
- enhance：21
- pair_interaction：12
- structural_relation：7
- gate：6
- weaken：2

## 四、关键理论反馈

### 1. 辅曜与佐曜不能放在同一个“吉星增益”桶中

源文明确区分：魁钺、辅弼偏他力；昌曲、禄马偏自力。后续模型至少应保留 `support_source = external/opportunity` 与 `support_source = self-effort`。

### 2. 同一曜的作用高度依赖配对、宫位、时间层和星系

例如魁钺必须重视成对会合与阴阳调和；辅弼单星可能只增加数量而不增加有效助力；昌曲在不同正曜星系中可由才华转为轻浮、桃花或文书风险；天马无禄只表示移动，不自动表示得财。

### 3. 组合存在明显非单调性

火羊、铃陀在特定结构中可互相抵消缺点；辅弼单星反而可能打破这种平衡。禄存本身为资源稳定，却因羊陀夹与化忌同度时可反转为破财语义。因此 operator 必须允许 pair_interaction / gate / transform。

### 4. 宫位投影应与状态变换分开

同一辅佐曜在命宫、夫妻、子女、交友、事业、迁移等宫的可观测语义不同。因此 modifier operator 只描述状态变化，传统婚恋/亲属/疾病等具体应象继续放在 projection/traditional label 层。

### 5. 时间激活不能只做“加权”

原局魁钺被流魁钺冲起、叠禄、叠马、流陀阻行等，说明原局结构与运限输入之间存在 activation 关系。后续引擎需显式识别 temporal trigger，而不是简单把流曜叠加分数。

## 五、安全与现代语义边界

疾病、事故、婚恋、性别、行为等古代断语均保留为 traditional_semantic_label / historical label，不作为现代医学、心理学、法律或因果结论。

## 六、下一步

进入煞曜页172–176：
- 擎羊
- 陀罗
- 火星
- 铃星
- 地空
- 地劫

目标是建立六煞 canonical operator catalog，并重点抽取：激发/磨炼/破坏、明暗冲突、宫位适配、与正曜星系的非单调相互作用。

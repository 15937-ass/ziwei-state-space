# KB-WP03 六十星系全局总审查

状态：EXTRACTION_COMPLETE / VALIDATION_PENDING

## 一、范围

本工作包覆盖《中州派紫微斗数深造讲义（上）》六十星系章节（印刷页33–164），共60个基本星系。

原书后记明确说明，本章主要介绍的是各星系经行十二宫时的“特殊反应”，并不重复初级讲义已经讲过的三方四正一般规则。因此本知识库的COMPLETE含义必须限定为“六十星系特殊反应规则抽取完整”，不能误称为整个中州派知识体系已经完整。

## 二、全局统计

- 60个系统全部有规则
- 规则总数：2193
- principal mode：60/60
- required fields缺失：0
- duplicate rule_id：0
- coverage matrix计数不一致：0
- 全部 source epistemic type = EXPLICIT
- 全部 status = reviewed

分组规则数：
- G1 系统1–10：314
- G2 系统11–20：332
- G3 系统21–32：365
- G4 系统33–42：369
- G5 系统43–52：437
- G6 系统53–60：376

主要interaction roles：
- temporal_reaction：1015
- cross_system_interaction：364
- mode_modifier：351
- mode_definition：234
- case_evidence：81

另有219条 interaction_delta，149条 case_level。

## 三、canonical产物

未来推演不再直接拼接六个分组文件，而优先使用：

- knowledge/rules/systems/sixty_systems_canonical_v0.1.csv
- knowledge/sixty_system_modes_v0.1.yaml

六个G1–G6文件继续保留，作为来源追踪和分组维护文件。

## 四、全局理论结论

### 1. 六十星系不是“组合后的吉凶分数”

60个principal mode几乎都表现为中尺度组织状态，例如：
- 精神/物质平衡
- 主动/被动
- 决断/短虑
- 有情/无情
- 浮荡/稳定
- 理智/情绪
- 权威/横霸
- 奉公/私利
- 正直/徇私
- 尖刻/明断

这些变量描述的是基础气机在特定结构中如何被组织，而不是简单的正负强度。因此星系层继续表示为：

`z_s = M_s(q_stars, modifiers, structure)`

而不是 `z_s = scalar_goodness`。

### 2. state-dependent reaction 得到大量文本支持

同一个运限输入对不同原局本质的反应经常不同，甚至方向相反。六十星系章节反复要求：先判原局本质，再判断该本质对后天宫垣的反应。

因此后续引擎应以：

`reaction = R(natal_essence, system_mode, temporal_input, context)`

作为核心，而不能用固定的 `rule -> event` 映射。

### 3. 非单调性是结构性特征，不是例外

全文大量出现：
- 化禄不一定更好；
- 化忌不一定只产生单一负面结果；
- 强旺不等于稳定；
- 吉曜可能强化错误的原局本质；
- 煞曜在少数星系中可作为激发；
- 同一好运对不同mode可能产生完全不同的利用率。

因此数值模型不能预设禄权科忌和煞曜为固定加减分。

### 4. context gate 与跨系统关系是必要变量

三方星系、对宫星系、夹宫结构、庙陷、禄存位置、特定四化联动等，经常改变principal mode或后天反应。

因此不能把星系看成独立节点；它必须是图结构中的局部状态。

### 5. 时间尺度不可压平

源文多次明确区分：
- 大限与流年同一星系的意义不同；
- 流年可以是短期触发；
- 大限可能形成长期路径；
- 当前运限是否善用会影响后运。

这支持未来区分 `u_decade`, `u_year`，并预留 `historical_context_t`。

### 6. human response 在源文内部就是显式中介

守成、进取、退居幕后、选择合作、是否弄权、是否持盈保泰、是否改变环境等，都反复作为结果差异的中介。

因此未来可定义：

`u_t = (u_t^astro, u_t^human, d_t^external)`

但 `u_t^human` 只有在外部因果数据建立后，才可以讨论真正的controllability；传统趋避建议不能直接当作已验证控制律。

### 7. path dependence 已有文本证据，但暂不重开G5

多个系统出现：某个大限形成的因循、顽嚣、冷退、浮荡、短志等，会继续影响后运；当前好运使用不当也可能形成后续不利。

因此未来模型可增加 `historical_context_t` 或递归状态更新接口，但Paper-1仍保持冻结的最简状态依赖反应结构。

## 五、知识边界

本知识库中的疾病、事故、自毁、官非、婚姻、性别等内容，只作为传统文本语义标签保留。它们不是现代医学、心理学、法律学或因果科学结论。

原书本身也强调现代社会背景变化会使传统断语需要重新统计与征验。因此这些字段进入未来实证阶段时，必须重新操作化，而不能直接作为真值标签。

## 六、完整度判断

KB-WP03可以结束“全文抽取”阶段。

推荐状态：

`EXTRACTION_COMPLETE_VALIDATION_PENDING`

暂不标记整个推演系统COMPLETE，原因是：
1. KB-WP06尚需将81个明确case_evidence及其他教材案例建立独立回归案例；
2. KB-WP07尚需用evidence-first inference engine做端到端重放；
3. 六十星系后记本身说明，本章只讲特殊反应，一般三方四正规则仍须与其他章节合并。

## 七、下一工作包

KB-WP04：辅佐、煞曜及化曜的完整operator库。

核心目标是把“加强、削弱、转化”从自然语言抽成可执行operator，并区分：
- star-specific modifier
- system-specific modifier
- relation-specific modifier
- temporal activation
- non-monotonic gate

之后再进入KB-WP05宫垣投影、KB-WP06教材案例、KB-WP07推演引擎。

# KB-WP03 六十星系全文规则库：全局红队审查 v0.1

状态：**WP03 RULE EXTRACTION REVIEWED**

> 注意：这里的 REVIEWED 只表示《中州派紫微斗数深造讲义（上）》六十星系章已完成结构化抽取、schema审计和全局一致性检查；不表示传统理论已经得到经验验证，也不等于推演引擎已完成。

## 一、最终覆盖

来源：SRC-ZZ-002，《中州派紫微斗数深造讲义（上）》六十星系章，印刷页约33–164。

六组规则数：

- G1 系统1–10：314
- G2 系统11–20：332
- G3 系统21–32：365
- G4 系统33–42：369
- G5 系统43–52：425
- G6 系统53–60：376

**总计：2181条 reviewed rules，60/60系统覆盖。**

另生成：

`knowledge/sixty_system_modes_canonical_v0.1.csv`

其中60个系统各有且仅有一个 source-grounded principal mode 入口。

## 二、工程完整性审计

最终检查：

- 60个 system_no 全部存在；
- 60个 principal mode 全部存在；
- required fields 缺失 = 0；
- duplicate rule_id = 0；
- source_id 全部来自 SRC-ZZ-002；
- epistemic_type_source 全部为 EXPLICIT；
- status 全部为 reviewed；
- controlled vocabulary 异常 = 0。

本轮全局红队还发现早期G2文件有9条旧schema列错位，G3/G4有3条 interaction_delta 字段放错位置，现已修复，未改变源文含义。

## 三、源文冲突审计

此前唯一开放项：

`CF-KB-0035-001`

涉及系统35“天相独坐巳亥”中刑忌夹与开创力的OCR疑义。

已直接核对原PDF印刷页104–105，确认原文意为：

> 刑忌所夹会使该天相偏向开创力，但伴随艰辛。

因此：
- `ZZ-SYS-35-005` 已修正为正式规则；
- conflict 已标记 resolved；
- 当前 open source conflicts = 0。

这也说明后续遇到OCR与结构逻辑冲突时，应优先回原PDF版面核验，而不是靠模型自动“合理化”。

## 四、六十星系规则的结构画像

2181条规则中，最大的一类是运限反应：

- temporal_reaction：1012条
- mode_modifier：351条
- cross_system_interaction：363条
- mode_definition：233条
- case_evidence：76条
- palace_projection：43条

这说明《深造讲义》的六十星系不是一份静态“性格词典”，而是大量描述：

```
原局本质 × 星系组合 × 辅煞四化 × 运限环境 -> 条件反应
```

因此我们最初把中州派形式化成 state-dependent reaction，而不是静态评分表，是合适的架构选择。

## 五、principal mode 的全局性质

60个 principal modes 大致可归入若干“派生状态族”，但这里只做 HYPOTHESIS 级聚类，不升级为 primitive qi：

### A. 稳定与承载族
安定/动荡、沉稳/虚浮、稳定/浮荡、刚毅/脆弱、坚忍/躁进、适应/反拗、豁达/短志。

### B. 行动与目标族
主动/被动、进取/因循、上进/下游、果敢/顽嚣、决断/短虑、开创/因人成事。

### C. 关系与支持族
得助/孤立、有情/无情、融合/孤克、不受拖累/受拖累、正直/徇私。

### D. 欲望与规范族
物欲/情欲、欲望/野心、奉公/私利、正直/精明、祥和/权术。

### E. 认知与情绪族
理智/情绪、深沉/冲动、明朗/阴暗、英华内敛/疑忌、尖刻/明断。

### F. 结构平衡族
精神/物质、感情/理智、刚/柔、发射/收敛、浪漫/原则等。

这些类别有大量交叉，因此当前正确做法不是新增几十个独立状态维度，而是下一阶段检查它们能否由较少的 primitive qi 维度、关系变量与 context gate 组合生成。

## 六、对G2/G3/G4的反向检验

### G2：气机本体分层

**无需重开。**

六十星系显示：
- 同一个自然语言概念可以分裂成多个可区分变量；
- 例如系统48源文明确区分“意志”与“毅力”；
- 因此 ontology refinement 必须依赖可区分性、可观测性与规则覆盖，而不是语义相近就合并。

### G3：十四正曜气核

**无需重开。**

系统层并未把十四正曜的基础性质推翻，而是通过：
- 同度组合；
- 三方结构；
- 辅佐煞化；
- 宫位庙陷；
- 运限输入

形成 emergent mode。

因此仍保留：

```
star cores -> system composition -> emergent system mode
```

### G4：六十星系结构

**得到显著加强。**

目前2181条规则直接支持：
- principal mode；
- mode modifier；
- cross-system interaction；
- palace projection；
- temporal reaction；
- interaction delta。

### G5：状态空间与反应模型

**主模型不重开，但需保留三个扩展接口：**

1. `historical_context_t`：某大限的反应会影响后运；
2. `human_response_t`：人的选择会调节同一传统输入的后果；
3. `time_scale`：大限与流年的reaction function不可强制相同。

这些在Paper-1中可定义为扩展接口，不必现在引入可学习递归参数。

## 七、最重要的红队结论：绝不能采用“固定吉凶加权表”

六十星系全文出现大量非单调关系：

- 吉化可能强化错误本质；
- 化忌在某些结构中可形成刺激、收敛或突破；
- 庙旺未必意味着更稳定；
- 良好运可能只产生虚名或短期收益；
- 相同运限对不同 natal mode 可产生相反输出；
- 同一结果可由不同机制产生。

因此禁止未来把规则简化为：

```
禄 = +1
权 = +1
科 = +1
忌 = -1
煞 = -1
```

更合适的形式是：

```
z_s = M_s(x_natal, structure)
x'_t = T_{star, transform, context}(z_s, u_t)
y_t = P(y | x'_t, palace, human_context)
```

其中算子可为：
- enhance
- weaken
- transform
- gate
- nonlinear/context-dependent reaction

## 八、传统高风险语句的边界

知识库保留疾病、事故、自毁、刑法、婚恋等传统应象，是为了完整保存源文语义。

但这些条目：
- 不自动转成现代医学诊断；
- 不自动转成心理风险判定；
- 不自动转成现代法律预测；
- 不作为经验因果关系。

此类规则通过 `case_level` / notes 保留来源语境，后续外部验证需独立设计标签体系。

## 九、WP03是否COMPLETE

**规则抽取层：完成。**  
**工程模块总体：暂不标 COMPLETE。**

原因：

- KB-WP06 尚需把76条教材案例整理成可执行 regression cases；
- KB-WP07 尚需将2181条规则接入 evidence-first inference engine；
- 只有规则可以被程序正确召回、组合、冲突处理并重放教材案例后，60个coverage unit才升级 COMPLETE。

因此当前统一状态：

```
60/60 systems = REVIEWED
WP03 extraction = DONE
WP03 executable validation = PENDING
```

## 十、下一步

下一主工作包切换到：

**KB-WP04：辅佐、煞曜、四化及相关修饰算子库。**

其目标不是再建立新的“星曜性格表”，而是从印刷页165以后抽取可作用于六十星系的：

```
增强 / 削弱 / 转化 / 门控 / 非线性条件算子
```

这将是把当前2181条星系规则真正转成可执行中州派推演系统的关键一层。

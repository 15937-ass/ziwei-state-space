# Paper 1 内部验证报告 v0.1

## 1. 目的

本报告只评价**形式化系统内部质量**，不评价紫微斗数对现实人生事件的预测有效性。

当前内部验证回答：

- 规则结构是否完整；
- 来源是否可追溯；
- 原子化是否稳定；
- 状态/评价/输出是否分层；
- 六十星系是否可放入统一交互框架；
- 潜状态是否至少具有结构观测通路；
- 模型是否能重构讲义自身的推断逻辑。

不回答：

- 是否优于随机基线预测真实人生；
- 是否具有因果有效性；
- 是否能用于医疗、投资、婚姻等现实决策。

## 2. 结构化规则语料

当前机器可读语料共 **200 条原子规则**，覆盖十四正曜：

- 紫微、天机、太阳、武曲：各 25 条；
- 其余十颗正曜：各 10 条代表性规则。

这是一套“跨十四星的建模样本”，不是全文穷尽式知识库。

### 2.1 Schema 完整性

对 Rule Schema v0.2 的 18 个关键字段检查：

- rule_id：200/200
- school：200/200
- source_work：200/200
- source_location：200/200
- subject / condition：200/200
- target_literal / target_normalized：200/200
- operator / state_change / valence：200/200
- epistemic_type_source：200/200
- evidence_text：200/200
- extraction_confidence / status：200/200

当前字段级完整率：**100%**。

这只说明数据结构完整，不说明规则含义绝对正确。

### 2.2 规则类型分布

当前 200 条规则中：

- qi_state：123
- structural_relation：10
- outcome_descriptor：67

算子分布：

- enhance：100
- weaken：24
- transform：16
- define：21
- assert：24
- condition：12
- compare：3

state_change：

- increase：100
- decrease：24
- transform：16
- nonlinear：4
- none：56

valence：

- context_dependent：93
- favorable：43
- unfavorable：41
- not_applicable：23

一个重要结果是：

> 46.5%（93/200）的规则在当前编码下明确属于 context-dependent valence。

这直接支持“状态变化不能与吉凶评价合并”的 G1 决定。

## 3. 双遍审查样本

首批 100 条中抽取 20 条进行了 producer -> red-team 二次审核。

结果：

- 来源追溯：20/20
- epistemic type：20/20
- target mapping：20/20
- atomicity：18/20
- 总体直接通过：18/20
- 需要修订：2/20

两条主要问题：
1. 三层排序关系应拆为 pairwise comparison；
2. 多结果分类规则不能塞在一个原子关系中。

注意：

> 这不是独立人类标注者之间的 Cohen's kappa。

当前只能称为**模型双遍一致性/审计**。若论文投稿要求正式 inter-annotator reliability，应增加一名独立人工标注者或另一套盲标流程。

## 4. 本体结构审计

G2 冻结的正式框架：

~~~text
L0 结构底座
L1 内在气机
L2 关系网络
L3 场景投影
L4 评价层
~~~

当前：
- 15 个 L1 候选；
- 4 个 L2 候选；
- QI-16 目标导向性暂作为 derived-only；
- QI-17 韧性作为高优先级候选。

结构能观性审计没有发现正式核心变量完全没有输出通路。

部分可观：
- QI-06 决策激活度
- QI-11 感性—理性张力
- QI-14 遮蔽—显明
- QR-03 竞争激活
- QR-04 支持资源

因此 Paper 1 可以报告：

> 当前候选本体在结构层面不存在明显“孤立状态变量”。

但不能报告：

> 系统已经在经典控制意义上完全可观。

## 5. 六十星系覆盖

已经建立：

- 60 个基本星系索引；
- 6 个基本盘组；
- 每个星系至少一个 principal mode；
- 10 个可复用 mode family。

这说明“六十星系”可以用：

~~~text
base composition
+ interaction delta
+ mode
+ context gates
~~~

统一描述，而不必建立 60 个互不相干的黑箱模型。

## 6. 内部重构测试

当前选取三类教材逻辑进行 reconstruction。

详细见：
`validation/internal_reconstruction_cases.md`

测试目标不是“案例预测正确”，而是：

> formal model 是否能复现原书的推理依赖关系。

三个测试分别覆盖：

1. **同一运限结构 + 不同原局本质 -> 不同反应**
2. **原局宫位本质 + 后天运限刺激 -> 具体反应**
3. **跨宫联合投影，而不是单宫孤立解释**

三类逻辑均可以在当前模型中表示。

## 7. 当前失败与限制

### 7.1 尚非完整规则库
200 条规则不足以声称穷尽十四正曜、六十星系、辅佐煞化与十二宫全部知识。

### 7.2 没有真正独立的人类双标
当前红队仍属于同一研究系统内的第二遍审核。

### 7.3 没有外部事件数据库
所以：
- 无 sensitivity/specificity；
- 无 calibration；
- 无 AUC；
- 无 prospective prediction；
- 无 causal validation。

### 7.4 OCR 仍存在风险
部分标题与字词有扫描识别错误，论文附录级数据应对关键原文做人工版面复核。

### 7.5 数值不可辨识尚未真正测试
目前只做结构性参数混淆预警。

## 8. Paper 1 可报告的 Results 边界

可以报告：

- 规则 schema 与机器可读表示；
- 200 条跨十四正曜规则的结构化结果；
- 60 星系统一交互架构；
- 层级本体；
- 结构能观性审计；
- 内部教材逻辑重构；
- 可执行软件规格。

不能报告：

- 紫微斗数“被科学证明”；
- 对真实人生具有预测力；
- 气是物理实体；
- 控制理论证明“趋吉避凶”有效；
- 模型已经具备临床/金融/职业决策能力。

## 9. 下一步

Paper 1 剩余工作主要是：

1. 完善规则引擎与自动 validation script；
2. 将本文结果整理为论文 Results；
3. 写完整 Manuscript v0.1；
4. 做 G6 结论、贡献、局限性红队审核。

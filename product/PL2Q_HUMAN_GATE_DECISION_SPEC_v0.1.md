# PL2 Human Gate Decision Specification v0.1

状态：**HUMAN APPROVED — CONSTRAINED SEMANTIC EXPANSION**

批准日期：**2026-10-05**

本文件冻结两个 PL2 Human Gate 的产品语义边界：

- HG_PL2N_PALACE_VALENCE_MODEL
- HG_PL2L_BAIGUAN_STRUCTURE

本决议的目标不是为了提高 W01 executable coverage 而补齐未知权重，而是允许产品增加必要的理论对象，同时继续保持 source-preserving、fail-closed、可校准、可审计。

---

## 1. 总体原则

### 1.1 五层语义边界

产品后续统一按以下层级处理：

~~~text
Observable Facts
    ↓
Named / Source-backed Structures
    ↓
Typed Latent / Aggregate States
    ↓
Contextual Semantic Projection
    ↓
Real-world Manifestation
~~~

对应含义：

1. **Observable Facts**：排盘可确定事实，例如星曜、宫位、四化、三方四正、夹、同度等。
2. **Structures**：source-defined 结构，例如禄马交驰、夹、成格/破格、百官支持结构。
3. **States**：星系或宫位的类型化状态与方向性修饰，例如 support 增强、disruption 增强、某性质被削弱或转化。
4. **Projection**：针对具体 palace/domain/question 得出的语境化判断。
5. **Manifestation**：现实中的财富、事业、婚姻、事件等实际应象。

PL2 只允许安全推进前四层；不得把第 2/3 层直接等同于第 5 层。

### 1.2 禁止 universal score

继续明确禁止：

- 吉星数量减煞星数量；
- 庙旺固定换算成 5/4/3/2/1；
- 左右、魁钺、昌曲、煞忌等人工指定固定数值权重；
- LLM 凭经验生成 palace score；
- 将不同宫位、不同星系中的同一星曜假定为相同增益；
- 将“吉/不吉”视为与具体问题无关的全局标量。

中州派资料将辅佐煞化杂曜对基本星系的作用概括为“加强、削弱、转化”，但没有给出统一可移植的数值权重；因此 PL2 只冻结 source-backed 的作用方向、作用对象与条件，不冻结未知幅值。

### 1.3 参数未知必须显式保留

凡来源只支持方向、不支持幅值时，运行时/知识层必须显式保留：

~~~yaml
effect_direction: increase | decrease | transform | conditional
magnitude_status: UNIDENTIFIED
parameter_status: CALIBRATION_REQUIRED
~~~

未来数值化只能进入独立 calibration / system-identification track，不得在 PL2 Human Gate 中拍板。

### 1.4 格局判定必须 pattern-specific

不得建立：

~~~text
三方四正无煞 = 所有格局成立
见任一煞 = 所有格局统一破格
~~~

这样的 universal rule。

只有当具体 source-defined pattern 明确给出成格、破格、无煞忌、某星破格等条件时，才能形成对应 predicate。

---

# 2. HG_PL2N_PALACE_VALENCE_MODEL

## 2.1 Human Gate 裁决

~~~yaml
gate_id: HG_PL2N_PALACE_VALENCE_MODEL
decision: APPROVE_WITH_CONSTRAINTS
human_status: HUMAN_APPROVED
approved_at: 2026-10-05
~~~

本 Gate **批准状态表示体系，不批准固定吉凶评分体系**。

原 Human Gate 名称保留，以兼容既有 PL2-K / PL2-P 路由；其正式语义升级为：

> 允许产品建立宫位/星系的多维、类型化、带不确定性的 state representation，并把“宫吉/不吉、格局大/小”解释为 source-backed state 或 contextual projection；不允许引入 universal palace score。

---

## 2.2 结构状态与程度状态分离

### A. pattern_status

source 明确给出结构成立/破坏条件时，可使用：

~~~text
FORMED
BROKEN
UNFORMED
UNKNOWN
~~~

其中：

- FORMED：命中 source-defined 成格 template；
- BROKEN：命中 source-defined 破格条件；
- UNFORMED：明确不满足 source-defined 成格条件；
- UNKNOWN：资料不足以安全判断。

### B. pattern_integrity

“破格”只表示结构模式发生变化，不等于“效果归零”。

因此结构完整度与 pattern_status 分离。

PL2 v0.1 不批准任意 0–1 数值；只允许：

~~~yaml
integrity_direction:
  - preserved
  - degraded
  - transformed
  - unresolved
magnitude_status: UNIDENTIFIED
~~~

未来如经案例辨识形成连续 pattern_integrity，必须保留 provenance、置信区间/后验分布与 calibration version。

---

## 2.3 格局大小与格局完整度分离

pattern_scale 与 pattern_integrity 是不同变量。

允许的 source-preserving 状态：

~~~text
LARGE
NOT_LARGE
UNKNOWN
~~~

只有源文明确给出“大/不大”或已有 source-backed 上游规则能够推出时才赋值。

不得因为：

- 吉曜多；
- 百官成员多；
- 无煞；
- pattern formed；

就自动推出 LARGE。

同样，LARGE 不自动推出财富、婚姻、事业结果优良。

---

## 2.4 palace valence 改为 contextual projection

不建立：

~~~text
palace_valence = GOOD / BAD
~~~

作为全局基础事实。

改为：

~~~text
ContextualValence(
    palace,
    domain,
    target/question,
    active_states,
    evidence
)
~~~

最小返回结构：

~~~yaml
palace: Pxx
domain: resource | career | relationship | support | ...
target: source_preserving_target
direction_or_state: increase | decrease | favorable | unfavorable | mixed | unresolved
evidence_rule_ids: [...]
confidence: HIGH | MEDIUM | LOW | CONFLICTED | INSUFFICIENT_EVIDENCE
~~~

“吉/不吉”允许作为**语境化、高层语言压缩**存在，但必须能回溯到底层状态/规则证据。

---

## 2.5 typed state 不新造重复本体

本 Gate 不批准重新建立一套脱离现有 QI/QR / WP05 projection ontology 的“七维评分表”。

实现时优先复用已有：

- projection_domain；
- projection_target；
- direction_or_state；
- state expression / relational projection / cross-palace constraint 等模式。

如后续确需 aggregate state，必须由现有 source-backed primitives 组合得到，并记录 component evidence。

---

## 2.6 行为、扰动与现实应象边界

本 Gate 的输出属于结构/状态/投影，不属于现实宿命结果。

PL3 及后续动态层预留：

~~~text
x_(t+1) = f(x_t, z_t, a_t, w_t, history; theta)
~~~

其中：

- z_t：命盘/时层结构环境；
- x_t：当前估计状态；
- a_t：本人行为与选择；
- w_t：不可控外部扰动；
- history：既往路径与已实现状态；
- theta：待辨识参数。

因此 PL2 不得把“某宫偏吉”直接翻译为“现实事件一定发生”。

---

## 2.7 对 W01 Human Gate rows 的影响

涉及：

- W01-016
- W01-017
- W01-022
- W01-023
- W01-035

本 Gate 批准后，这五条从“理论对象不允许存在”转为“可以进入 constrained implementation review”。

**不得自动全部提升 EXECUTABLE。**

逐条仍需验证：

1. 所引用的 palace/domain state 是否已有 source-backed producer；
2. “格局大/不大”是否有可执行上游证据；
3. 相关 cross-palace projection 是否保持原文作用域；
4. 无法唯一判断时必须返回 UNKNOWN / INSUFFICIENT_EVIDENCE。

---

# 3. HG_PL2L_BAIGUAN_STRUCTURE

## 3.1 Human Gate 裁决

~~~yaml
gate_id: HG_PL2L_BAIGUAN_STRUCTURE
decision: APPROVE_STRUCTURE_DEFER_ACTIVATION_THRESHOLD
human_status: HUMAN_APPROVED
approved_at: 2026-10-05
~~~

本 Gate 批准：

> “百官朝拱”作为可复用 named structural family 的 ontology / evidence profile。

本 Gate **不批准**：

> 任意人为规定“出现 N 颗/ N 对百官星即算百官朝拱”的统一阈值。

---

## 3.2 v0.1 scope：先限定紫微 anchor

当前 W01-095 / 096 / 098 均围绕紫微财帛宫条件。

因此 v0.1 executable ontology 先限定：

~~~yaml
anchor_star: ZI_WEI
~~~

其他主星使用“百官朝拱”的情形，后续按各自 source span 单独扩展，不从紫微定义自动泛化。

---

## 3.3 BAIGUAN_SUPPORT_PROFILE

新增一等结构对象：

~~~text
BAIGUAN_SUPPORT_PROFILE
~~~

最小结构：

~~~yaml
structure_id: BAIGUAN_SUPPORT_PROFILE
anchor_star: ZI_WEI

components:
  orthodox_support: []
  assistant_support: []
  auxiliary_support: []
  minor_attendants: []

relations: []
quality_guards: []
conflicts: []

activation_status: UNKNOWN
evidence_rule_ids: []
source_spans: []
~~~

### source-backed component families

对紫微，现有中州派 source 支持以下成员/类别：

**正曜支持**
- 天府
- 天相

但必须继续检查其自身质量条件，不能只检测“出现”。

**辅佐支持**
- 左辅 / 右弼
- 天魁 / 天钺
- 文昌 / 文曲
- 禄存 / 天马

各组对紫微的作用并不相同，不得统一计数或统一赋权。

**杂曜朝拱成员**
- 三台 / 八座
- 恩光 / 天贵
- 台辅 / 封诰
- 龙池 / 凤阁
- 天福 / 天寿

**明确排除**
- 化禄
- 化权
- 化科

三化可以改善/改变相关状态，但 source 明确不把它们本身称为“朝拱”成员。

---

## 3.4 relation 必须 source-preserving

BAIGUAN_SUPPORT_PROFILE 只记录 source 已支持的 relation evidence，例如：

- 同度；
- 三方会合；
- 三方四正会合；
- 夹；

具体成员适用哪一种 relation，必须由对应 source rule 决定。

不得新增“百官成员只要出现在任意相关宫就算”的泛化 operator。

---

## 3.5 quality guards

百官结构不是“成员存在即可”。

例如 source 对紫微所会天府、天相另有质量要求：

- 天府需检查禄、空库等条件；
- 天相需检查财荫夹印、刑忌夹印、羊陀夹等性质。

因此 profile 必须保存：

~~~yaml
quality_guards:
  - component
  - guard_rule
  - status
  - evidence
~~~

不能把失效/变质 component 与正常 component 等价计入。

---

## 3.6 activation_status：允许 profile，不虚构 threshold

v0.1 使用：

~~~text
EXPLICIT_TEMPLATE_MATCH
PARTIAL_SUPPORT
CONFLICTED
ABSENT
UNKNOWN
~~~

含义：

- EXPLICIT_TEMPLATE_MATCH：命中已冻结的 source-explicit 百官 template；
- PARTIAL_SUPPORT：存在多个百官 component，但资料不足以宣告完整“百官朝拱”；
- CONFLICTED：支持 component 与明确失效/破坏条件并存；
- ABSENT：确认缺少相关支持；
- UNKNOWN：尚不能判断。

在 BAIGUAN_ACTIVATION_CRITERION 未完成前：

> 不允许通过成员数量、pair 数量、人工权重或 LLM 判断把 PARTIAL_SUPPORT 自动升级为 EXPLICIT_TEMPLATE_MATCH。

---

## 3.7 百官朝拱不等于固定“吉”

结构层只允许：

~~~text
BAIGUAN_SUPPORT_PROFILE
    ↓
typed state modifiers
    ↓
palace/context projection
~~~

不允许：

~~~text
BAIGUAN = GOOD
~~~

同一结构在不同宫位/场景可产生不同投影。

例如：

- 财帛宫紫微化权见百官，source 可投影为较易得他人财务支持；
- 紫微化科见百官，可增强凭名誉/商誉求财的语义；
- 交友宫若百官结构“过分完美”，source 又可出现下属权威过强、反客为主风险。

因此百官只是一种结构/支持配置，不能成为全局 valence。

---

## 3.8 对 W01 Human Gate rows 的影响

涉及：

- W01-095
- W01-096
- W01-098

本 Gate 批准后：

1. 可以实现 BAIGUAN_SUPPORT_PROFILE ontology 与 evidence extraction；
2. 可以实现 component-level source-preserving detector；
3. **暂不自动把三条 W01 提升 EXECUTABLE**。

三条仍等待：

~~~text
BAIGUAN_ACTIVATION_CRITERION_v0.1
~~~

冻结一个 source-backed 的 activation contract 后，才允许用于 runtime truth predicate。

---

# 4. 新增后续研究/工程工作单元

## 4.1 PRODUCT_PL2Q_HUMAN_GATE_INTEGRATION

目标：

- 将两个 Human Gate 决议变成 schema/runtime contracts；
- 不引入数值权重；
- 不提升尚缺 producer / activation criterion 的 W01 条目。

应交付：

- contextual valence/state contract；
- pattern status / scale / integrity contract；
- BAIGUAN_SUPPORT_PROFILE registry/schema；
- regression tests；
- blocker refresh。

## 4.2 KNOWLEDGE_BAIGUAN_ACTIVATION_REVIEW

目标：

- 全库搜集 source 明确使用“百官朝拱”的实例；
- 区分列举成员、局部支持、完整命名结构；
- 提取 relation、anchor、quality guard；
- 判断是否存在 source-backed 最小成立模板。

输出：

~~~text
BAIGUAN_ACTIVATION_CRITERION_v0.1
~~~

若 source 本身仍无统一 threshold，则允许最终结论为：

~~~text
NO_UNIVERSAL_THRESHOLD
~~~

此时 runtime 必须长期保留 template-specific detection，而不是发明统一计数阈值。

## 4.3 CALIBRATION / SYSTEM IDENTIFICATION（后续，不属于 PL2 Gate）

以后真实案例用于辨识：

- modifier magnitude；
- pattern degradation severity；
- contextual interaction strength；
- temporal persistence；
- manifestation routing probability。

这些参数不得反写污染 source fact layer，必须版本化、可回滚，并与 source-backed deterministic layer 分离。

---

# 5. Acceptance Criteria

两个 Gate 只有同时满足以下约束，才视为产品实现符合 Human Decision：

1. 不存在 universal palace numeric score；
2. 不存在“吉星 +N、煞星 -N”的人工权重表；
3. pattern formed/broken 与 pattern scale/integrity 分离；
4. “吉/不吉”只能作为 contextual projection 或 source-explicit state；
5. UNKNOWN / INSUFFICIENT_EVIDENCE 是合法且优先于猜测的结果；
6. 百官 profile 的 component、relation、guard 均可回溯 source；
7. 百官未冻结 activation criterion 前，不使用人工数量阈值；
8. 百官结构不自动等同于 GOOD；
9. W01-016/017/022/023/035 与 W01-095/096/098 不因 Human Gate 批准而自动升为 executable；
10. PL3 最终应象必须允许 action、external disturbance、history feedback 进入后续动态模型。

---

# 6. Decision Summary

| Gate | Human Decision | 允许 | 暂不允许 |
|---|---|---|---|
| HG_PL2N_PALACE_VALENCE_MODEL | **APPROVE_WITH_CONSTRAINTS** | typed state、pattern status、scale/integrity 分离、contextual valence | universal score、人工权重、直接宿命结果 |
| HG_PL2L_BAIGUAN_STRUCTURE | **APPROVE_STRUCTURE_DEFER_ACTIVATION_THRESHOLD** | BAIGUAN_SUPPORT_PROFILE、component evidence、quality guards | 人工“几颗即成格”阈值、百官=固定吉 |

Human Gate 已完成。

下一产品工作单元建议：

**PRODUCT_PL2Q_HUMAN_GATE_INTEGRATION**

> **历史审计文档 / NON-CANONICAL**：本文件保留用于追踪 A2 形成过程。当前唯一 Gate A2 人工审核入口为 `validation/decontamination/GATE_A2_CANONICAL.md`。不要从本文件单独推断当前批准状态或自动执行边界。

# Gate A2：时序记忆 / 获得性状态架构审计

状态：**READY FOR PI REVIEW**  
分支：audit/decontamination-p0-v2  
前置 Gate：A0 APPROVED；A1 APPROVED

## 1. 为什么触发 A2

Gate A1 规定：只有发现会改变 primitive、六十星系 mode 架构或 G5 核心状态结构的证据，才停止自动推进并升级人工 Gate。

LB-06 回源时出现 3 条 source-supported architecture triggers：

- ZZ-SYS-31-033：当前运限可使顽嚣/破坏性进一步固化，并影响后运；
- ZZ-SYS-38-034：前期形成的享受/短志结构，会在后续七杀阶段被检验或放大；
- ZZ-SYS-41-023：大起大落的时序经历可进一步强化怯懦本质。

已登记于 validation/decontamination/A2_architecture_hold_v0.1.csv。

它们不进入 quarantine，因为源文依据成立；也暂不进入 ordinary effective split plan，因为当前 G5 无法忠实执行这种跨期记忆。

## 2. 这不是孤例

此前 source-reviewed 规则也出现同类结构：

- ZZ-SYS-30-033：某阶段若使原有积极性质发生改变，会影响后运；
- ZZ-SYS-31-020：某一关键运限能否被利用，会成为后续发展的分水岭。

因此重复出现的机制是：

~~~text
当前运限
  -> 当期反应
  -> 形成 / 强化 / 固化后天中间状态
  -> 改变后续运限的反应
~~~

## 3. 当前 G5 的不足

当前主模型近似：

~~~text
E = fixed natal essence
u_t = current temporal input
r_t = R(E, u_t, z_t, G_t, c_t)
y_t = P(r_t, c_t)
~~~

E 固定仍然正确。

问题是：若源文明确说某阶段会形成、强化或固化后天状态并影响后运，只依靠 R(E,current_input) 无法表示“同一原局 + 同一当前输入 + 不同过去经历”所产生的不同反应。

如果把后天变化写回 E，又会破坏“原局本质固定”。

因此需要第三个对象：

**获得性 / 历史状态（acquired history state）m_t**

## 4. A2 最小修订提案

保留固定原局：

~~~text
E_p = fixed natal essence
~~~

新增：

~~~text
m_(p,t) = acquired / history state
~~~

当前反应：

~~~text
r_(p,t) = R(
    E_p,
    m_(p,t),
    u_(p,t),
    z_(p,t),
    neighborhood(E,G_0),
    c_t
)
~~~

只有源文明确支持“形成、强化、固化、影响后运、前期经历改变后续反应”等结构时，才允许：

~~~text
m_(p,t+1) = M(
    m_(p,t),
    r_(p,t),
    u_(p,t);
    g_source
)
~~~

其中 g_source 是 source-grounded update gate。

## 5. 这不是自由递归模型

A2 不批准：

~~~text
x_(t+1) = arbitrary F_theta(x_t,u_t)
~~~

也不允许：

- 任意连续衰减系数；
- 任意学习率或记忆权重；
- 默认所有运限自动累积；
- 用神经网络自由学习“性格漂移”并称为中州派原理。

Paper 1 只允许：

~~~text
SOURCE_EXPLICIT_PERSISTENCE
=> history-state update allowed
~~~

否则 history state 不更新。

数值递归动力学、连续 transition matrix、observer、system identification 继续属于后续研究。

## 6. E 与 m 必须严格分开

E：原局本质
- 由本命结构建立；
- 不被运限重写；
- 表示 natal baseline。

m_t：获得性历史状态
- 由明确时序规则产生；
- 可以为空；
- 可以被强化、削弱、形成或转化；
- 不反向改变出生盘结构；
- 只影响后续 reaction。

因此：

~~~text
natal essence != acquired disposition
~~~

A2 不是推翻 G5，而是填补“原局固定”与“后运受前运影响”之间缺失的一层。

## 7. m_t 不一定等于 primitive qi

获得性状态可指向：

1. 已有 QI/QR 的历史偏移，例如 QI-16、QI-08、QI-04；
2. provisional candidate，例如 QI-17-CAND、QI-18-CAND；
3. system-mode / disposition memory，例如顽嚣、怯懦、浮荡等中尺度状态。

第三类不得为了方便全部升格 primitive。

## 8. 推荐数据对象

~~~yaml
history_update:
  update_id: HU-0001
  source_rule_id: ZZ-SYS-31-033
  scope: palace | system | dimension
  target:
    type: qi_state | relational_state | system_mode | derived_state
    id: ...
  trigger: ...
  direction: reinforce | weaken | form | transform
  persistence_scope: later_periods
  source_epistemic: EXPLICIT
  normalization_epistemic: INFERRED | IMPLEMENTATION
  review_status: SOURCE_SPAN_VERIFIED
~~~

禁止默认 persistence_scope = forever。

源文未给出持续期限时标记 UNRESOLVED，不擅自数值化。

## 9. G5-R 建议结构

若 A2 批准，G5 从：

~~~text
fixed natal essence
+ current temporal input
-> reaction
~~~

修订为：

~~~text
fixed natal essence E
+ acquired/history state m_t
+ current temporal input u_t
+ current mode z_t
-> reaction r_t
-> semantic projection y_t

source-explicit persistence gate
-> optional update of m_(t+1)
~~~

仍保留十二宫局部节点+稀疏图、natal/temporal 分离、astro/human/disturbance input 分离、qi->mode->projection、无预测有效性声明、无任意连续权重。

## 10. 与原 G5 递归 HYPOTHESIS 的关系

原 G5 已预留一般递归 x_(t+1)=F_theta(...)，但整体列为未来 HYPOTHESIS。

A2 建议拆为：

### Paper 1：SOURCE-GATED SYMBOLIC MEMORY

~~~text
m_(t+1) = M_source_gated(...)
~~~

只承载文本明确存在的路径依赖。

### Paper 2+：LEARNED GENERAL DYNAMICS

~~~text
x_(t+1) = F_theta(...)
~~~

由纵向案例与系统辨识决定是否成立及如何参数化。

## 11. 全量 history-marker 预扫描

为了判断 A2 是否只是 3 条偶然规则，我先对六十星系 2193 条 canonical 做了不改模型的 deterministic marker scan：

- heuristic candidates：45
- P0_HISTORY_REVIEW：27
- P1_SEQUENCE_REVIEW：18

文件：

`validation/decontamination/A2_history_marker_candidates_v0.1.csv`

扫描器：

`src/audit_history_markers.py`

注意：

> 45 只是“待回源候选”，不是 45 条已确认 HistoryUpdate。

其中 P1_SEQUENCE_REVIEW 包含大量“先挫后成、先败后兴”等单纯结果顺序，未必代表状态记忆；只有 source-span review 确认“前一阶段形成/强化状态并改变后续反应”时，才能转成 history update。

当前已确认的 3 条 A2 trigger 仍是：

- `ZZ-SYS-31-033`
- `ZZ-SYS-38-034`
- `ZZ-SYS-41-023`

另外，预扫描也命中了多个非常值得 A2 批准后优先回查的高优先候选，例如：

- `ZZ-SYS-21-017`：错误路向可能固化并影响后运；
- `ZZ-SYS-29-024`：因循固化并影响后运；
- `ZZ-SYS-32-014`：挫折可形成不求上进并影响后运；
- `ZZ-SYS-38-021`：关键运中退缩可使短志固化并影响后运；
- `ZZ-SYS-54-021`：当前行为影响后运。

这进一步说明 A2 的问题很可能是系统性的，但在人工批准前仍不把它们写入递归模型。

## 12. 当前 3 条 hold 的处理

A2 批准前：

- ZZ-SYS-31-033
- ZZ-SYS-38-034
- ZZ-SYS-41-023

保持 A2_ARCHITECTURE_HOLD，不进入普通 inference。

A2 批准后：

1. 建立 history-update schema；
2. 将三条转为第一批 HistoryUpdate；
3. 回查此前已 review 的 path-dependence rules；
4. 对六十星系 2193 条做 history-marker backward audit；
5. 只为 source-confirmed candidates 建立 history update；
6. 更新 G5 model spec 与 regression tests。

## 13. 风险分析

不加 m_t：会丢掉源文明确的“前运改变后运反应条件”。

直接修改 E：会混淆出生原局与后天形成状态。

直接启用一般递归 x_t：会给模型过大的自由度，重新制造 AI 自创动力学风险。

因此最小 source-constrained m_t 是当前最保守的修订。

## 14. Gate A2 需要 PI 审核的 5 项

### A2-1
批准新增独立于原局本质 E 的 acquired_history_state m_t。

### A2-2
批准只有 source-explicit persistence/path-dependence rule 才能更新 m_t。

### A2-3
批准 Paper 1 只实现 symbolic / ordinal history update，不引入任意连续记忆权重、衰减率或学习参数。

### A2-4
批准原 G5 一般递归 x_(t+1)=F_theta(...) 继续作为 Paper 2+ hypothesis；Paper 1 的 m_t 不代表已证明一般递归动力学成立。

### A2-5
批准对六十星系全文追加 history-marker backward audit，并把当前三条 held rules 转为第一批 HistoryUpdate 模板。

## 15. A2 批准后的自动路线

~~~text
A2 approval
-> D-016
-> HISTORY_UPDATE_SCHEMA v0.1
-> G5-R state-space v0.5
-> model_spec acquired-history objects
-> migrate 3 held rules
-> backward scan all 2193 systems
-> source-review persistence candidates
-> ontology / system-mode regression
-> resume LB-07 ... LB-16
~~~

只有 history state 需要新增 primitive、六十星系 mode 架构必须改变、或 palace graph / natal-temporal separation 被源文推翻时，再升级下一人工 Gate。

# Gate A2：路径依赖 / 获得性状态与 G5 非递归架构修订

状态：**READY FOR PI REVIEW**  
前置 Gate：A0 / A1 APPROVED  
触发来源：LB-05 + LB-06 全文 source-span review

## 1. 为什么触发 A2

G5 当前冻结的 Paper-1 主模型是：

~~~text
fixed natal essence E
+ temporal exogenous input U_t
-> state-dependent reaction R_t
-> projection Y_t
~~~

即：

~~~text
R_t = React(E, U_t, Z_t, G_t, C_t)
~~~

并把真正递归状态：

~~~text
x_(t+1) = F(x_t, ...)
~~~

留到未来研究。

这隐含：后天某一运限产生当期反应，但不会改变下一期反应所依赖的内部状态基底；下一期仍主要由固定原局 E 与当期输入决定。

LB-05 / LB-06 source review 已出现一组无法安全压回“当期投影”的明确反例。

## 2. 已确认的路径依赖证据簇

### ZZ-SYS-30-033
积极太阳在特定武曲运可出现情绪动荡、进退失据；若因此改变原本积极本质、转向迁就命运，后运也受影响。

### ZZ-SYS-31-020
天机化忌对顽嚣破军可能反而成为可利用阶段；能否利用此运势，被原文描述为今后运程发展的关键。

### ZZ-SYS-31-033
不良太阳环境可使顽嚣破军的破坏性逐渐形成、根深蒂固并影响后运。这是当前最强的 acquired-state 证据之一。

### ZZ-SYS-38-034
天同辰戌的材料把早期享受/短志结构与后来七杀阶段的承载能力连接起来，说明过去阶段形成的意志/持续性结构会改变后期反应。

### ZZ-SYS-41-023
紫贪火铃/化忌导致的暴起暴跌，可以进一步加深怯懦天府的怯懦本质。

共同结构是：

~~~text
past temporal history
-> acquired internal change
-> later response changes
~~~

## 3. G5 的固定原局本质仍应保留

A2 不建议推翻：

~~~text
E = natal essence
~~~

原局本质仍应固定。

问题在于模型缺少第二状态层：

~~~text
E   固定原局本质
A_t 后天获得性 / 历史依赖状态
~~~

源文支持的是：后天经历不能重写出生原局，但可以使某些倾向被强化、削弱、固化，进而改变以后面对同类运限时的反应。

因此：

~~~text
natal essence != acquired state
~~~

## 4. 三种处理方案

### 方案 A：继续完全 memoryless
仍用 R_t = R(E,U_t,...)，把“影响后运”“根深蒂固”等仅做历史语义备注。

优点：最简单，G5 不变。  
缺点：主动丢失源文明确的跨期机制，后续会不断积累例外。

**不建议。**

### 方案 B：增加 history/context H_t，但不承认它是状态
形式：

~~~text
R_t = R(E, U_t, H_t, ...)
~~~

H_t 总结过往经历。

优点：改动较小。  
缺点：如果 H_t 会由过去反应更新，它事实上就是 state memory，只是换了名字。

**不建议作为最终形式。**

### 方案 C：增加获得性慢状态 A_t，并采用稀疏、符号、源文门控递归

建议：

~~~text
E = fixed natal essence

A_t = acquired / history-dependent state

R_t = React(
    E,
    A_t,
    U_t,
    Z_t,
    G_t,
    C_t
)

A_(t+1) = Update_A(
    A_t,
    R_t,
    U_t
)
~~~

但 Update_A 严格限制为：

1. 源文明确出现跨期影响时才更新；
2. 只做 symbolic / ordinal update；
3. 必须有 provenance；
4. 不允许 AI 自行假设“所有事件都会塑造人格”；
5. 不允许 A_t 覆盖或修改 natal essence E；
6. 无 transition rule 时 A_(t+1)=A_t。

这是一种 source-gated sparse state transition，而不是完整数值动力学。

**A2 推荐方案 C。**

## 5. 状态分解

~~~text
Fixed natal substrate:
E

Acquired slow state:
A_t

Current reaction:
R_t
~~~

E 包括原局星系本质、原局宫位结构、出生盘固定关系，永远不被运限重写。

A_t 仅记录源文明示的长期强化/削弱，例如：

- 顽嚣倾向被长期固化；
- 怯懦倾向被强化；
- 短志/持续性结构在前一阶段形成；
- 积极性受到长期削弱；
- 某些模式经过后天经历发生长期转向。

R_t 则保留当期快速反应：情绪扰动、行动激活、决策变化、关系压力、mode activation。

## 6. Paper-1 建议形式

~~~text
E = BuildNatalEssence(chart_0)

A_0 = neutral / source-defined acquired baseline

R_t = React_theta(
    E,
    A_t,
    U_t,
    Z_t,
    G_t,
    C_t
)

Y_t = Project_phi(
    R_t,
    palace_graph,
    C_t
)
~~~

只在存在明确 transition rule 时：

~~~text
A_(t+1) = T_k(A_t, R_t)
~~~

否则：

~~~text
A_(t+1) = A_t
~~~

T_k 是 source-backed symbolic transition operator，不使用任意连续系数。

## 7. 对控制理论建模的意义

如果系统完全是 Y_t=f(E,U_t)，它更像 static nonlinear / conditional response model。

出现 A_(t+1)=T(A_t,R_t) 后，才真正出现“当前内部状态受过去历史影响并参与未来输出”的动态状态含义。

但 Paper 1 仍不声称：

- 已建立真实物理动力学；
- 已完成系统辨识；
- 已有连续 A matrix；
- 可运行 Kalman filter；
- 可计算经典 controllability。

它更准确地属于 symbolic hybrid / event-triggered state transition layer。

## 8. 与 QI-17 / QI-18 的关系

QI-17-CAND = 意志控制强度。  
QI-18-CAND = 毅力 / 持续性。

它们回答“状态是什么”。

A_t 回答“这些状态是否因历史经历而发生长期改变”。

因此不能写成 A_t = QI-17，而应允许：

~~~text
A_t[QI-17]
A_t[QI-18]
A_t[QI-08]
...
~~~

只对存在 source transition evidence 的维度启用。

## 9. 建议新增 schema

建议增加：

~~~text
transition_scope:
  CURRENT_ONLY
  ACQUIRED_STATE_UPDATE
  PATH_DEPENDENT_GATE

persistence_horizon:
  current_period
  later_periods
  unspecified_long_term
~~~

用于区分当期反应、长期强化、历史门控。

## 10. LB-06 当前处理

LB-06 共 50 条：

- 47 条已完成 source / normalization review，并形成 split plan；
- 3 条因触及 acquired-state architecture 被置于 ARCHITECTURE_HOLD_A2：

  - ZZ-SYS-31-033
  - ZZ-SYS-38-034
  - ZZ-SYS-41-023

它们已加入 knowledge/review/architecture_hold_v0.1.csv。

rule engine 已支持 architecture hold：在 A2 决策前默认不进入 effective executable view。

## 11. Gate A2 需要 PI 审核的 4 项

### A2-1
批准固定原局本质 E 继续永久冻结，不因运限重写。

### A2-2
批准新增 A_t：后天获得性 / 历史依赖慢状态层。只有原文明示跨期影响时才允许更新。

### A2-3
批准 Paper-1 出现有限递归：

~~~text
A_(t+1) = source-gated symbolic transition
~~~

但不使用任意连续参数、不做系统辨识、不把所有规则递归化，默认 A_(t+1)=A_t。

### A2-4
批准把原 G5：

“递归动力学只作为未来 HYPOTHESIS”

修订为：

“**一般连续递归动力学仍属未来 HYPOTHESIS；但源文明示的离散/符号型 acquired-state transition 纳入 Paper-1 正式结构。**”

## 12. A2 批准后自动执行

~~~text
A2 approval
-> DECISION_LOG D-016
-> theory/state_space_model v0.5
-> src/model_spec.py add AcquiredState / TransitionRule
-> transition_scope schema
-> convert held 3 rules into acquired-state transitions
-> backward scan all 2193 system rules for:
     影响后运
     根深蒂固
     养成
     形成
     转变本质
     后运受影响
     以后
     日久
     加深/加强原有本质
-> build path-dependence catalog
-> rerun G5 regression
-> resume LB-07 ... LB-16
~~~

只有全文反扫进一步显示 acquired state 会重写 natal essence、多宫长期状态传播，或需要第二时间尺度以上结构时，才触发 A3。

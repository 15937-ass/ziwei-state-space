# State-Space Model — Draft 0.2（G5 候选）

## 1. 目标

把中州派“原局本质 -> 运限刺激 -> 反应 -> 宫位应象”的推断逻辑，形式化成一个可执行、可审计、可为后续系统辨识提供接口的潜状态模型。

本版本刻意区分：

1. **源文直接支持的核心反应结构**；
2. **为了后续控制/系统辨识而增加的动力学扩展假设**。

两者不得混写。

---

## 2. 状态不是单一扁平向量

G2-G4 已经冻结的层次为：

~~~text
L0 结构底座：阴阳、五行、星系/宫位图结构
L1 内在气机：QI-01 ... QI-15（候选可修订）
L2 关系网络：QR-01 ... QR-04
L3 场景投影：十二宫语义域与可观察结果
L4 评价层：吉凶、适配、中和、风险
~~~

因此整体状态使用**层级图状态（hierarchical graph state）**，而不是把所有变量硬塞进一个同质向量。

---

## 3. 十二宫状态组织：采用“局部节点 + 全局堆叠”

### 3.1 固定原局基态

对十二宫每个节点 p 定义：

~~~text
e_p = E_p(H_p^natal, G_0)
~~~

其中：

- H_p^natal：该宫及其关联星系经过单星气核、星系交互、修正曜作用后的原局中尺度状态；
- G_0：原局结构图，包括本宫、三方、对宫及文本明确要求的跨宫边；
- e_p：该宫的**原局本质（natal essence）**。

将十二宫堆叠：

~~~text
E = [e_1, e_2, ..., e_12]
~~~

E 在 Paper 1 中视为原局固定基态，不随流年被重写。

### 3.2 为什么不采用“一个全局状态 + 十二个纯输出头”

下册宫垣论要求先分别认识原局十二宫的本质，而且同一星系处于不同宫垣，其现实语义不同。

因此只用一个 global x 再投影到十二宫，会丢失：

- 每个宫独立的原局结构；
- 宫间关系；
- 宫位迁移后“对某个既有本质发生反应”的机制。

所以采用十二宫局部节点，再将其堆叠为全局系统状态。

### 3.3 为什么也不把十二宫当作完全独立系统

原文明确要求：
- 三方四正；
- 命—财—官等联动；
- 兄弟—交友关系；
- 福德思想影响事业等跨宫作用。

因此使用稀疏图：

~~~text
G = (V, E_graph)
V = 12 palaces
~~~

边来源只允许：
1. 固定三方四正；
2. 源文明确跨宫依赖；
3. 后续经验数据支持的新边（Paper 2 以后）。

---

## 4. 源文最忠实的“反应模型”

中州派下册最关键的原则不是“前一年的状态递推到下一年”，而是：

> 先确定原局宫垣本质，再把大限/流年移动后的星曜结构视为对该本质的反应。

因此 Paper 1 的**核心模型**先写成非递归条件反应：

~~~text
u_(p,t) = U_p(chart_t, transformations_t, modifiers_t, G_t)

r_(p,t) = R_theta(
    e_p,
    u_(p,t),
    z_(p,t),
    neighborhood(E, G_0),
    c_t
)

y_(p,t) = P_p(r_(p,t), c_t)
~~~

其中：

- e_p：原局本质；
- u_(p,t)：大限/流年等外生时序输入；
- z_(p,t)：当期星系模态；
- c_t：现实上下文，如年龄、职业、婚姻状态、社会背景；
- r_(p,t)：当期反应状态；
- y_(p,t)：宫位输出/可观察应象。

最关键性质：

~~~text
R(e_a, u) != R(e_b, u)
~~~

即相同运限输入作用于不同原局本质，会产生不同反应。

---

## 5. 动力学扩展：标记为 HYPOTHESIS

如果未来纵向命例数据表明“前一期现实状态会影响下一期状态”，可加入真正递归动力学：

~~~text
x_(t+1) = F_theta(
    x_t,
    E,
    u_t,
    z_t,
    G_t,
    c_t
) + w_t
~~~

观察：

~~~text
y_t = H_phi(x_t, E, z_t, c_t) + v_t
~~~

其中：
- x_t：可学习的时变潜状态；
- E：固定原局基态；
- w_t：未建模扰动；
- v_t：观察噪声。

**这一递归结构不是当前中州文本直接给出的定律，而是为了系统辨识建立的研究假设。**

Paper 1 可以定义接口，但不得把它写成已被传统文本或数据证明的事实。

---

## 6. 星系模态与混杂系统

G4 已批准：

~~~text
h_s = A_s(S) + Delta_s(S, R_s, c)
z_s = M_s(h_s, c)
~~~

因此当 z_s 影响状态响应函数时，模型与混杂/切换系统兼容：

~~~text
r_t = R_(z_t)(E, u_t, G_t, c_t)
~~~

未来递归版本可写：

~~~text
x_(t+1) = F_(z_t)(x_t, E, u_t, G_t; theta)
~~~

但 Paper 1 不估计：
- 模态转移概率；
- 数值阈值；
- 模态停留时间。

---

## 7. 修正算子

修正曜统一为：

~~~text
T_m(state, mode, context)
~~~

支持：

- enhance；
- weaken；
- transform；
- gate；
- couple。

四化必须写成：

~~~text
T_(star, hua)
~~~

而不是统一的：

~~~text
T_hua
~~~

因为同一化曜作用于不同星曜，其目标维度和副作用不同。

多修正曜并存：

~~~text
T_total = Compose(T_m1, T_m2, ...)
~~~

暂不假设算子交换，也不做简单正负抵消。

---

## 8. 外生输入、控制输入与扰动必须分开

### 8.1 外生时序输入

~~~text
u_t^astro
~~~

包括：
- 大限；
- 流年；
- 流月（未来扩展）；
- 当期四化；
- 当期星系/宫位结构。

这些不是人可以控制的，因此不能叫 control input。

### 8.2 人的行为输入

未来若研究“趋吉避凶”：

~~~text
u_t^human
~~~

可能包括：
- 是否投资；
- 是否迁移；
- 是否合作；
- 是否就医；
- 是否学习/考试；
- 是否转换职业等。

只有具有干预/因果数据时，才讨论真正的 controllability 或 optimal control。

### 8.3 外部扰动

~~~text
d_t
~~~

包括：
- 宏观经济；
- 家庭事件；
- 公司政策；
- 社会环境；
- 随机事故等。

最终动态扩展可写：

~~~text
x_(t+1) = F(x_t, E, u_t^astro, u_t^human, d_t, z_t, G_t)
~~~

Paper 1 只明确变量位置，不做因果最优控制。

---

## 9. 输出模型：气 -> 象 -> 事

禁止：

~~~text
star -> event
~~~

采用：

~~~text
symbolic structure
    -> latent state
    -> star-system mode
    -> palace projection
    -> contextual manifestation
    -> observable event
~~~

形式化：

~~~text
q/z -> P_p -> semantic outcome class -> Y
~~~

未来概率模型：

~~~text
P(Y | q, z, palace, C_person)
~~~

Paper 1 不估计真实事件概率。

---

## 10. G5 对 QI-16 / QI-17 的处理建议

G4 新发现：

- QI-16-CAND：目标导向性；
- QI-17-CAND：持续意志/韧性。

当前建议：

### QI-16 目标导向性
暂不升格。

原因：
- 与 QI-04 守成—开创、QI-08 行动驱动高度相关；
- 目前可作为星系模态层的派生变量表示：
  ~~~text
  goal_directedness = f(QI-04, QI-08, z_s)
  ~~~
- 若后续事件/规则显示它有独立可观路径，再升格。

### QI-17 持续意志/韧性
暂不升格，但优先级高于 QI-16。

原因：
- 与“行动驱动”不同：可以行动强，但不能持续；
- 与“决策激活度”不同：可以决断快，但缺乏抗挫持续性；
- 多个星系反复出现“意志坚强/薄弱、坚忍/躁进、刚毅/脆弱”。

建议作为：
~~~text
derived_state_candidate
~~~

进入观察性审计；等有更完整规则支持后决定是否加入正式 L1。

---

## 11. Paper 1 最终状态架构

建议冻结为：

~~~text
Static natal structure:
    L0 structural substrate
    -> star cores S_i^0
    -> star-system states h_s
    -> palace natal essences E = {e_p}

Temporal layer:
    u_t^astro
    + modifier operators
    + current modes z_t
    + graph G_t

Reaction:
    r_t = R_theta(E, u_t^astro, z_t, G_t, c_t)

Projection:
    y_t = P(r_t, palace graph, c_t)

Optional future dynamic extension:
    x_(t+1) = F_theta(x_t, E, u_t, z_t, G_t, c_t)
~~~

这个架构既保留中州派“原局本质—后天反应”的核心逻辑，又为后续系统辨识、观察器和控制理论保留接口。

---

## 12. 当前不做的事情

Paper 1 不做：

- 任意给定连续权重；
- 拟合真实命例参数；
- 宣称 predictive validity；
- 计算数值可控性矩阵；
- 设计最优趋吉避凶控制器；
- 用 Kalman filter 对真实人生状态做定量估计；
- 声称“气”是物理能量。

这些留给后续论文。

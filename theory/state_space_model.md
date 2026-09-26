# State-Space Model — v0.4（G5 核心架构 + Gate A1 术语/本体修订）

## 1. 目标

把中州派“原局本质 -> 运限刺激 -> 反应 -> 宫位应象”的推断逻辑，形式化成一个可执行、可审计、并可为后续系统辨识提供接口的层级潜状态模型。

本版本严格区分：

1. **文本直接支持的结构**；
2. **由本项目提出的形式化映射**；
3. **为后续控制/系统辨识预留的动力学扩展假设**。

三者不得混写。

---

## 2. Paper 1 已冻结的结构层次

~~~text
L0 结构底座：阴阳、五行、星系/宫位图结构
L1 内在气机：QI-01 ... QI-16（QI-17/18 仍为候选）
L2 关系网络：QR-01 ... QR-04
L3 场景投影：十二宫语义域与可观察结果
L4 评价层：吉凶、适配、中和、风险
~~~

因此整体模型采用**层级图状态（hierarchical graph state）**，而不是把所有变量硬塞进一个同质欧氏向量。

---

## 3. 原局：十二宫局部本质 + 全局图

对十二宫每个宫位节点 p 定义：

~~~text
e_p = E_p(H_p^natal, G_0)
~~~

其中：

- `H_p^natal`：该宫经单星气核、星系交互、辅佐煞化算子处理后的原局中尺度状态；
- `G_0`：原局结构图，包括三方四正与源文明确要求的跨宫关系；
- `e_p`：第 p 宫的**原局本质（natal essence）**。

十二宫堆叠：

~~~text
E = {e_1, ..., e_12}
~~~

Paper 1 将 `E` 视为固定原局基态，不因流年而被重写。

### 为什么不用“一个全局状态 + 十二个纯输出头”

因为中州派要求先分别认识十二宫原局本质，再把大限、流年移动后的宫垣星曜作为对既有本质的反应。只使用一个全局 x 会丢失每宫独立的原局结构与迁宫反应对象。

### 为什么也不能把十二宫当作十二个独立系统

因为：
- 三方四正；
- 命、财、官等联动；
- 兄弟、交友关系；
- 福德思想影响事业；
- 其他源文明确跨宫依赖；

都要求使用稀疏图：

~~~text
G = (V, E_graph)
V = 12 palaces
~~~

边只允许来自：
1. 固定斗数结构；
2. 源文明确的跨宫依赖；
3. Paper 2 以后由数据支持的新边。

---

## 4. 单星、星系与修正算子接口

### 4.1 单星基态

~~~text
S_i^0
~~~

### 4.2 条件单星状态

~~~text
S_i(c) = T_c(S_i^0)
~~~

### 4.3 六十星系状态

~~~text
h_s = A_s(S) + Delta_s(S, R_s, c)
z_s = M_s(h_s, c)
~~~

其中：
- `A_s`：现有单星气核可解释部分；
- `Delta_s`：交互残差；
- `z_s`：星系模态；
- `R_s`：同度、对宫、三合等结构。

### 4.4 辅佐煞化算子

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

而不是统一 `T_hua`。

多曜并存：

~~~text
T_total = Compose(T_m1, T_m2, ...)
~~~

Paper 1 不假设算子交换，也不做简单正负抵消。

---

## 5. 核心反应模型：优先采用非递归条件反应

中州派下册的核心并不是“上一年状态递推到下一年”，而是：

> 先认识原局宫垣本质，再把移动后的大限、流年星曜性质视为对该本质的反应。

因此 Paper 1 的**主模型**采用：

~~~text
u_(p,t) = U_p(
    chart_t,
    transformations_t,
    modifiers_t,
    G_t
)

r_(p,t) = R_theta(
    e_p,
    u_(p,t),
    z_(p,t),
    neighborhood(E, G_0),
    c_t
)

y_(p,t) = P_p(
    r_(p,t),
    c_t
)
~~~

其中：

- `e_p`：原局本质；
- `u_(p,t)`：大限/流年等外生时序输入；
- `z_(p,t)`：当期星系模态；
- `c_t`：年龄、职业、婚姻状态、社会背景等现实上下文；
- `r_(p,t)`：当期反应状态；
- `y_(p,t)`：宫位输出/传统应象或后续可观察变量。

核心非线性条件：

~~~text
R(e_a, u) != R(e_b, u)
~~~

即相同运限输入作用于不同原局本质，可产生不同反应。

---

## 6. “气 -> 象 -> 事”的输出链

禁止：

~~~text
star -> event
~~~

采用：

~~~text
symbolic structure
    -> latent qi state
    -> star-system mode
    -> palace reaction
    -> palace/context projection
    -> semantic outcome class
    -> observable event
~~~

形式化：

~~~text
(q, z, e, r) -> P_p -> Y_semantic -> Y_observed
~~~

未来概率版本：

~~~text
P(Y | r, z, palace, C_person)
~~~

Paper 1 只定义接口，不估计真实事件概率。

---

## 7. 外生输入、人的控制输入与外部扰动分开

### 7.1 外生时序输入

~~~text
u_t^astro
~~~

包括：
- 大限；
- 流年；
- 流月（未来扩展）；
- 当期四化；
- 当期星系/宫位结构。

这些不是人的 control input。

### 7.2 人的行为输入

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
- 是否转换职业。

只有具备干预/因果数据时，才讨论真正 controllability 或 optimal control。

### 7.3 外部扰动

~~~text
d_t
~~~

包括：
- 宏观经济；
- 家庭事件；
- 公司政策；
- 社会环境；
- 随机事故。

---

## 8. 递归动力学扩展：明确标记为 HYPOTHESIS

若未来纵向命例显示“前一期现实状态会影响下一期状态”，可以加入：

~~~text
x_(t+1) = F_theta(
    x_t,
    E,
    u_t^astro,
    u_t^human,
    d_t,
    z_t,
    G_t,
    c_t
) + w_t
~~~

观察：

~~~text
y_t = H_phi(
    x_t,
    E,
    z_t,
    palace_graph,
    c_t
) + v_t
~~~

其中：
- `x_t`：可学习时变潜状态；
- `E`：固定原局基态；
- `w_t`：未建模扰动；
- `v_t`：观察噪声。

这不是中州文本直接给出的定律，只是后续系统辨识假设。

---

## 9. 混杂/多模态接口

G4 已批准：

~~~text
h_s = A_s(S) + Delta_s(...)
z_s = M_s(h_s,c)
~~~

因此若 `z_s` 参与反应函数，系统与混杂/切换动力学兼容：

~~~text
r_t = R_(z_t)(E,u_t,G_t,c_t)
~~~

未来递归版本：

~~~text
x_(t+1) = F_(z_t)(x_t,E,u_t,G_t;theta)
~~~

Paper 1 不估计：
- 模态转移概率；
- 数值阈值；
- 模态停留时间。

---

## 10. 状态组织的最终选择

G5 建议采用：

### 10.1 原局层

~~~text
E = {e_p}_{p=1}^{12}
~~~

每个 `e_p` 是局部宫位本质。

### 10.2 当期反应层

~~~text
R_t = {r_(p,t)}_{p=1}^{12}
~~~

每个 `r_(p,t)` 是原局本质在时序输入下的反应。

### 10.3 星系模态层

~~~text
Z_t = {z_(s,t)}
~~~

### 10.4 图结构

~~~text
G_t = G_0 + G_temporal(t)
~~~

但 Paper 1 只允许：
- `G_0`：固定原局结构；
- `G_temporal`：由明确时序迁宫/星系关系确定的边。

不允许无依据全连接。

---

## 11. Observation-path support：只做观测通路支持审计

Gate A1 明确修正术语：

> 当前模型没有建立经典控制理论意义上足以判定 structural observability 的状态—输出结构条件。

因此 Paper 1 不再把“独立观测路径数量”称为 structural observability，而称为：

`ObservationPathSupport`

### 11.1 通路定义

对每个候选状态 `q_i`，检查是否存在：

~~~text
q_i
 -> star/star-system state
 -> palace reaction
 -> palace/context projection
 -> semantic/output class
~~~

仅用于回答：

- 当前形式化语料中是否存在直接输出通路；
- 是否只有单一路径；
- 是否存在多条相对独立路径；
- 是否只是由其他状态派生。

建议分类：

~~~text
MULTI_PATH_SUPPORTED
SINGLE_PATH_SUPPORTED
NO_DIRECT_PATH
DERIVED_ONLY
~~~

### 11.2 这不等于经典结构能观性

不得由上述分类推出：

- observability matrix 满秩；
- generic rank 条件成立；
- graph matching 条件成立；
- 潜状态可由有限观测唯一重构。

只有后续真正建立明确的状态—输出结构图、输出映射和相应 generic-rank / matching 条件后，才恢复使用 `structural observability` 一词。

### 11.3 冗余/可区分性仍需检查

A1 后继续重点检查：

- QI-01 发射—收敛 vs QI-14 信息/状态遮蔽—显露；
- QI-03 稳定—变动 vs QI-04 守成—开创；
- QI-02 刚—柔 vs QI-15 缓冲/调和；
- QI-08 行动驱动 vs QI-06 决策激活；
- QI-04/QI-08 vs QI-16 目标导向性；
- QI-17-CAND 意志控制 vs QI-18-CAND 毅力/持续性；
- QR-01 关系整合—孤离 vs QR-04 支持资源。

---

## 12. Structural Identifiability：第一篇只做参数角色审计

Paper 1 不拟合连续参数，但必须标记哪些参数以后可能无法同时辨识。

参数分三类：

### theta_fixed
完全由规则确定：
- 排盘结构；
- 宫位关系；
- 年干四化规则；
- 六十星系身份；
- 原局/运限层级关系。

### theta_prior
由文本提供方向/序约束：
- `alpha > 0`；
- `alpha_A > alpha_B`；
- 单调/非单调关系；
- 条件门控关系。

### theta_learned
未来由命例数据估计：
- 修正增益；
- 交互强度；
- 星系模态阈值；
- 宫位投影权重；
- 事件概率映射。

若两个 `theta_learned` 永远以乘积或同一组合出现而无独立观测，则标记：
~~~text
POTENTIALLY_NON_IDENTIFIABLE
~~~

Paper 2 再做正式系统辨识。

---

## 13. Gate A1 后的 QI-16 / QI-17 / QI-18 状态

### QI-16：目标导向性

Gate A1 已批准正式升格为 L1：

~~~text
QI-16 = goal-directedness
~~~

定义为：

> 行动、变化与资源投入具有明确目标、方向与建设性组织的程度。

它与 QI-03 / QI-04 / QI-08 分开，因为：

~~~text
变化多 != 目标明确
开创强 != 目标明确
行动强 != 目标明确
~~~

QI-16 不代表成功、吉凶或结果质量。

### QI-17-CAND：意志控制强度

继续为候选，不进入冻结核心向量：

> 在欲望、情绪、诱因或环境压力下维持自主约束与方向的能力。

### QI-18-CAND：毅力/持续性

继续为候选，不进入冻结核心向量：

> 在时间、阻力、延迟或重复挫折下维持行动的持续程度。

A1 的关键依据是源文明确区分“意志强弱”与“毅力”，因此不得再合并为一个“持续意志/韧性”。

### 恢复力/韧性

当前只保留为：

~~~text
DERIVED_SYSTEM_PROPERTY
~~~

不作为 primitive qi。后续如有独立规则与独立输出通路，再重新审议。

---

## 14. Observer / Kalman-like 接口：只作为未来研究接口

未来有真实纵向观测时，可以定义：

~~~text
xhat_t^- = prediction(E,u_t,z_t)
innovation_t = y_t - yhat_t
xhat_t = xhat_t^- + K_t * innovation_t
~~~

其中 `K_t` 表示：
- 对模型先验的信任；
- 对事件标签/测量的信任；
- 观测噪声水平。

Paper 1 不实际运行 Kalman filter，也不声称传统命理存在“真实物理状态”被滤波器测出。

---

## 15. Controllability 的边界

Paper 1 不做真正能控性分析，因为：
- 大限/流年不是控制输入；
- 当前没有干预数据；
- 没有因果辨识。

只有未来引入 `u_t^human` 并具备因果/干预数据后，才讨论：

~~~text
Can human actions move the system between desired states?
~~~

因此 Paper 1 仅定义接口，不计算 controllability matrix。

---

## 16. 第一篇最终系统架构

~~~text
SOURCE TEXT
   ↓
atomic rules
   ↓
L0 structural substrate
   ↓
star cores S_i^0
   ↓
star-system interaction h_s / mode z_s
   ↓
modifier operators T_m
   ↓
12 palace natal essences E
   ↓
temporal exogenous input u_t^astro
   ↓
state-dependent reaction R_t
   ↓
palace/context projection P
   ↓
semantic/observable output Y
~~~

主模型：

~~~text
E = BuildNatalEssence(chart_0)

U_t = BuildTemporalInput(chart_t)

R_t = React_theta(
    E,
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

未来动力学扩展：

~~~text
x_(t+1) = F_theta(
    x_t,E,u_t^astro,u_t^human,d_t,z_t,G_t,c_t
) + w_t

y_t = H_phi(x_t,E,z_t,c_t) + v_t
~~~

---

## 17. G5 冻结建议

建议冻结：

1. Paper 1 主模型采用“固定原局本质 + 时序输入 + 状态依赖反应”，而非强制逐年递归；
2. 十二宫采用局部节点 + 全局稀疏图；
3. 外生时序输入、人类控制输入、外部扰动严格分开；
4. 星系模态 z 与连续/序数气机状态并存，允许 hybrid-compatible 表达；
5. 修正曜作为条件算子；
6. 宫位作为场景投影算子；
7. 气->象->事分层；
8. Paper 1 只做 observation-path support / 可区分性启发式审计，不声称经典 structural observability；
9. Paper 1 只做参数角色/潜在不可辨识审计，不做连续系统辨识；
10. QI-16 已于 A1 升格为 L1；QI-17-CAND 与 QI-18-CAND 保持候选，恢复力仅 derived；
11. observer、controllability、optimal control 仅保留未来接口；
12. 递归状态方程明确标记为后续 HYPOTHESIS，不作为中州派原文定律。

## 18. 当前明确不做

Paper 1 不做：

- 任意连续赋权；
- 命例参数拟合；
- predictive validity 声明；
- 数值可控性/能观性矩阵；
- 在没有正式状态—输出结构条件时声称 structural observability；
- Kalman filter 真实估计；
- 最优趋吉避凶控制器；
- 因果政策推荐；
- 把“气”当成实证物理能量。


---

## 19. G5 approval record

**Status:** APPROVED by PI at G5.

冻结范围：主模型、十二宫局部节点+稀疏图、输入类型分离、气→象→事分层、结构能观性/可辨识性审计边界，以及 observer/controllability 仅作为未来接口。

具体连续参数、递归动力学真实性、QI-17 是否升格等仍保持开放。

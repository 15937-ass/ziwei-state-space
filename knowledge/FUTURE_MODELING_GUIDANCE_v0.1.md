# Future Modeling Guidance v0.1

Status: **NORTH-STAR GUIDANCE — NOT CURRENT RUNTIME REQUIREMENT**  
Issue: #419  
Scope: Zhongzhou canonical knowledge -> future empirical/dynamic modeling

## 1. Purpose

本文件记录当前讨论已经形成、但**不应一次性实现**的长期原则。它的作用是防止后续 Knowledge / Product / Empirical 工作各自局部优化后重新产生架构冲突。

原则：

> 理论架构可以宽；当前实现必须窄。  
> 只有数据、coverage 与 benchmark 达到门槛时，才升级模型复杂度。

## 2. Current minimum path

当前真正需要实现的最小链路：

```text
Source
 -> Atomic / reviewed rule
 -> Response Semantics
 -> [future Product adapter]
 -> ResponseProfile / symbolic tendency
 -> Manifestation candidates
```

Issue #419 只实现 Knowledge 侧 Response Semantics；Product adapter 不在本 work unit。

## 3. Long-term conceptual model

长期研究允许使用下列分层：

```text
K      canonical Zhongzhou knowledge
N      natal symbolic prior
E_t    temporal symbolic environment
tau_t  structural tendency / response field
X_t    real acquired/latent life state (not directly known)
A_t    actual action / choice
C_t    external context / constraints
Y_t    manifestation / real-world outcome
O_t    observation record
b_t    system belief about latent state
```

概念关系：

```text
(N, E_t, K) -> tau_t

X_(t+1) ~ F(X_t, tau_t, A_t, C_t) + disturbance

Y_t ~ H(X_t, C_t)

O_<=t -> b_t(X)
```

这是一种**研究假设/实现方向**，不是已经被证明的真实人生机制。

## 4. Why dynamic memory remains a valid future hypothesis

相同命盘与相同时间结构不要求相同人生轨迹。

长期模型应允许：
- 两人具有相同 symbolic tendency `tau_t`；
- 但已有状态 `X_t` 不同；
- 行动 `A_t` 不同；
- 外部环境 `C_t` 不同；
- 因而后续状态继续分叉。

程序不应把所有分叉都解释成“自由意志”，也不应把所有无法解释的差异强行归回斗数规则。必须保留 external / stochastic / unmodeled variance。

## 5. Ziwei output boundary

斗数 canonical layer 的长期职责是：

```text
chart + time + source-grounded knowledge
-> structural tendency / response
```

不是：

```text
chart + time -> one inevitable event
```

因此 future forecasting 应允许：
- direction / tendency；
- multiple manifestation channels；
- no-observed-manifestation；
- uncertainty / abstention。

## 6. Knowledge vs learned magnitude

Canonical knowledge 可以提供：
- membership；
- direction where source supported；
- relation；
- gate；
- interaction existence；
- ordinal constraints such as A > B；
- scope / exception。

Canonical knowledge 不应在无来源时创建：
- `0.73` 等连续 weight；
- manifestation probability；
- population frequency；
- personalized posterior。

未来经验层可以估计 magnitude：

```text
effect = source-constrained sign/structure * learned non-negative magnitude
```

如来源明确 ordinal，可用 constrained parameterization 保证训练不违反已冻结顺序。

## 7. Unknown is not false

所有层必须区分：
- SUPPORTED；
- CONTRADICTED；
- UNKNOWN；
- CONFLICTING。

“书里没写”不能自动转成 `effect = 0`。  
“用户没反馈”不能自动转成 `event = false`。

## 8. Prior / posterior boundary

三种对象永久隔离：

```text
K      = source/canonical knowledge
theta  = population/cohort empirical parameters
b_i,t  = individual state belief/posterior
```

个人反馈主要更新 `b_i,t`，不能直接改写 `K`。  
单个人反馈不能直接改写 population `theta`。  
群体参数只能通过离线、版本化、可复现实验更新。

## 9. Blind vs personalized evaluation

未来必须保留两条预测轨道：

### Blind
只使用预测时点前预注册允许的信息，检验 Ziwei feature 本身的增量预测价值。

### Personalized
允许使用过去反馈、acquired state、action/context 与 individual posterior。

二者不能混报指标。

Retrospective smoothing 只能标为后验解释，不能冒充当时预测。

## 10. Non-Ziwei baseline is mandatory

未来经验验证至少比较：

```text
Baseline:
age / occupation / prior history / context

vs

Baseline + Ziwei response/tendency features
```

研究目标是检验：

```text
Does Ziwei add out-of-sample predictive information?
```

模型必须允许结果为“未发现增量预测价值”。

## 11. Identifiability before training

在训练单星、pair interaction、context gain 之前必须检查：
- feature co-occurrence；
- rank / collinearity；
- parameter separability；
- sample support；
- structural/practical identifiability。

不可辨识时应：
- 合并参数；
- 保留 symbolic constraint；
- 收集更有区分度的数据；
- 或承认该参数当前不可估。

不能用更大的 neural model 掩盖不可辨识。

## 12. Human choice model — future only

长期可以研究：

```text
A_t ~ pi(history, perceived options, goals, body state, context)
```

并区分：
- choice set；
- intent；
- planned action；
- actual action；
- external constraint。

但当前 Product 不实现“人为什么做决定”的模型。  
先把 action 当 observed / unknown variable。

身体状态、价值、主体 world model、habit/reflexivity 等只作为未来 candidate，不进入当前 canonical runtime。

## 13. Multi-timescale and state-space — future only

未来可检验：
- slow / medium / fast acquired states；
- natal / decade / year 等时间层是否与现实时间尺度存在稳定 correspondence；
- nonlinear state-space / switching model 是否优于简单 baseline。

不得因为理论形式优美就直接宣称这些对应关系成立。

## 14. Forecast ledger before sophisticated AI

在任何大规模 calibration 前，优先建立 versioned prospective record：

```text
forecast_id
information_cutoff
knowledge_version
model_version
mode = BLIND | PERSONALIZED
target_window
forecast
later_outcome
```

预测后不回写旧 forecast，只追加 evaluation。

## 15. Complexity ladder

建议复杂度按证据逐级升级：

```text
R0 Response Semantics
R1 symbolic / ordinal response inference
E0 longitudinal + forecast ledger
E1 GLM / ordinal / survival baseline
E2 hierarchical Bayesian
D1 Bayesian/state-space memory
D2 action/choice model
D3 nonlinear residual / neural state-space
P1 scenario/decision support
```

每次升级必须证明：
- simpler baseline 不够；
- held-out improvement；
- calibration 不恶化；
- traceability 可接受；
- 数据量与 identifiability 足够。

## 16. Program architecture rule

禁止把 future north-star 一次性变成当前需求。

当前仓库长期遵循：

```text
Source truth
!= modeling assumption
!= learned parameter
!= personal posterior
!= empirical finding
```

任何 Product runtime integration、empirical training、causal recommendation、decision support，均需对应 lane 的独立 Issue / gate。

## 17. Immediate consequence for Knowledge

Knowledge 当前只新增：
- Response Semantics schema；
- source-grounded pilot；
- 后续对 251 blocker 的 compatibility classification。

Knowledge 当前不新增：
- continuous weights；
- probabilities；
- personal state；
- user feedback model；
- world-model runtime。

这使本轮理论升级成为“增加一层语义表达能力”，而不是“重写整个项目”。

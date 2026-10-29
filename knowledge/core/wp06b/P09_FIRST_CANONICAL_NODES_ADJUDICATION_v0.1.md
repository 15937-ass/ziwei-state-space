# P09 第一批 canonical manifestation nodes 准入审定 v0.1

**状态：`THREE_ORDINARY_NODE_IDENTITIES_ACCEPTED_MAPPING_NOT_PROMOTED`**  
**工单：** #874 / `KB-CORE-WP06B-P09-FIRST-CANONICAL-NODES-01`

## 1. 结论

本批对 #864 已完成逐目标 mapping-review 的三个 P09 target 只做 **canonical node identity** 晋升：

| Source | Canonical ID | Identity | Node 结论 | Mapping / execution |
|---|---|---|---|---|
| CA01-035 | `KMN-000001` | 事业发展波折、经艰苦后趋于底定的过程概念 | ACCEPT | mapping 未晋升；火铃 AND/OR 未决；不可执行 |
| CA01-045 | `KMN-000002` | “勉强求变”现实行动条件下陷入事业困境的条件结果 | ACCEPT | mapping 未晋升；现实行为前提无接口；不可执行 |
| CA05-469 | `KMN-000003` | 血光象义对应的职业／行业场景 | ACCEPT | mapping 未晋升；个人伤病事件 target 明确不支持；不可执行 |

这里的 ACCEPT 只表示“这个概念已经有稳定 Knowledge identity”，不表示任何命盘条件已经与该 node 建立 canonical mapping。

## 2. 为什么 CA01-035 可以 canonicalize

来源已经直接核验，并且 #864 正向 review 支持 process target、反向 review 排除 single observed event。

“火铃”究竟是 BOTH_STARS 还是 EITHER_STAR 仍未决，但这影响的是**什么条件能触发 mapping**，不是“事业发展可能经历波折／艰苦后趋于底定”这个 target 本身的身份。

因此：

- node identity 稳定；
- trigger mapping 仍 held；
- 保留“往往”，不升级为必然、频率或时间。

## 3. 为什么 CA01-045 可以 canonicalize

原文完整语境为事业宫禄存，再见空劫同度，并出现现实行为“勉强求变”，随后“结果反而陷入困境”。

#864 已明确：

- action-conditioned target = supported candidate；
- chart-only unconditional target = not supported。

因此“现实行动条件下的困境结果”本身可以有稳定 identity，但：

- CA01-042 / CA01-044 上下文不能删除；
- 不能从盘面自动断言“勉强求变”已经发生；
- 在现实行为前提没有 accepted interface 前，mapping/runtime 仍保持 held。

## 4. 为什么 CA05-469 可以 canonicalize

CA05-469 来源位于事业语境，source span 已核验。#864 保留：

- `source_epistemic=EXPLICIT`；
- `normalization_epistemic=INFERRED`；
- career/industry scene target = supported candidate；
- person-level injury/illness/accident target = not supported。

PI 在 #866 接受 G2A，已经明确允许 transparent/traceable `INFERRED` normalization 支持 ordinary node identity。因此该职业／行业场景可以 canonicalize，但个人伤病事件仍是明确禁止推论。

## 5. review_provenance 中 normalization_verified 的含义

三个 node 均记录 `normalization_verified=true`，这里的“verified”含义严格限定为：

> normalization epistemic 和 target 边界已经在 #864 的 accepted formal mapping-review 中被显式审查，并符合 #866 G2A 与 #868 canonical gate。

它**不表示** normalized target 是古籍原文逐字表达；CA05-469 仍明确保留 `normalization_epistemic=INFERRED`。

## 6. Forest / abstraction_level

三个 node 当前都没有已接受 canonical parent，因此 `parent_id=null`。这不创建 universal root。

本批 `abstraction_level=ORDINARY_TARGET_CONCEPT` 只是开放描述性 metadata，用于标记其属于 G1A ordinary-node 范围；它不是新的 universal family、root 或受控 ontology primitive，也不冻结为穷尽枚举。

## 7. 明确未授权

- canonical mapping promotions = **0**
- executable mappings = **0**
- Product registry/runtime changes = **0**
- universal root/family/shared primitive = **0**
- probability / numeric strength / empirical validity = **0**

下一步若要把任何 source condition 与这些 node 建成 canonical mapping，必须另立有界 Core 工单。

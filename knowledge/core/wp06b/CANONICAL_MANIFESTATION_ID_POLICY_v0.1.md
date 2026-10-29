# Canonical Manifestation Stable-ID Policy v0.1

**状态：`CANONICAL_CONTRACT_FROZEN_NO_PRODUCTION_NODES_ASSIGNED`**  
**工单：** #868 / `KB-CORE-WP06B-CANONICAL-MANIFESTATION-NODE-CONTRACT-01`  
**PI 授权依据：** #866 已接受 G1A / G2A / G3A。

## 1. 这张工单冻结什么

本工单只冻结两件事：

1. 一个 Knowledge canonical manifestation node 至少必须保存什么；
2. stable ID 如何分配、保持稳定、处理 parent 与 supersession。

本工单**不分配任何真实 production node ID**，不把 P09 mapping 升成 canonical mapping，也不修改 Product。

## 2. Stable ID

正式 Knowledge manifestation node 使用：

`KMN-NNNNNN`

其中 NNNNNN 为六位单调递增整数。ID 是 opaque identity，不编码星曜、宫位、domain、层级、吉凶、概率或经验权重。

原则：

- 只在 accepted main 上读取现有最高 KMN 编号后分配下一个编号；
- Core WIP=1 + Knowledge merge serialized，避免并发抢号；
- ID 一旦分配永不改号、永不回收；
- display label、domain 文案或描述性措辞调整但 identity 不变时，ID 不变；
- 如果语义边界真的改变到“已不是同一个节点”，创建新 ID，并通过 supersession 显式连接；
- TEST_ONLY 的 `MFX-*` / `M0-FX-*` 不能升级为 production 命名规范。

## 3. Option C forest 与 parent

`parent_id=null` 的唯一含义是：

> 当前 canonical artifact 中没有已接受的 canonical parent。

它**不表示**存在一个隐含的 universal manifestation root，也不表示该节点已经被归入某个 universal family。

非空 parent 必须在同一 canonical artifact 中真实存在；parent graph 必须无环。新增 universal family/root/shared primitive 仍然触发 PI Human Gate。

## 4. Canonical node 最小字段

未来每个节点必须至少保存：

- stable `manifestation_id`；
- `parent_id`；
- `domain`、`abstraction_level`；
- source-supported labels、rule IDs、provenance refs；
- `output_kind` 与 `event_specificity` 的 state/value；
- `source_epistemic`、`normalization_epistemic`；
- review provenance；
- target-specific mapping-review refs；
- identity rationale；
- ambiguity / unresolved notes；
- `probability_status=UNKNOWN`；
- ambiguity notes 与 `unresolved_notes`；
- canonical identity status 与 supersession links / reason。

`output_kind` 与 `event_specificity` 的 value 字段保持开放字符串；schema **不**把当前候选值冻结成穷尽 production enum。状态仍使用 `KNOWN / UNKNOWN / MISSING / CONFLICT / NOT_APPLICABLE`。

## 5. Ordinary node canonicalization gate

G1A/G2A 下，ordinary node 不需要逐节点找 PI，但必须全部满足：

- source epistemic 为 `EXPLICIT` 或 `INFERRED_FROM_SOURCE`；
- source span 已核验，review status 至少为 `SOURCE_SPAN_VERIFIED` 或 `HUMAN_VERIFIED`；
- normalization 为 `SOURCE_PRESERVING` 或可追溯的 `INFERRED`；
- normalization 已验证；
- 至少一个 target-specific mapping review 明确支持该 concept；
- 没有会改变 identity 的 unresolved conflict；
- case-only / hypothesis 不能作为唯一支撑；
- `probability_status=UNKNOWN`；
- 没有顺带创建 universal root/family/shared primitive；
- exact-head deterministic validation 全绿。

`MISSING` 或 `CONFLICT` 在 review 层继续是合法状态，但**不能进入 canonical node schema**；canonical node 只接受 `KNOWN / UNKNOWN / NOT_APPLICABLE`。`UNKNOWN` 只有在该未知不改变节点 identity 边界时才可保留。canonical schema 同时直接拒绝 `UNRESOLVED_SOURCE / IMPLEMENTATION / HYPOTHESIS / UNRESOLVED` 等不满足 G1A/G2A 的 epistemic 值，避免“policy 阻断、schema 却放行”。

## 6. Supersession

节点拆分、合并或 identity 发生实质变化时：

- 原 ID 不改写；
- 原节点标记 `SUPERSEDED`；
- 新节点获取新 KMN ID；
- old/new 双向记录 `supersedes` / `superseded_by`；
- 禁止 silent repointing。

## 7. Product 边界

canonical Knowledge node 只说明“传统知识层已经有稳定身份”，**不等于 Product 可消费**。

Product 仍按 G3A fail-closed，后续由 Product-owned adapter/crosswalk 单独处理。Core 不修改 Product schema、registry 或 runtime。

## 8. 下一步

本合同通过并合并后，另开有界 Core 工单，从 P09 mapping-review pilot 中选择满足门槛的 ordinary nodes 做第一批真实 canonicalization。mapping promotion 继续单独处理。

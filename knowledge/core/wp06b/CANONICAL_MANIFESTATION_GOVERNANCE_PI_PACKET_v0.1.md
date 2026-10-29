# Canonical Manifestation Governance — PI 决策包 v0.1

**状态：`READY_FOR_PI_REVIEW_PROPOSAL_ONLY`**  
**工单：** #866 / `KB-CORE-WP06B06C-CANONICAL-NODE-GOVERNANCE-PI-PACKET-01`

## 1. 为什么现在必须让 PI 决定

#841 已经确定了应象审核的最小语义契约；#864 又用三条真实 P09 候选证明，这套契约确实可以做逐目标 mapping-review，而且不需要再发明新的审核字段。

真正的新问题出现在“从 reviewed candidate 迈向 canonical ontology”这一刻：

1. 路线图本来规定：ordinary ontology child node 不应每一条都触发 Human Gate；但 #841 又明确没有授权我们直接创建 canonical ontology ID。
2. Knowledge 现在已经有 PI 接受的 `output_kind` 与更细粒度的 `event_specificity`；Product v0.1 却没有 `output_kind`，事件粒度也只有 `ABSTRACT / SCENE_LEVEL / CONCRETE_EVENT`。
3. CA01-045 还带有“勉强求变”这一现实行为前提，而 Product router 当前只能匹配 activation ID / rule ID，不能靠命盘事实证明现实行为发生。

所以现在不应该“顺手给三条规则编号然后塞进 Product”。应该先把 canonicalization 的治理方式定下来。

## 2. 已确认的事实

- Knowledge 是 ontology owner；Product 文档明确把自己定义为 adapter / consumer。
- Product production ontology 仍是 `EMPTY_PENDING_KB_WP06B`，mapping registry 仍是 `EMPTY_PENDING_KB_WP06C`。
- 路线图要求 L4 节点保留稳定 identity、层级、domain、source labels/rules、event specificity、ambiguity、`probability_status=UNKNOWN`。
- #841 进一步接受了 `output_kind` 与 `event_specificity` 正交。
- Product 当前 node contract 没有 `output_kind`；直接把 Knowledge 压成 Product 字段会丢失已接受语义。
- 仓库目前只有 TEST_ONLY 的 `MFX-*` / `M0-FX-*` fixture ID，没有正式 production manifestation ID 命名规范；测试 ID 不能升级成生产约定。

## 3. 决策卡 G1 — 普通 child node 是否要逐条找 PI

### G1A — 推荐：一次性政策授权

PI 只批准一次规则：

> ordinary、source-backed 的 child node，只要满足冻结的证据与语义门槛，可以由 Core 自动分配稳定 Knowledge canonical identity；不再逐节点找 PI。

必须同时满足：

- 来源跨度与 provenance 已审核；
- 对该 target 的 mapping-review 为来源支持的候选；
- node 本身的语义边界稳定；
- 没有会改变 node identity 的未决冲突；
- case-only / hypothesis 不能作为唯一支撑；
- `probability_status=UNKNOWN`；
- 不新增 universal manifestation family / root / shared primitive；
- 不自动开放 Product/KIB/runtime；
- exact-head deterministic gate 全绿。

**仍然必须找 PI 的情况：** 新 universal family/root、共享 primitive、核心语义变更，以及既有政策无法表达的冲突。

具体 ID 字符串的格式属于实现细节，不需要 PI 逐个决定；但必须是稳定、Knowledge-owned、不能复用 TEST_ONLY fixture ID。

### G1B — 每个节点都 PI 审批

控制最强，但会把 PI 变成持续瓶颈，也比路线图对 ordinary child node 的原始治理更严格。

**建议：G1A。**

## 4. 决策卡 G2 — “透明推断”能不能进入普通 canonical node

这里不是问“案例猜出来的东西能不能 canonical”。答案仍然是不可以。

真正的问题是：像 CA05-469 这种**原文明确存在，但把原文职业象义归一成一个职业/行业场景节点时发生了可追溯的语义转换**，是否允许成为 ordinary canonical node。

### G2A — 推荐：允许可追溯推断，但必须保留认识论

允许：

- source-preserving normalization；
- transparent / traceable inference，且必须保存 `normalization_epistemic`、来源、理由和 target-specific review。

禁止：

- CASE_SUPPORT_ONLY 作为唯一支撑；
- HYPOTHESIS 作为唯一支撑；
- 无理由的 silent inference；
- 会改变 node identity 的 unresolved conflict。

对当前三条 P09：

| 候选 | G2A 下 |
|---|---|
| CA01-035 过程型 | 可进入普通 node eligibility |
| CA01-045 行动条件结果 | node identity 可审；但 mapping/runtime 仍因“勉强求变”现实行为前提被 hold |
| CA05-469 职业/行业场景 | 可作为 traceable inferred scene node eligibility；个人事件 target 仍明确不支持 |

### G2B — 仅 source-preserving 才能 canonical

CA01-035 / CA01-045 可继续，CA05-469 场景节点继续 held。

优点是极保守；缺点是会把很多“原文象义 → 分层 ontology”的必要透明归一化永久挡在 candidate 层，而 L4 本身就是为了完成这种可追溯抽象。

**建议：G2A。**

## 5. 决策卡 G3 — Knowledge 与 Product 字段不一致怎么办

### G3A — 推荐：Knowledge 保真，Product 后续单独做 adapter

Knowledge canonical artifact 保留完整 source-native 语义，包括 #841 接受的 `output_kind` 和细粒度事件关系。

Product 继续 fail-closed。等 Knowledge 真正有 canonical artifact 后，再由 **Product-owned** 工作单元设计显式 adapter/crosswalk。

这样：

- Product 的 `ABSTRACT / SCENE_LEVEL / CONCRETE_EVENT` 可以只是消费侧分类，不反向成为传统知识真理；
- `output_kind` 不会消失；
- 对无法无损映射的 Knowledge node，Product 可以 abstain / held，而不是强行压扁；
- CA01-045 在现实行为前提没有正式接口前继续不执行。

### G3B — 把 Knowledge 压成 Product 当前字段

**不建议。** 会丢掉 D1–D5 刚建立的正交语义。

### G3C — Core 现在直接改 Product schema

**不建议。** 这是跨 lane 混写；ontology owner 与 consumer implementation 应保持分离。

**建议：G3A。**

## 6. 推荐 PI 决议

**推荐：`G1A，G2A，G3A`。**

如果接受，下一步 Core 可以建立一套 Knowledge-owned canonical manifestation artifact / stable ID policy，并对满足规则的 ordinary child nodes进行有界 canonicalization，不再逐节点找 PI。

但即使三项都接受：

- 不代表当前三条 mapping 自动变成 canonical mapping；
- 不代表 Product registry 可以马上填充；
- 不代表 CA01-045 可以执行；
- 不代表可以创建 universal root/family；
- 不代表允许概率、权重或经验效度进入传统知识。

## 7. 当前明确不做的事

本工单不会创建任何 production manifestation ID，不修改 Product，不接受 canonical mapping，不开放 runtime，不引入概率，也不把 fixture ID 当生产规范。

**PI 只需回复：** `G1A，G2A，G3A`，或指出要改成的选项。

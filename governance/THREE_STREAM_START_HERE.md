# 三线推进操作卡（v2.2）

跟踪：[Issue #725](https://github.com/15937-ass/ziwei-state-space/issues/725)。这是已有总计划、恢复与交接规则的中文操作入口，不是另一份实时状态表。接受状态以该 Issue/PR 和 main 为准。

## 你只要保留三个工作对话

| 对话名称 | 新对话发什么 | 负责什么 |
| --- | --- | --- |
| 宫位线 | 推进宫位线 | 按既定逐宫顺序核对教材；对产品反馈做来源定向回溯，不打断当前批次 |
| Core线 | 推进Core线 | 按 #901 / v2.2：C9 已接受；下一项先核对 v0.5 原局结构与 Product 消费契约，再研究共享时间层语义 |
| 产品线 | 推进产品线 | 按 #900 / v2.2：完成 NATAL DetailedRead，随后做小型实际命盘/案例使用检验，再按 accepted Knowledge/Core checkpoint 升级 DECADE、YEAR |

三个不同工作线的对话可以同时推进独立工作。常态目标是“1 个宫位 + 1 个 Core + 1 个 Product”三槽并行；正式合入 main 由 Integration Lease 串行控制。不要为了等待别人合并而停止本线的独立研究/开发，也不要在 ACTIVE_BUILD 阶段为了无关 main 变化反复重跑最终全量门。不必每次重新创建对话；同一对话到下一轮时也可以只发“继续”。替换旧对话时先让旧对话停止并保存交接，再让新对话接手；不要让两个对话同时写同一条线。

对话不会因为已打开就永久在后台工作。每轮只完成一个有界工作单元或可恢复检查点；下一轮由你发“继续”或在新对话使用相同入口。外部 CI 可继续运行，但不代表聊天执行者还在工作。

## 首次启动的三段完整指令

下面三段分别复制到对应新对话；以后沿用该对话只发“继续”即可。

### 宫位线

> 继续 15937-ass/ziwei-state-space 的宫位线。先读取 main 上的 CHATGPT_START_HERE.md，按标准恢复顺序读取 governance/THREE_STREAM_START_HERE.md 的宫位安排，核对实时任务和旧对话交接。接续一个已获准、可执行的宫位工作单元，遵守一次一个宫位。若 Product 提供 KNOWLEDGE_GAP，只有在完成当前批次或达到 P0 正确性门槛时才做定向回溯；不得增加宫位槽位或把产品反馈当作来源真理。每轮完成到可恢复检查点，写回 Issue/PR，结束时用中文汇报三线状态和下次继续的位置。

### Core线

> 继续 15937-ass/ziwei-state-space 的Core线。先读取 main 上的 CHATGPT_START_HERE.md，按标准恢复顺序读取 governance/THREE_STREAM_START_HERE.md、governance/CORE_PRODUCT_CONTINUATION_PLAN_v2.md 和 Core plan pointer #901，核对实时 Core Issue/PR 与旧对话交接。若已有 ACTIVE Core 单则接续；若 Core 槽位空闲则直接领取计划中最早可执行的 bounded nominee（C9 #945/#946 已接受；下一项先复核已接受的 v0.5 NATAL 结构与 Product 消费契约，再推进共享时间层语义），无需让我重述顺序。每轮只推进一个 Core 工作单元，遇到计划规定的真实 Human Gate 才停下来给中文原文依据和例子，结束时汇报三线状态和下次继续的位置。

### 产品线

> 继续 15937-ass/ziwei-state-space 的产品线。先读取 main 上的 CHATGPT_START_HERE.md，按标准恢复顺序读取 governance/THREE_STREAM_START_HERE.md、governance/CORE_PRODUCT_CONTINUATION_PLAN_v2.md 和 Product plan pointer #900，核对实时 Product Issue/PR 与旧对话交接。若已有 ACTIVE Product 单则接续；若 Product 槽位空闲则直接领取计划中最早可执行的 bounded nominee（首个工作单元：PRODUCT_NATAL_DETAILED_READ_CLOSED_LOOP_V1），无需让我重述顺序。Product 原局详批可使用当前 main 已接受的 RUNTIME 与 allowed SOURCE；#951 接受后先完成一个小型、可复现的实际命盘/来源完整案例使用检验，核对证据消费、十二宫覆盖/缺口、跨宫行为与 provenance。没有合格案例时记录精确阻塞，不得用合成夹具冒充实际使用。DECADE/YEAR 只消费已接受且明确可供 Product 使用的时间层 checkpoint，不跟随未合并分支；每轮写回可恢复检查点，遇到计划规定的 Human Gate 才停下来，结束时汇报三线状态和下次继续的位置。

若只想看进度，发“查看三线状态”：只读核对实时宫位、Core、Product 及 main，给一个优先建议，不领取新任务。

## 执行者每轮如何接手

1. 先按 PROJECT_STATE.yaml -> CHATGPT_START_HERE.md -> governance/RECOVERY_PRECEDENCE_v1.md 恢复，再读所选工作线/分片缓存、实时 Issue、关联 PR 和最近交接。本文中的“先读取启动文件”是入口指路，不改变标准恢复优先级。
2. 先找已存在的有界任务，不能因 YAML 写着没有活动任务就重复建单。确认原执行者已停止/显式交接；若原对话仍在执行，新对话仅只读报告。交接不明确时不猜测领取写入权，先解决执行归属。Issue 评论、时间戳不是原子锁，也不能保证两个新对话同时领取时自动互斥。
3. “继续”授权恢复既有安排内的一轮工作，不自动批准新的语义、运行权限或优先级变更。对 Core/Product，PI 已通过 governance/CORE_PRODUCT_CONTINUATION_PLAN_v2.md 授权：若该线无 ACTIVE 单且槽位/依赖满足，可在这个新执行回合直接领取 plan pointer #901/#900 中最早可执行的 bounded nominee，无需再次向 PI 询问顺序。完成本轮后仍不要在同一回合自动执行下一个 Issue；先留下下一 nominee/交接，由后续“继续”回合领取。宫位线维持既有逐宫规则。
4. 只写自己的工作线与已登记分片路径；只读取正式接受的 main 成果作为正式输入。共享语义归 Core，宫位不跨线补定义，Product 不猜造知识。
5. 各线在 ACTIVE_BUILD 阶段独立准备并运行本线有界/相关检查；内容完成后进入 READY_TO_INTEGRATE，并在 Issue #888 排队。只有取得 Integration Lease 的工作单才进入 INTEGRATING：此时重核 main/base/head、同步一次当前 main、运行最终 exact-head 全量门并立即合入/释放。别的线在 lease 被占用时仍可继续工作，只是不能同时改 main。正式集成按依赖和验证就绪程度选择，不固定为“宫位 -> Core -> 产品”轮转；旧绿灯在 main 变化后仍不能直接沿用。
6. 停止前按 AGENT_WORKFLOW.md §§10.3、13 在现有 Issue/PR 留下版本、产物、已做/未做、疑点、执行归属、验证和精确下一步。用中文回答三条线各自能做什么、等什么；最多推荐一个近期集成候选。禁止只把关键安排留在聊天中。


## v2.2：产品反馈分类、优先级与三线闭环

三线常态仍是 **1 个宫位 + 1 个 Core + 1 个 Product** 并行；Core/Product 各 WIP <= 1，宫位继续 #676 一次一个。反馈只改变后续任务的定向优先级，不新增槽位，也不要求每个小问题立即打断当前批次。

Product 的实质性问题按一个主类别记录：
- `KNOWLEDGE_GAP`：宫位专属来源、条件或时间层证据缺失/不清 -> 对应 Knowledge shard。
- `CORE_GAP`：共享结构、跨宫或时间层语义无法由当前 Core 契约表达 -> Core；适用时沿用 `KNOWLEDGE_CORE_GAP` 交接标记。
- `PRODUCT_GAP`：读取、编排、证据消费、界面、provenance 或 fail-closed 实现错误 -> Product。
- `HOLD_UNKNOWN`：来源不足或不可调和冲突 -> 保留未知，不强行归因或下结论。

优先级：
- **P0**：相关输出若继续会形成无依据、结构错误或污染 canonical meaning 的判断；立即对受影响判断 fail closed，并交给责任线处理。
- **P1**：阻塞当前阶段验收或下一阶段准入；记录精确缺失输入，排入责任线下一个合格有界工作单元。
- **P2**：非阻塞改进；写入现有 Issue/PR，后续处理。

所有反馈沿用 `governance/CROSS_LANE_HANDOFF_v1.md` 的 producer、consumer、missing input、dependency、unblock evidence、safe parallel work 和 ownership 字段。记录命盘/案例 fixture 及版本、accepted main SHA、涉及宫位、实际/预期行为、证据、分类、优先级和复测结果。不得建立第二个状态台账，不得跨线写文件。

### 三线下一步

- **Knowledge**：继续当前唯一宫位批次；P2 不打断，P1 排入后续定向来源复核，P0 只阻断受影响结论。
- **Core**：C9 #945/#946 已接受。下一项 Core 有界研究先检查 accepted v0.5 NATAL 结构与 Product 消费契约，识别可复用内容和真正的共享语义缺口，再推进 NATAL/DECADE/YEAR response semantics；不重建状态空间模型。
- **Product**：继续 #951。#951 合并后做一个小型实际命盘/来源完整案例使用检验；它验证实现和来源/方法忠实度，不等于现实预测有效性。只有 NATAL 闭环、实际使用检查和匹配的 accepted、Product-consumable 时间层证据满足时，才进入 DECADE；YEAR 还须等待大限结构稳定和匹配流年证据。

阶段门槛按能力和证据判断，不按知识条目总量判断。允许明确存在覆盖缺口，但不允许把 UNKNOWN 填成结论。所有消费仍只基于 accepted main 和 allowed-use。
## 后续工作的依赖顺序

以下是 PI 已批准的长期路线，不是对未合并分支的消费授权，也不替代实时 Issue/PR。每一步先核对 live 状态、来源依赖和写集，复用已有交付。

### 宫位：继续现行逐宫来源研究

- 现行顺序与准入规则见 [逐宫审计安排](PALACE_AUDIT_SEQUENCE_2026-10-23.md) 和 #676；一次只准入一个宫位。
- 继续当前已准入宫位，按来源覆盖、残余疑点和阶段交接推进。
- 对大限/流年材料，逐步标记 NATAL / DECADE / YEAR 层级、前提、作用对象、跨层依赖和例外；不能把原局规则改写成时间层规则。
- WP06C 正式映射仍等待相关 Core 契约、节点 ID、来源审查和宫位准入条件全部满足。
- 本次 PI 决定没有批准两宫位并行；不得启用 P06 #773 作为第二槽。

### Core：C9 已接受 → NATAL 结构消费契约检查 → 共享时间层语义

详细顺序见 [Core + Product Continuous Progression Plan v2](CORE_PRODUCT_CONTINUATION_PLAN_v2.md) 与 plan pointer #901。

- C9 #945 / PR #946 已在 main 接受，不重新打开或扩展。下一项 Core 工作先用一个有界检查点核对 accepted v0.5 NATAL 结构与 Product 消费契约，识别已可复用内容和真实共享缺口，再推进时间层语义；不重建模型。
- C9 关闭后，Core 下一优先级是 NATAL、DECADE、YEAR 的共享时间层关系与 response semantics：区分 NATAL 基础、DECADE 环境、YEAR 环境、`tau_t` 反应及有来源支持的层间依赖。
- 不预设大限与流年简单相加或线性叠加；保留来源前提、继承关系、跨宫依赖、修饰条件和 UNKNOWN/HOLD。
- WP03 六十星系验证、WP06A 案例重建和王亭之案例作为原局/时间层推理链的验证材料，不再排在 Product 原局详批之前作为独立首要阻塞。
- Core WIP 永远 <=1；不新建未经批准的通用算子、概率、因果或 Product/runtime 授权。

### Product：NATAL DetailedRead → DECADE → YEAR

详细顺序见 [Core + Product Continuous Progression Plan v2](CORE_PRODUCT_CONTINUATION_PLAN_v2.md) 与 plan pointer #900。

- **第一优先级：`PRODUCT_NATAL_DETAILED_READ_CLOSED_LOOP_V1`。**
- 复用 Product #798 QuickRead capability/main-reader、#882 DetailedRead planner 和 #894/#895 DetailedRead Skill；不重复实现排盘、规则引擎或详批规划器。
- 十二宫全部进入 NATAL 检查，但每宫证据覆盖可以不同；RUNTIME、允许使用的 SOURCE、MODEL_SUPPLEMENT 和缺口分别记录。
- 渐进读取必须去重并 pin 同一 main snapshot；最终按人生主题综合，执行跨宫一致性检查，不强行填充。
- NATAL 详批可使用当前已接受且 allowed-use 允许的 RUNTIME/SOURCE，不以 KIB 晋升为前提；这不改变 active KIB/lock、registry 或 runtime 权限。
- #951 接受后，先做一个小型、可复现的实际命盘/来源完整案例使用检验，核对证据消费、覆盖/缺口、跨宫行为和来源链；没有合格 fixture 时如实记录阻塞。该检验只验证实现与来源/方法忠实度，不证明预测有效性。随后只有在 NATAL 闭环、实际使用检查及匹配的 Knowledge/Core 时间层成果进入 accepted main 并明确达到 Product 消费条件时，才升级 DECADE；大限结构稳定且匹配 YEAR 证据可消费后再升级 YEAR。
- 任何未获消费授权的 KMM、CASE_SUPPORT_ONLY、SEMANTIC_ONLY 或 BLOCKED 材料继续保持原状态；无证据时输出缺口，不输出具体时间事件。

### 三线并行和交接

- 常态目标仍为 1 个宫位 + 1 个 Core + 1 个 Product 并行生产；各线 WIP 上限不变。
- Product 原局详批可以与当前 Core C9、宫位来源研究并行，因为它消费的是当前 main 已接受的 NATAL 证据。
- Product 发现接口问题归 Product；发现共享时间层语义缺口才交 Core；宫位来源缺口交对应 shard。
- 正式集成仍由 #888 Integration Lease 串行控制。不得消费未合并分支。
- Forecast Ledger 继续等待第一条 source-only `N -> E -> tau -> M0` vertical slice 真正可执行；传统案例忠实度不等于现实预测有效性。

## 启动定位快照：只用于找任务

以下仅为 2026-10-24 的导航快照（观察 main：50e0d4d5a0c74baf522a9c5a43ec90e0142c92dd），不是需要各线维护的实时状态表。新对话必须查当前 Issue/PR，发现已关闭或已替换时沿最新交接继续。

| 线 | 观察到的定位 | 不能据此推断 |
| --- | --- | --- |
| 宫位 | 财帛宫 #723 / PR #724，太阴印刷页84–85；前批已由 #721 接受 | 未合入的新记录不能计入正式知识 |
| Core | #720 / PR #722，前七星33条直接证据审查；后续七星另批 | 来源核对不自动接受性质归一化或正式本体 |
| 产品 | #715 / PR #718，用户叙述候选校验；已记录 head 检查通过，仍 Draft/unmerged | 旧基线测试通过不等于可直接合入最新 main |

总计划：[W0–W8 与跨对话交接](proposals/700-durable-ontology-plan-and-cross-chat-handoff.md)；依赖交接：[CROSS_LANE_HANDOFF_v1.md](CROSS_LANE_HANDOFF_v1.md)。旧计划的 A/B/C 未选快照不能覆盖后续 #704/#710/#713 的真实批准范围；方向批准、提案接受、正式契约和运行消费分别核对。

## 本卡的边界与维护

本文只提供稳定入口和已有安排的依赖说明，不新增调度器、自动化、权限、必需检查或第四条执行线，不改变现有 WIP、Human Gate、逐宫安排和知识包晋升规则。打开新对话不保证其有 GitHub 工具权限；无法核实时明确报告“未核实”，不按旧聊天猜进度。

日常进度只写所属 Issue/PR 及其版本化证据，不为更新此导航快照而跨线改文件。只有入口或安排确需修改时才走独立有界 Governance 任务。回滚本次 Governance PR 中的计划、状态缓存与启动入口改动即可撤销本路线调整；历史知识成果和语义不受影响，原三线成果与语义不受影响。

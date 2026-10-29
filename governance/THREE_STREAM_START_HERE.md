# 三线推进操作卡

跟踪：[Issue #725](https://github.com/15937-ass/ziwei-state-space/issues/725)。这是已有总计划、恢复与交接规则的中文操作入口，不是另一份实时状态表。接受状态以该 Issue/PR 和 main 为准。

## 你只要保留三个工作对话

| 对话名称 | 新对话发什么 | 负责什么 |
| --- | --- | --- |
| 宫位线 | 推进宫位线 | 按既定逐宫顺序核对教材、保存条件和疑点 |
| Core线 | 推进Core线 | 按 #901 / continuation plan 连续扩展 canonical mapping、吸收真实共享语义 gap、再进入 WP07B |
| 产品线 | 推进产品线 | 按 #900 / continuation plan 从 manifestation crosswalk pilot 开始，消费已接受 Core checkpoint |

三个不同工作线的对话可以同时推进独立工作。常态目标是“1 个宫位 + 1 个 Core + 1 个 Product”三槽并行；正式合入 main 由 Integration Lease 串行控制。不要为了等待别人合并而停止本线的独立研究/开发，也不要在 ACTIVE_BUILD 阶段为了无关 main 变化反复重跑最终全量门。不必每次重新创建对话；同一对话到下一轮时也可以只发“继续”。替换旧对话时先让旧对话停止并保存交接，再让新对话接手；不要让两个对话同时写同一条线。

对话不会因为已打开就永久在后台工作。每轮只完成一个有界工作单元或可恢复检查点；下一轮由你发“继续”或在新对话使用相同入口。外部 CI 可继续运行，但不代表聊天执行者还在工作。

## 首次启动的三段完整指令

下面三段分别复制到对应新对话；以后沿用该对话只发“继续”即可。

### 宫位线

> 继续 15937-ass/ziwei-state-space 的宫位线。先读取 main 上的 CHATGPT_START_HERE.md，按标准恢复顺序读取 governance/THREE_STREAM_START_HERE.md 的宫位安排，核对实时任务和旧对话交接。接续一个已获准、可执行的宫位工作单元，遵守一次一个宫位；每轮完成到可恢复检查点，写回 Issue/PR，结束时用中文汇报三线状态和下次继续的位置。

### Core线

> 继续 15937-ass/ziwei-state-space 的Core线。先读取 main 上的 CHATGPT_START_HERE.md，按标准恢复顺序读取 governance/THREE_STREAM_START_HERE.md、governance/CORE_PRODUCT_CONTINUATION_PLAN_v1.md 和 Core plan pointer #901，核对实时 Core Issue/PR 与旧对话交接。若已有 ACTIVE Core 单则接续；若 Core 槽位空闲则直接领取计划中最早可执行的 bounded nominee（当前首单 #898），无需让我重述顺序。每轮只推进一个 Core 工作单元，遇到计划规定的真实 Human Gate 才停下来给中文原文依据和例子，结束时汇报三线状态和下次继续的位置。

### 产品线

> 继续 15937-ass/ziwei-state-space 的产品线。先读取 main 上的 CHATGPT_START_HERE.md，按标准恢复顺序读取 governance/THREE_STREAM_START_HERE.md、governance/CORE_PRODUCT_CONTINUATION_PLAN_v1.md 和 Product plan pointer #900，核对实时 Product Issue/PR 与旧对话交接。若已有 ACTIVE Product 单则接续；若 Product 槽位空闲则直接领取计划中最早可执行的 bounded nominee（当前首单 #897），无需让我重述顺序。Product 只消费正式接受且 pin 住的 Knowledge/Core checkpoint，不跟随未合并分支；每轮写回可恢复检查点，遇到计划规定的 Human Gate 才停下来，结束时汇报三线状态和下次继续的位置。

若只想看进度，发“查看三线状态”：只读核对实时宫位、Core、Product 及 main，给一个优先建议，不领取新任务。

## 执行者每轮如何接手

1. 先按 PROJECT_STATE.yaml -> CHATGPT_START_HERE.md -> governance/RECOVERY_PRECEDENCE_v1.md 恢复，再读所选工作线/分片缓存、实时 Issue、关联 PR 和最近交接。本文中的“先读取启动文件”是入口指路，不改变标准恢复优先级。
2. 先找已存在的有界任务，不能因 YAML 写着没有活动任务就重复建单。确认原执行者已停止/显式交接；若原对话仍在执行，新对话仅只读报告。交接不明确时不猜测领取写入权，先解决执行归属。Issue 评论、时间戳不是原子锁，也不能保证两个新对话同时领取时自动互斥。
3. “继续”授权恢复既有安排内的一轮工作，不自动批准新的语义、运行权限或优先级变更。对 Core/Product，PI 已通过 governance/CORE_PRODUCT_CONTINUATION_PLAN_v1.md 授权：若该线无 ACTIVE 单且槽位/依赖满足，可在这个新执行回合直接领取 plan pointer #901/#900 中最早可执行的 bounded nominee，无需再次向 PI 询问顺序。完成本轮后仍不要在同一回合自动执行下一个 Issue；先留下下一 nominee/交接，由后续“继续”回合领取。宫位线维持既有逐宫规则。
4. 只写自己的工作线与已登记分片路径；只读取正式接受的 main 成果作为正式输入。共享语义归 Core，宫位不跨线补定义，Product 不猜造知识。
5. 各线在 ACTIVE_BUILD 阶段独立准备并运行本线有界/相关检查；内容完成后进入 READY_TO_INTEGRATE，并在 Issue #888 排队。只有取得 Integration Lease 的工作单才进入 INTEGRATING：此时重核 main/base/head、同步一次当前 main、运行最终 exact-head 全量门并立即合入/释放。别的线在 lease 被占用时仍可继续工作，只是不能同时改 main。正式集成按依赖和验证就绪程度选择，不固定为“宫位 -> Core -> 产品”轮转；旧绿灯在 main 变化后仍不能直接沿用。
6. 停止前按 AGENT_WORKFLOW.md §§10.3、13 在现有 Issue/PR 留下版本、产物、已做/未做、疑点、执行归属、验证和精确下一步。用中文回答三条线各自能做什么、等什么；最多推荐一个近期集成候选。禁止只把关键安排留在聊天中。

## 后续工作的依赖顺序

以下是规划，不是新增工作单的启动或语义批准。每一步先核对现有后续单元与决定，复用交付，不能机械重做。

### 宫位：按原逐宫安排继续

- 先接当前已准入宫位。现行顺序和阶段退出条件在 [逐宫审计安排](PALACE_AUDIT_SEQUENCE_2026-10-23.md)；一次只准入一个宫位审计/映射单元。
- 当前批次结束不代表整宫结束。按来源覆盖、剩余疑点和阶段交接决定何时换宫，不能只看条目数。
- WP06C 正式映射同时等待：相关 Core 正式契约与节点 ID 已被接受、来源审查足够、该宫位轮到且槽位空闲。候选索引和正式映射是两种交付。
- 若希望提前插入事业宫映射，先记录并取得 PI 的优先级调整；不要在财帛宫工作仍准入时另开事业宫任务。

### Core：连续 canonical mapping -> schema stability -> real blocker

详细权威顺序见 [Core + Product Continuous Progression Plan v1](CORE_PRODUCT_CONTINUATION_PLAN_v1.md) 与常驻 plan pointer #901；实时 bounded Issue/PR 仍优先。

- **当前首单：#898。** 从已接受的 3 KMN / 3 KMM 开始，每批通常扩展 4–8 个 source-backed canonical mappings，只创建必要的来源支持 child KMN。
- **C1 milestone：约 15–30 KMM / 6–10 种语义结构。** 跨批覆盖 process、state、scene/context、relationship、conditional outcome、multiple antecedents、cross-palace dependency、temporal/dynamic、modifier interaction、unresolved semantics；不为凑类别强行晋升材料。
- Product 可同时消费旧 checkpoint。Product 报 `GAP_PRODUCT` 时 Core 不改；真正 `GAP_CORE` 才转成有界共享语义 gap；source ambiguity 可安全 HOLD 时继续 fail-closed，不强制解释。
- 达到 C1 milestone 后先做 schema stability/refinement review，不继续盲目堆 mapping。若稳定，再让 Product 扩大 crosswalk。
- 后续只从真实 blocker 中选择：Product-raised Core gap、宫位 `KNOWLEDGE_CORE_GAP`、真正阻塞 N -> E -> tau -> M0 的 WP07B 时间反应 gap。
- Core WIP 永远 1。普通来源支持 child node/mapping 可自动推进；universal root/family/shared primitive、不可保留 UNKNOWN 的传统语义冲突、流派/来源意义改变、probability/causal、Product/runtime 授权才停给 PI。
- 已完成的十四主星基础性质研究不因“继续 Core”自动重开。

### 产品：crosswalk pilot -> expanded checkpoint -> adapter freeze -> candidate KIB -> separate promotion

详细权威顺序见 [Core + Product Continuous Progression Plan v1](CORE_PRODUCT_CONTINUATION_PLAN_v1.md) 与常驻 plan pointer #900；实时 bounded Issue/PR 仍优先。

- **当前首单：#897。** 固定消费已接受 KMN-000001..000003 / KMM-000001..000003，做 Knowledge -> Product manifestation adapter/crosswalk pilot；不等待 Core 后续扩展。
- 每个字段只允许标为 `DIRECT / LOSSY / GAP_PRODUCT / GAP_CORE / HOLD`，不能把 UNKNOWN/conflict 偷换成 Product 值。
- 三个必测边界：KMM-000001 火铃 BOTH/EITHER 未决必须 HOLD；KMM-000002 `勉强求变` 现实前提不能从命盘推断；KMM-000003 只测试 scene/context 安全映射并保留“不是个人伤病/诊断/治疗”的负边界。
- P1 不填生产 manifestation registry、不 promote active KIB/K_manifest、不授权 runtime、不引入概率或预测有效性。
- Core 接受更大 checkpoint 后进入 P2 expanded-checkpoint pilot；Product pin 新 accepted checkpoint，而不是实时追 Core 分支。
- 至少两个 checkpoint 显示字段行为稳定后才进入 P3 正式 adapter/crosswalk freeze；之后 P4 才做 candidate K_manifest/KIB + semantic impact；P5 promotion 必须另开明确 Product 单。
- Knowledge merge 永远不自动刷新 active Product lock。等待 Core 时只做已经授权且独立的 Product 工作；没有合适工作就空槽，不造 filler。
- Product WIP 永远 1。重大 Product 架构边界、超出计划的 runtime/promotion、probability/causal 或试图改 canonical Knowledge 才停给 PI。

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

日常进度只写所属 Issue/PR 及其版本化证据，不为更新此导航快照而跨线改文件。只有入口或安排确需修改时才走独立有界 Governance 任务。回滚本次两份文档改动即可撤销入口，原三线成果与语义不受影响。

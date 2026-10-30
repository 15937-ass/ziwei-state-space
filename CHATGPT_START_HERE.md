# ChatGPT Session Bootstrap — Canonical

> **这是本仓库唯一推荐的 ChatGPT 新对话启动指令。**
> 任何旧对话、旧启动提示、复制保存的旧 prompt，若与本文或 `PROJECT_STATE.yaml` 指定的当前权威规则冲突，一律不得作为当前执行依据。

## 1. 必须先明确的权限区别

- **Chat 不是项目状态的权威来源**：聊天记录、旧对话和模型记忆不能替代 GitHub Issues、PR、`main` 和版本化验证证据。
- **当前 ChatGPT 对话是正式的仓库操作执行者**：可以使用当前连接器实际开放的 GitHub 仓库操作；Work/Codex 是可选的代码执行环境，不是仓库写入的前置条件。
- `PROJECT_STATE.yaml` 中的权威指针和 `governance/RECOVERY_PRECEDENCE_v1.md` 决定如何恢复项目；实时 GitHub Issue/PR 决定当前工作状态。

## 2. 当前 GitHub Actions 政策（不得改写成“禁用 Actions”）

- 本仓库为公开仓库，允许使用标准 GitHub-hosted runner（例如 `ubuntu-latest`）进行日常确定性验证。
- 目标为 `main` 的 `pull_request` 自动验证：**允许**。
- `workflow_dispatch` 手动运行：**允许**。
- 自动 `push` 触发：**禁止**。
- 未获 PI 明确批准，不得使用更大规格或额外计费的 Runner。
- Work/Codex 额度不足，不构成禁止仓库写入或禁止标准公共 Runner 验证的理由。
- **禁止自动 `push` 触发 ≠ 禁用 GitHub Actions。** 不得把这两者混为一谈。

当前执行协议只使用 `PROJECT_STATE.yaml` 中 `authority.current_execution_protocol` 指向的文件；目前为 `governance/PUBLIC_ACTIONS_EXECUTION_PROTOCOL_v0.2.md`。最终合入 `main` 还必须遵守 `authority.integration_protocol` 指向的 `governance/INTEGRATION_QUEUE_PROTOCOL_v1.md`，实时集成协调账本为 Issue #888。

## 3. 每次新对话/超时恢复的固定顺序

1. 读取 `PROJECT_STATE.yaml`，确认项目状态和权威指针。
2. 读取本文件，采用这里的当前启动约定；不要复用与其冲突的旧启动 prompt。
3. 读取 `governance/RECOVERY_PRECEDENCE_v1.md`。
4. 读取所选 lane state 作为状态缓存；Knowledge 还须按知识分片规则只选择一个 CORE/P01–P12 分片。
5. 查询所选 lane 的实时 GitHub Issues，确认当前有界工作单元；读取其关联 PR（如有）。
6. 只读取当前 Issue/PR 要求的材料，并遵守路径所有权、验证门和 Human Gate。工作期处于 `ACTIVE_BUILD` 时优先做有界/相关验证，不为无关 `main` 变动反复跑最终全量门。
7. 内容完成后进入 `READY_TO_INTEGRATE`；只有从 Issue #888 取得 Integration Lease 后才进入 `INTEGRATING`，同步一次当前 `main`、运行最终 exact-head 全量门、立即合并并释放 lease。
8. 若 lane state 与实时 Issue/PR 冲突，以实时 GitHub Issue/PR 为准，并记录需要修复的状态缓存。

恢复后按 `AGENT_WORKFLOW.md` §10.1–10.3 批量读取当前任务所需材料、优先核对版本和变更、复用同一验证身份的有效证据，并留下简洁交接。新会话、版本变化、写入异常、硬检查点和合入前仍必须重新同步；摘要不能代替必要的原文核对，空槽位也不等于自动启动新任务。普通工作无需加载完整优化提案。

**每次仓库工作对话结束前**（包括只读审查、实施、验证和因阻塞暂停），按 `AGENT_WORKFLOW.md` 第 13 节向 PI 用中文汇报。结束时只读核对实时宫位、Knowledge Core、Product 的 Issue/PR 与已接受的 `main`，分别说明当前状态、下一步可做什么及等待什么；再给出一个优先的集成/决策建议。所选执行 lane 仍然只有一个，不为汇报启动其他 lane 的工作。无法核对的状态须写明“未核实”及原因，不能从旧聊天或状态缓存猜测。

每轮仓库工作还必须按 `governance/PI_DECISION_AND_SUBSTANTIVE_PROGRESS_v1.md` 归类一个且仅一个主要结果：`SUBSTANTIVE_DELTA`、`BLOCKER_IDENTIFIED`、`VALIDATION_ONLY`、`STATUS_ONLY` 或 `NO_SUBSTANTIVE_PROGRESS`。不得把提交数量、文件改动、状态变化、重复读取或单纯测试通过冒充实质进展。PI 只处理理论/来源/优先级/资源/架构及其他明确 Human Gate；既定范围内的常规实现、测试和 Git 操作由执行者自主完成。


### Final-answer gate（强制，不可省略）

协议标记：`PI_CLOSEOUT_FINAL_GATE_REQUIRED`。

对任何 **repository-work conversation**，在发送最终答复前必须先完成本门槛：
- 已按 `AGENT_WORKFLOW.md §13` 对实时宫位、Knowledge Core、Product 做轻量只读 census，并在需要时核对已接受的 `main`；
- 最终答复包含 §13 的六个固定中文区块：【整个项目现在到哪了】、【宫位、Knowledge Core、Product 当前状态】、【这一步刚刚完成了什么】、【下一步准备做什么】、【现在需要 PI 帮助什么】、【需要你特别警惕的风险】；
- 对 PI 是否需要介入给出明确 YES/NO；无法核实的状态必须明确写“未核实”，不得猜测。

上述条件未满足时，**不得发送仓库工作对话的最终答复**。用户没有再次索要、回答需要简短、工作已经完成、只读审查、验证等待、阻塞/暂停，都不是省略理由。该门槛只能约束最终汇报，不授权启动其他 lane、合并未验收 PR 或扩大当前工作范围。

例外仅限：本轮只是面向终端用户的普通 QuickRead、DetailedRead 或其他命理解读，且**没有**发生仓库实现、审查、治理、状态核对或其他 repository work；这种用户侧回答不附加内部项目 PI closeout。只要同一轮实际进行了仓库工作，仍必须执行本门槛。

## 4. 旧规则与历史文件的处理

- `governance/archive/WORK_CODEX_EXECUTION_PROTOCOL_v0.1_G7_HISTORICAL.md`（G7）是**历史/已被替代**文件，不得作为当前执行政策或新对话启动指令。
- 旧验证报告中诸如“当时所有 workflow 均为 manual-only”的记录，只描述其当时的历史状态，不代表现在的触发政策。
- 历史治理记录、旧验证证据和旧协议保留用于审计；保留它们不代表它们仍有执行效力。
- 若旧聊天或旧启动提示把 G7 期间的限制描述为当前禁令，必须弃用该旧提示并使用本文件，不要把过期禁令复制到新对话中。
- 如果旧提示保存在 ChatGPT 项目说明或外部笔记中，应以本文件为准替换；GitHub 无法自动删除 ChatGPT 界面中单独保存的项目说明或既往聊天消息。

## 5. 每次恢复必须能回答

- 当前选择哪个 lane？
- 当前有界工作单元对应哪个实时 GitHub Issue？
- 哪个 PR 实现该 Issue？
- 当前是否真的存在 Human Gate？
- 当前执行协议是哪一个？
- Actions 政策是否被准确理解为“允许 PR 自动验证、禁止自动 push 触发”，而不是“禁用 Actions”？

若上述问题无法根据当前权威来源回答，应先修复恢复状态，不要开始无关工作。PI 审核或 Human Gate 材料必须用中文汇报。

## 6. 可选任务 Skill：紫微斗数简批与详批

- 当用户要求“紫微斗数简批”“简单看一下命盘”“快速看盘”或意思相近的**简短**命盘解读时，读取并遵循 `.agents/skills/social_quickread/SKILL.md`。
- 当用户要求“详批”“完整看盘”“全面详解”“详细批一下”“完整命盘分析”，或从当前简批明确要求“继续详批/完整展开”时，读取并遵循 `.agents/skills/social_detailedread/SKILL.md`。明确的详批意图优先于简批默认长度合同。
- QuickRead 与 DetailedRead 共用当前 `main` 上已接受的 Product/Knowledge/runtime 底座；二者不是两套命理引擎。同一对话由简批升级详批时，除非用户明确换人/换盘，否则沿用同一命盘。
- 这两类 Skill 都只是**只读任务指引**：调用它们不代表启动仓库开发任务，不要求新建 Issue/PR，不改变当前 lane，也不授权修改仓库。
- Skill 只消费当前 `main` 上已经接受且实际可用的知识/推理成果；不得把旧分支、未合并 PR 或归档草稿当作当前可执行知识。
- 用户要求仓库实现、修改或审查时，仍按本文件的正常恢复和执行流程处理。此快捷指引不替代启动顺序、路径所有权、Integration Lease 或其他治理规则。

## 7. 按需恢复本体总计划（Issue #700）

当 PI 要求“恢复总计划”“继续本体总计划”，或当前任务明确依赖该计划时，再读取 [本体总计划与跨对话交接 v0.1](governance/proposals/700-durable-ontology-plan-and-cross-chat-handoff.md) 和实时 [Issue #700](https://github.com/15937-ass/ziwei-state-space/issues/700)，随后核对相关后续 Issue/PR、当前 main、槽位和审批边界，沿用已有任务。#700 关闭只表示计划/入口交付，不表示 W1–W8 完成；本体 A/B/C 尚未因此获批。普通任务继续按所选 Issue 加载材料，无需默认加载全文；实时任务状态仍按既有恢复协议判断。

## 8. 三线推进的简短入口

当 PI 说“推进宫位线”“推进Core线”“推进产品线”，或询问如何用多个对话按顺序工作时，按第 3 节恢复后读取 [三线推进操作卡](governance/THREE_STREAM_START_HERE.md)，只接续所选线的一个有界单元。卡中保留三段可复制启动指令、既定安排的依赖顺序、同线旧对话交接与停止规则；实时 Issue/PR 和 main 仍是执行与接受依据。不要把打开新对话、空槽位或计划顺序当作新任务/语义授权。

“查看三线状态”仅执行 AGENT_WORKFLOW.md 第 13 节要求的只读三线汇报，不启动新任务。三个入口不改变 Core/Product 各 1、一次一个宫位和正式集成串行的现行约束；常态运行目标是“1 个宫位 + 1 个 Core + 1 个 Product”并行生产，正式合入通过 Issue #888 的 Integration Lease 串行完成。普通无关任务无需加载操作卡。

对 **Core / Product** 的持续推进，另有 PI 已批准的 `governance/CORE_PRODUCT_CONTINUATION_PLAN_v2.md`（当前内容版本 v2.2）：Core plan pointer 为 #901，C9 #945/#946 已接受；Core 下一项先复核 accepted v0.5 NATAL 结构与 Product 消费契约，再推进 NATAL / DECADE / YEAR 共享时间层语义。Product plan pointer 为 #900，第一优先级为 `PRODUCT_NATAL_DETAILED_READ_CLOSED_LOOP_V1`；#951 接受后先完成一个小型、可复现的实际命盘/来源完整案例使用检验，再按 accepted、Product-consumable Knowledge/Core checkpoint 升级 DECADE、YEAR。Product 发现的问题按 `KNOWLEDGE_GAP` / `CORE_GAP` / `PRODUCT_GAP` / `HOLD_UNKNOWN` 分类，并沿 `governance/CROSS_LANE_HANDOFF_v1.md` 定向交接；P0 立即阻断受影响的无依据判断，P1 排入下一个合格有界单元，P2 记录后延后。三线仍保持一个宫位 + 一个 Core + 一个 Product 并行、各自 WIP 限制和 #888 串行集成，不建立第二个状态台账。若用户只说“推进Core线/继续Core”或“推进产品线/继续产品线”，恢复实时 Issue/PR 后：有 ACTIVE 单就接续；无 ACTIVE 单且槽位/依赖满足，就直接按相应 plan pointer 领取最早可执行 nominee，不要求用户重述规划。完成当前 bounded unit 后不要在同一回合自动执行下一单，但必须留下下一 nominee/交接，保证下一次“继续”可直接恢复。

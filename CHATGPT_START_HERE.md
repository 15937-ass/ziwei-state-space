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

当前执行协议只使用 `PROJECT_STATE.yaml` 中 `authority.current_execution_protocol` 指向的文件；目前为 `governance/PUBLIC_ACTIONS_EXECUTION_PROTOCOL_v0.2.md`。

## 3. 每次新对话/超时恢复的固定顺序

1. 读取 `PROJECT_STATE.yaml`，确认项目状态和权威指针。
2. 读取本文件，采用这里的当前启动约定；不要复用与其冲突的旧启动 prompt。
3. 读取 `governance/RECOVERY_PRECEDENCE_v1.md`。
4. 读取所选 lane state 作为状态缓存；Knowledge 还须按知识分片规则只选择一个 CORE/P01–P12 分片。
5. 查询所选 lane 的实时 GitHub Issues，确认当前有界工作单元；读取其关联 PR（如有）。
6. 只读取当前 Issue/PR 要求的材料，并遵守路径所有权、验证门、Human Gate 和 `Issue -> branch -> PR -> validation -> merge` 流程。
7. 若 lane state 与实时 Issue/PR 冲突，以实时 GitHub Issue/PR 为准，并记录需要修复的状态缓存。

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

## 6. 可选任务 Skill：紫微斗数简批

- 当用户要求“紫微斗数简批”“简单看一下命盘”“快速看盘”或意思相近的简短命盘解读时，读取并遵循 `.agents/skills/social_quickread/SKILL.md`。
- 这只是一个**只读任务指引**：调用它不代表启动仓库开发任务，不要求新建 Issue/PR，不改变当前 lane，也不授权修改仓库。
- Skill 只消费当前 `main` 上已经接受且实际可用的知识/推理成果；不得把旧分支、未合并 PR 或归档草稿当作当前可执行知识。
- 用户要求仓库实现、修改或审查时，仍按本文件的正常恢复和执行流程处理。此快捷指引不替代启动顺序、路径所有权或其他治理规则。

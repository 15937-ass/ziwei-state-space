# 三线推进操作卡（v2.2）— 精简索引（可选，不是默认上下文）

> 本文件只用于 PI 明确要求继续某条线时定位入口。普通对话、普通仓库任务和命理解读都不需要读取本文件。

## 共同规则

- 当前对话中的 PI 明确指令决定本轮目标、优先级和停止条件。
- 一轮只处理一条线、一个有界任务；不自动扩展、不自动接续下一单。
- 宫位一次一个宫位；不得增加宫位槽位，不得启用 P06 #773 作为第二槽。
- live Issue/PR 决定执行状态，accepted main 才是正式成果；状态 YAML 只是缓存。
- 不做全局三线盘点，除非 PI 明确要求或确有跨线依赖。
- 正式合并仍须遵守 Issue #888 Integration Lease 和 exact-head 验收。
- 所有后台自主执行代理已暂停；GitHub Actions 仅用于确定性 PR 验证。

## 三条线的唯一入口

| PI 指令 | 只需读取 | 边界 |
| --- | --- | --- |
| 推进宫位线 | 当前 palace live Issue/PR；无活动单时才读 #676 和宫位顺序文件 | 一次一个宫位；只写当前宫位分片 |
| 推进 Core 线 | Core live Issue/PR；无活动单时才读 #901 与 CORE_PRODUCT_CONTINUATION_PLAN_v2.md | Core WIP <= 1；只做共享语义 |
| 推进产品线 | Product live Issue/PR；无活动单时才读 #900 与 CORE_PRODUCT_CONTINUATION_PLAN_v2.md | Product WIP <= 1；路线为 NATAL → DECADE → YEAR |

## 停止与汇报

完成当前任务后，记录必要交接并简洁汇报结果、验证、阻塞和一个必要的下一步，然后停止。不要为了交接复制整份路线图，不要在一个对话里同时推进多条线。

本索引不是任务队列、语义授权或状态台账。具体顺序、Human Gate、来源边界和消费许可，以当前 PI 指令、正式批准决定、live Issue/PR 与 accepted main 为准。


## 已批准路线的最小恢复提示

- Core plan pointer #901；C9 #945/#946 已接受。Core 只处理共享语义，WIP <= 1。
- Product plan pointer #900；首个闭环为 PRODUCT_NATAL_DETAILED_READ_CLOSED_LOOP_V1，先做实际命盘使用检验，再按证据准入 DECADE、YEAR。
- Product-availability note：只消费 accepted main 且明确允许 Product 使用的材料；未合并分支不是正式输入。
- 反馈分类：KNOWLEDGE_GAP / CORE_GAP / PRODUCT_GAP / HOLD_UNKNOWN。
- PI 已批准的 NATAL → DECADE → YEAR 顺序无需让我重述顺序；仍须遵守当前 live Issue/PR 和单任务停止规则。

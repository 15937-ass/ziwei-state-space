# Gate A2（Canonical）：时序记忆与获得性状态架构审计

状态：**READY FOR PI REVIEW — 未批准**  
前置 Gate：A0 APPROVED；A1 APPROVED  
当前执行状态：**FROZEN_FOR_GATE_A2**

> 本文件是 Gate A2 的唯一 canonical 人工审核入口。  
> 以下两个文件保留为历史审计记录，不再作为当前 Gate 入口：
> - `GATE_A2_路径依赖与获得性状态审计.md`
> - `GATE_A2_时序记忆与获得性状态.md`

## 1. 触发原因

LB-06 source-span review 确认 3 条 source-supported path-dependence rules：

- `ZZ-SYS-31-033`
- `ZZ-SYS-38-034`
- `ZZ-SYS-41-023`

其共同结构为：

```text
当前运限
-> 当期反应
-> 形成 / 强化 / 固化后天状态
-> 改变后续运限反应
```

这类规则无法由当前近似 memoryless 的 G5 主结构
`fixed natal essence E + current temporal input -> reaction`
完整表达。

## 2. 当前冻结边界

在 PI 明确批准 A2 之前：

- 不修改 G5 核心状态结构；
- 不把 3 条 architecture-hold 规则纳入 ordinary effective inference；
- 不把 45 条 history-marker heuristic candidates 自动转换为状态更新；
- 不继续 architecture-sensitive 的 LB-07 ... LB-16 migration；
- 不新增任意连续记忆权重、衰减率、学习率或一般神经网络递归。

允许继续的仅是：

- 仓库维护；
- provenance / metadata 修复；
- deterministic lint / test 修复；
- 不改变理论含义的文档归一化。

## 3. A2 最小提案

保留：

```text
E = fixed natal essence
```

新增独立的获得性历史状态：

```text
m_t = acquired / history state
```

当前反应：

```text
r_t = R(E, m_t, u_t, z_t, G_t, c_t)
```

只有 source-explicit persistence/path-dependence rule 才允许：

```text
m_(t+1) = M_source_gated(m_t, r_t, u_t)
```

否则：

```text
m_(t+1) = m_t
```

Paper 1 只允许 symbolic / ordinal / source-gated 的获得性状态更新。一般连续递归
`x_(t+1)=F_theta(...)`
继续保留为 Paper 2+ hypothesis。

## 4. 术语归一化

历史 A2 草案曾分别使用 `A_t` 与 `m_t` 指代同一类“后天获得性 / 历史依赖状态”。

为避免 Agent 分叉，本 canonical Gate 统一使用：

`m_t = acquired_history_state`

旧文档中的 `A_t` 仅作为历史草案别名，不代表第二套状态对象。

## 5. 已确认与未确认的证据

已确认 architecture trigger：

- `ZZ-SYS-31-033`
- `ZZ-SYS-38-034`
- `ZZ-SYS-41-023`

此前 source-reviewed、具有同类路径依赖意味的规则还包括：

- `ZZ-SYS-30-033`
- `ZZ-SYS-31-020`

全 corpus deterministic marker scan：

- heuristic candidates：45
- high-priority history review：27
- sequence-only review：18

注意：45 条只是待回源候选，不等于 45 条已确认 HistoryUpdate。

## 6. PI 需要审核的五项

### A2-1
是否批准新增独立于固定原局本质 `E` 的 `acquired_history_state m_t`。

### A2-2
是否批准只有 source-explicit persistence / path-dependence 规则才能更新 `m_t`。

### A2-3
是否批准 Paper 1 只实现 symbolic / ordinal history update，不引入任意连续记忆权重、衰减率或学习参数。

### A2-4
是否批准一般连续递归动力学继续作为 Paper 2+ hypothesis，而不把其声称为中州派原文定律。

### A2-5
是否批准 A2 后执行全文 history-marker backward audit，并将当前 3 条 held rules 转为第一批 HistoryUpdate 模板。

## 7. A2 批准后的自动路线

```text
A2 approval
-> D-016
-> HISTORY_UPDATE_SCHEMA v0.1
-> G5-R state-space revision
-> model_spec acquired-history objects
-> migrate 3 held rules
-> backward audit all 2193 system rules
-> source-review persistence candidates
-> ontology / system-mode regression
-> resume LB-07 ... LB-16
```

如全文反扫进一步要求重写 natal essence、引入多宫长期状态传播，或出现第二时间尺度以上的新结构，再升级新的人工 Gate。

## 8. 当前唯一合法下一步

在没有 PI 明确回复“批准 A2”之前，**不得进入 A2 后自动路线**。

仓库状态以根目录 `PROJECT_STATE.yaml` 为启动入口。

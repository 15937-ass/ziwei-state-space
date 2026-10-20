# Proposal #374 — Conversation repository authority

Status: **IMPLEMENTED BY PR #377**  
Tracking Issue: #374  
Risk: R3 / Human Gate

## Motivation

PI 要求普通 ChatGPT 对话模式本身成为完整仓库执行者，不再因为不是 Work/Codex 而被限制为 bounded edits。

## Goals

- 当前对话可使用 connector 实际暴露的全部 GitHub 仓库操作能力。
- repository write 不再专属于 Work/Codex。
- 保留 GitHub 作为项目 canonical state。
- 保留 Issue-first、lane、PR、validation、Human Gate 和 source-integrity 边界。

## Non-Goals

- 不取消 Human Gate 或 lane/path ownership。
- 不授权未验证内容绕过 PR gate 直接进入 main。
- 不把 connector 未暴露的 API 说成已经技术可用。
- 不改变中州派 canonical meaning、概率/因果语义或 Product maturity。

## Current Problem

G7 把仓库编辑集中到 Codex；G8 虽允许当前 session 做 GitHub edits，但仍写成 bounded。该定义会使普通对话模式在 Work/Codex 不可用时被错误降格。

## Proposed Design

当前 ChatGPT conversation/session 定义为 **first-class repository operator**，可直接使用 connected tools 暴露的所有 GitHub repository operations，包括 file create/update/delete、branch、Issue、PR、review/comment、draft/ready、merge/auto-merge、workflow/run 以及其他实际可用的仓库管理动作。

这是操作能力授权，不是语义越权授权。正常流程仍为：

`Issue -> branch -> PR -> validation -> merge`

Work/Codex 仍可承担 shell/coding runtime；G8 public Actions 仍可承担 deterministic Python/Node/Go validation。它们不再是 GitHub repository write 的必要前置条件。

## Alternatives

- **只改 G7**：拒绝；G7 已被 G8 supersede，单改历史文件不会改变当前有效协议。
- **取消 lane/Human Gate**：拒绝；这超出 PI 本次授权。
- **继续让 Work/Codex 独占写权限**：拒绝；与 PI 当前要求冲突。

## Compatibility

兼容 G8 public Actions。runner/cost policy 不变；只修改 repository operator authority。

## Knowledge Impact

无 canonical 紫微知识语义变化。

## Product Impact

无 Product runtime 或 inference semantics 变化。

## Risks and Failure Modes

- 把“完整仓库权限”误解为“可以绕过治理”。
- 有 merge 能力后过早合并未验证 PR。
- 混淆治理授权与 connector 实际 API scope。

控制方式：保留 lane、Issue-first、PR、validation、Human Gate；connector/tool surface 是技术上限。

## Test Plan

- governance contract tests 检查 full repository authority 文本；
- 检查 G7 historical 状态；
- 检查正常 PR discipline 仍存在；
- governance validator；
- scope inspection 确认没有 Product/Knowledge semantic changes。

## Migration Plan

同一 Governance PR 修改：
- G7 historical status；
- G8 active authority split；
- AGENT_WORKFLOW；
- GOVERNANCE_STATE；
- governance tests；
- 本 Proposal。

## Rollback Plan

回滚实施 PR，恢复 G8 的 bounded GitHub edits 描述。

## Graduation Criteria

- 当前对话被 active protocol 明确定义为 first-class repository operator；
- G7 不再被误读为 active execution contract；
- connector scope ceiling 明确；
- lane/Human Gate/PR/validation 边界仍明确；
- governance validation 通过并合并。

## Human Gate

PI 已在当前对话明确批准：对话模式可以完全使用仓库的所有权限。

该批准解释为：**可以使用所有 connector 实际暴露的 repository permissions，但不自动取消更高层研究治理约束。**

## Decision

**APPROVED.**

由于 G7 已被 G8 supersede，本次实施同时修正 G7 历史状态并修改当前有效 G8 authority split。

## Implementation History

- 2026-10-20：Issue #374 建立；PI 指令构成 R3 Human Gate 批准。
- 2026-10-20：实施分支更新 G7、G8、AGENT_WORKFLOW、GOVERNANCE_STATE 和 governance tests。
- 2026-10-20：PR #377 通过 repository quality gate 后作为本 Proposal 的实施 PR 合并。

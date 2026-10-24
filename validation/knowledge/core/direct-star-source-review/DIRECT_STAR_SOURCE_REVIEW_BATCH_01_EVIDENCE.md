# DIRECT_STAR 来源优先审查 — 验收证据

状态：`PROPOSAL_ONLY_NOT_CANONICAL`

- Issue：[#720](https://github.com/15937-ass/ziwei-state-space/issues/720)
- 工作单元：`KB-CORE-DIRECT-STAR-SOURCE-REVIEW-BATCH-01`
- 激活 main / 初始 base：`75770dad05e93c61ccbf769d361db5f1536f8697`
- 工作分支：`knowledge/core-720-direct-star-source-review-batch-01`
- 规则行级表：`knowledge/core/direct-star-source-review/DIRECT_STAR_SOURCE_REVIEW_BATCH_01_v0.1.csv`
- 审查报告：`knowledge/core/direct-star-source-review/DIRECT_STAR_SOURCE_REVIEW_BATCH_01_v0.1.md`
- 测试：`tests/test_knowledge_core_direct_star_source_review_batch_01.py`

## 来源审计

- 目标覆盖：33 个唯一 rule ID；每条一行，无重复 ID。
- `SRC-ZZ-002` 的本地 PDF SHA-256 与 `sources/source_index.csv` 一致：`1cd57c205297f78004c0d59db7cb77b05ecad53313757e55d8f1c78600609e9a`。
- `SRC-ZZ-001` 的本地 PDF SHA-256 与 `sources/source_index.csv` 一致：`7ebafc8e3477430e2f8e69c6925ecc373d3c28966955f7035078c4949b7475a2`。
- 来源清点：`SRC-ZZ-002` 30 条规则，`SRC-ZZ-001` 3 条规则；合计 33 个唯一 rule ID。
- 本轮逐项核对了来源扫描页；CSV 记录 PDF 扫描页、印刷页、简短原文片段及对应气核引用位置。
- 本轮没有修改 canonical source CSV 中的 `source_span_verified=false`，也没有修改 `normalization_epistemic=UNRESOLVED`。
- 行级 CSV 单独保留 canonical `source_epistemic=EXPLICIT`、原始条件/时间/宫位/前置规则/排除/冲突字段，以及 canonical source-span 原值 `false`；研究审查的视觉核对状态不会覆盖这些 canonical 字段。- 本轮没有修改 canonical source CSV 中的 `source_span_verified=false`，也没有修改 `normalization_epistemic=UNRESOLVED`。

## 验收边界

- 所有交付物保持 `PROPOSAL_ONLY_NOT_CANONICAL`。
- 没有修改 `knowledge/star_cores.yaml`、`knowledge/qi_ontology.yaml`、`knowledge/star_systems.yaml`、canonical source CSV、source registry、Product 文件、runtime、registries、locks 或其他宫位文件。
- 没有新增或接受 QI/QR primitive / mapping，没有 Product consumption authorization，没有概率或经验预测有效性主张。
- `ZZ-TY-010` / `ZZ-TY-X02` 的原文重叠和 `ZZ-WQ-004` 的多处气核引用均明确保留；统计按唯一规则 ID，而非引用次数。

## 验证状态

### 已完成的 exact-head 验证快照

- Base：`main @ 75770dad05e93c61ccbf769d361db5f1536f8697`。
- Head：`3959d79ff80fe2beec8d062b9665b6857082405d`。
- GitHub Actions：[`repository-quality-gate` run #40052144239](https://github.com/15937-ass/ziwei-state-space/actions/runs/40052144239) — **PASS**。
- 全仓 pytest：**2658 passed，132 subtests passed，312.19 秒**。
- Product JS adapter syntax：**PASS**。
- deterministic P0 repository gate：**PASS**（命令成功退出）。
- Repository Governance v1：**PASS**（日志明确输出 Governance validation passed）。

### 版本化说明

本快照记录的是上面明确标出的 base/head 和对应 run。把验证结果写入本文件会生成新的 PR head，因此该新 head 必须再跑一次完整 gate。为避免每次把最终 run 写回同一个文件而无限制造新 head，第二次 exact-head run 的 SHA 与 workflow run 将记录在 live Issue #720 / PR #722；该 run 通过后不再改动本文件。最终接受状态以 live Issue / PR / GitHub Actions 为准，不从旧绿 CI 推断。

## 解释限制

本审查验证的是来源片段与研究分类的可追溯性，不证明星性分类的历史唯一性，不证明 QI/QR 映射正确，不证明十四主星性质空间完备，也不证明现实预测有效。所有概率状态为 `UNKNOWN`；Product/runtime 消费未授权。

## Current mainline resynchronization

- The activation base for this Issue was `75770dad05e93c61ccbf769d361db5f1536f8697`; main subsequently advanced to `50e0d4d5a0c74baf522a9c5a43ec90e0142c92dd`.
- The earlier passing run #40052144239 tested head `3959d79ff80fe2beec8d062b9665b6857082405d` on the older base. It is historical evidence only and is not used as final merge authorization after main advanced.
- This branch was first replayed from main `50e0d4d5a0c74baf522a9c5a43ec90e0142c92dd`; main then advanced again to `4171b2f0cf809a98541b344fee4100a7eb63f8a0`. The branch was replayed once more from `4171b2f0cf809a98541b344fee4100a7eb63f8a0`, preserving only the four scoped research/test/evidence files in this PR. No canonical, Product/runtime, registry, lock, or state-cache paths are introduced.
- At the time this evidence update was prepared, the gate for the prior replay head `da387b024edd30423e9450905dec510abbc96b2f` was in progress. This evidence correction creates a new head and therefore requires a fresh exact-head gate. The final SHA and run will be recorded in live Issue #720 / PR #722; this file will not be edited after that run, avoiding a self-referential validation loop.

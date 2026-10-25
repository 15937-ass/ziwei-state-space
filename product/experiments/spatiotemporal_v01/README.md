# 空间—时间工程对照实验 v0.1

状态：`TEST_ONLY_NOT_CANONICAL`。跟踪 Issue #764。工作线 `PRODUCT_ONLY`，复用现有 Product 单槽；#715 / Draft PR #718 已暂停并保留 head `d8d65de57f66484652d80fa8b6bfe1ca7c919672`。Core #757 独立继续。

PI 于2026-10-25批准“产品旧任务暂停 -> 利用Product槽位开展小型工程原型”，仅批准本轮实验。未批准统一生产架构、共享语义、正式规则、知识包晋升或真实事件推断。

## 实验问题与范围

1. 同一个明确的12位置循环，索引重排与离散置换矩阵是否等价？矩阵是否值得成为执行表示？
2. 已接受的时间fixture经现有adapter输出后，能否在实验包装中保留快照、target与layer身份？
3. 未知/冲突与否定条件如何在测试策略中保持可审计？与现有bool接口有何差异？
4. 证据重放、重复执行与四化绑定是否保持边界？

没有新增生产接口。`probe.py`放在实验目录，现有`src/product/`不导入它；它只读调用现有adapter/condition compiler。该实验不能替代WP07B归一化或WP06B/C正式映射。

## 固定位置、矩阵与未知

合成坐标`i`是实验slot identity，不是某个已批准流年命宫或地支规则。正偏移k定义为源slot i移动到目标slot (i+k) mod 12；P[dest,src]=1当且仅当src=(dest-k) mod 12。只对该数学映射测试恒等、逆、组合和人工锚点。禁止从fixture的scope.index推断传统盘面映射。

0/1仅编码占位。矩阵与索引视图都从同一个`Occupancy`对象生成，状态掩码同步变换。UNKNOWN/MISSING/CONFLICT槽的0必须先经过状态检查，不是确认不存在。所有对象保持原输入不变。没有qi向量、吉凶分数或四化加法。

## 事实身份与测试策略

Scope=(snapshot_sha256,target_id,layer)。这是快照容器身份；不是已定义的历法有效区间。原始typed atom仍保留其args，layer必须等于查询scope。不同target或快照不能拼接，跨层规则在v0.1中拒绝执行。

当前已接受的`PL3T_TEMPORAL_ASSET_FIXTURE_v0.1.json`是演示fixture：natal为空，各scope只有两个位置，engine.source_revision为demo。事实视图不声明其完整性，不补成真实12宫。scope-level四化不推断star绑定；只有原星对象明确携带mutagen时保留现有adapter的直接绑定。

实验三值策略：显式正证据为TRUE，显式负证据为FALSE，二者冲突为UNKNOWN并保留CONFLICT。未见事实默认UNKNOWN；只有TEST_ONLY声明相应scope和predicate完整时才将缺席视为FALSE。AND/OR/NOT使用明确三值表，诊断不因决定性分支而丢失。这不是正式共享否定契约，也不评价生产输入是否完整。

只能执行`TEST-`规则，至少有一个条件；无规则递归、事实写回、首次/持续/再次触发。execution_id包含规则、scope、输入证据、策略与代码hash；同输入同版本得到同ID，重放须使用相同策略/代码版本。所有输出runtime_effect_allowed=false，canonical_accepted=false。

## 复现

仓库根目录：

```bash
PYTHONPATH=. python product/experiments/spatiotemporal_v01/probe.py --output /tmp/spatiotemporal-comparison.json
PYTHONPATH=. python -m pytest -q tests/test_product_spatiotemporal_probe.py
```

固定输入版本见`fixture_manifest_v0.1.json`。对照结果见`COMPARISON_REPORT_v0.1.json`与同名Markdown，实际验证见`validation/product/spatiotemporal_v01/EXECUTION_EVIDENCE.md`。不能把未运行或旧head检查记为本次PASS。

## 阶段结论与下一轮

本轮只交付工程对照。允许结论为不采用矩阵、未证明性能收益或来源不足；不为了继续架构研究创造正式规则。

以后说“继续产品线”或“继续实验线”，先按canonical bootstrap恢复实时Product Issue/PR：优先接续#764当前检查点；#715仍暂停，不能同时恢复。#764验收后停止，是否扩大实验需另选有界任务；生产迁移、共享语义及KIB接入分别审议。旧产品恢复前必须交接槽位和current-main重验。

本次不改main的三线操作卡或治理规则。WIP仍是Product 1、Core 1；新实验不是第四条长期执行线。

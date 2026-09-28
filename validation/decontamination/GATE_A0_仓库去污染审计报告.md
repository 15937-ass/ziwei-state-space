# Gate A0：仓库去污染审计报告

审计分支：`audit/decontamination-p0-v2`  
基线：`main` at A0 branch creation  
状态：**GATE A0 APPROVED / P0 SCHEMA REPAIR COMPLETE IN EFFECTIVE v0.3 VIEW**

## 一、审计目的

本轮不判断紫微斗数本身的经验有效性，也不重写 G1–G6 已冻结理论。

唯一目标是回答：

1. 当前机器可读知识库是否遵守自己的 schema；
2. “源文明确”与“模型归一化解释”是否被混为一谈；
3. `reviewed` 是否真实代表了可复核的审查层级；
4. 规则是否出现大批量 LLM 摘要化、非原子化；
5. L1/L2 状态层与 L3 输出层是否发生混层；
6. 当前 Agent / validator 是否真的执行了仓库文档宣称的审核。

## 二、当前基线数据

A0 对 main 中以下 canonical / operator 文件做了确定性扫描：

| 文件 | 记录数 |
|---|---:|
| 十四正曜 canonical | 430 |
| 六十星系 canonical | 2193 |
| 四化 operator | 56 |
| 杂曜 operator | 73 |
| 辅佐八曜 operator | 103 |
| 六煞 operator | 81 |
| 六十星系 modifier edge | 654 |

说明：edge 文件属于派生产物，本轮主要用于交叉观察，不作为源文 canonical 替代物。

## 三、P0：已确认的硬性 schema 违规

最终确认 **61 条 deterministic P0 违规**。

详细记录：

`validation/decontamination/A0_hard_schema_violations.csv`

### 3.1 六十星系 target_type 越界：59 条

`knowledge/KB_SCHEMA.md` 当前允许：

- qi_state
- relational_state
- structural_relation
- outcome_descriptor

但六十星系 canonical 实际出现：

- `inference_rule`：58 条
- `evaluation`：1 条

这不是语义争议，而是 controlled vocabulary 被绕过。

典型记录：

- ZZ-SYS-23-013
- ZZ-SYS-47-003
- ZZ-SYS-48-037
- ZZ-SYS-57-052
- ZZ-SYS-60-035

### 3.2 六十星系 valence 越界：1 条

`ZZ-SYS-22-006` 使用 `valence=mixed`，但 v0.1 controlled vocabulary 只允许 favorable / unfavorable / context_dependent / not_applicable。

A0 采用非破坏式 override：`mixed -> context_dependent`，并将该修复标记为 `normalization_epistemic=IMPLEMENTATION`，不改变源文 literal claim。

### 3.3 六煞 operator_type 越界：1 条

`knowledge/operators/operator_schema.yaml` 当前不允许：

`time_scale_effect`

但：

`MOD-MAL-0017`

使用了该值。

### A0 判断

> 当前 “required fields 缺失 = 0” 不能等价于 “schema valid”。

原 validator 主要做字段存在性检查，没有真正验证 controlled vocabulary。

## 四、P0：reviewed 状态不可作为独立质量证明

当前主要 canonical 数据呈现：

- 十四正曜：430/430 = `EXPLICIT + reviewed`
- 六十星系：2193/2193 = `EXPLICIT + reviewed`
- 四化：56/56 = `EXPLICIT + reviewed`
- 辅佐八曜：103/103 = `EXPLICIT + reviewed`
- 六煞：81/81 = `EXPLICIT + reviewed`
- 杂曜：72 EXPLICIT + 1 INFERRED，全部 reviewed

但代码检查显示：

- `agents/a1_extractor.py` 仍是 skeleton，extract() 返回空列表；
- `agents/a2_ontology.py` 返回 not_implemented；
- `agents/a4_auditor.py` 只做极少字段检查，而且字段名与 canonical schema 并不一致；
- `agents/orchestrator.py` 只打印流水线步骤，然后直接把 task 标成 completed。

因此当前 `reviewed` 不能被解释为：

> 独立 Agent 已经按源文逐条完成了可靠验证。

A0 建议把历史 reviewed 的实际含义重新编码。

## 五、P1：认识论泄漏

当前最大结构风险不是“源文全是假的”，而是：

> source claim 的认识论等级与 normalization 的认识论等级没有分开。

例如：

~~~text
源文 literal claim
        ↓
target_normalized / QI / QR / operator
~~~

前一层可能是 EXPLICIT；后一层仍可能只是 INFERRED、IMPLEMENTATION 或 HYPOTHESIS。

如果只保留一个 `epistemic_type_source=EXPLICIT`，就会让模型归一化看起来也像是原书直接提出的状态维度。

A0 已新增提案：

`validation/decontamination/A0_epistemic_review_schema_v0.3_PROPOSAL.md`

建议拆为：

- source_epistemic
- normalization_epistemic

并把 review 拆为：

- MODEL_EXTRACTED
- MODEL_SELF_REVIEWED
- SOURCE_SPAN_VERIFIED
- HUMAN_VERIFIED

## 六、P1：原子性风险

新的 deterministic linter 采用较保守规则：

只有 condition 同时出现至少两类复合标记时，才进入高风险列表。

当前统一 heuristic 下发现 **39 条高风险 atomicity candidates**。

例：

`ZZ-SYS-01-009`

condition 同时压入多组独立组合：

~~~text
贪狼见天刑/空曜、
廉贞见桃花/昌曲、
刑忌夹印天相、
紫微见空曜华盖桃花
~~~

但最后统一压成一个 effect。

这种记录可能保存了总体语义，却不适合：

- 单条件激活；
- 消融测试；
- operator 组合；
- source-span 精确回放。

注意：

> 39 是统一 heuristic 下的高风险候选，不是已经判定错误的数量。

此前宽松关键词筛查得到的数量更高，A0 不把宽松数字作为正式 Gate 指标。

## 七、P1：L1/L2 与 L3 混层风险

六十星系 canonical 中：

- outcome_descriptor：997 条
- 其中 **800 条**仍使用 enhance / weaken / transform / inhibit / activate 等方向性状态算子

这不代表 800 条都错，但说明目前存在系统性层级混用风险。

需要区分：

~~~text
潜状态被增强
vs
潜状态投影为某种事件/语义输出
~~~

后续 source-span review 要把：

`state operator`

和

`projection operator`

重新分层。

## 八、P1：本体 anchoring 风险

当前核心时间顺序是：

1. 早期约 200 条样本；
2. 冻结 G2 气机本体；
3. 冻结 G3 十四正曜气核；
4. 冻结 G4 / G5 架构；
5. 之后才扩展到：
   - 十四正曜 canonical 430 条
   - 六十星系 canonical 2193 条
   - 大量辅佐煞化杂曜 operators

但 `qi_ontology.yaml` 与 `star_cores.yaml` 并未在全文规则扩充后重新进行一次反向审计。

风险是：

> 新材料被迫解释成旧 QI，而不是旧 QI 接受新材料的反证。

因此 A0 后必须执行 ontology backward audit，但不在本次硬性 schema 修复里直接修改冻结理论。

## 九、P1：控制理论术语风险

当前 `src/model_spec.py` 中的 observability 分类主要依靠 observation path 数量进行启发式分类。

该实现适合作为：

- observation-path support audit
- structural distinguishability heuristic

但不能直接等同于经典控制理论中的严格 structural observability 判定。

A0 暂不改 G5 理论，只登记术语重构任务。

## 十、当前建模真实进度

### 已建立

- G1–G6 Paper-1 概念架构
- 中州派核心 source inventory
- 十四正曜 canonical
- 六十星系 canonical
- 辅佐八曜 / 六煞 operator
- 部分四化 / 杂曜 operator
- symbolic state-space shell

### 尚未完成

- WP04 杂曜缺口仍存在
- 十二宫全文 KB-WP05
- 教材案例 regression KB-WP06
- evidence-first inference engine KB-WP07
- 全文规则反向重审 qi ontology
- 可复现实质 Agent runtime
- 严格 source-span audit pipeline

因此项目当前不应声明为“完整中州派推演系统”。

## 十一、本分支已执行的动作

A0 分支目前只新增审计工具和审计材料，不删除、不重写 canonical：

1. `src/audit_repository.py`
   - schema enum 检查
   - duplicate ID 检查
   - 原子性高风险筛查
   - L3 layer-boundary 筛查
   - epistemic/status 汇总

2. `tests/test_audit_repository.py`
   - 对 P0/P1 audit logic 建立回归测试

3. `validation/decontamination/A0_hard_schema_violations.csv`
   - 当前 61 条硬性违规

4. `validation/decontamination/A0_epistemic_review_schema_v0.3_PROPOSAL.md`
   - source / normalization epistemic 拆分
   - review status 四级化提案

## 十二、Gate A0 人工审核事项

请 PI 只审核以下五个原则，不需要逐条审 2636 条 canonical：

1. **批准** source_epistemic 与 normalization_epistemic 分离；
2. **批准** review_status 四级化；
3. **批准** 历史 GPT-only reviewed 默认降级为 MODEL_SELF_REVIEWED；
4. **批准** L1/L2 状态算子与 L3 projection 重新分层；
5. **批准** deterministic linter 成为 main 的强制 schema gate。

如批准 A0，下一阶段自动执行：

~~~text
A0 approval
-> 修复 61 条 P0 schema violation
-> 全库 review-status migration
-> epistemic 双层迁移
-> P1 高风险 source-span 分批回查
-> ontology backward audit
-> G2/G3/G4/G5 保留 / 修订差异报告
~~~

任何会改变 primitive qi、核心 mode 或 G1–G6 冻结原则的项，仍单独升级人工 Gate，不自动合并。

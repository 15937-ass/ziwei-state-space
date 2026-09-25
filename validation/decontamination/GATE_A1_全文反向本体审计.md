# Gate A1：全文反向本体审计与 G2/G3/G4/G5 修订提案

状态：**READY FOR PI REVIEW**  
分支：`audit/decontamination-p0-v2`  
前置 Gate：A0 APPROVED

## 1. 为什么现在必须回头审计本体

`knowledge/qi_ontology.yaml v0.2` 明确写明其 basis 只有 **200 条代表性规则**。

当前已扩展到：

- 十四正曜 canonical：430
- 六十星系 canonical：2193
- 辅佐八曜：103
- 六煞：81
- 四化：56
- 杂曜：73
- 六十星系派生 operator edges：654

因此 A1 不把 G2 当作错误，而是检查：

> 后来的全文知识是否被强迫塞进早期 200-rule ontology。

结论是：**L0-L4 分层架构仍稳定，但若干具体 QI/QR 维度和十四正曜 core evidence 已出现 anchoring / cross-layer contamination。**

---

## 2. A0/P1 对全文语料的直接结果

### 2.1 P0 已关闭

A0 最终确认 61 条 deterministic schema violation。

通过 raw canonical + review sidecar + controlled override 的 effective v0.3 view：

> **P0 = 0**

### 2.2 原子性高风险源文复核

39 条 strict atomicity candidates 已完成第一批 source-span review：

| 结果 | 数量 |
|---|---:|
| SOURCE_SUPPORTED | 30 |
| SOURCE_SUPPORTED_DEFINITION | 3 |
| SOURCE_SUPPORTED_CASE | 4 |
| CLAIM_SUPPORTED_PROVENANCE_WRONG | 1 |
| SOURCE_MISMATCH_CONFIRMED | 1 |

即：

- 38/39 的核心 source claim 可找到支持，其中 1 条需要修正 provenance；
- 1/39 为确认 source mismatch。

这说明当前问题主要不是“整批幻觉”，而是：

- 原子化压平；
- source / normalization 混写；
- provenance 漂移；
- state / output 混层。

---

## 3. 已隔离的两条代表性污染

### 3.1 ZZ-TT-010：确认 source mismatch

当前 canonical 把“天同 + 太阴 + 忌煞”归一化为“不经心 / 见事不明”。

P1 回到上册原文后：

- 天同相关段落可以支持疑虑、情绪/感情困扰、意志等性质；
- “办事不经心 / 大意”对应的是文昌化忌段落；
- 未找到当前 ZZ-TT-010 所声称的直接天同依据。

因此已：

- 写入 `knowledge/review/quarantine_v0.1.csv`
- source_epistemic 降为 `UNRESOLVED_SOURCE`
- 禁止进入 inference / ontology evidence

raw canonical 不删除，以保留审计历史。

### 3.2 ZZ-TX-003：claim 有依据，但 provenance 错位

“财荫夹 + 天府得禄 / 辅佐会合，可使天相软弱转为能力”的直接表述位于：

`六十星系·7 武曲天相坐寅申`

而不是当前 canonical 标注的：

`十四正曜·天相·书页25-26`

已通过：

`knowledge/migrations/p1_provenance_overrides_v0.1.csv`

进行非破坏式 provenance repair。

但这又暴露更深的问题：

> 该证据属于星系/条件环境，不能未经区分直接当成“天相单星 intrinsic core”的证据。

---

## 4. Ontology evidence 的结构问题

### 4.1 证据复用过多

当前 QI/QR evidence 中，有 **24 条规则被同时用作两个或三个维度的证据**。

典型：

- ZZ-PJ-003 同时用于 QI-03 / QI-04 / QI-08
- ZZ-JM-009 同时用于 QI-07 / QI-13 / QI-14
- ZZ-TX-009 同时用于 QI-02 / QI-11 / QI-15

多维证据本身不等于错误，但高复用说明早期 ontology 可能把同一原文性质拆成多个高度共线维度，需要重新做 redundancy audit。

### 4.2 L3 outcome 被拿来证明 L1/L2

当前 ontology evidence 中至少 **12 个引用是 outcome_descriptor**，例如：

- QI-05 <- ZZ-TJ-007 “实际成效”
- QI-06 <- ZZ-WQ-025 “失败风险”
- QI-08 <- ZZ-TJ-013 “用世能力”
- QI-13 <- ZZ-JM-006 “表达资源化”
- QR-04 当前 4 条 evidence 全部是 outcome_descriptor

A1 判断：

> L3 outcome 可以作为潜状态的下游支持，但不能与直接 L1/L2 证据等权使用。

后续 evidence schema 应区分：

- direct_state_evidence
- relational_evidence
- projection_evidence

---

## 5. 十四正曜 core 的 anchoring 污染

`star_cores.yaml` 的统一结构仍可保留，但具体 evidence 需要重建。

### 5.1 已确认的 cross-subject evidence

至少两颗星的 intrinsic signature 使用了其他星曜的 rule 作为直接 evidence：

- 天府 QI-15 使用 ZZ-WQ-020 / ZZ-WQ-021（subject=武曲）
- 太阴 QI-05 使用 ZZ-WQ-003（subject=武曲）

这些规则可以说明“该星对另一星有调节作用”或用于 interaction evidence，
但不能直接等同于该星自身的 intrinsic-state evidence。

### 5.2 core signature 中仍混入 outcome / system-context evidence

当前至少 8 个 `strength_class=core` 的 signature 含：

- outcome_descriptor；
- 六十星系上下文；
- “相关”类模糊 provenance。

高风险例：

- 廉贞 QI-11 的 core evidence 主要来自六十星系关联记录；
- 贪狼 QI-09 的 core evidence 大量来自紫微贪狼系统；
- 天相 QI-15 使用明显的 context/system evidence；
- 太阴 QI-01/QI-15 含 outcome evidence。

A1 建议：

> 重建十四正曜 core 时，优先级必须是  
> direct star-chapter evidence > explicit same-star modifier evidence > system-context evidence。

system-context evidence 进入：

- conditional_modifier
- interaction_delta
- mode evidence

而不是自动升格为 intrinsic core。

---

## 6. 现有 QI/QR 的反向审计结论

### 6.1 保留，但净化 evidence

以下维度在扩大语料后仍有明显独立来源支持，建议保留：

- QI-01 发射—收敛
- QI-02 刚—柔
- QI-03 稳定—变动
- QI-04 守成—开创
- QI-06 决策激活度
- QI-08 行动驱动
- QI-12 资源保存/管理
- QI-13 表达/传播
- QI-15 缓冲/调和
- QR-01 关系整合—孤离
- QR-04 支持资源

其中 QI-03 与 QI-04 仍建议分开：

- QI-03：状态迁移/变化幅度；
- QI-04：改变的结构方向/开创性。

不建议因为部分 rule overlap 就合并。

### 6.2 保留概念，但必须重建 evidence / 边界

#### QI-05 现实化—空泛

全文中“现实化下降 / 空想 / 虚而不实 / 踏实”等结构反复出现，
但早期 evidence 中混入资源空置、行动性等异质概念。

建议：

- 保留 QI-05；
- 清除不直接支持“落实—空泛”的 evidence；
- 使用全文中明确的现实化/空想规则重建证据集。

#### QI-07 认知机变

早期 evidence 把巨门“表达优化/善辩”也放入 QI-07。

建议：

- QI-07 收窄为认知、聪敏、策略适应；
- 巨门表达类主要归 QI-13；
- 只有原文明确涉及思维/认知变化时才同时进入 QI-07。

#### QI-09 欲望驱动

当前 evidence 混有：

- 欲望强度；
- 欲望类型；
- 感性；
- 精神享受；
- 享乐。

建议：

- QI-09 只表示趋求/欲望强度；
- “物欲/情欲/精神取向”留在 mode/orientation 层；
- 不把欲望类型自动扩展成额外 primitive。

#### QI-10 原则/规范约束

核心概念仍可保留，但“独行”“调处纠纷”等结果性性质不应直接等同规范约束。

建议净化 evidence，不改变概念主轴。

#### QR-03 竞争激活

保留；但七杀的刚克性本身不能直接作为竞争 evidence。

应优先使用明确“竞争/争夺/对抗”文本。

---

## 7. QI-14：不删除，但必须重新定义边界

早期 QI-14 “遮蔽—显明”与 QI-01 “发射—收敛”高度混用。

全文检索后仍能看到大量独立的：

- 巨门暗曜 / 遮蔽；
- 同巨明朗—阴暗；
- 遮蔽下降；
- 内向隐藏与外部可见性变化。

因此 A1 **不建议删除 QI-14**。

建议改成更窄的：

> **信息/状态可见性：遮蔽—显露**

并：

- 删除仅以太阳/太阴“发射—收敛”作为 QI-14 evidence 的引用；
- 主要用巨门、同巨等明确“暗/明/遮蔽”文本重建；
- 保留与 QI-01 的 redundancy test。

这会使：

- QI-01 = 动力学的内收/外放
- QI-14 = 信息/状态是否被遮蔽或显露

二者不再靠同一组证据维持。

---

## 8. QI-16：建议正式升格“目标导向性”

G4 已发现 QI-16-CAND。

全文扩大后，宽松检索得到：

- 六十星系相关规则约 61 条；
- 十四正曜相关规则约 4 条。

数字本身不是最终证据，真正关键是原文存在直接对照：

- 有目标 vs 盲动；
- 有目标改变 vs 无目的破坏；
- 目标是否明确决定同一“变动”是否能突破环境；
- 同样高行动/高变化，并不保证有目标。

因此它不能被 QI-03 / QI-04 / QI-08 完全替代：

~~~text
变化多 ≠ 有目标
行动强 ≠ 有目标
开创强 ≠ 有目标
~~~

### A1 proposal

正式新增 L1：

`QI-16 目标导向性 / goal-directedness`

定义：

> 行动、变化与资源投入具有明确目标、方向与建设性组织的程度。

注意：

- 不代表结果成功；
- 不把“建设性”直接等同吉；
- 是可被运限/星系条件改变的状态，不是人格永久标签。

---

## 9. QI-17-CAND：禁止按当前定义直接升格

G4 当前候选：

> “持续意志/韧性”

全文反查发现它实际上把至少三个不同概念压在一起：

1. **意志控制/自我约束强弱**
2. **毅力/持续性**
3. **受冲击后的恢复/韧性**

最关键的源文反证出现在天同巳亥：

> 原文明确区分“意志坚强”与“毅力”，并说明意志薄弱者仍可能有毅力。

因此：

`QI-17-CAND = 持续意志/韧性`

作为单一 primitive **不成立**。

### A1 proposal

废止当前合并候选，改成两个独立 candidate：

#### QI-17A-CAND：意志控制强度

定义：

> 在欲望、情绪、诱因或环境压力下维持自主约束与方向的能力。

主要来源簇：

- 太阴卯酉：意志强弱
- 天同巳亥：意志强弱

#### QI-17B-CAND：持续性 / 毅力

定义：

> 在时间、阻力或重复挫折下维持行动的持续程度。

主要来源簇：

- 天同辰戌的短志/持续不足
- 天同巳亥明确区分意志与毅力

### 暂不升格“韧性/恢复力”

“恢复力”目前很多是本项目对案例/适应效果的 normalization，
建议继续作为：

- system-level emergent property
- derived_state

而不是立即新增 primitive。

A1 批准后再决定正式编号是否为 QI-17 / QI-18。

---

## 10. G3：十四正曜气核的建议处理

G3 的**数据结构**保留：

~~~text
L0 substrate
+ intrinsic signature
+ relational signature
+ contextual sensitivity
~~~

但当前具体 14 星气核不再视为可直接冻结使用。

建议执行一次 **G3-R / Core Refit**：

1. 每颗星先只用 direct-star source 重建 baseline core；
2. 四化/辅佐煞曜进入 conditional modifiers；
3. 六十星系 evidence 进入 interaction_delta / mode；
4. outcome_descriptor 不作为等权 intrinsic evidence；
5. 允许某颗星当前没有某 QI，而不是为了填满 ontology 强行映射。

其中天相是最高优先级重构对象：

- QI-02 的“柔/软弱”可有 direct-star evidence；
- QI-15“调和平衡能力”目前高度上下文依赖，应重新判断是否真为 intrinsic core；
- QR-02“协同/辅弼端”当前主要依赖错误 provenance 的 TX-003，不应直接冻结。

---

## 11. G4：六十星系架构保留

A1 暂未发现需要推翻 G4 的证据。

以下继续保留：

~~~text
base composition
+ interaction_delta
+ mode
+ context gates
~~~

尤其全文数据反而加强了：

> principal mode 是中尺度状态，不应全部升级为 primitive qi。

需要修订的主要是：

- QI-16 / QI-17 candidate feedback；
- 部分 mode normalization；
- case-level rule 与 generic mode rule 分离。

---

## 12. G5：状态空间架构保留，但“能观性”术语必须降级

`src/model_spec.py` 当前：

~~~text
independent_paths >= 2
=> STRUCTURALLY_OBSERVABLE
~~~

这只是基于 observation-path count 的启发式分类。

它不是经典/结构系统理论意义上的 structural observability 判定。

### A1 proposal

Paper 1 和代码中将当前机制改名为：

`ObservationPathSupport`

建议状态：

- MULTI_PATH_SUPPORTED
- SINGLE_PATH_SUPPORTED
- NO_DIRECT_PATH
- DERIVED_ONLY

只有以后真正建立：

- 状态—输出结构图；
- generic rank / matching 或等价结构条件；
- 清晰输出映射；

才使用 `structural observability`。

这不改变 G5 的：

- natal essence 与 temporal input 分离；
- 12 宫图状态；
- state-dependent reaction；
- qi -> mode -> projection 链。

---

## 13. Gate A1 需要 PI 审核的 6 项

### A1-1
**保留 G2 的 L0-L4 分层架构，但允许基于全文重新拟合具体 QI/QR evidence 与边界。**

### A1-2
**正式升格 QI-16 “目标导向性”为 L1 状态。**

### A1-3
**否决当前合并式 QI-17-CAND；拆成“意志控制”与“毅力/持续性”两个独立候选，恢复力暂留 derived。**

### A1-4
**保留 QI-14，但收窄为“信息/状态遮蔽—显露”，与 QI-01 发射—收敛重新分证据。**

### A1-5
**批准 G3-R：十四正曜 core 从全文重新拟合；direct-star > modifier > system-context，禁止为适配旧 ontology 强填气核。**

### A1-6
**批准把当前所谓 structural observability 改名为 observation-path support；真正结构能观性留到有正式状态—输出图后。**

---

## 14. A1 批准后自动执行

~~~text
A1 approval
-> qi_ontology v0.3 refit
-> star_cores v0.2 G3-R
-> QI-16 formalization
-> QI-17A/B candidate library
-> QI-14 evidence rebuild
-> QI-05/07/09/10/QR-03 evidence purification
-> observability terminology/code migration
-> atomicity executable split/gate migration
-> 800-row L1/L2 -> L3 boundary batch audit
-> regression + source-trace tests
-> Gate A2 only if new conflicts change system-mode or state-space architecture
~~~

不需要 PI 逐条审核所有规则；只有新增/删除 primitive、改变核心星曜气核原则、改变六十星系架构或 G5 结构时再升级 Gate。

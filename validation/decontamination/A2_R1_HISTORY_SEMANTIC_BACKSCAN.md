# A2-R1 History Semantic Backscan v0.1

状态：**COMPLETE FOR SIXTY-SYSTEM SOURCE RANGE — NO NEW ARCHITECTURE GATE**

## 目标

在 45 条 regex heuristic candidates 全部闭环后，对《中州派紫微斗数深造讲义（上）》六十星系章再次按语义关键词与上下文回扫，避免“正则未命中 = 不存在跨期状态”的假阴性。

本轮检索与复核重点包括：

- 影响后运 / 后运受影响
- 他日
- 以后数年
- 养成 / 形成 / 根深蒂固
- 改变性格 / 影响人生观
- 后天人事
- 明确把当前应对连接到后来反应资格的语句

## 结果

在原 45 条 heuristic queue 之外，本轮确认 13 个需要登记的 source hits，另登记 2 个容易误判为 history 的 lookahead rules。

新增可执行 history transitions：**12 条**。

其中：

- ACQUIRED_DISPOSITION：8 条
- PATH_DEPENDENT_GATE：4 条
- CASE_HISTORY_EVIDENCE：1 条，不迁移为通用 transition
- LOOKAHEAD_RULE：2 条，不迁移

因此当前 history transition sidecar 从 18 条增至 **30 条**。

## 关键新增

1. 巨门系统：青年期疑忌形成、同梁困难环境下沉着/疑忌两种后天形成，以及成功诱因改变原有性格后的跨期风险。
2. 贪狼系统：太阳落陷流年中“退居幕后”与以后数年突发机会之间的明确路径门控。
3. 天同卯酉：早年天梁权名失配的应对影响后运，以及七杀阶段可造成精神空虚。
4. 武曲辰戌：天梁化科是否创造声誉、七杀大限影响人生观、天同良好运反而养成因循性格。
5. 天府丑未：顺遂后天人事形成谦和，以及早期太阳阶段进一步形成怯懦并影响后运。

## Canonical alignment

部分源文语义已被父规则概括，但父规则没有完整保存跨期条件。为不重写 raw canonical，本轮新增：

`knowledge/migrations/history_semantic_split_plan_v0.1.csv`

仅通过 auditable child rule 补齐 source-supported branch。

## 非 history 项

“参详以后几个流年”“检查后运再决定当前行止”等属于 **lookahead / planning constraint**，不进入 `M_t`。

教材个案中出现的“某运养成独立性格”保留为 case evidence，除非有可泛化的通用规则支持，否则不自动升格为 transition。

## 架构判断

本轮新增证据仍完全落在 A2-R1 的两类 typed memory 中：

- ACQUIRED_DISPOSITION
- PATH_DEPENDENT_GATE

没有发现必须：
- 重写固定 natal essence E；
- 新增第三类 history primitive；
- 引入默认衰减；
- 引入连续递归参数；
- 引入第二独立时间尺度。

因此 **不触发新 Human Gate**。

## 下一步

History backward audit 现在可在六十星系章范围内关闭。

下一机械工作单元：

`LB-07 source-normalization review`

随后按既定批次继续 LB-08 ... LB-16。

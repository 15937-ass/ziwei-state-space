# 当前检查点 — 阶段 B 首轮紫微候选研究（2026-10-25）

- Lane/shard/Issue/PR：KNOWLEDGE_ONLY / CORE / #757 / Draft #763。
- Base main：`0c9210855d874045f577914e8ec27e909438ecf4`；本轮接手head：`db42f5ffd8cdf5e2b8fa87e9360a55c701c16d54`；分支：`knowledge/core-757-14star-property-normalization`。
- 本轮来源：`SRC-ZZ-002`，《中州派紫微斗数深造讲义（上）》；源文件SHA-256 `1cd57c205297f78004c0d59db7cb77b05ecad53313757e55d8f1c78600609e9a` 与 `sources/source_index.csv` 一致。
- 已对PDF扫描页3（印刷页5–6）做视觉复核；当前canonical文件中的43条 `ZZ-ZW` 规则全部出现在 `ZIWEI_SOURCE_SPAN_REVIEW_v0.1.csv` 中。既有DIRECT_STAR Batch 01的4条紫微行被复用，不重复计证。
- 更新baseline JSON、Core恢复缓存、专用来源审查CSV和Core测试；新增12条逐目标mapping_review记录。全部候选仍 `PROPOSAL_ONLY_NOT_CANONICAL` / `UNRESOLVED`。
- 研究发现：帝座/君主是符号性主导角色候选，不是现实领导能力；具体性质依赖同度/会合；在野孤君必须保留“落陷且无百官朝拱”前提及空曜/煞忌分支；运限领导力不等于本命人格。
- 未修改正式星核、本体、canonical源规则、共享schema、正式ID、Product/runtime、KIB或消费权限。canonical `source_span_verified` 保持 false。
- 本次提交后的exact-head完整质量门禁：PENDING；必须以最终PR head自己的运行结果为准，历史绿色结果不转移。

---

以下为此前上下文方法检查点的历史证据；等待PI方法决定的停止点已被阶段B授权取代。

# 当前补充检查点 — 上下文方法审查（2026-10-25）

- Lane/shard/Issue/PR：KNOWLEDGE_ONLY / CORE / #757 / Draft #763。
- 本轮接手head：401a4ab61ae306124a5b2f4cf90eeebf45e9a4c1；同步base main：0c9210855d874045f577914e8ec27e909438ecf4。最终head/run在实时Issue/PR中记录；本文件不能自包含其结果commit SHA。
- PI已接受“补一次有界上下文检查、退出条件满足后继续”的建议；本轮只完成该检查点，不自动展开十一星。
- SHA-256已与source index核对；本次使用原PDF视觉复核scan pages 5、10、13、24左半，对应印刷9—10、19—20、25—26、46。源哈希：1cd57c205297f78004c0d59db7cb77b05ecad53313757e55d8f1c78600609e9a。
- 复用已有source_claim与定位，不新增canonical规则或独立证据计数。page47相关规则仍未逐项裁定。
- 具体修正：太阴原文“落陷、化忌之时”曾被研究卡改写为“落陷或化忌”；研究卡/理由已纠正，保留组内连接未决，明确外层或。canonical CSV与历史来源审查CSV不改。
- 研究记录增加本单局部context_method_audit，分开事实依据、知识内容层与规则作用；原有38条mapping_review对象保持已接受的字段形状。
- 五行复杂标签、四生等分类作用、无煞完整性仅登记局部缺口。没有共享Schema扩展、正式星核/本体/源规则、Product/runtime、KIB或消费权限修改。
- 变更限本单baseline MD/JSON、gaps、PI review、PI decision memo、现有test、Core恢复缓存和本执行证据；主线宫位更新只经同步继承，不算Core写集。
- 研究退出条件已满足；候选归一化仍UNRESOLVED。下一轮紫微候选研究已有方法授权；编译相关局部语义仍未定稿。
- 本次针对性pytest：23 passed；JS adapter语法检查通过；确定性P0检查退出0，P0=0（现存P1=907）。完整pytest及Core写集检查按最终exact head独立执行，结果在Issue/PR以精确base/head/run记录；历史run不替代本次验证。

---

以下是此前检查点的历史证据；其中等待PI方法决定的停止点已被上述授权与补充检查取代。

# 执行证据 — Issue #757 / 十四主星基础性质归一化

## 当前检查点

- Artifact status: `PROPOSAL_ONLY_NOT_CANONICAL`; this evidence records research-only work and does not authorize canonicalization or Product consumption.

- 太阳、太阴、天相三个有界试点均已形成候选卡与逐目标审核记录；pilot checkpoint head 9e0364015758a387c3351a6516183cad0e7a54d7 的 exact-head 质量门 Run #40169844516 已通过，完整 pytest、Product JS adapter、确定性 P0 与 Repository Governance v1 均成功。
- 三星横向比较已完成，当前状态为 READY_FOR_PI_METHOD_DECISION_STAGE_A_COMPLETE；跨星比较文档的新提交仍必须由 PR #763 当前 exact-head 检查独立验证，不能沿用旧 head 的绿色结果。
- 本轮来源覆盖边界仍有效：太阳未逐行审完全部 40 条规则；太阴书页 19–20 的 25 条已审但书页 42 的 ZZ-TYI-010 未审；天相 25 条范围内规则已审，ZZ-TX-009/010 的书页 47 相关星系内容未审。所有结果仍为研究候选，非 canonical。

- Lane / shard：`KNOWLEDGE_ONLY / CORE`
- Work unit：`KB-CORE-14STAR-PROPERTY-NORMALIZATION-BASELINE-01`
- 状态：`READY_FOR_PI_METHOD_DECISION_STAGE_A_COMPLETE`
- Activation base main：`74864f572cdd04407c241c483f3a34c646f69d3a`（历史启动基线）
- Working branch：`knowledge/core-757-14star-property-normalization`
- 当前检查点范围：太阳、太阴、天相三个有界试点与跨星方法比较已形成；不代表完整十四星交付。当前详细审议入口见 `knowledge/core/14star-property-normalization/14STAR_PROPERTY_NORMALIZATION_PI_DECISION_MEMO_v0.1.md`。

## 输入与来源

- 已接受的映射审核契约：`knowledge/core/wp06b/MAPPING_REVIEW_SCHEMA_v0.1.json`，由 #755 / PR #758 合入 main。
- 既有矩阵：`knowledge/core/14star-property-matrix/14STAR_PROPERTY_MATRIX_QIQR_AUDIT_v0.1.{md,csv,json}`，状态仍为研究草案。
- 既有直接来源审查：`knowledge/core/direct-star-source-review/DIRECT_STAR_SOURCE_REVIEW_BATCH_01_v0.1.csv`，太阳七条既有行级记录被复用，太阴 25 条视觉来源审查另存于 `knowledge/core/14star-property-normalization/TAIYIN_SOURCE_SPAN_REVIEW_v0.1.csv`；不修改 #720 Batch 01 的固定覆盖表。
- 原文：`SRC-ZZ-002`《中州派紫微斗数深造讲义（上）》，来源登记 SHA-256 `1cd57c205297f78004c0d59db7cb77b05ecad53313757e55d8f1c78600609e9a`，太阳 PDF 扫描页 5 / 印刷页 9–10；太阴 PDF 扫描页 10 / 印刷页 19–20。
- 已核对项目所附原文 PDF 的第 5 个与第 10 个 PDF 页面，并确认 PDF SHA-256 与 `sources/source_index.csv` 一致；太阳 40 条规则未全审；太阴本轮仅覆盖书页 19–20 的 25 条规则，书页 42 的 `ZZ-TYI-010` 未审。

## 变更与限制

- 新建/更新候选基线 JSON/Markdown、缺口清单、PI 审议草稿、太阳与太阴试点测试、执行证据及 Core 状态；新增独立的 25 条太阴来源审查 CSV，不修改 #720 Batch 01 固定覆盖表。
- `knowledge/star_cores.yaml`、`knowledge/star_systems.yaml`、`knowledge/qi_ontology.yaml`、`knowledge/rules/stars/major_stars_canonical_v0.1.csv` 未修改。
- 未新增正式 ontology ID、共享枚举、数值权重、概率、时间阈值或 Product 消费权限。
- 当前是研究检查点；PR exact-head gate 在 PR 建立后执行。尚未将本文件标记为最终验收证据。

## 验证

- 历史检查点：太阳 exact head `bb7d4a25551438c2a519a906e12e86dbb392d1d3` 的 Run #40159112167 曾通过；该结果不替代当前跨星比较提交的 exact-head 检查。当前权威质量门以 PR #763 的最新 head 与其关联 Actions run 为准。
- Product 回归：由当前路径过滤与 CI 实际结果决定；不预先宣称通过。

## 当前下一步

太阳、太阴、天相三个有界试点与跨星方法比较已形成；下一步是等待 PR #763 当前 exact-head 质量门完成，并由 PI 决定是否接受该研究方法进入阶段 B。当前不扩展剩余十一星，不进行 canonicalization，也不授权 Product 消费。


## Main synchronization after the Taiyin pilot update

- Latest main at synchronization: `cb48ac8fe6316eb9644448c99c596b72d72776c3` (P05 source-first Tianliang audit merge).
- The Core branch was synchronized with this main through a two-parent merge commit; P05 changes are retained from main and are not part of the Core semantic change set.
- This was a historical handoff note. The Taiyin and Tianxiang pilot checkpoints and the cross-star comparison have since been completed; the current gate is the latest exact-head run linked from PR #763.


## Tianxiang pilot source-first checkpoint

- Source: SRC-ZZ-002, 《中州派紫微斗数深造讲义（上）》.
- SHA-256: 1cd57c205297f78004c0d59db7cb77b05ecad53313757e55d8f1c78600609e9a, matches sources/source_index.csv.
- Visually inspected PDF scan page 13, which displays printed pages 25–26. Because the canonical locator for ZZ-TX-005/006 did not match that spread, also inspected PDF scan page 24 / printed p46 and corrected their locator in the research sidecar only.
- The dedicated TIANXIANG_SOURCE_SPAN_REVIEW_v0.1.csv records 25 in-scope rule IDs. The main span is printed pp25–26; ZZ-TX-005/006 are directly verified on printed p46 after locator correction. ZZ-TX-009 and ZZ-TX-010 have a related-star locator lead on printed p47 but remain explicitly out of scope and are not adjudicated here.
- Added 19 grouped source claims, 19 target-specific mapping-review records, Tianxiang gap/PI observations, and regression tests.
- Key finding: the source's direct emphasis is on contextual dependence and clamp/relational structure; it does not directly establish a fixed intrinsic QI-02 softness baseline. The specific TianTong/JuMen HuaJi branches are located on printed p46; the p46 scan visibly reads `是非尤的徵兆`, while the canonical target literal is `是非怨尤`, so that wording remains unresolved.
- All candidate claims remain PROPOSAL_ONLY_NOT_CANONICAL; no canonical source flag, normalization epistemic status, ontology ID, Product/runtime, KIB lock, or consumer permission is changed.
- Tianxiang's pilot checkpoint was validated by exact-head Run #40169844516 on head 9e0364015758a387c3351a6516183cad0e7a54d7. This result does not transfer to later cross-star comparison commits; the latest PR #763 check is authoritative for the current head.
- The canonical rules CSV, star cores, star systems, ontology and Product/runtime files remain unchanged; only research sidecars/card/evidence are updated.


## 三星横向比较与 PI 停止点

- 比较范围：太阳、太阴、天相三张试点卡；结论与机器可读 cross_star_comparison 对齐。
- 方法结论：现有 #755 v0.1 mapping-review 契约可记录本轮逐目标审核形状；目前没有必须新增共享 schema 的阻塞。研究卡仍须承载来源层次、条件/OR/AND、比较范围、关系与 L3 投影，因为结构校验不能自动证明语义解释正确。
- 建议：请 PI 先决定是否接受该方法进入阶段 B。未获决定前，不扩展剩余十一星；不修改正式星核、本体、canonical rule rows、Product/runtime 或消费者权限。
- 已通过的 pilot checkpoint exact head/run 是本节所列历史验证；跨星比较修改后的 head 以 PR #763 的最新 exact-head check 为准。

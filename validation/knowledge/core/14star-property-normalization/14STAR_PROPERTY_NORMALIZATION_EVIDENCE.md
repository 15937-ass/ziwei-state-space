# 当前 PI 裁决与审计交接（2026-10-28）

- 工作线：KNOWLEDGE_ONLY / CORE / Issue #757 / Draft PR #783；当前分支 `knowledge/core-757-14star-property-normalization-main-sync2`。
- 最新main `b42512b7e96b513a8ad65c08d6903b1791e244a7` 已通过同步 PR [#826](https://github.com/15937-ass/ziwei-state-space/pull/826) 合入Core分支，合并提交 `5b6dc02a65970a4f2287648341bde4b94fc58ad3`。本轮只同步main到Core分支，不把Core合入main。
- PI已裁定：`ZZ-TLIA-001`“第三得”是“第三星”的印刷错误；`ZZ-QS-005`“廉洁”是“廉贞”的印刷错误。原始扫描字面保留，正式canonical行与`source_span_verified=false`不变。
- PI映射语义决定（2026-10-28）：**1A、2B、3B**。1A接受太阳发射端／太阴收敛端的有限方向性对应，仅限候选研究层；2B采用定义驱动的QI-05严格审核门槛，不自动接受具体候选；3B将廉贞QI-11保留为未决候选。
- 以上决定不构成canonical晋升授权；候选仍为`PROPOSAL_ONLY_NOT_CANONICAL` / `UNRESOLVED`，canonical行、正式星核、本体、共享Schema未改，Product/runtime与KIB未获消费权限。
- 来源状态现为423条完整视觉核对、5条部分核对、1条未核实（`ZZ-TL-010`）、1条错配（`ZZ-TT-010`）。
- Mapping-review记录增至241条；处置分布为58 supported_candidate、57 candidate_only、100 needs_review、26 not_supported_for_target。候选性质182项全部链接有效。
- 原13项候选来源范围差异已逐项处理；当前仅保留`EXP-WQ-06 / ZZ-WQ-X06`一个与WQ-018/019重叠的摘要，不重复作为独立直接证据。`EXP-WQ-10`已对齐到L3候选审核；QI-05不支持记录保留。
- 原4条`evidence_role=UNKNOWN`中3条按既有schema处理，`MR-LZ-SYMBOLIC-ROLE-002`继续UNKNOWN，因为现有枚举无法准确表示传统象征标签。
- 引用复用统计已按更新后的mapping-review ledger重算：428次使用、360个唯一引用、59组精确引用复用；复用不增加独立证据权重。
- **质量门验收原则：** 每次源文件、测试或审计文档更新后，均以 PR #783 的最新 exact-head Checks 为准；本文件不写入自身提交的验收结论，避免自引用。父提交绿色运行不能替代最终head验收。
- 未修改正式星核、本体、canonical规则、共享Schema、Product/runtime、KIB或消费者权限；未批准 canonical 正式映射。

---

# 当前执行证据 — 破军候选检查点（2026-10-28）

- 执行分支：`knowledge/core-757-14star-property-normalization-main-sync2`；本轮接续七杀检查点，不回退、不重复审查已完成星曜。
- 来源：`SRC-ZZ-002`《中州派紫微斗数深造讲义（上）》；SHA-256 `1cd57c205297f78004c0d59db7cb77b05ecad53313757e55d8f1c78600609e9a`与来源索引一致。基础性质主跨度为扫描页16/印刷页31–32；七杀/破军比较补充扫描页15/印刷页29。
- `POJUN_SOURCE_SPAN_REVIEW_v0.1.csv` 覆盖30条 `ZZ-PJ` canonical行，30/30条均完成来源跨度视觉核对。`ZZ-PJ-006`位于扫描页96/印刷页191，`ZZ-PJ-007..010`位于扫描页97/印刷页193；五条四化规则未在本轮逐条扩展目标映射审核。canonical `source_span_verified=false` 与 `normalization_epistemic=UNRESOLVED` 均保持不变。
- 新增20条source-claim、20项candidate property、20条mapping-review记录和专用回归测试。
- 关键边界：破军“先锋/只攻不守”与“旧事创新”仅作传统描述候选；禄/权区别、英星入庙条件、昌曲例外、天马互动、天相对宫及星系结构保留分层；传统风险应象不作为现代预测。
- 全部候选仍为 `PROPOSAL_ONLY_NOT_CANONICAL` / `UNRESOLVED`；未修改正式星核、本体、canonical规则、共享Schema、Product/runtime、KIB或消费者权限。
- 本提交后的完整exact-head质量门须通过后才可记录最终验收；父检查点的绿色运行不替代本次验收。

---

# 当前执行证据 — 七杀候选检查点（2026-10-28）

- Lane/shard/Issue/PR：KNOWLEDGE_ONLY / CORE / #757 / Draft PR #783；分支 `knowledge/core-757-14star-property-normalization-main-sync2`。
- 天梁检查点在合并最新 main 的 head `02e63bec0e41e99e6481837ac02c72a883bad430` 上通过 [Run #40622883672](https://github.com/15937-ass/ziwei-state-space/actions/runs/40622883672)：2,833 passed、132 subtests passed；产品 JS adapters、deterministic P0 与 Repository Governance v1 均成功。
- 七杀来源为 `SRC-ZZ-002`《中州派紫微斗数深造讲义（上）》；SHA-256 `1cd57c205297f78004c0d59db7cb77b05ecad53313757e55d8f1c78600609e9a` 与 `sources/source_index.csv` 一致。直接视觉核对扫描页15/印刷页29–30。
- `QISHA_SOURCE_SPAN_REVIEW_v0.1.csv` 对26条 `ZZ-QS` canonical行逐一登记：26条完整视觉核对。`ZZ-QS-005`的“廉洁”按PI裁决理解为“廉贞”的印刷误字，原始literal保留。新增20条source-claim卡、20项候选性质、20条mapping-review记录和专用回归测试。
- 字面裁决：扫描字面“化杀为权的廉洁”按PI裁决理解为“化杀为权的廉贞”之印刷误字；保留扫描literal，不修改canonical来源标记或映射状态。
- 七杀新提交的 exact-head 完整质量门须在 PR #783 同步事件运行后确认；在关联运行成功前，不声称七杀新提交已通过。
- 未修改正式星核、本体、canonical规则、共享Schema、Product/runtime、KIB或消费者权限；所有候选保持 `PROPOSAL_ONLY_NOT_CANONICAL` / `UNRESOLVED`，canonical `source_span_verified=false` 保持不变。

---

# 当前执行证据 — 天梁候选检查点（2026-10-28）

- Lane/shard/Issue/PR：KNOWLEDGE_ONLY / CORE / #757 / Draft PR #783；分支 `knowledge/core-757-14star-property-normalization-main-sync2`。
- 天梁研究开始前 main/base 为 `5f697a5a02812e9781acf8d78e0f28d5087bd6ce`，研究开始前分支 head 为 `98f144b3acd69ab1bdf272e6557df674eda94306`。
- 研究开始前的 [Run #40616682474](https://github.com/15937-ass/ziwei-state-space/actions/runs/40616682474) 已在该父检查点的 PR merge ref 上通过：2,818 passed、132 subtests passed；JS adapter、deterministic P0 与 Repository Governance/Core write-set 步骤成功。该运行仅验证研究开始前的父检查点，不替代本轮新提交的 exact-head gate。
- 来源为 `SRC-ZZ-002`《中州派紫微斗数深造讲义（上）》；SHA-256 `1cd57c205297f78004c0d59db7cb77b05ecad53313757e55d8f1c78600609e9a` 与 `sources/source_index.csv` 一致。直接视觉核对扫描页14/印刷页27–28。
- `TIANLIANG_SOURCE_SPAN_REVIEW_v0.1.csv` 对26条 `ZZ-TLIA` canonical行逐一登记：26条完整视觉核对。`ZZ-TLIA-001`的“第三得”按PI裁决理解为“第三星”的印刷误字；`ZZ-TLIA-010`已在扫描页80/印刷页159补核。新增20条source-claim卡、20项候选性质、20条mapping-review记录和专用回归测试。
- 来源复核：`ZZ-TLIA-001`的字面差异已按PI裁决登记为印刷误字，literal保留；`ZZ-TLIA-010`已在扫描页80/印刷页159补核。两项来源跨度现均完成视觉核对，目标映射仍未决。
- Run #40621879283（head `91b17359e52b40728d13a284df58fce9b76170ca`）完成但未通过：`test_context_audit_refs_existing_source_claims_without_growing_canonical_evidence` 的前缀库存仍只统计原有11组映射记录，导致总数断言仍期待180；实际200条中新增的20条 `MR-TLIA-` 记录已通过映射校验。结果为1 failed、2,825 passed、132 subtests passed。
- 本次修正测试中的前缀库存，将 `MR-TLIA-` 纳入并把期望总数更新为200；修正后的新提交必须再通过完整质量门，才能认定本轮验收完成。
- 未修改正式星核、本体、canonical规则、共享Schema、Product/runtime、KIB或消费者权限；所有候选保持 `PROPOSAL_ONLY_NOT_CANONICAL` / `UNRESOLVED`，canonical `source_span_verified=false` 保持不变。

---

# 当前执行证据 — 贪狼候选检查点（2026-10-27）

- Lane/shard/Issue/PR：KNOWLEDGE_ONLY / CORE / #757 / Draft PR #783；分支 `knowledge/core-757-14star-property-normalization-main-sync2`。
- 本轮写入前 main head：`d45e2cfd6c0dc59fb80ec2210f7e729c53391c4f`；写入前分支 head：`61ef9f4bfef4d95f7143da735aa71dda6652f8ad`。本文件先于本轮 exact-head 质量门提交；最终结果以 Issue #757 / PR #783 对应提交的实时 workflow 记录为准，不作自引用证据提交。
- 来源：`SRC-ZZ-002`《中州派紫微斗数深造讲义（上）》；SHA-256 `1cd57c205297f78004c0d59db7cb77b05ecad53313757e55d8f1c78600609e9a`，与 `sources/source_index.csv` 一致。主跨度为扫描页11/印刷页21–22；另核扫描页51/印刷页100–101，以及扫描页93/印刷页184–185。
- `TANLANG_SOURCE_SPAN_REVIEW_v0.1.csv` 对29条既有canonical行逐条登记处置：27条完整视觉核对、`ZZ-TL-009` 部分核对、`ZZ-TL-010`未核实；`ZZ-TL-006/007/008`已在`SRC-ZZ-001`扫描页41–42/印刷页81–83补核。未复用既有DIRECT_STAR贪狼视觉审查行。
- 新增20条source-claim卡、20条mapping-review记录、20项候选性质及贪狼专用测试。测试覆盖精确规则ID集合、主/附来源定位、部分核对与未核实行、候选映射契约、进度顺序及非晋升边界。
- 主要边界：欲望强度与物欲/情欲类型分开；四旺宫异常映射按原文保留；紫贪/武贪/廉贪与命身结构保持条件化；煞曜作用不数值化；传统格局不转为现实结果保证；`ZZ-TL-009` 仅核实化禄分支。
- 未修改正式星核、本体、canonical规则、共享Schema、Product/runtime、KIB或消费者权限；所有候选仍 `PROPOSAL_ONLY_NOT_CANONICAL` / `UNRESOLVED`，canonical `source_span_verified=false` 保持不变。


---

# 当前检查点 — 阶段 B 第四轮天同候选研究（2026-10-26）

- Lane/shard/Issue/PR：KNOWLEDGE_ONLY / CORE / #757 / Draft #783。
- 当前base main：6b0828b5b722c4c71053b9da7f5ad89ac8022360；父提交：b8c9c12859f4bd40cd3e1a764eb8eab0a8b811a6。最终head与exact-head质量门以PR #783/Issue #757实时记录为准；父提交绿灯不替代本次内容提交验收。
- 主来源`SRC-ZZ-002` SHA-256 `1cd57c205297f78004c0d59db7cb77b05ecad53313757e55d8f1c78600609e9a`，扫描页7/印刷页13–14；另核对初级讲义印刷页87及上册印刷页23、146、178、228。
- `TIANTONG_SOURCE_SPAN_REVIEW_v0.1.csv`覆盖25条canonical行，复用6条既有审查，不重复计证。canonical source_span_verified仍为false，normalization_epistemic仍为UNRESOLVED。
- 关键发现：和气为比较性描述；化福不自动等于QI-15；享受与主动争取分开；煞忌有禄/昌曲门控；两类反背不可合并；页146同阴描述受紫杀行运主体限制。
- `ZZ-TT-010`不经心文字属于文昌化忌，继续隔离。
- 候选仍为PROPOSAL_ONLY_NOT_CANONICAL / UNRESOLVED；未修改正式星核、本体、规则、共享Schema、Product/runtime、KIB或消费者权限。
- 本提交后的exact-head质量门在GitHub Actions完成前为PENDING。下一颗：廉贞。

---

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


## 阶段 B 第二轮 — 天机来源与候选检查点（2026-10-25）

- Issue / PR：#757 / successor Draft PR pending creation；分支 `knowledge/core-757-14star-property-normalization-main-sync2`。
- 起始 head：`500415d6b5bb61aa3d798fa5464de8ebe0c968a6`；同步后的 main 基线：`e2d550b8fbc9893560c0c93957f30cae8ce21f71`（已包含 P05 廉贞尾段验收；Core 写集与该提交的 P05 文件不重叠）。新分支上的最终 exact head 与对应质量门以 successor PR 的实时执行记录为准；不沿用旧 head 的绿色结果。
- 来源：`SRC-ZZ-002`《中州派紫微斗数深造讲义（上）》，SHA-256 `1cd57c205297f78004c0d59db7cb77b05ecad53313757e55d8f1c78600609e9a`；PDF扫描页4，印刷页7–8。源文件哈希与 `sources/source_index.csv` 一致。
- 对当前 canonical 文件中的39条 `ZZ-TJ` 规则逐行视觉核对并新增 `TIANJI_SOURCE_SPAN_REVIEW_v0.1.csv`；复用 DIRECT_STAR Batch 01 中3条既有天机记录，不将复用行算作独立来源证据。
- 新增天机候选卡、17条逐目标 mapping-review 记录、天机缺口与回归测试。全部候选仍为 `PROPOSAL_ONLY_NOT_CANONICAL` / `UNRESOLVED`。
- 研究重点：谋士/军师与认知机敏是描述候选，但固定高 QI-07 仍需目标特定复审；近贵/天阙是关系门控；本命与运限变化分层；四化与不同煞曜的条件效应不合并。
- 未修改 `star_cores.yaml`、`star_systems.yaml`、`qi_ontology.yaml`、canonical rule rows、共享 schema、正式 ID、Product/runtime、KIB 或消费者权限。canonical `source_span_verified` 继续为 false。
- 当前阶段停止在天机候选检查点；下一颗为武曲，不在同一轮自动展开下一星。


## 阶段 B 第三轮 — 武曲来源与候选检查点

- Issue / PR：#757 / Draft PR #783。
- 基线 main：`e2d550b8fbc9893560c0c93957f30cae8ce21f71`。
- 来源：`SRC-ZZ-002`《中州派紫微斗数深造讲义（上）》，SHA-256 `1cd57c205297f78004c0d59db7cb77b05ecad53313757e55d8f1c78600609e9a`，与来源索引一致。
- 视觉核对范围：PDF 扫描页 6，印刷页 11–12。新增 `WUQU_SOURCE_SPAN_REVIEW_v0.1.csv` 覆盖 41 条 `ZZ-WQ` 行；新增 15 条 source-claim 卡、11 项候选性质和 17 条逐目标 mapping-review 记录。
- 既有 DIRECT_STAR Batch 01 中 6 条武曲审查记录均交叉核对；ZZ-WQ-005 的历史 literal_source_span 与原页不符。新侧车保留实际原文并记录差异，未修改历史审查 CSV 或 canonical 规则。
- 前一检查点 Tianji exact-head gate（head `67bec2c3dbbd4d462333735fbd2b959306ce61cf`）通过：Run [#40194363706](https://github.com/15937-ass/ziwei-state-space/actions/runs/40194363706)，2772 passed + 132 subtests；JS adapter、P0 audit、Repository Governance v1 均通过。该结果不替代新增武曲内容后的 exact-head gate。
- 本文件不从历史绿色结果推断新提交通过；以本提交对应的 GitHub Actions exact-head 运行和 Issue #757 最新交接为准。



## Core #757 recovery and 巨门 checkpoint — 2026-10-28

- Main synchronization: recovery-only PR #809 merged the latest accepted main commit 5f697a5a02812e9781acf8d78e0f28d5087bd6ce into the Core working branch. The P03 SP05 files were disjoint from the Core write set. Core PR #783 remains Draft and unmerged.
- The prior Tanlang checkpoint head 63aae8d57af0533e6491ab6d49349c8d7c222105 failed one test because the prefix-count assertion still expected 140 mapping-review records after the 20 MR-TL records had been added; actual total was 160. No source/candidate semantics were changed by that repair.
- Recovery/test repair head 287bdd52c40b911d9fea72a1c2e733fd5e60fab9 passed exact-head Run #40612148716: 2817 tests passed, 132 subtests passed; Product JS adapter, deterministic P0 and Repository Governance v1/Core write-set checks all passed. This run validates the recovery/test repair before the 巨门 additions.
- 巨门 source: SRC-ZZ-002, 《中州派紫微斗数深造讲义（上）》，SHA-256 1cd57c205297f78004c0d59db7cb77b05ecad53313757e55d8f1c78600609e9a, visually inspected PDF scan page 12 / printed pp23–24.
- The 巨门 checkpoint adds 20 source claims, 20 candidate properties, 20 mapping-review records, and JUMEN_SOURCE_SPAN_REVIEW_v0.1.csv for all 26 existing ZZ-JM canonical rows. Current sidecar disposition: 22 full visual confirmations, four partial confirmations (ZZ-JM-003/004/006/007), and zero unverified rows; ZZ-JM-005 was additionally checked in SRC-ZZ-001, scan page 42 / printed page 83. All candidates remain PROPOSAL_ONLY_NOT_CANONICAL / UNRESOLVED; canonical source flags remain false.
- Exact-head Jumen research gate: head 0505d04c74f936f39ab5d4cd1e28d4380269c110, Run #40615055215 — PASS. Full pytest: 2818 passed, 132 subtests passed (413.85 seconds); Product JS adapters, deterministic P0 repository audit, and Repository Governance v1/Core write-set validation all passed.
- The evidence-only commit that adds this checkpoint record and strengthens the Jumen recovery locator/test assertions must itself pass the full exact-head quality gate. The final head/run will be recorded in the latest Issue #757 / PR #783 handoff comment. Do not make another source/candidate change after final validation.


## 巨门来源引文精确性复核 — 2026-10-28

- 复核基线：Core head c736fb2bdd8185fc9bd143268ac54d6cfcb9585c，exact-head Run #40615965406 — PASS：2818 tests passed，132 subtests passed（370.75秒）；Product JS adapters、确定性P0审计及Repository Governance v1/Core写集检查全部通过。
- 逐页对照SRC-ZZ-002扫描页12/印刷页23–24后，发现若干研究摘录曾用省略号压缩非连续文字，或把连续原文的逗号改成句号。本次将source_excerpt与literal_source_span改为连续、逐字的原文片段；补充回归断言，防止再次把省略号占位当作原文。
- 扫描页24的“调各”“双能”继续按可见字面保留；本次只修复引文精确性，不改变候选语义、映射处置、来源状态或任何canonical字段。
- 本次修订后的精确head为待提交版本；必须再次通过完整exact-head质量门后，才能将巨门检查点正式交接。最终head/run将记录在Issue #757 / Draft PR #783最新交接评论中。此后不再修改来源/候选文件。


## 预 PI 来源审计与分支同步（2026-10-28）

- 已将 main `4cc89ead106c315d451d2d39b72e33ccc73398b5` 同步进入 Core 分支，合并提交 `cd11b672058e82efbdc08ee69a61f153aacb4a81`；PR #783 仍保持 Draft/unmerged。
- 两份本地来源PDF的SHA-256均与 `sources/source_index.csv` 一致：SRC-ZZ-001 `7ebafc8e3477430e2f8e69c6925ecc373d3c28966955f7035078c4949b7475a2`；SRC-ZZ-002 `1cd57c205297f78004c0d59db7cb77b05ecad53313757e55d8f1c78600609e9a`。
- 新增 `SUN_SOURCE_SPAN_REVIEW_v0.1.csv`，覆盖40条太阳canonical规则；来源跨度为扫描页5/印刷页9–10。
- 已补核太阴 `ZZ-TYI-010`（扫描页21/印刷页41；canonical定位页42的一页差异已记录）、天相 `ZZ-TX-009/010`（扫描页24/印刷页47）、贪狼 `ZZ-TL-006/007/008`（SRC-ZZ-001扫描页41–42/印刷页81–83）、巨门 `ZZ-JM-005`（SRC-ZZ-001扫描页42/印刷页83）、天梁 `ZZ-TLIA-010`（扫描页80/印刷页159）、破军 `ZZ-PJ-006..010`（扫描页96–97/印刷页191–193）。
- 14份侧车覆盖全部430条canonical规则ID：423条完整视觉核对、5条部分核对、1条来源未核实（`ZZ-TL-010`）、1条来源错配（`ZZ-TT-010`）。当前部分核对仅为 `ZZ-TL-009` 与 `ZZ-JM-003/004/006/007`；`ZZ-TLIA-001`和`ZZ-QS-005`的印刷误字已按PI裁决处理，来源跨度均为完整视觉核对。
- 所有canonical行仍保持 `source_span_verified=false` 与 `normalization_epistemic=UNRESOLVED`；没有canonical化或Product消费授权。
- 最新源审计及测试变更之后的exact-head完整质量门尚待确认；不能复用此前head的绿色运行作为本次最终验收。



## Mapping-review 预 PI 审计补充（2026-10-28）

- 241条mapping-review记录ID全部唯一；182项候选性质均关联到有效审核记录；未发现指向不存在canonical规则的引用。
- 428次来源引用使用、360个唯一来源引用；59组精确来源引用在多条审核记录中复用，共127次使用。引用复用不构成独立证据倍增。
- `evidence_role=UNKNOWN`当前仅1条：`MR-LZ-SYMBOLIC-ROLE-002`。其余原UNKNOWN记录已按现有schema得到有依据的处置；细节见 `MAPPING_REVIEW_PRE_PI_AUDIT_v0.1.md`。
- 候选属性仍为182项，所有映射链接有效；canonicalization授权为0、数值强度赋值为0、normalization epistemic全部为UNRESOLVED。


## 候选来源范围审计补充（2026-10-28）

- 交叉核对候选性质 `source_rule_ids` 与对应mapping-review记录 `source_refs` 后，初始发现13项候选、26个规则ID未在该记录的直接引用列表中出现。
- 逐项处置后，12项候选/25个规则ID已补充有依据的直接引用或缩窄范围；仅保留 `EXP-WQ-06 / ZZ-WQ-X06` 作为与 `ZZ-WQ-018/019` 重叠的摘要，不重复计证。
- 详细裁决见 `MAPPING_REVIEW_CANDIDATE_SOURCE_SCOPE_AUDIT_v0.1.md`。该剩余项不是缺失的独立证据，也不阻塞三张PI决策卡；未修改canonical规则、正式本体或消费者权限。

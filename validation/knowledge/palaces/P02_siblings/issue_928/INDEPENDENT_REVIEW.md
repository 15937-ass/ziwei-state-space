# P02 #928 独立来源与阶段交接审查

独立执行者：`p02_independent_review`（任务身份 `/root/p02_independent_review`）。本执行者未参与 #921 生产；#921 producer/root 只承担协调、机械实现和最终 GitHub 集成，不签本裁决。审查日期：2026-10-29。已读取 PDF skill，属只读原件审查，无 PDF authoring marker。

**裁决：NEEDS_BOUNDED_CENSUS_EVIDENCE_REPAIR；当前不能关闭来源审计阶段。** 找到一处重复出现在两个冻结清点文件中的跨页左尾证据错误。原来源原子 P02S-167 正确，不应按错误清点摘录“修复”其触发名单。140 held、49 gap 继续保留；条件编译、mapping、runtime、经验效度均未完成或授权。

## 权威、独立性与可复现输入

读取 PROJECT_STATE、CHATGPT_START_HERE、RECOVERY_PRECEDENCE、Knowledge/P02 state；实时读取 #928 正文与全部评论、Draft #929、已合并 #927。#927 接受 merge 为 `870c8df7097e94460b79d9ea6bea2fbd29881ade`；输入锁接受 main 为 `e15f284238f5a29c98e998abd961e5c7fea2ea44`。实时 #928 评论已登记本独立 reviewer 接手。准备 PR head 为 `e8928c8160c3363387bfa33a99b8ef0d21e82577`；本地准备提交 `27ef1ad5` 与其树相同是 owner 已核实的提交元数据差异，本审查不切分支、不 reset、不 commit。

自己对批准原件 `/workspace/scratch/bfbcfc0eab64/project_sources/05-pdf` 重算 SHA256，结果严格等于 `6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c`。自己用 pdftoppm 重渲染物理12–17，2400px全页与物理14的4000px局部；未用 producer 的“direct_visual_verified”布尔值替代看原扫描。19个冻结输入自己逐一重算 SHA256，并用 `git show e15f2842:<path>` 比较原字节，全部一致。独立 inline Python 未导入准备者 verifier；结果见同目录 `INDEPENDENT_MECHANICAL_EVIDENCE.json`。

## 原页覆盖与四跨页裁决

原扫描物理13左右为p25/26，物理14为p27/28，物理15为p29/30，物理16为p31/32。十四节顺序为紫微、天机、太阳、武曲、天同、廉贞、天府、太阴、贪狼、巨门、天相、天梁、七杀、破军。逐页视觉对照段落起止及既有locator；其段数分别15/17/21/16/17/16/6/6/6/5/5/9/5/7，合计151。p24（物理12右）是命宫破军尾，p33（物理17左）已题夫妻宫；两页不纳入兄弟宫。上述只确认覆盖与归属，不表示424行逐字语义重审全部通过。

| 唯一owner | 原页接缝独立核读 | owner原子 | 裁决 |
|---|---|---|---|
| SB03:S09 | p26“有极”接p27“大纠纷” | P02S-103–106 | 接续完整；化曜主体和克应承接继续held |
| SB04:W13 | p27“为武曲、破”接p28“军、七杀躔兄弟宫之年” | P02S-165–167 | 原子归属与167条件正确；清点left_tail错误，见阻塞项 |
| SB05:T17 | p28“且主为人能结交中下层”接p29“的朋友，唯无太多实际助力” | P02S-225–228 | 接续完整；228的唯句承接继续held |
| SB09:J03 | p30“以见煞”接p31“忌刑曜者为确” | P02S-342–344 | 接续完整；三条共同保留修饰范围未决 |

四个跨页owner各唯一，继续页只引用；151唯一段落产生155页面切片。不存在因这次清点证据错误而应增减原子或段落的依据。

## 唯一阻塞项与精确修复后继

`IR928-B01 / CENSUS_CROSSPAGE_QUOTE_MISMATCH`：

- `census/issue_921/P02_CHAPTER_CENSUS_MANIFEST_v0.1.json` 的 `cross_page_links` 中 `SB04:W13.left_tail` 写为“天机、巨门、破”。
- `census/issue_921/P02_SOURCE_COVERAGE_PHYSICAL_14_v0.1.json` 的 `continuations` 中同一owner同样写为“天机、巨门、破”。
- 两处均宣称 `direct_visual_verified:true`，但原扫描实际左尾为“为武曲、破”，右首为“军、七杀躔兄弟宫之年”。完整触发句为“不利之克应，为武曲、破军、七杀躔兄弟宫之年。”段首基底也是“辰戌宫武曲”；不能因为段首与触发名单均有武曲而删掉名单里的武曲，亦不能把清点误摘录的天机、巨门添加进167。
- 核对十一来源账本的全部字段：P02S-167.condition 已为“不利之克应，为武曲、破军、七杀躔兄弟宫之年”，与扫描一致。其 C01/承见煞夺权未唯一仍成立。这里不是一个新增星曜语义裁决，也不是 source atom 缺项。

首次2400px总览后，本 reviewer 曾向owner暂报167遗漏天机/巨门；4000px局部回核证伪该暂报，已显式撤回。此更正记录用于避免后继修复误改正确来源行。最终判断只依据放大后的扫描。

有界后继应在独立新工单中，以可追溯的勘误/替代证据登记这两处locator错误，重核同一跨页与owner；若经新工单明确授权改清点，须同步受影响清点hash pins与验证，并保留旧接受版本的审计关系。当前#928的19冻结输入及十一旧来源账本保持原字节。不要在本单静默改旧账本，不要修改167正确条件，不要新增/接受原子、消gap或改执行门。后继通过独立复核之前，whole_chapter_complete与stage_closure_authorized保持false。

放大证据在scratch：`p02-independent-pages/W13-p27-tail.png`，SHA256 `951cb499e7c8bd0796f60680fd91c82deadd7e38a7bc75eccdd50055af508fdd`；`W13-p28-head.png`，SHA256 `9d25f4450bb2b644896d55053963e73bb31ce5d60e18d282eefd5ed391ea3339`。可用同一批准PDF重渲染物理14到4000px再查看左页末/右页首复现；PNG仅是定位辅助，批准PDF及其hash为原件依据。

## 独立机械对账

424 ID严格连续且唯一；各原子source_span_id/source_anchor与唯一owner吻合。284接受包含180可复用来源/方法与104 CASE，不能合称284可执行规则。held分片45/48/47共140；49个gap的affected_record_ids与held恰双向唯一对应，没有孤儿或重复。索引每行condition、claim、notes与冻结来源完全一致，主gap一致；45条早期held的非空规范化文本仍无有效规范化或执行权。全部424的executable、canonical_mapping_approved、history_feedback均false/0。时间字段机械分布NATAL359/YEAR41/null24；null不是准许从邻段补时间层。

## 有界语义抽检与保留项

此审查按物理页41/45/37/28个owner分别对照；每次推理不超过50。风险行抽检首批32条，接缝/例外追加批15条；49个gap理由单独成批，不把424全表机械扫描称为单批语义重审。持久证据分片为19pins加有限聚合结果；没有单检查点保存超过100个新语义审查对象。

- 家庭身份/排序：001仅CASE；103异族友人同时CASE且主体held；203/204的卯本与长兄难养、223配偶不和仍held且CASE。358双胞胎CASE完整保留“必须家族有双胞胎传统”现实前提，不能当遗传医学事实。
- 合作现实前提与例外：004副手地位、005“不甘心”与大限流年关系不抹除；137把命宫辅弼与武府吉化分开，例外完整；377即使见吉仍不宜合作及“除非合作者完全退居幕后”都保留；274伙伴工作能力强与受怨并存；420保留“易”而非必然破裂。
- 时间：005的大限/流年并提不硬选主层；039/040宫垣泛称不从邻句借YEAR，040的末尾“宫垣克应”保存在source_time_expression，不能因claim字段只止于“的”误当整段丢失；224年限/之期不强选YEAR/DECADE；261明确YEAR只确认来源时间，并不消除主体/执行未决。
- 多未决：415除祀出字形之外notes保留火铃量词；418同时保留否则管辖及火铃；419/420保存此格局指代以及模态。主gap单列不代表副疑点丢弃；原notes逐字机械核对通过。
- 原件异常按已有gap继续保留：赞凶、卯本、故以人合作、见寿、各胞、祀出等均不凭常识纠字。P02S-261的忌星主体/冲起与P02S-414/416/417火铃BOTH/EITHER为两个主Core-gap组（主登记4held），仍LOCAL fail-closed。Core#915或后续描述性审查不能给本宫建立共享算子或消除这些未决；未消费未合并Core分支。

## 阶段交接边界

source_census_complete/held_gap_accounting_complete的计数与登记结论得到机械支持；但一个错误的跨页原文证据仍需有界勘误，不能把这些布尔值当作独立整章通过。独立审查已完成并提出阻塞，`approved=false`，`stage_closure_authorized=false`，`whole_chapter_complete=false`。本报告可以作为#928的独立审查结果被版本化接受，但这种接受不等于来源审计stage关闭。保留140held/49gap、45非空held禁用以及history_feedback=conditions_compiled=execution_unlocked=0；不启动P04，不触碰#888lease，最终GitHub集成由owner执行。

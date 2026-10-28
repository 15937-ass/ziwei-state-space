# P03 夫妻宫全量来源覆盖审计与时间层残项交接

状态：**审计草稿已形成，等待 exact-head CI 与 PI 验收；P03 尚未完成，P11 不得启动。**

## 1. 来源与边界

- 来源：SRC-ZZ-003，《中州派紫微斗数深造讲义（下册）》。
- 批准 PDF SHA-256：`6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c`，与本地原 PDF 实测 SHA-256 一致。
- 直接检查了原扫描图的 PDF physical pp17–26；对应印刷页 pp33–51。physical p26 同时包含印刷 p52，P03 在印刷 p51 最后一句结束，紧接“子女宫”标题前停止。
- OCR/文本提取仅用于定位，不作为独立来源证据。
- 既有 SP01–SP09 九份接受账本、836 条候选和历史 CSV 均保持只读。

## 2. 覆盖核对结果

- 19 / 19 个印刷页锚点已逐页登记。
- 664 条已接受来源记录均可唯一追溯；source-record ID 无重复。
- 836 条历史候选 ID 唯一；本轮未重开或重判其来源结论。
- 17 个来源缺口 ID 均已逐项列入；13 项按已接受账本记录为已解决，4 项仍开放或部分解决。
- 三个清晰但未被独立记录的来源原子已交给排队中的 [Issue #819](https://github.com/15937-ass/ziwei-state-space/issues/819)；该 Issue 在 #818 交接前不得成为第二个并行的 P03 worker。
- p37 扫描字样“机录像”保留原样；不得猜成其他星系名。该句的“经行至”也没有唯一确定 YEAR / DECADE，继续 fail-closed。

## 3. 逐页覆盖表

表中的候选范围只作为导航索引；覆盖证据来自原扫描图锚点和已接受 source-record refs。跨页记录会在相关页同时出现，但在 664 条全局唯一记录总数中只计一次。

| 印刷页 | PDF 物理页 | 可见章节锚点 | 已接受来源记录引用数 | 来源缺口 | 本页处置 |
|---:|---:|---|---:|---|---|
| 33 | 17 | 夫妻宫 / 1 紫微 | 41 | P03-SP01-GAP-001 | OPEN_SOURCE_ATOM |
| 34 | 17 | 紫微续段；后起 2 天机 | 51 | — | PAGE_END_CONTINUES_TO_P35 |
| 35 | 18 | 2 天机续段 | 37 | P03-SP01-GAP-002, P03-SP01-GAP-003, P03-SP01-GAP-004, P03-SP02-GAP-004 | OPEN_SOURCE_ATOM |
| 36 | 18 | 天机续段；转入 3 太阳 | 39 | P03-SP02-GAP-005 | OPEN_SOURCE_ATOM |
| 37 | 19 | 3 太阳 | 40 | P03-SP02-GAP-001, P03-SP02-GAP-002, P03-SP02-GAP-003 | OPEN_AMBIGUOUS_SOURCE_AND_TIME_SCOPE |
| 38 | 19 | 太阳续段；起 4 武曲 | 41 | — | PAGE_END_CONTINUES_TO_P39 |
| 39 | 20 | 4 武曲续段 | 43 | — | PAGE_END_CONTINUES_TO_P40 |
| 40 | 20 | 武曲续段；起 5 天同 | 32 | — | PAGE_END_CONTINUES_TO_P41 |
| 41 | 21 | 5 天同续段；起 6 廉贞 | 24 | — | PAGE_END_CONTINUES_TO_P42 |
| 42 | 21 | 6 廉贞续段；起 7 天府 | 38 | P03-SP05-GAP-001, P03-SP05-GAP-002 | PAGE_END_CONTINUES_TO_P43 |
| 43 | 22 | 7 天府续段；起 8 太阴 | 44 | P03-SP06-GAP-001 | PAGE_END_CONTINUES_TO_P44 |
| 44 | 22 | 8 太阴续段；起 9 贪狼 | 30 | — | PAGE_END_CONTINUES_TO_P45 |
| 45 | 23 | 9 贪狼续段；起 10 巨门 | 25 | P03-SP06-GAP-002, P03-SP06-GAP-003 | PAGE_END_CONTINUES_TO_P46 |
| 46 | 23 | 10 巨门续段；起 11 天相 | 34 | — | PAGE_END_AT_SECTION_TRANSITION |
| 47 | 24 | 11 天相 | 34 | P03-SP07-GAP-001, P03-SP07-GAP-002, P03-SP07-GAP-003 | PAGE_END_CONTINUES_TO_P48 |
| 48 | 24 | 11 天相续段；起 12 天梁 | 32 | — | PAGE_END_CONTINUES_TO_P49 |
| 49 | 25 | 12 天梁续段；起 13 七杀 | 35 | — | PAGE_END_CONTINUES_TO_P50 |
| 50 | 25 | 13 七杀续段；起 14 破军 | 38 | — | PAGE_END_CONTINUES_TO_P51 |
| 51 | 26 | 14 破军续段；夫妻宫章节结束 | 21 | — | P03_END_BOUNDARY_VERIFIED_BEFORE_CHILDREN |

## 4. 17 项来源缺口逐项对账

| Gap ID | 来源位置 | 已接受账本最新状态 | 本轮交接处置 |
|---|---|---|---|
| P03-SP01-GAP-001 | p33 / PDF p17 | CARRIED_FORWARD | OPEN_CLEAR_UNINDEXED_SOURCE_ATOM |
| P03-SP01-GAP-002 | p35 / PDF p18 | RESOLVED_BY_SP02-101 | RESOLVED_IN_ACCEPTED_SUPPLEMENTAL_RECORD_OR_BATCH |
| P03-SP01-GAP-003 | p35 / PDF p18 | RESOLVED_BY_SEPARATE_SP02-102_AND_SP02-103 | RESOLVED_IN_ACCEPTED_SUPPLEMENTAL_RECORD_OR_BATCH |
| P03-SP01-GAP-004 | p35 / PDF p18 | RESOLVED_BY_SOURCE_NARROWED_SP02-104 | RESOLVED_IN_ACCEPTED_SUPPLEMENTAL_RECORD_OR_BATCH |
| P03-SP02-GAP-001 | p37 / PDF p19 | PARTIALLY_RESOLVED_SOURCE_SPAN_VERIFIED_INTERPRETATION_HELD | PARTIALLY_RESOLVED_SOURCE_LITERAL_AND_TIME_SCOPE_HELD |
| P03-SP02-GAP-002 | p37 / PDF p19 | RESOLVED_BY_SUPPLEMENTAL_SOURCE_RECORDS | RESOLVED_IN_ACCEPTED_SUPPLEMENTAL_RECORD_OR_BATCH |
| P03-SP02-GAP-003 | p37 / PDF p19 | RESOLVED_BY_SP03-201_AND_SP03-202 | RESOLVED_IN_ACCEPTED_SUPPLEMENTAL_RECORD_OR_BATCH |
| P03-SP02-GAP-004 | p35 / PDF p18 | CARRIED_FORWARD | OPEN_CLEAR_UNINDEXED_SOURCE_ATOM |
| P03-SP02-GAP-005 | p36 / PDF p18 | CARRIED_FORWARD | OPEN_CLEAR_UNINDEXED_SOURCE_ATOM |
| P03-SP05-GAP-001 | p42 / PDF p21 | RESOLVED_BY_P03S-SP05-SUP-001 | RESOLVED_IN_ACCEPTED_SUPPLEMENTAL_RECORD_OR_BATCH |
| P03-SP05-GAP-002 | p42 / PDF p21 | RESOLVED_BY_P03S-SP05-SUP-002 | RESOLVED_IN_ACCEPTED_SUPPLEMENTAL_RECORD_OR_BATCH |
| P03-SP06-GAP-001 | p43 / PDF p22 | RESOLVED_BY_P03S-SP06-SUP-002 | RESOLVED_IN_ACCEPTED_SUPPLEMENTAL_RECORD_OR_BATCH |
| P03-SP06-GAP-002 | p45 / PDF p23 | RESOLVED_BY_P03S-SP06-SUP-001 | RESOLVED_IN_ACCEPTED_SUPPLEMENTAL_RECORD_OR_BATCH |
| P03-SP06-GAP-003 | p45 / PDF p23 | RESOLVED_BY_P03S-SP06-SUP-003 | RESOLVED_IN_ACCEPTED_SUPPLEMENTAL_RECORD_OR_BATCH |
| P03-SP07-GAP-001 | p47 / PDF p24 | RESOLVED_BY_P03S-SP07-SUP-001 | RESOLVED_IN_ACCEPTED_SUPPLEMENTAL_RECORD_OR_BATCH |
| P03-SP07-GAP-002 | p47 / PDF p24 | RESOLVED_BY_P03S-SP07-SUP-002 | RESOLVED_IN_ACCEPTED_SUPPLEMENTAL_RECORD_OR_BATCH |
| P03-SP07-GAP-003 | p47 / PDF p24 | RESOLVED_BY_P03S-SP07-SUP-003 | RESOLVED_IN_ACCEPTED_SUPPLEMENTAL_RECORD_OR_BATCH |

### 仍未关闭的四项

- **P03-SP01-GAP-001（p33）**：扫描原文读作“此等宫垣，见煞忌空劫即为生变之兆。”旧 gap 元数据中的“则更为”与扫描图不一致。已创建 Issue #819，后续补录必须以扫描图逐字为准。
- **P03-SP02-GAP-001（p37）**：扫描图可见“机录像”；不擅自改成看似合理的星系名称。“经行至”不能唯一推出流年或大限，故来源解释与时间层仍暂挂。
- **P03-SP02-GAP-004（p35）**：相关候选分别记录了部分子句，但未完整保留女命前提及“火铃或陀罗与天同同躔”的组合条件；由 Issue #819 处理。
- **P03-SP02-GAP-005（p36）**：现有记录保留了吉曜例外，却没有独立表示“天机在夫妻宫者，基本上不利”的基线；由 Issue #819 处理。

## 5. 时间层残项交接

- 最新接受账本包含 **63 组、175 条候选引用**。
- 本轮把每组赋予稳定审计 ID `P03-TEMP-001…063`，并将每个候选引用与所属批次、历史来源位置、验证位置、原文字段、历史时间层标签和处置理由连接。
- 175 条引用全部唯一，零重复、零缺失；全部 175 个 ID 都能回查至 SP01–SP09 的候选处置行。
- 旧标签 YEAR / DECADE 不是来源证据。“限”“枢纽”“克应之期”等措辞不自动授权时间层赋值。来源明确写“大运或流年”的条目保留原生范围，不静默折叠或拆成未经授权的新时间尺度。
- 未解决项继续 fail-closed；没有编译条件、解锁执行或改写历史反馈。

## 6. 下一步与阻塞关系

1. 先让本次 census/handoff artifacts 与 P03 回归测试通过 exact-head 完整质量门并合并。
2. 合并后将唯一 P03 工作槽位交给排队的 Issue #819，逐字补齐三个清晰来源原子。
3. p37“机录像”继续作为明确的来源解释/时间范围残项，除非直接证据支持更强结论。
4. 在 Issue #819 被接受、四项残项都有可审计处置、覆盖与时间层交接被 PI 接受前，不关闭 P03，不启动 P11。

## 7. 安全边界

`history_feedback=0`; `conditions_compiled=0`; `execution_unlocked=0`. 本轮不修改 Product/runtime、Core 共享语义、其他宫位、已接受账本或历史候选 CSV。

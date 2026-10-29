# P03 夫妻宫来源原子补录 — Issue #819

状态：**三个指定来源原子已直接视觉核对并形成 P03-local supplemental records；p37 残项继续开放。最终验收以当前 PR head 的完整质量门为准。**

## 1. 来源与方法

- 来源：`SRC-ZZ-003`，《中州派紫微斗数深造讲义（下册）》。
- 批准 PDF SHA-256：`6bddb3cac2e4b4efcf265229cbda22904ab3394aeef832e338ee5939088e5c5c`。
- 本地附件重新计算的 SHA-256 与批准 pin 完全一致。
- 直接检查原扫描图：PDF physical p17（印刷 pp33–34）及 physical p18（印刷 pp35–36）。OCR/文本提取只用于定位，不作为独立来源证据。
- 只处理 Issue #819 指定的 printed pp33、35、36；不重开 836 条既有候选裁决。

## 2. 三个来源原子

### P03-SP01-GAP-001 — 印刷页 33 / PDF physical p17

扫描图可见的句子为：

> 此等宫垣，见煞忌空劫即为生变之兆。

其前文条件保留在同一 source atom 中：寅申宫紫府同度、辅佐诸曜/单星与府库空露的上下文，以及贪狼、破军、巨门大运下婚姻变化的原文。历史 gap literal 中的“则更为”与扫描图不符；补录采用扫描图可见的“即为”，不把旧台账字面覆盖原文。

- 补录 ID：`P03S-SP01-SUP-001`
- 处置：`RESOLVED_BY_ISSUE819_SUPPLEMENTAL_SOURCE_RECORD`
- 限制：不推断新的量词、强度值或共享修饰语义。

### P03-SP02-GAP-004 — 印刷页 35 / PDF physical p18

扫描图逐字记录：

> 女命夫妻宫不宜「机巨」。古人说，「天机巨门为破荡」，虽指命宫，在夫妻宫者亦然。见火铃或陀罗与天同同躔，即非一婚之命。

完整保留女命前提和“火铃或陀罗与天同同躔”的组合条件。引号与标点按扫描图转录，不静默改写成现代术语。

- 补录 ID：`P03S-SP02-SUP-004`
- 处置：`RESOLVED_BY_ISSUE819_SUPPLEMENTAL_SOURCE_RECORD`
- 限制：只记录传统来源主张，不将其推广为现代关系建议或已验证因果规律。

### P03-SP02-GAP-005 — 印刷页 36 / PDF physical p18

扫描图逐字记录：

> 天机在夫妻宫者，基本上不利。唯与太阴相对或同度的情形下，见吉曜，然后始主谐美。

基线和例外作为同一个来源原子保留；不只摘录例外，也不将例外改写成无条件结论。

- 补录 ID：`P03S-SP02-SUP-005`
- 处置：`RESOLVED_BY_ISSUE819_SUPPLEMENTAL_SOURCE_RECORD`
- 限制：不新增现代本体映射或共享语义。

## 3. 仍开放的 p37 残项

- Gap：`P03-SP02-GAP-001`
- 位置：印刷页 37 / PDF physical p19（不属于本单获准的三个补录跨度）。
- 原文照录：**“机录像”**。
- 时间范围：`YEAR / DECADE` 仍无法唯一确定；“经行至”不构成强行指定流年或大限的依据。
- 处置：`OPEN_SOURCE_LITERAL_AND_TIME_SCOPE_UNRESOLVED`。不猜测星系名称，不自动合并、改写或关闭此缺口。

## 4. 验收边界

- 新增 3 条 P03-local supplemental source records；3 个指定缺口有直接来源记录。
- Issue #818 的 census/handoff 保持为已接受快照；本单不改写它或 SP01–SP09 已接受账本。
- 不修改历史候选 CSV；不重新裁决 836 条候选。
- `canonical_promotion=0`、新增 canonical rule rows = 0。
- `history_feedback=0`、`conditions_compiled=0`、`execution_unlocked=0`。
- 不修改 Product/runtime、Core 共享语义、其他宫位、权重、概率或独立时间尺度。
- P03 不得推进到 P11，直至本单被接受且 p37 残项有明确、可审计的处置。

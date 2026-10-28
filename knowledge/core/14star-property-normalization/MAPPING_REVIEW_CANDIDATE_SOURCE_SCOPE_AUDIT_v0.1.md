# 候选性质与 Mapping-review 直接来源范围核对（2026-10-28）

## 审计目的

核对每项候选性质的 `source_rule_ids` 与其关联 mapping-review 记录的 `source_refs` 是否一致。此检查只核对直接引用范围，不推断候选映射正确性。

## 结果

- 候选性质总数：182。
- 关联 mapping-review 记录：全部有效。
- 发现候选 `source_rule_ids` 中有规则未在对应审核记录的 `source_refs` 中直接出现：**26处，涉及13项候选性质**。
- 这些规则 ID 本身均存在于 canonical 规则集；本次发现是“候选性质所列来源范围”与“该条审核记录的直接引用范围”不完全一致，不代表 canonical ID 不存在，也不能直接断定为内容错误。
- 不应机械地把缺少的 ID 全部添加到审核记录：部分 mapping-review rationale 明确限定直接支持范围或指出目标不受支持。需要 PI 前逐项决定是（a）候选的来源清单是上下文材料，应明确区分直接证据/相关上下文；（b）审核记录应补充直接来源引用；或（c）候选来源清单应缩窄。

## 待核对清单

| 星曜 | 候选键 | 未在对应审核记录中直接引用的规则 | Mapping-review ID | 当前处置 | 审核记录现有直接引用 |
|---|---|---|---|---|---|
| 天相 | `PILOT-TX-02` | `ZZ-TX-X08`, `ZZ-TX-Y03`, `ZZ-TX-Y04` | `MR-TX-CLAMP-PRIORITY-005` | supported_candidate | `SRC-ZZ-002#pdf_scan_page=13#printed_page=25#ZZ-TX-X03` |
| 天相 | `PILOT-TX-03` | `ZZ-TX-004`, `ZZ-TX-X04`, `ZZ-TX-X05`, `ZZ-TX-X06`, `ZZ-TX-X07`, `ZZ-TX-Y02` | `MR-TX-CAIYIN-SOFTNESS-006` | needs_review | `SRC-ZZ-002#pdf_scan_page=13#printed_page=25#ZZ-TX-002`<br>`SRC-ZZ-002#pdf_scan_page=13#printed_page=25#ZZ-TX-003` |
| 紫微 | `EXP-ZW-02` | `ZZ-ZW-004` | `MR-ZW-CONTEXT-SENSITIVITY-003` | supported_candidate | `SRC-ZZ-002#pdf_scan_page=3#printed_page=5#ZZ-ZW-002`<br>`SRC-ZZ-002#pdf_scan_page=3#printed_page=5#ZZ-ZW-003`<br>`SRC-ZZ-002#pdf_scan_page=3#printed_page=5#ZZ-ZW-005` |
| 天机 | `EXP-TJ-05` | `ZZ-TJ-019` | `MR-TJ-QI03-TEMPORAL-007` | supported_candidate | `SRC-ZZ-002#pdf_scan_page=4#printed_page=7#ZZ-TJ-018`<br>`SRC-ZZ-002#pdf_scan_page=4#printed_page=7#ZZ-TJ-020`<br>`SRC-ZZ-002#pdf_scan_page=4#printed_page=7-8#ZZ-TJ-X04` |
| 天机 | `EXP-TJ-07` | `ZZ-TJ-024`, `ZZ-TJ-X05` | `MR-TJ-QI06-FIREBELL-011` | needs_review | `SRC-ZZ-002#pdf_scan_page=4#printed_page=7#ZZ-TJ-006`<br>`SRC-ZZ-002#pdf_scan_page=4#printed_page=7-8#ZZ-TJ-Y04` |
| 武曲 | `EXP-WQ-04` | `ZZ-WQ-Y01` | `MR-WQ-QR01-KINSHIP-006` | needs_review | `SRC-ZZ-002#pdf_scan_page=6#printed_page=11#ZZ-WQ-006`<br>`SRC-ZZ-002#pdf_scan_page=6#printed_page=11#ZZ-WQ-007`<br>`SRC-ZZ-002#pdf_scan_page=6#printed_page=11#ZZ-WQ-008` |
| 武曲 | `EXP-WQ-06` | `ZZ-WQ-X06` | `MR-WQ-QI06-CHANGQU-010` | needs_review | `SRC-ZZ-002#pdf_scan_page=6#printed_page=11#ZZ-WQ-018`<br>`SRC-ZZ-002#pdf_scan_page=6#printed_page=11#ZZ-WQ-019` |
| 武曲 | `EXP-WQ-09` | `ZZ-WQ-Y04` | `MR-WQ-QI06-WUPO-015` | needs_review | `SRC-ZZ-002#pdf_scan_page=6#printed_page=12#ZZ-WQ-024`<br>`SRC-ZZ-002#pdf_scan_page=6#printed_page=12#ZZ-WQ-025`<br>`SRC-ZZ-002#pdf_scan_page=6#printed_page=12#ZZ-WQ-Y03` |
| 武曲 | `EXP-WQ-10` | `ZZ-WQ-015`, `ZZ-WQ-016`, `ZZ-WQ-017` | `MR-WQ-FINANCIAL-ROLE-002` | not_supported_for_target | `SRC-ZZ-002#pdf_scan_page=6#printed_page=11#ZZ-WQ-002`<br>`SRC-ZZ-002#pdf_scan_page=6#printed_page=11#ZZ-WQ-X01` |
| 天同 | `EXP-TT-05` | `ZZ-TT-006` | `MR-TT-QI15-FU-AND-TRANSFORM-003` | needs_review | `SRC-ZZ-002#pdf_scan_page=7#printed_page=13#ZZ-TT-003`<br>`SRC-ZZ-002#pdf_scan_page=7#printed_page=13#ZZ-TT-X01` |
| 天同 | `EXP-TT-08` | `ZZ-TT-008`, `ZZ-TT-009`, `ZZ-TT-X08`, `ZZ-TT-X09` | `MR-TT-SYSTEM-STABILITY-018` | needs_review | `SRC-ZZ-002#pdf_scan_page=7#printed_page=14#ZZ-TT-X10`<br>`SRC-ZZ-002#pdf_scan_page=7#printed_page=14#ZZ-TT-Y04`<br>`SRC-ZZ-002#pdf_scan_page=7#printed_page=14#ZZ-TT-Y02`<br>`SRC-ZZ-002#pdf_scan_page=7#printed_page=14#ZZ-TT-Y03` |
| 天府 | `EXP-TF-04` | `ZZ-TF-003` | `MR-TF-RESOURCE-GENERATION-004` | needs_review | `SRC-ZZ-002#pdf_scan_page=9#printed_page=17#ZZ-TF-004` |
| 天府 | `EXP-TF-05` | `ZZ-TF-X03` | `MR-TF-QI04-GUARD-005` | needs_review | `SRC-ZZ-002#pdf_scan_page=9#printed_page=17#ZZ-TF-005` |

## 处理边界

- 不自动改写 canonical 规则。
- 不自动把候选性质来源 ID 视为直接证据。
- 不因引用列表更长而增加证据权重。
- 每项决定应保留来源范围、适用条件与映射目标之间的边界。
- 本审计是 PI 前的透明度/交叉引用核对，不授予正式映射批准，也不授权 Product 消费。

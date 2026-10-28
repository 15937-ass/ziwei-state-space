# Mapping-review 来源引用复用清单 v0.1

日期：2026-10-28（PI审计后重算）  

用途：核对相同来源引用被多个映射目标重复使用的情况。此清单只统计精确引用字符串的复用；同一印刷页中不同rule ID指向的重叠原文跨度，还需按来源跨度组去重。

- mapping-review记录：241；来源引用总使用次数：428；唯一来源引用：360。
- 重复出现的精确来源引用：59组；这些组累计127次引用使用。
- 相同引用出现在多个审核记录中，不因跨目标复用而计为多份独立证据。相同原文可服务于不同目标，但每个目标仍须分别审查其语义与条件。
- `shared_span:`引用表示记录显式将多个rule ID归为同一来源跨度；其余重复引用也应按精确引用去重。
- 额外识别的重叠跨度：`ZZ-WQ-X06` 与 `ZZ-WQ-018/019` 的昌曲调柔/优柔寡断内容重叠。即使rule ID不同，也不据此增加独立证据权重。

| 精确来源引用 | 使用次数 | 引用该来源的mapping-review记录 |
|---|---:|---|
| `SRC-ZZ-002#pdf_scan_page=11#printed_page=22#ZZ-TL-Y02` | 3 | MR-TL-L2-FOUR-WANG-ALTERNATIVE-007, MR-TL-L2-ZIWOLF-SYSTEM-008, MR-TL-L2-TAOHUA-FANZHU-015 |
| `SRC-ZZ-002#pdf_scan_page=11#printed_page=22#ZZ-TL-Y03` | 3 | MR-TL-L2-ZIWOLF-CONTROL-009, MR-TL-QI10-RESTRAINT-013, MR-TL-L2-TAOHUA-FANZHU-015 |
| `SRC-ZZ-002#pdf_scan_page=12#printed_page=23#ZZ-JM-X01` | 3 | MR-JM-QI14-MASKING-002, MR-JM-QI13-VERBAL-003, MR-JM-INTERPRETIVE-GATE-007 |
| `SRC-ZZ-002#pdf_scan_page=12#printed_page=23#ZZ-JM-X02` | 3 | MR-JM-SUSPICION-004, MR-JM-NEGATIVE-INFO-005, MR-JM-INTERPRETIVE-GATE-007 |
| `SRC-ZZ-002#pdf_scan_page=3#printed_page=5#ZZ-ZW-002` | 3 | MR-ZW-CONTEXT-SENSITIVITY-003, MR-ZW-QI08-INTRINSIC-004, MR-ZW-QI01-INTRINSIC-012 |
| `SRC-ZZ-002#pdf_scan_page=4#printed_page=7#ZZ-TJ-002` | 3 | MR-TJ-QI07-BASELINE-002, MR-TJ-CONTEXT-DEPENDENCE-003, MR-TJ-QI07-CONDITIONAL-004 |
| `SRC-ZZ-002#pdf_scan_page=42#printed_page=82-83#ZZ-LZ-009` | 3 | MR-LZ-CONTEXT-SENSITIVITY-006, MR-LZ-TIANXIANG-010, MR-LZ-LIANXIANG-CONTEXT-019 |
| `SRC-ZZ-002#pdf_scan_page=7#printed_page=13#ZZ-TT-X02` | 3 | MR-TT-QI09-ENJOYMENT-004, MR-TT-QI02-SOFTNESS-005, MR-TT-QI08-COMPARISON-012 |
| `SRC-ZZ-002#pdf_scan_page=75#printed_page=148-149#ZZ-LZ-010` | 3 | MR-LZ-CONTEXT-SENSITIVITY-006, MR-LZ-POJUN-011, MR-LZ-LIANPO-CONTEXT-020 |
| `SRC-ZZ-001#pdf_scan_page=44#printed_page=87#ZZ-TT-004` | 2 | MR-TT-QI09-ENJOYMENT-004, MR-TT-INITIAL-SUMMARY-006 |
| `SRC-ZZ-001#pdf_scan_page=44#printed_page=87#ZZ-TT-005` | 2 | MR-TT-QI02-SOFTNESS-005, MR-TT-INITIAL-SUMMARY-006 |
| `SRC-ZZ-001#pdf_scan_page=44#printed_page=87#ZZ-TT-006` | 2 | MR-TT-QI15-FU-AND-TRANSFORM-003, MR-TT-INITIAL-SUMMARY-006 |
| `SRC-ZZ-002#pdf_scan_page=11#printed_page=21#ZZ-TL-X05` | 2 | MR-TL-L2-FOUR-WANG-GATE-006, MR-TL-L2-FOUR-WANG-ALTERNATIVE-007 |
| `SRC-ZZ-002#pdf_scan_page=12#printed_page=23#ZZ-JM-X07` | 2 | MR-JM-NEGATIVE-INFO-005, MR-JM-TIANJI-INTERACTION-011 |
| `SRC-ZZ-002#pdf_scan_page=12#printed_page=23#ZZ-TT-008` | 2 | MR-TT-L2-JUMEN-INTERACTION-007, MR-TT-SYSTEM-STABILITY-018 |
| `SRC-ZZ-002#pdf_scan_page=12#printed_page=24#ZZ-JM-Y05` | 2 | MR-JM-STAR-SYSTEM-FAMILY-015, MR-JM-TRIAD-COMPARISON-016 |
| `SRC-ZZ-002#pdf_scan_page=13#printed_page=25#ZZ-TX-001` | 2 | MR-TX-QI02-INTRINSIC-002, MR-TX-CONTEXTUAL-SENSITIVITY-003 |
| `SRC-ZZ-002#pdf_scan_page=13#printed_page=25#ZZ-TX-X02` | 2 | MR-TX-QI02-INTRINSIC-002, MR-TX-CONTEXTUAL-SENSITIVITY-003 |
| `SRC-ZZ-002#pdf_scan_page=13#printed_page=25#ZZ-TX-X09` | 2 | MR-TX-POJUN-INTERACTION-014, MR-TX-L3-MIGRATION-017 |
| `SRC-ZZ-002#pdf_scan_page=13#printed_page=25#ZZ-TX-X10` | 2 | MR-TX-POJUN-INTERACTION-014, MR-TX-L3-HOLD-018 |
| `SRC-ZZ-002#pdf_scan_page=13#printed_page=25#ZZ-TX-Y03` | 2 | MR-TX-CLAMP-PRIORITY-005, MR-TX-POJUN-INTERACTION-014 |
| `SRC-ZZ-002#pdf_scan_page=13#printed_page=26#ZZ-TX-X08` | 2 | MR-TX-CLAMP-PRIORITY-005, MR-TX-STAR-SPECIFIC-HUA-011 |
| `SRC-ZZ-002#pdf_scan_page=13#printed_page=26#ZZ-TX-X11` | 2 | MR-TX-LIANWU-HUAJI-016, MR-TX-L3-CRAFT-019 |
| `SRC-ZZ-002#pdf_scan_page=13#printed_page=26#ZZ-TX-Y04` | 2 | MR-TX-CLAMP-PRIORITY-005, MR-TX-STAR-FAMILY-015 |
| `SRC-ZZ-002#pdf_scan_page=14#printed_page=27#ZZ-TLIA-004` | 2 | MR-TLIA-ISOLATION-004, MR-TLIA-METHOD-009 |
| `SRC-ZZ-002#pdf_scan_page=14#printed_page=27#ZZ-TLIA-006` | 2 | MR-TLIA-ARBITRATION-005, MR-TLIA-PROFESSION-006 |
| `SRC-ZZ-002#pdf_scan_page=14#printed_page=27#ZZ-TLIA-X01` | 2 | MR-TLIA-PRINCIPLE-003, MR-TLIA-ISOLATION-004 |
| `SRC-ZZ-002#pdf_scan_page=14#printed_page=27#ZZ-TLIA-X05` | 2 | MR-TLIA-METHOD-009, MR-TLIA-SHA-011 |
| `SRC-ZZ-002#pdf_scan_page=14#printed_page=27#ZZ-TLIA-X06` | 2 | MR-TLIA-METHOD-009, MR-TLIA-SHA-011 |
| `SRC-ZZ-002#pdf_scan_page=14#printed_page=28#ZZ-TLIA-Y05` | 2 | MR-TLIA-FAMILIES-019, MR-TLIA-PALACE-020 |
| `SRC-ZZ-002#pdf_scan_page=15#printed_page=29#ZZ-QS-X02` | 2 | MR-QS-COMPARISON-003, MR-QS-INDEPENDENT-004 |
| `SRC-ZZ-002#pdf_scan_page=16#printed_page=31-32#ZZ-PJ-X10` | 2 | MR-PJ-SPL-010, MR-PJ-OLDNEW-011 |
| `SRC-ZZ-002#pdf_scan_page=20#printed_page=38-39#ZZ-LZ-008` | 2 | MR-LZ-CONTEXT-SENSITIVITY-006, MR-LZ-LIANFU-CONTEXT-018 |
| `SRC-ZZ-002#pdf_scan_page=3#printed_page=5-6#ZZ-ZW-X01` | 2 | MR-ZW-QR01-INTRINSIC-006, MR-ZW-QR01-CONDITIONAL-007 |
| `SRC-ZZ-002#pdf_scan_page=3#printed_page=5#ZZ-ZW-001` | 2 | MR-ZW-L0-SUBSTRATE-001, MR-ZW-QI01-INTRINSIC-012 |
| `SRC-ZZ-002#pdf_scan_page=3#printed_page=6#ZZ-ZW-X05` | 2 | MR-ZW-QR01-INTRINSIC-006, MR-ZW-QR01-CONDITIONAL-007 |
| `SRC-ZZ-002#pdf_scan_page=3#printed_page=6#ZZ-ZW-X11` | 2 | MR-ZW-QI08-INTRINSIC-004, MR-ZW-TEMPORAL-QR02-009 |
| `SRC-ZZ-002#pdf_scan_page=4#printed_page=7-8#ZZ-TJ-Y01` | 2 | MR-TJ-QI07-BASELINE-002, MR-TJ-L4-APPRAISAL-016 |
| `SRC-ZZ-002#pdf_scan_page=4#printed_page=7#ZZ-TJ-005` | 2 | MR-TJ-CONTEXT-DEPENDENCE-003, MR-TJ-QI07-CONDITIONAL-004 |
| `SRC-ZZ-002#pdf_scan_page=4#printed_page=7#ZZ-TJ-010` | 2 | MR-TJ-L2-NEAR-NOBLE-005, MR-TJ-L3-OUTCOMES-013 |
| `SRC-ZZ-002#pdf_scan_page=4#printed_page=7#ZZ-TJ-011` | 2 | MR-TJ-L2-TIANQUE-006, MR-TJ-L3-OUTCOMES-013 |
| `SRC-ZZ-002#pdf_scan_page=4#printed_page=7#ZZ-TJ-012` | 2 | MR-TJ-L2-TIANQUE-006, MR-TJ-L3-OUTCOMES-013 |
| `SRC-ZZ-002#pdf_scan_page=4#printed_page=7#ZZ-TJ-013` | 2 | MR-TJ-QI08-HUAQUAN-010, MR-TJ-L3-OUTCOMES-013 |
| `SRC-ZZ-002#pdf_scan_page=4#printed_page=7#ZZ-TJ-014` | 2 | MR-TJ-QI07-CONDITIONAL-004, MR-TJ-QI10-HUAKE-009 |
| `SRC-ZZ-002#pdf_scan_page=4#printed_page=7#ZZ-TJ-016` | 2 | MR-TJ-QI07-CONDITIONAL-004, MR-TJ-L3-OUTCOMES-013 |
| `SRC-ZZ-002#pdf_scan_page=4#printed_page=7#ZZ-TJ-018` | 2 | MR-TJ-QI03-TEMPORAL-007, MR-TJ-TIME-SEPARATION-008 |
| `SRC-ZZ-002#pdf_scan_page=6#printed_page=11#ZZ-WQ-002` | 2 | MR-WQ-FINANCIAL-ROLE-002, MR-WQ-L3-FINANCIAL-ROLE-016 |
| `SRC-ZZ-002#pdf_scan_page=6#printed_page=11#ZZ-WQ-004` | 2 | MR-WQ-QI05-ACTION-003, MR-WQ-QI08-ACTION-004 |
| `SRC-ZZ-002#pdf_scan_page=6#printed_page=11#ZZ-WQ-014` | 2 | MR-WQ-QI02-YANGTUO-007, MR-WQ-L3-YANGTUO-008 |
| `SRC-ZZ-002#pdf_scan_page=6#printed_page=11#ZZ-WQ-X01` | 2 | MR-WQ-FINANCIAL-ROLE-002, MR-WQ-L3-FINANCIAL-ROLE-016 |
| `SRC-ZZ-002#pdf_scan_page=6#printed_page=12#ZZ-WQ-Y04` | 2 | MR-WQ-L2-SYSTEM-FAMILY-014, MR-WQ-QI06-WUPO-015 |
| `SRC-ZZ-002#pdf_scan_page=7#printed_page=13#ZZ-TT-X01` | 2 | MR-TT-QI15-FU-AND-TRANSFORM-003, MR-TT-SETBACK-PROCESS-011 |
| `SRC-ZZ-002#pdf_scan_page=7#printed_page=14#ZZ-TT-X08` | 2 | MR-TT-TIANMA-SYSTEM-016, MR-TT-SYSTEM-STABILITY-018 |
| `SRC-ZZ-002#pdf_scan_page=7#printed_page=14#ZZ-TT-X09` | 2 | MR-TT-FIREBELL-CONFLICT-017, MR-TT-SYSTEM-STABILITY-018 |
| `SRC-ZZ-002#pdf_scan_page=74#printed_page=146#ZZ-TT-009` | 2 | MR-TT-SAMEYIN-SCOPE-008, MR-TT-SYSTEM-STABILITY-018 |
| `SRC-ZZ-002#pdf_scan_page=8#printed_page=15-16#ZZ-LZ-X01` | 2 | MR-LZ-DUALITY-TENSION-003, MR-LZ-CONTEXT-SENSITIVITY-006 |
| `SRC-ZZ-002#pdf_scan_page=8#printed_page=15-16#ZZ-LZ-Y06` | 2 | MR-LZ-SHAJI-GATE-014, MR-LZ-XIONGSU-GATE-017 |
| `SRC-ZZ-002#pdf_scan_page=9#printed_page=17#ZZ-TF-003` | 2 | MR-TF-RESOURCE-MANAGEMENT-003, MR-TF-RESOURCE-GENERATION-004 |
| `SRC-ZZ-002#pdf_scan_page=9#printed_page=17#ZZ-TF-X01` | 2 | MR-TF-RELATIVE-LEADERSHIP-006, MR-TF-ZIWEI-HIERARCHY-011 |

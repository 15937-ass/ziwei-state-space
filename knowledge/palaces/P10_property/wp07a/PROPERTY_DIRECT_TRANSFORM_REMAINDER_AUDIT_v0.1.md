# Property Direct-Transformation Remainder Audit v0.1

Status: **3/3 source-rechecked and mapped to existing atom; not production**

Work unit: `KB-WP07A-PROPERTY-DIRECT-TRANSFORM-MAP-REMAINDER` / Issue #565  
Approved source: SRC-ZZ-003, 《中州派紫微斗数深造讲义（下册）》, 田宅宫  
Canonical baseline: 358/358 source-rechecked

## Mapped direct NATAL conditions

- **TP01-095 — 太阳化忌在田宅宫** (printed p158). The source explicitly says this does not directly mean harm to the father; it points to ancestral-property decline or a lifetime career lacking a firm foundation. The following `更见煞刑虚耗` extension is separately preserved as TP01-096.
- **TP02-148 — 天同化禄** (printed p160). The source says property can become abundant in the mid/later-life stage and be located in an upper-status area. The literal life-stage wording remains source metadata; it is not converted into an age threshold. TP02-149 separately preserves the exception that accompanying煞 can lower location quality without implying fewer holdings.
- **TP03-270 — 巨门化忌于田宅** (printed p163). The direct source projection is household unrest or separation from the household. Litigation and deception branches remain separately bounded as TP03-271/272 and CASE_SUPPORT_ONLY.

Each accepted condition uses exactly one existing atom:

`TRANSFORMATION_PRESENT(palace=P10, star=<source star>, mutagen=<source mutagen>)`

The current natal palace resolver already emits this palace/star/mutagen fact when the P10 star object itself carries the mutagen. The mapping proves fact-shape representability only; it does **not** create a production rule or authorize runtime execution.

## Source and provenance cross-check

All three IDs were rechecked against the canonical TP01/TP02/TP03 CSV rows, the corresponding source-readjudication records, and source-time-scope sidecars. The supplied PDF text was also directly inspected at the printed source passages. Canonical condition, projection domain, projection target, projection mode, time layer, source location, and CASE_SUPPORT_ONLY status are preserved exactly.

## Explicitly excluded nearby branches

| Rule | Why it is not collapsed into the direct atom |
|---|---|
| TP01-096 | Separate `太阳化忌更见煞刑虚耗` compound condition |
| TP02-149 | Separate `天同化禄同时见煞` exception: holdings need not be few, but location quality may be lower |
| TP03-271 | Litigation under 羊陀/空劫/刑耗: CASE_SUPPORT_ONLY event candidate |
| TP03-272 | Sale-deception under 文曲化忌: CASE_SUPPORT_ONLY event candidate |
| TP03-273 | Original-chart auspicious transformation becoming 大运/流年化忌 with 煞: multi-layer CASE_SUPPORT_ONLY event candidate |

Generic 吉曜/煞曜 groups, brightness, relation geometry, 前格 dependencies, temporal conditions, and case-only events remain outside this direct-transform mapping. Any missing shared meaning must fail closed and be recorded as a Knowledge Core gap rather than invented in P10.

## Boundary

- 3 nominated; 3 mapped; 0 blocked.
- Only the existing `TRANSFORMATION_PRESENT` atom is used.
- No source row, Product runtime, production registry, shared Core semantic, probability, numeric weight, or threshold is modified.
- Validation is data-only and follows the OpenAI/Codex execution preference in Issue #565. Full repository pytest is not claimed unless actually run in an available repository-mounted environment.

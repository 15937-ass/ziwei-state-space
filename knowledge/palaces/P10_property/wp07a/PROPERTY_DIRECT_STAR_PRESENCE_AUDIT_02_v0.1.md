# Property Direct Star-Presence Mapping Audit 02 — Residual Batch

Status: **6/6 mapped with existing atom; not production**

Work unit: `KB-WP07A-PROPERTY-DIRECT-STAR-PRESENCE-MAP-REMAINDER-01` / Issue #597  
Approved source: SRC-ZZ-003, 《中州派紫微斗数深造讲义（下册）》, 田宅宫  
Canonical baseline: 358/358 source-rechecked on main

## Mapped source conditions

- **TP02-134 — 武曲守田宅** (printed p160). The extracted source anchor is retained as `又武曲守宅，直服务财经机构。`. This is a scene translation to a financial-institution service context; it does not promise stable employment or success.
- **TP02-139 — 天同守田宅宫** (printed p160). The source directly links the baseline condition with 白手兴家 / 可以置业. The separate 禄 modifier is not included in the star-presence atom. This rule is not dependent on 天梁对拱; the separate comparison rule is TP02-163.
- **TP03-207 — 天府守田宅一般情况** (printed p162). The baseline work/institution stability statement is mapped separately from the source's forced-movement and personnel-dispute conditions.
- **TP03-214 — 天府守田宅一般情况** (printed p162). The baseline low fengshui-sensitivity statement is mapped separately from TP03-215 (天姚、阴煞同度).
- **TP04-319 — 天梁守田宅一般情况** (printed p164). The baseline low fengshui-sensitivity statement is mapped separately from TP04-320 (阴煞同度又见火铃).
- **TP04-339 — 七杀守田宅一般情况** (printed p165). The baseline low fengshui-sensitivity statement is mapped separately from TP04-340 (廉贞七杀或武曲七杀).

Each mapped condition uses exactly one existing atom:

`PALACE_HAS_STAR(palace=P10, star=<source star>)`

## Separate contextual / compound rows preserved

| Rule | Boundary |
|---|---|
| TP03-204 | 天府关陀夹同时火铃夹: forced property movement/sale remains a separate compound condition |
| TP03-209 | 天府见煞忌刑耗同会: institution personnel disputes remain separate |
| TP03-215 | 天府与天姚阴煞同度: fengshui exception remains separate |
| TP04-320 | 天梁与阴煞同度又见火铃: fengshui exception remains separate |
| TP04-340 | 廉贞七杀或武曲七杀: compound fengshui caveat remains separate |

## Deferred rows

- **TP03-299** (`天相守田宅` → long-term residence in older property scene) is not included. Its “亦主终身住旧宅” sentence follows a compound/contextual fengshui statement; defer until its exact condition scope is re-adjudicated.
- TP01-018 still requires exclusivity/absence semantics; TP02-170 retains source-glyph uncertainty; TP03-261 retains literal `中年后`; TP03-275 retains its 化忌 modifier; TP03-288 / TP03-289 retain the Tianfu cross-palace / treasury-state dependency.

## Boundary

- 6 nominated; 6 mapped; 0 blocked.
- All selected rows are source-span-verified, NATAL, and non-CASE_SUPPORT_ONLY.
- Only `PALACE_HAS_STAR` is used.
- No source row, Product runtime, production registry, shared Core semantics, probability, numeric weight, or threshold is modified.
- Mapping proves representability only; it does not authorize production execution.

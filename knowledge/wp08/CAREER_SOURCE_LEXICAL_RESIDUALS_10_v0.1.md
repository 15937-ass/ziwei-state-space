# Career Source Lexical Residuals 10 v0.1

Issue: #472  
Lane: **KNOWLEDGE_ONLY**  
Status: **10/10 source-dispositioned; no global ANY/ALL/N default**

本工作单元复核 WP08 留下的 6 条 source shorthand 与 4 条 source-list quantifier 残项。成功的标准不是“多解锁”，而是把每条残项分成：可由中州派原文恢复、只能做 source-local 绑定、或应正式冻结为 `NO_UNIVERSAL_RULE / INSUFFICIENT_SOURCE`。

## 结果

- 10/10 完成 source disposition。
- 旧 `SOURCE_SHORTHAND_MEMBERSHIP_UNSPECIFIED`: **6 → 0**。
- 旧 `SOURCE_LIST_QUANTIFIER_UNSPECIFIED`: **4 → 3**。注意 CA01-059 回退到原文三项显名后新增 1 个 list-quantifier 残项，因此净变化不是简单 -2。
- 两条规则获得完整的 source-local list structure：**CA03-289、CA05-484**。
- 三条 source surface 得到修复：**CA01-059、CA04-345、CA05-484**。
- **CA04-391** 冻结为 `NO_UNIVERSAL_RULE_SOURCE_LOCAL_ENUMERATION_QUANTIFIER_UNSPECIFIED`。
- **CA05-433** 冻结为 `INSUFFICIENT_SOURCE_FOR_LIST_QUANTIFIER`。
- 无 Product runtime 修改；无规则执行解锁；无数值阈值、权重或概率。

## 关键修复

### CA01-059
旧抽取把原文压成“财星化禄”。原文实际显名为“廉贞化禄、贪狼化禄、武曲化禄”。因此删除虚构 shorthand membership 问题，改为显名列表；但列表内部 ANY/ALL 仍不由标点猜测。

### CA03-289
事业宫原文说太阳喜“三台八座，恩光天贵等杂曜朝拱，皆有助于事业”；上册又明确三台八座必须成对会照，恩光天贵处于“对星”章节并说明对星多需成对同会。因此可冻结为两个 source-local paired patterns 的 ANY_OF，不把“等杂曜”扩成封闭列表。

### CA04-345
旧抽取“多见火曜”过度压缩。原文是“多见属火的星曜”。改为 open property category；“多见”仍保持 nonnumeric，`CARDINALITY_THRESHOLD_UNSPECIFIED` 不动。

### CA05-484
旧表达把“武曲化禄 + 禄存”误成同时条件。原文是“会禄（武曲化禄为上，禄存次之），或会天府化科”。改为三项 source-local alternative，并只保留“武曲化禄 > 禄存”的序位，不赋权重。

## 合法的未决状态

- CA04-391：五项显名，但原文没有给可移植的 ANY/ALL/N 量词。
- CA05-433：“天厨、火星同度”单句不足以证明固定 pair、BOTH 或 ANY。
- CA06-502：“见禄”有廉贞化禄、破军化禄两个紧邻实例，但来源没有明确说成员仅止于二者。
- CA08-723：“刑忌来会”是 source compound/pattern surface，不是可直接闭合的星名集合；也不能偷换为“刑忌夹印”。
- CA09-864：“吉辅”只做 scoped alias 到既有“辅佐吉曜” qualified category，成员量词与“吉”的语境限定仍不闭合。

## Red-team

红队重点检查了五类偷换：标点=>ANY/ALL、局部 pair=>全局 pair、source example=>closed membership、ordinal=>numeric weight、同义缩写=>全局语言规则。全部 guardrail 通过。

结论：本轮真正增加的是**可审计的 source semantics**，不是为了执行率制造规则。

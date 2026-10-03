# MAL01 — 六煞 Source Review

status: **CHECKPOINT_CLOSED_SOURCE_SPAN_VERIFIED**

## Scope

- source: SRC-ZZ-002《中州派紫微斗数深造讲义（上册）》
- printed pages: 171–175
- catalog: `knowledge/operators/six_malefics_v0.1.csv`
- reviewed rules: MOD-MAL-0001 … MOD-MAL-0081
- source sections: 煞曜总论、擎羊陀罗、火星铃星、地空地劫

## Result

- reviewed: 81
- SOURCE_SPAN_VERIFIED: 81 / 81
- ADD_CANDIDATE: 49
- CASE_SUPPORT_ONLY: 32
- new primitive qi: 0
- new history-memory type: 0
- new Human Gate: 0
- continuous weights / decay / fixed persistence duration invented: 0

## Review semantics

The legacy catalog remains provenance-preserving. The authoritative v0.3 review overlay is `MAL01_malefic_source_review_v0.1.csv`.

Traditional gendered, family, relationship, legal, health, occupation and severe-incident labels are retained as `CASE_SUPPORT_ONLY` where they are primarily L3 projection semantics. Mechanistic interaction rules remain `ADD_CANDIDATE`.

## Model feedback

1. 六煞不能编码成统一负分。源文明示火羊、铃陀在特定组合中可由煞转为激发或磨炼。
2. 擎羊/陀罗需要区分明面破坏与暗面拖延；火星/铃星也分别偏明、暗，不能合并成单一“煞强度”。
3. 地空/地劫的主要作用域不同：前者偏精神打击与幻想，后者偏物质损失与反传统行为。
4. 多个规则属于 pair interaction / gate：火羊、铃陀、羊铃、火陀、羊陀夹、火铃夹等均不是单星线性叠加。
5. 宫位和正曜条件决定煞曜是激发、磨炼、破格还是投影到具体事件，因此仍支持状态依赖的非线性 operator。

## History feedback

MAL01-017 的源文明确称大运行四墓擎羊宫度时，经历坎坷后可“对后运发生良好影响”。这构成跨期路径依赖证据，已记录为：

- proposed transition: `HG-027`
- memory kind: `PATH_DEPENDENT_GATE`
- action: `ADD_AFTER_OPERATOR_NORMALIZATION`

它沿用 A2-R1 既有记忆类型，不触发新 Human Gate，也不引入持续年数、衰减率或连续增益。

## Chapter closure

六煞 81 条 legacy operator rules 已全部完成 source-span review。下一步执行 WP04 全局 closure audit。
